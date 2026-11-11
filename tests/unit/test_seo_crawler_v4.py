import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tests.support import make_project
from ipanema.core import IpanemaError, Project
from ipanema.seo.crawl_policy import Fetcher, Limits, Policy, normalize, public_addresses
from ipanema.seo.crawler import crawl, export
from ipanema.seo.extractor import extract
from ipanema.seo.indexability import Content, classify, layers, readiness
from ipanema.seo.robots import Robots, google_directives

HOME = 'https://example.invalid/'


def doc(path='/', links='', *, kind='page', extra=''):
    return f'<html><head><title>Fixture {path}</title><link rel="canonical" href="{HOME.rstrip("/")}{path}">{extra}</head><body class="template-{kind}"><main><h1>Fixture {path}</h1><p>Main text {path}</p>{links}</main></body></html>'


class FakeClock:
    def __init__(self): self.value = 0
    def __call__(self): return self.value
    def sleep(self, seconds): self.value += seconds


class FixtureTransport:
    def __init__(self, pages): self.pages, self.calls = pages, []
    def __call__(self, url, **kwargs):
        self.calls.append(url)
        value = self.pages.get(url, {'status': 404, 'body': '', 'headers': {}})
        return {'headers': {'content-type': 'text/html'}, **value}


class PolicyV4(unittest.TestCase):
    def test_normalization_preserves_real_parameters(self):
        self.assertEqual(normalize('/blog?page=2#x', HOME), HOME + 'blog?page=2')
        self.assertEqual(normalize(HOME + 'x?b=2&a=1'), HOME + 'x?a=1&b=2')

    def test_policy_private_external_actions_filters_and_secrets(self):
        policy = Policy(HOME)
        for url in ['http://example.invalid/', 'file:///etc/passwd', 'https://other.invalid/', '/account', '/%2561ccount', '/cart/add', '/checkout/', '/admin', '/x?token=abc', '/x?sort_by=price', '/search?q=x', '/x?page=0', '/x?page=2&page=3', 'https://user:pass@example.invalid/']:
            with self.subTest(url=url), self.assertRaises((IpanemaError, ValueError)):
                policy.check(url)
        self.assertEqual(policy.check('/blog?page=2'), HOME + 'blog?page=2')

    def test_permissions_limits_stop_and_rate(self):
        with self.assertRaises(IpanemaError): Fetcher(Policy(HOME))
        for limits in [Limits(max_urls=0), Limits(concurrency=2), Limits(requests_per_second=float('nan'))]:
            with self.assertRaises(IpanemaError): Policy(HOME, limits)
        clock = FakeClock(); transport = FixtureTransport({HOME: {'status': 403}})
        f = Fetcher(Policy(HOME), transport=transport, clock=clock, sleep=clock.sleep)
        self.assertEqual(f.get(HOME)['status'], 403)
        with self.assertRaises(IpanemaError): f.get(HOME)
        self.assertEqual(len(transport.calls), 1)
        f = Fetcher(Policy(HOME, Limits(max_requests=2)), transport=FixtureTransport({}), clock=clock, sleep=clock.sleep)
        f.get(HOME); f.get(HOME + 'a')
        self.assertEqual(clock.value, 2)
        with self.assertRaises(IpanemaError): f.get(HOME + 'b')

    def test_ip_validation_rejects_mixed_private_dns(self):
        for ip in ['127.0.0.1', '169.254.169.254', '10.1.1.1', '::1', '192.0.2.1']:
            with patch('socket.getaddrinfo', return_value=[(2, 1, 6, '', (ip, 443))]), self.assertRaises(IpanemaError):
                public_addresses('example.invalid')
        with patch('socket.getaddrinfo', return_value=[(2, 1, 6, '', ('8.8.8.8', 443))]):
            self.assertEqual(public_addresses('example.invalid'), ['8.8.8.8'])

    def test_captcha_and_deadline(self):
        clock = FakeClock()
        f = Fetcher(Policy(HOME), transport=FixtureTransport({HOME: {'status': 200, 'body': '<title>Just a moment</title>'}}), clock=clock, sleep=clock.sleep)
        f.get(HOME); self.assertEqual(f.stop_reason, 'access_challenge')
        f = Fetcher(Policy(HOME, Limits(max_seconds=1)), transport=FixtureTransport({}), clock=clock, sleep=clock.sleep)
        f.get(HOME)
        with self.assertRaises(IpanemaError): f.get(HOME)
        self.assertEqual(f.stop_reason, 'time_budget')


