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


FRAMEWORK_CANDIDATES = {
    'shopify-liquid': {
        'performance': ['layout/theme.liquid', 'sections/hero.liquid', 'snippets/image.liquid'],
        'accessibility': ['layout/theme.liquid', 'sections/header.liquid', 'snippets/product-card.liquid'],
        'seo': ['layout/theme.liquid', 'templates/product.json', 'sections/main-product.liquid'],
        'best-practices': ['layout/theme.liquid', 'config/settings_schema.json'],
        'interaction': ['assets/global.js', 'sections/header.liquid'],
    },
    'shopify-hydrogen': {
        'performance': ['app/root.tsx', 'app/routes/_index.tsx', 'vite.config.ts'],
        'accessibility': ['app/root.tsx', 'app/components/Header.tsx'],
        'seo': ['app/root.tsx', 'app/routes/products.$handle.tsx'],
        'best-practices': ['app/entry.server.tsx', 'vite.config.ts'],
        'interaction': ['app/components/CartMain.tsx', 'app/root.tsx'],
    },
    'react-web': {
        'performance': ['index.html', 'vite.config.ts', 'src/App.tsx'],
        'accessibility': ['index.html', 'src/App.tsx'],
        'seo': ['index.html', 'src/main.tsx'],
        'best-practices': ['index.html', 'package.json'],
        'interaction': ['src/App.tsx'],
    },
    'tiendanube-ipanema': {
        'performance': ['layouts/layout.tpl', 'sections/hero.tpl', 'snippets/image.tpl'],
        'accessibility': ['layouts/layout.tpl', 'snippets/product-list/product-item/item.tpl'],
        'seo': ['layouts/layout.tpl', 'templates/product.tpl'],
        'best-practices': ['layouts/layout.tpl', 'config/settings_schema.json'],
        'interaction': ['static/js/store.js.tpl', 'layouts/layout.tpl'],
    },
}

GENERIC_LINK_LABELS = frozenset({
    'click here', 'read more', 'learn more', 'more', 'here', 'link',
    'clic aqui', 'clic aquí', 'leer mas', 'leer más', 'ver mas', 'ver más', 'aqui', 'aquí',
})


def infer_framework(framework: str | None = None, source_files: dict[str, str] | None = None) -> str:
    if framework in (*FRAMEWORK_CANDIDATES, 'remix', 'nextjs'):
        return framework
    paths = [p.lower() for p in (source_files or {})]
    joined = ' '.join(paths)
    contents = ' '.join((source_files or {}).values()).lower()
    if any(p.endswith('.liquid') for p in paths) or 'content_for_header' in contents:
        return 'shopify-liquid'
    if '@shopify/hydrogen' in contents or ('app/routes/' in joined and 'storefront' in contents):
        return 'shopify-hydrogen'
    if '@remix-run/' in contents or ('app/routes/' in joined and 'loader' in contents and '@shopify/hydrogen' not in contents):
        return 'remix'
    if 'next/dynamic' in contents or 'next/server' in contents or 'next/image' in contents or 'next.config' in joined:
        return 'nextjs'
    if any(p.endswith(('.tsx', '.jsx')) for p in paths) and 'app/routes/' in joined:
        return 'shopify-hydrogen'
    if any(p.endswith('.tpl') for p in paths) or 'snippets/image.tpl' in joined:
        return 'tiendanube-ipanema'
    if any(p.endswith(('.tsx', '.jsx')) for p in paths) or 'from "react"' in contents or "from 'react'" in contents or 'vite.config' in joined or 'webpack.config' in joined:
        return 'react-web'
    return framework or 'tiendanube-ipanema'


