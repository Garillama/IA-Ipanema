"""Recuperación con fixtures sin cuentas; watchdog usa proceso OS real aislado."""
import json
from pathlib import Path
import tempfile
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor
import unittest
from unittest.mock import patch

from tests.support import ROOT
from ipanema.core import IpanemaError
from ipanema.orchestration.recovery import Supervisor, WorkerFailure, classify_failure, candidates, health_check, policy
from ipanema.orchestration.isolation import probe, run_isolated


class Classification(unittest.TestCase):
    def test_failure_categories_never_export_private_message(self):
        cases={'rate_limit':'429 too many requests', 'permission_denied':'HTTP403 forbidden',
               'authentication':'authentication_error invalid token synthetic-secret',
               'model_unavailable':'model not available', 'cli_incompatible':'unknown option --fixture',
               'transient_network':'ECONNRESET', 'unknown_provider_error':'unrecognized private detail'}
        for expected, text in cases.items():
            with self.subTest(expected=expected):
                value=classify_failure({'exit_code':1,'stderr':text})
                self.assertEqual(value,expected)
                self.assertNotIn('synthetic-secret',value)
        self.assertEqual(classify_failure({'timed_out':True}),'timeout')
        self.assertEqual(classify_failure({'idle_timed_out':True}),'inactivity')
        self.assertEqual(classify_failure({'output_limited':True}),'output_limit')

    def test_denial_takes_precedence_over_all_recoverable_limits(self):
        for status,category in [('403','permission_denied'),('429','rate_limit')]:
            for flag in ('timed_out','idle_timed_out','output_limited','cancelled'):
                with self.subTest(status=status,flag=flag):
                    self.assertEqual(classify_failure({'stderr':'HTTP '+status,flag:True}),category)

    def test_config_and_local_health_are_not_auth_proof(self):
        for value in (-1,3,True):
            with self.assertRaises(IpanemaError):policy({'recovery':{'max_retries':value}})
        with patch('ipanema.orchestration.recovery.shutil.which',return_value=None):
            self.assertFalse(health_check('claude')['installed'])
        self.assertEqual(policy({})['max_retries'],1)


