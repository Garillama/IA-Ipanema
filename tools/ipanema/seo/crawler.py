"""Crawler de lectura integrado con Project, extractor y auditor SEO existentes."""
from __future__ import annotations

from collections import Counter, defaultdict, deque
import csv
import hashlib
import json
from urllib.parse import urljoin, urlsplit

from ..core import IpanemaError, now
from .adapters import authorize_url
from .crawl_policy import AGENT, Fetcher, Policy, normalize
from .extractor import extract
from .indexability import Content, classify, layers, page_type, pagination, readiness, template_checks
from .page_audit import audit_snapshot, crawlable
from .sitemaps import parse_sitemap
from .robots import Robots


def _public_link(link):
    """Filtra antes de persistir. Los controles nativos sin href se conservan."""
    if not link.get('href') or link['href'].startswith('#'):
        return link
    if urlsplit(link.get('absolute') or link['href']).scheme not in ('http', 'https'):
        return None
    try:
        value = normalize(link.get('absolute') or link['href'])
        from .crawl_policy import PRIVATE, ACTIONS
        from urllib.parse import unquote
        if PRIVATE.search(unquote(urlsplit(value).path)) or ACTIONS.search(value):
            return None
    except ValueError:
        return None
    return {**link, 'href': value, 'absolute': value}


def graph(nodes, edges, home, sitemap_urls, *, complete=False):
    incoming, outgoing, adjacency = defaultdict(set), defaultdict(set), defaultdict(set)
    for edge in edges:
        source, target = edge['source'], edge['target']
        incoming[target].add(source)
        outgoing[source].add(target)
        if edge.get('relation') in ('html', 'redirect'):
            adjacency[source].add(target)
    depths, queue = {home: 0}, deque([home])
    while queue:
        source = queue.popleft()
        for target in sorted(adjacency[source]):
            if target not in depths:
                depths[target] = depths[source] + 1
                queue.append(target)
    by_url = {n['url']: n for n in nodes}
    broken = [e for e in edges if by_url.get(e['target'], {}).get('status') in (404, 410)]
    site = set(sitemap_urls)
    return {'nodes': [{**n, 'depth_from_home': depths.get(n['url']), 'incoming': sorted(incoming[n['url']]),
                       'outgoing': sorted(outgoing[n['url']])} for n in nodes],
            'edges': edges, 'broken_internal_links': broken,
            'sitemap_not_discovered_from_home': sorted(site - set(depths)),
            'potential_orphans': [{'url': u, 'reason': 'sitemap_url_not_reached_in_observed_home_graph',
                                   'page_type': by_url.get(u, {}).get('page_type', 'unknown')} for u in sorted(site - set(depths))],
            'confirmed_orphans': [], 'complete_for_policy': complete,
            'orphan_scope': 'Candidates within observed inventory; partial crawl is not proof of orphanhood',
            'duplicate_content_candidates': _duplicates(nodes)}


def _duplicates(nodes):
    hashes = defaultdict(list)
    for node in nodes:
        h = node.get('content', {}).get('main_text_sha256')
        if h and node.get('status') == 200:
            hashes[h].append(node['url'])
    return [{'urls': urls, 'basis': 'same_extracted_main_text_hash_not_google_deduplication'}
            for urls in hashes.values() if len(urls) > 1]


def _sanitized_audit(snapshot, project, kind):
    snapshot['links'] = [clean for link in snapshot['links'] if (clean := _public_link(link)) is not None]
    # Raw JSON-LD is used by validator in memory, not retained by crawl export.
    return audit_snapshot(project, snapshot, kind)


