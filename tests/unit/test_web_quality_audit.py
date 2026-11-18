"""Etapa 2: Pruebas obligatorias (1–10) para la integración de Web Quality Audit (web-quality-audit)."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from support import ROOT
from ipanema.coordinator import AUTHORIZED_SKILLS, EXTERNAL_SKILLS, route
from ipanema.core import IpanemaError, Project
from ipanema.evals import evaluate
from ipanema.orchestration import engine, planner
from ipanema.performance import model
from ipanema.validation import validate


class WebQualityAuditIntegrationTests(unittest.TestCase):
    def test_01_registration_and_activation_of_web_quality_audit(self):
        skill_path = ROOT / ".agents/skills/web-quality-audit/SKILL.md"
        self.assertTrue(skill_path.is_file())
        content = skill_path.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\nname: web-quality-audit\n"))
        self.assertIn("afa8da942115f2961fdbfa80807ea0b232ff6c00", content)
        self.assertIn("MIT", content)
        self.assertIn("web-quality-audit", AUTHORIZED_SKILLS)
        meta = EXTERNAL_SKILLS["web-quality-audit"]
        self.assertEqual(meta["domain"], "quality-audit")
        self.assertEqual(meta["reuses"], ["cloudflare-web-perf"])

        trigger_prompts = [
            "Realiza una auditoría completa de una página de producto en Shopify",
            "Haz una revisión general de calidad web del sitio",
            "Necesito un diagnóstico técnico de una tienda Hydrogen",
            "Ejecuta una evaluación de Lighthouse y buenas prácticas",
            "Realiza una revisión integral de una interfaz React",
        ]
        for prompt in trigger_prompts:
            with self.subTest(prompt=prompt):
                routed = route(prompt)
                self.assertIn("web-quality-audit", routed["skills"])
                self.assertEqual(routed["primary_skills"]["quality-audit"], "web-quality-audit")
                self.assertIn("cloudflare-web-perf", routed["reused_engines"])

    def test_02_framework_recognition_in_router_and_analyzer(self):
        self.assertEqual(route("Auditoría completa de tienda Shopify Liquid")["framework"], "shopify-liquid")
        self.assertEqual(route("Diagnóstico técnico en Shopify Hydrogen Remix")["framework"], "shopify-hydrogen")
        self.assertEqual(route("Revisión general de calidad web en React Vite")["framework"], "react-web")
        self.assertEqual(route("Auditoría integral en Tiendanube Ipanema")["framework"], "tiendanube-ipanema")

        self.assertEqual(model.infer_framework(None, {"layout/theme.liquid": "{{ content_for_header }}"}), "shopify-liquid")
        self.assertEqual(model.infer_framework(None, {"app/routes/_index.tsx": "import {Image} from '@shopify/hydrogen'"}), "shopify-hydrogen")
        self.assertEqual(model.infer_framework(None, {"src/App.tsx": "export default function App(){}"}), "react-web")
        self.assertEqual(model.infer_framework(None, {"layouts/layout.tpl": "{% include 'snippets/image.tpl' %}"}), "tiendanube-ipanema")

    def test_03_on_demand_loading_without_redundant_skills(self):
        project = Project(ROOT, "ipanema")
        # 1. Pure performance request -> loads cloudflare-web-perf, NOT web-quality-audit
        perf_only = route("Analiza el rendimiento LCP, CLS y TTFB de esta tienda Shopify")
        self.assertIn("cloudflare-web-perf", perf_only["skills"])
        self.assertNotIn("web-quality-audit", perf_only["skills"])

        # 2. General quality audit request -> loads web-quality-audit, does NOT redundantly load cloudflare-web-perf
        quality_plan = planner.make_plan(
            project,
            "Revisión general de calidad web y buenas prácticas",
            files=["README.md"],
            scope="workspace",
            read_only=True,
        )
        self.assertIn("web-quality-audit", quality_plan["skills"])
        self.assertNotIn("cloudflare-web-perf", quality_plan["skills"])
        self.assertEqual(
            quality_plan["council_required_constraints"],
            ["accessibility", "performance", "responsive", "seo"],
        )
        ctx = engine.instruction_context(project, quality_plan)
        self.assertIn("web-quality-audit", ctx["skills"])
        self.assertNotIn("cloudflare-web-perf", ctx["skills"])

        # 3. Unrelated task -> loads neither
        unrelated_plan = planner.make_plan(project, "Corrige una errata", files=["README.md"], scope="workspace")
        unrelated_ctx = engine.instruction_context(project, unrelated_plan)
        self.assertNotIn("web-quality-audit", unrelated_ctx["skills"])
        self.assertNotIn("cloudflare-web-perf", unrelated_ctx["skills"])

    def test_04_reuses_cloudflare_web_perf_engine(self):
        with patch("ipanema.performance.model.diagnose_web_perf", wraps=model.diagnose_web_perf) as spy:
            report = model.audit_web_quality({})
            self.assertEqual(spy.call_count, 1)
            self.assertEqual(report["reused_engine"], "cloudflare-web-perf")
            self.assertEqual(report["performance_diagnosis"]["skill"], "cloudflare-web-perf")

    def test_05_detects_web_quality_issues_across_all_categories(self):
        fixtures = ROOT / "tests/fixtures/performance"
        psi_raw = json.loads((fixtures / "pagespeed-mobile.json").read_text())
        psi_obs = model.lighthouse(
            psi_raw,
            {"url": "https://example.invalid", "device": "mobile", "categories": ["performance"], "locale": "es"},
        )
        psi_obs["metrics"]["lcp"] = 4300  # poor LCP
        psi_obs["observations"]["audits"]["render-blocking-resources"] = {
            "score": 0,
            "details": {"items": [{"url": "https://example.invalid/app.css", "wastedMs": 420, "totalBytes": 60000}]},
        }
        rendered = {
            "title": "",
            "lang": "",
            "viewport": {"innerWidth": 390, "scrollHeight": 800, "scrollWidth": 480},
            "headings": [{"tag": "H2", "text": "Subtitulo sin H1"}],
            "metadata": [{"name": "robots", "content": "noindex, nofollow"}],
            "links": [
                {"href": "https://example.invalid/promo", "text": "click here", "ariaLabel": None},
                {"href": "https://example.invalid/icon", "text": "", "ariaLabel": ""},
            ],
            "images": [{"src": "https://example.invalid/banner.jpg", "currentSrc": "https://example.invalid/banner.jpg", "alt": None, "width": 390, "height": 200, "visible": True}],
            "forms": [{"action": "/search", "method": "get", "inputs": [{"tag": "INPUT", "type": "text", "name": "q", "hasLabel": False, "ariaLabel": None}]}],
            "jsonld": [{"component": "product", "error": "SyntaxError: Unexpected token"}],
            "performance": {"lcp": [{"tag": "IMG", "loading": "lazy", "fetchPriority": "low"}]},
        }
        network_records = [
            {"url": "http://insecure.example.invalid/script.js", "type": "Script", "status": 200, "encoded_bytes": 5000},
            {"url": "https://example.invalid/bundle.js.map", "type": "Other", "status": 200, "encoded_bytes": 90000},
        ]
        console_messages = [{"type": "error", "text": "Uncaught TypeError: Cannot read properties of undefined"}]

        result = model.audit_web_quality(
            {"sources": {"pagespeed": psi_obs}},
            network_records=network_records,
            rendered=rendered,
            console_messages=console_messages,
            framework="shopify-liquid",
        )
        ids = {issue["id"] for issue in result["verified_issues"]}
        self.assertIn("WQA-PERF-LAB-LCP", ids)
        self.assertIn("WQA-PERF-RENDER-BLOCKING", ids)
        self.assertIn("WQA-PERF-LCP-LAZY", ids)
        self.assertIn("WQA-A11Y-MISSING-LANG", ids)
        self.assertIn("WQA-A11Y-IMG-MISSING-ALT", ids)
        self.assertIn("WQA-A11Y-FORM-UNLABELED", ids)
        self.assertIn("WQA-SEO-MISSING-TITLE", ids)
        self.assertIn("WQA-SEO-MISSING-DESCRIPTION", ids)
        self.assertIn("WQA-SEO-MISSING-CANONICAL", ids)
        self.assertIn("WQA-SEO-NOINDEX-DETECTED", ids)
        self.assertIn("WQA-SEO-MISSING-H1", ids)
        self.assertIn("WQA-SEO-GENERIC-LINK-TEXT", ids)
        self.assertIn("WQA-SEO-INVALID-JSONLD", ids)
        self.assertIn("WQA-BP-CONSOLE-ERROR", ids)
        self.assertIn("WQA-BP-INSECURE-HTTP-RESOURCE", ids)
        self.assertIn("WQA-BP-EXPOSED-SOURCEMAP", ids)
        self.assertIn("WQA-INT-HORIZONTAL-OVERFLOW", ids)
        self.assertIn("WQA-INT-EMPTY-LINK", ids)
        self.assertEqual(result["framework"], "shopify-liquid")

    def test_06_separation_of_verified_evidence_and_code_hypotheses(self):
        source_files = {
            "layout/theme.liquid": (
                "<html><head><title>Tienda</title></head><body>"
                "<img src='hero.jpg'>"
                "<script>document.write('legacy');</script>"
                "<a href='http://external.example.invalid/item'>Item</a>"
                "<svg xmlns='http://www.w3.org/2000/svg'></svg>"
                "</body></html>"
            )
        }
        result = model.audit_web_quality({}, source_files=source_files)
        self.assertTrue(result["evidence_vs_hypothesis_separated"])
        self.assertEqual(result["counts"]["verified_by_tool"], 0)
        self.assertGreaterEqual(result["counts"]["code_hypothesis"], 5)
        self.assertTrue(all(h["evidence_type"] == "code_hypothesis" for h in result["code_hypotheses"]))
        h_ids = {h["id"] for h in result["code_hypotheses"]}
        self.assertIn("WQA-SRC-MISSING-DOCTYPE", h_ids)
        self.assertIn("WQA-SRC-MISSING-CHARSET", h_ids)
        self.assertIn("WQA-SRC-MISSING-VIEWPORT", h_ids)
        self.assertIn("WQA-SRC-IMG-WITHOUT-ALT", h_ids)
        self.assertIn("WQA-SRC-DOCUMENT-WRITE", h_ids)
        self.assertIn("WQA-SRC-INSECURE-HTTP-URL", h_ids)
        # Ensure standard SVG namespace http://www.w3.org was NOT flagged as insecure HTTP
        urls_flagged = [h["evidence"].get("url") for h in result["code_hypotheses"] if h["id"] == "WQA-SRC-INSECURE-HTTP-URL"]
        self.assertEqual(urls_flagged, ["http://external.example.invalid/item"])

    def test_07_protection_against_unauthorized_executions_and_secret_leaks(self):
        # 1. Secret redaction in evidence
        result = model.audit_web_quality(
            {},
            network_records=[{"url": "http://example.invalid/app.js?api_key=supersecret999", "type": "Script", "status": 200}],
        )
        self.assertNotIn("supersecret999", json.dumps(result))

        # 2. Outside --source-file rejected by CLI
        with tempfile.TemporaryDirectory() as tmp:
            outside_file = Path(tmp) / "outside.html"
            outside_file.write_text("<html></html>", encoding="utf-8")
            report_file = Path(tmp) / "report.json"
            report_file.write_text("{}", encoding="utf-8")
            run = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "tools/ia.py"),
                    "--project",
                    "ipanema",
                    "performance",
                    "quality-audit",
                    str(report_file),
                    "--source-file",
                    str(outside_file),
                ],
                capture_output=True,
                text=True,
                timeout=15,
            )
            self.assertEqual(run.returncode, 2)
            self.assertIn("fuera del alcance autorizado", run.stderr)

    def test_08_compatibility_with_existing_skills(self):
        project = Project(ROOT, "ipanema")
        val = validate(project)
        self.assertEqual(val["errors"], [])
        self.assertGreaterEqual(val["skills"], 11)

    def test_09_absence_of_regressions_in_coordinator_evals(self):
        project = Project(ROOT, "ipanema")
        eval_report = evaluate(project)
        self.assertEqual(eval_report["outcome"], "passed")

    def test_10_cli_quality_audit_subcommand(self):
        with tempfile.TemporaryDirectory() as tmp:
            report_file = Path(tmp) / "report.json"
            rendered_file = Path(tmp) / "rendered.json"
            report_file.write_text(json.dumps({}), encoding="utf-8")
            rendered_file.write_text(
                json.dumps({"title": "Demo", "lang": "es", "headings": [{"tag": "H1", "text": "Demo"}], "metadata": [{"name": "description", "content": "ok"}, {"name": "canonical", "href": "https://example.invalid/"}]}),
                encoding="utf-8",
            )
            run = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "tools/ia.py"),
                    "--project",
                    "ipanema",
                    "performance",
                    "quality-audit",
                    str(report_file),
                    "--rendered",
                    str(rendered_file),
                    "--framework",
                    "shopify-hydrogen",
                ],
                capture_output=True,
                text=True,
                timeout=15,
            )
            self.assertEqual(run.returncode, 0, run.stderr)
            out = json.loads(run.stdout)
            self.assertEqual(out["skill"], "web-quality-audit")
            self.assertEqual(out["reused_engine"], "cloudflare-web-perf")
            self.assertEqual(out["framework"], "shopify-hydrogen")
            self.assertEqual(out["counts"]["verified_by_tool"], 0)


if __name__ == "__main__":
    unittest.main()
