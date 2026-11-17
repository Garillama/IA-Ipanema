"""Controlled synthetic reviewer records: gate tests, NOT real AI detection.

All native identities/receipts below are deliberately synthetic. No inference,
Context7, browser or client project is accessed by this suite.
"""
import copy
import hashlib
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest

from ipanema.core import IpanemaError
from ipanema.orchestration import code_review
from ipanema.orchestration.council import review_code_candidate


class CrossReview(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.texts = {'existing.py': 'def original(data):\n    return data[::-1]\n',
                      'candidate.py': 'def duplicate(data):\n    return list(reversed(data))\n',
                      'ui.js': "target.addEventListener('click', handler);\ntarget.addEventListener('click', handler);\n"}
        for name, text in self.texts.items():
            (self.root / name).write_text(text)
        self.candidate = {'author': 'codex', 'contributors': ['codex'], 'risk': 'medium', 'objective': 'Review a controlled fixture',
                          'diff_sha256': hashlib.sha256(b'synthetic diff').hexdigest(),
                          'context': {'project': 'fixture', 'run_id': 'synthetic-review',
                                      'objective_sha256': hashlib.sha256(b'Review a controlled fixture').hexdigest(),
                                      'permissions_sha256': code_review._hash({'network': False}),
                                      'files': {k: hashlib.sha256(v.encode()).hexdigest()
                                                for k, v in self.texts.items()}},
                          'preflight': {k: k for k in ('reuse_search', 'module_placement', 'implementation_plan')},
                          'required_qa': ['regression-test']}
        self.ledger = []
        for key in self.candidate['preflight']:
            self.receipt(key, 'constraint', constraint=key)
        self.receipt('source', 'source')
        self.receipt('regression-test', 'qa')
        self.reviews = [self.review(a) for a in ['claude', 'antigravity']]
        self.answers = []

    def receipt(self, ident, kind, **extra):
        row = {'id': ident, 'kind': kind, 'sha256': 'f' * 64, 'executed': True, 'passed': True,
               'context': copy.deepcopy(self.candidate['context']),
               'alternative_sha256': code_review.fingerprint(self.candidate),
               'method': 'synthetic_unit_fixture', **extra}
        self.ledger.append(row)
        return row

    def review(self, agent):
        response = {'candidate_sha256': code_review.fingerprint(self.candidate),
                    'reviewed_files': list(self.texts), 'decision': 'approve',
                    'challenges': {k: {'status': 'pass', 'evidence_refs': ['source'],
                                      'notes': 'Synthetic assessed fixture, not provider output'}
                                   for k in code_review.CHALLENGES},
                    'objections': [], 'summary': 'Synthetic reviewer'}
        env = {'requested_agent': agent, 'effective_agent': agent, 'response': response,
               'attempt_ref': 'attempt-' + agent}
        self.receipt(env['attempt_ref'], 'constraint', constraint='review_transport', reviewer=agent,
                     phase='independent_code_review', response_sha256=code_review._hash(response))
        return env

    def stamp(self):
        for env in self.reviews:
            for row in self.ledger:
                if row['id'] == env['attempt_ref']:
                    row['response_sha256'] = code_review._hash(env['response'])

    def evaluate(self):
        self.stamp()
        return review_code_candidate(self.candidate, self.reviews, evidence=self.ledger,
                                     root=self.root, answers=self.answers)

    def finding(self, category='duplication', kind='semantic', severity='HIGH'):
        obj = {'id': 'O1', 'severity': severity, 'challenge': category,
               'sites': [{'file': 'existing.py', 'function': 'original', 'start': 1, 'end': 2},
                         {'file': 'candidate.py', 'function': 'duplicate', 'start': 1, 'end': 2}],
               'evidence_refs': ['source'], 'claim': 'Synthetic contextual finding',
               'impact': 'Repeated responsibility in controlled source example',
               'recommendation': 'Reuse if context and contracts match',
               'resolution_condition': 'Origin reviewer confirms controller evidence',
               'duplication_kind': kind if category == 'duplication' else 'not_applicable'}
        self.reviews[0]['response']['objections'].append(obj)
        return obj

    def test_01_exact_duplicate_finding_blocks_even_two_approvals(self):
        # Equal bodies; duplicate classification is supplied as a synthetic review, not inferred.
        self.texts['candidate.py'] = 'def duplicate(data):\n    return data[::-1]\n'
        (self.root / 'candidate.py').write_text(self.texts['candidate.py'])
        self.candidate['context']['files']['candidate.py'] = hashlib.sha256(self.texts['candidate.py'].encode()).hexdigest()
        identity = code_review.fingerprint(self.candidate)
        for row in self.ledger:
            row['context'] = copy.deepcopy(self.candidate['context']);row['alternative_sha256'] = identity
        for env in self.reviews:
            env['response']['candidate_sha256'] = identity
        self.finding(kind='exact')
        self.assertEqual(self.evaluate()['state'], 'changes_requested')

    def test_02_semantic_equivalence_finding_is_not_ignored(self):
        # Bounded fixture equivalence is verified, but the reviewer classification remains synthetic.
        for values in [[], [1], [3, -1, 3]]:
            self.assertEqual(values[::-1], list(reversed(values)))
        self.finding(kind='semantic')
        self.assertEqual(self.evaluate()['state'], 'changes_requested')

    def test_03_wrong_module_architecture_finding(self):
        self.finding(category='architecture')
        self.assertEqual(self.evaluate()['state'], 'changes_requested')

    def test_04_unnecessary_dependency_finding(self):
        self.finding(category='maintainability')
        self.assertEqual(self.evaluate()['state'], 'changes_requested')

    def test_05_duplicate_listener_finding_has_two_real_locations(self):
        obj = self.finding(category='performance')
        obj['sites'] = [{'file': 'ui.js', 'function': '<module>', 'start': x, 'end': x} for x in [1, 2]]
        self.assertEqual(self.evaluate()['state'], 'changes_requested')

    def test_06_executed_regression_test_fails_gate(self):
        # Real failing assertion in a fixed controller-owned fixture, never model-provided code.
        result = subprocess.run([sys.executable, '-c',
                                 'price = 100; percent = 10; actual = price * (1 + percent / 100); assert actual == 90'],
                                capture_output=True, text=True, timeout=3)
        self.assertNotEqual(result.returncode, 0)
        next(r for r in self.ledger if r['id'] == 'regression-test')['passed'] = result.returncode == 0
        self.assertEqual(self.evaluate()['state'], 'changes_requested')

    def test_07_legitimate_similarity_info_does_not_block(self):
        self.finding(kind='legitimate', severity='INFO')
        self.assertEqual(self.evaluate()['state'], 'approved_for_authorization')

    def test_08_high_refuted_requires_origin_confirmation_and_controller_receipt(self):
        self.finding()
        self.answers = [{'reviewer': 'claude', 'objection_id': 'O1', 'action': 'refute'}]
        self.assertEqual(self.evaluate()['state'], 'changes_requested')
        row = self.receipt('resolution', 'resolution', subject='claude:O1', resolves=['claude:O1'],
                           confirmed_by='codex')
        self.assertEqual(self.evaluate()['state'], 'changes_requested')
        row['confirmed_by'] = 'claude'
        self.assertEqual(self.evaluate()['state'], 'approved_for_authorization')

    def test_09_missing_fundamental_evidence(self):
        self.ledger = [r for r in self.ledger if r['id'] != 'regression-test']
        self.assertEqual(self.evaluate()['state'], 'needs_evidence')

    def test_10_clean_candidate_has_both_reviewers_but_no_operation_permission(self):
        result = self.evaluate()
        self.assertEqual(result['state'], 'approved_for_authorization')
        for key in ['implementation_allowed', 'production_authorized', 'activation_allowed']:
            self.assertFalse(result[key])

    def test_author_review_blocked_for_all_three_possible_authors(self):
        for author in code_review.PARTICIPANTS:
            with self.subTest(author=author):
                self.reviews[0]['effective_agent'] = author
                self.candidate['author'] = author
                self.candidate['contributors'] = [author]
                self.assertEqual(self.evaluate()['state'], 'blocked')

    def test_reviewer_substitution_or_duplicate_is_blocked(self):
        self.reviews[1]['effective_agent'] = 'claude'
        self.assertEqual(self.evaluate()['state'], 'blocked')

    def test_missing_second_reviewer_is_not_fake_consensus(self):
        self.reviews = self.reviews[:1]
        self.assertEqual(self.evaluate()['state'], 'needs_evidence')

    def test_changed_diff_invalidates_both_reviews_preflight_and_qa(self):
        self.candidate['diff_sha256'] = '1' * 64
        self.assertEqual(self.evaluate()['state'], 'needs_evidence')

    def test_changed_source_requires_fresh_review(self):
        (self.root / 'existing.py').write_text('new contents\n')
        self.assertNotEqual(self.evaluate()['state'], 'approved_for_authorization')

    def test_no_response_can_supply_own_receipts(self):
        self.reviews[0]['response']['evidence'] = [{'passed': True}]
        with self.assertRaises(IpanemaError):
            self.evaluate()

    def test_missing_five_challenge_field_is_rejected(self):
        del self.reviews[0]['response']['challenges']['architecture']
        with self.assertRaises(IpanemaError):
            self.evaluate()

    def test_source_citation_outside_scope_rejected(self):
        obj = self.finding();obj['sites'][0]['file'] = '../secret'
        with self.assertRaises(IpanemaError):
            self.evaluate()

    def test_unilateral_author_closure_and_wildcard_resolution_rejected(self):
        self.finding();self.answers = [{'reviewer': 'claude', 'objection_id': 'O1', 'action': 'accept'}]
        self.receipt('bad-resolution', 'resolution', subject='*', resolves=['claude:O1'], confirmed_by='claude')
        self.assertEqual(self.evaluate()['state'], 'changes_requested')

    def test_bad_line_number_and_missing_function_rejected(self):
        obj = self.finding();obj['sites'][0]['end'] = 999
        with self.assertRaises(IpanemaError):
            self.evaluate()
        obj['sites'][0]['end'] = 2;obj['sites'][0]['function'] = 'missing_fn'
        with self.assertRaises(IpanemaError):
            self.evaluate()

    def test_low_style_preference_does_not_block(self):
        self.finding(category='maintainability', severity='LOW')
        self.assertEqual(self.evaluate()['state'], 'approved_for_authorization')

    def test_blocker_not_overridden_by_missing_qa_or_votes(self):
        self.finding(severity='BLOCKER')
        self.ledger = [r for r in self.ledger if r['id'] != 'regression-test']
        self.assertEqual(self.evaluate()['state'], 'blocked')

    def test_scope_permission_and_objective_changes_invalidate_review(self):
        self.candidate['context']['permissions_sha256'] = 'e' * 64
        self.assertEqual(self.evaluate()['state'], 'needs_evidence')

    def test_unverified_transport_cannot_count_as_independent_review(self):
        self.ledger = [r for r in self.ledger if r['id'] != 'attempt-antigravity']
        self.assertEqual(self.evaluate()['state'], 'needs_evidence')

    def test_packet_excludes_author_conclusions_and_peer_reviews(self):
        self.candidate['author_rationale'] = 'Do not seed reviewer conclusions'
        packet = code_review.independent_packet(self.candidate, self.texts, 'synthetic diff',
                                                ['unit'], {'network': False})
        self.assertNotIn('author_rationale', packet)
        self.assertNotIn('peer_reviews', packet)
        self.assertNotIn('author_rationale', packet['candidate'])
        packet['candidate']['author'] = 'claude'
        self.assertEqual(self.candidate['author'], 'codex')
        with self.assertRaises(IpanemaError):
            code_review.independent_packet(self.candidate, self.texts, 'changed diff', [], {})

    def test_no_qa_list_cannot_be_silently_empty(self):
        self.candidate['required_qa'] = []
        with self.assertRaises(IpanemaError):
            self.evaluate()

    def test_readonly_related_source_symlink_cannot_escape(self):
        (self.root / 'candidate.py').unlink()
        (self.root / 'candidate.py').symlink_to(self.root / 'existing.py')
        with self.assertRaises(IpanemaError):
            self.evaluate()

    def test_medium_objection_requires_author_answer_not_silent_approval(self):
        self.finding(severity='MEDIUM')
        self.assertEqual(self.evaluate()['state'], 'needs_evidence')
        self.answers = [{'reviewer': 'claude', 'objection_id': 'O1', 'action': 'request_evidence'}]
        result = self.evaluate()
        self.assertEqual(result['state'], 'approved_for_authorization')
        self.assertFalse(result['findings'][0]['closed'])

    def test_same_objection_id_of_another_reviewer_cannot_close_origin(self):
        obj = self.finding()
        self.reviews[1]['response']['objections'].append(copy.deepcopy(obj))
        self.answers = [{'reviewer': 'claude', 'objection_id': 'O1', 'action': 'refute'}]
        self.receipt('resolution', 'resolution', subject='claude:O1', resolves=['claude:O1'], confirmed_by='claude')
        result = self.evaluate()
        self.assertEqual(result['state'], 'changes_requested')
        self.assertIn('antigravity:O1', result['changes'])

    def test_coauthors_leave_no_two_independent_reviewers(self):
        self.candidate['contributors'].append('claude')
        self.assertEqual(self.evaluate()['state'], 'blocked')

    def test_permission_packet_mismatch_cannot_be_sent_to_review(self):
        with self.assertRaises(IpanemaError):
            code_review.independent_packet(self.candidate, self.texts, 'synthetic diff', [], {'network': True})


if __name__ == '__main__':
    unittest.main()
