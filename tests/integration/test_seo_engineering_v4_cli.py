import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from tests.support import ROOT, make_project, put


class EngineeringCLI(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='seo v4 moved ')
        self.root = make_project(Path(self.tmp.name) / 'agent with spaces', theme=False)
        shutil.copytree(ROOT / 'tools', self.root / 'tools', ignore=shutil.ignore_patterns('__pycache__'))
        self.env = {k: v for k, v in os.environ.items() if not k.startswith('IPANEMA_')}
        self.home = 'https://example.invalid/'
        self.html = '<html><head><title>Fixture</title><link rel="canonical" href="' + self.home + '"></head><body class="template-home"><main><h1>Fixture</h1><p>Main</p><a href="/cat">Category</a></main></body></html>'
        self.responses = self.root / 'responses.json'
        put(self.responses, {'project': 'sample', 'home': self.home, 'responses': {
            self.home + 'robots.txt': {'status': 200, 'body': 'User-agent: *\nAllow: /'},
            self.home + 'sitemap.xml': {'status': 200, 'headers': {'content-type': 'application/xml'},
                                     'body': '<urlset><url><loc>' + self.home + '</loc></url></urlset>'},
            self.home: {'status': 200, 'body': self.html}}})

    def tearDown(self): self.tmp.cleanup()

    def cli(self, *args):
        return subprocess.run([sys.executable, str(self.root / 'tools/ia.py'), 'seo', *map(str, args)],
                              cwd=self.tmp.name, env=self.env, capture_output=True, text=True, timeout=20)

    def capture(self, name, *, no_js=False, rendered=None):
        path = self.root / (name + '.json')
        put(path, {'kind': 'seo-browser-projection', 'project': 'sample', 'url': self.home,
                   'page_type': 'home', 'mode': 'no-js' if no_js else 'rendered', 'status': 200,
                   'at': '2026-11-11T00:00:00Z', 'headers': {}, 'initial': {'html': self.html},
                   'rendered': {'html': rendered or self.html}})
        return path

    def test_offline_crawl_json_csv_relocated_and_no_network(self):
        result = self.cli('crawl', '--responses', self.responses)
        self.assertEqual(result.returncode, 0, result.stderr)
        saved = json.loads(result.stdout)
        run = Path(saved['report']).parent
        report = json.loads((run / 'report.json').read_text())
        self.assertEqual(report['source'], 'offline_injected_transport')
        self.assertEqual(report['provenance']['clock'], 'virtual_offline_not_network_timing')
        self.assertEqual(report['urls'][0]['indexability']['state'], 'indexable_candidate')
        self.assertFalse(report['urls'][0]['indexability']['indexation_observed'])
        for filename in ['urls.csv', 'edges.csv', 'sitemap.csv', 'backlog.csv']:
            self.assertTrue((run / filename).is_file())
        self.assertEqual(len(report['graph']['broken_internal_links']), 1)

    def test_explicit_network_permission_and_limits_required(self):
        result = self.cli('crawl')
        self.assertEqual(result.returncode, 2)
        result = self.cli('crawl', '--responses', self.responses, '--concurrency', '4')
        self.assertEqual(result.returncode, 2)
        self.assertNotIn('Traceback', result.stderr)

    def test_sitemap_command_preserves_native_urlset(self):
        xml = self.root / 'sitemap.xml'
        put(xml, '<urlset><url><loc>' + self.home + '</loc></url></urlset>')
        result = self.cli('sitemap', '--xml', xml, '--source-url', self.home + 'sitemap.xml')
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(Path(json.loads(result.stdout)['report']).read_text())
        self.assertEqual(report['xml_kind'], 'urlset')
        self.assertFalse(report['remote_mutations'])

    def test_readiness_and_regression_noindex_href_h1(self):
        capture, no_js = self.capture('capture'), self.capture('nojs', no_js=True)
        robots = self.root / 'robots.txt'; put(robots, 'User-agent: *\nAllow: /')
        first = self.cli('readiness', '--capture', capture, '--no-js', no_js, '--robots', robots)
        self.assertEqual(first.returncode, 0, first.stderr)
        before = json.loads(first.stdout)['report']
        changed = self.html.replace('</head>', '<meta name="robots" content="noindex"></head>').replace('<h1>Fixture</h1>', '<h1>Changed</h1>').replace('href="/cat"', '')
        document = json.loads(capture.read_text()); document['initial']['html'] = changed; document['rendered']['html'] = changed; put(capture, document)
        second = self.cli('readiness', '--capture', capture, '--no-js', no_js, '--robots', robots)
        after = json.loads(second.stdout)['report']
        gate = self.cli('gate', '--before', before, '--after', after)
        self.assertEqual(gate.returncode, 1, gate.stderr)
        report = json.loads(Path(json.loads(gate.stdout)['report']).read_text())
        failures = [c['name'] for c in report['checks'] if c['status'] == 'failed']
        for name in ['noindex', 'h1', 'links']:
            self.assertTrue(any(c.endswith(':' + name) for c in failures), failures)
        self.assertEqual(report['network_requests'], 0)

    def test_enrich_dom_and_nojs_keep_observation_provenance(self):
        run = self.cli('crawl', '--responses', self.responses)
        crawl_path = json.loads(run.stdout)['report']
        capture = self.capture('capture', rendered=self.html.replace('</main>', '<a href="/late">Late</a></main>'))
        no_js = self.capture('nojs', no_js=True)
        result = self.cli('enrich', '--crawl', crawl_path, '--capture', capture, '--no-js', no_js)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(Path(json.loads(result.stdout)['report']).read_text())
        self.assertIn(self.home + 'late', report['urls'][0]['layers']['initial_to_rendered']['links_only_after_js'])
        self.assertIn('capture_provenance', report['urls'][0])

    def test_foreign_captures_and_google_exports_rejected(self):
        capture = self.capture('foreign')
        data = json.loads(capture.read_text()); data['project'] = 'other'; put(capture, data)
        result = self.cli('readiness', '--capture', capture)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn('Traceback', result.stderr)
