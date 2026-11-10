"""Bounded protocol validation; fixtures, not real provider inferences."""
import copy,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from tests.support import make_project
from ipanema.core import Project,IpanemaError
from ipanema.orchestration import council,adapters,engine,recovery,isolation

class Protocol(unittest.TestCase):
    def test_native_schemas_match_examples_and_enforce_every_field(self):
        for role in ('council_proposal','council_objection'):
            good=council.contract(role)['example'];schema=council.response_schema(role)
            self.assertEqual(adapters.validate_schema(good,schema),good)
            for field in good:
                bad=copy.deepcopy(good);bad.pop(field)
                with self.assertRaises(adapters.ResponseContractError) as cm:adapters.validate_schema(bad,schema)
                self.assertEqual(cm.exception.diagnostic['category'],'missing_field')
                self.assertEqual(cm.exception.diagnostic['path'],'$.'+field)

    def test_normalization_preserves_already_valid_evidence(self):
        response=copy.deepcopy(council.contract('council_proposal')['example'])
        response['evidence']=['source:fixture.txt']
        normalized=council.validate_proposal(response,[])
        self.assertEqual(normalized['evidence'],response['evidence'])
        adapters.validate_schema(normalized,council.response_schema('council_proposal'))

    def test_progress_filter_preserves_tool_and_error_signals(self):
        progress=json.dumps({'type':'event','event':{'type':'message_update','private':'not logged'}}).encode()
        self.assertEqual(isolation._commandcode_frame(progress),b'')
        for kind in ('tool_running','error','rate_limit'):
            frame=json.dumps({'type':'event','event':{'type':kind}}).encode()
            self.assertEqual(isolation._commandcode_frame(frame),frame+b'\n')
        final=json.dumps({'type':'result','subtype':'success','finalText':'{}'}).encode()
        self.assertEqual(isolation._commandcode_frame(final),final+b'\n')

    def test_schema_errors_show_path_but_never_rejected_value(self):
        good=copy.deepcopy(council.contract('council_proposal')['example'])
        good['analysis']['confidence']='private value must not be logged'
        with self.assertRaises(adapters.ResponseContractError) as cm:adapters.validate_schema(good,council.response_schema('council_proposal'))
        self.assertEqual(cm.exception.diagnostic['path'],'$.analysis.confidence')
        self.assertNotIn('private',str(cm.exception))

    def test_schema_strict_enum_extra_fields_and_lengths(self):
        for mode in ('extra','enum','length'):
            good=copy.deepcopy(council.contract('council_proposal')['example'])
            if mode=='extra':good['private arbitrary key']='secret'
            elif mode=='enum':good['decision']='success'
            else:good['summary']='x'*1001
            with self.assertRaises(adapters.ResponseContractError):adapters.validate_schema(good,council.response_schema('council_proposal'))

    @patch("ipanema.orchestration.adapters.require_agent")
    def test_cli_uses_real_native_schema_flags(self, historical_argv_only):
        schema=council.response_schema('council_proposal')
        with patch.object(adapters.shutil,'which',return_value='/usr/bin/fixture'):
            codex=adapters.argv('codex','fixture',response_schema=schema)
            self.assertIn('--output-schema',codex)
            claude=adapters.argv('claude','fixture',response_schema=schema)
            self.assertIn('--json-schema',claude);self.assertIn('stream-json',claude)
            command=adapters.argv('commandcode','fixture',response_schema=schema)
            self.assertEqual(command[command.index('--output-format')+1],'json')
            self.assertNotIn('--json-schema',command)

    def test_native_structured_frame_and_tool_violation_after_result(self):
        good=council.contract('council_proposal')['example']
        frame={'type':'result','structured_output':good}
        self.assertEqual(adapters.parse_response('claude',json.dumps(frame),strict=True),good)
        bad={'type':'item.completed','item':{'type':'command_execution','command':'private'}}
        with self.assertRaises(adapters.ResponseContractError) as cm:adapters.parse_response('codex',json.dumps(frame)+'\n'+json.dumps(bad),strict=True)
        self.assertEqual(cm.exception.diagnostic['category'],'unexpected_tool_execution')

    def test_syntax_not_ambiguous_repair_or_unproven_truncation(self):
        for text in ('{"decision":','```json\n{"decision":"approve","changes":[]}\n```','prefix {"decision":"approve","changes":[]}'):
            frame={'type':'result','subtype':'success','result':text}
            with self.assertRaises(adapters.ResponseContractError) as cm:adapters.parse_response('commandcode',json.dumps(frame),strict=True)
            self.assertEqual(cm.exception.diagnostic['category'],'json_syntax')
        with self.assertRaises(adapters.ResponseContractError) as cm:adapters.parse_response('claude',json.dumps({'finish_reason':'length'}),strict=True)
        self.assertEqual(cm.exception.diagnostic['category'],'output_truncation')

    def test_duplicate_fields_non_objects_and_max_turns_rejected_precisely(self):
        for text,category in [('{"decision":"approve","decision":"blocked","changes":[]}','json_duplicate_key'),
                              ('[]','schema_type'),('{"value":NaN}','json_syntax')]:
            with self.assertRaises(adapters.ResponseContractError) as cm:
                adapters.parse_response('commandcode',json.dumps({'type':'result','subtype':'success','finalText':text}),strict=True)
            self.assertEqual(cm.exception.diagnostic['category'],category)
        with self.assertRaises(adapters.ResponseContractError) as cm:
            adapters.parse_response('commandcode',json.dumps({'type':'result','subtype':'max_turns'}),strict=True)
        self.assertEqual(cm.exception.diagnostic['category'],'incomplete_response')

    def test_context_is_selective_and_shared_without_duplicated_discovery(self):
        with tempfile.TemporaryDirectory() as temp:
            root=make_project(Path(temp),theme=False);(root/'AGENTS.md').write_text('Local read-only fixture rules')
            (root/'sample.txt').write_text('one\ntwo\nthree\n')
            project=Project(root);task=council.participant_task('claude',0,['sample.txt'],'balanced','Inspect fixture')
            plan={'scope':'workspace','skills':[],'knowledge':{'huge_irrelevant_discovery':'x'*100000},'source_windows':{'sample.txt':[[2,2]]}}
            prompt=engine.prompt_for(project,plan,task,root,[]);packet=json.loads(prompt)
            self.assertLess(len(prompt),15000);self.assertNotIn('huge_irrelevant_discovery',prompt)
            self.assertNotIn('peer_proposals',packet);self.assertNotIn('task',packet)
            self.assertEqual(packet['files']['sample.txt']['excerpts'][0]['content'],'two')
            self.assertFalse(packet['files']['sample.txt']['full_content_in_prompt'])

    def test_limits_vary_without_premium_escalation(self):
        fast=recovery.execution_limits({'agent':'claude','tier':'fast'},{})
        strong=recovery.execution_limits({'agent':'codex','tier':'strong'},{})
        self.assertLess(fast['timeout'],strong['timeout'])
        self.assertNotEqual(fast['first_response_timeout'],strong['first_response_timeout'])
        with self.assertRaises(IpanemaError):recovery.execution_limits({'agent':'codex','tier':'fast'},{'time_limits':{'codex':{'total':-1}}})

