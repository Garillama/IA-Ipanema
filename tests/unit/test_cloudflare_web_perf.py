"""Etapa D: Pruebas de estructura, activación, herramientas, funcionalidad, regresión y seguridad de cloudflare-web-perf."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from support import ROOT, make_project
from ipanema.coordinator import AUTHORIZED_SKILLS, EXTERNAL_SKILLS, detect_context, plan, route
from ipanema.core import IpanemaError, Project
from ipanema.orchestration import engine, planner
from ipanema.performance import model
from ipanema.validation import validate


class CloudflareWebPerfIntegrationTests(unittest.TestCase):
    def test_1_structure_and_configuration_validation(self):
        skill_path = ROOT / ".agents/skills/cloudflare-web-perf/SKILL.md"
        self.assertTrue(skill_path.is_file())
        content = skill_path.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\nname: cloudflare-web-perf\n"))
        self.assertIn("description:", content)
        self.assertIn("5108325ecceabc899c761e07aa617b09c02445ee", content)
        self.assertIn("Apache-2.0", content)
        self.assertIn("cloudflare-web-perf", AUTHORIZED_SKILLS)
        self.assertEqual(EXTERNAL_SKILLS["cloudflare-web-perf"]["role"], "primary")
        self.assertEqual(EXTERNAL_SKILLS["cloudflare-web-perf"]["domain"], "performance")
        project = Project(ROOT, "ipanema")
        report = validate(project)
        self.assertEqual(report["errors"], [])
        self.assertGreaterEqual(report["skills"], 10)

    def test_2_skill_activation_and_framework_detection(self):
        shopify_prompt = (
            "Analiza el rendimiento de esta tienda Shopify, encuentra sus principales problemas, "
            "implementa las mejoras permitidas y comprueba qué cambió"
        )
        routed_shopify = route(shopify_prompt)
        self.assertIn("cloudflare-web-perf", routed_shopify["skills"])
        self.assertEqual(routed_shopify["skills"][0], "cloudflare-web-perf")
        self.assertEqual(routed_shopify["primary_skills"]["performance"], "cloudflare-web-perf")
        self.assertEqual(routed_shopify["framework"], "shopify-liquid")

        hydrogen_prompt = "Audit Core Web Vitals LCP CLS INP and TTFB waterfall on Shopify Hydrogen"
        routed_hydrogen = route(hydrogen_prompt)
        self.assertIn("cloudflare-web-perf", routed_hydrogen["skills"])
        self.assertEqual(routed_hydrogen["framework"], "shopify-hydrogen")

        react_prompt = "Optimize render-blocking CSS and tree-shaking bundle in React Vite app"
        routed_react = route(react_prompt)
        self.assertIn("cloudflare-web-perf", routed_react["skills"])
        self.assertEqual(routed_react["framework"], "react-web")

        # Non-performance task must NOT activate cloudflare-web-perf (on-demand loading)
        non_perf = route("Corrige el H1 duplicado de una página de producto")
        self.assertNotIn("cloudflare-web-perf", non_perf["skills"])

    def test_3_on_demand_loading_and_tool_selection_in_orchestrator(self):
        project = Project(ROOT, "ipanema")
        perf_plan = planner.make_plan(
            project,
            "Optimiza LCP y recursos bloqueantes en hero",
            files=["sections/hero.tpl"],
            scope="theme",
        )
        self.assertIn("cloudflare-web-perf", perf_plan["skills"])
        self.assertIn("performance", perf_plan["council_required_constraints"])
        ctx = engine.instruction_context(project, perf_plan)
        self.assertIn("cloudflare-web-perf", ctx["skills"])
        self.assertIn("LCPBreakdown", ctx["skills"]["cloudflare-web-perf"])

        # Non-performance workspace plan does not load cloudflare-web-perf into context
        simple_plan = planner.make_plan(
            project,
            "Corrige una errata",
            files=["README.md"],
            scope="workspace",
        )
        self.assertNotIn("cloudflare-web-perf", simple_plan["skills"])
        simple_ctx = engine.instruction_context(project, simple_plan)
        self.assertNotIn("cloudflare-web-perf", simple_ctx["skills"])

    def test_4_functional_cwv_thresholds_and_field_vs_lab_separation(self):
        self.assertEqual(model.rate_metric("ttfb", 650), "good")
        self.assertEqual(model.rate_metric("ttfb", 1200), "needs-improvement")
        self.assertEqual(model.rate_metric("ttfb", 2100), "poor")
        self.assertEqual(model.rate_metric("lcp", 2400), "good")
        self.assertEqual(model.rate_metric("lcp", 3100), "needs-improvement")
        self.assertEqual(model.rate_metric("lcp", 4500), "poor")
        self.assertEqual(model.rate_metric("inp", 180), "good")
        self.assertEqual(model.rate_metric("inp", 350), "needs-improvement")
        self.assertEqual(model.rate_metric("inp", 600), "poor")
        self.assertEqual(model.rate_metric("cls", 0.05), "good")
        self.assertEqual(model.rate_metric("cls", 0.18), "needs-improvement")
        self.assertEqual(model.rate_metric("cls", 0.32), "poor")
        self.assertEqual(model.rate_metric("tbt", None), "not_measured")

        fixtures = ROOT / "tests/fixtures/performance"
        psi_raw = json.loads((fixtures / "pagespeed-mobile.json").read_text())
        crux_raw = json.loads((fixtures / "crux-mobile.json").read_text())

        psi_obs = model.lighthouse(
            psi_raw,
            {"url": "https://example.invalid", "device": "mobile", "categories": ["performance"], "locale": "es"},
        )
        psi_obs["observations"]["audits"]["server-response-time"] = {"numericValue": 920}
        psi_obs["observations"]["audits"]["render-blocking-resources"] = {
            "score": 0,
            "details": {
                "items": [
                    {"url": "https://example.invalid/assets/theme.css?token=secret123", "wastedMs": 340, "totalBytes": 85000},
                    {"url": "https://example.invalid/assets/reset.css", "wastedMs": 0, "totalBytes": 1200},
                ]
            },
        }
        psi_obs["observations"]["audits"]["lcp-breakdown-insight"] = {
            "score": 0,
            "details": {"items": [{"ttfb": 920, "resourceLoadDelay": 180, "resourceLoadDuration": 850, "elementRenderDelay": 450}]},
        }
        crux_obs = model.crux(
            crux_raw,
            {"source": "crux", "scope": "url", "url": "https://example.invalid", "origin": "https://example.invalid", "form_factor": "PHONE"},
        )

        network_records = [
            {"url": "https://example.invalid/start", "type": "Document", "status": 301, "redirect": True, "redirect_hop": 0, "encoded_bytes": 200},
            {"url": "https://example.invalid/", "type": "Document", "status": 200, "redirect_hop": 1, "encoded_bytes": 18000},
            {"url": "https://cdn.example.invalid/app.js", "type": "Script", "status": 200, "redirect_hop": 0, "encoded_bytes": 220000},
            {"url": "https://cdn.example.invalid/app.js", "type": "Script", "status": 200, "redirect_hop": 0, "encoded_bytes": 220000},
        ]
        rendered = {
            "performance": {
                "lcp": [{"tag": "IMG", "id": "hero-img", "loading": "lazy", "fetchPriority": "auto", "currentSrc": "https://example.invalid/hero.jpg"}]
            },
            "images": [
                {"currentSrc": "https://example.invalid/hero.jpg", "width": 390, "height": 0, "naturalWidth": 1920, "visible": True, "srcset": "", "sizes": None}
            ],
        }

        diag = model.diagnose_web_perf(
            {"sources": {"pagespeed": psi_obs, "crux": crux_obs}},
            network_records=network_records,
            rendered=rendered,
            preconnect_origins=["https://cdn.example.invalid", "https://unused-fonts.example.invalid"],
        )

        self.assertTrue(diag["field_vs_lab_separated"])
        self.assertEqual(diag["field_metrics"]["inp"]["value"], 190.0)
        self.assertEqual(diag["field_metrics"]["inp"]["rating"], "good")
        self.assertNotIn("inp", diag["lab_metrics"])
        self.assertEqual(diag["lab_metrics"]["ttfb"]["value"], 920.0)
        self.assertEqual(diag["lab_metrics"]["ttfb"]["rating"], "needs-improvement")
        self.assertEqual(diag["lab_metrics"]["lcp"]["value"], 2400.0)
        self.assertEqual(diag["lab_metrics"]["lcp"]["rating"], "good")

        # 0ms render-blocking resource skipped, >0ms retained and sanitized
        self.assertEqual(len(diag["render_blocking"]["actionable"]), 1)
        self.assertEqual(diag["render_blocking"]["actionable"][0]["wasted_ms"], 340.0)
        self.assertEqual(len(diag["render_blocking"]["zero_impact_skipped"]), 1)
        self.assertNotIn("secret123", json.dumps(diag))

        # Duplicate resources, redirects, large payloads, unused preconnects
        self.assertEqual(diag["network"]["duplicate_resources"], [{"url": "https://cdn.example.invalid/app.js", "count": 2}])
        self.assertEqual(len(diag["network"]["redirects"]), 2)
        self.assertEqual(diag["network"]["large_resources"][0]["encoded_bytes"], 220000.0)
        self.assertEqual(diag["network"]["unused_preconnects"], ["https://unused-fonts.example.invalid"])
        self.assertEqual(diag["network"]["verified_preconnects"], ["https://cdn.example.invalid"])
        self.assertEqual(diag["network"]["lcp_breakdown"]["ttfb"], 920)

        # Responsive image & LCP loading priority diagnostics
        self.assertTrue(diag["images"]["lcp_lazy_loaded"])
        self.assertTrue(diag["images"]["lcp_missing_high_priority"])
        self.assertEqual(len(diag["images"]["unsized_images"]), 1)
        self.assertEqual(len(diag["images"]["oversized_images"]), 1)

    def test_5_regression_and_before_after_comparison_and_cli_diagnose(self):
        # Verify risk level classification regression: 2 domain specialties remain L1 for single file
        level_two_domains = planner.classify(
            "Evita descargar imágenes mobile cuando se muestra desktop; comprueba las solicitudes reales.",
            ["snippets/image.tpl"],
        )
        self.assertEqual(level_two_domains["level"], "L1")

        # Verify CLI performance diagnose runs offline and compares before/after accurately
        fixtures = ROOT / "tests/fixtures/performance"
        psi_raw = json.loads((fixtures / "pagespeed-mobile.json").read_text())
        before = model.lighthouse(
            psi_raw,
            {"url": "https://example.invalid", "device": "mobile", "categories": ["performance"], "locale": "es"},
        )
        after = copy.deepcopy(before)
        after["metrics"]["lcp"] = 1850
        after["measured_at"] = "2026-11-18T12:00:00Z"
        comparison = model.compare(before, after)
        self.assertEqual(comparison["status"], "compared")
        self.assertEqual(comparison["delta_after_minus_before"]["lcp"], -550)

        with tempfile.TemporaryDirectory() as tmp:
            report_file = Path(tmp) / "report.json"
            report_file.write_text(json.dumps({"sources": {"pagespeed": before}}), encoding="utf-8")
            run = subprocess.run(
                [sys.executable, str(ROOT / "tools/ia.py"), "--project", "ipanema", "performance", "diagnose", str(report_file)],
                capture_output=True,
                text=True,
                timeout=15,
            )
            self.assertEqual(run.returncode, 0, run.stderr)
            out = json.loads(run.stdout)
            self.assertEqual(out["skill"], "cloudflare-web-perf")
            self.assertEqual(out["lab_metrics"]["lcp"]["value"], 2400.0)

    def test_6_security_controls_and_skill_boundaries(self):
        project = Project(ROOT, "ipanema")
        bad_plan = {"skills": ["unregistered-external-skill"]}
        with self.assertRaises(IpanemaError):
            engine.instruction_context(project, bad_plan)
        traversal_plan = {"skills": ["../outside"]}
        with self.assertRaises(IpanemaError):
            engine.instruction_context(project, traversal_plan)
        # Ensure SKILL.md explicitly forbids npx -y chrome-devtools-mcp@latest execution
        skill_text = (ROOT / ".agents/skills/cloudflare-web-perf/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("No ejecutes `npx -y chrome-devtools-mcp@latest`", skill_text)


if __name__ == "__main__":
    unittest.main()
