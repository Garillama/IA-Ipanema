"""Clasificación observable y evidencia por plantilla, sin inferir el índice de Google."""
from __future__ import annotations

import hashlib
from html.parser import HTMLParser
import re
from urllib.parse import urlsplit

from .crawl_policy import normalize
from .extractor import VOID
from .page_audit import crawlable, snapshot_delta
from .robots import google_directive_evidence


class Content(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.stack, self.main, self.body = [], [], []
        self.body_class, self.main_seen, self.product_ids, self.times = '', False, set(), []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'body':
            self.body_class = a.get('class', '')
        if tag == 'main':
            self.main_seen = True
        if tag == 'time' and a.get('datetime'):
            self.times.append(a['datetime'])
        if a.get('data-product-id') and re.fullmatch(r'[0-9]{1,30}', a['data-product-id']):
            self.product_ids.add(a['data-product-id'])
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in self.stack:
            self.stack = self.stack[:len(self.stack) - 1 - self.stack[::-1].index(tag)]

    def handle_data(self, text):
        if any(t in self.stack for t in ('script', 'style', 'template', 'head', 'nav', 'footer', 'header')):
            return
        if 'body' in self.stack or not self.stack:
            self.body.append(text)
        if 'main' in self.stack:
            self.main.append(text)

    def evidence(self):
        text = ' '.join(' '.join(self.main if self.main_seen else self.body).split())
        soft = bool(re.search(r'\b(?:404|p[aá]gina no encontrada|page not found|producto no encontrado)\b', text[:1000], re.I))
        return {'main_present': self.main_seen, 'main_text_characters': len(text),
                'main_text_sha256': hashlib.sha256(text.encode()).hexdigest() if text else None,
                'soft_404_candidate': soft, 'body_class': self.body_class,
                'product_ids': sorted(self.product_ids), 'declared_times': self.times[:20]}


def page_type(url, content):
    classes = content.get('body_class', '').split()
    for marker, kind in [('template-blog-post', 'post'), ('template-product', 'product'),
                         ('template-category', 'category'), ('template-blog', 'blog'),
                         ('template-home', 'home'), ('template-search', 'search'), ('template-404', '404')]:
        if marker in classes:
            return kind, 'observed_body_class'
    path = urlsplit(url).path
    if path == '/':
        return 'home', 'url_root'
    if re.search(r'/blog/posts/', path):
        return 'post', 'url_heuristic'
    if re.search(r'/productos?/[^/]+', path):
        return 'product', 'url_heuristic'
    return 'page', 'fallback_needs_template_evidence'


def classify(snapshot, *, googlebot_allowed=None, robots_known=False, content=None):
    status = snapshot.get('status')
    canonical = snapshot.get('canonical', [])
    reasons = []
    robots_evidence = None
    if status in (301, 302, 303, 307, 308):
        state = 'redirected'
    elif status in (404, 410):
        state = 'not_found'
    elif status is not None and 500 <= status < 600:
        state = 'server_error'
    elif googlebot_allowed is False:
        state = 'blocked_by_robots'
    elif status != 200:
        state = 'insufficient_evidence'
    else:
        meta = snapshot.get('meta', {})
        robots_evidence = google_directive_evidence(meta, snapshot.get('headers', {}).get('x-robots-tag', ''))
        if robots_evidence['noindex']:
            state = 'noindex'
        elif robots_evidence['relevant_errors']:
            state = 'insufficient_evidence'
            reasons.append('malformed_robots_directives')
        elif len(canonical) > 1:
            state = 'insufficient_evidence'
            reasons.append('ambiguous_canonical')
        elif canonical:
            try:
                state = 'canonicalized' if normalize(canonical[0]) != normalize(snapshot['url']) else 'indexable_candidate'
            except ValueError:
                state = 'insufficient_evidence'
                reasons.append('invalid_canonical')
        else:
            state = 'indexable_candidate'
        if state == 'indexable_candidate' and (not robots_known or googlebot_allowed is not True):
            state = 'insufficient_evidence'
            reasons.append('robots_not_verified')
        if state == 'indexable_candidate' and content is not None:
            if content.get('soft_404_candidate') or not content.get('main_text_characters'):
                state = 'insufficient_evidence'
                reasons.append('soft404_or_content_needs_evidence')
    return {'state': state, 'reasons': reasons, 'robots_evidence': robots_evidence, 'indexation_observed': False,
            'google_selected_canonical': None, 'evidence_scope': 'technical_observation_not_google_index'}


def layers(initial, rendered=None, no_js=None):
    result = {'rendered_available': rendered is not None, 'no_js_available': no_js is not None,
              'googlebot_rendering_tested': False, 'initial_to_rendered': None, 'initial_to_no_js': None}
    for name, other in [('initial_to_rendered', rendered), ('initial_to_no_js', no_js)]:
        if other is not None:
            delta = snapshot_delta(initial, other)
            delta.update({'canonical_before': initial['canonical'], 'canonical_after': other['canonical'],
                          'headings_before': initial['headings'], 'headings_after': other['headings']})
            result[name] = delta
    return result


def pagination(snapshot):
    controls = [l for l in snapshot.get('links', []) if (l.get('context', {}).get('pagination') or set(l.get('rel', '').split()) & {'next', 'prev'})
                and not l.get('disabled') and not l.get('action_hint')]
    links = [l['absolute'] for l in controls if crawlable(l) and not l.get('context', {}).get('hidden')]
    rel = [l for l in snapshot.get('links_rel', []) if set(l['rel'].split()) & {'next', 'prev'} and l.get('href')]
    actions_without_href = [l for l in controls if not crawlable(l)]
    return {'observed_links': sorted(set(links)), 'head_rel_links': rel,
            'active_controls_without_href': len(actions_without_href) + sum(not b['disabled'] for b in snapshot.get('pagination_buttons', [])),
            'state': 'missing_crawlable_links' if (actions_without_href or any(not b['disabled'] for b in snapshot.get('pagination_buttons', []))) and not links else 'observed_links' if links else 'needs_evidence',
            'continuity': 'needs_multi_page_evidence', 'native_contract': 'observed_hrefs_only_no_invented_routes'}


def template_checks(snapshot, kind, content, audit):
    """Inventario por plantilla: ausencia no inventa datos ni obligación de Schema."""
    from .schema_graph import entities_from_snapshot
    entities = entities_from_snapshot(snapshot)
    products = [e['obj'] for e in entities if 'Product' in e['types'] or 'ProductGroup' in e['types']]
    offers = [e['obj'] for e in entities if 'Offer' in e['types'] or 'AggregateOffer' in e['types']]
    articles = [e['obj'] for e in entities if 'Article' in e['types'] or 'BlogPosting' in e['types']]
    types = sorted({t for e in entities for t in e['types']})
    checks = {'title': snapshot['title'], 'meta_description': snapshot['meta'].get('description', []),
              'h1': [h['text'] for h in snapshot['headings'] if h['level'] == 1],
              'canonical': snapshot['canonical'], 'schema_types': types,
              'navigation_links': sum(crawlable(l) for l in snapshot['links']),
              'main_content': content, 'source': 'observed_markup_not_commercial_truth'}
    if kind in ('category', 'blog', 'search'):
        checks.update({'pagination': pagination(snapshot), 'linked_item_identifiers': content.get('product_ids'),
                       'filter_sort_contract': 'needs_native_event_and_url_evidence'})
    if kind == 'product':
        checks.update({'declared_offer_values': [{k: o[k] for k in ('price', 'lowPrice', 'highPrice', 'priceCurrency', 'availability') if k in o} for o in offers],
                       'declared_skus': [p['sku'] for p in products if p.get('sku')],
                       'variants': [p.get('hasVariant') for p in products if p.get('hasVariant')],
                       'images': snapshot['images'], 'breadcrumbs_observed': 'BreadcrumbList' in types,
                       'visible_price_truth': audit['structured_data']['states']['consistency'],
                       'price_contract': 'native/authorized facts required; no price/stock inferred from buttons'})
    if kind == 'post':
        checks.update({'declared_authors': [a['author'] for a in articles if a.get('author')],
                       'declared_published_dates': [a['datePublished'] for a in articles if a.get('datePublished')],
                       'declared_modified_dates': [a['dateModified'] for a in articles if a.get('dateModified')],
                       'date_author_truth': 'declared_not_editorially_verified'})
    return checks


def readiness(record, audit=None, *, rendered=None, no_js=None):
    status = record.get('status')
    idx = record.get('indexability', {})
    checks = []
    def add(name, passed, critical, basis):
        checks.append({'name': name, 'status': 'unknown' if passed is None else 'passed' if passed else 'failed',
                       'critical': critical, 'evidence': basis})
    add('http_access', None if status is None else status == 200, True, status)
    add('indexability', idx.get('state') == 'indexable_candidate' if idx.get('state') not in (None, 'insufficient_evidence') else None, True, idx)
    add('main_content', bool(record.get('content', {}).get('main_text_characters')), True, 'text length/hash, not tags counted')
    add('crawlable_navigation', bool(record.get('outgoing_links')), record.get('page_type') in ('home', 'category', 'blog'), 'observed href targets')
    add('sitemap_membership', record.get('in_sitemap') if record.get('sitemap_checked') else None, False, 'native sitemap inventory')
    findings = (audit or {}).get('findings', [])
    add('structured_data', not any(f['severity'] == 'error' for f in findings) if audit is not None else None, True, 'existing SEO validator A-D, limits preserved')
    paginated = record.get('page_type') in ('category', 'blog', 'search')
    add('pagination', False if paginated and record.get('pagination', {}).get('state') == 'missing_crawlable_links' else None if paginated else True, paginated, record.get('pagination'))
    add('render_comparison', True if rendered is not None else None, False, 'capture supplied, not Googlebot')
    add('no_js_navigation', not no_js.get('links_removed', []) if no_js is not None else None, True, 'no-JS capture required')
    main_layers = record.get('layers', {}).get('main_content', {})
    no_js_main = main_layers.get('no_js')
    add('no_js_main_content', bool(no_js_main.get('main_text_characters')) if no_js_main is not None else None,
        True, 'extracted main text in no-JS DOM; hidden/visual state requires browser QA')
    failed = [c['name'] for c in checks if c['critical'] and c['status'] == 'failed']
    unknown = [c['name'] for c in checks if c['critical'] and c['status'] == 'unknown']
    known = [c for c in checks if c['status'] != 'unknown']
    return {'checks': checks, 'critical_blockers': failed, 'required_evidence_missing': unknown,
            'approval': 'blocked' if failed else 'insufficient_evidence' if unknown else 'passed_scoped_checks',
            'score': round(100 * sum(c['status'] == 'passed' for c in known) / len(checks)),
            'coverage': round(len(known) / len(checks), 3),
            'meaning': 'diagnostic evidence completion, not Google ranking; blockers override score'}
