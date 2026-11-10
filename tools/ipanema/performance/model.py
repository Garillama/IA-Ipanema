"""Proyecciones observadas; laboratorio, campo y comparabilidad sin puntuación inventada."""
from __future__ import annotations
import copy
import datetime as dt
import math
import re
import statistics
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit, quote, unquote

CATEGORIES = ('performance', 'accessibility', 'best-practices', 'seo')
LAB_METRICS = {'lcp': 'largest-contentful-paint', 'fcp': 'first-contentful-paint',
               'cls': 'cumulative-layout-shift', 'tbt': 'total-blocking-time', 'speed_index': 'speed-index'}
FIELD_METRICS = {'lcp': 'largest_contentful_paint', 'inp': 'interaction_to_next_paint',
                 'cls': 'cumulative_layout_shift', 'fcp': 'first_contentful_paint'}
SENSITIVE = re.compile(r'key|token|secret|password|cookie|authorization|session|email|phone|snippet|nodeLabel|headers|postData', re.I)


def numeric(value):
    if isinstance(value, bool):
        return None
    try:
        number = float(value)
        return number if math.isfinite(number) else None
    except (ValueError, TypeError):
        return None


def sanitize(value, secrets=(), key=''):
    """Keep public observations, never transport URLs, headers, node HTML or key echoes."""
    identity_key = key == 'key' and isinstance(value, dict) and set(value) <= {'url','origin','formFactor'}
    if not identity_key and SENSITIVE.search(unquote(unquote(key))):
        return '[redacted]'
    if isinstance(value, dict):
        return {sanitize(str(k), secrets): sanitize(v, secrets, str(k)) for k, v in value.items()}
    if isinstance(value, list):
        return [sanitize(v, secrets) for v in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if not isinstance(value, str):
        return value
    for secret in secrets:
        if secret:
            for version in (secret, quote(secret, safe=''), quote(quote(secret, safe=''), safe='')):
                value = value.replace(version, '[redacted]')
    if value.startswith('data:'):
        return '[inline-resource]'
    def clean(match):
        try:
            u = urlsplit(match.group(0))
            host = u.hostname or ''
            netloc = ('[' + host + ']' if ':' in host else host) + (':' + str(u.port) if u.port else '')
            query = [(k, '[redacted]' if SENSITIVE.search(unquote(unquote(k))) else v) for k, v in parse_qsl(u.query)]
            return urlunsplit((u.scheme, netloc, u.path, urlencode(query), ''))
        except ValueError:
            return '[invalid-url]'
    return re.sub(r'https?://[^\s<>"\]]+', clean, value)


def lighthouse(payload, request, *, source='pagespeed'):
    lhr = payload.get('lighthouseResult', {}) if source == 'pagespeed' else payload
    if not isinstance(lhr, dict):
        return {'status': 'invalid_response', 'source': source}
    audits = lhr.get('audits') or {}
    categories = lhr.get('categories') or {}
    metrics = {k: numeric((audits.get(v) or {}).get('numericValue')) for k, v in LAB_METRICS.items()}
    scores = {k: numeric((categories.get(k) or {}).get('score')) for k in request['categories']}
    settings = lhr.get('configSettings') or {}
    ua = ((lhr.get('environment') or {}).get('actualBrowserVersion') if source == 'lighthouse_local' else None) or (lhr.get('environment') or {}).get('hostUserAgent') or lhr.get('userAgent') or ''
    chrome = re.search(r'(?:HeadlessChrome|Chrome)/([\d.]+)', ua)
    profile = {'source': source, 'url': request['url'],
               'final_url': lhr.get('finalDisplayedUrl') or lhr.get('finalUrl'),
               'device': request['device'], 'categories': request['categories'], 'locale': request['locale'],
               'lighthouse_version': lhr.get('lighthouseVersion'), 'chrome_version': chrome.group(1) if chrome and not chrome.group(1).endswith('.0.0.0') else None,
               'screen': settings.get('screenEmulation'), 'throttling_method': settings.get('throttlingMethod'),
               'throttling': settings.get('throttling'), 'cache': settings.get('disableStorageReset'),
               'network_policy': request.get('network_policy', 'google-managed')}
    # Missing requested metrics/categories never become zero or a complete success.
    missing = [k for k, v in metrics.items() if v is None] + ['category:' + k for k, v in scores.items() if v is None]
    observed = {k: lhr.get(k) for k in ('requestedUrl','finalUrl','finalDisplayedUrl','fetchTime',
                'lighthouseVersion','configSettings','environment','categories','runWarnings','runtimeError')}
    observed['audits'] = {k: {field: a[field] for field in ('id','title','description','score','scoreDisplayMode',
        'numericValue','numericUnit','displayValue','details','errorMessage') if field in a}
        for k, a in audits.items() if isinstance(a, dict)}
    return {'source': source, 'measurement': 'laboratory', 'status': 'runtime_error' if lhr.get('runtimeError') else 'partial' if missing else 'observed',
            'measured_at': lhr.get('fetchTime') or payload.get('analysisUTCTimestamp'),
            'metrics': metrics, 'units': {k: 'unitless' if k == 'cls' else 'ms' for k in metrics},
            'scores': scores, 'profile': profile, 'missing': missing,
            'observations': observed, 'warnings': lhr.get('runWarnings') or [],
            'runtime_error': lhr.get('runtimeError'), 'field_inp': None,
            'limitations': ['Laboratorio; TBT no mide INP. Scores no certifican SEO/WCAG.',
                            'PSI no mide cambios locales sin una URL publicada accesible.']}


def crux(payload, request):
    record = payload.get('record')
    if not isinstance(record, dict) or not isinstance(record.get('key'), dict):
        return {'status': 'invalid_response', 'source': request['source']}
    identity = record['key']
    scope = request['scope']
    expected = request['url'] if scope == 'url' else request['origin']
    returned = identity.get(scope)
    normalized = payload.get('urlNormalizationDetails') or {}
    identity_matches = returned == expected
    if scope == 'url' and not identity_matches:
        identity_matches = normalized.get('originalUrl') == expected and normalized.get('normalizedUrl') == returned
    if not identity_matches or identity.get('formFactor') != request['form_factor'] or ('origin' if scope == 'url' else 'url') in identity:
        return {'status': 'identity_mismatch', 'source': request['source'], 'requested_identity': {scope: expected, 'formFactor': request['form_factor']}}
    history = request['source'] == 'crux_history'
    periods = record.get('collectionPeriods') if history else record.get('collectionPeriod')
    if periods is not None:
        try:
            ordered = []
            for period in periods if history else [periods]:
                first = dt.date(**period['firstDate'])
                last = dt.date(**period['lastDate'])
                if first > last or ordered and last <= ordered[-1]:
                    raise ValueError('invalid_period')
                ordered.append(last)
        except (TypeError, KeyError, ValueError):
            return {'status': 'invalid_response', 'source': request['source']}
    metrics = {}
    incomplete = []
    for name, field in FIELD_METRICS.items():
        item = (record.get('metrics') or {}).get(field)
        if not isinstance(item, dict):
            continue
        if history:
            p75s = (item.get('percentilesTimeseries') or {}).get('p75s')
            bins = item.get('histogramTimeseries')
            if (not isinstance(periods, list) or not isinstance(p75s, list) or len(p75s) != len(periods)
                    or not isinstance(bins, list) or any(not isinstance(b.get('densities'), list) or len(b['densities']) != len(periods) for b in bins)):
                return {'status': 'invalid_response', 'source': request['source']}
            metrics[name] = {'p75s': [numeric(v) for v in p75s], 'histogram_timeseries':
                             [{**b, 'densities': [numeric(v) for v in b['densities']]} for b in bins]}
            if any(numeric(v) is None for v in p75s) or any(numeric(v) is None for b in bins for v in b['densities']):
                incomplete.append(name + ':nullable_history')
        else:
            metrics[name] = {'p75': numeric((item.get('percentiles') or {}).get('p75')), 'histogram': item.get('histogram')}
            if metrics[name]['p75'] is None or not isinstance(item.get('histogram'), list) or not item['histogram']:
                incomplete.append(name + ':missing_values')
        metrics[name]['unit'] = 'unitless' if name == 'cls' else 'ms'
    missing = sorted(set(FIELD_METRICS) - set(metrics)) + incomplete
    return {'source': request['source'], 'status': 'partial' if missing or not periods else 'observed',
            'measurement': 'field_history' if history else 'field', 'scope': scope,
            'requested_identity': {scope: expected, 'formFactor': request['form_factor']}, 'returned_identity': identity,
            'collection_periods' if history else 'collection_period': periods,
            'metrics': metrics, 'missing': missing, 'observations': payload,
            'limitations': ['Periodos agregados de usuarios reales; sin causalidad inmediata.',
                            'Origen no representa una URL individual. No hay fallback silencioso.']}


def compare(before, after, *, profile_only=False):
    if before.get('source') != after.get('source') or before.get('measurement') != 'laboratory' or after.get('measurement') != 'laboratory':
        return {'status': 'not_comparable', 'reason': 'Solo laboratorio de la misma fuente; CrUX conserva periodos, no certifica mejoras inmediatas.'}
    required = ('source','url','final_url','device','categories','locale','lighthouse_version','chrome_version',
                'screen','throttling_method','throttling','cache','network_policy')
    a, b = before.get('profile', {}), after.get('profile', {})
    invalid = [k for k in required if a.get(k) is None or b.get(k) is None or a.get(k) != b.get(k)]
    if before.get('sample_count', 1) != after.get('sample_count', 1):
        invalid.append('sample_count')
    if before.get('status') != 'observed' or after.get('status') != 'observed':
        invalid.append('status')
    if invalid:
        return {'status': 'not_comparable', 'fields': invalid}
    if not profile_only and (not before.get('measured_at') or not after.get('measured_at') or before['measured_at'] == after['measured_at']):
        return {'status': 'not_comparable', 'reason': 'Se necesitan observaciones distintas y fechadas; la caché no es una medición nueva.'}
    delta = {k: after['metrics'][k] - value for k, value in before.get('metrics', {}).items()
             if numeric(value) is not None and numeric(after.get('metrics', {}).get(k)) is not None}
    return {'status': 'compared', 'delta_after_minus_before': delta,
            'regressions': [k for k, v in delta.items() if v > 0], 'causality_confirmed': False}


def summarize(samples):
    if not samples:
        return {'status': 'not_measured'}
    profiles = [s.get('profile') for s in samples]
    if compare(samples[0], samples[0], profile_only=True).get('status') != 'compared':
        return {'status': 'not_comparable', 'samples': samples}
    if any(p != profiles[0] for p in profiles) or any(s.get('status') != 'observed' for s in samples):
        return {'status': 'not_comparable', 'samples': samples}
    summary = copy.deepcopy(samples[0])
    summary.update(sample_count=len(samples), samples=samples, statistics={})
    for name in LAB_METRICS:
        values = [s['metrics'].get(name) for s in samples if numeric(s.get('metrics', {}).get(name)) is not None]
        summary['statistics'][name] = {'median': statistics.median(values) if values else None,
                                      'min': min(values) if values else None, 'max': max(values) if values else None,
                                      'available_samples': len(values)}
        summary['metrics'][name] = summary['statistics'][name]['median']
    return summary


def findings(result, url, device):
    rows = []
    for name, audit in result.get('observations', {}).get('audits', {}).items():
        score = numeric(audit.get('score'))
        if score is None or score >= 1:
            continue
        rows.append({'id': 'PERF-' + name, 'source': result['source'], 'url': url, 'device': device,
                     'metric_affected': [k for k, v in LAB_METRICS.items() if v == name] or ['requires_diagnosis'],
                     'evidence': {'audit': name, 'score': score, 'details': audit.get('details')},
                     'cause_state': 'hypothesis', 'severity': 'review_required',
                     'potential_impact': 'No cuantificado; comprobar recurso, interacción y consumidores.',
                     'candidate_files': [], 'consumers': [], 'alternatives': ['Inspeccionar motor/componente nativo y confirmar causa antes de cambiar.'],
                     'risks': ['Regresión fuera del alcance de una auditoría automática.'], 'estimated_cost': None,
                     'required_tests': ['Perfil comparable antes/después', 'QA funcional, SEO, accesibilidad y revisión independiente']})
    return rows
