"""Controlador puro y contratos CLI: sin inferencia ni cuentas remotas."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tests.support import ROOT, make_project
from ipanema.core import IpanemaError, Project, digest
from ipanema.orchestration import planner, adapters, engine


class Planning(unittest.TestCase):
    def test_commercial_risk_is_critical_even_for_one_file(self):
        for request in ('Cambia precio', 'Corrige carrito', 'Revisa checkout', 'Cambia stock', 'Publicar producción'):
            with self.subTest(request=request):
                value=planner.classify(request,['one.txt'])
                self.assertEqual(value['level'],'L4')
                self.assertTrue(value['independent_review_required'])
        self.assertTrue(planner.classify('Publicar producción')['production_request'])

    def test_simple_and_crosscutting_tasks_are_proportional(self):
        self.assertEqual(planner.classify('Corrige una errata',['one.txt'])['level'],'L1')
        self.assertEqual(planner.classify('Refactor de carrusel compartido',['one.txt'])['level'],'L3')
        self.assertEqual(planner.classify('Ajusta etiquetas',['a.txt','b.txt'])['level'],'L2')

    def test_make_plan_without_theme_or_knowledge(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Project(make_project(Path(folder),theme=False))
            simple=planner.make_plan(p,'Corrige una errata',files=['copy.txt'],scope='workspace')
            self.assertEqual(simple['project'],'sample')
            self.assertEqual(len(simple['tasks']),1)
            self.assertEqual(simple['tasks'][0]['agent'],'codex')
            self.assertFalse(simple.get('implementation_executed',False))
            self.assertIsNone(simple['knowledge'])
            complex_plan=planner.make_plan(p,'Optimiza carrusel sin afectar SEO',files=['carousel.tpl'],scope='theme')
            self.assertEqual([t['agent'] for t in complex_plan['tasks']],['claude','codex','commandcode'])
            self.assertEqual(complex_plan['tasks'][1]['dependencies'],['architecture'])
            audit=planner.make_plan(p,'Audita un texto',files=['copy.txt'],scope='workspace',read_only=True)
            self.assertEqual(audit['tasks'][0]['allowed_files'],[])
            self.assertEqual(audit['tasks'][0]['agent'],'commandcode')

    def test_ready_wave_dependencies_and_duplicate_writers(self):
        tasks=[{'id':'a','state':'pending','dependencies':[],'allowed_files':['a.txt']},
               {'id':'b','state':'pending','dependencies':[],'allowed_files':['b.txt']},
               {'id':'qa','state':'pending','dependencies':['a','b'],'allowed_files':[]}]
        self.assertEqual([t['id'] for t in planner.ready_wave(tasks,set())],['a','b'])
        tasks[0]['state']=tasks[1]['state']='completed'
        self.assertEqual([t['id'] for t in planner.ready_wave(tasks,{'a','b'})],['qa'])
        tasks[0]['state']=tasks[1]['state']='pending';tasks[1]['allowed_files']=['a.txt']
        with self.assertRaises(IpanemaError):planner.ready_wave(tasks,set())

    def test_file_paths_must_not_escape_or_export_private_configuration(self):
        for name in ('.','./','../file','/etc/passwd','projects/shop.local.json','.env','a\\b','.git/config','node_modules/lib.js','private.key'):
            with self.subTest(name=name),self.assertRaises(IpanemaError):planner.safe_path(name)

    def test_reader_waits_for_concurrent_dependency_writer(self):
        tasks=[{'id':'tokens','state':'pending','dependencies':[],'allowed_files':['tokens.css'],'read_files':['tokens.css']},
               {'id':'header','state':'pending','dependencies':[],'allowed_files':['header.tpl'],'read_files':['header.tpl','tokens.css']}]
        self.assertEqual([t['id'] for t in planner.ready_wave(tasks,set())],['tokens'])
        tasks[0]['state']='completed'
        self.assertEqual([t['id'] for t in planner.ready_wave(tasks,{'tokens'})],['header'])


class AdapterContracts(unittest.TestCase):
    def test_verified_argv_modes_do_not_bypass_permissions(self):
        with patch('ipanema.orchestration.adapters.shutil.which',side_effect=lambda name:'/usr/bin/'+name):
            for agent in adapters.NAMES:
                args=adapters.argv(agent,'explicit-reviewed-model','low')
                self.assertIn('explicit-reviewed-model',args)
                self.assertNotIn('--yolo',args)
                self.assertNotIn('--dangerously-bypass-approvals-and-sandbox',args)
                self.assertNotIn('--dangerously-skip-permissions',args)
            codex=adapters.argv('codex','model','low')
            self.assertIn('--ignore-user-config',codex);self.assertIn('read-only',codex)
            claude=adapters.argv('claude','model','low')
            self.assertEqual(claude[claude.index('--tools')+1],'')
            self.assertIn('--strict-mcp-config',claude)

    def test_missing_runtime_is_not_simulated(self):
        with patch('ipanema.orchestration.adapters.shutil.which',return_value=None):
            with self.assertRaises(IpanemaError):adapters.argv('codex','model')

    def test_parse_provider_json_and_ndjson(self):
        response={'decision':'approve','changes':[],'summary':'fixture'}
        self.assertEqual(adapters.parse_response('claude',json.dumps({'result':json.dumps(response)})),response)
        frames=[{'type':'thread.started','thread_id':'fixture'},
                {'type':'item.completed','item':{'type':'agent_message','text':json.dumps(response)}},
                {'type':'turn.completed','usage':{'input_tokens':1}}]
        self.assertEqual(adapters.parse_response('codex','\n'.join(json.dumps(f) for f in frames)),response)
        self.assertEqual(adapters.parse_response('commandcode',json.dumps({'type':'result','subtype':'success','result':json.dumps(response)})),response)

    def test_provider_error_tools_and_malformed_response_rejected(self):
        for value in ('not json',json.dumps({'is_error':True}),json.dumps({'type':'result','subtype':'error'}),
                      json.dumps({'type':'item.completed','item':{'type':'command_execution','command':'publish'}})):
            with self.subTest(value=value),self.assertRaises(IpanemaError):adapters.parse_response('codex',value)

    def test_model_selection_uses_dated_catalog(self):
        for agent in adapters.NAMES:
            for tier in ('fast','balanced','strong','critical'):
                selected=adapters.model_for(ROOT,agent,tier)
                self.assertTrue(selected['model']);self.assertTrue(selected['verified_at'])
                self.assertIn(tier,selected['reason'])


class ResponseBoundaries(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        (self.root/'a.txt').write_text('before')
        self.task={'role':'implementation','allowed_files':['a.txt']}
    def tearDown(self):self.tmp.cleanup()

    def response(self,path='a.txt',before=None):
        return {'decision':'proposed','changes':[{'path':path,'before_sha256':before or digest(self.root/'a.txt'),'content':'after'}]}

    def test_allowed_content_validates_without_writing(self):
        result=engine.validate_response(self.task,self.response(),self.root)
        self.assertEqual(result[0]['content'],'after');self.assertEqual((self.root/'a.txt').read_text(),'before')

    def test_escape_duplicate_hash_and_reviewer_changes_rejected(self):
        for response in (self.response('../outside'),self.response('/tmp/outside'),self.response('other.txt'),self.response(before='wrong')):
            with self.assertRaises(IpanemaError):engine.validate_response(self.task,response,self.root)
        response=self.response();response['changes']*=2
        with self.assertRaises(IpanemaError):engine.validate_response(self.task,response,self.root)
        with self.assertRaises(IpanemaError):engine.validate_response({**self.task,'role':'review'},self.response(),self.root)

    def test_sanitized_view_excludes_private_paths_and_symlinks(self):
        private=self.root/'.env';private.write_text('synthetic-private')
        (self.root/'project.local.json').write_text('{}')
        (self.root/'escape').symlink_to('/etc/passwd')
        git=self.root/'.git';git.mkdir();(git/'config').write_text('private metadata')
        view=engine.sanitized_view(self.root,self.root.parent/(self.root.name+'-view'))
        try:
            self.assertTrue((view/'a.txt').is_file())
            self.assertFalse((view/'.env').exists());self.assertFalse((view/'.git').exists())
            self.assertFalse((view/'project.local.json').exists());self.assertFalse((view/'escape').exists())
        finally:
            import shutil
            shutil.rmtree(view)

    def test_runtime_defaults_do_not_mount_entire_provider_home(self):
        with patch('ipanema.orchestration.engine.shutil.which',return_value='/opt/provider/bin/agent'):
            cfg=engine.runtime_defaults('codex')
            self.assertEqual(cfg['runtime_paths'],['/opt/provider/bin/agent'])
            self.assertNotIn(str(Path.home()),cfg['runtime_paths'])


if __name__=='__main__':unittest.main()