@unittest.skipUnless(isolation.probe()['available'],'Actual sandbox unavailable; not simulated')
class PhaseTiming(unittest.TestCase):
    @patch("ipanema.orchestration.adapters.require_agent")
    def test_commandcode_progress_does_not_consume_final_response_budget(self, historical_python_fixture_only):
        with tempfile.TemporaryDirectory() as temp:
            script='import json\nfor i in range(2500): print(json.dumps({"type":"event","event":{"type":"message_update","text":"x"*1000}}))\nprint(json.dumps({"type":"result","subtype":"success","finalText":"{\\"decision\\":\\"approve\\",\\"changes\\":[]}"}))'
            raw=isolation.run_isolated(['/usr/bin/python3','-c',script],'',Path(temp),provider='commandcode',network=False,timeout=10)
            self.assertFalse(raw['output_limited']);self.assertEqual(raw['exit_code'],0)
            self.assertGreater(raw['output_accounting']['transport_bytes'],2000000)
            self.assertLess(raw['output_accounting']['retained_bytes'],1000)
            self.assertEqual(adapters.parse_response('commandcode',raw['stdout'],strict=True)['decision'],'approve')

    def test_first_response_and_inactivity_are_distinct(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            first=isolation.run_isolated(['/usr/bin/python3','-c','import time;time.sleep(2)'],'',root,provider='qa',network=False,timeout=3,first_response_timeout=.25,idle_timeout=.1)
            self.assertEqual(first['timing']['timeout_phase'],'first_response');self.assertTrue(first['process_reaped'])
            self.assertFalse(first['idle_timed_out'])
            progress=isolation.run_isolated(['/usr/bin/python3','-c','import time;print("ready",flush=True);time.sleep(2)'],'',root,provider='qa',network=False,timeout=3,first_response_timeout=1,idle_timeout=.2)
            self.assertTrue(progress['idle_timed_out']);self.assertIsNotNone(progress['timing']['first_stdout_s'])
            self.assertTrue(progress['process_reaped'])
