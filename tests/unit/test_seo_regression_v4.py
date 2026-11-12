import copy
from pathlib import Path
import tempfile
import unittest

from tests.support import make_project
from ipanema.core import Project, IpanemaError
from ipanema.seo.regression import compare


class RegressionV4(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.project = Project(make_project(Path(self.tmp.name), theme=False))
        self.url = 'https://example.invalid/'
        node = {'url': self.url, 'status': 200, 'canonical': [self.url], 'indexability': {'state': 'indexable_candidate'},
                'outgoing_links': [self.url + 'product'], 'pagination': {'active_controls_without_href': 0},
                'template_audit': {'content': {'headings': [{'level': 1, 'text': 'Home'}]}, 'findings': [],
                                   'structured_data': {'states': {'syntax_valid': True}}},
                'layers': {'initial_to_no_js': {'links_removed_after_js': []},
                           'main_content': {'no_js': {'main_text_characters': 100}}}}
        self.before = {'kind': 'seo-crawl-v4', 'project': 'sample', 'urls': [node]}

    def tearDown(self): self.tmp.cleanup()

    def test_identical_complete_evidence_passes(self):
        self.assertEqual(compare(self.project, self.before, copy.deepcopy(self.before))['outcome'], 'passed_scoped_checks')

    def test_missing_after_partial_never_passes(self):
        after = copy.deepcopy(self.before); after['urls'] = []
        self.assertEqual(compare(self.project, self.before, after)['outcome'], 'insufficient_evidence')

    def test_main_disappears_without_javascript(self):
        after = copy.deepcopy(self.before)
        after['urls'][0]['layers']['main_content']['no_js']['main_text_characters'] = 0
        result = compare(self.project, self.before, after)
        self.assertEqual(result['outcome'], 'blocked')
        self.assertTrue(any(c['name'].endswith(':no_js_main_content') and c['status'] == 'failed' for c in result['checks']))

    def test_independent_critical_changes_block(self):
        for key, value in [('canonical', ['https://example.invalid/other']), ('status', 500), ('outgoing_links', []),
                           ('indexability', {'state': 'noindex'}), ('pagination', {'active_controls_without_href': 1})]:
            with self.subTest(key=key):
                after = copy.deepcopy(self.before); after['urls'][0][key] = value
                self.assertEqual(compare(self.project, self.before, after)['outcome'], 'blocked')

    def test_jsonld_and_commerce_errors_block(self):
        after = copy.deepcopy(self.before)
        after['urls'][0]['template_audit']['structured_data']['states']['syntax_valid'] = False
        after['urls'][0]['template_audit']['findings'] = [{'rule': 'D020', 'severity': 'error', 'message': 'Offer price differs from authorized facts'}]
        self.assertEqual(compare(self.project, self.before, after)['outcome'], 'blocked')

    def test_scope_and_approved_removed_link(self):
        after = copy.deepcopy(self.before); after['urls'][0]['outgoing_links'] = []
        self.assertEqual(compare(self.project, self.before, after, allow_removed=[self.url + 'product'])['outcome'], 'passed_scoped_checks')
        after['project'] = 'other'
        with self.assertRaises(IpanemaError): compare(self.project, self.before, after)
