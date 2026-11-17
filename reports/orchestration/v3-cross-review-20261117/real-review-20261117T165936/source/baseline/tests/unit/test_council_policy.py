"""Política pura del consejo. Todos los proveedores/recibos son fixtures offline."""
import copy
import unittest

from tests.support import ROOT
from ipanema.core import IpanemaError
from ipanema.orchestration.council import (
    AGENTS, CRITERIA, HARD_CONSTRAINTS, aggregate, config_policy, contract,
    participant_task, validate_objections, validate_proposal, alternative_fingerprint,
)


def context(**updates):
    value = {'project': 'fixture', 'run_id': 'synthetic-run-1', 'source_sha256': 'a' * 64,
             'objective_sha256': 'b' * 64, 'files': ['fixture.txt'], 'required_constraints': []}
    return {**value, **updates}


def proposal(agent='claude', *, effective_agent=None, alternative='native', status='pass'):
    response = copy.deepcopy(contract('council_proposal')['example'])
    analysis = response['analysis']
    analysis.update(problem='Caso sintético', cause='Código del fixture', recommendation=alternative,
                    files=['fixture.txt'], native_components=['fixture component'], risks=[])
    alt = analysis['alternatives'][0]
    alt.update(id=alternative, files=['fixture.txt'], description='Usar componente existente')
    alt['constraints'] = {k: {'status': status, 'evidence_refs': []} for k in CRITERIA}
    return {'requested_agent': agent, 'effective_agent': effective_agent or agent, 'response': response}


def receipts(ctx, *, alternative='native', criteria=CRITERIA, passed=True, fingerprint=None):
    fingerprint = fingerprint or alternative_fingerprint(proposal(alternative=alternative)['response']['analysis']['alternatives'][0])
    return [{'id': 'check-' + alternative + '-' + k, 'kind': 'constraint', 'subject': alternative,
             'constraint': k, 'executed': True, 'passed': passed, 'sha256': 'c' * 64,
             'context': copy.deepcopy(ctx), 'alternative_sha256': fingerprint} for k in criteria]


def objection(agent='commandcode', *, alternative='native', severity='critical', resolved=False):
    response = copy.deepcopy(contract('council_objection')['example'])
    response['objections'][0].update(alternative_id=alternative, severity=severity,
                                     status='resolved' if resolved else 'open')
    return {'requested_agent': agent, 'effective_agent': agent, 'response': response}


