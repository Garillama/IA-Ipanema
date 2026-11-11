"""Chrome real sobre fixture local; nunca representa un resultado de Google."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from tests.support import ROOT, make_project, put
from tests.browser.fixture_server import server
from tests.browser import test_browser_qa as existing
from ipanema.core import Project
from ipanema.seo.engineering import captured_readiness


class EngineeringBrowserV4(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        existing.BrowserQATests.setUpClass()

    def test_initial_rendered_nojs_and_blocked_commercial_post(self):
        with tempfile.TemporaryDirectory(prefix='seo v4 browser ') as folder, server() as (base, state):
            root = make_project(Path(folder) / 'agent', identifier='fixture', theme=False)
            cfg = root / 'projects/fixture.json'
            data = json.loads(cfg.read_text()); data['public_url'] = base + '/'; put(cfg, data)
            out = root / 'browser'
            job = {'project': 'fixture', 'output': str(out), 'pages': [{'name': 'home', 'page_type': 'home', 'url': base + '/?probe=seo&extra_probe=post'}],
                   'widths': [390], 'mode': 'full', 'axe': True, 'capture_seo': True, 'interactions': []}
            put(root / 'job.json', job)
            env = {k: v for k, v in os.environ.items() if not k.startswith('IPANEMA_') or k in ('IPANEMA_NODE_MODULE_ROOT', 'IPANEMA_CHROME_PATH')}
            env.update({'IPANEMA_PUBLIC_URL': base, 'IPANEMA_EVIDENCE_DIR': str(out), 'IPANEMA_ALLOW_NETWORK': '0'})
            completed = subprocess.run(['node', str(ROOT / 'tools/qa_browser.mjs'), str(root / 'job.json')], cwd=ROOT,
                                       env=env, capture_output=True, text=True, timeout=90)
            capture = out / 'home-390-rendered.seo.json'
            no_js = out / 'home-390-no-js.seo.json'
            self.assertTrue(capture.is_file(), completed.stderr)
            self.assertTrue(no_js.is_file(), completed.stderr)
            result = captured_readiness(Project(root), capture, no_js)
            delta = result['node']['layers']['initial_to_rendered']
            self.assertIn(base + '/late-product/', delta['links_only_after_js'])
            self.assertFalse(result['node']['layers']['googlebot_rendering_tested'])
            self.assertFalse(result['node']['template_audit']['structured_data']['states']['syntax_valid'])
            self.assertEqual(state['posts'], 0)
            self.assertTrue(result['node']['layers']['no_js_available'])
