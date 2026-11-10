"""CLI y MCP reales sobre pipes; proveedores sin credenciales/red, fixtures aparte."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock
from tests.support import ROOT, make_project
from ipanema.core import Project, IpanemaError
from ipanema.access.gateway import Gateway
from ipanema.access.policy import Policy
from ipanema.access.mcp import StdioClient
from ipanema.performance.service import Service


class PerformanceCLI(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='performance relocated ');self.addCleanup(self.tmp.cleanup)
        self.root=make_project(Path(self.tmp.name)/'repo con espacios',theme=False)
        shutil.copytree(ROOT/'tools',self.root/'tools',ignore=shutil.ignore_patterns('__pycache__'))
        self.env={k:v for k,v in os.environ.items()if not k.startswith('IPANEMA_')}

    def cli(self,*args):
        return subprocess.run([sys.executable,str(self.root/'tools/ia.py'),*args],cwd=self.tmp.name,env=self.env,capture_output=True,text=True,timeout=15)

    def test_relocated_and_no_theme_required(self):
        result=self.cli('performance','doctor')
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertFalse(json.loads(result.stdout)['network_tested'])

    def test_network_permission_and_missing_keys(self):
        for device in ('mobile','desktop'):
            denied=self.cli('performance','pagespeed','--device',device)
            self.assertEqual(denied.returncode,2)
            allowed=self.cli('performance','pagespeed','--device',device,'--allow-network')
            report=json.loads(allowed.stdout);r=report['sources']['pagespeed']
            self.assertEqual(r['status'],'credentials_unavailable');self.assertEqual(r['network_attempts'],0)
            self.assertFalse(report['validation']['external_request_attempted'])

    def test_crux_not_anonymous(self):
        for command in ('crux','history'):
            report=json.loads(self.cli('performance',command,'--allow-network').stdout)
            self.assertEqual(next(iter(report['sources'].values()))['status'],'credentials_unavailable')

    def test_foreign_url_denied(self):
        result=self.cli('performance','pagespeed','--url','https://foreign.invalid','--allow-network')
        self.assertEqual(result.returncode,2);self.assertNotIn('sources',json.loads(result.stderr))

    def test_real_mcp_transport_missing_keys_and_no_write_tools(self):
        project=Project(root=self.root)
        for agent in ('claude','codex'):
            grant=Policy(project).issue(agent,'perf-read',['psi.read','crux.read'],allow_network=True,max_calls=5)
            client=StdioClient([sys.executable,str(self.root/'tools/access_mcp.py'),'--project','sample','--grant',grant['id']],cwd=self.root,env=self.env)
            try:
                tools=client.tools();self.assertEqual(len(tools),3)
                response=client.request('tools/call',{'name':'psi_run_pagespeed','arguments':{'request':{'device':'mobile'}}})
                result=json.loads(response['content'][0]['text'])
                self.assertEqual(result['status'],'credentials_unavailable')
                self.assertTrue(response['isError'])
                denied=client.request('tools/call',{'name':'publish','arguments':{}})
                self.assertTrue(denied['isError'])
            finally:client.close()

    def test_gateway_shares_service_and_counts_cache_as_task_call(self):
        project=Project(root=self.root)
        transport=Mock(return_value=json.loads((ROOT/'tests/fixtures/performance/pagespeed-mobile.json').read_text()))
        # Offline fixture env is explicitly installed and removed; no real API request.
        from unittest.mock import patch
        with patch.dict(os.environ,{'IPANEMA_SAMPLE_PSI_KEY':'synthetic'}):
            project.data['google']={'performance':{'pagespeed_key_env':'IPANEMA_SAMPLE_PSI_KEY'}}
            grant=Policy(project).issue('codex','perf-fixture',['psi.read'],allow_network=True,max_calls=3)
            gateway=Gateway(project,grant['id'],performance_factory=lambda p:Service(p,transport=transport))
            a=gateway.call('psi_run_pagespeed',{'request':{}})
            b=gateway.call('psi_run_pagespeed',{'request':{}})
            self.assertEqual(a['status'],'observed');self.assertTrue(b['cache_hit'])
            self.assertEqual(transport.call_count,1);self.assertEqual(Policy(project).load(grant['id'])['calls'],2)
            with self.assertRaises(IpanemaError):gateway.call('crux_query_record',{'request':{}})
            with self.assertRaises(IpanemaError):Policy(project).issue('commandcode','disabled',['psi.read'],allow_network=True)