def crawl(project, *, limits=None, allow_network=False, transport=None, captures=None, clock=None, sleep=None):
    authorize_url(project, project.data['public_url'])
    policy = Policy(project.data['public_url'], limits)
    options = {k: v for k, v in [('clock', clock), ('sleep', sleep)] if v is not None}
    fetcher = Fetcher(policy, allow_network=allow_network, transport=transport, **options)
    result = {'kind': 'seo-crawl-v4', 'project': project.id, 'at': now(), 'home': policy.home,
              'source': 'offline_injected_transport' if transport else 'live_read_only_http',
              'urls': [], 'edges': [], 'sitemaps': [], 'sitemap_entries': [], 'errors': [], 'excluded': [],
              'google': {'connection': 'not_consulted', 'indexation_observed': False},
              'robots': {'known': False, 'status': None}, 'remote_mutations': False}
    robot = Robots()
    robots_text, robots_known = None, False
    def excluded(reason, source=None):
        result['excluded_total'] = result.get('excluded_total', 0) + 1
        if len(result['excluded']) < 2000:
            result['excluded'].append({'reason': reason, 'source': source})
    def allowed(url):
        return robots_known and robot.can_fetch(AGENT, url)
    try:
        robots_url = urljoin(policy.home, 'robots.txt')
        # Redirects de robots se validan sin reutilizar reglas de otro origen.
        seen_robots = set()
        for _ in range(policy.limits.max_redirects + 1):
            if robots_url in seen_robots:
                raise IpanemaError('Ciclo de redirección en robots.')
            seen_robots.add(robots_url)
            response = fetcher.get(robots_url, document=True)
            if fetcher.stop_reason:
                break
            if response['status'] in (301, 302, 303, 307, 308):
                robots_url = policy.check(urljoin(robots_url, response['headers'].get('location', '')), document=True)
                continue
            robots_text = response['body'].decode('utf-8', 'replace') if response['status'] == 200 else '' if response['status'] in (404, 410) else None
            robots_known = robots_text is not None
            if robots_known:
                robot.parse(robots_text.splitlines())
                robots_known = not robot.errors
            result['robots'] = {'known': robots_known, 'status': response['status'], 'url': robots_url,
                                'sha256': hashlib.sha256(response['body']).hexdigest(),
                                'crawler_agent': AGENT, 'googlebot_is_separate': True}
            delay = robot.crawl_delay(AGENT) if robots_known else None
            rate = robot.request_rate_interval(AGENT) if robots_known else 0
            fetcher.interval = max(fetcher.interval, delay or 0, rate)
            break
        if not robots_known and not fetcher.stop_reason:
            result['errors'].append({'operation': 'robots', 'reason': 'robots_unavailable_no_crawl'})
        # Solo metadata; jamás usa sitemap como semillas de navegación.
        sitemap_queue = deque((url, 0) for url in ((robot.site_maps() or [urljoin(policy.home, 'sitemap.xml')]) if robots_known else []))
        sitemap_seen, sitemap_urls, normalized_sitemap = set(), [], set()
        while sitemap_queue and len(sitemap_seen) < policy.limits.max_sitemaps and not fetcher.stop_reason:
            raw_url, depth = sitemap_queue.popleft()
            try:
                url = policy.check(raw_url, document=True)
                if url in sitemap_seen:
                    continue
                sitemap_seen.add(url)
                if not allowed(url):
                    result['errors'].append({'operation': 'sitemap', 'url': url, 'reason': 'blocked_by_robots'})
                    continue
                response = fetcher.get(url, document=True)
                if fetcher.stop_reason:
                    result['sitemaps'].append({'url': url, 'status': response['status']})
                    break
                if response['status'] in (301, 302, 303, 307, 308):
                    target = policy.check(urljoin(url, response['headers'].get('location', '')), document=True)
                    result['sitemaps'].append({'url': url, 'status': response['status'], 'redirect': target})
                    if depth < policy.limits.max_redirects:
                        sitemap_queue.append((target, depth + 1))
                    continue
                if response['status'] != 200:
                    result['sitemaps'].append({'url': url, 'status': response['status']})
                    continue
                parsed = parse_sitemap(response['body'], source=url, max_entries=policy.limits.max_sitemap_entries,
                                       max_bytes=policy.limits.max_bytes)
                result['sitemaps'].append({k: v for k, v in parsed.items() if k != 'entries'})
                for entry in parsed['entries']:
                    try:
                        target = policy.check(entry['url'], document=parsed['kind'] == 'sitemapindex')
                    except ValueError:
                        excluded('sitemap_target_outside_policy', url)
                        continue
                    if parsed['kind'] == 'sitemapindex':
                        if depth < 3:
                            sitemap_queue.append((target, depth + 1))
                        else:
                            result['errors'].append({'operation': 'sitemap', 'reason': 'sitemap_depth_limit'})
                    else:
                        result['sitemap_entries'].append({**entry, 'url': target})
                        if target not in normalized_sitemap:
                            normalized_sitemap.add(target)
                            sitemap_urls.append(target)
            except IpanemaError as exc:
                result['errors'].append({'operation': 'sitemap', 'reason': str(exc)})
        if sitemap_queue:
            result['errors'].append({'operation': 'sitemap', 'reason': 'sitemap_document_limit'})
        queue, queued, seen, path_variants = deque([(policy.home, 0, 'home', 0)]), {policy.home}, set(), defaultdict(set)
        navigation_exhausted = False
        # Chequeos de URLs adicionales del sitemap son independientes del BFS de home.
        sitemap_checks_added = False
        while robots_known and not fetcher.stop_reason and len(seen) < policy.limits.max_urls:
            if not queue:
                navigation_exhausted = True
                if sitemap_checks_added:
                    break
                sitemap_checks_added = True
                for url in sitemap_urls:
                    if url not in queued:
                        queue.append((url, None, 'sitemap_check', 0))
                        queued.add(url)
                if not queue:
                    break
            url, depth, discovery, redirects = queue.popleft()
            if url in seen:
                continue
            seen.add(url)
            path_variants[urlsplit(url).path].add(url)
            node = {'url': url, 'discovery': discovery, 'crawl_depth': depth, 'in_sitemap': url in normalized_sitemap,
                    'sitemap_checked': bool(result['sitemaps']) and not any(s.get('status', 200) != 200 or s.get('errors') or not s.get('kind') for s in result['sitemaps'])}
            result['urls'].append(node)
            google_allowed = robot.can_fetch('Googlebot', url)
            node['robots'] = {'crawler_allowed': allowed(url), 'googlebot_allowed': google_allowed}
            if not allowed(url):
                node.update({'status': None, 'indexability': classify({'url': url}, googlebot_allowed=google_allowed, robots_known=True),
                             'error': 'blocked_by_robots_for_audit_agent'})
                continue
            try:
                response = fetcher.get(url)
                node['status'] = response['status']
                node['indexability'] = classify({'url': url, 'status': response['status']}, googlebot_allowed=google_allowed, robots_known=True)
                node['headers'] = {k: v for k, v in response['headers'].items() if k in ('content-type', 'x-robots-tag')}
                node['html_sha256'] = hashlib.sha256(response['body']).hexdigest()
                if response['status'] in (301, 302, 303, 307, 308):
                    target = policy.check(urljoin(url, response['headers'].get('location', '')))
                    node['redirect'] = target
                    result['edges'].append({'source': url, 'target': target, 'text': '', 'relation': 'redirect'})
                    if target not in queued and redirects < policy.limits.max_redirects:
                        queued.add(target)
                        queue.append((target, depth, 'redirect', redirects + 1))
                    elif target in seen or redirects >= policy.limits.max_redirects:
                        node['redirect_limit_or_cycle'] = True
                snap = extract(response['body'].decode('utf-8', 'replace') if response['status'] == 200 and not fetcher.stop_reason else '',
                               url, status=response['status'], headers=node['headers'])
                node['indexability'] = classify(snap, googlebot_allowed=google_allowed, robots_known=True)
                if response['status'] != 200 or fetcher.stop_reason:
                    continue
                if 'html' not in node['headers'].get('content-type', 'text/html'):
                    node['error'] = 'non_html_document'
                    node['indexability']['state'] = 'insufficient_evidence'
                    continue
                content = Content(response['body'].decode('utf-8', 'replace')).evidence()
                node['content'] = content
                node['page_type'], node['type_basis'] = page_type(url, content)
                node['indexability'] = classify(snap, googlebot_allowed=google_allowed, robots_known=True, content=content)
                node['title'], node['canonical'] = snap['title'], snap['canonical']
                node['pagination'] = pagination(snap)
                node['template_audit'] = _sanitized_audit(snap, project, node['page_type'])
                node['template_checks'] = template_checks(snap, node['page_type'], content, node['template_audit'])
                node['navigation_without_href'] = sum(not l.get('href') and not l.get('action_hint') and not l.get('disabled') for l in snap['links'])
                node['outgoing_links'] = []
                for link in snap['links']:
                    if not crawlable(link):
                        continue
                    try:
                        target = policy.check(link['absolute'])
                    except ValueError:
                        excluded('link_outside_policy', url)
                        continue
                    node['outgoing_links'].append(target)
                    if len(result['edges']) >= policy.limits.max_edges:
                        excluded('edge_budget', url)
                        node['links_truncated'] = True
                        break
                    result['edges'].append({'source': url, 'target': target, 'text': link.get('text', '')[:200],
                                            'relation': 'html', 'context': link.get('context', {})})
                    if depth is None or target in queued:
                        continue
                    if len(queued) >= policy.limits.max_discovered_urls:
                        excluded('discovery_budget', url)
                        continue
                    if depth >= policy.limits.max_depth:
                        excluded('depth_limit', url)
                        continue
                    path = urlsplit(target).path
                    if len(path_variants[path]) >= policy.limits.max_variants_per_path:
                        excluded('query_variants_limit', url)
                        continue
                    path_variants[path].add(target)
                    queued.add(target)
                    queue.append((target, depth + 1, 'html', 0))
                supplied = (captures or {}).get(url, {})
                rendered = extract(supplied['rendered'], url) if supplied.get('rendered') is not None else None
                no_js = extract(supplied['no_js'], url) if supplied.get('no_js') is not None else None
                node['layers'] = layers(snap, rendered, no_js)
                node['readiness'] = readiness(node, node['template_audit'], rendered=rendered,
                    no_js={'links_removed': node['layers']['initial_to_no_js']['links_removed_after_js']} if no_js is not None else None)
            except (IpanemaError, ValueError) as exc:
                node['error'] = str(exc)
                node.setdefault('status', None)
                node.setdefault('indexability', {'state': 'insufficient_evidence', 'indexation_observed': False})
        result['navigation_queue_remaining'] = len(queue)
        result['navigation_exhausted_before_sitemap_checks'] = navigation_exhausted
        result['sitemap_urls'] = sitemap_urls
    except (IpanemaError, ValueError) as exc:
        result['errors'].append({'operation': 'crawl', 'reason': str(exc)})
    result['provenance'] = fetcher.provenance()
    result['sitemap_urls'] = result.get('sitemap_urls', [])
    complete = bool(robots_known and not fetcher.stop_reason and not result['errors'] and
                    not any(n.get('error') for n in result['urls']) and
                    not result.get('navigation_queue_remaining') and
                    not any(x['reason'] in ('depth_limit', 'query_variants_limit', 'discovery_budget', 'edge_budget') for x in result['excluded']))
    result['graph'] = graph(result['urls'], result['edges'], policy.home, result['sitemap_urls'], complete=complete)
    result['coverage_by_type'] = dict(Counter(n.get('page_type', 'unknown') for n in result['urls']))
    result['indexability_counts'] = dict(Counter(n.get('indexability', {}).get('state', 'insufficient_evidence') for n in result['urls']))
    result['state'] = 'stopped' if fetcher.stop_reason else 'complete_for_policy' if complete else 'partial'
    result['backlog'] = backlog(result)
    result['limitations'] = ['No es Googlebot ni prueba de indexación; DOM solo si se aporta captura explícita.',
                            'Concurrencia real 1, límites explícitos. Sin JS de terceros durante el rastreo HTTP.',
                            'No se inventan rutas de paginación. Búsqueda/filtros/privadas/activos quedan fuera de la política.',
                            'Orfandad/soft404/duplicación son candidatos en un inventario posiblemente parcial.',
                            'Métricas LCP/CLS/TBT/axe se obtienen con QA existente selectivo; sin INP de campo no se afirma INP.']
    return result