def audit_web_quality(
    payload: dict | None = None,
    *,
    network_records: list | None = None,
    rendered: dict | None = None,
    console_messages: list | None = None,
    source_files: dict[str, str] | None = None,
    preconnect_origins: list | None = None,
    framework: str | None = None,
) -> dict:
    """Auditoría integral Web Quality Audit: reutiliza diagnose_web_perf y separa evidencia de hipótesis."""
    data = payload if isinstance(payload, dict) else {}
    detected_fw = infer_framework(framework, source_files)
    candidates_map = FRAMEWORK_CANDIDATES.get(detected_fw, FRAMEWORK_CANDIDATES['tiendanube-ipanema'])

    # Reutilizar directamente el motor de Cloudflare Web Performance sin duplicar cálculos
    perf = diagnose_web_perf(
        data,
        network_records=network_records,
        rendered=rendered,
        preconnect_origins=preconnect_origins,
    )

    verified_issues = []
    code_hypotheses = []

    def add_verified(issue_id, category, severity, title, impact, evidence, fix, files=None):
        verified_issues.append({
            'id': issue_id,
            'category': category,
            'severity': severity,
            'confidence': 'high',
            'evidence_type': 'verified_by_tool',
            'title': title,
            'impact': impact,
            'evidence': sanitize(evidence),
            'candidate_files': files or candidates_map.get(category, []),
            'fix': fix,
        })

    def add_hypothesis(issue_id, category, severity, title, impact, evidence, fix, files):
        code_hypotheses.append({
            'id': issue_id,
            'category': category,
            'severity': severity,
            'confidence': 'medium',
            'evidence_type': 'code_hypothesis',
            'title': title,
            'impact': impact,
            'evidence': sanitize(evidence),
            'candidate_files': files,
            'fix': fix,
        })

    # 1. Performance (delegado en cloudflare-web-perf)
    for m_name, m_info in perf['field_metrics'].items():
        if m_info['rating'] in ('poor', 'needs-improvement'):
            sev = 'high' if m_info['rating'] == 'poor' else 'medium'
            add_verified(
                f'WQA-PERF-FIELD-{m_name.upper()}',
                'performance',
                sev,
                f'Métrica de campo {m_name.upper()} en estado {m_info["rating"]} ({m_info["value"]} {m_info["unit"]})',
                'Afecta directamente la experiencia de usuarios reales (CrUX p75).',
                m_info,
                f'Optimizar {m_name.upper()} siguiendo el desglose de cloudflare-web-perf.',
            )
    for m_name, m_info in perf['lab_metrics'].items():
        if m_info['rating'] in ('poor', 'needs-improvement'):
            sev = 'high' if m_info['rating'] == 'poor' else 'medium'
            add_verified(
                f'WQA-PERF-LAB-{m_name.upper()}',
                'performance',
                sev,
                f'Métrica de laboratorio {m_name.upper()} en estado {m_info["rating"]} ({m_info["value"]} {m_info["unit"]})',
                'Retrasa la carga o bloquea el hilo principal en laboratorio.',
                m_info,
                f'Reducir {m_name.upper()} eliminando bloqueos o recursos pesados.',
            )
    for rb in perf['render_blocking']['actionable']:
        sev = 'high' if rb['wasted_ms'] >= 300 else 'medium'
        add_verified(
            'WQA-PERF-RENDER-BLOCKING',
            'performance',
            sev,
            f'Recurso bloqueante de renderizado ({rb["wasted_ms"]} ms)',
            f'Retrasa FCP/LCP en aproximadamente {rb["wasted_ms"]} ms.',
            rb,
            'Añadir defer/async al script o extraer CSS crítico y diferir el resto.',
        )
    if perf['images']['lcp_lazy_loaded']:
        add_verified(
            'WQA-PERF-LCP-LAZY',
            'performance',
            'high',
            'Imagen LCP tiene loading="lazy"',
            'Retrasa el descubrimiento y la descarga del elemento principal de la página.',
            {'lcp_lazy_loaded': True},
            'Usar loading="eager" y fetchpriority="high" en la imagen LCP.',
        )
    if perf['images']['lcp_missing_high_priority']:
        add_verified(
            'WQA-PERF-LCP-PRIORITY',
            'performance',
            'medium',
            'Imagen LCP sin fetchpriority="high"',
            'El navegador puede no priorizar la imagen principal frente a otros activos.',
            {'lcp_missing_high_priority': True},
            'Añadir fetchpriority="high" al elemento <img> del LCP.',
        )

    # Extraer scores de categorías Lighthouse si existen
    sources = data.get('sources') if isinstance(data.get('sources'), dict) else {}
    if not sources and isinstance(data.get('measurement'), str):
        sources = {data.get('source', 'primary'): data}
    category_scores = {}
    for src in sources.values():
        if isinstance(src, dict) and isinstance(src.get('scores'), dict):
            for k, v in src['scores'].items():
                if numeric(v) is not None:
                    category_scores[k] = numeric(v)

    # 2. Accessibility, 3. SEO, 4. Best Practices, 5. Interaction & Rendered HTML
    if isinstance(rendered, dict):
        lang = str(rendered.get('lang') or '').strip()
        if not lang:
            add_verified(
                'WQA-A11Y-MISSING-LANG',
                'accessibility',
                'high',
                'Elemento <html> sin atributo lang válido',
                'Los lectores de pantalla no pueden determinar el idioma de lectura.',
                {'lang': rendered.get('lang')},
                'Definir el atributo lang en la etiqueta raíz <html lang="es">.',
            )
        for img in rendered.get('images') or []:
            if not isinstance(img, dict):
                continue
            if img.get('alt') is None:
                add_verified(
                    'WQA-A11Y-IMG-MISSING-ALT',
                    'accessibility',
                    'high',
                    'Imagen renderizada sin atributo alt',
                    'Usuarios de tecnologías de asistencia no reciben alternativa textual.',
                    {'src': img.get('currentSrc') or img.get('src')},
                    'Añadir alt descriptivo o alt="" si la imagen es puramente decorativa.',
                )
        for form in rendered.get('forms') or []:
            if not isinstance(form, dict):
                continue
            for inp in form.get('inputs') or []:
                if not isinstance(inp, dict):
                    continue
                itype = str(inp.get('type') or '').lower()
                if itype in ('hidden', 'submit', 'button', 'reset', 'image'):
                    continue
                if not inp.get('hasLabel') and not inp.get('ariaLabel'):
                    add_verified(
                        'WQA-A11Y-FORM-UNLABELED',
                        'accessibility',
                        'high',
                        'Campo de formulario sin etiqueta <label> ni aria-label',
                        'Impide identificar el propósito del campo con lector de pantalla o navegación asistida.',
                        {'tag': inp.get('tag'), 'type': itype, 'name': inp.get('name')},
                        'Asociar un elemento <label for="..."> explícito o atributo aria-label.',
                    )
        axe_violations = (rendered.get('axe') or {}).get('violations') or []
        for v in axe_violations:
            if isinstance(v, dict):
                impact_map = {'critical': 'critical', 'serious': 'high', 'moderate': 'medium', 'minor': 'low'}
                sev = impact_map.get(str(v.get('impact') or '').lower(), 'medium')
                add_verified(
                    'WQA-A11Y-AXE-' + str(v.get('id') or 'VIOLATION').upper(),
                    'accessibility',
                    sev,
                    f'Violación axe-core: {v.get("id")}',
                    v.get('description') or v.get('help') or 'Barrera de accesibilidad detectada por axe-core.',
                    {'id': v.get('id'), 'impact': v.get('impact')},
                    v.get('help') or 'Corregir estructura semántica o contraste según regla WCAG.',
                )

        # SEO sobre DOM renderizado
        title = str(rendered.get('title') or '').strip()
        if not title:
            add_verified(
                'WQA-SEO-MISSING-TITLE',
                'seo',
                'high',
                'Página renderizada sin etiqueta <title>',
                'Afecta la identificación del documento en pestañas, historial y resultados de búsqueda.',
                {'title': rendered.get('title')},
                'Incluir un <title> único y descriptivo en <head>.',
            )
        meta_list = [m for m in (rendered.get('metadata') or []) if isinstance(m, dict)]
        has_desc = any(str(m.get('name') or '').lower() == 'description' and str(m.get('content') or '').strip() for m in meta_list)
        if not has_desc:
            add_verified(
                'WQA-SEO-MISSING-DESCRIPTION',
                'seo',
                'medium',
                'Página sin meta description',
                'Reduce el control sobre el resumen descriptivo de la página.',
                {'metadata_count': len(meta_list)},
                'Añadir <meta name="description" content="..."> específico para la plantilla.',
            )
        has_canonical = any(str(m.get('name') or '').lower() == 'canonical' and str(m.get('href') or '').strip() for m in meta_list)
        if not has_canonical:
            add_verified(
                'WQA-SEO-MISSING-CANONICAL',
                'seo',
                'medium',
                'Página sin enlace canonical',
                'Dificulta la consolidación de URLs duplicadas o con parámetros.',
                {'canonical_present': False},
                'Añadir <link rel="canonical" href="..."> con la URL canónica autorizada.',
            )
        for m in meta_list:
            if str(m.get('name') or '').lower() == 'robots' and 'noindex' in str(m.get('content') or '').lower():
                add_verified(
                    'WQA-SEO-NOINDEX-DETECTED',
                    'seo',
                    'critical',
                    'Directiva noindex detectada en meta robots',
                    'Impide que los motores de búsqueda indexen la página si es una ruta pública comercial.',
                    {'robots': m.get('content')},
                    'Verificar si la página debe indexarse y retirar noindex si es accidental.',
                )
        headings = [h for h in (rendered.get('headings') or []) if isinstance(h, dict)]
        h1s = [h for h in headings if str(h.get('tag') or '').upper() == 'H1' and str(h.get('text') or '').strip()]
        if not h1s:
            add_verified(
                'WQA-SEO-MISSING-H1',
                'seo',
                'medium',
                'Página sin encabezado principal <h1> con texto',
                'Debilita la jerarquía semántica del contenido principal.',
                {'headings_count': len(headings)},
                'Asegurar un encabezado <h1> descriptivo para el contenido primario.',
            )
        for link in rendered.get('links') or []:
            if not isinstance(link, dict):
                continue
            ltext = str(link.get('text') or '').strip()
            aria = str(link.get('ariaLabel') or '').strip()
            effective = (ltext or aria).lower()
            if not effective:
                add_verified(
                    'WQA-INT-EMPTY-LINK',
                    'interaction',
                    'high',
                    'Enlace interactivo sin texto ni aria-label',
                    'Inaccesible para lectores de pantalla y navegación agéntica.',
                    {'href': link.get('href')},
                    'Añadir texto visible descriptivo o atributo aria-label al enlace.',
                )
            elif effective in GENERIC_LINK_LABELS:
                add_verified(
                    'WQA-SEO-GENERIC-LINK-TEXT',
                    'seo',
                    'low',
                    f'Texto de enlace genérico ("{ltext or aria}")',
                    'Aporta poco contexto semántico a usuarios con lectores de pantalla y buscadores.',
                    {'href': link.get('href'), 'text': ltext or aria},
                    'Reemplazar por un texto que describa el destino del enlace.',
                )
        for jld in rendered.get('jsonld') or []:
            if isinstance(jld, dict) and jld.get('error'):
                add_verified(
                    'WQA-SEO-INVALID-JSONLD',
                    'seo',
                    'high',
                    'Bloque JSON-LD con error de sintaxis',
                    'Impide el procesamiento de datos estructurados.',
                    {'component': jld.get('component'), 'error': jld.get('error')},
                    'Corregir el JSON-LD generado en la plantilla para que sea JSON válido.',
                )

        # Interaction / Layout stability
        vp = rendered.get('viewport') or {}
        iw, sw = numeric(vp.get('innerWidth')), numeric(vp.get('scrollWidth'))
        if iw and sw and sw > iw:
            add_verified(
                'WQA-INT-HORIZONTAL-OVERFLOW',
                'interaction',
                'high',
                f'Desbordamiento horizontal detectado (scrollWidth {int(sw)}px > innerWidth {int(iw)}px)',
                'Rompe la navegación táctil y el layout móvil/responsivo.',
                {'innerWidth': iw, 'scrollWidth': sw},
                'Inspeccionar elementos con ancho fijo o márgenes negativos fuera del contenedor.',
            )

    # 4. Best Practices (Consola, HTTPS, Source Maps)
    for msg in (console_messages or []):
        if isinstance(msg, dict) and str(msg.get('type') or msg.get('level') or '').lower() == 'error':
            add_verified(
                'WQA-BP-CONSOLE-ERROR',
                'best-practices',
                'high',
                'Error de ejecución en consola del navegador',
                'Puede interrumpir interacciones de usuario, carrito o componentes dinámicos.',
                {'text': msg.get('text') or msg.get('message')},
                'Depurar y corregir la excepción JavaScript o recurso fallido.',
            )
    for row in (network_records or []):
        if not isinstance(row, dict):
            continue
        r_url = sanitize(str(row.get('url') or ''))
        if r_url.startswith('http://') and not any(h in r_url for h in ('http://127.0.0.1', 'http://localhost', 'http://[::1]')):
            add_verified(
                'WQA-BP-INSECURE-HTTP-RESOURCE',
                'best-practices',
                'critical',
                'Solicitud de red insegura por HTTP (contenido mixto)',
                'Compromete la seguridad del documento HTTPS y puede ser bloqueada por el navegador.',
                {'url': r_url, 'type': row.get('type')},
                'Actualizar la referencia del recurso a HTTPS.',
            )
        if r_url.split('?', 1)[0].endswith('.map') and row.get('status') == 200:
            add_verified(
                'WQA-BP-EXPOSED-SOURCEMAP',
                'best-practices',
                'medium',
                'Source map expuesto públicamente en producción',
                'Expone estructura interna del código fuente y aumenta descargas si se solicita.',
                {'url': r_url},
                'Desactivar o restringir la publicación de archivos .map en builds de producción.',
            )

    # 5. Inspección estática de código fuente (reemplazo seguro en Python de scripts/analyze.sh -> code_hypothesis)
    for path, content in sorted((source_files or {}).items()):
        if not isinstance(content, str):
            continue
        lower = content.lower()
        is_full_doc = '<html' in lower or '<head' in lower or path.endswith(('layout.tpl', 'theme.liquid', 'index.html', 'root.tsx'))
        if is_full_doc:
            if '<!doctype html>' not in lower and not path.endswith(('.tsx', '.jsx')):
                add_hypothesis(
                    'WQA-SRC-MISSING-DOCTYPE',
                    'best-practices',
                    'medium',
                    'Falta declaración <!DOCTYPE html> en plantilla base',
                    'Puede activar quirks mode en el navegador si el documento se sirve sin doctype.',
                    {'file': path, 'line': 1},
                    'Añadir <!DOCTYPE html> en la primera línea del layout.',
                    [path],
                )
            if 'charset' not in lower and 'utf-8' not in lower:
                add_hypothesis(
                    'WQA-SRC-MISSING-CHARSET',
                    'best-practices',
                    'low',
                    'No se observa declaración explícita de charset UTF-8 en plantilla base',
                    'Riesgo de codificación incorrecta de caracteres si las cabeceras HTTP no lo especifican.',
                    {'file': path, 'line': 1},
                    'Incluir <meta charset="UTF-8"> al inicio de <head>.',
                    [path],
                )
            if 'name="viewport"' not in lower and "name='viewport'" not in lower and 'viewport' not in lower:
                add_hypothesis(
                    'WQA-SRC-MISSING-VIEWPORT',
                    'seo',
                    'high',
                    'Falta meta viewport en plantilla base',
                    'Impide el escalado adaptable en dispositivos móviles.',
                    {'file': path, 'line': 1},
                    'Añadir <meta name="viewport" content="width=device-width, initial-scale=1">.',
                    [path],
                )
        for idx, line in enumerate(content.splitlines(), start=1):
            for img_match in re.finditer(r'<img\b[^>]*>', line, re.I):
                tag = img_match.group(0)
                if not re.search(r'\balt\s*=', tag, re.I):
                    add_hypothesis(
                        'WQA-SRC-IMG-WITHOUT-ALT',
                        'accessibility',
                        'medium',
                        'Etiqueta <img> en código fuente sin atributo alt explícito',
                        'Si se renderiza sin alt en el DOM final, generará una barrera de accesibilidad.',
                        {'file': path, 'line': idx, 'snippet': sanitize(tag[:120])},
                        'Añadir alt="{{ ... | escape }}" o alt="" en la plantilla.',
                        [path],
                    )
            if 'document.write(' in line:
                add_hypothesis(
                    'WQA-SRC-DOCUMENT-WRITE',
                    'best-practices',
                    'high',
                    'Uso de API obsoleta y bloqueante document.write()',
                    'Bloquea el parser HTML y degrada severamente el rendimiento y las buenas prácticas.',
                    {'file': path, 'line': idx},
                    'Reemplazar document.write() por manipulación DOM asíncrona o carga diferida.',
                    [path],
                )
            for http_match in re.finditer(r'http://[^\s"\'<>)]+', line, re.I):
                raw_http = http_match.group(0)
                if any(raw_http.lower().startswith(allow) for allow in (
                    'http://www.w3.org', 'http://schema.org', 'http://localhost', 'http://127.0.0.1'
                )):
                    continue
                add_hypothesis(
                    'WQA-SRC-INSECURE-HTTP-URL',
                    'best-practices',
                    'medium',
                    'Referencia http:// detectada en código fuente',
                    'Si corresponde a un activo o enlace en producción, puede causar contenido mixto o redirección.',
                    {'file': path, 'line': idx, 'url': sanitize(raw_http)},
                    'Cambiar el esquema de la URL a https://.',
                    [path],
                )

    severity_rank = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
    verified_issues.sort(key=lambda x: (severity_rank.get(x['severity'], 9), x['category'], x['id']))
    code_hypotheses.sort(key=lambda x: (severity_rank.get(x['severity'], 9), x['category'], x['id']))

    categories_summary = {}
    for cat in ('performance', 'accessibility', 'seo', 'best-practices', 'interaction'):
        v_count = sum(1 for i in verified_issues if i['category'] == cat)
        h_count = sum(1 for i in code_hypotheses if i['category'] == cat)
        categories_summary[cat] = {
            'lighthouse_score': category_scores.get(cat),
            'verified_issues_count': v_count,
            'code_hypotheses_count': h_count,
            'status': 'needs_attention' if v_count > 0 else 'hypothesis_only' if h_count > 0 else 'passed_observed_checks',
        }

    return {
        'skill': 'web-quality-audit',
        'reused_engine': 'cloudflare-web-perf',
        'framework': detected_fw,
        'evidence_vs_hypothesis_separated': True,
        'performance_diagnosis': perf,
        'categories_summary': categories_summary,
        'verified_issues': verified_issues,
        'code_hypotheses': code_hypotheses,
        'counts': {
            'verified_by_tool': len(verified_issues),
            'code_hypothesis': len(code_hypotheses),
            'critical': sum(1 for i in verified_issues if i['severity'] == 'critical'),
            'high': sum(1 for i in verified_issues if i['severity'] == 'high'),
            'medium': sum(1 for i in verified_issues if i['severity'] == 'medium'),
            'low': sum(1 for i in verified_issues if i['severity'] == 'low'),
        },
        'limitations': [
            'Una ejecución correcta de la auditoría no equivale a una mejora comprobada del sitio.',
            'Las hipótesis en código (code_hypothesis) deben confirmarse en el DOM/red renderizados antes de declararlas fallos reales.',
            'La ausencia de violaciones automatizadas no certifica cumplimiento total WCAG 2.2 AA ni indexación en Google.',
        ],
    }


