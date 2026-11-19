"""Focused offline tests for the isolated Antigravity council adapter."""
import copy
import json
import tempfile
import threading
import unittest
import subprocess
from pathlib import Path
from unittest.mock import patch

from tests.support import make_project
from tests.unit.test_council_policy import context, proposal, receipts
from ipanema.core import IpanemaError, Project
from ipanema.orchestration import adapters, council, engine, planner, isolation, recovery
from ipanema.orchestration.council_runtime import deliberate


class AntigravityAdapterTests(unittest.TestCase):
    agents = ('claude', 'codex')
    triad = ('claude', 'codex', 'antigravity')

    def triad_policy(self):
        value=copy.deepcopy(adapters.agent_policy())
        value.update(mode='multi-agent',members=list(self.triad),disabled=['commandcode'])
        return value

    def test_registry_and_profiles_are_separate_from_runtime_readiness(self):
        self.assertEqual(adapters.enabled_agents(), self.agents)
        selected = adapters.model_for(Path(__file__).resolve().parents[2], 'antigravity', 'balanced')
        self.assertIsNone(selected['model'])
        self.assertEqual(selected['selection_status'], 'unverified')
        self.assertFalse(adapters.execution_policy('antigravity')['enabled'])
        with self.assertRaisesRegex(IpanemaError, 'Agente deshabilitado por política: antigravity'):
            adapters.require_execution_agent('antigravity')

    def test_local_registry_cannot_clear_code_level_security_blockers(self):
        base = json.loads((Path(__file__).resolve().parents[2] / 'tools/ipanema/orchestration/models.json').read_text())
        base['provider_execution']['antigravity']={'enabled':True,'blockers':[]}
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);path=root/'tools/ipanema/orchestration/models.json';path.parent.mkdir(parents=True)
            path.write_text(json.dumps(base))
            status=adapters.execution_policy('antigravity',root)
            self.assertFalse(status['enabled'])
            self.assertIn('B1_cli_authentication_not_separated_from_tool_capable_worker',status['blockers'])
            self.assertIn('B2_destination_egress_not_enforced',status['blockers'])

    @patch('ipanema.orchestration.adapters.enabled_agents',return_value=('claude','codex','antigravity'))
    @patch('ipanema.orchestration.adapters.shutil.which',return_value='/synthetic/agy')
    def test_cli_argv_uses_only_help_documented_interface_and_closed_json(self, _binary, _agents):
        schema = council.response_schema('council_proposal')
        args = adapters.argv('antigravity', 'synthetic-model', response_schema=schema,
                             prompt='synthetic review only')
        self.assertEqual(Path(args[0]).name, 'agy')
        self.assertIn('--model', args); self.assertIn('--output-format', args)
        self.assertIn('--json-schema', args); self.assertIn('--mode', args)
        self.assertIn('--sandbox', args); self.assertIn('--disable-slash-commands', args)
        self.assertIn('-p', args); self.assertEqual(args[-1], 'synthetic review only')
        self.assertNotIn('--dangerously-skip-permissions', args)
        self.assertNotIn('--remote-agent', args)
        with self.assertRaisesRegex(IpanemaError, '[Mm]odelo.*no verificado'):
            adapters.argv('antigravity', None, prompt='synthetic')
        effort_args=adapters.argv('antigravity', 'synthetic-model', 'high', response_schema=schema,prompt='synthetic')
        self.assertIn('--effort',effort_args);self.assertEqual(effort_args[effort_args.index('--effort')+1],'high')
        with self.assertRaisesRegex(IpanemaError, '[Ee]sfuerzo'):
            adapters.argv('antigravity', 'synthetic-model', 'turbo', response_schema=schema,prompt='synthetic')

    def test_output_parser_accepts_only_direct_structured_json_and_rejects_unknown_envelopes(self):
        fixture = {'decision': 'proposed', 'changes': []}
        schema={'type':'object','required':['decision','changes'],
                'properties':{'decision':{'type':'string'},'changes':{'type':'array'}},
                'additionalProperties':False}
        envelope={'conversation_id':'fixture','status':'SUCCESS','response':json.dumps(fixture),
                  'duration_seconds':0.1,'num_turns':1,
                  'usage':{'input_tokens':1,'output_tokens':1,'thinking_tokens':0,'cache_read_tokens':0,'total_tokens':2},
                  'structured_output':fixture,'json_schema':schema}
        self.assertEqual(adapters.parse_response('antigravity', json.dumps(envelope),
                         expected_schema=schema), fixture)
        failed={'conversation_id':'fixture','status':'ERROR','response':'failure',
                'duration_seconds':0.1,'num_turns':1,
                'usage':{'input_tokens':0,'output_tokens':0,'thinking_tokens':0,'cache_read_tokens':0,'total_tokens':0}}
        with self.assertRaisesRegex(adapters.ResponseContractError, 'antigravity_execution_status'):
            adapters.parse_response('antigravity', json.dumps(failed),expected_schema=schema)
        with self.assertRaisesRegex(adapters.ResponseContractError, 'antigravity_json_invalid'):
            adapters.parse_response('antigravity', '{broken')

    def test_incomplete_json_and_synthetic_auth_failure_are_classified_without_provider(self):
        incomplete={'decision':'proposed'}
        schema=council.response_schema('council_proposal')
        with self.assertRaises(adapters.ResponseContractError):
            adapters.parse_response('antigravity',json.dumps({'conversation_id':'fixture','status':'SUCCESS',
                'response':json.dumps(incomplete),'duration_seconds':0.1,'num_turns':1,
                'usage':{'input_tokens':1,'output_tokens':1,'thinking_tokens':0,'cache_read_tokens':0,'total_tokens':2},
                'structured_output':incomplete,'json_schema':schema}),expected_schema=schema)
        self.assertEqual(recovery.classify_failure({'stderr':'401 unauthorized','stdout':''}),'authentication')

    def test_runtime_has_no_credential_mount_or_env_and_real_worker_is_blocked(self):
        runtime = engine.runtime_defaults('antigravity')
        self.assertEqual(runtime['auth_files'], {})
        self.assertEqual(runtime['auth_env'], [])
        self.assertEqual(isolation._ENV_PREFIX['antigravity'], ())
        with patch('subprocess.Popen') as spawn:
            with self.assertRaisesRegex(IpanemaError, 'B1_.*B2_'):
                isolation.run_isolated(['/bin/true'], '', Path(__file__).resolve().parents[2],
                                       provider='antigravity')
            spawn.assert_not_called()

    @unittest.skipUnless(isolation.probe()['available'],'Local bubblewrap unavailable; cancellation not simulated')
    def test_supervisor_cancels_synthetic_process_and_reaps_it(self):
        with tempfile.TemporaryDirectory() as folder:
            cancel=threading.Event()
            timer=threading.Timer(0.15,cancel.set);timer.start()
            try:
                result=isolation.run_isolated(['/usr/bin/python3','-c','import time;time.sleep(5)'],'',Path(folder),
                                              provider='qa',network=False,timeout=10,cancel_event=cancel)
            finally:timer.cancel()
            self.assertTrue(result['cancelled'])
            self.assertTrue(result['process_reaped'])
            self.assertTrue(result['process_started'])

    def test_access_policy_does_not_grant_antigravity_tools(self):
        with tempfile.TemporaryDirectory() as folder:
            project = Project(make_project(Path(folder), theme=False))
            from ipanema.access.policy import Policy
            with self.assertRaisesRegex(IpanemaError, 'Agente o identificador'):
                Policy(project).issue('antigravity', 'synthetic', ['devtools.read'], allow_network=True)

    def test_three_agent_policy_and_cross_review_route_without_self_review(self):
        with tempfile.TemporaryDirectory() as folder:
            project = Project(make_project(Path(folder), theme=False))
            (project.root / 'AGENTS.md').write_text('Synthetic fixture only')
            with patch('ipanema.orchestration.adapters.agent_policy',return_value=self.triad_policy()):
                plan = planner.make_plan(project, 'Revisión crítica de seguridad de credenciales',
                                         files=['fixture.txt'], scope='workspace', implementation_agent='codex')
                self.assertEqual(plan['council']['required_agents'], list(self.triad))
            reviewers = [t['agent'] for t in plan['tasks'] if t['role'] == 'review']
            implementation = next(t['agent'] for t in plan['tasks'] if t['role'] == 'implementation')
            self.assertEqual(implementation, 'codex')
            self.assertEqual(len(set(reviewers)), 2)
            self.assertNotIn(implementation, reviewers)
            self.assertEqual(set(reviewers), {'claude', 'antigravity'})
            for agent in self.triad:
                task = council.participant_task(agent, 0, ['fixture.txt'], 'critical', 'synthetic')
                self.assertEqual(task['allowed_files'], [])
                self.assertNotIn('peer_proposals', task['council_context'])
                if agent=='antigravity':self.assertIn('rendimiento', task['council_context']['specialty'])

    def test_evidence_controls_selection_not_majority_preference(self):
        ctx = context()
        proposals = [proposal('claude', alternative='native'),
                     proposal('codex', alternative='native'),
                     proposal('antigravity', alternative='other')]
        proof = receipts(ctx, alternative='native') + receipts(ctx, alternative='other')
        next(r for r in proof if r['subject'] == 'native' and r['constraint'] == 'security')['passed'] = False
        adr = council.aggregate(proposals, [], evidence=proof, required_agents=list(self.triad),
                                context=ctx, project='fixture', objective='synthetic')
        self.assertEqual(adr['selected_alternative'], 'other')
        self.assertFalse(adr['production_authorized'])

    def test_three_agent_execution_stops_before_qa_or_any_worker(self):
        with tempfile.TemporaryDirectory() as folder:
            project = Project(make_project(Path(folder), theme=False))
            (project.root / 'AGENTS.md').write_text('Synthetic fixture only')
            (project.root / 'fixture.txt').write_text('synthetic')
            with patch('ipanema.orchestration.adapters.agent_policy',return_value=self.triad_policy()):
                plan = planner.make_plan(project, 'Revisión crítica de seguridad de credenciales',
                                         files=['fixture.txt'], scope='workspace', implementation_agent='codex')
                with patch.object(engine, 'central_qa') as qa, patch.object(engine, 'run_council') as run_council:
                    with self.assertRaisesRegex(IpanemaError, 'antes de QA/proveedores'):
                        engine.execute(project, plan, authorize=True)
                    qa.assert_not_called();run_council.assert_not_called()

    def test_readonly_and_dual_v2_policy_contract_remain_representable(self):
        base = json.loads((Path(__file__).resolve().parents[2] / 'tools/ipanema/orchestration/models.json').read_text())
        base['council'].update(mode='dual-agent', members=['claude', 'codex'], disabled=['commandcode', 'antigravity'])
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); policy_file = root / 'tools/ipanema/orchestration/models.json'
            policy_file.parent.mkdir(parents=True); policy_file.write_text(json.dumps(base))
            self.assertEqual(adapters.enabled_agents(root), ('claude', 'codex'))
            self.assertEqual(adapters.agent_policy(root)['mode'], 'dual-agent')


    @patch('ipanema.orchestration.adapters.agent_policy')
    def test_mocked_three_agent_council_runs_independent_proposals_debate_and_defense(self, agent_policy):
        catalog=json.loads((Path(__file__).resolve().parents[2]/'tools/ipanema/orchestration/models.json').read_text())
        triad_policy=copy.deepcopy(catalog['council'])
        triad_policy.update(mode='multi-agent',members=list(self.triad),disabled=['commandcode'])
        agent_policy.return_value=triad_policy
        with tempfile.TemporaryDirectory() as folder:
            root=make_project(Path(folder),theme=False)
            (root/'AGENTS.md').write_text('Synthetic fixture only')
            (root/'fixture.txt').write_text('offline source evidence')
            project=Project(root)
            for cmd in (['init','-q'],['add','.'],['-c','user.name=Fixture','-c','user.email=fixture@invalid','commit','-qm','fixture']):
                subprocess.run(['git','-C',str(root),*cmd],check=True,capture_output=True)
            plan=planner.make_plan(project,'Revisión de arquitectura compartida',files=['fixture.txt'],scope='workspace',read_only=True)
            calls=[]
            def fake_worker(project,plan,task,tree,history,settings):
                calls.append((task['role'],task['agent'],list(history)))
                response=copy.deepcopy(council.contract(task['role'])['example'])
                response['summary']='Synthetic controller fixture only'
                if task['role']=='council_proposal':
                    response['analysis']['files']=['fixture.txt']
                    response['analysis']['alternatives'][0]['files']=['fixture.txt']
                    response['analysis']['alternatives'][0]['constraints']={k:{'status':'unknown','evidence_refs':[]} for k in council.CRITERIA}
                elif task['role']=='council_objection':
                    response['preferred_alternative']='native'
                    response['objections']=[]
                    peer=next(a for a in self.triad if a!=task['agent'])
                    response['questions']=[{'id':'Q-'+task['agent'],'to_agent':peer,'alternative_id':'native',
                                            'question':'What evidence supports this exact claim?','evidence_refs':[]}]
                else:
                    response['preferred_alternative']='native'
                    response['objections']=[]
                    answers=[]
                    for env in task['council_context']['cross_examination']:
                        for question in env.get('response',{}).get('questions',[]):
                            if question['to_agent']==task['agent']:
                                answers.append({'question_id':question['id'],'from_agent':env['requested_agent'],
                                                'answer':'Synthetic fixture answer; no real provider evidence.',
                                                'evidence_refs':[],'disposition':'defend'})
                    response['answers']=answers
                return response
            # This test substitutes only the runtime readiness predicate and worker with fixtures;
            # it does not spawn, authenticate, contact, or claim a real provider.
            with patch('ipanema.orchestration.adapters.execution_policy',return_value={'enabled':True,'blockers':[]}), \
                 patch.object(engine,'worker',side_effect=fake_worker):
                run=project.new_run('antigravity-triad-fixture')
                adr=engine.run_council(project,plan,root,{},run,{'executed':True,'passed':True,'kind':'synthetic-offline'},lambda:None)
            proposals=[row for row in calls if row[0]=='council_proposal']
            objections=[row for row in calls if row[0]=='council_objection']
            defenses=[row for row in calls if row[0]=='council_defense']
            self.assertEqual({row[1] for row in proposals},set(self.triad))
            self.assertEqual({row[1] for row in objections},set(self.triad))
            self.assertEqual({row[1] for row in defenses},set(self.triad))
            self.assertEqual(len(proposals),3);self.assertEqual(len(objections),3);self.assertEqual(len(defenses),3)
            self.assertTrue(all(row[2]==[] for row in proposals))
            self.assertEqual(adr['phases_executed'],['independent_proposals','cross_examination','defense'])
            self.assertFalse(adr['production_authorized'])
            self.assertTrue(all(row['effective_agent']==row['requested_agent'] for row in json.loads((run/'council/proposals.json').read_text())))



if __name__ == '__main__':
    unittest.main()
