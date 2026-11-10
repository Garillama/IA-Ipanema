"""Contrato MCP real sobre pipes y CLI relocatable, sin cuentas externas."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from tests.support import ROOT, make_project, put
from ipanema.access.mcp import StdioClient


class AccessCLI(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='access relocated ')
        self.addCleanup(self.tmp.cleanup)
        self.root = make_project(Path(self.tmp.name) / 'repo with spaces', theme=False)
        shutil.copytree(ROOT / 'tools', self.root / 'tools', ignore=shutil.ignore_patterns('__pycache__'))
        self.env = {k:v for k,v in os.environ.items() if not k.startswith('IPANEMA_')}

    def cli(self, *args):
        return subprocess.run([sys.executable, str(self.root / 'tools/ia.py'), 'access', *map(str, args)],
                              cwd=self.tmp.name, env=self.env, capture_output=True, text=True, timeout=15)

    def test_no_install_no_network_and_no_false_connection(self):
        result = self.cli('doctor')
        self.assertEqual(result.returncode, 0, result.stderr)
        providers = json.loads(result.stdout)['providers']
        self.assertFalse(providers['devtools']['installed'])
        for name in ('gsc', 'analytics', 'merchant'):
            self.assertIsNone(providers[name]['api_available'])
            self.assertFalse(providers[name]['account_access_tested'])

    def test_each_runtime_gets_runnable_config_and_revocation_is_immediate(self):
        for agent in ('claude', 'codex', 'commandcode'):
            with self.subTest(agent=agent):
                result = self.cli('grant', '--agent', agent, '--task', 'seo-test', '--capability',
                                  'gsc.read', '--allow-network', '--allow-account-read')
                self.assertEqual(result.returncode, 0, result.stderr)
                grant = json.loads(result.stdout)
                config = json.loads(self.cli('config', '--grant', grant['id']).stdout)
                server = next(iter(config['mcpServers'].values()))
                client = StdioClient([server['command'], *server['args']], cwd=self.root, env=self.env)
                try:
                    self.assertEqual(len(client.tools()), 3)
                    self.assertEqual(self.cli('revoke', '--grant', grant['id']).returncode, 0)
                    with self.assertRaises(ValueError):
                        client.tools()
                finally:
                    client.close()

    def test_stdio_rejects_write_tools_and_does_not_leak_credentials(self):
        grant = json.loads(self.cli('grant', '--agent', 'codex', '--task', 'seo-test', '--capability',
                                    'gsc.read', '--allow-network', '--allow-account-read').stdout)
        self.env['IPANEMA_GSC_TOKEN'] = 'synthetic-private-value'
        client = StdioClient([sys.executable, str(self.root / 'tools/access_mcp.py'),
                              '--project', 'sample', '--grant', grant['id']], cwd=self.root, env=self.env)
        try:
            result = client.request('tools/call', {'name': 'submit_sitemap', 'arguments': {}})
            self.assertTrue(result['isError'])
            self.assertNotIn('synthetic-private-value', json.dumps(result))
        finally:
            client.close()


if __name__ == '__main__':
    unittest.main()
