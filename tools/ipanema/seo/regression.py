"""Gates SEO offline sobre evidencias del mismo proyecto; nunca rastrea al comparar."""
from __future__ import annotations

from ..core import IpanemaError, now
from .adapters import authorize_url
from .crawl_policy import normalize


def _nodes(report):
    if report.get('kind') == 'seo-readiness-v4':
        return {report['node']['url']: report['node']}
    if report.get('kind') == 'seo-crawl-v4':
        return {n['url']: n for n in report['urls']}
    if report.get('kind') == 'seo-page-audit':
        return {report['url']: {'url': report['url'], 'status': report.get('http_status'),
            'canonical': report.get('canonical'), 'template_audit': report,
            'outgoing_links': [l['absolute'] for l in report.get('crawl', {}).get('links', [])],
            'indexability': {'state': 'noindex' if 'noindex' in report.get('robots_directives', '') else 'insufficient_evidence'},
            'pagination': {'active_controls_without_href': sum(not l.get('href') for l in report.get('crawl', {}).get('pagination_controls', []))}}}
    raise IpanemaError('Gate necesita auditorías SEO o crawler V4.')


def compare(project, before, after, *, important_urls=None, allow_removed=None):
    if any(r.get('project') != project.id for r in (before, after)):
        raise IpanemaError('No se comparan evidencias de proyectos distintos.')
    if before.get('kind') != after.get('kind'):
        raise IpanemaError('Los tipos de evidencia no son comparables.')
    a, b = _nodes(before), _nodes(after)
    for url in set(a) | set(b) | set(important_urls or []) | set(allow_removed or []):
        authorize_url(project, url)
    if set(a) and set(b) and normalize(next(iter(a))).split('/')[2] != normalize(next(iter(b))).split('/')[2]:
        raise IpanemaError('Origen distinto en el gate.')
    checks = []
    def check(name, passed, details, *, unknown=False):
        checks.append({'name': name, 'status': 'unknown' if unknown else 'passed' if passed else 'failed', 'details': details})
    important = {normalize(u) for u in (important_urls or a)}
    allowed = {normalize(u) for u in (allow_removed or [])}
    for url in sorted(important):
        old, new = a.get(url), b.get(url)
        if old is None:
            check(url + ':baseline', False, 'URL importante no observada en baseline', unknown=True)
            continue
        if new is None:
            check(url + ':capture', False, 'URL ausente de evidencia posterior; no equivale a eliminación real', unknown=True)
            continue
        check(url + ':http', not (old.get('status') == 200 and new.get('status') != 200), {'before': old.get('status'), 'after': new.get('status')})
        check(url + ':canonical', old.get('canonical') == new.get('canonical'), {'before': old.get('canonical'), 'after': new.get('canonical')})
        before_state, after_state = old.get('indexability', {}).get('state'), new.get('indexability', {}).get('state')
        check(url + ':noindex', not (before_state != 'noindex' and after_state == 'noindex'), after_state)
        check(url + ':robots', not (before_state != 'blocked_by_robots' and after_state == 'blocked_by_robots'), after_state)
        lost = set(old.get('outgoing_links', [])) - set(new.get('outgoing_links', [])) - allowed
        check(url + ':links', not lost, {'removed': sorted(lost), 'approved_removals': sorted(allowed)})
        old_audit, new_audit = old.get('template_audit', {}), new.get('template_audit', {})
        old_h1 = [h['text'] for h in old_audit.get('content', {}).get('headings', []) if h['level'] == 1]
        new_h1 = [h['text'] for h in new_audit.get('content', {}).get('headings', []) if h['level'] == 1]
        check(url + ':h1', old_h1 == new_h1, {'before': old_h1, 'after': new_h1})
        old_pagination, new_pagination = old.get('pagination', {}), new.get('pagination', {})
        check(url + ':pagination', new_pagination.get('active_controls_without_href', 0) <= old_pagination.get('active_controls_without_href', 0), new_pagination)
        old_errors = {(f['rule'], f['message']) for f in old_audit.get('findings', []) if f['severity'] == 'error'}
        new_errors = {(f['rule'], f['message']) for f in new_audit.get('findings', []) if f['severity'] == 'error'}
        check(url + ':schema_commerce', not (new_errors - old_errors), {'new_error_rules': sorted(rule for rule, _ in new_errors - old_errors),
              'scope': 'existing validator; prices verified only with authorized facts'})
        old_syntax = old_audit.get('structured_data', {}).get('states', {}).get('syntax_valid')
        new_syntax = new_audit.get('structured_data', {}).get('states', {}).get('syntax_valid')
        check(url + ':jsonld', not (old_syntax is True and new_syntax is not True), {'before': old_syntax, 'after': new_syntax})
        old_layer, new_layer = old.get('layers', {}), new.get('layers', {})
        no_js = new_layer.get('initial_to_no_js')
        if no_js is not None:
            check(url + ':no_js_links', not no_js['links_removed_after_js'], no_js['links_removed_after_js'])
        else:
            check(url + ':no_js_links', False, 'Sin captura no-JS; no se considera aprobado', unknown=True)
        main_layers = new_layer.get('main_content', {})
        no_js_main = main_layers.get('no_js')
        check(url + ':no_js_main_content', bool((no_js_main or {}).get('main_text_characters')),
              main_layers, unknown=no_js_main is None)
        check(url + ':href', new.get('navigation_without_href', 0) <= old.get('navigation_without_href', 0), new.get('navigation_without_href', 0))
    failed = [c for c in checks if c['status'] == 'failed']
    unknown = [c for c in checks if c['status'] == 'unknown']
    return {'kind': 'seo-regression-gate-v4', 'project': project.id, 'at': now(),
            'outcome': 'blocked' if failed else 'insufficient_evidence' if unknown else 'passed_scoped_checks',
            'checks': checks, 'remote_mutations': False, 'network_requests': 0,
            'limitations': ['No comparación causal de ventas ni prueba de Google.',
                            'Las URLs ausentes de un crawl parcial necesitan evidencia, no se declaran eliminadas.',
                            'Cambios intencionados de H1/canonical y eliminaciones requieren revisión; no se autoaprueban.']}
