"""CLI portable y DAG/Git reales con workers/QA MOCK identificados explícitamente.

No invoca Claude/Codex/CommandCode ni constituye validación real de modelos.
"""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

from tests.support import ROOT, make_project
from ipanema.core import Project, IpanemaError, digest
from ipanema.orchestration import engine, planner


class PortableOrchestrationCLI(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='orchestration portable ')
        self.root=Path(self.tmp.name)/'agent with spaces'
        make_project(self.root,theme=False)
        shutil.copytree(ROOT/'tools',self.root/'tools',ignore=shutil.ignore_patterns('__pycache__'))
        (self.root/'AGENTS.md').write_text('# Fixture instructions\nNo production writes.\n')
        shutil.copytree(ROOT/'.agents',self.root/'.agents')
        self.env={k:v for k,v in os.environ.items() if not k.startswith('IPANEMA_')}

    def tearDown(self):self.tmp.cleanup()

    def cli(self,*args):
        return subprocess.run([sys.executable,str(self.root/'tools/ia.py'),'orchestrate',*map(str,args)],
                              cwd=self.tmp.name,env=self.env,capture_output=True,text=True,timeout=20)

    def test_doctor_reports_capabilities_without_model_inference(self):
        run=self.cli('doctor');self.assertEqual(run.returncode,0,run.stderr)
        report=json.loads(run.stdout)
        self.assertEqual(report['project'],'sample');self.assertFalse(report['production_executor'])
        self.assertTrue(report['no_unsafe_fallback'])
        self.assertTrue(all(not item['inference_tested'] for item in report['runtimes'].values()))

    def test_plan_runs_from_another_directory_without_theme_or_knowledge(self):
        run=self.cli('plan','Corrige una errata','--scope','workspace','--file','copy.txt')
        self.assertEqual(run.returncode,0,run.stderr)
        result=json.loads(run.stdout)
        self.assertFalse(result['execution_performed']);self.assertEqual(result['classification']['level'],'L1')
        self.assertTrue(Path(result['plan']).is_file())
        denied=self.cli('run',result['plan'])
        self.assertEqual(denied.returncode,2);self.assertIn('--execute',denied.stderr)

    def test_smoke_cannot_start_without_execute(self):
        run=self.cli('smoke','--agent','codex')
        self.assertEqual(run.returncode,2);self.assertIn('--execute',run.stderr)


