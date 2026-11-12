from html import escape
"""Casos adicionales offline: no hacen solicitudes a tiendas ni a Google."""
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
from tests.support import make_project
from tests.unit import test_seo_crawler_v4 as fixtures
from ipanema.core import Project, IpanemaError
from ipanema.seo.crawl_policy import Limits, Policy, public_addresses, Fetcher
from ipanema.seo.crawler import crawl
from ipanema.seo.extractor import extract
from ipanema.seo.indexability import classify
from ipanema.seo.robots import Robots, google_directives
HOME = fixtures.HOME

class PatchReview(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.project = Project(make_project(Path(self.tmp.name), theme=False))
        self.clock = fixtures.FakeClock()
    def tearDown(self): self.tmp.cleanup()
    def run_crawl(self, pages=None, robots='User-agent: *\nAllow: /', **limits):
        pages = {HOME+'robots.txt': {'status':200,'body':robots},
                 HOME+'sitemap.xml': {'status':200,'body':'<urlset><url><loc>'+HOME+'</loc></url></urlset>'},
                 HOME:{'status':200,'body':fixtures.doc()}, **(pages or {})}
        self.transport=fixtures.FixtureTransport(pages)
        return crawl(self.project,limits=Limits(**limits),transport=self.transport,clock=self.clock,sleep=self.clock.sleep)
    def state(self, meta='', header=None, name='robots'):
        snap=extract(fixtures.doc(extra=f'<meta name="{name}" content="{escape(meta,quote=True)}">'),HOME,status=200,headers={'x-robots-tag':header or ''})
        return classify(snap,googlebot_allowed=True,robots_known=True)['state']
    def test_O1_preview_none_is_not_noindex(self):
        for value in ('max-image-preview:none','max-image-preview: none','max-image-preview: "none"','max-snippet:-1, max-image-preview:none'):
            with self.subTest(value=value): self.assertEqual(self.state(value),'indexable_candidate')
    def test_O2_robot_product_token_not_substring(self):
        r=Robots();r.parse(['User-agent: bot','Disallow: /','User-agent: *','Allow: /'])
        self.assertTrue(r.can_fetch('Googlebot',HOME))
    def test_O3_late_exclusion_partial(self):
        links='<a href="https://other.invalid/">External</a>'*2001+'<a href="/deep">Deep</a>'
        self.assertEqual(self.run_crawl({HOME:{'status':200,'body':fixtures.doc(links=links)}},max_depth=0)['state'],'partial')
    def test_O4_unchecked_sitemap_partial(self):
        xml='<urlset><url><loc>'+HOME+'unlinked</loc></url></urlset>'
        self.assertEqual(self.run_crawl({HOME+'sitemap.xml':{'status':200,'body':xml}},max_urls=1)['state'],'partial')
    def test_O5_editorial_action_word_allowed(self):
        self.assertEqual(Policy(HOME).check('/blog/posts/como-comprar-x'),HOME+'blog/posts/como-comprar-x')
    def test_meta_and_specific_agents(self):
        for name,value,expected in [('robots','none','noindex'),('robots','NOINDEX, INDEX','noindex'),('googlebot','none','noindex'),('otherbot','noindex','indexable_candidate'),('robots','nofollow','indexable_candidate')]:
            with self.subTest(name=name,value=value): self.assertEqual(self.state(value,name=name),expected)
    def test_headers_multiple_and_scope(self):
        for header,expected in [(['otherbot: noindex','index'],'indexable_candidate'),(['otherbot: noindex','noindex'],'noindex'),('otherbot: none, nofollow, googlebot: index','indexable_candidate'),('googlebot: none, otherbot: index','noindex'),(['googlebot: noindex','index'],'noindex'),('max-image-preview: none, max-snippet: -1','indexable_candidate'),('googlebot: max-image-preview:none, noindex','noindex')]:
            with self.subTest(header=header): self.assertEqual(self.state(header=header),expected)
    def test_header_preview_does_not_mask_meta_noindex(self):
        self.assertEqual(self.state('noindex',header='max-image-preview:none'),'noindex')
    def test_robots_merge_exact_groups_case_and_fallback(self):
        r=Robots();r.parse(['User-agent: GoOgLeBoT','Disallow: /one','User-agent: Googlebot','Disallow: /two','User-agent: *','Disallow: /'])
        for path in ('one','two'): self.assertFalse(r.can_fetch('Googlebot',HOME+path))
        self.assertTrue(r.can_fetch('Googlebot',HOME+'other'))
        self.assertFalse(r.can_fetch('IAIpanemaAudit/4.0',HOME))
    def test_audit_agent_separate_from_google(self):
        r=Robots();r.parse(['User-agent: audit','Disallow: /','User-agent: IAIpanemaAudit','Disallow: /private','User-agent: Googlebot','Disallow: /google','User-agent: *','Allow: /'])
        self.assertTrue(r.can_fetch('IAIpanemaAudit/4.0',HOME+'google'))
        self.assertFalse(r.can_fetch('IAIpanemaAudit/4.0',HOME+'private'))
        self.assertFalse(r.can_fetch('Googlebot',HOME+'google'))
    def test_wildcard_anchor_percent_reserved_and_case(self):
        r=Robots();r.parse(['User-agent: *','Disallow: /private/*$','Allow: /private/public$','Disallow: /caf%C3%A9$','Disallow: /%61bc$','Disallow: /a%2Fb$'])
        for path in ('private/x','caf%C3%A9','café','abc','a%2Fb'): self.assertFalse(r.can_fetch('Googlebot',HOME+path))
        for path in ('private/public','Private/x','abc/more','a/b'): self.assertTrue(r.can_fetch('Googlebot',HOME+path))
    def test_actions_private_multiencoded_and_ambiguous(self):
        p=Policy(HOME)
        for path in ('/comprar/','/COMPRAR','/cart/add','/cart/update','/carrito','/checkout','/add-to-cart','/add_to_cart','/add.to.cart','/agregar.al.carrito','/%2561ccount','/%252563omprar','/%2e%2e/checkout','/%2fcheckout','/%5ccheckout','/checkout?token=private'):
            with self.subTest(path=path),self.assertRaises((ValueError,UnicodeError)):p.check(path)
    def test_public_unicode_and_legitimate_pagination(self):
        p=Policy(HOME)
        for path in ('/blog/posts/compra-segura','/compradores','/productos/café','/cat?page=2','/cat?page_part=cursor123'):
            with self.subTest(path=path): self.assertTrue(p.check(path).startswith(HOME))
    def test_domain_schemes_and_actions_in_query(self):
        p=Policy(HOME)
        for path in ('http://example.invalid/','https://other.invalid/','https://example.invalid.evil/','https://example.invalid:444/','https://user:pass@example.invalid/','//other.invalid/','/?add_to_cart=1','/?sort=price','/?page=2&page=3','/?page=0'):
            with self.subTest(path=path),self.assertRaises(ValueError):p.check(path)
    def test_all_sitemap_urls_verified_when_complete(self):
        xml='<urlset>'+''.join('<url><loc>'+HOME+u+'</loc></url>' for u in ('','a','b'))+'</urlset>'
        r=self.run_crawl({HOME+'sitemap.xml':{'status':200,'body':xml},HOME+'a':{'status':200,'body':fixtures.doc('/a')},HOME+'b':{'status':404}})
        self.assertEqual(r['state'],'complete_for_policy')
        self.assertTrue(all(n.get('status') is not None for n in r['urls']))
    def test_blocked_required_sitemap_is_partial(self):
        xml='<urlset><url><loc>'+HOME+'a</loc></url></urlset>'
        r=self.run_crawl({HOME+'sitemap.xml':{'status':200,'body':xml}},robots='User-agent: *\nDisallow: /a')
        self.assertEqual(r['state'],'partial');self.assertNotIn(HOME+'a',self.transport.calls)
    def test_sitemap_redirect_cycle_not_complete(self):
        r=self.run_crawl({HOME+'sitemap.xml':{'status':302,'headers':{'location':'/child.xml'}},HOME+'child.xml':{'status':301,'headers':{'location':'/sitemap.xml'}}})
        self.assertNotEqual(r['state'],'complete_for_policy')
    def test_sitemap_redirect_limit_not_complete(self):
        r=self.run_crawl({HOME+'sitemap.xml':{'status':302,'headers':{'location':'/child.xml'}}},max_redirects=0)
        self.assertNotEqual(r['state'],'complete_for_policy')
    def test_required_redirect_not_fetched_partial(self):
        r=self.run_crawl({HOME:{'status':302,'headers':{'location':'/target'}}},max_urls=1)
        self.assertNotEqual(r['state'],'complete_for_policy');self.assertNotIn(HOME+'target',self.transport.calls)
    def test_disconnected_sitemap_outgoing_required_unchecked(self):
        xml='<urlset><url><loc>'+HOME+'a</loc></url></urlset>'
        r=self.run_crawl({HOME+'sitemap.xml':{'status':200,'body':xml},HOME+'a':{'status':200,'body':fixtures.doc('/a','<a href="/b">B</a>')}})
        # A known permitted internal target without HTTP evidence must not support completeness.
        self.assertNotEqual(r['state'],'complete_for_policy')
    def test_sitemap_child_budget_and_malformed_partial(self):
        xml='<sitemapindex><sitemap><loc>'+HOME+'child.xml</loc></sitemap></sitemapindex>'
        for pages,limits in [({HOME+'sitemap.xml':{'status':200,'body':xml}},{'max_sitemaps':1}),({HOME+'sitemap.xml':{'status':200,'body':'<urlset><url/></urlset>'}},{}),({HOME+'sitemap.xml':{'status':500}}, {})]:
            with self.subTest(pages=pages):self.assertNotEqual(self.run_crawl(pages,**limits)['state'],'complete_for_policy')
    def test_403_429_stop_from_sitemap_no_home(self):
        for code in (403,429):
            with self.subTest(code=code):
                self.clock=fixtures.FakeClock();r=self.run_crawl({HOME+'sitemap.xml':{'status':code}})
                self.assertEqual(r['state'],'stopped');self.assertNotIn(HOME,self.transport.calls)
    def test_redirect_to_private_external_never_requested(self):
        for target in ('/checkout','/%2561ccount','https://other.invalid/'):
            with self.subTest(target=target):
                self.clock=fixtures.FakeClock();self.run_crawl({HOME:{'status':302,'headers':{'location':target}}})
                self.assertEqual(len(self.transport.calls),3)
    def test_robots_unreachable_and_challenge_no_crawl(self):
        for row in ({'status':500},{'status':200,'body':'<title>CAPTCHA</title>'}):
            with self.subTest(row=row):
                self.clock=fixtures.FakeClock();r=self.run_crawl({HOME+'robots.txt':row})
                self.assertNotIn(HOME,self.transport.calls);self.assertNotEqual(r['state'],'complete_for_policy')
    def test_public_dns_rejects_mapped_private(self):
        for address in ('127.0.0.1','::1','::ffff:127.0.0.1','169.254.169.254'):
            with patch('socket.getaddrinfo',return_value=[(2,1,6,'',(address,443))]),self.assertRaises(ValueError):public_addresses('example.invalid')
    def test_dns_transition_prefix_private_not_accepted(self):
        # No NAT64 network is contacted. Test only resolver output policy.
        for address in ('64:ff9b::7f00:1','64:ff9b::a00:1'):
            with patch('socket.getaddrinfo',return_value=[(10,1,6,'',(address,443))]),self.assertRaises(ValueError):public_addresses('example.invalid')
    def test_commercial_suffix_and_matrix_routes_excluded(self):
        for path in ('/cart.json','/checkout;step=1','/cart%3Bfoo/add','/comprar.json'):
            with self.subTest(path=path),self.assertRaises(ValueError):Policy(HOME).check(path)
    def test_deadline_rechecked_after_scheduler_delay(self):
        clock=fixtures.FakeClock();calls=[]
        def delayed_sleep(seconds): clock.value += seconds+2
        f=Fetcher(Policy(HOME,Limits(max_seconds=1)),transport=lambda *a,**k: calls.append(a) or {'status':200},clock=clock,sleep=delayed_sleep)
        with self.assertRaises(ValueError):f.get(HOME)
        self.assertEqual(calls,[])
    def test_missing_redirect_location_not_complete(self):
        r=self.run_crawl({HOME:{'status':302,'headers':{}}})
        self.assertNotEqual(r['state'],'complete_for_policy')
    def test_action_prefix_suffix_regression(self):
        for path in ('/add-to-cart-123','/add_to_cart123','/comprar-ahora','/%2561dd-to-cart-123','/comprar123','/ADD.TO.CART123'):
            with self.subTest(path=path),self.assertRaises(ValueError):Policy(HOME).check(path)
        self.assertEqual(Policy(HOME).check('/blog/posts/como-comprar-x'),HOME+'blog/posts/como-comprar-x')
    def test_private_prefix_delimiters_and_action_compact(self):
        for path in ('/checkout-step','/cart,1','/checkout123','/addtocart','/%2563art,1'):
            with self.subTest(path=path),self.assertRaises(ValueError):Policy(HOME).check(path)
        self.assertEqual(Policy(HOME).check('/cartografia'),HOME+'cartografia')
    def test_missing_location_is_explicit_error(self):
        for url in (HOME,HOME+'sitemap.xml',HOME+'robots.txt'):
            with self.subTest(url=url):
                self.clock=fixtures.FakeClock();r=self.run_crawl({url:{'status':302,'headers':{}}})
                reasons=[e.get('reason','') for e in r['errors']]+[n.get('error','') for n in r['urls']]
                self.assertTrue(any('Location' in e for e in reasons));self.assertNotEqual(r['state'],'complete_for_policy')
    def test_malformed_sitemap_parser_record_fails_closed(self):
        record={'kind':'urlset','entries':[],'errors':[],'duplicates':[]}
        with patch('ipanema.seo.crawler.parse_sitemap',return_value=record):
            r=self.run_crawl();self.assertEqual(r['state'],'partial')
    def test_invalid_robots_agent_with_version_fails_closed(self):
        r=Robots();r.parse(['User-agent: Googlebot/2.1','Disallow: /x'])
        self.assertTrue(r.errors);self.assertFalse(r.can_fetch('Googlebot',HOME+'x'))
