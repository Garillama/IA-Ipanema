"""Etapa 5: Preflight conjunto de las 4 skills (Casos A–F) y 14 pruebas obligatorias de Vercel React Best Practices."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from support import ROOT, make_project
from ipanema.coordinator import AUTHORIZED_SKILLS, EXTERNAL_SKILLS, plan, route
from ipanema.core import IpanemaError, Project, read_json
from ipanema.evals import evaluate as evaluate_coordinator
from ipanema.orchestration import engine, planner
from ipanema.performance import model
from ipanema.seo.evals import evaluate as evaluate_seo
from ipanema.seo.page_audit import comprehensive_seo_audit
from ipanema.seo.schema_validator import audit_and_propose_schema
from ipanema.validation import validate


class VercelReactBestPracticesIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix="ipanema-vercel-react-skill-")
        cls.root = make_project(Path(cls.tmp.name), theme=True)
        shutil.copytree(ROOT / "tools", cls.root / "tools", ignore=shutil.ignore_patterns("__pycache__"))
        cls.project = Project(cls.root)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_00_preflight_joint_4_skills_cases_a_to_f_and_b1_b2_unchanged(self):
        # Caso A — Rendimiento
        ra = route("Analiza el LCP y los scripts que ralentizan una tienda Shopify")
        self.assertIn("cloudflare-web-perf", ra["skills"])
        for other in ("web-quality-audit", "seo-audit", "schema", "vercel-react-best-practices"):
            self.assertNotIn(other, ra["skills"])
        perf_diag = model.diagnose_web_perf({})
        self.assertTrue(perf_diag["field_vs_lab_separated"])

        # Caso B — Calidad web
        rb = route("Realiza una auditoría integral de calidad de esta página")
        self.assertIn("web-quality-audit", rb["skills"])
        for other in ("cloudflare-web-perf", "seo-audit", "schema", "vercel-react-best-practices"):
            self.assertNotIn(other, rb["skills"])
        self.assertIn("cloudflare-web-perf", rb["reused_engines"])
        wqa = model.audit_web_quality({}, rendered={"title": "", "lang": ""})
        self.assertEqual(wqa["reused_engine"], "cloudflare-web-perf")
        self.assertGreater(wqa["counts"]["verified_by_tool"], 0)

        # Caso C — SEO
        rc = route("Audita el SEO técnico de una colección Shopify")
        self.assertIn("seo-audit", rc["skills"])
        for other in ("cloudflare-web-perf", "web-quality-audit", "schema", "vercel-react-best-practices"):
            self.assertNotIn(other, rc["skills"])
        seo_rep = comprehensive_seo_audit(self.project, "<html><head></head><body></body></html>", "https://example.invalid/collections/all", "category")
        self.assertFalse(seo_rep["indexation_claimed"])

        # Caso D — Datos estructurados
        rd = route("Revisa el JSON-LD de un producto Shopify")
        self.assertIn("schema", rd["skills"])
        for other in ("cloudflare-web-perf", "web-quality-audit", "seo-audit", "vercel-react-best-practices"):
            self.assertNotIn(other, rd["skills"])
        sch_rep = audit_and_propose_schema(
            self.project,
            "<html><head><script type='application/ld+json' data-component='judgeme-app'>{\"@context\":\"https://schema.org\",\"@type\":\"Product\",\"name\":\"P\"}</script></head><body><h1>P</h1></body></html>",
            "https://example.invalid/products/p",
            "product",
        )
        self.assertFalse(sch_rep["inventory"]["json_ld_blocks"][0]["auto_modify_allowed"])

        # Caso E — Solicitud ambigua
        re_amb = route("Optimiza mi tienda Shopify")
        self.assertEqual(re_amb["external_skills"], [])
        self.assertEqual(re_amb["skills"], ["ipanema-architect"])
        pe_amb = plan(Project(ROOT, "ipanema"), "Optimiza mi tienda Shopify")
        self.assertFalse(pe_amb["implementation_executed"])

        # Caso F — Seguridad y preservación de bloqueos B1/B2 / Council
        models_cfg = read_json(ROOT / "tools/ipanema/orchestration/models.json")
        self.assertEqual(models_cfg["council"]["members"], ["claude", "codex"])
        self.assertIn("commandcode", models_cfg["council"]["disabled"])
        self.assertNotIn("antigravity", models_cfg["council"]["members"])
        with self.assertRaises(IpanemaError):
            engine.instruction_context(Project(ROOT, "ipanema"), {"skills": ["../outside"]})

    def test_01_authorized_registration_of_vercel_react_best_practices(self):
        skill_path = ROOT / ".agents/skills/vercel-react-best-practices/SKILL.md"
        self.assertTrue(skill_path.is_file())
        content = skill_path.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\nname: vercel-react-best-practices\n"))
        self.assertIn("1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62", content)
        self.assertIn("237988de4a66dd8a71d30a2c24ebe1a86b58d04e", content)
        self.assertIn("MIT", content)
        self.assertIn("vercel-react-best-practices", AUTHORIZED_SKILLS)
        meta = EXTERNAL_SKILLS["vercel-react-best-practices"]
        self.assertEqual(meta["domain"], "react")
        self.assertEqual(meta["role"], "primary")

    def test_02_correct_detection_of_react_hydrogen_remix_and_nextjs(self):
        self.assertEqual(route("Optimiza este componente React y sus hooks")["framework"], "react-web")
        self.assertEqual(route("Revisión de rendimiento de Hydrogen en loaders")["framework"], "shopify-hydrogen")
        self.assertEqual(route("Refactorización de hooks y loaders en Remix")["framework"], "remix")
        self.assertEqual(route("Reducción de bundle con next/dynamic en Next.js")["framework"], "nextjs")

        self.assertEqual(model.infer_framework(None, {"app/routes/products.$handle.tsx": "import {useLoaderData} from '@remix-run/react'; import {Image} from '@shopify/hydrogen';"}), "shopify-hydrogen")
        self.assertEqual(model.infer_framework(None, {"app/routes/_index.tsx": "import {json} from '@remix-run/node'; export async function loader(){}"}), "remix")
        self.assertEqual(model.infer_framework(None, {"app/page.tsx": "import dynamic from 'next/dynamic';"}), "nextjs")
        self.assertEqual(model.infer_framework(None, {"src/ProductCard.tsx": "import React from 'react';"}), "react-web")

    def test_03_no_activation_in_shopify_liquid_without_react(self):
        liquid_prompts = [
            "Optimiza las imágenes y CSS de mi tema Shopify Liquid",
            "Analiza el rendimiento de esta tienda Shopify, encuentra sus principales problemas",
            "Audita el SEO técnico de sections/main-product.liquid en Shopify",
            "Revisa el JSON-LD en snippets/product-schema.liquid de Shopify",
        ]
        for prompt in liquid_prompts:
            with self.subTest(prompt=prompt):
                routed = route(prompt)
                self.assertNotIn("vercel-react-best-practices", routed["skills"])

        liquid_audit = model.audit_react_best_practices(
            {"sections/main-product.liquid": "{{ content_for_header }}<div>{{ product.title }}</div>"},
            framework="shopify-liquid",
        )
        self.assertFalse(liquid_audit["applicable"])
        self.assertEqual(liquid_audit["findings"], [])

    def test_04_on_demand_loading_in_orchestrator(self):
        repo_project = Project(ROOT, "ipanema")
        react_plan = planner.make_plan(
            repo_project,
            "Optimiza un componente React y refactoriza hooks useEffect para evitar renderizados innecesarios",
            files=["README.md"],
            scope="workspace",
            read_only=True,
        )
        self.assertIn("vercel-react-best-practices", react_plan["skills"])
        self.assertEqual(react_plan["council_required_constraints"], ["performance"])
        ctx = engine.instruction_context(repo_project, react_plan)
        self.assertIn("vercel-react-best-practices", ctx["skills"])
        self.assertNotIn("cloudflare-web-perf", ctx["skills"])
        self.assertNotIn("web-quality-audit", ctx["skills"])
        self.assertNotIn("seo-audit", ctx["skills"])
        self.assertNotIn("schema", ctx["skills"])

    def test_05_compatibility_and_evidence_sharing_with_previous_four_skills(self):
        # Combined measured CWV + Hydrogen React optimization activates both cloudflare-web-perf and vercel-react-best-practices
        combined = route("Mide LCP y TTFB con Lighthouse y elimina waterfalls en componentes React de Hydrogen")
        self.assertIn("cloudflare-web-perf", combined["skills"])
        self.assertIn("vercel-react-best-practices", combined["skills"])
        self.assertIn("cloudflare-web-perf", combined["reused_engines"])

        # And audit_react_best_practices can consume a cloudflare-web-perf report without re-measuring
        perf_stub = {
            "skill": "cloudflare-web-perf",
            "lab_metrics": {"tbt": {"value": 450, "unit": "ms", "rating": "needs-improvement"}},
            "field_metrics": {"inp": {"value": 280, "unit": "ms", "rating": "needs-improvement"}},
            "network": {"large_resources": [{"url": "https://example.invalid/bundle.js", "encoded_bytes": 320000}]},
        }
        res = model.audit_react_best_practices(
            {"src/App.tsx": "export default function App(){ return <div />; }"},
            framework="react-web",
            perf_report=perf_stub,
        )
        self.assertEqual(res["reused_engines"], ["cloudflare-web-perf"])
        self.assertEqual(res["performance_correlation"]["large_resources_count"], 1)

    def test_06_waterfall_detection_sequential_awaits_and_effect_fetch(self):
        code = """
        import {useEffect} from 'react';
        export async function loader({context}) {
          const product = await context.storefront.query(PRODUCT_QUERY);
          const recommendations = await context.storefront.query(RECOMMENDATIONS_QUERY);
          return {product, recommendations};
        }
        export default function ProductPage() {
          useEffect(() => {
            fetch('/api/reviews').then(r => r.json());
          }, []);
          return <div />;
        }
        """
        result = model.audit_react_best_practices({"app/routes/products.$handle.tsx": code}, framework="shopify-hydrogen")
        ids = {f["id"] for f in result["findings"]}
        self.assertIn("RBP-ASYNC-SEQUENTIAL-WATERFALL", ids)
        self.assertIn("RBP-ASYNC-EFFECT-FETCH-WATERFALL", ids)

    def test_07_bundle_splitting_and_barrel_import_detection(self):
        code = """
        import _ from 'lodash';
        import * as Icons from 'lucide-react';
        import HeavyProductModal from './components/HeavyProductModal';
        export default function Catalog() {
          return <HeavyProductModal />;
        }
        """
        result = model.audit_react_best_practices({"src/Catalog.tsx": code}, framework="react-web")
        ids = {f["id"] for f in result["findings"]}
        self.assertIn("RBP-BUNDLE-BARREL-IMPORT", ids)
        self.assertIn("RBP-BUNDLE-DYNAMIC-IMPORT", ids)

    def test_08_unnecessary_rerenders_inline_components_and_hooks_review(self):
        code = """
        import {useState, useEffect} from 'react';
        let sharedCustomerSession = null;
        export default function CartDrawer({items, selectedIds}) {
          const [saved, setSaved] = useState(JSON.parse(localStorage.getItem('cart') || '{}'));
          const [total, setTotal] = useState(0);
          useEffect(() => {
            setTotal(items.length);
          }, [items]);
          function InlineItemRow({item}) {
            return <li>{item.name}</li>;
          }
          window.addEventListener('scroll', onScroll);
          const active = items.filter(item => selectedIds.includes(item.id));
          return <div>{items.length && <InlineItemRow item={active[0]} />}</div>;
        }
        """
        result = model.audit_react_best_practices({"app/components/CartDrawer.tsx": code}, framework="shopify-hydrogen")
        ids = {f["id"] for f in result["findings"]}
        self.assertIn("RBP-SERVER-SHARED-MODULE-STATE", ids)
        self.assertIn("RBP-RERENDER-LAZY-STATE-INIT", ids)
        self.assertIn("RBP-RERENDER-DERIVED-STATE-EFFECT", ids)
        self.assertIn("RBP-RERENDER-INLINE-COMPONENT", ids)
        self.assertIn("RBP-RENDERING-AND-ZERO-LEAK", ids)
        self.assertIn("RBP-JS-SET-MAP-LOOKUP", ids)
        self.assertIn("RBP-CLIENT-PASSIVE-LISTENER", ids)

    def test_09_framework_compatibility_of_recommendations_hydrogen_vs_nextjs(self):
        # Using next/dynamic inside a Shopify Hydrogen route must be flagged as incompatible
        hydrogen_code = """
        import dynamic from 'next/dynamic';
        import HeavyChart from './HeavyChart';
        export default function HydrogenRoute() { return <HeavyChart />; }
        """
        h_res = model.audit_react_best_practices({"app/routes/_index.tsx": hydrogen_code}, framework="shopify-hydrogen")
        h_ids = {f["id"] for f in h_res["findings"]}
        self.assertIn("RBP-FW-INCOMPATIBLE-NEXT-API", h_ids)
        dyn_finding_h = next(f for f in h_res["findings"] if f["id"] == "RBP-BUNDLE-DYNAMIC-IMPORT")
        self.assertIn("React.lazy", dyn_finding_h["fix"])
        self.assertIn("no usar `next/dynamic`", dyn_finding_h["fix"])

        # In Next.js, next/dynamic IS recommended and NOT flagged as incompatible
        next_code = """
        import HeavyChart from './HeavyChart';
        export default function NextPage() { return <HeavyChart />; }
        """
        n_res = model.audit_react_best_practices({"app/page.tsx": next_code}, framework="nextjs")
        n_ids = {f["id"] for f in n_res["findings"]}
        self.assertNotIn("RBP-FW-INCOMPATIBLE-NEXT-API", n_ids)
        dyn_finding_n = next(f for f in n_res["findings"] if f["id"] == "RBP-BUNDLE-DYNAMIC-IMPORT")
        self.assertIn("next/dynamic", dyn_finding_n["fix"])

    def test_10_protection_of_functional_and_commercial_behavior(self):
        commerce_code = """
        import {CartForm, useOptimisticCart} from '@shopify/hydrogen';
        export async function action({context}) {
          const res = await context.cart.cartLinesAdd([]);
          return res;
        }
        export default function AddToCart({checkoutUrl, customerAccessToken}) {
          return <CartForm route="/cart" action={CartForm.ACTIONS.LinesAdd} />;
        }
        """
        res = model.audit_react_best_practices({"app/components/AddToCart.tsx": commerce_code}, framework="shopify-hydrogen")
        guards = res["commercial_safety_guards"]
        self.assertTrue(guards["preserve_cart_checkout_auth_state"])
        self.assertEqual(len(guards["protected_commerce_files"]), 1)
        markers = guards["protected_commerce_files"][0]["markers"]
        for expected in ("CartForm", "cartLinesAdd", "checkoutUrl", "customerAccessToken", "useOptimisticCart"):
            self.assertIn(expected, markers)

    def test_11_absence_of_regressions_across_all_suites(self):
        repo_project = Project(ROOT, "ipanema")
        val = validate(repo_project)
        self.assertEqual(val["errors"], [])
        self.assertGreaterEqual(val["skills"], 14)
        self.assertEqual(evaluate_coordinator(repo_project)["outcome"], "passed")
        self.assertEqual(evaluate_seo()["outcome"], "passed")

    def test_12_security_path_confinement_and_secret_redaction(self):
        res = model.audit_react_best_practices(
            {"src/App.tsx": "const a = await fetch('https://example.invalid/api?api_key=secret_token_555');\nconst b = await fetch('https://example.invalid/b');"},
            framework="react-web",
        )
        self.assertNotIn("secret_token_555", json.dumps(res))

        with tempfile.TemporaryDirectory() as tmp:
            outside = Path(tmp) / "Outside.tsx"
            outside.write_text("export default function Outside(){ return null; }", encoding="utf-8")
            run = subprocess.run(
                [
                    sys.executable,
                    str(self.root / "tools/ia.py"),
                    "--project",
                    "sample",
                    "performance",
                    "react-audit",
                    "--source-file",
                    str(outside),
                ],
                capture_output=True,
                text=True,
                timeout=15,
            )
            self.assertEqual(run.returncode, 2)
            self.assertIn("fuera del alcance autorizado", run.stderr)

    def test_13_cli_react_audit_command_execution(self):
        comp_file = self.root / "ProductRoute.tsx"
        comp_file.write_text(
            "import _ from 'lodash';\n"
            "export async function loader({context}) {\n"
            "  const a = await context.storefront.query(Q1);\n"
            "  const b = await context.storefront.query(Q2);\n"
            "  return {a, b};\n"
            "}\n",
            encoding="utf-8",
        )
        run = subprocess.run(
            [
                sys.executable,
                str(self.root / "tools/ia.py"),
                "--project",
                "sample",
                "performance",
                "react-audit",
                "--source-file",
                str(comp_file),
                "--framework",
                "shopify-hydrogen",
            ],
            capture_output=True,
            text=True,
            timeout=15,
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        out = json.loads(run.stdout)
        self.assertEqual(out["kind"], "react-best-practices-audit")
        self.assertEqual(out["skill"], "vercel-react-best-practices")
        self.assertTrue(out["applicable"])
        self.assertEqual(out["framework"], "shopify-hydrogen")
        self.assertGreaterEqual(out["counts"]["critical"], 2)

    def test_14_verifiable_documentation_and_report_links(self):
        doc_path = ROOT / "reports/performance/vercel-react-best-practices-integration.md"
        self.assertTrue(doc_path.is_file())
        text = doc_path.read_text(encoding="utf-8")
        self.assertIn("1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62", text)
        self.assertIn("Caso A", text)
        self.assertIn("Caso F", text)


if __name__ == "__main__":
    unittest.main()