def backlog(result):
    rows = []
    for node in result['urls']:
        url = node['url']
        if node.get('status') in (404, 410) or (node.get('status') or 0) >= 500:
            rows.append({'priority': 'P1', 'url': url, 'issue': 'http_error', 'component': 'linked destination / platform response', 'action': 'Verify destination and real incoming links; never delete automatically'})
        if node.get('pagination', {}).get('state') == 'missing_crawlable_links':
            rows.append({'priority': 'P1', 'url': url, 'issue': 'pagination_without_href', 'component': 'native pagination / hybridScroll candidate, attribution needs source check', 'action': 'Verify native href/cursor, JS events, filters and no-JS continuity before proposing a patch'})
        for finding in node.get('template_audit', {}).get('findings', []):
            rows.append({'priority': finding.get('priority', 'P2'), 'url': url, 'issue': finding['rule'],
                         'component': 'template/theme/platform source requires verification', 'action': finding.get('fix') or finding['message']})
    return sorted(rows, key=lambda row: (row['priority'], row['url'], row['issue']))


def save_csv(path, rows, fields):
    def cell(value):
        text = json.dumps(value, ensure_ascii=False) if isinstance(value, (list, dict)) else str(value) if value is not None else ''
        return "'" + text if text.lstrip().startswith(('=', '+', '-', '@', '\t', '\r')) else text
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows({key: cell(row.get(key)) for key in fields} for row in rows)


def export(run, result):
    save_csv(run / 'urls.csv', [{'url': n['url'], 'status': n.get('status'), 'page_type': n.get('page_type'),
              'indexability': n.get('indexability', {}).get('state'), 'canonical': n.get('canonical'),
              'depth': n.get('depth_from_home'), 'in_sitemap': n.get('in_sitemap'), 'incoming': n.get('incoming'),
              'readiness': n.get('readiness', {}).get('approval')} for n in result['graph']['nodes']],
              ['url', 'status', 'page_type', 'indexability', 'canonical', 'depth', 'in_sitemap', 'incoming', 'readiness'])
    save_csv(run / 'edges.csv', result['edges'], ['source', 'target', 'text', 'relation'])
    save_csv(run / 'sitemap.csv', result['sitemap_entries'], ['url', 'source_sitemap', 'lastmod', 'lastmod_state'])
    save_csv(run / 'backlog.csv', result['backlog'], ['priority', 'url', 'issue', 'component', 'action'])
