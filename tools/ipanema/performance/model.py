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


CWV_THRESHOLDS = {
    'ttfb': (800.0, 1800.0, 'ms'),
    'fcp': (1800.0, 3000.0, 'ms'),
    'lcp': (2500.0, 4000.0, 'ms'),
    'inp': (200.0, 500.0, 'ms'),
    'tbt': (200.0, 600.0, 'ms'),
    'cls': (0.1, 0.25, 'unitless'),
    'speed_index': (3400.0, 5800.0, 'ms'),
}


def rate_metric(metric: str, value) -> str:
    num = numeric(value)
    if num is None or metric not in CWV_THRESHOLDS or num < 0:
        return 'not_measured'
    good_max, poor_min, _ = CWV_THRESHOLDS[metric]
    if num <= good_max:
        return 'good'
    if num <= poor_min:
        return 'needs-improvement'
    return 'poor'


def _extract_origin(url: str) -> str | None:
    if not isinstance(url, str) or not url.startswith(('http://', 'https://')):
        return None
    try:
        u = urlsplit(url)
        return f'{u.scheme}://{u.netloc}' if u.hostname else None
    except ValueError:
        return None


def diagnose_web_perf(payload: dict, *, network_records: list | None = None, rendered: dict | None = None, preconnect_origins: list | None = None) -> dict:
    """Diagnóstico Cloudflare Web Performance: separa campo/laboratorio, filtra 0ms y analiza red/imágenes."""
    sources = payload.get('sources') if isinstance(payload.get('sources'), dict) else {}
    if not sources and isinstance(payload.get('measurement'), str):
        sources = {payload.get('source', 'primary'): payload}

    field_summary = {}
    lab_summary = {}
    audits = {}

    for src_name, src in sources.items():
        if not isinstance(src, dict):
            continue
        kind = src.get('measurement')
        if kind == 'field':
            for m, data in (src.get('metrics') or {}).items():
                val = numeric(data.get('p75')) if isinstance(data, dict) else numeric(data)
                field_summary[m] = {
                    'value': val,
                    'unit': CWV_THRESHOLDS.get(m, (0, 0, 'ms'))[2],
                    'rating': rate_metric(m, val),
                    'source': src_name,
                }
        elif kind in ('laboratory', 'lighthouse-laboratory'):
            obs_audits = (src.get('observations') or {}).get('audits') or src.get('audits') or {}
            if isinstance(obs_audits, dict) and not audits:
                audits = obs_audits
            metrics = dict(src.get('metrics') or {})
            if metrics.get('ttfb') is None:
                srv = obs_audits.get('server-response-time') or {}
                lcp_b = ((obs_audits.get('lcp-breakdown-insight') or {}).get('details') or {}).get('items') or []
                metrics['ttfb'] = numeric(srv.get('numericValue'))
                if metrics['ttfb'] is None and lcp_b and isinstance(lcp_b[0], dict):
                    metrics['ttfb'] = numeric(lcp_b[0].get('ttfb'))
            for m in ('ttfb', 'fcp', 'lcp', 'tbt', 'cls', 'speed_index'):
                val = numeric(metrics.get(m))
                lab_summary[m] = {
                    'value': val,
                    'unit': CWV_THRESHOLDS[m][2],
                    'rating': rate_metric(m, val),
                    'source': src_name,
                }

    if rendered and isinstance(rendered, dict):
        nav = rendered.get('navigation') or []
        if nav and isinstance(nav[0], dict) and ('ttfb' not in lab_summary or lab_summary['ttfb']['value'] is None):
            req_s = numeric(nav[0].get('requestStart'))
            res_s = numeric(nav[0].get('responseStart'))
            if req_s is not None and res_s is not None and res_s >= req_s:
                ttfb_val = round(res_s - req_s, 2)
                lab_summary['ttfb'] = {'value': ttfb_val, 'unit': 'ms', 'rating': rate_metric('ttfb', ttfb_val), 'source': 'navigation_timing'}

    # 1. Render-blocking resources (skip 0ms impact per Cloudflare web-perf guideline)
    rb_audit = audits.get('render-blocking-resources') or audits.get('render-blocking-insight') or {}
    rb_items = ((rb_audit.get('details') or {}).get('items')) or []
    actionable_rb, skipped_zero_rb = [], []
    for item in rb_items:
        if not isinstance(item, dict):
            continue
        wasted_ms = numeric(item.get('wastedMs')) or 0.0
        entry = {
            'url': sanitize(item.get('url', '')),
            'wasted_ms': wasted_ms,
            'total_bytes': numeric(item.get('totalBytes')),
        }
        if wasted_ms > 0:
            actionable_rb.append(entry)
        else:
            skipped_zero_rb.append(entry)
    actionable_rb.sort(key=lambda r: r['wasted_ms'], reverse=True)

    # 2. Network analysis: duplicate resources, redirects, unused preconnects
    net_rows = list(network_records or [])
    if not net_rows:
        net_audit_items = (((audits.get('network-requests') or {}).get('details') or {}).get('items')) or []
        for item in net_audit_items:
            if isinstance(item, dict) and item.get('url'):
                net_rows.append({
                    'url': item.get('url'),
                    'type': item.get('resourceType'),
                    'status': item.get('statusCode'),
                    'encoded_bytes': numeric(item.get('transferSize')),
                    'redirect_hop': 0,
                })
    url_counts = {}
    redirects = []
    observed_origins = set()
    large_resources = []
    for row in net_rows:
        if not isinstance(row, dict):
            continue
        clean_u = sanitize(row.get('url', ''))
        orig = _extract_origin(clean_u)
        if orig:
            observed_origins.add(orig)
        if row.get('redirect') or (numeric(row.get('redirect_hop')) or 0) > 0:
            redirects.append({'url': clean_u, 'hop': row.get('redirect_hop', 0), 'status': row.get('status')})
        else:
            if clean_u:
                url_counts[clean_u] = url_counts.get(clean_u, 0) + 1
            size = numeric(row.get('encoded_bytes'))
            if size is not None and size >= 150_000:
                large_resources.append({'url': clean_u, 'type': row.get('type'), 'encoded_bytes': size})

    duplicate_resources = [{'url': u, 'count': c} for u, c in sorted(url_counts.items()) if c > 1]
    large_resources.sort(key=lambda r: r['encoded_bytes'], reverse=True)

    declared_preconnects = set()
    for orig in (preconnect_origins or []):
        extracted = _extract_origin(orig) or orig
        if isinstance(extracted, str) and extracted:
            declared_preconnects.add(extracted)
    unused_preconnects = sorted(o for o in declared_preconnects if o not in observed_origins)
    verified_preconnects = sorted(o for o in declared_preconnects if o in observed_origins)

    # 3. Network dependency chains & LCP breakdown
    lcp_breakdown_items = (((audits.get('lcp-breakdown-insight') or {}).get('details') or {}).get('items')) or []
    lcp_breakdown = lcp_breakdown_items[0] if lcp_breakdown_items and isinstance(lcp_breakdown_items[0], dict) else None
    lcp_discovery_items = (((audits.get('lcp-discovery-insight') or {}).get('details') or {}).get('items')) or []
    chains_details = (audits.get('critical-request-chains') or audits.get('network-dependency-tree-insight') or {}).get('details') or {}

    # 4. Responsive images and loading priorities
    image_issues = {'lcp_lazy_loaded': False, 'lcp_missing_high_priority': False, 'unsized_images': [], 'oversized_images': []}
    if rendered and isinstance(rendered, dict):
        perf_obs = rendered.get('performance') or {}
        lcp_entries = perf_obs.get('lcp') or []
        if lcp_entries and isinstance(lcp_entries[-1], dict):
            last_lcp = lcp_entries[-1]
            if last_lcp.get('tag') == 'IMG':
                if str(last_lcp.get('loading') or '').lower() == 'lazy':
                    image_issues['lcp_lazy_loaded'] = True
                if str(last_lcp.get('fetchPriority') or '').lower() != 'high':
                    image_issues['lcp_missing_high_priority'] = True
        for img in rendered.get('images') or []:
            if not isinstance(img, dict):
                continue
            src = sanitize(img.get('currentSrc') or img.get('src') or '')
            w, h = numeric(img.get('width')), numeric(img.get('height'))
            nw = numeric(img.get('naturalWidth'))
            if img.get('visible') and (not w or not h):
                image_issues['unsized_images'].append({'src': src, 'width': w, 'height': h})
            if w and nw and nw > w * 1.5 and (nw - w) >= 200:
                image_issues['oversized_images'].append({
                    'src': src,
                    'rendered_width': w,
                    'natural_width': nw,
                    'has_srcset': bool(img.get('srcset')),
                    'sizes': img.get('sizes'),
                })

    return {
        'skill': 'cloudflare-web-perf',
        'field_vs_lab_separated': True,
        'field_metrics': field_summary,
        'lab_metrics': lab_summary,
        'render_blocking': {
            'actionable': actionable_rb,
            'zero_impact_skipped': skipped_zero_rb,
        },
        'network': {
            'duplicate_resources': duplicate_resources,
            'redirects': redirects,
            'large_resources': large_resources,
            'unused_preconnects': unused_preconnects,
            'verified_preconnects': verified_preconnects,
            'lcp_breakdown': lcp_breakdown,
            'lcp_discovery': lcp_discovery_items,
            'dependency_chains_present': bool(chains_details),
        },
        'images': image_issues,
        'limitations': [
            'TBT es métrica de laboratorio y nunca sustituye a INP de campo.',
            'Recursos con 0ms de impacto estimado se registran pero no se recomiendan como cambios.',
        ],
    }