REACT_COMPATIBLE_FRAMEWORKS = frozenset({'shopify-hydrogen', 'remix', 'nextjs', 'react-web'})

COMMERCE_CRITICAL_MARKERS = re.compile(
    r'\b(CartForm|cartLinesAdd|cartLinesUpdate|cartLinesRemove|checkoutUrl|customerAccessToken|session\.commit|useOptimisticCart)\b'
)


def audit_react_best_practices(
    source_files: dict[str, str] | None = None,
    *,
    framework: str | None = None,
    perf_report: dict | None = None,
) -> dict:
    """Auditoría Vercel React Best Practices (Etapa 5): waterfalls, bundles, re-renders y adaptación por framework."""
    files = source_files or {}
    detected_fw = infer_framework(framework, files)
    has_react_files = any(
        p.lower().endswith(('.tsx', '.jsx', '.ts', '.js', '.mjs'))
        and not p.lower().endswith(('.liquid', '.tpl'))
        for p in files
    )
    applicable = detected_fw in REACT_COMPATIBLE_FRAMEWORKS or has_react_files
    if detected_fw in ('shopify-liquid', 'tiendanube-ipanema') and not has_react_files:
        applicable = False

    findings = []
    protected_flows = []

    def add_finding(rule_id, vercel_rule, category, priority, title, impact, evidence, fix, file_path):
        findings.append({
            'id': rule_id,
            'vercel_rule': vercel_rule,
            'category': category,
            'priority': priority,
            'evidence_type': 'code_hypothesis',
            'title': title,
            'impact': impact,
            'evidence': sanitize(evidence),
            'candidate_files': [file_path],
            'fix': fix,
        })

    if applicable:
        dynamic_import_rec = (
            "Usar `next/dynamic` (`dynamic(() => import('./Component'))`)"
            if detected_fw == 'nextjs'
            else "Usar `React.lazy(() => import('./Component'))` envuelto en `<Suspense fallback={...}>` (no usar `next/dynamic` fuera de Next.js)."
        )
        server_cache_rec = (
            "Usar `React.cache()` para deduplicación por request y `after()` de `next/server` para tareas no bloqueantes."
            if detected_fw == 'nextjs'
            else "En Hydrogen/Remix usar `context.storefront.CacheShort()`/`CacheLong()` en consultas GraphQL, `defer()` para datos secundarios y `context.waitUntil()` para trabajo no bloqueante."
        )

        for path, content in sorted(files.items()):
            if not isinstance(content, str):
                continue

            # Protección de flujos comerciales críticos (carrito, checkout, auth, sesión)
            commerce_hits = sorted(set(COMMERCE_CRITICAL_MARKERS.findall(content)))
            if commerce_hits:
                protected_flows.append({'file': path, 'markers': commerce_hits})

            # 0. Incompatibilidad de APIs de Next.js en Hydrogen / Remix / React Vite
            if detected_fw in ('shopify-hydrogen', 'remix', 'react-web'):
                next_imports = re.findall(r'from\s+["\'](next/[a-zA-Z0-9_/-]+)["\']', content)
                if next_imports:
                    add_finding(
                        'RBP-FW-INCOMPATIBLE-NEXT-API',
                        'bundle-dynamic-imports',
                        'framework-compatibility',
                        'CRITICAL',
                        f'Importación de API exclusiva de Next.js ({", ".join(next_imports)}) en proyecto {detected_fw}',
                        'Romperá la compilación o el runtime en Hydrogen/Remix/Vite.',
                        {'file': path, 'imports': next_imports, 'framework': detected_fw},
                        f'Reemplazar {next_imports[0]} por primitivas compatibles con {detected_fw}: {dynamic_import_rec}',
                        path,
                    )

            # 1. Waterfalls: sequential awaits in loader / async function
            await_matches = list(re.finditer(r'(?:const|let)\s+(\w+)\s*=\s*await\s+([a-zA-Z0-9_.$]+)\s*\(([^;\n]*)\)', content))
            if len(await_matches) >= 2:
                for first, second in zip(await_matches, await_matches[1:]):
                    first_var = first.group(1)
                    second_args = second.group(3)
                    # Si la segunda llamada no usa la variable de la primera, son independientes -> waterfall
                    if not re.search(r'\b' + re.escape(first_var) + r'\b', second_args):
                        add_finding(
                            'RBP-ASYNC-SEQUENTIAL-WATERFALL',
                            'async-parallel',
                            'eliminating-waterfalls',
                            'CRITICAL',
                            f'Waterfall secuencial detectado entre `await {first.group(2)}(...)` y `await {second.group(2)}(...)`',
                            'Suma las latencias de red en serie y retrasa el TTFB/FCP de la ruta.',
                            {'file': path, 'first_await': first.group(0), 'second_await': second.group(0)},
                            'Ejecutar operaciones independientes en paralelo con `await Promise.all([...])` o diferir datos secundarios con `defer()` y `<Suspense><Await>`.',
                            path,
                        )
                        break

            # Waterfall en cliente: fetch dentro de useEffect
            if re.search(r'useEffect\s*\(\s*\(\s*\)\s*=>\s*\{[^}]*\bfetch\s*\(', content, re.S):
                add_finding(
                    'RBP-ASYNC-EFFECT-FETCH-WATERFALL',
                    'server-parallel-fetching',
                    'eliminating-waterfalls',
                    'HIGH',
                    'Fetching de datos dentro de `useEffect` tras el montaje del componente',
                    'Crea una cascada documento -> JS -> hidratación -> fetch que retrasa el LCP.',
                    {'file': path},
                    'Mover la carga de datos al `loader` de la ruta (Hydrogen/Remix) o iniciar la promesa antes del renderizado.',
                    path,
                )

            # 2. Bundle Size Optimization: barrel / wholesale imports & heavy components
            barrel_hits = re.findall(
                r'import\s+(?:\*\s+as\s+\w+|\w+|\{[^}]+\})\s+from\s+["\'](lodash|moment|lucide-react|@mui/icons-material|date-fns|\.\.?/[^"\']*index)["\']',
                content,
            )
            if barrel_hits:
                add_finding(
                    'RBP-BUNDLE-BARREL-IMPORT',
                    'bundle-barrel-imports',
                    'bundle-size',
                    'CRITICAL',
                    f'Importación de archivo barril o librería monolítica ({", ".join(sorted(set(barrel_hits)))})',
                    'Impide un tree-shaking eficiente e infla el bundle de JavaScript enviado al cliente.',
                    {'file': path, 'modules': sorted(set(barrel_hits))},
                    'Importar directamente desde el submódulo específico (ej. `lodash/debounce` o el componente directo sin pasar por `index`).',
                    path,
                )

            heavy_imports = re.findall(
                r'import\s+(\w+)\s+from\s+["\']([^"\']*(?:Modal|Chart|Editor|Carousel3D|VideoPlayer|Map|Drawer)[^"\']*)["\']',
                content,
            )
            if heavy_imports and 'React.lazy' not in content and 'lazy(' not in content and 'dynamic(' not in content:
                add_finding(
                    'RBP-BUNDLE-DYNAMIC-IMPORT',
                    'bundle-dynamic-imports',
                    'bundle-size',
                    'HIGH',
                    f'Componente pesado importado de forma ansiosa ({heavy_imports[0][0]})',
                    'Incluye código de interfaz secundaria o interactiva en el bundle inicial de la página.',
                    {'file': path, 'component': heavy_imports[0][0], 'source': heavy_imports[0][1]},
                    dynamic_import_rec,
                    path,
                )

            # 3. Server-Side Performance: module-level mutable state
            if re.search(r'(?m)^\s*let\s+(?:current|shared|cached|active|global)[A-Za-z0-9_]*\s*=', content):
                add_finding(
                    'RBP-SERVER-SHARED-MODULE-STATE',
                    'server-no-shared-module-state',
                    'server-performance',
                    'CRITICAL',
                    'Estado mutable a nivel de módulo detectado en archivo SSR/ruta',
                    'En entornos SSR concurrentes (Hydrogen/Oxygen, Remix, Node/Workers) puede filtrar datos de sesión o carrito entre usuarios distintos.',
                    {'file': path},
                    f'Encapsular el estado dentro del contexto del request (`loader`/`action`). {server_cache_rec}',
                    path,
                )

            # 4. Re-render Optimization: derived state in useEffect, inline components, lazy state init
            if re.search(r'useEffect\s*\(\s*\(\s*\)\s*=>\s*\{\s*set[A-Z]\w*\s*\(', content):
                add_finding(
                    'RBP-RERENDER-DERIVED-STATE-EFFECT',
                    'rerender-derived-state-no-effect',
                    'rerender-optimization',
                    'MEDIUM',
                    'Actualización de estado derivado dentro de `useEffect` (`setState` síncrono)',
                    'Fuerza un pase de renderizado adicional innecesario con valores intermedios obsoletos.',
                    {'file': path},
                    'Calcular el estado derivado directamente durante el renderizado o mediante `useMemo` sin `useEffect`.',
                    path,
                )

            # Inline component inside another component
            func_comps = list(re.finditer(r'(?:export\s+default\s+|export\s+)?function\s+([A-Z]\w*)\s*\([^)]*\)\s*\{', content))
            if len(func_comps) >= 1:
                outer_start = func_comps[0].end()
                inner_comp = re.search(r'\b(?:function\s+[A-Z]\w*\s*\(|const\s+[A-Z]\w*\s*=\s*\([^)]*\)\s*=>\s*[<({])', content[outer_start:])
                if inner_comp:
                    add_finding(
                        'RBP-RERENDER-INLINE-COMPONENT',
                        'rerender-no-inline-components',
                        'rerender-optimization',
                        'HIGH',
                        'Definición de componente anidado dentro del cuerpo de otro componente',
                        'Recrea el tipo de componente en cada render, desmontando el DOM y perdiendo el foco y el estado local.',
                        {'file': path, 'outer_component': func_comps[0].group(1)},
                        'Extraer el subcomponente al nivel superior del módulo y pasarle los datos necesarios mediante props.',
                        path,
                    )

            if re.search(r'useState\s*\(\s*(?:JSON\.parse|localStorage\.getItem|sessionStorage\.getItem)\s*\(', content):
                add_finding(
                    'RBP-RERENDER-LAZY-STATE-INIT',
                    'rerender-lazy-state-init',
                    'rerender-optimization',
                    'MEDIUM',
                    'Inicialización costosa ejecutada en cada render dentro de `useState(...)`',
                    'Ejecuta `JSON.parse` o lectura de storage en todos los re-renderizados aunque solo se use en el montaje inicial.',
                    {'file': path},
                    'Pasar una función inicializadora perezosa: `useState(() => JSON.parse(...))`.',
                    path,
                )

            # 5. Rendering & JS performance: `.length && <JSX>`, O(n^2) `.includes` in `.filter/.map`, non-passive scroll
            if re.search(r'\.\s*length\s*&&\s*<[A-Za-z]', content):
                add_finding(
                    'RBP-RENDERING-AND-ZERO-LEAK',
                    'rendering-conditional-render',
                    'rendering-performance',
                    'MEDIUM',
                    'Renderizado condicional con `.length && <Componente />`',
                    'Cuando la lista está vacía (`length === 0`), React renderiza el número literal `0` en el DOM.',
                    {'file': path},
                    'Usar una comparación booleana explícita o ternario: `items.length > 0 ? <Componente /> : null`.',
                    path,
                )

            if re.search(r'\.(?:filter|map)\s*\([^)]*=>[^)]*\.(?:includes|find)\s*\(', content):
                add_finding(
                    'RBP-JS-SET-MAP-LOOKUP',
                    'js-set-map-lookups',
                    'js-performance',
                    'LOW-MEDIUM',
                    'Búsqueda lineal `.includes()` / `.find()` dentro de `.filter()` o `.map()` (complejidad O(n²))',
                    'Incrementa el tiempo de bloqueo del hilo principal (TBT/INP) al procesar listas de productos o variantes.',
                    {'file': path},
                    'Construir un `Set` o `Map` previo fuera del bucle para búsquedas en tiempo constante `O(1)`.',
                    path,
                )

            if re.search(r'addEventListener\s*\(\s*["\'](?:scroll|touchstart|wheel)["\']\s*,\s*[^,)]+\)', content):
                add_finding(
                    'RBP-CLIENT-PASSIVE-LISTENER',
                    'client-passive-event-listeners',
                    'client-fetching-and-events',
                    'MEDIUM',
                    'Listener de `scroll`/`touchstart`/`wheel` sin `{ passive: true }`',
                    'Obliga al compositor del navegador a esperar al hilo principal antes de desplazar la página.',
                    {'file': path},
                    'Añadir `{ passive: true }` como tercer argumento de `addEventListener`.',
                    path,
                )

    perf_correlation = None
    if isinstance(perf_report, dict):
        diag = perf_report if perf_report.get('skill') == 'cloudflare-web-perf' else diagnose_web_perf(perf_report)
        perf_correlation = {
            'reused_skill': 'cloudflare-web-perf',
            'lab_metrics': diag.get('lab_metrics', {}),
            'field_metrics': diag.get('field_metrics', {}),
            'large_resources_count': len((diag.get('network') or {}).get('large_resources', [])),
        }

    priority_rank = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM-HIGH': 2, 'MEDIUM': 3, 'LOW-MEDIUM': 4, 'LOW': 5}
    findings.sort(key=lambda x: (priority_rank.get(x['priority'], 9), x['id']))

    return sanitize({
        'kind': 'react-best-practices-audit',
        'skill': 'vercel-react-best-practices',
        'applicable': applicable,
        'framework': detected_fw,
        'reused_engines': ['cloudflare-web-perf'] if perf_correlation else [],
        'performance_correlation': perf_correlation,
        'commercial_safety_guards': {
            'preserve_cart_checkout_auth_state': True,
            'protected_commerce_files': protected_flows,
            'note': 'Ninguna optimización modifica reglas de negocio, mutaciones de carrito, precios, checkout, autenticación ni sesión.',
        },
        'findings': findings,
        'counts': {
            'total': len(findings),
            'critical': sum(1 for f in findings if f['priority'] == 'CRITICAL'),
            'high': sum(1 for f in findings if f['priority'] == 'HIGH'),
            'medium': sum(1 for f in findings if f['priority'] in ('MEDIUM-HIGH', 'MEDIUM')),
            'low': sum(1 for f in findings if f['priority'] in ('LOW-MEDIUM', 'LOW')),
        },
        'limitations': [
            'No aplicar reglas de React/Next.js a plantillas Shopify Liquid o Tiendanube sin React.',
            'Las hipótesis de código deben verificarse con pruebas funcionales y mediciones antes/después.',
        ],
    })


