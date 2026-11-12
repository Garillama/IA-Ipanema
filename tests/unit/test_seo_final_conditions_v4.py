import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from tests.support import make_project
from ipanema.core import Project
from ipanema.seo import robots
from ipanema.seo.regression import compare, _nodes
from ipanema.seo.indexability import classify
from ipanema.seo.page_audit import audit_snapshot


class FinalGate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.project = Project(make_project(Path(self.tmp.name), theme=False))
        self.url = 'https://example.invalid/'

    def tearDown(self):
        self.tmp.cleanup()

    def report(self, evidence):
        return {'kind': 'seo-page-audit', 'project': self.project.id, 'url': self.url,
                'http_status': 200, 'canonical': [self.url], 'robots_evidence': evidence}

    def check(self, before, after):
        gate = compare(self.project, self.report(before), self.report(after))
        return next(c for c in gate['checks'] if c['name'].endswith(':noindex'))

    def test_clean_directives_pass_only_scoped_check(self):
        e = robots.google_directive_evidence({}, '')
        self.assertEqual(self.check(e, e)['status'], 'passed')
        n = _nodes(self.report(e))[self.url]
        self.assertFalse(n['indexability']['indexation_observed'])
        self.assertEqual(n['indexability']['state'], 'insufficient_evidence')

    def test_legacy_and_absent_remain_unknown(self):
        for e in (None, {}, {'noindex': False}, 'index,follow'):
            with self.subTest(e=e): self.assertEqual(self.check(e, e)['status'], 'unknown')

    def test_malformed_remains_unknown(self):
        e = robots.google_directive_evidence({'robots': ['foo="open']}, '')
        self.assertEqual(self.check(e, e)['status'], 'unknown')

    def test_invalid_structure_never_passes(self):
        e = robots.google_directive_evidence({}, '')
        for k, v in [('noindex', 'false'), ('flags', 'index'), ('sources', None), ('relevant_errors', 'none'), ('processing_complete', 1)]:
            bad = copy.deepcopy(e);bad[k] = v
            with self.subTest(k=k): self.assertEqual(self.check(bad, bad)['status'], 'unknown')

    def test_new_noindex_fails_from_unknown(self):
        e = robots.google_directive_evidence({'robots': ['noindex']}, '')
        self.assertEqual(self.check(None, e)['status'], 'failed')

    def test_noindex_survives_incomplete_other_source(self):
        e = robots.google_directive_evidence({'robots': ['noindex', 'x' * (robots.MAX_SOURCE_BYTES + 1)]}, '')
        self.assertFalse(e['processing_complete']);self.assertTrue(e['noindex'])
        self.assertEqual(self.check(None, e)['status'], 'failed')

    def test_existing_noindex_both_sides_not_new_regression(self):
        e = robots.google_directive_evidence({'robots': ['noindex']}, '')
        self.assertEqual(self.check(e, e)['status'], 'passed')

    def test_clean_does_not_override_content_uncertainty(self):
        e = robots.google_directive_evidence({}, '')
        n = {'url': self.url, 'status': 200, 'canonical': [self.url],
             'indexability': {'state': 'insufficient_evidence', 'robots_evidence': e}}
        crawl = {'kind': 'seo-crawl-v4', 'project': self.project.id, 'urls': [n]}
        gate = compare(self.project, crawl, copy.deepcopy(crawl))
        self.assertEqual(next(c for c in gate['checks'] if c['name'].endswith(':noindex'))['status'], 'passed')
        self.assertEqual(n['indexability']['state'], 'insufficient_evidence')


