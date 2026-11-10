"""DevTools instalado real + Chrome + gateway MCP; solo servidores loopback sintéticos."""
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from tests.support import ROOT, make_project, put
from ipanema.core import Project
from ipanema.access.mcp import StdioClient
from ipanema.access.policy import Policy


class Fixture(BaseHTTPRequestHandler):
    hits = []
    posts = []
    asset_url = None
    def do_GET(self):
        type(self).hits.append(self.path)
        self.send_response(403 if self.path == '/forbidden' else 200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        resource = f'<link rel="stylesheet" href="{type(self).asset_url}">' if type(self).asset_url else ''
        self.wfile.write(('<!doctype html><title>SEO fixture</title>' + resource + '<h1>IA-Ipanema fixture</h1><script>console.error("synthetic-browser-error");fetch("/should-not-write",{method:"POST",body:"synthetic"}).catch(()=>{});</script>').encode())
    def do_POST(self):
        type(self).posts.append(self.path)
        self.send_response(200); self.end_headers()
    def log_message(self, *args): pass


@unittest.skipUnless((ROOT / '.local/devtools/node_modules/chrome-devtools-mcp/package.json').exists(),
                     'DevTools opcional no instalado; no se instala en los tests')
class AccessBrowser(unittest.TestCase):
    def setUp(self):
        Fixture.posts = []
        Fixture.asset_url = None
        self.tmp = tempfile.TemporaryDirectory(prefix='access browser ')
        self.addCleanup(self.tmp.cleanup)
        self.server = ThreadingHTTPServer(('127.0.0.1', 0), Fixture)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.origin = 'http://127.0.0.1:' + str(self.server.server_port)
        root = make_project(Path(self.tmp.name) / 'repo with spaces', theme=False)
        config_path = root / 'projects/sample.json'
        config = json.loads(config_path.read_text())
        config['public_url'] = self.origin
        put(config_path, config)
        shutil.copytree(ROOT / 'tools', root / 'tools', ignore=shutil.ignore_patterns('__pycache__'))
        (root / '.local').mkdir()
        (root / '.local/devtools').symlink_to(ROOT / '.local/devtools', target_is_directory=True)
        self.project = Project(root)
        self.env = {k:v for k,v in os.environ.items() if not k.startswith('IPANEMA_')}

    def connect(self, profile='security'):
        grant = Policy(self.project).issue('codex', 'browser-fixture', ['devtools.read', 'devtools.performance'], allow_network=True, browser_profile=profile)
        client = StdioClient([sys.executable, str(self.project.root / 'tools/access_mcp.py'),
                              '--project', 'sample', '--grant', grant['id']], cwd=self.project.root, env=self.env, timeout=45)
        self.addCleanup(client.close)
        return client

    def call(self, client, name, args=None):
        result = client.call(name, args or {})
        return json.loads(result['content'][0]['text'])

    def test_real_discovery_navigation_snapshot_network_console_and_trace(self):
        client = self.connect()
        self.assertEqual(len(client.tools()), 6)
        self.assertEqual(self.call(client, 'devtools_open', {'url': self.origin + '/'})['status'], 'observed')
        self.assertIn('IA-Ipanema fixture', json.dumps(self.call(client, 'devtools_snapshot')))
        self.assertIn('[200]', json.dumps(self.call(client, 'devtools_network')))
        self.assertIn('synthetic-browser-error', json.dumps(self.call(client, 'devtools_console')))
        trace = self.call(client, 'devtools_trace')
        self.assertEqual(trace['status'], 'observed')
        self.assertIn('trace', json.dumps(trace).lower())
        denied = client.request('tools/call', {'name': 'devtools_open', 'arguments': {'url': 'https://example.invalid/'}})
        self.assertTrue(denied['isError'])
        denied = client.request('tools/call', {'name': 'evaluate_script', 'arguments': {'function': 'alert(1)'}})
        self.assertTrue(denied['isError'])

    def test_real_http_403_stops_browser_and_new_grants(self):
        client = self.connect()
        response = client.request('tools/call', {'name': 'devtools_open', 'arguments': {'url': self.origin + '/forbidden'}})
        self.assertTrue(response['isError'])
        self.assertEqual(json.loads(response['content'][0]['text'])['status'], 'forbidden_stop')
        self.assertTrue(Policy(self.project).stop_path('devtools').exists())
        next_client = self.connect()
        response = next_client.request('tools/call', {'name': 'devtools_open', 'arguments': {'url': self.origin + '/'}})
        self.assertTrue(response['isError'])

    def test_profiles_allow_registered_asset_only_and_block_post(self):
        class Asset(BaseHTTPRequestHandler):
            hits = []
            def do_GET(self):
                type(self).hits.append(self.path)
                self.send_response(200); self.send_header('Content-Type','text/css'); self.end_headers()
                self.wfile.write(b'h1{color:rgb(12,34,56)}')
            def log_message(self,*args): pass
        server = ThreadingHTTPServer(('127.0.0.1',0),Asset)
        threading.Thread(target=server.serve_forever,daemon=True).start()
        self.addCleanup(server.server_close); self.addCleanup(server.shutdown)
        resource_origin = 'http://127.0.0.1:' + str(server.server_port)
        Fixture.asset_url = resource_origin + '/legitimate.css'
        config_path = self.project.root/'projects/sample.json'
        config = json.loads(config_path.read_text()); config['browser'] = {'devtools_audit_origins':[resource_origin]}
        put(config_path,config); self.project = Project(self.project.root)
        security = self.connect()
        self.call(security,'devtools_open',{'url':self.origin+'/'})
        self.assertEqual(Asset.hits,[])
        audit = self.connect('audit')
        self.call(audit,'devtools_open',{'url':self.origin+'/'})
        self.assertIn('/legitimate.css',Asset.hits)
        self.assertIn('/legitimate.css',json.dumps(self.call(audit,'devtools_network')))
        self.assertEqual(Fixture.posts,[])


if __name__ == '__main__':
    unittest.main()