AMBIGUOUS_CTA_LABELS = frozenset({
    'continue', 'continuar', 'submit', 'enviar', 'click', 'click here', 'ok', 'go', 'more', 'ver',
})

DESIGN_COMMERCE_CONTRACT_MARKERS = re.compile(
    r'(?:(?<!\w)(?:js-[a-zA-Z0-9_-]+|data-store|LS\.[a-zA-Z0-9_]+|CartForm|cartLinesAdd|cartLinesUpdate|cartLinesRemove|checkoutUrl|product_form)\b|/cart/add)'
)


def audit_web_design_guidelines(
    source_files: dict[str, str] | None = None,
    *,
    rendered: dict | None = None,
    framework: str | None = None,
    quality_audit_report: dict | None = None,
    accessibility_report: dict | None = None,
    delegate_accessibility: bool = True,
) -> dict:
    """Auditoría Vercel Web Design Guidelines (Etapa 6): jerarquía visual, UX e-commerce, estados interactivos, responsive y consistencia visual sin descarga dinámica."""
    files = source_files or {}
    detected_fw = infer_framework(framework, files)
    candidates_map = FRAMEWORK_CANDIDATES.get(detected_fw, FRAMEWORK_CANDIDATES['tiendanube-ipanema'])

    verified_by_tool = []
    code_hypothesis = []
    requires_external_verification = []
    reused_wqa_ids = []

    def add_verified(issue_id, category, vercel_rule, severity, title, impact, evidence, fix, candidate_files=None):
        verified_by_tool.append({
            'id': issue_id,
            'category': category,
            'vercel_rule': vercel_rule,
            'severity': severity,
            'evidence_type': 'verified_by_tool',
            'title': title,
            'impact': impact,
            'evidence': sanitize(evidence),
            'candidate_files': candidate_files or list(files.keys())[:2] or candidates_map.get('accessibility', []),
            'fix': fix,
        })

    def add_hypothesis(issue_id, category, vercel_rule, severity, title, impact, evidence, fix, file_path, line=1):
        code_hypothesis.append({
            'id': issue_id,
            'category': category,
            'vercel_rule': vercel_rule,
            'severity': severity,
            'evidence_type': 'code_hypothesis',
            'title': title,
            'impact': impact,
            'evidence': sanitize({**evidence, 'file': file_path, 'line': line, 'location': f'{file_path}:{line}'}),
            'candidate_files': [file_path],
            'fix': fix,
        })

    def add_external(issue_id, category, title, reason, required_check):
        requires_external_verification.append({
            'id': issue_id,
            'category': category,
            'evidence_type': 'requires_external_verification',
            'title': title,
            'reason': reason,
            'required_check': required_check,
        })

    # Reutilizar hallazgos de web-quality-audit cuando se suministra un informe previo
    if isinstance(quality_audit_report, dict) and quality_audit_report.get('skill') == 'web-quality-audit':
        for item in quality_audit_report.get('verified_issues') or []:
            if isinstance(item, dict) and item.get('category') in ('accessibility', 'interaction'):
                reused_wqa_ids.append(item.get('id'))

    # 1. Evidencia verificada por herramienta en DOM/viewport renderizado
    if isinstance(rendered, dict):
        vp = rendered.get('viewport') or {}
        iw, sw = numeric(vp.get('innerWidth')), numeric(vp.get('scrollWidth'))
        if iw and sw and sw > iw:
            add_verified(
                'WDG-RESP-HORIZONTAL-OVERFLOW',
                'responsive',
                'safe-areas-and-layout',
                'high',
                f'Desbordamiento horizontal medido en viewport ({int(sw)}px > {int(iw)}px)',
                'Rompe la experiencia móvil, genera scroll lateral no deseado y desplaza controles táctiles.',
                {'innerWidth': iw, 'scrollWidth': sw},
                'Corregir elementos con ancho fijo mayor al contenedor y aplicar min-w-0 en hijos flexibles.',
            )

        meta_list = [m for m in (rendered.get('metadata') or []) if isinstance(m, dict)]
        for m in meta_list:
            if str(m.get('name') or '').lower() == 'viewport':
                v_content = str(m.get('content') or '').lower()
                if 'user-scalable=no' in v_content or 'user-scalable=0' in v_content or re.search(r'maximum-scale\s*=\s*1(?:\.0)?\b', v_content):
                    add_verified(
                        'WDG-RESP-ZOOM-DISABLED',
                        'responsive',
                        'anti-patterns:user-scalable',
                        'critical',
                        'Meta viewport bloquea el zoom del usuario (user-scalable=no / maximum-scale=1)',
                        'Impide ampliar texto e imágenes en móvil y viola principios de accesibilidad e interfaz.',
                        {'viewport': m.get('content')},
                        'Permitir escalado del usuario en <meta name="viewport" content="width=device-width, initial-scale=1">.',
                    )

        headings = [h for h in (rendered.get('headings') or []) if isinstance(h, dict)]
        h1_count = sum(1 for h in headings if str(h.get('tag') or '').upper() == 'H1' and str(h.get('text') or '').strip())
        if headings and h1_count == 0:
            add_verified(
                'WDG-VH-MISSING-PRIMARY-HEADING',
                'visual-hierarchy',
                'accessibility:headings-hierarchical',
                'high',
                'Página renderizada sin encabezado primario <h1> visible',
                'Debilita la jerarquía visual y la orientación inmediata del usuario en la página.',
                {'headings_count': len(headings)},
                'Definir un único encabezado principal <h1> claro para el título de página o producto.',
            )
        prev_level = 0
        for h in headings:
            tag = str(h.get('tag') or '').upper()
            if tag.startswith('H') and tag[1:].isdigit():
                lvl = int(tag[1:])
                if prev_level and lvl > prev_level + 1:
                    add_verified(
                        'WDG-VH-HEADING-LEVEL-SKIP',
                        'visual-hierarchy',
                        'accessibility:headings-hierarchical',
                        'medium',
                        f'Salto en jerarquía de encabezados (H{prev_level} -> H{lvl})',
                        'Rompe la progresión visual y semántica de secciones de la interfaz.',
                        {'from': f'H{prev_level}', 'to': f'H{lvl}', 'text': h.get('text')},
                        'Mantener orden jerárquico secuencial h1 -> h2 -> h3 y ajustar el tamaño visual mediante clases CSS del sistema de diseño.',
                    )
                    break
                prev_level = lvl

        for btn in (rendered.get('buttons') or []):
            if not isinstance(btn, dict):
                continue
            btext = str(btn.get('text') or '').strip()
            baria = str(btn.get('ariaLabel') or '').strip()
            if not btext and not baria:
                add_verified(
                    'WDG-INT-ICON-BUTTON-MISSING-LABEL',
                    'interactive-states',
                    'accessibility:icon-button-aria-label',
                    'high',
                    'Botón interactivo (solo icono) sin texto visible ni aria-label',
                    'Los usuarios no pueden identificar la acción del botón (ej. cerrar drawer, abrir carrito, buscar).',
                    {'id': btn.get('id'), 'class': btn.get('class')},
                    'Añadir aria-label descriptivo de la acción al elemento <button>.',
                )
            elif (btext or baria).lower() in AMBIGUOUS_CTA_LABELS:
                add_verified(
                    'WDG-VH-AMBIGUOUS-CTA-LABEL',
                    'visual-hierarchy',
                    'content-and-copy:specific-button-labels',
                    'medium',
                    f'Etiqueta de botón ambigua o poco específica ("{btext or baria}")',
                    'Reduce la claridad de la acción primaria o secundaria en flujos de compra.',
                    {'label': btext or baria},
                    'Usar etiquetas de acción explícitas (ej. "Agregar al carrito", "Guardar dirección", "Aplicar cupón") respetando el tono de la marca.',
                )
            w, h = numeric(btn.get('width')), numeric(btn.get('height'))
            if (w is not None and 0 < w < 44) or (h is not None and 0 < h < 44):
                add_verified(
                    'WDG-RESP-SMALL-TOUCH-TARGET',
                    'responsive',
                    'touch-and-interaction',
                    'medium',
                    f'Área táctil de control interactivo menor a 44x44px ({w}x{h}px)',
                    'Dificulta la pulsación precisa en pantallas móviles (selectores de talla/color o cantidad).',
                    {'label': btext or baria, 'width': w, 'height': h},
                    'Aumentar el área clicable/táctil a mínimo 44x44px usando padding o min-height/min-width sin alterar la estética de la marca.',
                )

        for form in (rendered.get('forms') or []):
            if not isinstance(form, dict):
                continue
            for inp in (form.get('inputs') or []):
                if not isinstance(inp, dict):
                    continue
                itype = str(inp.get('type') or '').lower()
                if itype in ('hidden', 'submit', 'button', 'reset', 'image'):
                    continue
                if not inp.get('hasLabel') and not inp.get('ariaLabel'):
                    add_verified(
                        'WDG-ECOM-FORM-UNLABELED-CONTROL',
                        'ecommerce-ux',
                        'forms:form-controls-need-label',
                        'high',
                        'Campo de formulario sin <label> asociado ni aria-label',
                        'Genera fricción en formularios de compra, búsqueda, cupón o contacto.',
                        {'name': inp.get('name'), 'type': itype},
                        'Asociar un <label for="..."> clicable o aria-label descriptivo.',
                    )

        for img in (rendered.get('images') or []):
            if not isinstance(img, dict):
                continue
            if img.get('visible') and (not numeric(img.get('width')) or not numeric(img.get('height'))):
                add_verified(
                    'WDG-ECOM-IMG-MISSING-DIMENSIONS',
                    'ecommerce-ux',
                    'images:explicit-width-height',
                    'medium',
                    'Imagen visible sin width y height explícitos',
                    'Provoca saltos visuales de layout (CLS) al cargar galerías de producto o tarjetas de colección.',
                    {'src': img.get('currentSrc') or img.get('src')},
                    'Definir atributos width y height explícitos o aspect-ratio consistente en el contenedor.',
                )
    else:
        add_external(
            'WDG-EXT-RENDERED-VIEWPORT-AND-COMPUTED-STYLES',
            'responsive',
            'Verificación visual en navegador real (mobile 360/390px y desktop 1440px)',
            'Solo se analizaron archivos fuente estáticos; no se midió el DOM/CSS computado en un viewport real.',
            'Ejecutar QA visual/browser en 360px, 390px, 768px y 1440px para confirmar ausencia de overflow, contraste real y visibilidad de :focus-visible.',
        )

    # 2. Inspección estática de archivos fuente (code_hypothesis en formato file:line)
    protected_contracts = []
    detected_design_tokens = set()

    for path, content in sorted(files.items()):
        if not isinstance(content, str):
            continue
        lines = content.splitlines()
        lower = content.lower()

        # Inventario de tokens del sistema de diseño y contratos comerciales para proteger identidad visual
        tokens_in_file = re.findall(r'--(?:color|font|space|radius|shadow|btn|text|bg)-[a-zA-Z0-9_-]+', content)
        detected_design_tokens.update(tokens_in_file)
        contracts_in_file = sorted(set(DESIGN_COMMERCE_CONTRACT_MARKERS.findall(content)))
        if contracts_in_file:
            protected_contracts.append({'file': path, 'contracts': contracts_in_file})

        has_focus_visible = ':focus-visible' in lower or 'focus-visible:' in lower
        has_reduced_motion = 'prefers-reduced-motion' in lower
        has_tabular_nums = 'tabular-nums' in lower

        for idx, line in enumerate(lines, start=1):
            llower = line.lower()

            # Anti-patrón: user-scalable=no o maximum-scale=1 en fuente
            if 'user-scalable=no' in llower or 'user-scalable=0' in llower or re.search(r'maximum-scale\s*=\s*1(?:\.0)?\b', llower):
                add_hypothesis(
                    'WDG-SRC-ZOOM-DISABLED',
                    'responsive',
                    'anti-patterns:user-scalable',
                    'critical',
                    'Meta viewport deshabilita el zoom en plantilla fuente',
                    'Impide hacer zoom en dispositivos táctiles.',
                    {'snippet': line.strip()[:120]},
                    'Retirar user-scalable=no y maximum-scale=1 del meta viewport.',
                    path,
                    idx,
                )

            # Anti-patrón: outline: none / outline-none sin reemplazo :focus-visible
            if ('outline: none' in llower or 'outline:none' in llower or 'outline: 0' in llower or 'outline-none' in llower) and 'focus-visible' not in llower and not has_focus_visible:
                add_hypothesis(
                    'WDG-SRC-OUTLINE-NONE-NO-FOCUS-VISIBLE',
                    'interactive-states',
                    'focus-states:never-outline-none-without-replacement',
                    'high',
                    'Eliminación de contorno de foco (outline: none / outline-none) sin reemplazo :focus-visible',
                    'Oculta el indicador de foco para navegación por teclado en botones, enlaces o selectores de variantes.',
                    {'snippet': line.strip()[:120]},
                    'Reemplazar por estilos `:focus-visible` (ej. `focus-visible:ring-2` o `outline: 2px solid var(--color-primary)`).',
                    path,
                    idx,
                )

            # Anti-patrón: transition: all / transition-all
            if re.search(r'transition\s*:\s*all\b', llower) or re.search(r'(?<![\w-])transition-all(?![\w-])', llower):
                add_hypothesis(
                    'WDG-SRC-TRANSITION-ALL',
                    'interactive-states',
                    'animation:never-transition-all',
                    'medium',
                    'Uso de `transition: all` / `transition-all` en lugar de propiedades explícitas',
                    'Anima propiedades de layout no deseadas y degrada la fluidez visual; animar solo `transform`, `opacity` o `color`.',
                    {'snippet': line.strip()[:120]},
                    'Especificar explícitamente las propiedades a transicionar (ej. `transition: opacity 150ms ease, transform 150ms ease`).',
                    path,
                    idx,
                )

            # Anti-patrón: <div onClick> o <span onClick>
            if re.search(r'<(?:div|span)\b[^>]*\bonclick\s*=', llower):
                add_hypothesis(
                    'WDG-SRC-NON-SEMANTIC-CLICK-HANDLER',
                    'interactive-states',
                    'accessibility:button-for-actions-link-for-nav',
                    'high',
                    'Elemento no semántico `<div>`/`<span>` con manejador `onClick`',
                    'Carece de foco por teclado, rol semántico, activación con Enter/Espacio y soporte de clic central si es navegación.',
                    {'snippet': line.strip()[:120]},
                    'Usar `<button type="button">` para acciones (ej. seleccionar variante, abrir modal) o `<a href="...">` para navegación.',
                    path,
                    idx,
                )

            # Anti-patrón: bloqueo de pegado onPaste + preventDefault
            if 'onpaste' in llower and ('preventdefault' in llower or 'return false' in llower):
                add_hypothesis(
                    'WDG-SRC-PASTE-BLOCKED',
                    'interactive-states',
                    'forms:never-block-paste',
                    'high',
                    'Bloqueo de pegado (`onPaste` con `preventDefault`) en campo de formulario',
                    'Impide pegar contraseñas, códigos de descuento, correos o direcciones desde gestores.',
                    {'snippet': line.strip()[:120]},
                    'Eliminar el bloqueo de `onPaste` y validar el formato del valor ingresado sin impedir pegar.',
                    path,
                    idx,
                )

            # Anti-patrón: botón de solo icono sin aria-label en la misma línea
            for btn_match in re.finditer(r'<button\b([^>]*)>\s*(?:<(?:svg|i|img)\b[^>]*>(?:</(?:svg|i)>)?)\s*</button>', line, re.I):
                attrs = btn_match.group(1)
                if 'aria-label' not in attrs.lower() and 'aria-labelledby' not in attrs.lower():
                    add_hypothesis(
                        'WDG-SRC-ICON-BUTTON-MISSING-ARIA-LABEL',
                        'interactive-states',
                        'accessibility:icon-button-aria-label',
                        'high',
                        'Botón de solo icono sin atributo `aria-label`',
                        'El propósito del botón (cerrar, carrito, búsqueda, favorito) queda oculto para tecnologías de asistencia.',
                        {'snippet': btn_match.group(0)[:120]},
                        'Añadir `aria-label="..."` descriptivo en `<button>` y `aria-hidden="true"` en el icono decorativo.',
                        path,
                        idx,
                    )

            # Anti-patrón: <img> sin width o height explícitos
            for img_match in re.finditer(r'<img\b([^>]*)>', line, re.I):
                attrs = img_match.group(1).lower()
                if 'width=' not in attrs or 'height=' not in attrs:
                    add_hypothesis(
                        'WDG-SRC-IMG-MISSING-DIMENSIONS',
                        'ecommerce-ux',
                        'images:explicit-width-height',
                        'medium',
                        'Etiqueta `<img>` sin atributos `width` y `height` explícitos',
                        'Puede causar desplazamiento acumulativo de diseño (CLS) al cargar imágenes de producto o banners.',
                        {'snippet': img_match.group(0)[:120]},
                        'Añadir atributos `width` y `height` explícitos acordes a la proporción de la imagen.',
                        path,
                        idx,
                    )

            # Anti-patrón: <input> visible sin label en línea ni aria-label
            for inp_match in re.finditer(r'<input\b([^>]*)>', line, re.I):
                attrs = inp_match.group(1)
                alower = attrs.lower()
                if any(t in alower for t in ('type="hidden"', "type='hidden'", 'type="submit"', "type='submit'", 'type="button"', "type='button'")):
                    continue
                has_aria = 'aria-label' in alower or 'aria-labelledby' in alower
                has_id = re.search(r'\bid\s*=\s*["\']([^"\']+)["\']', attrs, re.I)
                linked_label = bool(has_id and re.search(r'for\s*=\s*["\']' + re.escape(has_id.group(1)) + r'["\']', content, re.I)) or bool(has_id and re.search(r'htmlFor\s*=\s*["\']' + re.escape(has_id.group(1)) + r'["\']', content, re.I))
                if not has_aria and not linked_label and '<label' not in llower:
                    add_hypothesis(
                        'WDG-SRC-INPUT-MISSING-LABEL',
                        'ecommerce-ux',
                        'forms:form-controls-need-label',
                        'high',
                        'Control `<input>` sin `<label>` vinculado ni `aria-label`',
                        'Dificulta completar formularios de cantidad, variantes, búsqueda, cupón o newsletter.',
                        {'snippet': inp_match.group(0)[:120]},
                        'Vincular un `<label for="...">` clicable o añadir `aria-label` y `autocomplete`/`name` apropiados.',
                        path,
                        idx,
                    )

            # Anti-patrón: autoFocus sin restricción desktop
            if re.search(r'\bautofocus\b', llower):
                add_hypothesis(
                    'WDG-SRC-UNRESTRICTED-AUTOFOCUS',
                    'responsive',
                    'touch-and-interaction:autofocus-sparingly',
                    'low',
                    'Uso de `autoFocus` que puede abrir el teclado virtual abruptamente en móvil',
                    'En dispositivos móviles desplaza el viewport y cubre el contenido principal al abrir un drawer o página.',
                    {'snippet': line.strip()[:120]},
                    'Evitar `autoFocus` en vistas móviles o restringirlo únicamente a entradas primarias en desktop.',
                    path,
                    idx,
                )

            # Anti-patrón: lectura síncrona de layout en render
            if any(m in line for m in ('getBoundingClientRect(', '.offsetWidth', '.offsetHeight')):
                add_hypothesis(
                    'WDG-SRC-LAYOUT-READ-IN-UI',
                    'responsive',
                    'performance:no-layout-reads-in-render',
                    'medium',
                    'Medición de layout con JS (`getBoundingClientRect` / `offsetWidth` / `offsetHeight`)',
                    'Puede provocar forced synchronous layout (thrashing) y saltos visuales al redimensionar.',
                    {'snippet': line.strip()[:120]},
                    'Preferir CSS Flex/Grid, Container Queries o CSS custom properties en lugar de medir layout en JS durante el render.',
                    path,
                    idx,
                )

            # Anti-patrón tipográfico: "..." en lugar de "…" en estados de carga o placeholders
            if re.search(r'(?:loading|cargando|saving|guardando|buscar|search|placeholder\s*=\s*["\'][^"\']*)\.\.\.', llower):
                add_hypothesis(
                    'WDG-SRC-STRAIGHT-ELLIPSIS',
                    'visual-hierarchy',
                    'typography:ellipsis-character',
                    'low',
                    'Uso de tres puntos `...` en lugar del carácter tipográfico de elipsis `…` en estado de carga o placeholder',
                    'Detalle de pulido tipográfico en microcopy de estados de carga y placeholders.',
                    {'snippet': line.strip()[:120]},
                    'Sustituir `...` por el carácter de elipsis `…` (ej. `"Cargando…"`).',
                    path,
                    idx,
                )

        # Chequeos a nivel de archivo (animación sin prefers-reduced-motion, precios sin tabular-nums, drawers sin overscroll-behavior)
        if ('@keyframes' in lower or 'animation:' in lower or 'animate-' in lower) and not has_reduced_motion:
            add_hypothesis(
                'WDG-SRC-MISSING-PREFERS-REDUCED-MOTION',
                'interactive-states',
                'animation:honor-prefers-reduced-motion',
                'medium',
                'Animación CSS/UI sin soporte para `prefers-reduced-motion`',
                'No ofrece variante reducida o desactivada para usuarios con sensibilidad al movimiento.',
                {'has_animation': True, 'prefers_reduced_motion': False},
                'Añadir `@media (prefers-reduced-motion: reduce)` o utilidades `motion-reduce:` para atenuar o desactivar la animación.',
                path,
                1,
            )

        if any(k in lower for k in ('drawer', 'modal', 'cart-drawer', 'sheet', 'dialog')) and 'overscroll-behavior' not in lower:
            add_hypothesis(
                'WDG-SRC-DRAWER-MISSING-OVERSCROLL-CONTAIN',
                'ecommerce-ux',
                'touch-and-interaction:overscroll-behavior-contain',
                'medium',
                'Modal o drawer de carrito sin `overscroll-behavior: contain`',
                'El desplazamiento dentro del drawer o modal se propaga al fondo de la página en móvil y trackpads.',
                {'component_kind': 'modal_or_drawer'},
                'Añadir `overscroll-behavior: contain` (o `overscroll-contain`) al contenedor desplazable del drawer/modal.',
                path,
                1,
            )

        if any(k in lower for k in ('price', 'precio', 'compare-at', 'subtotal', 'total')) and (path.endswith(('.css', '.scss')) or '<style' in lower) and not has_tabular_nums:
            add_hypothesis(
                'WDG-SRC-PRICE-MISSING-TABULAR-NUMS',
                'visual-hierarchy',
                'typography:tabular-nums',
                'low',
                'Estilos de precios o totales sin `font-variant-numeric: tabular-nums`',
                'Dificulta comparar precios, descuentos y cantidades alineadas verticalmente o durante actualizaciones dinámicas.',
                {'has_price_styles': True},
                'Añadir `font-variant-numeric: tabular-nums` (o `tabular-nums`) en selectores de precios, descuentos y contadores.',
                path,
                1,
            )

        # Consistencia visual: colores hex hardcodeados cuando existen tokens CSS del tema
        hex_colors = re.findall(r'#[0-9a-fA-F]{3,6}\b', content)
        if tokens_in_file and hex_colors:
            add_hypothesis(
                'WDG-SRC-HARDCODED-COLOR-BYPASSING-TOKENS',
                'visual-consistency',
                'theming:preserve-design-tokens',
                'low',
                f'Valores de color hexadecimales hardcodeados ({", ".join(sorted(set(hex_colors))[:3])}) en archivo que ya utiliza variables CSS de marca',
                'Puede generar inconsistencias visuales con la paleta oficial configurada en el tema o en modo oscuro.',
                {'hardcoded_colors': sorted(set(hex_colors))[:5], 'available_css_vars_sample': sorted(tokens_in_file)[:5]},
                'Reutilizar las variables CSS existentes del sistema de diseño de la tienda sin alterar su paleta de marca.',
                path,
                1,
            )

    severity_rank = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
    verified_by_tool.sort(key=lambda x: (severity_rank.get(x['severity'], 9), x['category'], x['id']))
    code_hypothesis.sort(key=lambda x: (severity_rank.get(x['severity'], 9), x['category'], x['id']))

    # Generar resumen terse file:line al estilo Web Interface Guidelines
    terse_report = []
    for h in code_hypothesis:
        loc = (h.get('evidence') or {}).get('location') or f"{h['candidate_files'][0]}:1"
        terse_report.append(f"{loc} - [{h['id']}] {h['title']}")

    categories = ('visual-hierarchy', 'ecommerce-ux', 'interactive-states', 'responsive', 'visual-consistency')
    categories_summary = {}
    for cat in categories:
        v_c = sum(1 for i in verified_by_tool if i['category'] == cat)
        h_c = sum(1 for i in code_hypothesis if i['category'] == cat)
        categories_summary[cat] = {
            'verified_by_tool': v_c,
            'code_hypothesis': h_c,
            'status': 'needs_attention' if v_c > 0 else 'hypothesis_only' if h_c > 0 else 'passed_observed_checks',
        }

    accessibility_issue_rules = (
        'accessibility:', 'focus-states:', 'forms:', 'anti-patterns:user-scalable',
        'animation:honor-prefers-reduced-motion', 'touch-and-interaction',
    )
    has_a11y_signals = any(
        str(item.get('vercel_rule') or '').startswith(accessibility_issue_rules)
        for item in verified_by_tool + code_hypothesis
    )
    delegated_a11y = None
    if isinstance(accessibility_report, dict) and accessibility_report.get('skill') == 'better-accessibility':
        delegated_a11y = accessibility_report
    elif delegate_accessibility and has_a11y_signals:
        delegated_a11y = audit_better_accessibility(
            files,
            rendered=rendered,
            framework=detected_fw,
            quality_audit_report=quality_audit_report,
        )

    reused_list = (['web-quality-audit'] if reused_wqa_ids else [])
    if delegated_a11y is not None:
        reused_list.append('better-accessibility')
    reused_list.extend(['ipanema-responsive', 'ipanema-visual-qa'])

    return sanitize({
        'kind': 'web-design-guidelines-audit',
        'skill': 'web-design-guidelines',
        'framework': detected_fw,
        'rules_source': {
            'skill_repo': 'vercel-labs/agent-skills',
            'skill_commit': '1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62',
            'skill_git_blob_sha1': 'ceae92ab319216a68274168fba9b63b998b65997',
            'rules_repo': 'vercel-labs/web-interface-guidelines',
            'rules_commit': '434b7f91364665f2f733b310ec54809bf8f37937',
            'rules_git_blob_sha1': '3eb3a212b7b89493922ea418489d4c6f67ae8bd5',
            'dynamic_fetch_performed': False,
        },
        'reused_engines': list(dict.fromkeys(reused_list)),
        'reused_web_quality_findings': reused_wqa_ids,
        'delegated_accessibility': (
            {
                'skill': 'better-accessibility',
                'verdict': delegated_a11y.get('verdict'),
                'counts': delegated_a11y.get('counts'),
                'wcag_criteria_breakdown': delegated_a11y.get('wcag_criteria_breakdown'),
            }
            if delegated_a11y is not None
            else None
        ),
        'brand_and_commerce_guards': {
            'preserve_brand_identity': True,
            'arbitrary_redesign_prohibited': True,
            'detected_css_variables': sorted(detected_design_tokens),
            'protected_commerce_contracts': protected_contracts,
            'note': 'Las mejoras de interfaz deben reutilizar las variables CSS, colores, fuentes y contratos funcionales (js-*, data-store, LS.*, CartForm) del proyecto.',
        },
        'categories_summary': categories_summary,
        'verified_by_tool': verified_by_tool,
        'code_hypothesis': code_hypothesis,
        'requires_external_verification': requires_external_verification,
        'terse_file_line_findings': terse_report,
        'counts': {
            'verified_by_tool': len(verified_by_tool),
            'code_hypothesis': len(code_hypothesis),
            'requires_external_verification': len(requires_external_verification),
            'critical': sum(1 for i in verified_by_tool + code_hypothesis if i['severity'] == 'critical'),
            'high': sum(1 for i in verified_by_tool + code_hypothesis if i['severity'] == 'high'),
            'medium': sum(1 for i in verified_by_tool + code_hypothesis if i['severity'] == 'medium'),
            'low': sum(1 for i in verified_by_tool + code_hypothesis if i['severity'] == 'low'),
        },
        'limitations': [
            'Las reglas de Web Interface Guidelines se evalúan desde la versión estática fijada (commit 434b7f91364665f2f733b310ec54809bf8f37937); no se realizan descargas dinámicas.',
            'Las hipótesis de código (code_hypothesis) deben confirmarse en el DOM/CSS renderizado antes de modificar estilos compartidos.',
            'Ninguna recomendación autoriza rediseñar arbitrariamente la identidad visual de la marca ni alterar precios, variantes, carrito o checkout.',
        ],
    })


from .accessibility import (  # noqa: E402, F401
    audit_better_accessibility,
    contrast_ratio,
    propose_safe_accessibility_fixes,
)