class Supervision(unittest.TestCase):
    def setUp(self):
        from tests.support import historical_trio_policy
        historical_trio_policy(self)
        self.binary=patch('ipanema.orchestration.recovery.shutil.which',side_effect=lambda name:'/bin/'+name)
        self.binary.start();self.addCleanup(self.binary.stop)

    def task(self):return {'id':'architecture','agent':'claude','role':'architecture','tier':'strong','read_files':['same.tpl'],'allowed_files':[]}

    def test_auth_fallback_preserves_context_scope_and_checkpoint(self):
        task=self.task();snapshot=json.dumps(task['read_files']);calls=[];checkpoints=[]
        def invoke():
            calls.append(task['agent'])
            if task['agent']=='claude':raise WorkerFailure('authentication')
            return {'decision':'proposed','changes':[]}
        value=Supervisor({}).run({'tasks':[task]},task,invoke,lambda:checkpoints.append(task['agent']))
        self.assertEqual(calls,['claude','codex']);self.assertEqual(value['decision'],'proposed')
        self.assertEqual(task['assigned_agent'],'claude');self.assertEqual(task['agent'],'codex')
        self.assertEqual(snapshot,json.dumps(task['read_files']));self.assertEqual(task['allowed_files'],[])
        self.assertGreaterEqual(len(checkpoints),4)
        self.assertTrue(task['substitutions'][0]['previous_process_reaped'])

    def test_retry_only_transient_bounded_then_circuit_is_shared(self):
        task=self.task();s=Supervisor({});calls=[]
        def invoke():
            calls.append(task['agent'])
            if task['agent']=='claude':raise WorkerFailure('transient_network')
            return {'decision':'proposed','changes':[]}
        with patch('ipanema.orchestration.recovery.time.sleep'):
            s.run({},task,invoke)
        self.assertEqual(calls,['claude','claude','codex'])
        second=self.task();s.run({},second,lambda:{'decision':'proposed','changes':[]})
        self.assertEqual(second['agent'],'codex')
        self.assertEqual(second['recovery_attempts'][0]['category'],'circuit_open')

    def test_rate_limits_and_unreaped_process_never_reassign(self):
        for category,reaped in [('rate_limit',True),('permission_denied',True),('timeout',False)]:
            with self.subTest(category=category):
                task=self.task();calls=[]
                def invoke():
                    calls.append(task['agent']);raise WorkerFailure(category,reaped=reaped)
                with self.assertRaises(IpanemaError):Supervisor({}).run({},task,invoke)
                self.assertEqual(calls,['claude']);self.assertEqual(task['agent'],'claude')

    def test_l3_and_l4_independent_reviews_survive_fallback(self):
        impl={'id':'implementation','role':'implementation','agent':'codex'}
        r1={'id':'review-a','role':'review','agent':'claude','dependencies':['implementation']}
        r2={'id':'review-b','role':'review','agent':'commandcode','dependencies':['implementation']}
        p={'tasks':[impl,r1,r2],'classification':{'level':'L4'},'read_only':False}
        self.assertEqual(candidates(p,r1),[])
        self.assertEqual(candidates(p,impl),[])
        p['tasks']=[impl,r2];p['classification']['level']='L3'
        self.assertEqual(candidates(p,impl),['claude'])
        self.assertEqual(candidates(p,r2),['claude'])
        with self.assertRaises(IpanemaError):
            Supervisor({}).run({'tasks':[impl,r1,r2]},r1,lambda:(_ for _ in ()).throw(WorkerFailure('authentication')))

    def test_actual_reassigned_implementer_is_excluded_from_review(self):
        impl={'id':'implementation','role':'implementation','agent':'claude','assigned_agent':'codex'}
        review={'id':'review','role':'review','agent':'commandcode','dependencies':['implementation']}
        self.assertEqual(candidates({'tasks':[impl,review]},review),['codex'])

    def test_circuit_opened_by_another_worker_during_backoff(self):
        task=self.task();s=Supervisor({});calls=[]
        def invoke():
            calls.append(task['agent'])
            if task['agent']=='claude':raise WorkerFailure('transient_network')
            return {'decision':'proposed','changes':[]}
        with patch('ipanema.orchestration.recovery.time.sleep',side_effect=lambda _:s.failed('claude','authentication')):
            s.run({},task,invoke)
        self.assertEqual(calls,['claude','codex'])

    def test_shared_denial_cancels_other_worker_and_prevents_new_invocation(self):
        s=Supervisor({});active=threading.Event();stopped=threading.Event();calls=[]
        a=self.task();b={**self.task(),'id':'second','agent':'commandcode'}
        def wait():
            calls.append('waiting');active.set()
            self.assertTrue(s.cancel_event.wait(2));stopped.set()
            raise WorkerFailure('run_cancelled')
        def deny():
            self.assertTrue(active.wait(2));calls.append('denial');raise WorkerFailure('permission_denied')
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures=[pool.submit(s.run,{},a,wait),pool.submit(s.run,{},b,deny)]
            for f in futures:
                with self.assertRaises(IpanemaError):f.result(timeout=3)
        self.assertTrue(stopped.is_set());self.assertEqual(calls,['waiting','denial'])
        with self.assertRaises(IpanemaError):s.run({},self.task(),lambda:calls.append('unexpected'))
        self.assertNotIn('unexpected',calls)

    def test_success_arriving_after_shared_cancellation_is_not_accepted(self):
        s=Supervisor({});task=self.task()
        def invoke():
            s.cancel_event.set();return {'decision':'proposed','changes':[]}
        with self.assertRaises(IpanemaError):s.run({},task,invoke)
        self.assertFalse(any(a['status']=='completed' for a in task['recovery_attempts']))

    def test_response_contract_error_does_not_retry_or_switch(self):
        task=self.task();calls=[]
        def invoke():
            calls.append(task['agent']);raise IpanemaError('Tools/contract violation')
        with self.assertRaises(IpanemaError):Supervisor({}).run({},task,invoke)
        self.assertEqual(calls,['claude'])


