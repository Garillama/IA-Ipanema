"""Focused synthetic tests for explicit candidate/context/write contracts."""
import copy
import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tests.support import make_project
from ipanema.core import IpanemaError, Project, digest
from ipanema.orchestration import council, engine, planner


class FileContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = make_project(Path(self.tmp.name), theme=False)
        for name in ('candidate/a.tpl', 'candidate/b.tpl',
                     'context/one.tpl', 'context/two.tpl', 'context/three.tpl',
                     'context/four.tpl', 'context/five.tpl', 'context/six.tpl',
                     'context/seven.tpl'):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('fixture ' + name + '\n')
        self.project = Project(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def plan(self, *, read_only=True):
        return planner.make_plan(
            self.project, 'Revisión de solo lectura de dos candidatos y sus dependencias',
            candidate_files=['candidate/a.tpl', 'candidate/b.tpl'],
            context_files=[f'context/{n}.tpl' for n in
                           ('one', 'two', 'three', 'four', 'five', 'six', 'seven')],
            scope='workspace', read_only=read_only, council_mode='full')

    def test_two_candidates_seven_context_and_dual_council_are_read_only(self):
        plan = self.plan()
        self.assertEqual(plan['candidate_files'], ['candidate/a.tpl', 'candidate/b.tpl'])
        self.assertEqual(len(plan['context_files']), 7)
        self.assertEqual(plan['write_files'], [])
        self.assertEqual(plan['allowed_files'], plan['candidate_files'] + plan['context_files'])
        self.assertEqual(plan['classification']['level'], 'L2')
        self.assertTrue(all(t['read_files'] == plan['allowed_files'] for t in plan['tasks']))
        self.assertTrue(all(t['allowed_files'] == [] for t in plan['tasks']))
        self.assertEqual(planner.validate_file_contract(plan), plan)

    def test_context_count_does_not_promote_candidate_risk(self):
        small = planner.make_plan(self.project, 'Revisa dos archivos',
            candidate_files=['candidate/a.tpl', 'candidate/b.tpl'], context_files=[],
            scope='workspace', read_only=True)
        many = self.plan()
        self.assertEqual(small['classification']['level'], many['classification']['level'])

    def test_write_subset_is_limited_to_candidates_and_context_sets_are_disjoint(self):
        plan = planner.make_plan(
            self.project, 'Edit only the first fixture candidate',
            candidate_files=['candidate/a.tpl', 'candidate/b.tpl'],
            context_files=['context/one.tpl'], write_files=['candidate/a.tpl'],
            scope='workspace', read_only=False, council_mode='full')
        self.assertEqual(plan['write_files'], ['candidate/a.tpl'])
        implementation = next(task for task in plan['tasks'] if task['role'] == 'implementation')
        self.assertEqual(implementation['allowed_files'], ['candidate/a.tpl'])
        self.assertTrue(all(task['allowed_files'] == [] for task in plan['tasks'] if task is not implementation))
        planner.validate_file_contract(plan)
        with self.assertRaises(IpanemaError):
            planner.make_plan(self.project, 'Invalid overlapping sets', candidate_files=['candidate/a.tpl'],
                context_files=['candidate/a.tpl'], write_files=[], scope='workspace', read_only=True)

    def test_context_can_be_cited_as_evidence_but_not_as_candidate_diff(self):
        plan = self.plan()
        binding = {
            'project': self.project.id, 'run_id': 'synthetic-run',
            'candidate_files': plan['candidate_files'], 'context_files': plan['context_files'],
            'write_files': [],
            'files': {name: digest(self.root / name) for name in plan['allowed_files']},
        }
        ledger = [{
            'id': 'source:' + name, 'kind': 'source', 'subject': name,
            'executed': True, 'passed': True, 'sha256': binding['files'][name],
            'context': binding,
        } for name in plan['allowed_files']]
        proposal = copy.deepcopy(council.contract('council_proposal')['example'])
        proposal['analysis'].update(
            problem='Fixture', cause='Fixture', recommendation='native',
            evidence_refs=['source:context/one.tpl'], files=['candidate/a.tpl'],
        )
        proposal['analysis']['alternatives'][0]['files'] = ['candidate/a.tpl']
        normalized = council.validate_proposal(
            proposal, plan['candidate_files'], evidence_ledger=ledger, evidence_context=binding)
        self.assertIn('source:context/one.tpl', normalized['analysis']['evidence_refs'])
        proposal['analysis']['files'] = ['context/one.tpl']
        with self.assertRaises(IpanemaError):
            council.validate_proposal(
                proposal, plan['candidate_files'], evidence_ledger=ledger, evidence_context=binding)
        write = {'role': 'implementation', 'allowed_files': plan['candidate_files']}
        context_diff = {'decision': 'proposed', 'changes': [{'path': 'context/one.tpl',
                        'before_sha256': digest(self.root / 'context/one.tpl'), 'content': 'mutated'}]}
        with self.assertRaises(IpanemaError):
            engine.validate_response(write, context_diff, self.root)

    def test_nonexistent_and_other_run_evidence_references_are_rejected(self):
        plan = self.plan()
        candidate = plan['candidate_files'][0]
        current = {'project': 'sample', 'run_id': 'run-current', 'candidate_files': [candidate],
                   'context_files': [], 'write_files': [],
                   'files': {candidate: digest(self.root / candidate)}}
        receipt = {'id': 'source:' + candidate, 'kind': 'source', 'subject': candidate,
                   'executed': True, 'passed': True, 'sha256': current['files'][candidate],
                   'context': current}
        base = copy.deepcopy(council.contract('council_objection')['example'])
        base['objections'][0]['evidence_refs'] = ['invented-id']
        with self.assertRaises(IpanemaError):
            council.validate_objections(base, [candidate], evidence_ledger=[receipt], evidence_context=current)

        old_run = copy.deepcopy(current)
        old_run['run_id'] = 'run-previous'
        old_receipt = {**receipt, 'context': old_run}
        base['objections'][0]['evidence_refs'] = [receipt['id']]
        with self.assertRaises(IpanemaError):
            council.validate_objections(base, [candidate], evidence_ledger=[old_receipt], evidence_context=current)

        another_candidate = copy.deepcopy(current)
        another_candidate['candidate_files'] = ['candidate/b.tpl']
        another_candidate['files'] = {'candidate/b.tpl': digest(self.root / 'candidate/b.tpl')}
        old_candidate_receipt = {**receipt, 'context': another_candidate}
        with self.assertRaises(IpanemaError):
            council.validate_objections(base, [candidate], evidence_ledger=[old_candidate_receipt],
                                        evidence_context=current)

    def test_arbitrary_normalized_map_is_not_trusted_as_controller_ledger(self):
        candidate = 'candidate/a.tpl'
        binding = {'project': 'sample', 'run_id': 'run-current', 'candidate_files': [candidate],
                   'context_files': [], 'write_files': [], 'files': {candidate: 'a' * 64}}
        forged = {'invented': {'id': 'source:' + candidate, 'kind': 'source', 'subject': candidate,
                   'executed': True, 'passed': True, 'sha256': 'a' * 64, 'context': binding}}
        response = copy.deepcopy(council.contract('council_objection')['example'])
        response['objections'][0]['evidence_refs'] = ['source:' + candidate]
        with self.assertRaises(IpanemaError):
            council.validate_objections(response, [candidate], evidence_ledger=forged, evidence_context=binding)

    def test_valid_current_candidate_evidence_is_accepted_in_questions_and_defense(self):
        candidate = 'candidate/a.tpl'
        binding = {'project': 'sample', 'run_id': 'run-current', 'candidate_files': [candidate],
                   'context_files': [], 'write_files': [],
                   'files': {candidate: hashlib.sha256(b'fixture candidate/a.tpl\n').hexdigest()}}
        ledger = [{'id': 'source:' + candidate, 'kind': 'source', 'subject': candidate,
                   'executed': True, 'passed': True, 'sha256': binding['files'][candidate],
                   'context': binding}]
        response = copy.deepcopy(council.contract('council_objection')['example'])
        response['objections'][0]['evidence_refs'] = ['source:' + candidate]
        response['questions'] = [{'id': 'Q1', 'to_agent': 'codex', 'alternative_id': 'native',
                                  'question': 'Revisar fuente', 'evidence_refs': ['source:' + candidate]}]
        council.validate_objections(response, [candidate], evidence_ledger=ledger, evidence_context=binding)

        defense = copy.deepcopy(council.contract('council_defense')['example'])
        defense['objections'][0]['evidence_refs'] = ['source:' + candidate]
        defense['answers'] = [{'question_id': 'Q1', 'from_agent': 'claude', 'answer': 'Revisado',
                               'evidence_refs': ['source:' + candidate], 'disposition': 'defend'}]
        council.validate_defense(defense, [candidate], expected_answers={('claude', 'Q1')},
                                 evidence_ledger=ledger, evidence_context=binding)

    def test_read_only_and_modified_plan_cannot_expand_write_set_without_regeneration(self):
        plan = self.plan()
        altered = copy.deepcopy(plan)
        altered['write_files'] = ['context/one.tpl']
        altered['tasks'][0]['allowed_files'] = ['context/one.tpl']
        with self.assertRaises(IpanemaError):
            planner.validate_file_contract(altered)

        changed_task = copy.deepcopy(plan['tasks'][0])
        changed_task['allowed_files'] = ['candidate/a.tpl']
        with self.assertRaises(IpanemaError):
            planner.validate_file_contract({**plan, 'tasks': [changed_task] + plan['tasks'][1:]})

    def test_legacy_plan_is_rejected_explicitly_and_old_receipt_contract_still_parses(self):
        plan = self.plan()
        legacy = {k: v for k, v in plan.items()
                  if k not in ('candidate_files', 'context_files', 'write_files',
                               'file_contract_version', 'file_contract_sha256')}
        with self.assertRaisesRegex(IpanemaError, 'obsoleto'):
            planner.validate_file_contract(legacy)
        with patch('ipanema.orchestration.engine.worker') as worker, \
             patch('ipanema.orchestration.engine.central_qa') as qa:
            with self.assertRaisesRegex(IpanemaError, 'obsoleto'):
                engine.execute(self.project, legacy, authorize=True)
        worker.assert_not_called()
        qa.assert_not_called()
        # Historical untyped evidence bindings remain readable under their original meaning.
        legacy_binding = {'project': 'sample', 'run_id': 'legacy-run', 'files': ['fixture.txt']}
        historical = [{'id': 'legacy-check', 'kind': 'constraint', 'subject': 'native',
                       'constraint': 'security', 'executed': True, 'passed': True,
                       'sha256': 'a' * 64, 'context': legacy_binding,
                       'alternative_sha256': 'b' * 64}]
        valid, invalid = council._ledger(historical, legacy_binding)
        self.assertEqual(set(valid), {'legacy-check'})
        self.assertEqual(invalid, [])

    def test_engine_rejects_read_only_write_attempt_before_provider_or_qa(self):
        plan = self.plan()
        task = {'role': 'audit', 'allowed_files': []}
        response = {'decision': 'proposed', 'changes': [{'path': 'candidate/a.tpl',
                   'before_sha256': digest(self.root / 'candidate/a.tpl'), 'content': 'changed'}]}
        with self.assertRaises(IpanemaError):
            engine.validate_response(task, response, self.root)
        altered = copy.deepcopy(plan)
        altered['tasks'][0]['allowed_files'] = ['candidate/a.tpl']
        with patch('ipanema.orchestration.engine.worker') as worker, \
             patch('ipanema.orchestration.engine.central_qa') as qa:
            with self.assertRaises(IpanemaError):
                engine.execute(self.project, altered, authorize=True)
        worker.assert_not_called()
        qa.assert_not_called()


if __name__ == '__main__':
    unittest.main()
