"""Etapa 6: Precheck de procedencia inmutable y 16 pruebas obligatorias para Vercel Web Design Guidelines (web-design-guidelines)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from support import ROOT, make_project
from ipanema.coordinator import AUTHORIZED_SKILLS, EXTERNAL_SKILLS, route
from ipanema.core import IpanemaError, Project, read_json
from ipanema.evals import evaluate as evaluate_coordinator
from ipanema.orchestration import engine, planner
from ipanema.performance import model
from ipanema.seo.evals import evaluate as evaluate_seo
from ipanema.validation import validate


def _git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("utf-8") + data).hexdigest()


class WebDesignGuidelinesIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix="ipanema-web-design-guidelines-")
        cls.root = make_project(Path(cls.tmp.name), theme=True)
        shutil.copytree(ROOT / "tools", cls.root / "tools", ignore=shutil.ignore_patterns("__pycache__"))
        cls.project = Project(cls.root)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_00_upstream_manifest_git_sha1_and_sha256_integrity(self):
        upstream_dir = ROOT / ".local/upstream/web-design-guidelines"
        manifest_path = upstream_dir / "manifest.json"
        if manifest_path.is_file():
            manifest = read_json(manifest_path)
            for item in manifest["sources"]:
                raw = (upstream_dir / item["file"]).read_bytes()
                self.assertEqual(_git_blob_sha1(raw), item["git_blob_sha1"])
                self.assertEqual(hashlib.sha256(raw).hexdigest(), item["sha256"])
                self.assertEqual(len(raw), item["bytes"])

    def test_01_authorized_registration_of_web_design_guidelines(self):
        skill_path = ROOT / ".agents/skills/web-design-guidelines/SKILL.md"
        self.assertTrue(skill_path.is_file())
        content = skill_path.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\nname: web-design-guidelines\n"))
        self.assertIn("1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62", content)
        self.assertIn("ceae92ab319216a68274168fba9b63b998b65997", content)
        self.assertIn("434b7f91364665f2f733b310ec54809bf8f37937", content)
        self.assertIn("3eb3a212b7b89493922ea418489d4c6f67ae8bd5", content)
        self.assertIn("MIT", content)
        self.assertIn("web-design-guidelines", AUTHORIZED_SKILLS)
        meta = EXTERNAL_SKILLS["web-design-guidelines"]
        self.assertEqual(meta["domain"], "ui-ux-design")
        self.assertEqual(meta["role"], "primary")
        self.assertFalse(meta["dynamic_fetch_enabled"])

    def test_02_correct_activation_for_design_ui_and_ux_requests(self):
        prompts = [
            "Revisa el diseño de una página de producto Shopify, identifica problemas de jerarquía visual, claridad de CTA, estados interactivos y diseño responsive, y prepara mejoras seguras",
            "Necesito una evaluación de UX, formularios y navegación del carrito",
            "Revisa los estados interactivos, hover y focus-visible de este componente",
            "Realiza una auditoría de diseño con web-design-guidelines",
        ]
        for p in prompts:
            with self.subTest(prompt=p):
                routed = route(p)
                self.assertIn("web-design-guidelines", routed["skills"])
                self.assertEqual(routed["primary_skills"]["ui-ux-design"], "web-design-guidelines")
                self.assertNotIn("seo-audit", routed["skills"])
                self.assertNotIn("schema", routed["skills"])

    def test_03_framework_and_project_detection(self):
        self.assertEqual(route("Revisa el diseño y jerarquía visual en Shopify Liquid")["framework"], "shopify-liquid")
        self.assertEqual(route("Audita UX y estados interactivos en Shopify Hydrogen")["framework"], "shopify-hydrogen")
        self.assertEqual(route("Revisa el diseño de formularios en Remix")["framework"], "remix")
        self.assertEqual(route("Audita consistencia visual en React Vite")["framework"], "react-web")
        self.assertEqual(route("Revisa jerarquía visual de tarjeta en Tiendanube Ipanema")["framework"], "tiendanube-ipanema")

    def test_04_on_demand_loading_in_orchestrator(self):
        repo_project = Project(ROOT, "ipanema")
        design_plan = planner.make_plan(
            repo_project,
            "Revisa el diseño, jerarquía visual y estados interactivos del componente",
            files=["README.md"],
            scope="workspace",
            read_only=True,
        )
        self.assertIn("web-design-guidelines", design_plan["skills"])
        self.assertEqual(design_plan["council_required_constraints"], ["accessibility", "responsive"])
        ctx = engine.instruction_context(repo_project, design_plan)
        self.assertIn("web-design-guidelines", ctx["skills"])
        self.assertNotIn("cloudflare-web-perf", ctx["skills"])
        self.assertNotIn("web-quality-audit", ctx["skills"])
        self.assertNotIn("seo-audit", ctx["skills"])
        self.assertNotIn("schema", ctx["skills"])
        self.assertNotIn("vercel-react-best-practices", ctx["skills"])

    def test_05_compatibility_with_previous_five_skills(self):
        # 1. Performance request remains routed to cloudflare-web-perf only
        r_perf = route("Analiza el LCP y los scripts que ralentizan una tienda Shopify")
        self.assertIn("cloudflare-web-perf", r_perf["skills"])
        self.assertNotIn("web-design-guidelines", r_perf["skills"])

        # 2. General quality request remains routed to web-quality-audit
        r_wqa = route("Realiza una revisión integral de una interfaz React")
        self.assertIn("web-quality-audit", r_wqa["skills"])
        self.assertNotIn("web-design-guidelines", r_wqa["skills"])

        # 3. SEO request remains routed to seo-audit
        r_seo = route("Audita el SEO técnico de una colección Shopify")
        self.assertIn("seo-audit", r_seo["skills"])
        self.assertNotIn("web-design-guidelines", r_seo["skills"])

        # 4. Schema request remains routed to schema
        r_sch = route("Revisa el JSON-LD de un producto Shopify")
        self.assertIn("schema", r_sch["skills"])
        self.assertNotIn("web-design-guidelines", r_sch["skills"])

        # 5. React hooks/waterfall request remains routed to vercel-react-best-practices
        r_react = route("Optimiza este componente React y refactoriza hooks useEffect para evitar renderizados innecesarios")
        self.assertIn("vercel-react-best-practices", r_react["skills"])
        self.assertNotIn("web-design-guidelines", r_react["skills"])

        # 6. audit_web_design_guidelines can reuse findings from a prior web-quality-audit report
        wqa_stub = {
            "skill": "web-quality-audit",
            "verified_issues": [
                {"id": "WQA-A11Y-FORM-UNLABELED", "category": "accessibility"},
                {"id": "WQA-INT-HORIZONTAL-OVERFLOW", "category": "interaction"},
            ],
        }
        res = model.audit_web_design_guidelines(
            {"sections/main-product.liquid": "<div>Producto</div>"},
            framework="shopify-liquid",
            quality_audit_report=wqa_stub,
        )
        self.assertIn("web-quality-audit", res["reused_engines"])
        self.assertEqual(res["reused_web_quality_findings"], ["WQA-A11Y-FORM-UNLABELED", "WQA-INT-HORIZONTAL-OVERFLOW"])

    def test_06_visual_hierarchy_and_cta_clarity_evaluation(self):
        rendered = {
            "headings": [
                {"tag": "H2", "text": "Subtítulo sin H1"},
                {"tag": "H4", "text": "Salto directo a H4"},
            ],
            "buttons": [
                {"id": "cta-main", "text": "Continue", "ariaLabel": None, "width": 160, "height": 48},
            ],
        }
        source = {
            "assets/product.css": ".product-price { font-size: 1.5rem; color: var(--color-primary); }\n",
            "sections/main-product.liquid": '<span>Loading...</span>\n',
        }
        res = model.audit_web_design_guidelines(source, rendered=rendered, framework="shopify-liquid")
        v_ids = {i["id"] for i in res["verified_by_tool"]}
        h_ids = {i["id"] for i in res["code_hypothesis"]}
        self.assertIn("WDG-VH-MISSING-PRIMARY-HEADING", v_ids)
        self.assertIn("WDG-VH-HEADING-LEVEL-SKIP", v_ids)
        self.assertIn("WDG-VH-AMBIGUOUS-CTA-LABEL", v_ids)
        self.assertIn("WDG-SRC-PRICE-MISSING-TABULAR-NUMS", h_ids)
        self.assertIn("WDG-SRC-STRAIGHT-ELLIPSIS", h_ids)

    def test_07_interactive_states_hover_focus_forms_and_animation_detection(self):
        source = {
            "src/ProductForm.tsx": (
                "export default function ProductForm() {\n"
                "  return (\n"
                "    <form>\n"
                "      <style>{`.btn { outline: none; transition: all 0.2s ease; @keyframes pulse { from { opacity: 1; } to { opacity: 0.5; } } }`}</style>\n"
                "      <div onClick={() => selectVariant('M')}>Talla M</div>\n"
                "      <input type='text' name='coupon' onPaste={(e) => e.preventDefault()} />\n"
                "      <button><svg viewBox='0 0 24 24'></svg></button>\n"
                "    </form>\n"
                "  );\n"
                "}\n"
            )
        }
        rendered = {
            "buttons": [{"id": "close-cart", "text": "", "ariaLabel": "", "width": 44, "height": 44}],
        }
        res = model.audit_web_design_guidelines(source, rendered=rendered, framework="react-web")
        v_ids = {i["id"] for i in res["verified_by_tool"]}
        h_ids = {i["id"] for i in res["code_hypothesis"]}
        self.assertIn("WDG-INT-ICON-BUTTON-MISSING-LABEL", v_ids)
        self.assertIn("WDG-SRC-OUTLINE-NONE-NO-FOCUS-VISIBLE", h_ids)
        self.assertIn("WDG-SRC-TRANSITION-ALL", h_ids)
        self.assertIn("WDG-SRC-NON-SEMANTIC-CLICK-HANDLER", h_ids)
        self.assertIn("WDG-SRC-PASTE-BLOCKED", h_ids)
        self.assertIn("WDG-SRC-ICON-BUTTON-MISSING-ARIA-LABEL", h_ids)
        self.assertIn("WDG-SRC-MISSING-PREFERS-REDUCED-MOTION", h_ids)

    def test_08_responsive_overflow_zoom_touch_targets_and_layout_reads(self):
        rendered = {
            "viewport": {"innerWidth": 390, "scrollWidth": 465, "scrollHeight": 900},
            "metadata": [{"name": "viewport", "content": "width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"}],
            "buttons": [{"id": "swatch-sm", "text": "S", "ariaLabel": "Talla S", "width": 28, "height": 28}],
        }
        source = {
            "src/Gallery.tsx": (
                "export function Gallery() {\n"
                "  const w = document.body.getBoundingClientRect().width;\n"
                "  return <input autoFocus aria-label='Buscar' />;\n"
                "}\n"
            )
        }
        res = model.audit_web_design_guidelines(source, rendered=rendered, framework="react-web")
        v_ids = {i["id"] for i in res["verified_by_tool"]}
        h_ids = {i["id"] for i in res["code_hypothesis"]}
        self.assertIn("WDG-RESP-HORIZONTAL-OVERFLOW", v_ids)
        self.assertIn("WDG-RESP-ZOOM-DISABLED", v_ids)
        self.assertIn("WDG-RESP-SMALL-TOUCH-TARGET", v_ids)
        self.assertIn("WDG-SRC-LAYOUT-READ-IN-UI", h_ids)
        self.assertIn("WDG-SRC-UNRESTRICTED-AUTOFOCUS", h_ids)

    def test_09_ecommerce_components_pdp_cart_drawer_forms_and_images(self):
        rendered = {
            "forms": [{"action": "/cart/add", "inputs": [{"name": "quantity", "type": "number", "hasLabel": False, "ariaLabel": None}]}],
            "images": [{"src": "https://example.invalid/pdp.jpg", "width": None, "height": None, "visible": True}],
        }
        source = {
            "snippets/cart-drawer.liquid": (
                "<div class='cart-drawer js-cart-drawer' data-store='cart-drawer'>\n"
                "  <img src='{{ item.image | image_url }}'>\n"
                "  <input type='number' name='updates[]'>\n"
                "</div>\n"
            )
        }
        res = model.audit_web_design_guidelines(source, rendered=rendered, framework="shopify-liquid")
        v_ids = {i["id"] for i in res["verified_by_tool"]}
        h_ids = {i["id"] for i in res["code_hypothesis"]}
        self.assertIn("WDG-ECOM-FORM-UNLABELED-CONTROL", v_ids)
        self.assertIn("WDG-ECOM-IMG-MISSING-DIMENSIONS", v_ids)
        self.assertIn("WDG-SRC-DRAWER-MISSING-OVERSCROLL-CONTAIN", h_ids)
        self.assertIn("WDG-SRC-IMG-MISSING-DIMENSIONS", h_ids)
        self.assertIn("WDG-SRC-INPUT-MISSING-LABEL", h_ids)

    def test_10_preservation_of_brand_identity_design_tokens_and_commerce_contracts(self):
        source = {
            "sections/main-product.liquid": (
                "<style>.pdp-title { color: var(--color-heading); font-family: var(--font-heading); background: #ff0055; }</style>\n"
                "<form action='/cart/add' method='post' class='js-product-form' data-store='product-form'>\n"
                "  <button type='submit' class='js-add-to-cart'>Agregar al carrito</button>\n"
                "</form>\n"
            )
        }
        res = model.audit_web_design_guidelines(source, framework="shopify-liquid")
        guards = res["brand_and_commerce_guards"]
        self.assertTrue(guards["preserve_brand_identity"])
        self.assertTrue(guards["arbitrary_redesign_prohibited"])
        self.assertIn("--color-heading", guards["detected_css_variables"])
        self.assertIn("--font-heading", guards["detected_css_variables"])
        contracts = guards["protected_commerce_contracts"][0]["contracts"]
        self.assertIn("/cart/add", contracts)
        self.assertIn("js-product-form", contracts)
        self.assertIn("data-store", contracts)
        h_ids = {i["id"] for i in res["code_hypothesis"]}
        self.assertIn("WDG-SRC-HARDCODED-COLOR-BYPASSING-TOKENS", h_ids)

    def test_11_strict_separation_of_evidence_hypotheses_and_external_verification(self):
        res_static = model.audit_web_design_guidelines(
            {"sections/hero.liquid": "<img src='hero.jpg'>"},
            rendered=None,
            framework="shopify-liquid",
        )
        self.assertEqual(res_static["counts"]["verified_by_tool"], 0)
        self.assertGreaterEqual(res_static["counts"]["code_hypothesis"], 1)
        self.assertGreaterEqual(res_static["counts"]["requires_external_verification"], 1)
        self.assertTrue(all(x["evidence_type"] == "code_hypothesis" for x in res_static["code_hypothesis"]))
        self.assertTrue(all(x["evidence_type"] == "requires_external_verification" for x in res_static["requires_external_verification"]))

    def test_12_no_dynamic_fetching_and_security_protection(self):
        res = model.audit_web_design_guidelines(
            {"src/App.tsx": "<a href='https://example.invalid/checkout?api_key=secret_design_999'>Checkout</a>"},
            framework="react-web",
        )
        self.assertFalse(res["rules_source"]["dynamic_fetch_performed"])
        self.assertEqual(res["rules_source"]["rules_commit"], "434b7f91364665f2f733b310ec54809bf8f37937")
        self.assertNotIn("secret_design_999", json.dumps(res))

        with tempfile.TemporaryDirectory() as tmp:
            outside = Path(tmp) / "outside.liquid"
            outside.write_text("<div>Outside</div>", encoding="utf-8")
            run = subprocess.run(
                [
                    sys.executable,
                    str(self.root / "tools/ia.py"),
                    "--project",
                    "sample",
                    "performance",
                    "design-audit",
                    "--source-file",
                    str(outside),
                ],
                capture_output=True,
                text=True,
                timeout=15,
            )
            self.assertEqual(run.returncode, 2)
            self.assertIn("fuera del alcance autorizado", run.stderr)

    def test_13_preservation_of_b1_b2_and_council_policy(self):
        models_cfg = read_json(ROOT / "tools/ipanema/orchestration/models.json")
        self.assertEqual(models_cfg["council"]["members"], ["claude", "codex"])
        self.assertIn("commandcode", models_cfg["council"]["disabled"])
        self.assertNotIn("antigravity", models_cfg["council"]["members"])

    def test_14_absence_of_regressions_across_all_suites(self):
        repo_project = Project(ROOT, "ipanema")
        val = validate(repo_project)
        self.assertEqual(val["errors"], [])
        self.assertGreaterEqual(val["skills"], 15)
        self.assertEqual(evaluate_coordinator(repo_project)["outcome"], "passed")
        self.assertEqual(evaluate_seo()["outcome"], "passed")

    def test_15_cli_design_audit_execution_and_section_9_pdp_functional_test(self):
        pdp_file = self.root / "main-product.liquid"
        pdp_file.write_text(
            "<style>.pdp-btn { outline: none; transition: all 0.2s; } .pdp-price { color: var(--color-primary); }</style>\n"
            "<div class='pdp-gallery'><img src='{{ product.featured_image | image_url }}'></div>\n"
            "<form action='/cart/add' method='post' class='js-product-form' data-store='product-form'>\n"
            "  <div onClick='selectVariant(1)'>Talla Única</div>\n"
            "  <input type='number' name='quantity' value='1'>\n"
            "  <button type='submit'>Continue</button>\n"
            "</form>\n",
            encoding="utf-8",
        )
        rendered_file = self.root / "rendered-pdp.json"
        rendered_file.write_text(
            json.dumps({
                "viewport": {"innerWidth": 390, "scrollWidth": 430},
                "headings": [{"tag": "H2", "text": "Producto sin H1"}],
                "buttons": [{"id": "buy-btn", "text": "Continue", "ariaLabel": None, "width": 120, "height": 36}],
                "forms": [{"action": "/cart/add", "inputs": [{"name": "quantity", "type": "number", "hasLabel": False, "ariaLabel": None}]}],
                "images": [{"src": "https://example.invalid/pdp.jpg", "width": None, "height": None, "visible": True}],
            }),
            encoding="utf-8",
        )
        run = subprocess.run(
            [
                sys.executable,
                str(self.root / "tools/ia.py"),
                "--project",
                "sample",
                "performance",
                "design-audit",
                "--source-file",
                str(pdp_file),
                "--rendered",
                str(rendered_file),
                "--framework",
                "shopify-liquid",
            ],
            capture_output=True,
            text=True,
            timeout=15,
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        out = json.loads(run.stdout)
        self.assertEqual(out["kind"], "web-design-guidelines-audit")
        self.assertEqual(out["skill"], "web-design-guidelines")
        self.assertEqual(out["framework"], "shopify-liquid")
        self.assertFalse(out["rules_source"]["dynamic_fetch_performed"])
        self.assertGreaterEqual(out["counts"]["verified_by_tool"], 5)
        self.assertGreaterEqual(out["counts"]["code_hypothesis"], 5)
        self.assertTrue(len(out["terse_file_line_findings"]) >= 5)


if __name__ == "__main__":
    unittest.main()