class EffectiveRisk(unittest.TestCase):
    def test_recomputed_l4_is_written_to_plan_before_review_gate(self):
        from types import SimpleNamespace
        from ipanema.orchestration.engine import execute
        plan={'kind':'orchestration-plan','project':'synthetic','objective':'fixture','scope':'workspace',
              'allowed_files':['fixture.txt'],'read_only':False,'skills':[],
              'classification':{'level':'L1','production_request':False},
              'tasks':[{'id':'implementation','role':'implementation','agent':'codex','dependencies':[]}]}
        risk={'level':'L4','production_request':False,'risk':'critical','reasons':['fixture'],'independent_review_required':True}
        with patch('ipanema.orchestration.engine.classify',return_value=risk):
            with self.assertRaisesRegex(IpanemaError,'revisiones independientes'):
                execute(SimpleNamespace(id='synthetic'),plan,authorize=True)
        self.assertEqual(plan['classification']['level'],'L4')
        self.assertEqual(plan['declared_classification']['level'],'L1')


class FrozenContext(unittest.TestCase):
    def test_fallback_receives_identical_frozen_prompt_despite_source_mutation(self):
        from types import SimpleNamespace
        from ipanema.orchestration.engine import worker
        prompts=[]
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'AGENTS.md').write_text('Initial synthetic rules')
            tree=root/'fixture';tree.mkdir();(tree/'same.tpl').write_text('initial synthetic source')
            task={'id':'architecture','agent':'claude','role':'architecture','tier':'strong','read_files':['same.tpl'],'allowed_files':[]}
            project=SimpleNamespace(root=root,id='synthetic')
            def raw(args,prompt,*rest,**kwargs):
                prompts.append(prompt)
                (root/'AGENTS.md').write_text('modified rules after failure')
                (tree/'same.tpl').write_text('modified source after failure')
                common={'process_reaped':True,'context_complete':True}
                if len(prompts)==1:return {**common,'exit_code':1,'stderr':'authentication_error','stdout':''}
                return {**common,'exit_code':0,'stderr':'','stdout':json.dumps({'decision':'proposed','changes':[]})}
            with patch('ipanema.orchestration.recovery.shutil.which',side_effect=lambda x:'/bin/'+x), \
                 patch('ipanema.orchestration.engine.argv',return_value=['/bin/true']), \
                 patch('ipanema.orchestration.engine.runtime_defaults',return_value={}), \
                 patch('ipanema.orchestration.engine.model_for',return_value={'model':'fixture'}), \
                 patch('ipanema.orchestration.isolation.run_isolated',side_effect=raw):
                result=worker(project,{'tasks':[task],'skills':[]},task,tree,[],{})
            self.assertEqual(result['decision'],'proposed');self.assertEqual(len(prompts),2)
            self.assertEqual(prompts[0],prompts[1]);self.assertIn('initial synthetic source',prompts[1])
            self.assertNotIn('modified rules after failure',prompts[1])
            self.assertTrue(task['substitutions'][0]['context_preserved'])
            self.assertEqual(task['substitutions'][0]['current_prompt_sha256'],task['frozen_context']['sha256'])