class MockWorkersRealGit(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='orchestration real git ')
        self.root=make_project(Path(self.tmp.name),theme=False)
        (self.root/'AGENTS.md').write_text('Synthetic project; no production.\n')
        for name in ('alpha.txt','beta.txt'):(self.root/name).write_text('before '+name+'\n')
        self.p=Project(self.root)
        self.git('init','-q');self.git('add','.')
        self.git('-c','user.name=Fixture','-c','user.email=fixture@invalid','commit','-qm','Synthetic fixture')
        self.head=self.git('rev-parse','HEAD')

    def tearDown(self):self.tmp.cleanup()

    def git(self,*args):
        run=subprocess.run(['git','-C',str(self.root),*args],capture_output=True,text=True,timeout=20)
        self.assertEqual(run.returncode,0,run.stderr);return run.stdout.strip()

    def plan(self):
        return planner.make_plan(self.p,'Corrige textos',files=['alpha.txt','beta.txt'],scope='workspace')

    @staticmethod
    def mock_qa(*args):
        return {'executed':False,'passed':True,'kind':'mock-central-qa','mock':True,
                'limitations':['Fixture only: no real QA/model approval.']}

    def test_two_disjoint_workers_run_in_parallel_with_real_isolated_worktrees(self):
        plan=self.plan();plan['tasks']=[
            {'id':'alpha','objective':'Synthetic alpha edit','agent':'codex','tier':'fast','role':'implementation','state':'pending',
             'read_files':['alpha.txt'],'allowed_files':['alpha.txt'],'dependencies':[],'tests':['mock-central-qa'],'result':None},
            {'id':'beta','objective':'Synthetic beta edit','agent':'codex','tier':'fast','role':'implementation','state':'pending',
             'read_files':['beta.txt'],'allowed_files':['beta.txt'],'dependencies':[],'tests':['mock-central-qa'],'result':None}]
        plan['tasks'].append({'id':'review','objective':'Independent fixture review','agent':'claude','tier':'fast','role':'review','state':'pending',
             'read_files':['alpha.txt','beta.txt'],'allowed_files':[],'dependencies':['alpha','beta'],'tests':['mock-central-qa'],'result':None})
        barrier=threading.Barrier(2);trees=[];guard=threading.Lock()
        def mock_worker(project,plan,task,tree,history,settings):
            if task['role']=='review':
                task['execution']={'backend':'mock','inference_executed':False}
                return {'decision':'approve','summary':'Independent offline fixture review','changes':[]}
            with guard:trees.append(tree)
            self.assertTrue((tree/'.git').is_file())  # Actual Git worktree pointer.
            barrier.wait(timeout=10)
            name=task['allowed_files'][0]
            task['execution']={'backend':'mock','inference_executed':False}
            return {'decision':'proposed','summary':'Synthetic mock proposal','evidence':['fixture-only'],
                    'changes':[{'path':name,'before_sha256':digest(tree/name),'content':'after '+name+'\n'}]}
        before={name:(self.root/name).read_bytes() for name in plan['allowed_files']}
        with patch('ipanema.orchestration.engine.worker',side_effect=mock_worker),patch('ipanema.orchestration.engine.central_qa',side_effect=self.mock_qa),patch('ipanema.orchestration.isolation.probe',return_value={'available':True}):
            result=engine.execute(self.p,plan,authorize=True)
        self.assertEqual(result['state'],'reviewable_partial_qa',result.get('error'))
        self.assertEqual(len(trees),2);self.assertNotEqual(trees[0],trees[1])
        self.assertTrue(result['original_still_matches']);self.assertFalse(result['original_modified'])
        self.assertEqual(self.git('rev-parse','HEAD'),self.head)
        self.assertEqual(before,{name:(self.root/name).read_bytes() for name in before})
        diff=Path(result['patch']).read_text()
        self.assertIn('+after alpha.txt',diff);self.assertIn('+after beta.txt',diff)
        report=json.loads((Path(result['run'])/'run.json').read_text())
        self.assertEqual(report['baseline']['kind'],'mock-central-qa')
        self.assertTrue(all(t['execution']['backend']=='mock' for t in report['plan']['tasks']))

    def test_cross_project_escaped_scope_and_execution_gate(self):
        plan=self.plan()
        with self.assertRaises(IpanemaError):engine.execute(self.p,plan)
        with self.assertRaises(IpanemaError):engine.execute(self.p,{**plan,'project':'other'},authorize=True)
        with self.assertRaises(IpanemaError):engine.execute(self.p,{**plan,'allowed_files':['../outside']},authorize=True)

    def test_duplicate_writers_never_dispatch_models(self):
        plan=self.plan();first=plan['tasks'][0]
        first['allowed_files']=['alpha.txt'];first['read_files']=['alpha.txt'];first['dependencies']=[]
        reviewer=next(t for t in plan['tasks']if t['role']=='review')
        reviewer['dependencies']=[first['id'],'duplicate']
        plan['tasks']=[first,{**first,'id':'duplicate'},reviewer]
        with patch('ipanema.orchestration.engine.worker') as mock,patch('ipanema.orchestration.engine.central_qa',side_effect=self.mock_qa),patch('ipanema.orchestration.isolation.probe',return_value={'available':True}):
            result=engine.execute(self.p,plan,authorize=True)
        self.assertEqual(result['state'],'blocked');mock.assert_not_called()
        self.assertTrue(result['original_still_matches'])

    def test_bounded_correction_restores_each_own_attempt_before_retry(self):
        plan=self.plan();plan['max_correction_attempts']=2
        task=plan['tasks'][0];task['allowed_files']=['alpha.txt'];task['read_files']=['alpha.txt']
        initial=(self.root/'alpha.txt').read_text();before=digest(self.root/'alpha.txt')
        result={'attempts':0};qa_results=iter([False,False,True]);retry_contents=[]
        def proposal(content):
            return {'decision':'proposed','summary':'Mock correction only','changes':[
                {'path':'alpha.txt','before_sha256':before,'content':content}]}
        def mock_qa(project,plan,tree,settings):
            return {**self.mock_qa(),'passed':next(qa_results)}
        def mock_retry(project,plan,task,tree,history,settings):
            self.assertEqual((tree/'alpha.txt').read_text(),initial)
            self.assertTrue(history[-1]['restored_own_changes'])
            retry_contents.append('fixed '+str(len(retry_contents)+1)+'\n')
            return proposal(retry_contents[-1])
        with patch('ipanema.orchestration.engine.central_qa',side_effect=mock_qa),patch('ipanema.orchestration.engine.worker',side_effect=mock_retry) as worker:
            final=engine.apply_and_test(self.p,plan,task,proposal('broken initial\n'),self.root,{},[],result)
        self.assertEqual(worker.call_count,2);self.assertEqual(result['attempts'],2)
        self.assertEqual([c['qa']['passed'] for c in result['corrections']],[False,False,True])
        self.assertEqual((self.root/'alpha.txt').read_text(),retry_contents[-1])
        self.assertEqual(final['changes'][0]['content'],retry_contents[-1])
        self.assertNotEqual(self.git('rev-parse','HEAD'),self.head)

    def test_persistent_failure_hits_limit_and_restores_only_own_changes(self):
        plan=self.plan();plan['max_correction_attempts']=2
        task=plan['tasks'][0];task['allowed_files']=['alpha.txt','new-file.txt']
        initial=(self.root/'alpha.txt').read_text();before=digest(self.root/'alpha.txt')
        (self.root/'beta.txt').write_text('unrelated user change\n')
        result={'attempts':0}
        def proposal():
            return {'decision':'proposed','summary':'Synthetic failing correction','changes':[
                {'path':'alpha.txt','before_sha256':before,'content':'still broken\n'},
                {'path':'new-file.txt','before_sha256':None,'content':'new own file\n'}]}
        def mock_retry(project,plan,task,tree,history,settings):
            self.assertEqual((tree/'alpha.txt').read_text(),initial)
            self.assertFalse((tree/'new-file.txt').exists())
            self.assertEqual((tree/'beta.txt').read_text(),'unrelated user change\n')
            return proposal()
        with patch('ipanema.orchestration.engine.central_qa',return_value={**self.mock_qa(),'passed':False}),patch('ipanema.orchestration.engine.worker',side_effect=mock_retry) as worker:
            with self.assertRaisesRegex(IpanemaError,'Límite'):
                engine.apply_and_test(self.p,plan,task,proposal(),self.root,{},[],result)
        self.assertEqual(worker.call_count,2);self.assertEqual(result['attempts'],2)
        self.assertEqual(len(result['corrections']),3)
        self.assertEqual((self.root/'alpha.txt').read_text(),initial)
        self.assertFalse((self.root/'new-file.txt').exists())
        self.assertEqual((self.root/'beta.txt').read_text(),'unrelated user change\n')
        self.assertEqual(self.git('rev-parse','HEAD'),self.head)

    def test_concurrent_original_edit_blocks_and_diff_uses_immutable_baseline(self):
        plan=planner.make_plan(self.p,'Corrige errata',files=['alpha.txt'],scope='workspace')
        def mock_worker(project,plan,task,tree,history,settings):
            # Explicitly simulate a separate user editing the original while the
            # actual worker would only see its isolated worktree/snapshot.
            (self.root/'alpha.txt').write_text('user edit during inference\n')
            task['execution']={'backend':'mock','inference_executed':False}
            return {'decision':'proposed','summary':'Synthetic isolated edit','changes':[
                {'path':'alpha.txt','before_sha256':digest(tree/'alpha.txt'),'content':'worker proposal\n'}]}
        with patch('ipanema.orchestration.engine.worker',side_effect=mock_worker),patch('ipanema.orchestration.engine.central_qa',side_effect=self.mock_qa),patch('ipanema.orchestration.isolation.probe',return_value={'available':True}):
            result=engine.execute(self.p,plan,authorize=True)
        self.assertEqual(result['state'],'blocked');self.assertFalse(result['original_still_matches'])
        self.assertEqual((self.root/'alpha.txt').read_text(),'user edit during inference\n')
        diff=Path(result['patch']).read_text()
        self.assertIn('-before alpha.txt',diff);self.assertIn('+worker proposal',diff)
        self.assertNotIn('user edit during inference',diff)
        self.assertEqual(self.git('rev-parse','HEAD'),self.head)

    def test_inherited_git_routing_and_configuration_cannot_escape_snapshot(self):
        snapshot=self.root/'separate-snapshot';snapshot.mkdir()
        (snapshot/'fixture.txt').write_text('isolated data\n')
        initial={name:(self.root/name).read_bytes() for name in ('alpha.txt','beta.txt')}
        polluted={
            'GIT_DIR':str(self.root/'.git'),'GIT_WORK_TREE':str(self.root),
            'GIT_INDEX_FILE':str(self.root/'.git/index'),
            'GIT_CONFIG_COUNT':'1','GIT_CONFIG_KEY_0':'core.worktree','GIT_CONFIG_VALUE_0':str(self.root),
            'GIT_CONFIG_PARAMETERS':'malformed-environment-configuration',
            'GIT_TRACE':str(self.root/'unexpected-git-trace.log'),
            'GIT_CONFIG_GLOBAL':str(self.root/'unexpected-global-config'),
        }
        with patch.dict(os.environ,polluted):
            engine.git(snapshot,'init','-q')
            engine.git(snapshot,'add','fixture.txt')
            engine.git(snapshot,'-c','user.name=Fixture','-c','user.email=fixture@invalid','commit','-qm','Isolated commit')
            actual=engine.git(snapshot,'rev-parse','--show-toplevel').strip()
            self.assertEqual(Path(actual),snapshot)
            self.assertEqual(engine.git(snapshot,'config','--get','core.hooksPath').strip(),'/dev/null')
            allowed=engine.git_environment()
            self.assertEqual({k for k in allowed if k.startswith('GIT_')},{'GIT_CONFIG_NOSYSTEM','GIT_CONFIG_GLOBAL'})
        self.assertEqual(self.git('rev-parse','HEAD'),self.head)
        self.assertEqual(initial,{name:(self.root/name).read_bytes() for name in initial})
        self.assertFalse((self.root/'unexpected-git-trace.log').exists())
        self.assertFalse((self.root/'fixture.txt').exists())

    def test_critical_plan_cannot_remove_independent_review_by_forging_risk(self):
        plan=planner.make_plan(self.p,'Corrige precio',files=['alpha.txt'],scope='workspace')
        self.assertEqual(plan['classification']['level'],'L4')
        plan['classification']={'level':'L1','risk':'normal','production_request':False}
        plan['tasks']=[task for task in plan['tasks'] if task['role']!='review']
        with patch('ipanema.orchestration.engine.worker') as worker,patch('ipanema.orchestration.engine.central_qa') as qa:
            with self.assertRaisesRegex(IpanemaError,'revisiones independientes'):
                engine.execute(self.p,plan,authorize=True)
        worker.assert_not_called();qa.assert_not_called()
        self.assertEqual(self.git('rev-parse','HEAD'),self.head)


if __name__=='__main__':unittest.main()
