import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from tests.support import make_project
from tests.unit.test_seo_crawler_v4 import FakeClock, FixtureTransport, doc, HOME
from ipanema.core import Project, IpanemaError
from ipanema.seo.crawler import crawl
from ipanema.seo.crawl_policy import Limits, Fetcher, Policy


class ClosedPilot(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory();self.project = Project(make_project(Path(self.tmp.name),theme=False))
        self.targets = [HOME + 'selected-' + str(i) for i in range(5)]
        self.pages = {HOME+'robots.txt': {'status':200,'body':'User-agent: *\nAllow: /\nSitemap: '+HOME+'sitemap.xml'}}
        self.pages.update({u:{'status':200,'body':doc('/'+u.rsplit('/',1)[1],links='<a href="/extra">extra</a>')} for u in self.targets})

    def tearDown(self):self.tmp.cleanup()

    def run_crawl(self, pages=None, transport=None, **kwargs):
        clock=FakeClock();t=transport or FixtureTransport(pages or self.pages)
        z=crawl(self.project,targets=self.targets,limits=kwargs.pop('limits',Limits(timeout=20)),transport=t,clock=clock,sleep=clock.sleep,**kwargs)
        return z,t,clock

    def test_exact_selection_no_home_sitemap_or_extra(self):
        z,t,_=self.run_crawl();self.assertEqual(t.calls,[HOME+'robots.txt',*self.targets])
        self.assertEqual([n['url'] for n in z['urls']],self.targets)
        self.assertEqual(z['state'],'complete_for_selected_scope');self.assertFalse(z['graph']['complete_for_policy'])
        self.assertFalse(z['whole_site_complete'])

    def test_caps_and_rate_shared_with_robots(self):
        z,t,clock=self.run_crawl(limits=Limits(max_requests=100,requests_per_second=2,max_seconds=300,timeout=30,max_bytes=5000000))
        caps=z['provenance']['limits'];self.assertEqual(caps['max_requests'],12);self.assertEqual(caps['max_redirects'],3)
        self.assertEqual(caps['requests_per_second'],.5);self.assertEqual(caps['max_seconds'],120);self.assertEqual(caps['timeout'],20)
        self.assertEqual(caps['max_bytes'],2000000);self.assertEqual(clock.value,10)

    def test_robots_slower_rate(self):
        pages=copy.deepcopy(self.pages);pages[HOME+'robots.txt']['body']='User-agent: *\nCrawl-delay: 3'
        _,_,clock=self.run_crawl(pages);self.assertEqual(clock.value,15)

    def test_invalid_targets_rejected_before_any_request(self):
        for bad in (self.targets[:4],self.targets[:4]+[self.targets[0]],self.targets[:4]+[HOME+'checkout/'],self.targets[:4]+['https://other.invalid/a']):
            t=FixtureTransport(self.pages)
            with self.subTest(targets=bad),self.assertRaises((IpanemaError,ValueError)):
                crawl(self.project,targets=bad,transport=t)
            self.assertEqual(t.calls,[])

    def test_403_and_429_abort_globally(self):
        for status in (403,429):
            pages=copy.deepcopy(self.pages);pages[self.targets[0]]={'status':status}
            z,t,_=self.run_crawl(pages);self.assertEqual(t.calls,[HOME+'robots.txt',self.targets[0]])
            self.assertEqual(z['provenance']['stop_reason'],'http_'+str(status))

    def test_unknown_robots_aborts(self):
        pages=copy.deepcopy(self.pages);pages[HOME+'robots.txt']={'status':500}
        z,t,_=self.run_crawl(pages);self.assertEqual(t.calls,[HOME+'robots.txt']);self.assertEqual(z['provenance']['stop_reason'],'robots_unknown')

    def test_absent_robots_404_410_native_semantics(self):
        for status in (404,410):
            pages=copy.deepcopy(self.pages);pages[HOME+'robots.txt']={'status':status}
            z,t,_=self.run_crawl(pages);self.assertEqual(len(t.calls),6);self.assertTrue(z['robots']['known'])

    def test_robots_block_no_document_get(self):
        pages=copy.deepcopy(self.pages);pages[HOME+'robots.txt']['body']='User-agent: *\nDisallow: /'
        z,t,_=self.run_crawl(pages);self.assertEqual(t.calls,[HOME+'robots.txt']);self.assertEqual(z['state'],'stopped')

    def test_generic_transport_safety_failures_abort_remaining(self):
        for reason in ('TLS','private IP','DNS','timeout','gzip incomplete','encoding rejected'):
            class F(FixtureTransport):
                def __call__(inner,url,**kw):
                    if url==self.targets[0]:inner.calls.append(url);raise IpanemaError(reason)
                    return super().__call__(url,**kw)
            z,t,_=self.run_crawl(transport=F(self.pages));self.assertEqual(t.calls,[HOME+'robots.txt',self.targets[0]])
            self.assertEqual(z['provenance']['stop_reason'],'closed_scope_error')

    def test_redirect_external_private_missing_and_cycle_stop(self):
        for location in ('https://other.invalid/a',HOME+'checkout/',None,self.targets[0]):
            pages=copy.deepcopy(self.pages);pages[self.targets[0]]={'status':302,'headers':{'location':location} if location else {}}
            z,t,_=self.run_crawl(pages);self.assertEqual(t.calls,[HOME+'robots.txt',self.targets[0]]);self.assertEqual(z['state'],'stopped')

    def test_robots_and_documents_share_three_hops(self):
        pages=copy.deepcopy(self.pages);pages[HOME+'robots.txt']={'status':302,'headers':{'location':HOME+'robots-real.txt'}}
        pages[HOME+'robots-real.txt']={'status':200,'body':'User-agent: *\nAllow: /'}
        pages[self.targets[0]]={'status':302,'headers':{'location':HOME+'hop-1'}}
        pages[HOME+'hop-1']={'status':302,'headers':{'location':HOME+'hop-2'}}
        pages[HOME+'hop-2']={'status':302,'headers':{'location':HOME+'hop-3'}}
        z,t,_=self.run_crawl(pages);self.assertNotIn(HOME+'hop-3',t.calls);self.assertEqual(z['redirect_hops_used'],3)
        self.assertEqual(z['state'],'stopped')

    def test_redirect_blocked_by_robots_not_fetched(self):
        pages=copy.deepcopy(self.pages);pages[HOME+'robots.txt']['body']='User-agent: *\nDisallow: /blocked'
        pages[self.targets[0]]={'status':302,'headers':{'location':HOME+'blocked'}}
        z,t,_=self.run_crawl(pages);self.assertNotIn(HOME+'blocked',t.calls);self.assertEqual(z['state'],'stopped')

    def test_convergent_redirect_is_not_cycle_or_duplicate_get(self):
        pages=copy.deepcopy(self.pages);pages[self.targets[1]]={'status':302,'headers':{'location':self.targets[0]}}
        z,t,_=self.run_crawl(pages);self.assertEqual(z['state'],'complete_for_selected_scope')
        self.assertEqual(t.calls.count(self.targets[0]),1);self.assertEqual(len(t.calls),6)

    def test_two_selected_urls_redirect_cycle_is_terminal(self):
        pages=copy.deepcopy(self.pages);pages[self.targets[0]]={'status':302,'headers':{'location':self.targets[1]}}
        pages[self.targets[1]]={'status':302,'headers':{'location':self.targets[0]}}
        z,t,_=self.run_crawl(pages);self.assertEqual(z['state'],'stopped')
        self.assertEqual(t.calls,[HOME+'robots.txt',self.targets[0],self.targets[1]])

    def test_request_budget_and_time_budget_stop(self):
        z,t,_=self.run_crawl(limits=Limits(max_requests=2));self.assertEqual(len(t.calls),2);self.assertEqual(z['state'],'stopped')
        z,t,_=self.run_crawl(limits=Limits(max_seconds=1));self.assertEqual(len(t.calls),1);self.assertEqual(z['state'],'stopped')

    def test_checkpoint_failure_prevents_transport(self):
        t=FixtureTransport(self.pages)
        def failure(row):raise OSError('checkpoint fixture failure')
        with self.assertRaises(OSError):self.run_crawl(transport=t,on_event=failure)
        self.assertEqual(t.calls,[])

    def test_request_events_preserve_unconfirmed_arrival(self):
        events=[]
        class F(FixtureTransport):
            def __call__(inner,url,**kw):
                if url==self.targets[0]:inner.calls.append(url);raise IpanemaError('fixture')
                return super().__call__(url,**kw)
        z,t,_=self.run_crawl(transport=F(self.pages),on_event=events.append)
        self.assertEqual([x['event'] for x in events],['started','completed','started','unconfirmed'])

    def test_general_mode_unchanged_home_seed(self):
        t=FixtureTransport({HOME+'robots.txt':{'status':200,'body':'User-agent: *'},HOME:{'status':200,'body':doc()}});clock=FakeClock()
        z=crawl(self.project,transport=t,limits=Limits(max_urls=1,max_sitemaps=0),clock=clock,sleep=clock.sleep)
        self.assertEqual(t.calls,[HOME+'robots.txt',HOME]);self.assertNotIn('selected_scope',z)