class WorkspaceQA(unittest.TestCase):
    @unittest.skipUnless(probe()['available'],'Bubblewrap no disponible; no simular QA de workspace')
    def test_workspace_qa_gets_synthetic_registry_and_knowledge(self):
        from types import SimpleNamespace
        from tests.support import make_project, put
        from ipanema.orchestration.engine import central_qa
        with tempfile.TemporaryDirectory() as folder:
            tree=make_project(Path(folder)/'source',identifier='private-fixture',theme=False)
            put(tree/'projects/private-fixture.local.json',{'synthetic_private_marker':'do-not-copy'})
            shutil.copytree(ROOT/'tools/ipanema',tree/'tools/ipanema',ignore=shutil.ignore_patterns('__pycache__'))
            knowledge=tree/'ipanema-discovery/13-evidence/measurements/source-baseline'
            for name,value in {'source-summary.json':{'verified_at':'2026-11-09'},'components.json':[],
                               'dependency-graph.json':[],'settings.json':[],'source-inventory.json':[]}.items():
                put(knowledge/name,value)
            put(tree/'tests/unit/test_fixture_knowledge.py',"""import unittest,sys,json
from pathlib import Path
root=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root/'tools'))
from ipanema.core import Project
from ipanema.knowledge import Knowledge
class FixtureKnowledge(unittest.TestCase):
 def test_project_and_knowledge(self):
  p=Project(root,'ipanema')
  self.assertEqual(p.data['environment'],'offline-test')
  self.assertIsNone(p.theme_root)
  self.assertEqual(Knowledge(p).components,[])
  self.assertEqual(sorted(x.name for x in (root/'projects').iterdir()),['ipanema.json','registry.json'])
""")
            result=central_qa(SimpleNamespace(root=ROOT),{'scope':'workspace'},tree,{})
            self.assertTrue(result['passed'],result.get('summary'))
            self.assertEqual(result['kind'],'unit-tests-isolated')
            self.assertEqual(result['project_configuration'],'synthetic_offline_no_theme')
            self.assertIn('Ran 1 test',result['summary'])
            self.assertEqual(json.loads((tree/'projects/registry.json').read_text())['default'],'private-fixture')


class ActualWatchdog(unittest.TestCase):
    @unittest.skipUnless(probe()['available'],'Bubblewrap no disponible; no simular prueba real')
    def test_silent_process_killed_and_reaped_before_reassignment(self):
        with tempfile.TemporaryDirectory() as folder:
            snapshot=Path(folder);(snapshot/'fixture.txt').write_text('public synthetic fixture')
            raw=run_isolated(['/bin/sleep','5'],'',snapshot,provider='qa',network=False,timeout=4,idle_timeout=.2)
            self.assertTrue(raw['idle_timed_out']);self.assertFalse(raw['timed_out'])
            self.assertTrue(raw['process_reaped']);self.assertLess(raw['duration_s'],3)

    @unittest.skipUnless(probe()['available'],'Bubblewrap no disponible; no simular prueba real')
    def test_cancel_event_kills_active_process_and_blocks_pre_cancelled_start(self):
        with tempfile.TemporaryDirectory() as folder:
            event=threading.Event();snapshot=Path(folder)
            timer=threading.Timer(.25,event.set);timer.start()
            try:
                raw=run_isolated(['/bin/sleep','5'],'',snapshot,provider='qa',network=False,timeout=4,cancel_event=event)
            finally:timer.join()
            self.assertTrue(raw['cancelled']);self.assertTrue(raw['process_reaped'])
            self.assertLess(raw['duration_s'],3)
            blocked=run_isolated(['/bin/sleep','5'],'',snapshot,provider='qa',network=False,timeout=4,cancel_event=event)
            self.assertFalse(blocked['process_started']);self.assertTrue(blocked['cancelled'])

    @unittest.skipUnless(probe()['available'],'Bubblewrap no disponible; no simular prueba real')
    def test_context_complete_and_process_exit_are_observed(self):
        with tempfile.TemporaryDirectory() as folder:
            snapshot=Path(folder)
            raw=run_isolated(['/usr/bin/python3','-c','import sys; sys.stdin.read(); print("fixture")'],
                             'payload',snapshot,provider='qa',network=False,timeout=3,idle_timeout=2)
            self.assertEqual(raw['exit_code'],0);self.assertTrue(raw['process_reaped'])
            self.assertTrue(raw['context_complete']);self.assertEqual(raw['stdin_bytes_written'],7)