class EvidenceBudgets(unittest.TestCase):
    def test_tail_restriction_after_two_hundred_thousand_parameters(self):
        e = robots.google_directive_evidence({'robots': ['foo:bar,' * 200000 + 'noindex']}, '')
        self.assertTrue(e['noindex']);self.assertTrue(e['processing_complete'])
        self.assertEqual(e['counts']['parameters'], 200000)
        self.assertLessEqual(len(e['sources'][0]['parameters']), robots.MAX_SAMPLES)
        self.assertTrue(e['truncated'])
        self.assertLessEqual(len(json.dumps(e, ensure_ascii=False).encode()), robots.MAX_EVIDENCE_BYTES)

    def test_error_after_sample_cap_cannot_be_lost(self):
        e = robots.google_directive_evidence({'robots': ['foo:bar,' * 100 + 'noindex=bad']}, '')
        self.assertEqual(e['state'], 'insufficient_evidence')
        self.assertGreater(e['counts']['errors'], 0)

    def test_unknown_quoted_parameter_after_cap_stays_uncertain(self):
        e = robots.google_directive_evidence({'robots': ['foo:bar,' * 100 + 'foo="x; noindex"']}, '')
        self.assertFalse(e['noindex']);self.assertEqual(e['state'], 'insufficient_evidence')

    def test_late_raw_header_quote_error_survives_sample_cap(self):
        value = 'otherbot: ' + 'bad/,' * 20 + 'foo="open'
        e = robots.google_directive_evidence({}, value)
        self.assertFalse(e['noindex'])
        self.assertEqual(e['state'], 'insufficient_evidence')
        self.assertTrue(e['relevant_errors'])

    def test_source_oversize_explicit_incomplete(self):
        with patch.object(robots, 'MAX_SOURCE_BYTES', 64):
            e = robots.google_directive_evidence({'robots': ['x' * 65 + ',noindex']}, '')
        self.assertFalse(e['processing_complete'])
        self.assertEqual(e['state'], 'insufficient_evidence')

    def test_source_budget_exact_boundary(self):
        with patch.object(robots, 'MAX_SOURCE_BYTES', 5):
            e = robots.google_directive_evidence({'robots': ['index']}, '')
            self.assertTrue(e['processing_complete'])
            e = robots.google_directive_evidence({'robots': ['index ']}, '')
            self.assertFalse(e['processing_complete'])

    def test_utf8_bytes_not_characters(self):
        with patch.object(robots, 'MAX_SOURCE_BYTES', 5):
            e = robots.google_directive_evidence({'robots': ['ééé']}, '')
        self.assertFalse(e['processing_complete'])

    def test_total_budget_preserves_prior_noindex(self):
        with patch.object(robots, 'MAX_TOTAL_BYTES', 12):
            e = robots.google_directive_evidence({'robots': ['noindex', 'index,index']}, '')
        self.assertTrue(e['noindex']);self.assertFalse(e['processing_complete'])

    def test_source_limit_does_not_claim_complete_counts(self):
        with patch.object(robots, 'MAX_PROCESS_SOURCES', 2):
            e = robots.google_directive_evidence({'robots': ['index'] * 3}, '')
        self.assertFalse(e['processing_complete']);self.assertIsNone(e['unvisited_sources_count'])
        self.assertEqual(e['counts']['sources_seen'], 2)

    def test_omitted_source_restriction_and_errors_still_aggregate(self):
        e = robots.google_directive_evidence({'robots': ['index'] * 20 + ['noindex', 'foo="open']}, '')
        self.assertTrue(e['noindex']);self.assertTrue(e['relevant_errors'])
        self.assertEqual(e['counts']['sources_processed'], 22)
        self.assertLessEqual(len(e['sources']), robots.MAX_RETAINED_SOURCES)

    def test_whole_result_cap_with_long_names(self):
        value = ','.join(('f' + 'x' * 500 + str(i) + ':bar') for i in range(20))
        e = robots.google_directive_evidence({'robots': [value] * 30}, '')
        self.assertTrue(e['processing_complete']);self.assertTrue(e['truncated'])
        self.assertLessEqual(len(json.dumps(e, ensure_ascii=False).encode()), robots.MAX_EVIDENCE_BYTES)

    def test_source_hash_stable_across_retention(self):
        e = robots.google_directive_evidence({'robots': ['index'] * 20}, '')
        with patch.object(robots, 'MAX_RETAINED_SOURCES', 1):
            f = robots.google_directive_evidence({'robots': ['index'] * 20}, '')
        self.assertEqual(e['processed_collection_sha256'], f['processed_collection_sha256'])


class LegacyDisplay(unittest.TestCase):
    def test_exact_historical_fixtures(self):
        cases = [({'robots': ['max-snippet:50'], 'googlebot': ['index']}, '', 'max-snippet:50,index,'),
                 ({}, 'otherbot: noindex, nofollow, googlebot: index', 'index'),
                 ({}, 'googlebot: max-snippet:50, nofollow', 'max-snippet:50, nofollow'),
                 ({}, '*: noindex', '*: noindex'),
                 ({'robots': ['index']}, ['otherbot: noindex', 'max-snippet:50'], 'index,,,max-snippet:50')]
        for meta, header, expected in cases:
            with self.subTest(header=header):self.assertEqual(robots.google_directives(meta, header), expected)

    def test_decision_consumers_do_not_call_display(self):
        snap = {'url': 'https://example.invalid/', 'status': 200, 'canonical': [],
                'meta': {'robots': ['noindex']}, 'headers': {}, 'headings': [], 'images': [],
                'links': [], 'jsonld': [], 'html': '<html><main>Example content</main></html>'}
        with patch.object(robots, 'google_directives', side_effect=AssertionError('display called')):
            self.assertEqual(classify(snap, googlebot_allowed=True, robots_known=True)['state'], 'noindex')
            from ipanema.seo.regression import _robots_state
            self.assertEqual(_robots_state({'indexability': {'robots_evidence': robots.google_directive_evidence({'robots': ['noindex']}, '')}}), 'noindex')


if __name__ == '__main__': unittest.main()
