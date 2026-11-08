import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from tests.support import ROOT, make_project, put
from ipanema.core import digest


class SEOCLI(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='seo relocated ');self.root=Path(self.tmp.name)/'agent with spaces'
        make_project(self.root,theme=False)
        shutil.copytree(ROOT/'tools',self.root/'tools',ignore=shutil.ignore_patterns('__pycache__'))
        self.env={k:v for k,v in os.environ.items() if not k.startswith('IPANEMA_')}
        self.url='https://example.invalid/product'
        self.html=self.root/'initial.html'
        put(self.html,'<title>Fixture</title><h1>Fixture</h1><link rel="canonical" href="'+self.url+'">')

    def tearDown(self):self.tmp.cleanup()

    def cli(self,*args):
        return subprocess.run([sys.executable,str(self.root/'tools/ia.py'),'seo',*map(str,args)],cwd=self.tmp.name,env=self.env,capture_output=True,text=True,timeout=20)

    def test_offline_audit_runs_relocated_without_theme(self):
        rendered=self.root/'rendered.html';put(rendered,self.html.read_text()+'<a href="/late-product">Product</a>')
        result=self.cli('audit','--html',self.html,'--url',self.url,'--type','category','--rendered',rendered,'--status','200')
        self.assertEqual(result.returncode,0,result.stderr)
        summary=json.loads(result.stdout);report=json.loads(Path(summary['report']).read_text())
        self.assertFalse(report['indexation_verified']);self.assertIn('SEO020',{f['rule'] for f in report['findings']})
        self.assertTrue(Path(summary['summary']).is_file())

    def test_invalid_jsonld_yields_error_report_not_pass(self):
        put(self.html,self.html.read_text()+'<script type="application/ld+json">{"@type":"WebPage",}</script>')
        result=self.cli('audit','--html',self.html,'--url',self.url,'--type','category')
        self.assertEqual(result.returncode,1,result.stderr)
        self.assertGreater(json.loads(result.stdout)['error_findings'],0)

    def test_unauthorized_google_read_never_needs_credentials(self):
        path=self.root/'request.json';put(path,{'inspectionUrl':self.url})
        result=self.cli('google-read','--provider','gsc','--operation','inspect_url','--request',path)
        self.assertEqual(result.returncode,2);self.assertIn('autorización',result.stderr)
        self.assertNotIn('Traceback',result.stderr)
        self.assertFalse((self.root/'reports').exists())

    def test_no_connection_fallback_and_source_block(self):
        result=self.cli('connections');self.assertEqual(result.returncode,0,result.stderr)
        self.assertTrue(all(not p['connected'] for p in json.loads(result.stdout)['providers']))
        source=self.cli('source');self.assertEqual(source.returncode,2);self.assertIn('theme_root',source.stderr)

    def test_generate_requires_real_evidence_and_checks_existing(self):
        catalog={'project':'sample','url':self.url,'data':{'product':{'name':'Fixture','price':'12','currency':'MXN','image':'https://example.invalid/i.webp'}}}
        evidence=self.root/'reports/runs/catalog.json';put(evidence,catalog)
        facts=self.root/'facts.json';put(facts,{'project':'sample','url':self.url,'page_type':'product','source':{
            'kind':'authorized_catalog_export','observed_at':'2026-11-08','reference':'reports/runs/catalog.json','sha256':digest(evidence)}})
        result=self.cli('generate','--facts',facts,'--target','Product','--html',self.html)
        self.assertEqual(result.returncode,0,result.stderr)
        proposal=json.loads(Path(json.loads(result.stdout)['report']).read_text())
        self.assertEqual(proposal['data']['offers']['price'],'12');self.assertFalse(proposal['theme_modified'])
        put(self.html,self.html.read_text()+'<script type="application/ld+json">'+proposal['json_ld']+'</script>')
        result=self.cli('generate','--facts',facts,'--target','Product','--html',self.html)
        self.assertEqual(result.returncode,2);self.assertIn('ya existe',result.stderr)

    def test_projection_initial_rendered_nojs(self):
        capture=self.root/'capture.json';nojs=self.root/'nojs.json'
        data={'kind':'seo-browser-projection','project':'sample','url':self.url,'page_type':'category','status':200,'at':'2026-11-08',
              'width':390,'mode':'rendered','initial':{'html':self.html.read_text(),'limitations':['Fixture projection.']},
              'rendered':{'html':self.html.read_text()+'<a href="/late">Late</a>'}}
        put(capture,data);put(nojs,{**data,'mode':'no-js','rendered':data['initial']})
        result=self.cli('audit','--capture',capture,'--no-js',nojs)
        self.assertEqual(result.returncode,0,result.stderr)
        report=json.loads(Path(json.loads(result.stdout)['report']).read_text())
        self.assertTrue(report['no_js_captured']);self.assertIn('rendered_validation',report)

    def test_seo_evals_are_actions_not_model_approval(self):
        result=self.cli('evals');self.assertEqual(result.returncode,0,result.stderr)
        report=json.loads(Path(json.loads(result.stdout)['report']).read_text())
        self.assertEqual(len(report['cases']),8);self.assertEqual(report['outcome'],'passed')
        self.assertTrue(all(not c['live_google_test'] for c in report['cases']))


if __name__=='__main__':unittest.main()