class RobotsV4(unittest.TestCase):
    def test_groups_wildcards_end_anchor_longest_and_allow_tie(self):
        r = Robots(); r.parse('User-agent: *\nDisallow: /\nUser-agent: Googlebot\nDisallow: /*?sort=\nAllow: /good\nDisallow: /good/private\nAllow: /good/private/public$'.splitlines())
        self.assertFalse(r.can_fetch('IAIpanemaAudit/4', HOME))
        self.assertTrue(r.can_fetch('Googlebot', HOME + 'good'))
        self.assertFalse(r.can_fetch('Googlebot', HOME + 'good/private/x'))
        self.assertTrue(r.can_fetch('Googlebot', HOME + 'good/private/public'))
        self.assertFalse(r.can_fetch('Googlebot', HOME + 'good/private/public/more'))
        self.assertFalse(r.can_fetch('Googlebot', HOME + 'x?sort=price'))
        r = Robots(); r.parse(['User-agent: *', 'Disallow: /a', 'Allow: /a'])
        self.assertTrue(r.can_fetch('Googlebot', HOME + 'a'))

    def test_octets_unknown_and_user_agent_scoped_headers(self):
        r = Robots(); r.parse(['User-agent: *', 'Disallow: /caf%C3%A9$', 'Disallow: /%61bc$'])
        self.assertFalse(r.can_fetch('Googlebot', HOME + 'café'))
        self.assertFalse(r.can_fetch('Googlebot', HOME + 'abc'))
        self.assertTrue(r.can_fetch('Googlebot', HOME + 'abcd'))
        r = Robots(); r.parse(['User-agent: *', 'Disallow: bad'])
        self.assertTrue(r.errors); self.assertFalse(r.can_fetch('Googlebot', HOME))
        self.assertNotIn('noindex', google_directives({}, 'otherbot: noindex, nofollow, googlebot: index'))
        self.assertIn('noindex', google_directives({}, 'googlebot: noindex, nofollow'))
        self.assertIn('noindex', google_directives({}, ['otherbot: noindex', 'noindex']))


class IndexabilityV4(unittest.TestCase):
    def test_states_and_unknown_robots(self):
        for status, expected in [(301, 'redirected'), (302, 'redirected'), (404, 'not_found'), (500, 'server_error'), (403, 'insufficient_evidence')]:
            self.assertEqual(classify(extract('', HOME, status=status))['state'], expected)
        snap = extract(doc(), HOME, status=200)
        self.assertEqual(classify(snap)['state'], 'insufficient_evidence')
        self.assertEqual(classify(snap, googlebot_allowed=False, robots_known=True)['state'], 'blocked_by_robots')
        self.assertEqual(classify(snap, googlebot_allowed=True, robots_known=True)['state'], 'indexable_candidate')
        self.assertFalse(classify(snap, googlebot_allowed=True, robots_known=True)['indexation_observed'])
        snap = extract(doc(extra='<meta name="robots" content="noindex">'), HOME, status=200)
        self.assertEqual(classify(snap, googlebot_allowed=True, robots_known=True)['state'], 'noindex')

    def test_canonical_and_soft404_main_excludes_footer(self):
        snap = extract(doc('/other'), HOME, status=200)
        self.assertEqual(classify(snap, googlebot_allowed=True, robots_known=True)['state'], 'canonicalized')
        html = '<body><main><h1>Página no encontrada</h1></main><footer>Lots of navigation</footer></body>'
        content = Content(html).evidence()
        self.assertTrue(content['soft_404_candidate'])
        self.assertEqual(classify(extract(html, HOME, status=200), googlebot_allowed=True, robots_known=True, content=content)['state'], 'insufficient_evidence')

    def test_render_comparison_and_critical_gate(self):
        initial = extract(doc(), HOME, status=200)
        rendered = extract(doc(links='<a href="/late">Late</a>'), HOME, status=200)
        self.assertIn(HOME + 'late', layers(initial, rendered)['initial_to_rendered']['links_only_after_js'])
        self.assertFalse(layers(initial, rendered)['googlebot_rendering_tested'])
        r = readiness({'status': 200, 'page_type': 'home', 'content': {'main_text_characters': 100}, 'indexability': {'state': 'noindex'}, 'outgoing_links': [HOME], 'sitemap_checked': True, 'in_sitemap': True}, {'findings': []})
        self.assertEqual(r['approval'], 'blocked'); self.assertIn('indexability', r['critical_blockers'])


