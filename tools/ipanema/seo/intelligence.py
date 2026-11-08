"""Correlación observable, prioridades explicadas y periodos compatibles (offline)."""
from __future__ import annotations

import datetime as dt
from collections import defaultdict
from urllib.parse import urlsplit

from ..core import IpanemaError, now
from .adapters import authorize_url
from .page_audit import page_key


def compare_periods(before, after):
    """Search Analytics rows, not an attribution model or complete traffic totals."""
    for field in ('project','domain','provider','operation'):
        if field in before or field in after:
            if before.get(field)!=after.get(field):raise IpanemaError('Observaciones de distinto proyecto/proveedor o alcance.')
    a, b = before.get('data', before), after.get('data', after)
    if 'rows' not in a or 'rows' not in b:
        raise IpanemaError('Faltan filas observadas; ausencia de conexión no equivale a cero tráfico.')
    fields = ('dimensions', 'filters', 'timezone', 'search_type', 'data_state', 'start_row', 'row_limit')
    differences = [f for f in fields if a.get(f) != b.get(f)]
    if differences:
        raise IpanemaError('Periodos incompatibles: ' + ', '.join(differences))
    windows = []
    for item in (a, b):
        try:
            start, end = [dt.date.fromisoformat(item['period'][k]) for k in ('startDate', 'endDate')]
        except (KeyError, TypeError, ValueError):
            raise IpanemaError('Faltan periodos ISO comprobables.') from None
        if end < start:
            raise IpanemaError('Periodo invertido.')
        windows.append((start, end))
    if (windows[0][1] - windows[0][0]) != (windows[1][1] - windows[1][0]):
        raise IpanemaError('Los periodos tienen distinta duración; normalizar antes de comparar.')
    def summary(item):
        rows = item['rows']
        if any(not isinstance(r, dict) or any(type(r.get(k)) not in (int, float) for k in ('clicks', 'impressions', 'position')) for r in rows):
            raise IpanemaError('Formato de métricas Search Analytics incompatible.')
        clicks = sum(r['clicks'] for r in rows); impressions = sum(r['impressions'] for r in rows)
        return {'returned_rows': len(rows), 'returned_clicks': clicks, 'returned_impressions': impressions,
                'ctr_returned_rows': clicks / impressions if impressions else None,
                'position_weighted_returned_rows': sum(r['position'] * r['impressions'] for r in rows) / impressions if impressions else None}
    sa, sb = summary(a), summary(b)
    change = {}
    for key in ('returned_clicks', 'returned_impressions', 'ctr_returned_rows', 'position_weighted_returned_rows'):
        x, y = sa[key], sb[key]
        change[key] = {'absolute': y - x if x is not None and y is not None else None,
                       'relative': (y - x) / x if x not in (None, 0) and y is not None else None}
    warnings=['Zona horaria no documentada; compatibilidad temporal no demostrada.'] if not a.get('timezone') else []
    if max(windows[0][0], windows[1][0]) <= min(windows[0][1], windows[1][1]):warnings.append('Los periodos se solapan.')
    return {'kind': 'seo-period-comparison', 'at': now(), 'before_period': a['period'], 'after_period': b['period'],
            'contract': {k: a.get(k) for k in fields}, 'before': sa, 'after': sb, 'changes': change,
            'warnings': warnings,
            'limitations': ['Solo filas devueltas: límites, anonimización y agregación pueden alterar los totales.',
                            'Un cambio temporal no demuestra que la corrección técnica causó tráfico o ventas.']}


