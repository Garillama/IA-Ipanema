"""Verificación Node de proyecciones nuevas, sin navegador ni red."""
import json
import subprocess
import unittest
from tests.support import ROOT


class LighthouseProjection(unittest.TestCase):
    def test_safe_projection_reuses_diagnostics_without_private_html(self):
        script="""
import {safeLighthouseReport,lighthouseEvidence} from './tools/performance_evidence.mjs';
const lhr={audits:{'network-requests':{score:1,details:{items:[{url:'https://user:pass@example.invalid/?%2561pi_key=hidden',snippet:'private-html'}]}}},runWarnings:['See https://example.invalid/?token=hidden']};
console.log(JSON.stringify({report:safeLighthouseReport(lhr),diagnostics:lighthouseEvidence(lhr)}));
"""
        result=subprocess.run(['node','--input-type=module','-e',script],cwd=ROOT,capture_output=True,text=True,timeout=10)
        self.assertEqual(result.returncode,0,result.stderr)
        for value in ('private-html','user:pass','hidden'):self.assertNotIn(value,result.stdout)
        report=json.loads(result.stdout);self.assertIn('network-requests',report['report']['audits'])
        self.assertIsNone(report['diagnostics']['field_inp'])