class CrawlerV4(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.project = Project(make_project(Path(self.tmp.name), theme=False))
        self.clock = FakeClock()

    def tearDown(self): self.tmp.cleanup()

    def run_crawl(self, pages, **limits):
        pages = {HOME + 'robots.txt': {'status': 200, 'body': 'User-agent: *\nAllow: /'},
                 HOME + 'sitemap.xml': {'status': 404}, **pages}
        self.transport = FixtureTransport(pages)
        return crawl(self.project, limits=Limits(**limits), transport=self.transport, clock=self.clock, sleep=self.clock.sleep)

    def test_bfs_native_pagination_graph_and_broken_links(self):
        result = self.run_crawl({HOME: {'status': 200, 'body': doc(links='<a href="/cat">Cat</a>')},
            HOME + 'cat': {'status': 200, 'body': doc('/cat', '<nav class="pagination"><a href="/cat?page=2">Next</a></nav><a href="/product">P</a>', kind='category')},
            HOME + 'cat?page=2': {'status': 200, 'body': doc('/cat?page=2', '<a href="/old">Old</a>', kind='category')},
            HOME + 'product': {'status': 200, 'body': doc('/product', kind='product')}, HOME + 'old': {'status': 404}})
        self.assertIn(HOME + 'cat?page=2', self.transport.calls)
        self.assertEqual(len(result['graph']['broken_internal_links']), 1)
        node = next(n for n in result['graph']['nodes'] if n['url'] == HOME + 'product')
        self.assertEqual(node['depth_from_home'], 2)
        self.assertFalse(result['remote_mutations'])

    def test_sitemap_index_only_urls_are_candidates_not_orphans(self):
        index = '<sitemapindex><sitemap><loc>' + HOME + 'child.xml</loc></sitemap></sitemapindex>'
        child = '<urlset><url><loc>' + HOME + 'unlinked</loc></url><url><loc>' + HOME + 'unlinked</loc></url></urlset>'
        result = self.run_crawl({HOME: {'status': 200, 'body': doc()}, HOME + 'sitemap.xml': {'status': 200, 'body': index},
            HOME + 'child.xml': {'status': 200, 'body': child}, HOME + 'unlinked': {'status': 200, 'body': doc('/unlinked')}})
        self.assertEqual(result['graph']['sitemap_not_discovered_from_home'], [HOME + 'unlinked'])
        self.assertEqual(result['graph']['confirmed_orphans'], [])
        self.assertEqual(len(result['sitemap_entries']), 2)

    def test_no_links_is_detected_and_private_actions_not_fetched(self):
        result = self.run_crawl({HOME: {'status': 200, 'body': doc(links='<div class="pagination"><a>Más</a></div><a href="/checkout">Checkout</a><a href="/?token=secret">Secret</a><a href="/a?sort=price">Sort</a>')}})
        self.assertNotIn(HOME + 'checkout', self.transport.calls)
        self.assertNotIn('secret', json.dumps(result))
        self.assertEqual(result['urls'][0]['pagination']['state'], 'missing_crawlable_links')

    def test_stop_403_429_global_and_redirect_validation(self):
        for code in [403, 429]:
            self.clock = FakeClock()
            result = self.run_crawl({HOME + 'robots.txt': {'status': code}})
            self.assertEqual(len(self.transport.calls), 1)
            self.assertEqual(result['state'], 'stopped')
        self.clock = FakeClock()
        result = self.run_crawl({HOME: {'status': 302, 'headers': {'location': 'https://other.invalid/'}}})
        self.assertFalse(any('other.invalid' in u for u in self.transport.calls))
        self.assertEqual(result['urls'][0]['indexability']['state'], 'redirected')

    def test_depth_url_cycles_and_request_limits(self):
        result = self.run_crawl({HOME: {'status': 200, 'body': doc(links='<a href="/">Home</a><a href="/a">A</a>')},
            HOME + 'a': {'status': 200, 'body': doc('/a', '<a href="/b">B</a>')}}, max_depth=0)
        self.assertNotIn(HOME + 'a', self.transport.calls)
        self.assertFalse(result['graph']['complete_for_policy'])
        self.clock = FakeClock()
        result = self.run_crawl({HOME: {'status': 200, 'body': doc(links='<a href="/a">A</a>')}}, max_urls=1)
        self.assertEqual(len(result['urls']), 1)
        self.assertEqual(result['state'], 'partial')

    def test_csv_formula_neutralized(self):
        result = self.run_crawl({HOME: {'status': 200, 'body': doc(links='<a href="/a">=1+1</a>')}})
        export(Path(self.tmp.name), result)
        self.assertIn("'=1+1", (Path(self.tmp.name) / 'edges.csv').read_text())
