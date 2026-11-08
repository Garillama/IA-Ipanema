import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from tests.support import ROOT, make_project, put
from tests.browser.fixture_server import server
from ipanema.compare import visual


class BrowserQATests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not shutil.which('node'):
            raise unittest.SkipTest('Node opcional no instalado')
        r=subprocess.run(['node',str(ROOT/'tools/browser_runtime.mjs'),'--doctor'],capture_output=True,text=True,timeout=20)
        if r.returncode:
            raise unittest.SkipTest('Runtime de navegador no disponible')
        doctor=json.loads(r.stdout)
        if not doctor['chrome'] or not all(d['available'] for name,d in doctor['dependencies'].items() if name!='lighthouse'):
            raise unittest.SkipTest('Chrome/Puppeteer/axe opcionales ausentes')

    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='ipanema browser ')
        self.root=Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def run_job(self, base, suffix='', *, widths=None, mode='quick', interactions=None, pages=None, lighthouse=False):
        job={'project':'fixture','output':str(self.root/'out'),'pages':pages or [{'name':'home','url':base+suffix}],
             'widths':widths or [390,1440],'mode':mode,'axe':True,'interactions':interactions or [],'lighthouse':lighthouse}
        put(self.root/'job.json',job)
        env={k:v for k,v in os.environ.items() if not k.startswith('IPANEMA_') or k in ('IPANEMA_NODE_MODULE_ROOT','IPANEMA_CHROME_PATH')}
        env.update({'IPANEMA_PUBLIC_URL':base,'IPANEMA_EVIDENCE_DIR':str(self.root/'out'),'IPANEMA_ALLOW_NETWORK':'0'})
        r=subprocess.run(['node',str(ROOT/'tools/qa_browser.mjs'),str(self.root/'job.json')],env=env,capture_output=True,text=True,timeout=120)
        path=self.root/'out/browser-report.json'
        self.assertTrue(path.is_file(),r.stderr)
        result=json.loads(path.read_text())
        artifact=os.getenv('IPANEMA_FIXTURE_ARTIFACT_DIR')
        if artifact:
            destination=Path(artifact)/self._testMethodName
            if not destination.exists():
                shutil.copytree(self.root/'out',destination)
        return r,result

    def test_good_page_all_widths_no_js_motion_network_and_menu(self):
        interactions=[{'name':'menu','page':'home','widths':[390],'steps':[
            {'action':'click','selector':'#menu-toggle'}, {'action':'assert_visible','selector':'#menu'},
            {'action':'assert_focus','selector':'#menu'}, {'action':'press','key':'Escape'},
            {'action':'assert_hidden','selector':'#menu'}]}]
        with server() as (base,state):
            r,result=self.run_job(base,widths=[360,390,768,1024,1440,1920],mode='full',interactions=interactions)
            self.assertEqual(r.returncode,0,(r.stderr,result.get('error'),[c['name'] for c in result['checks'] if c['status']=='failed']))
            self.assertEqual(len(result['records']),8)
            mobile=json.loads((self.root/'out/home-390-rendered.json').read_text())
            desktop=json.loads((self.root/'out/home-1440-rendered.json').read_text())
            self.assertTrue(any(n['url'].endswith('/mobile.png') and n.get('completed') for n in mobile['navigation_network']))
            self.assertFalse(any(n['url'].endswith('/mobile.png') for n in desktop['navigation_network']))
            self.assertTrue(any(n['url'].endswith('/desktop.png') and n.get('completed') for n in desktop['navigation_network']))
            self.assertEqual(state['posts'],0)
            self.assertEqual(visual(self.root/'out/home-390-rendered.png',self.root/'out/home-390-rendered.png')['status'],'passed')

    def test_bad_page_detects_seo_overflow_and_keyboard_regression(self):
        interaction=[{'name':'menu','widths':[390],'steps':[{'action':'click','selector':'#menu-toggle'},
            {'action':'press','key':'Escape'},{'action':'assert_hidden','selector':'#menu'}]}]
        with server() as (base,state):
            r,result=self.run_job(base,'/broken/',widths=[390],interactions=interaction)
            self.assertEqual(r.returncode,1)
            failures=[c['name'] for c in result['checks'] if c['status']=='failed']
            for check in ('overflow','h1','canonical','jsonld','carousel-links','assert_hidden'):
                self.assertTrue(any(check in name for name in failures),(check,failures))
            self.assertEqual(state['posts'],0)

    def test_runtime_blocks_page_post_requests(self):
        with server() as (base,state):
            r,result=self.run_job(base,'/?probe=post',widths=[390])
            self.assertEqual(r.returncode,0,(r.stderr,result.get('error')))
            self.assertEqual(state['posts'],0)
            record=json.loads((self.root/'out/home-390-rendered.json').read_text())
            self.assertTrue(any(n['method']=='POST' and n.get('completed') is False for n in record['network']))

    def test_http_429_stops_before_next_page(self):
        with server() as (base,state):
            r,result=self.run_job(base,widths=[390],pages=[{'name':'limited','url':base+'/rate-limited/'},{'name':'next','url':base+'/should-not-run/'}])
            self.assertEqual(r.returncode,2)
            self.assertEqual(result['outcome'],'blocked')
            self.assertNotIn('/should-not-run/',state['gets'])

    def test_lighthouse_local_profiles_have_real_lab_metrics(self):
        doctor=subprocess.run(['node',str(ROOT/'tools/browser_runtime.mjs'),'--doctor'],capture_output=True,text=True,timeout=20)
        if not json.loads(doctor.stdout)['dependencies']['lighthouse']['available']:
            self.skipTest('Lighthouse opcional ausente')
        with server() as (base,state):
            r,result=self.run_job(base,'/?probe=post',widths=[390],lighthouse=True)
            self.assertEqual(r.returncode,0,(r.stderr,result.get('error')))
            for profile in ('mobile','desktop'):
                metrics=json.loads((self.root/f'out/home-{profile}-metrics.json').read_text())
                self.assertGreater(metrics['metrics']['lcp_ms'],0)
                self.assertIsNone(metrics['field_inp'])
                self.assertEqual(metrics['profile'],profile)
                self.assertIn('throttling',metrics['config'])
                self.assertTrue(metrics['environment']['browser'])
            self.assertEqual(state['posts'],0)
            artifact=os.getenv('IPANEMA_FIXTURE_ARTIFACT_DIR')
            if artifact:
                put(Path(artifact)/self._testMethodName/'post-probe.json',{'server_post_requests':state['posts'],'profiles':['mobile','desktop'],'expectation':0})

    def test_legacy_collector_uses_portable_runtime_and_new_output(self):
        with server() as (base,state):
            env={k:v for k,v in os.environ.items() if not k.startswith('IPANEMA_') or k in ('IPANEMA_NODE_MODULE_ROOT','IPANEMA_CHROME_PATH')}
            env.update({'IPANEMA_PUBLIC_URL':base,'IPANEMA_EVIDENCE_DIR':str(self.root/'legacy')})
            r=subprocess.run(['node',str(ROOT/'tools/inspect_storefront.mjs'),base],cwd=self.tmp.name,env=env,capture_output=True,text=True,timeout=30)
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertTrue((self.root/'legacy/measurements/browser/storefront-discovery.json').is_file())
            self.assertEqual(state['posts'],0)

    def test_unified_python_component_runner_and_measured_budgets(self):
        from ipanema.core import Project
        from ipanema.qa import execute
        agent=make_project(self.root/'agent')
        shutil.copytree(ROOT/'tools',agent/'tools',ignore=shutil.ignore_patterns('__pycache__'))
        with server() as (base,state):
            put(agent/'projects/sample.local.json',{'qa_base_url':base})
            project=Project(agent)
            passed=execute(project,'component',pages=['home'],component='.cards')
            self.assertEqual(passed['outcome'],'passed',passed['checks'])
            project.qa['budgets']={'requests':0}
            failed=execute(project,'page',pages=['home'])
            self.assertEqual(failed['outcome'],'failed')
            browser=failed['checks'][0]['details']['report']
            self.assertTrue(any(':budget:requests' in c['name'] and c['status']=='failed' for c in browser['checks']))
            self.assertEqual(state['posts'],0)
