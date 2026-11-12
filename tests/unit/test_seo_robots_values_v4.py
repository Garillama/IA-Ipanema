"""Directivas independientes frente a valores; casos offline de la observación humana."""
from html import escape
import unittest
from tests.unit import test_seo_crawler_v4 as fixtures
from ipanema.seo.robots import has_noindex, google_directives
from ipanema.seo.extractor import extract
from ipanema.seo.indexability import classify

class DirectiveValues(unittest.TestCase):
    def state(self, value='', header='', name='robots'):
        html=fixtures.doc(extra=f'<meta name="{name}" content="{escape(value,quote=True)}">')
        snapshot=extract(html,fixtures.HOME,status=200,headers={'x-robots-tag':header})
        return classify(snapshot,googlebot_allowed=True,robots_known=True)['state']
    def test_assignment_values_are_not_directives(self):
        for value in ('foo="noindex"',"foo='noindex'",'foo=noindex','foo = noindex','foo = "noindex"','foo: noindex','foo: "none"','foo=none','foo="x, noindex"','foo="x; none"'):
            with self.subTest(value=value):self.assertFalse(has_noindex(value))
    def test_standalone_restrictive_flags(self):
        for value in ('noindex','none','NOINDEX','index, noindex','nofollow; none','foo="noindex", noindex','foo=bar noindex','max-image-preview:none, noindex'):
            with self.subTest(value=value):self.assertTrue(has_noindex(value))
    def test_values_with_escaped_quotes(self):
        for value in ('foo="abc\\\" noindex"',"foo='abc\\' none'",'foo="a, otherbot: noindex"'):
            with self.subTest(value=value):self.assertFalse(has_noindex(value))
    def test_quoted_standalone_words_are_not_flags(self):
        for value in ('"noindex"',"'none'",'"x, noindex"','foo/noindex','x-noindex','noindexable'):
            with self.subTest(value=value):self.assertFalse(has_noindex(value))
    def test_colon_preview_and_other_values(self):
        for value in ('max-image-preview:none','max-image-preview: none','max-image-preview: "none"','unavailable_after: Wed, 25 Jun 2030 15:00:00 GMT','foo="none", max-snippet:-1'):
            with self.subTest(value=value):self.assertFalse(has_noindex(value))
    def test_meta_assignment_and_flag(self):
        self.assertEqual(self.state('foo="noindex"'),'indexable_candidate')
        self.assertEqual(self.state('foo="none", noindex'),'noindex')
        self.assertEqual(self.state('foo="noindex", nofollow'),'indexable_candidate')
    def test_header_assignment_and_flag(self):
        self.assertEqual(self.state(header='foo="noindex"'),'indexable_candidate')
        self.assertEqual(self.state(header='foo="none", noindex'),'noindex')
    def test_header_quoted_agent_name_does_not_change_scope(self):
        self.assertEqual(self.state(header='foo="x, otherbot: none", noindex'),'noindex')
        self.assertEqual(self.state(header='otherbot: foo="x, googlebot: none", noindex'),'insufficient_evidence')
    def test_repeated_headers_keep_agent_scope(self):
        for headers,expected in [(['otherbot: noindex','foo="noindex"'],'indexable_candidate'),(['otherbot: noindex','googlebot: noindex'],'noindex'),(['googlebot: foo="noindex"','index'],'indexable_candidate'),(['otherbot: foo="googlebot: noindex"','none'],'noindex')]:
            with self.subTest(headers=headers):self.assertEqual(self.state(header=headers),expected)
    def test_specific_meta_robots_rules(self):
        self.assertEqual(self.state('foo="noindex"',name='googlebot'),'indexable_candidate')
        self.assertEqual(self.state('foo="noindex", none',name='googlebot'),'noindex')
        self.assertEqual(self.state('noindex',name='otherbot'),'indexable_candidate')
    def test_global_meta_restriction_cannot_be_relaxed_by_header(self):
        self.assertEqual(self.state('noindex',header='foo="noindex", index'),'noindex')
    def test_many_values_and_unclosed_quote_do_not_leak_flags(self):
        self.assertFalse(has_noindex(('foo="noindex, none" '*2000)))
        self.assertFalse(has_noindex('foo="open noindex, none'))
        self.assertTrue(has_noindex('noindex, foo="open none'))