def correlate(project, audits, observations, *, business_weights=None, corrections=None):
    business_weights = business_weights or {}; corrections = corrections or []
    pages = {}; unmatched = []; connections = []
    for audit in audits:
        if audit.get('project') != project.id:
            raise IpanemaError('Auditoría de otro proyecto.')
        authorize_url(project, audit['url'])
        key = page_key(audit['url'])
        pages[key] = {'url': audit['url'], 'page_type': audit['page_type'], 'classification_source': 'explicit_audit',
                      'technical_findings': audit.get('findings', []), 'components': audit.get('schema_sources', []),
                      'google_observations': [], 'search_rows': [], 'analytics_rows': [], 'corrections': [],
                      'audit_at': audit.get('at'), 'indexation': 'not_observed'}
    def attach(url, data, source):
        authorize_url(project, url)
        key = page_key(url)
        if key not in pages:
            unmatched.append({'url': url, 'source': source, 'reason': 'Sin auditoría: tipo de página no inferido solo por patrón.'})
            return
        pages[key]['google_observations'].append({'source': source, **data})
    for obs in observations:
        if obs.get('project') != project.id or obs.get('domain') != urlsplit(project.data['public_url']).hostname:
            raise IpanemaError('Observación Google ajena al proyecto/dominio.')
        connections.append({k: obs.get(k) for k in ('provider', 'operation', 'status', 'at', 'observed_at', 'live_connection_tested')})
        if obs.get('status') not in ('observed', 'imported_observation'):
            continue
        data = obs.get('data') or {}; provider, operation = obs.get('provider'), obs.get('operation')
        evidence_at = obs.get('observed_at') or obs.get('at')
        if provider == 'gsc' and operation == 'inspect_url':
            attach(data['url'], {'at': evidence_at, 'index_status': data.get('index_status', {})}, 'gsc_inspection_known_index')
            if page_key(data['url']) in pages:
                pages[page_key(data['url'])]['indexation'] = data.get('index_status', {}).get('coverageState', 'not_returned')
        elif provider == 'gsc' and operation == 'search_analytics':
            for row in data.get('rows', []):
                url = row.get('dimensions', {}).get('page')
                if not url:
                    continue  # Query-only reports cannot be assigned to a specific URL.
                attach(url, {'at': evidence_at, 'period': data.get('period'), 'row': row}, 'gsc_search_analytics')
                if page_key(url) in pages:
                    pages[page_key(url)]['search_rows'].append(row)
        elif provider == 'analytics':
            from urllib.parse import urljoin
            for row in data.get('rows', []):
                landing = row.get('dimensions', {}).get('landingPagePlusQueryString')
                if not landing or not landing.startswith('/') or landing.startswith('//'):
                    continue
                url = urljoin(project.data['public_url'], landing)
                attach(url, {'at': evidence_at, 'period': data.get('period'), 'row': row}, 'analytics_report')
                if page_key(url) in pages:
                    pages[page_key(url)]['analytics_rows'].append(row)
        elif provider == 'merchant':
            for product in data.get('products', []):
                attach(product['productAttributes']['link'], {'at': evidence_at, 'diagnostic': product.get('productStatus')}, 'merchant_product_status')
    for correction in corrections:
        if correction.get('project') != project.id:
            raise IpanemaError('Corrección sin proyecto coincidente.')
        authorize_url(project, correction.get('url', ''))
        key = page_key(correction['url'])
        if key in pages:
            pages[key]['corrections'].append({k: correction[k] for k in ('id', 'url', 'at', 'component', 'files', 'evidence', 'status') if k in correction})
    groups = defaultdict(list)
    for page in pages.values():
        for finding in page['technical_findings']:
            groups[finding['rule']].append((page, finding))
    priorities = []
    for rule, affected in groups.items():
        severity = max({'error': 4, 'warning': 2, 'recommendation': 1, 'optional': 0}.get(f['severity'], 0) for p, f in affected)
        urls = sorted({p['url'] for p, f in affected})
        impressions = sum(sum(r['impressions'] for r in p['search_rows']) for p, _ in {p['url']: (p, f) for p, f in affected}.values())
        business = max(float(business_weights.get(url, 1)) for url in urls)
        if not 0 <= business <= 5:
            raise IpanemaError('Pesos comerciales deben estar entre 0 y 5 y ser explícitos.')
        confidence = 'local_observation' if severity else 'optional_not_a_defect'
        # Transparent ordering aid, not an SEO score or promised return on investment.
        rank = severity * len(urls) * business
        priorities.append({'rule': rule, 'severity_weight': severity, 'affected_urls': urls, 'url_count': len(urls),
                           'returned_impressions_context': impressions, 'business_weight': business, 'confidence': confidence,
                           'triage_order_weight': rank, 'effort': 'requires_source_review', 'risk': 'requires_consumer_review',
                           'message': affected[0][1]['message'], 'potential_impact': 'Sin promesa de mejora; priorización revisable.',
                           'next_step': 'Relacionar fuente, revisar consumidores y probar corrección local antes/después.'})
    priorities.sort(key=lambda x: (x['triage_order_weight'], x['returned_impressions_context']), reverse=True)
    return {'kind': 'seo-intelligence', 'project': project.id, 'at': now(), 'connections': connections,
            'pages': list(pages.values()), 'unmatched_urls': unmatched, 'priorities': priorities,
            'hypotheses': ['Una señal de Google y un defecto local en la misma URL justifican investigar; no demuestran una causa única.'],
            'limitations': ['No se atribuye indexación ni tráfico al tema automáticamente.',
                            'Filas de varios periodos no son tráfico único; evitar sumar reportes solapados.',
                            'Profundidad/huérfanas necesitan un corpus de enlaces; Search Console no ofrece ese inventario completo.']}
