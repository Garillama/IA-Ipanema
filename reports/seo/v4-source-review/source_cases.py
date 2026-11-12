"""Source-boundary regressions: purely local, no storefront or Google requests."""
from html import escape
import hashlib
from pathlib import Path
import tempfile
import unittest
from tests.support import make_project
from tests.unit import test_seo_crawler_v4 as fixtures
from ipanema.core import Project
from ipanema.seo import robots
from ipanema.seo.extractor import extract
from ipanema.seo.indexability import classify
from ipanema.seo.page_audit import audit_snapshot
from ipanema.seo.regression import compare
HOME=fixtures.HOME

class SourceBoundaries(unittest.TestCase):
    def snapshot(self, meta=None, headers=''):
        tags=''.join(f'<meta name="{name}" content="{escape(value,quote=True)}">' for name,values in (meta or {}).items() for value in values)
        html=fixtures.doc(extra=tags)
        return extract(html,HOME,status=200,headers={'x-robots-tag':headers})
    def state(self,meta=None,headers=''):
        return classify(self.snapshot(meta,headers),googlebot_allowed=True,robots_known=True)['state']
    def test_original_meta_quote_cannot_mask_header_noindex(self):
        self.assertEqual(self.state({'robots':['foo="x']},'noindex'),'noindex')
    def test_original_repeated_header_quote_cannot_mask_next(self):
        self.assertEqual(self.state(headers=['foo="x','noindex']),'noindex')
    def test_01_valid_meta_robots(self):
        self.assertEqual(self.state({'robots':['noindex']}),'noindex')
    def test_02_valid_header(self):
        self.assertEqual(self.state(headers='none'),'noindex')
    def test_03_independent_meta_sources(self):
        for meta in ({'robots':['foo="x','noindex']},{'robots':['foo="x'],'googlebot':['noindex']},{'robots':['noindex'],'googlebot':['foo="x']}):
            with self.subTest(meta=meta):self.assertEqual(self.state(meta),'noindex')
    def test_04_open_meta_without_valid_restriction_unknown(self):
        self.assertEqual(self.state({'robots':['foo="x']}),'insufficient_evidence')
    def test_05_open_header_without_valid_restriction_unknown(self):
        self.assertEqual(self.state(headers='foo="x'),'insufficient_evidence')
    def test_06_valid_restriction_after_malformed_source(self):
        for headers in (['foo="x','none'],['foo="x','index','noindex'],['otherbot: foo="x','noindex']):
            with self.subTest(headers=headers):self.assertEqual(self.state(headers=headers),'noindex')
    def test_07_preview_none_not_restriction(self):
        self.assertEqual(self.state({'robots':['max-image-preview:none']}),'indexable_candidate')
    def test_08_quoted_values_not_flags(self):
        for value in ('foo="noindex"','foo="none"','foo=noindex','foo: noindex','foo="googlebot: noindex"'):
            with self.subTest(value=value):self.assertEqual(self.state({'robots':[value]}),'indexable_candidate')
    def test_09_header_scope_resets_for_each_field(self):
        self.assertEqual(self.state(headers=['otherbot: noindex','index']),'indexable_candidate')
        self.assertEqual(self.state(headers=['otherbot: index','noindex']),'noindex')
    def test_10_agents_and_quoted_agent_names(self):
        self.assertEqual(self.state(headers='otherbot: noindex'),'indexable_candidate')
        self.assertEqual(self.state(headers='GoogleBot: none'),'noindex')
        self.assertEqual(self.state(headers='otherbot: foo="googlebot: noindex"'),'indexable_candidate')
        self.assertEqual(self.state(headers='foo="otherbot: none", noindex'),'noindex')
    def test_11_index_never_neutralizes_noindex(self):
        for meta,headers in [({'robots':['noindex']},'index'),({'robots':['index']},'noindex'),({'googlebot':['index'],'robots':['none']},'index')]:
            with self.subTest(meta=meta,headers=headers):self.assertEqual(self.state(meta,headers),'noindex')
    def test_12_unknown_complete_and_incomplete(self):
        self.assertEqual(self.state({'robots':['unknownrule, foo="noindex"']}),'indexable_candidate')
        for value in ('foo=','max-image-preview:','noindex=foo','googlebot:'):
            with self.subTest(value=value):
                if value=='googlebot:':self.assertEqual(self.state(headers=value),'insufficient_evidence')
                else:self.assertEqual(self.state({'robots':[value]}),'insufficient_evidence')
    def test_unrelated_agent_malformed_field_not_relevant(self):
        self.assertEqual(self.state(headers='otherbot: foo="x'),'indexable_candidate')
    def test_malformed_robots_and_unrelated_noindex_is_unknown(self):
        self.assertEqual(self.state({'robots':['foo="x']},'otherbot: noindex'),'insufficient_evidence')
    def test_googlebot_news_not_text_googlebot(self):
        self.assertEqual(self.state({'googlebot-news':['noindex']}),'indexable_candidate')
        self.assertEqual(self.state(headers='googlebot-news: noindex'),'indexable_candidate')
    def test_independent_errors_and_provenance_retained(self):
        e=robots.google_directive_evidence({'robots':['foo="x'],'googlebot':['index']},['noindex','otherbot: noindex'])
        self.assertEqual(len(e['sources']),4);self.assertTrue(e['noindex']);self.assertTrue(e['relevant_errors'])
        self.assertEqual(e['sources'][0]['input_sha256'],hashlib.sha256(b'foo="x').hexdigest())
        self.assertEqual(e['sources'][2]['index'],0);self.assertEqual(e['sources'][3]['index'],1)
        self.assertEqual(e['sources'][3]['flags'],[])
    def test_never_uses_legacy_joined_string_for_decision(self):
        from unittest.mock import patch
        with patch.object(robots,'google_directives',side_effect=AssertionError('legacy display must not decide')):
            self.assertEqual(self.state({'robots':['foo="x']},'noindex'),'noindex')
    def test_evidence_stays_on_classification(self):
        e=classify(self.snapshot({'robots':['foo="x']},'index'),googlebot_allowed=True,robots_known=True)
        self.assertEqual(e['state'],'insufficient_evidence');self.assertIn('malformed_robots_directives',e['reasons'])
        self.assertTrue(e['robots_evidence']['relevant_errors'])
    def test_noindex_before_malformed_tail_stays_restrictive(self):
        self.assertEqual(self.state({'robots':['noindex, foo="x']}),'noindex')
    def test_malformed_does_not_get_approved_by_nonself_canonical(self):
        snap=self.snapshot({'robots':['foo="x']});snap['canonical']=[HOME+'other']
        self.assertEqual(classify(snap,googlebot_allowed=True,robots_known=True)['state'],'insufficient_evidence')
    def test_audit_consumer_marks_unknown_and_keeps_sources(self):
        with tempfile.TemporaryDirectory() as folder:
            project=Project(make_project(Path(folder),theme=False))
            report=audit_snapshot(project,self.snapshot({'robots':['foo="x']},'index'),'home')
            self.assertEqual(report['indexability_observable'],'insufficient_evidence')
            self.assertTrue(report['robots_evidence']['relevant_errors'])
    def test_legacy_page_audit_gate_does_not_parse_display_substring(self):
        with tempfile.TemporaryDirectory() as folder:
            project=Project(make_project(Path(folder),theme=False))
            report=audit_snapshot(project,self.snapshot({'robots':['foo="noindex"']}),'home')
            report['robots_directives']='foo="noindex"'
            gate=compare(project,report,report)
            checks=[c for c in gate['checks'] if c['name'].endswith(':noindex')]
            self.assertNotEqual(checks[0]['details'],'noindex')

    def test_valid_restriction_is_monotonic_across_sources(self):
        from itertools import permutations
        for fields in permutations(['foo="open','noindex','index']):
            with self.subTest(fields=fields):
                self.assertEqual(self.state(headers=list(fields)),'noindex')
                self.assertEqual(self.state({'robots':list(fields)}),'noindex')
                self.assertEqual(self.state({'googlebot':list(fields)}),'noindex')