class CouncilPolicyTests(unittest.TestCase):
    def setUp(self):
        from tests.support import historical_trio_policy
        historical_trio_policy(self)
        self.ctx = context()
        self.proposals = [proposal(agent) for agent in AGENTS]

    def decide(self, proposals=None, objections=None, evidence=None, ctx=None):
        return aggregate(self.proposals if proposals is None else proposals,
                         [] if objections is None else objections,
                         evidence=receipts(self.ctx) if evidence is None else evidence,
                         context=self.ctx if ctx is None else ctx, project='fixture', objective='synthetic case')

    def test_proportional_policy_and_bounded_rounds(self):
        self.assertFalse(config_policy('L1')['enabled'])
        self.assertTrue(config_policy('L3')['enabled'])
        self.assertTrue(config_policy('L1', 'full')['enabled'])
        self.assertEqual(config_policy('L4')['max_rounds'], 2)
        for mode, rounds in [('off', 2), ('auto', 3), ('auto', 0), ('auto', True)]:
            with self.subTest(mode=mode, rounds=rounds), self.assertRaises(IpanemaError):
                config_policy('L3', mode, rounds)

    def test_first_round_is_blind_and_read_only(self):
        task = participant_task('claude', 0, ['fixture.txt'], 'strong', 'case', self.proposals)
        self.assertEqual(task['allowed_files'], [])
        self.assertEqual(task['role'], 'council_proposal')
        self.assertNotIn('peer_proposals', task['council_context'])
        second = participant_task('codex', 1, ['fixture.txt'], 'strong', 'case', self.proposals)
        self.assertEqual(second['role'], 'council_objection')
        second['council_context']['peer_proposals'].clear()
        self.assertEqual(len(self.proposals), 3)

    def test_schema_and_scope_cannot_request_writes(self):
        response = self.proposals[0]['response']
        self.assertEqual(validate_proposal(response, ['fixture.txt'])['analysis']['recommendation'], 'native')
        for field, value in [('changes', [{'path': 'fixture.txt'}]), ('analysis', {})]:
            bad = copy.deepcopy(response); bad[field] = value
            with self.assertRaises(IpanemaError): validate_proposal(bad, ['fixture.txt'])
        bad = copy.deepcopy(response); bad['analysis']['files'] = ['outside.tpl']
        with self.assertRaises(IpanemaError): validate_proposal(bad, ['fixture.txt'])
        bad = copy.deepcopy(response); bad['analysis']['confidence'] = True
        with self.assertRaises(IpanemaError): validate_proposal(bad, ['fixture.txt'])

    def test_three_proven_independent_proposals_allow_local_only(self):
        adr = self.decide()
        self.assertEqual(adr['status'], 'approved')
        self.assertTrue(adr['implementation_allowed'])
        self.assertTrue(adr['coverage']['complete'])
        self.assertFalse(adr['production_authorized'])
        self.assertEqual(adr['files'], ['fixture.txt'])
        self.assertTrue(adr['post_implementation_requirements'][0]['required'])

    def test_hashes_and_three_claims_do_not_prove_constraints(self):
        source = {'id': 'file-fixture', 'kind': 'source', 'subject': 'fixture.txt', 'executed': True,
                  'passed': True, 'sha256': 'a' * 64, 'context': self.ctx}
        for evidence in [[], [source]]:
            adr = self.decide(evidence=evidence)
            self.assertEqual(adr['status'], 'needs_evidence')
            self.assertFalse(adr['implementation_allowed'])

    def test_failed_hard_constraint_cannot_be_averaged(self):
        proof = receipts(self.ctx)
        next(r for r in proof if r['constraint'] == 'security')['passed'] = False
        adr = self.decide(evidence=proof)
        self.assertEqual(adr['status'], 'blocked')
        self.assertIsNone(adr['selected_alternative'])

    def test_missing_and_duplicate_effective_providers_never_make_three_votes(self):
        for proposals in [self.proposals[:2], [proposal('claude', effective_agent='codex'), proposal('codex'), proposal('commandcode')],
                          [proposal('claude'), proposal('claude'), proposal('commandcode')]]:
            adr = self.decide(proposals=proposals)
            self.assertFalse(adr['coverage']['complete'])
            self.assertFalse(adr['implementation_allowed'])

    def test_critical_objection_cannot_be_self_resolved(self):
        obj = objection(resolved=True)
        adr = self.decide(objections=[obj])
        self.assertEqual(adr['status'], 'blocked')
        self.assertFalse(adr['objections'][0]['resolved_by_controller'])

    def test_controller_receipt_resolves_specific_objection(self):
        obj = objection()
        evidence = receipts(self.ctx) + [{'id': 'resolution-O1', 'kind': 'resolution', 'subject': 'native',
                                        'resolves': ['commandcode:O1'], 'executed': True, 'passed': True,
                                        'sha256': 'd' * 64, 'context': self.ctx,
                                        'alternative_sha256': receipts(self.ctx)[0]['alternative_sha256']}]
        adr = self.decide(objections=[obj], evidence=evidence)
        self.assertTrue(adr['implementation_allowed'])
        self.assertEqual(adr['status'], 'approved_with_conditions')
        self.assertNotEqual(adr['coverage']['consensus'], 'complete')
        self.assertTrue(adr['objections'][0]['resolved_by_controller'])

    def test_source_hash_cannot_resolve_objection(self):
        proof = receipts(self.ctx) + [{'id': 'fake-resolution', 'kind': 'source', 'subject': 'native',
                                     'resolves': ['commandcode:O1'], 'executed': True, 'passed': True,
                                     'sha256': 'd' * 64, 'context': self.ctx}]
        self.assertEqual(self.decide(objections=[objection()], evidence=proof)['status'], 'blocked')

    def test_transferred_receipts_are_rejected(self):
        for mutation in [{'project': 'other'}, {'run_id': 'other'}, {'source_sha256': 'd' * 64},
                         {'objective_sha256': 'd' * 64}]:
            with self.subTest(mutation=mutation):
                adr = self.decide(evidence=receipts(context(**mutation)))
                self.assertFalse(adr['implementation_allowed'])
                self.assertEqual(adr['status'], 'needs_evidence')

    def test_unverified_refs_are_not_covered_by_unrelated_positive_checks(self):
        self.proposals[0]['response']['analysis']['evidence_refs'] = ['invented-source']
        adr = self.decide()
        self.assertEqual(adr['status'], 'needs_evidence')

    def test_required_seo_and_performance_need_own_receipts(self):
        ctx = context(required_constraints=['seo', 'performance'])
        proof = receipts(ctx, criteria=HARD_CONSTRAINTS)
        adr = self.decide(evidence=proof, ctx=ctx)
        self.assertEqual(adr['status'], 'needs_evidence')
        self.assertFalse(adr['implementation_allowed'])
        self.assertTrue(all(c['required'] for c in adr['conditions']))

    def test_optional_unknowns_are_conditions_not_hard_failure(self):
        adr = self.decide(evidence=receipts(self.ctx, criteria=HARD_CONSTRAINTS))
        self.assertEqual(adr['status'], 'approved_with_conditions')
        self.assertTrue(adr['implementation_allowed'])
        self.assertTrue(all(not c['required'] and c['status'] == 'pending' for c in adr['conditions']))

    def test_no_majority_rule_among_equally_proven_alternatives(self):
        proposals = [proposal('claude'), proposal('codex'), proposal('commandcode', alternative='other')]
        adr = self.decide(proposals=proposals, evidence=receipts(self.ctx) + receipts(self.ctx, alternative='other'))
        self.assertEqual(adr['status'], 'needs_evidence')
        self.assertFalse(adr['implementation_allowed'])

    def test_verified_comparison_can_select_without_majority(self):
        proposals = [proposal('claude', alternative='other'), proposal('codex', alternative='other'), proposal('commandcode')]
        proof = receipts(self.ctx) + receipts(self.ctx, alternative='other')
        next(r for r in proof if r['subject'] == 'other' and r['constraint'] == 'execution_cost')['passed'] = False
        adr = self.decide(proposals=proposals, evidence=proof)
        self.assertEqual(adr['selected_alternative'], 'native')
        self.assertTrue(adr['implementation_allowed'])

    def test_declared_constraint_conflict_needs_explicit_resolution(self):
        self.proposals[0]['response']['analysis']['alternatives'][0]['constraints']['compatibility']['status'] = 'fail'
        self.assertFalse(self.decide()['implementation_allowed'])
        proof = receipts(self.ctx) + [{'id': 'resolve-conflict', 'kind': 'resolution', 'subject': 'native',
                                     'resolves': ['constraint:native:compatibility'], 'executed': True,
                                     'passed': True, 'sha256': 'd' * 64, 'context': self.ctx,
                                     'alternative_sha256': receipts(self.ctx)[0]['alternative_sha256']}]
        self.assertTrue(self.decide(evidence=proof)['implementation_allowed'])

    def test_debate_can_be_required_and_unavailable_reply_blocks(self):
        ctx = context(require_objections=True)
        adr = self.decide(evidence=receipts(ctx), ctx=ctx)
        self.assertFalse(adr['implementation_allowed'])
        replies = []
        for agent in AGENTS:
            obj = objection(agent); obj['response']['objections'] = []; replies.append(obj)
        adr = self.decide(objections=replies, evidence=receipts(ctx), ctx=ctx)
        self.assertTrue(adr['implementation_allowed'])
        self.assertTrue(adr['coverage']['objections_complete'])

    def test_same_local_id_cannot_merge_distinct_solutions(self):
        for field, value in [('description', 'Create an incompatible component'), ('files', []), ('tests', ['Different acceptance'])]:
            with self.subTest(field=field):
                proposals = copy.deepcopy(self.proposals)
                proposals[1]['response']['analysis']['alternatives'][0][field] = value
                adr = self.decide(proposals=proposals)
                self.assertEqual(adr['status'], 'needs_evidence')
                self.assertFalse(adr['implementation_allowed'])
                self.assertNotEqual(adr['coverage']['consensus'], 'complete')
                self.assertEqual(adr['matrix'][0]['files'], [])
                self.assertTrue(adr['contradictions'])

    def test_receipts_cannot_transfer_to_changed_solution_with_same_id(self):
        proposals = copy.deepcopy(self.proposals)
        for env in proposals:
            env['response']['analysis']['alternatives'][0]['description'] = 'A different implementation'
        adr = self.decide(proposals=proposals)
        self.assertEqual(adr['status'], 'needs_evidence')
        self.assertFalse(adr['implementation_allowed'])

    def test_receipts_without_solution_binding_do_not_approve(self):
        evidence = receipts(self.ctx)
        for receipt in evidence: receipt.pop('alternative_sha256')
        self.assertFalse(self.decide(evidence=evidence)['implementation_allowed'])

    def test_model_cannot_self_declare_file_authority(self):
        ctx = context(); ctx.pop('files')
        adr = self.decide(evidence=receipts(ctx), ctx=ctx)
        self.assertFalse(adr['implementation_allowed'])
        self.assertEqual(adr['files'], [])

    def test_partial_debate_is_not_complete(self):
        ctx = context(require_objections=True)
        replies = []
        for agent in AGENTS[:2]:
            row = objection(agent); row['response']['objections'] = []; replies.append(row)
        adr = self.decide(objections=replies, evidence=receipts(ctx), ctx=ctx)
        self.assertFalse(adr['implementation_allowed'])
        self.assertFalse(adr['coverage']['objections_complete'])

    def two_options(self):
        proposals = copy.deepcopy(self.proposals)
        for env in proposals:
            other = copy.deepcopy(env['response']['analysis']['alternatives'][0])
            other['id'] = 'compose'
            env['response']['analysis']['alternatives'].append(other)
        return proposals

    def final_replies(self, preference):
        replies = []
        for agent in AGENTS:
            row = objection(agent)
            row['response']['objections'] = []
            row['response']['preferred_alternative'] = preference
            replies.append(row)
        return replies

    def test_final_unanimous_debate_can_replace_initial_preference(self):
        adr = self.decide(proposals=self.two_options(), objections=self.final_replies('compose'),
                          evidence=receipts(self.ctx) + receipts(self.ctx, alternative='compose'))
        self.assertEqual(adr['selected_alternative'], 'compose')
        self.assertTrue(adr['implementation_allowed'])
        self.assertEqual(adr['coverage']['consensus'], 'complete')
        self.assertEqual(set(adr['final_preferences'].values()), {'compose'})

    def test_invalid_and_missing_final_preferences_do_not_reuse_stale_consensus(self):
        for preference in ['not-proposed', None, 123]:
            with self.subTest(preference=preference):
                adr = self.decide(proposals=self.two_options(), objections=self.final_replies(preference),
                                  evidence=receipts(self.ctx) + receipts(self.ctx, alternative='compose'))
                self.assertFalse(adr['implementation_allowed'])
                self.assertEqual(adr['status'], 'needs_evidence')
                self.assertNotEqual(adr['coverage']['consensus'], 'complete')

    def test_final_majority_cannot_select_tied_alternative(self):
        replies = self.final_replies('compose')
        replies[0]['response']['preferred_alternative'] = 'native'
        adr = self.decide(proposals=self.two_options(), objections=replies,
                          evidence=receipts(self.ctx) + receipts(self.ctx, alternative='compose'))
        self.assertFalse(adr['implementation_allowed'])
        self.assertEqual(adr['status'], 'needs_evidence')

    def test_final_preference_never_overrides_failed_hard_constraint(self):
        proof = receipts(self.ctx) + receipts(self.ctx, alternative='compose')
        next(r for r in proof if r['subject'] == 'compose' and r['constraint'] == 'security')['passed'] = False
        adr = self.decide(proposals=self.two_options(), objections=self.final_replies('compose'), evidence=proof)
        self.assertEqual(adr['selected_alternative'], 'native')
        self.assertNotEqual(adr['coverage']['consensus'], 'complete')
        self.assertEqual(adr['status'], 'approved_with_conditions')


if __name__ == '__main__':
    unittest.main()
