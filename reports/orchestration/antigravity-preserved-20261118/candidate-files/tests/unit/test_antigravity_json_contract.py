"""Focused offline contract tests for the documented Antigravity JSON envelope."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ipanema.orchestration import adapters,engine,planner
from ipanema.core import IpanemaError,Project
from tests.support import make_project


class AntigravityJsonContractTests(unittest.TestCase):
    schema = {
        'type': 'object',
        'required': ['decision', 'changes'],
        'properties': {
            'decision': {'type': 'string', 'enum': ['proposed', 'approve']},
            'changes': {'type': 'array', 'maxItems': 0},
        },
        'additionalProperties': False,
    }
    payload = {'decision': 'proposed', 'changes': []}

    def envelope(self, *, status='SUCCESS', structured_output=None, response=None,
                 schema=None, conversation_id='synthetic-conversation', duration_seconds=0.01,
                 num_turns=1, usage=None, extra=None):
        payload=structured_output if structured_output is not None else self.payload
        value = {'conversation_id':conversation_id,'status': status,
                 'response':response if response is not None else json.dumps(payload),
                 'duration_seconds':duration_seconds,'num_turns':num_turns,
                 'usage':usage if usage is not None else {'input_tokens':1,'output_tokens':1,
                     'thinking_tokens':0,'cache_read_tokens':0,'total_tokens':2}}
        if structured_output is not None:
            value['structured_output'] = structured_output
        if schema is not None:
            value['json_schema']=schema
        if extra:value.update(extra)
        return json.dumps(value)

    def test_accepts_success_envelope_and_validates_structured_output(self):
        result = adapters.parse_response(
            'antigravity', self.envelope(structured_output=self.payload,schema=self.schema),
            expected_schema=self.schema)
        self.assertEqual(result, self.payload)

    def test_rejects_error_and_cancelled_execution_statuses(self):
        for status in ('ERROR', 'CANCELED', 'INTERRUPTED', 'INVALID', 'RUNNING'):
            with self.subTest(status=status), self.assertRaisesRegex(
                    adapters.ResponseContractError, 'antigravity_execution_status'):
                adapters.parse_response('antigravity', self.envelope(
                    status=status, structured_output=self.payload,schema=self.schema), expected_schema=self.schema)

    def test_rejects_missing_status_and_missing_structured_output(self):
        with self.assertRaisesRegex(adapters.ResponseContractError, 'envelope_incomplete'):
            adapters.parse_response('antigravity', json.dumps({'response': 'ok'}), expected_schema=self.schema)
        with self.assertRaisesRegex(adapters.ResponseContractError, 'antigravity_structured_output_missing'):
            adapters.parse_response('antigravity', self.envelope(schema=self.schema), expected_schema=self.schema)
        with self.assertRaisesRegex(adapters.ResponseContractError, 'antigravity_json_invalid'):
            adapters.parse_response('antigravity', '', expected_schema=self.schema)
        empty_response=json.loads(self.envelope(structured_output=self.payload,schema=self.schema))
        empty_response['response']='  '
        with self.assertRaisesRegex(adapters.ResponseContractError, 'antigravity_response_missing'):
            adapters.parse_response('antigravity', json.dumps(empty_response), expected_schema=self.schema)

    def test_rejects_incomplete_schema_payload(self):
        with self.assertRaisesRegex(adapters.ResponseContractError, 'missing_field'):
            adapters.parse_response('antigravity', self.envelope(
                structured_output={'decision': 'proposed'},schema=self.schema), expected_schema=self.schema)

    def test_rejects_malformed_truncated_and_duplicate_key_json(self):
        for raw in ('{broken', '{"status":"SUCCESS"',
                    '{"status":"SUCCESS","status":"ERROR"}'):
            with self.subTest(raw=raw), self.assertRaises(adapters.ResponseContractError):
                adapters.parse_response('antigravity', raw, expected_schema=self.schema)

    def test_rejects_schema_incompatible_output(self):
        with self.assertRaisesRegex(adapters.ResponseContractError, 'schema_enum'):
            adapters.parse_response('antigravity', self.envelope(
                structured_output={'decision': 'unknown', 'changes': []},schema=self.schema),
                expected_schema=self.schema)

    def test_rejects_identity_claim_in_schema_bound_payload(self):
        payload = {**self.payload, 'agent': 'codex'}
        with self.assertRaisesRegex(adapters.ResponseContractError, 'identity_claim_rejected'):
            adapters.parse_response('antigravity', self.envelope(
                structured_output=payload,schema=self.schema), expected_schema=self.schema)

    def test_requires_schema_for_antigravity_and_rejects_unsupported_roles(self):
        with patch('ipanema.orchestration.adapters.enabled_agents',return_value=('claude','codex','antigravity')), \
             patch('ipanema.orchestration.adapters.shutil.which',return_value='/synthetic/agy'):
            with self.assertRaisesRegex(IpanemaError,'JSON Schema verificado'):
                adapters.argv('antigravity','synthetic-model',prompt='synthetic')
        with self.assertRaisesRegex(adapters.ResponseContractError,'antigravity_schema_required'):
            adapters.parse_response('antigravity',self.envelope())
        self.assertEqual(adapters.ANTIGRAVITY_SCHEMA_ROLES,
                         frozenset(('council_proposal','council_objection','council_defense')))

    def test_prompt_byte_limit_boundaries_do_not_start_a_provider(self):
        with patch('ipanema.orchestration.adapters.enabled_agents',return_value=('claude','codex','antigravity')), \
             patch('ipanema.orchestration.adapters.shutil.which',return_value='/synthetic/agy'):
            args=adapters.argv('antigravity','synthetic-model',response_schema=self.schema,
                               prompt='x'*(adapters.ANTIGRAVITY_MAX_PROMPT_BYTES-1))
            self.assertEqual(len(args[-1].encode()),adapters.ANTIGRAVITY_MAX_PROMPT_BYTES-1)
            args=adapters.argv('antigravity','synthetic-model',response_schema=self.schema,
                               prompt='x'*adapters.ANTIGRAVITY_MAX_PROMPT_BYTES)
            self.assertEqual(len(args[-1].encode()),adapters.ANTIGRAVITY_MAX_PROMPT_BYTES)
            with self.assertRaisesRegex(IpanemaError,'límite explícito'):
                adapters.argv('antigravity','synthetic-model',response_schema=self.schema,
                              prompt='x'*(adapters.ANTIGRAVITY_MAX_PROMPT_BYTES+1))
            with self.assertRaisesRegex(IpanemaError,'límite explícito'):
                adapters.argv('antigravity','synthetic-model',response_schema=self.schema,
                              prompt='é'*(adapters.ANTIGRAVITY_MAX_PROMPT_BYTES//2+1))

    def test_success_envelope_required_fields_types_and_identity_fail_closed(self):
        valid=self.envelope(structured_output=self.payload,schema=self.schema)
        for field in ('conversation_id','duration_seconds','num_turns','usage'):
            value=json.loads(valid);value.pop(field)
            with self.subTest(missing=field), self.assertRaisesRegex(
                    adapters.ResponseContractError,'antigravity_envelope_incomplete'):
                adapters.parse_response('antigravity',json.dumps(value),expected_schema=self.schema)
        invalid=[{'conversation_id':''},{'duration_seconds':'0.2'},{'duration_seconds':float('inf')},
                 {'num_turns':0},{'usage':[]},{'usage':{'input_tokens':0}},
                 {'response':''},{'error':'failed'}, {'agent':'codex'},
                 {'json_schema':{'type':'string'}}]
        for change in invalid:
            value=json.loads(valid);value.update(change)
            with self.subTest(change=change), self.assertRaises(adapters.ResponseContractError):
                adapters.parse_response('antigravity',json.dumps(value),expected_schema=self.schema)
        with self.assertRaisesRegex(adapters.ResponseContractError,'antigravity_identity_claim_rejected'):
            adapters.parse_response('antigravity',self.envelope(
                structured_output={'decision':'proposed','changes':[],'nested':{'identity':'codex'}},
                schema=self.schema),expected_schema=self.schema)
        with self.assertRaisesRegex(adapters.ResponseContractError,'response_structured_mismatch'):
            adapters.parse_response('antigravity',self.envelope(
                structured_output=self.payload,response='{}',schema=self.schema),expected_schema=self.schema)

    def test_l3_l4_default_plans_keep_the_v2_dual_council(self):
        self.assertEqual(adapters.enabled_agents(),('claude','codex'))
        policy=adapters.agent_policy()
        self.assertEqual(policy['mode'],'dual-agent')
        self.assertEqual(set(policy['disabled']),{'commandcode','antigravity'})
        with tempfile.TemporaryDirectory() as folder:
            project=Project(make_project(Path(folder),theme=False))
            (project.root/'AGENTS.md').write_text('Synthetic test rules')
            for objective in ('Revisión de arquitectura compartida','Revisión crítica de autenticación'):
                plan=planner.make_plan(project,objective,files=['fixture.txt'],scope='workspace',read_only=True)
                self.assertEqual(plan['classification']['level'],'L3' if 'arquitectura' in objective else 'L4')
                self.assertTrue(plan['council']['enabled'])
                self.assertEqual(plan['council']['required_agents'],['claude','codex'])
                self.assertTrue({task['agent'] for task in plan['tasks']} <= {'claude','codex'})

    def test_explicit_triad_fails_before_workers_when_b1_b2_remain(self):
        with tempfile.TemporaryDirectory() as folder:
            project=Project(make_project(Path(folder),theme=False))
            (project.root/'AGENTS.md').write_text('Synthetic test rules')
            triad=adapters.agent_policy().copy()
            triad.update(mode='multi-agent',members=['claude','codex','antigravity'],disabled=['commandcode'])
            with patch('ipanema.orchestration.adapters.agent_policy',return_value=triad):
                plan=planner.make_plan(project,'Revisión de arquitectura compartida',files=['fixture.txt'],
                                       scope='workspace',read_only=True)
                with patch.object(engine,'central_qa') as qa, patch.object(engine,'run_council') as council_run:
                    with self.assertRaisesRegex(IpanemaError,'B1_cli_authentication.*B2_destination_egress'):
                        engine.execute(project,plan,authorize=True)
                    qa.assert_not_called();council_run.assert_not_called()

    def test_future_triad_preflights_all_three_runtime_binaries(self):
        with tempfile.TemporaryDirectory() as folder:
            project=Project(make_project(Path(folder),theme=False))
            (project.root/'AGENTS.md').write_text('Synthetic test rules')
            triad=adapters.agent_policy().copy()
            triad.update(mode='multi-agent',members=['claude','codex','antigravity'],disabled=['commandcode'])
            with patch('ipanema.orchestration.adapters.agent_policy',return_value=triad):
                plan=planner.make_plan(project,'Revisión de arquitectura compartida',files=['fixture.txt'],
                                       scope='workspace',read_only=True)
                with patch('ipanema.orchestration.adapters.execution_policy',return_value={'enabled':True,'blockers':[]}), \
                     patch('ipanema.orchestration.adapters.runtime_binary',side_effect=lambda agent: None if agent=='antigravity' else '/bin/'+agent), \
                     patch.object(engine,'central_qa') as qa, patch.object(engine,'run_council') as council_run:
                    with self.assertRaisesRegex(IpanemaError,'faltan runtimes requeridos: antigravity'):
                        engine.execute(project,plan,authorize=True)
                    qa.assert_not_called();council_run.assert_not_called()

    def test_effort_flag_matches_confirmed_cli_enum(self):
        with patch('ipanema.orchestration.adapters.enabled_agents',return_value=('claude','codex','antigravity')), \
             patch('ipanema.orchestration.adapters.shutil.which',return_value='/synthetic/agy'):
            args = adapters.argv('antigravity', 'synthetic-model', 'xhigh', response_schema=self.schema,prompt='synthetic')
            self.assertEqual(args[args.index('--effort') + 1], 'xhigh')
            with self.assertRaisesRegex(IpanemaError, '[Ee]sfuerzo'):
                adapters.argv('antigravity', 'synthetic-model', 'turbo', response_schema=self.schema,prompt='synthetic')

    def test_claude_and_codex_parser_contracts_are_unchanged(self):
        raw = json.dumps({'decision': 'approve', 'changes': []})
        self.assertEqual(adapters.parse_response('claude', raw), json.loads(raw))
        self.assertEqual(adapters.parse_response('codex', raw), json.loads(raw))


if __name__ == '__main__':
    unittest.main()
