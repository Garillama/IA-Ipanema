"""Etapa 9: Pruebas adversarias e independientes para estabilización P0/P1, parsing estructural, routing y E2E reversible."""
from __future__ import annotations

import hashlib
import shutil
import sys
import tempfile
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from support import ROOT, make_project
from ipanema.coordinator import EXTERNAL_SKILLS, route
from ipanema.core import Project, read_json
from ipanema.performance import html_liquid, model
from ipanema import transactions


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class Stage9StabilizationTests(unittest.TestCase):
    def test_01_jsx_tsx_abstains_from_unsafe_autofix_without_ast_parser(self):
        jsx_code = (
            "export function VariantSwatch({onSelect}: {onSelect: (v: string) => void}) {\n"
            "  return (\n"
            "    <div className='swatch-wrap'>\n"
            "      <div className='js-swatch' onClick={(e) => { if (e.detail >= 0) onSelect('M'); }}>Talla M</div>\n"
            "      <img src='/swatch.jpg' />\n"
            "      <input type='text' name='note' />\n"
            "      <button onClick={() => onSelect('close')}>\n"
            "        <svg aria-hidden='true'></svg>\n"
            "      </button>\n"
            "    </div>\n"
            "  );\n"
            "}\n"
        )
        # Diagnóstico TSX debe funcionar sin truncar en =>
        diag = model.audit_better_accessibility({"src/VariantSwatch.tsx": jsx_code}, framework="shopify-hydrogen")
        ids = {f["id"] for f in diag["code_hypothesis"]}
        self.assertIn("A11Y-SRC-NON-SEMANTIC-CLICKABLE", ids)
        self.assertIn("A11Y-SRC-IMG-MISSING-ALT", ids)
        self.assertIn("A11Y-SRC-FORM-MISSING-LABEL", ids)
        self.assertIn("A11Y-SRC-ICON-BUTTON-NO-NAME", ids)

        # Autofix sin parser AST JSX/TSX instalado debe abstenerse y no corromper /> ni =>
        fixes = model.propose_safe_accessibility_fixes({"src/VariantSwatch.tsx": jsx_code})
        self.assertFalse(fixes["changed"])
        self.assertEqual(fixes["patched_files"]["src/VariantSwatch.tsx"], jsx_code)
        self.assertFalse(fixes["strategy_by_file"]["src/VariantSwatch.tsx"]["auto_apply_enabled"])
        self.assertEqual(fixes["abstained_files"][0]["file"], "src/VariantSwatch.tsx")
        self.assertGreaterEqual(len(fixes["manual_proposals"]), 4)
        self.assertNotIn("/ alt=", fixes["patched_files"]["src/VariantSwatch.tsx"])
        self.assertNotIn("/ aria-label=", fixes["patched_files"]["src/VariantSwatch.tsx"])

    def test_02_html_nested_div_abstention_prevents_misnested_tags(self):
        nested_html = (
            "<div class='card-wrap'>\n"
            "  <div class='js-card-btn' onclick='openProduct()'><span>Ver</span><div>Detalle</div></div>\n"
            "</div>\n"
        )
        fixes = model.propose_safe_accessibility_fixes({"snippets/card.html": nested_html})
        after = fixes["patched_files"]["snippets/card.html"]
        self.assertEqual(after, nested_html)
        self.assertFalse(fixes["changed"])
        self.assertEqual(len(fixes["abstained_elements"]), 1)
        self.assertIn("anidadas", fixes["abstained_elements"][0]["reason"])
        parsed_after = html_liquid.parse_structural_document("snippets/card.html", after)
        self.assertTrue(parsed_after.balanced)

    def test_03_liquid_interpolations_self_closing_and_dynamic_attrs_preserved(self):
        liquid_code = (
            "{% if product.available %}\n"
            "  <div class='product-media'>\n"
            "    <img\n"
            "      src='{{ product.featured_image | image_url: width: 800 }}'\n"
            "      data-price='{% if product.price > 0 %}{{ product.price }}{% endif %}' />\n"
            "    <input type='number' name='quantity' value='1' />\n"
            "    <img {{ dynamic_image_attributes }} />\n"
            "  </div>\n"
            "{% endif %}\n"
        )
        fixes = model.propose_safe_accessibility_fixes({"sections/pdp-media.liquid": liquid_code})
        after = fixes["patched_files"]["sections/pdp-media.liquid"]
        self.assertTrue(fixes["changed"])
        # Valida estructura HTML + preservación exacta de self-closing />
        self.assertNotIn("/ alt=", after)
        self.assertNotIn("/ aria-label=", after)
        self.assertIn('alt="Imagen de producto" />', after)
        self.assertIn('aria-label="quantity" />', after)
        # No debe tocar el <img {{ dynamic_image_attributes }} />
        self.assertIn("<img {{ dynamic_image_attributes }} />", after)
        self.assertGreaterEqual(len(fixes["abstained_elements"]), 1)

        parsed_before = html_liquid.parse_structural_document("sections/pdp-media.liquid", liquid_code)
        parsed_after = html_liquid.parse_structural_document("sections/pdp-media.liquid", after)
        self.assertTrue(parsed_after.balanced)
        self.assertEqual([s.raw for s in parsed_after.liquid_spans], [s.raw for s in parsed_before.liquid_spans])

    def test_04_unbalanced_or_malformed_html_fails_safely(self):
        broken_html = "<div><span>Texto sin cerrar</div><img src='/a.jpg'>\n"
        fixes = model.propose_safe_accessibility_fixes({"snippets/broken.html": broken_html})
        self.assertFalse(fixes["changed"])
        self.assertEqual(fixes["patched_files"]["snippets/broken.html"], broken_html)
        self.assertEqual(fixes["abstained_files"][0]["file"], "snippets/broken.html")
        self.assertFalse(fixes["post_patch_verified"]["snippets/broken.html"])

    def test_05_multiline_buttons_accessible_name_matrix_no_false_positives(self):
        # 1. Multilínea icon-only sin nombre -> debe detectarse como code_hypothesis
        # 2. Multilínea con texto visible + svg aria-hidden -> sin violación
        # 3. Multilínea con aria-label Liquid dinámico + svg aria-hidden -> sin violación
        # 4. Botón con solo <svg aria-hidden="true"><title>Oculto</title></svg> -> debe detectarse (title dentro de aria-hidden no nombra botón)
        # 5. Botón en <label> envolvente con <input> multilínea -> sin falso positivo en input
        liquid = (
            "<button class='icon-btn'>\n"
            "  <svg aria-hidden='true'></svg>\n"
            "</button>\n"
            "<button class='add-btn'>\n"
            "  <svg aria-hidden='true'></svg>\n"
            "  <span>Agregar al carrito</span>\n"
            "</button>\n"
            "<button class='close-btn' aria-label=\"{{ 'actions.close' | t }}\">\n"
            "  <svg aria-hidden='true'></svg>\n"
            "</button>\n"
            "<label>\n"
            "  <input type='checkbox' name='terms' />\n"
            "  Acepto términos\n"
            "</label>\n"
        )
        res = model.audit_better_accessibility({"snippets/buttons.liquid": liquid}, framework="shopify-liquid")
        # Ningún hallazgo debe declararse como violación DOM verificada solo por análisis estático
        self.assertEqual(res["counts"]["wcag_violations_verified"], 0)
        icon_findings = [f for f in res["code_hypothesis"] if f["id"] == "A11Y-SRC-ICON-BUTTON-NO-NAME"]
        self.assertEqual(len(icon_findings), 1)
        self.assertEqual(icon_findings[0]["location"], "snippets/buttons.liquid:1")
        # El checkbox envuelto en <label> multilínea NO debe generar falso positivo FORM-MISSING-LABEL
        form_findings = [f for f in res["code_hypothesis"] if f["id"] == "A11Y-SRC-FORM-MISSING-LABEL"]
        self.assertEqual(form_findings, [])

        # Autofix solo añade aria-label al botón 1, sin tocar botones 2 y 3 ni el checkbox envuelto
        fixes = model.propose_safe_accessibility_fixes({"snippets/buttons.liquid": liquid})
        self.assertEqual(len(fixes["applied_changes"]), 1)
        after = fixes["patched_files"]["snippets/buttons.liquid"]
        self.assertIn("aria-label=\"Acción\"", after)

    def test_06_idempotency_double_application_produces_zero_diff(self):
        pdp_html = (
            "<style>.btn { outline: none; } @keyframes pulse { from { opacity: 1; } to { opacity: 0.7; } }</style>\n"
            "<img src='/hero.jpg' />\n"
            "<div class='js-swatch' onclick='pickVar(1)'>Rojo</div>\n"
            "<button class='close-cart'>\n  <svg></svg>\n</button>\n"
            "<div id='cart-drawer' class='cart-drawer js-cart-drawer'></div>\n"
        )
        first = model.propose_safe_accessibility_fixes({"sections/pdp.liquid": pdp_html})
        self.assertTrue(first["changed"])
        patched_once = first["patched_files"]["sections/pdp.liquid"]

        second = model.propose_safe_accessibility_fixes({"sections/pdp.liquid": patched_once})
        self.assertFalse(second["changed"])
        self.assertEqual(second["applied_changes"], [])
        self.assertEqual(second["diff"], "")
        self.assertEqual(second["patched_files"]["sections/pdp.liquid"], patched_once)

    def test_07_coordinator_p1_combined_seo_schema_symptom_a11y_and_partial_match_fixes(self):
        # Problema A: Solicitud combinada SEO técnico + JSON-LD -> activa BOTH seo-audit y schema
        r_seo_schema = route("Audita el SEO técnico y los datos estructurados JSON-LD de mi tienda Shopify")
        self.assertIn("seo-audit", r_seo_schema["skills"])
        self.assertIn("schema", r_seo_schema["skills"])
        self.assertIn("seo-audit", r_seo_schema["reused_engines"])
        self.assertIn("ipanema-seo-expert", r_seo_schema["reused_engines"])

        # Solicitud específica solo Schema sigue sin activar seo-audit
        r_schema_only = route("Revisa el JSON-LD Product y Offer de una página de producto Shopify")
        self.assertIn("schema", r_schema_only["skills"])
        self.assertNotIn("seo-audit", r_schema_only["skills"])

        # Problema B: Síntomas de accesibilidad sin palabras 'WCAG', 'ARIA' o 'accesibilidad'
        r_symptom = route("El modal del carrito no atrapa el foco y el selector de talla con div onclick no funciona sin ratón")
        self.assertIn("better-accessibility", r_symptom["skills"])
        self.assertEqual(r_symptom["primary_skills"]["accessibility"], "better-accessibility")
        self.assertIn("ipanema-commerce", r_symptom["skills"])
        self.assertNotIn("web-design-guidelines", r_symptom["skills"])

        # Problema C: 'bloqueo' NO debe activar 'ipanema-component-builder' (bloque)
        r_perf = route("Analiza el rendimiento LCP y bloqueo de renderizado de esta tienda Shopify")
        self.assertIn("cloudflare-web-perf", r_perf["skills"])
        self.assertNotIn("ipanema-component-builder", r_perf["skills"])

        # Verificar que 'bloque' / 'bloques' sí sigue activando component-builder cuando corresponde
        r_block = route("Crea un bloque de hero usando componentes nativos")
        self.assertIn("ipanema-component-builder", r_block["skills"])

        # Verificar Caso E histórico ('compartida' sigue coincidiendo con stem 'compartid')
        r_card = route("Modificar la product card compartida de home, categoría y búsqueda.")
        self.assertIn("ipanema-architect", r_card["skills"])
        self.assertIn("ipanema-component-builder", r_card["skills"])

    def test_08_end_to_end_pdp_liquid_nested_jsx_tx_cycle_with_reversion(self):
        with tempfile.TemporaryDirectory(prefix="ipanema-stage9-e2e-") as tmp:
            root = make_project(Path(tmp), "sample", theme=True)
            pdp_rel = "sections/main-product.liquid"
            card_rel = "snippets/nested-card.html"
            tsx_rel = "app/components/VariantDrawer.tsx"

            (root / "sections").mkdir(exist_ok=True)
            (root / "snippets").mkdir(exist_ok=True)
            (root / "app/components").mkdir(parents=True, exist_ok=True)

            pdp_orig = (
                "<style>:root { --color-brand: #0b2239; } .pdp-btn { outline: none; }</style>\n"
                "<form action='/cart/add' method='post' class='js-product-form' data-store='product-form'>\n"
                "  <img src=\"{{ product.featured_image | image_url }}\" />\n"
                "  <div class='variant-chip js-variant-option' data-option='L' onclick='selectVariant(\"L\")'>Talla L</div>\n"
                "  <input type='number' name='quantity' value='1' />\n"
                "  <button type='submit' class='pdp-btn js-add-to-cart'>Agregar al carrito</button>\n"
                "</form>\n"
                "<div id='cart-drawer' class='cart-drawer js-cart-drawer' data-store='cart-drawer'>\n"
                "  <button class='close-drawer'>\n"
                "    <svg viewBox='0 0 24 24'></svg>\n"
                "  </button>\n"
                "</div>\n"
            )
            card_orig = "<div class='js-card-link' onclick='goCard()'><span>Item</span><div>Sub</div></div>\n"
            tsx_orig = (
                "export function VariantDrawer({onClose}: {onClose: () => void}) {\n"
                "  return <div><img src='/a.jpg' /><button onClick={() => onClose()}><svg /></button></div>;\n"
                "}\n"
            )

            (root / pdp_rel).write_text(pdp_orig, encoding="utf-8")
            (root / card_rel).write_text(card_orig, encoding="utf-8")
            (root / tsx_rel).write_text(tsx_orig, encoding="utf-8")

            sources_before = {pdp_rel: pdp_orig, card_rel: card_orig, tsx_rel: tsx_orig}
            hashes_before = {k: _sha256(v) for k, v in sources_before.items()}

            # 1. Diagnóstico
            diag_before = model.audit_better_accessibility(sources_before, framework="shopify-liquid")
            self.assertGreaterEqual(diag_before["counts"]["wcag_violations_hypothesis"], 7)

            # 2. Propuesta segura
            plan_fix = model.propose_safe_accessibility_fixes(sources_before)
            self.assertEqual(plan_fix["patched_files"][card_rel], card_orig)
            self.assertEqual(plan_fix["patched_files"][tsx_rel], tsx_orig)
            self.assertNotEqual(plan_fix["patched_files"][pdp_rel], pdp_orig)

            # 3. Transacción autorizada solo sobre archivos seguros (pdp_rel modificado; card_rel y tsx_rel intactos)
            proj = Project(root, "sample")
            tx = transactions.begin(proj, [pdp_rel, card_rel, tsx_rel], scope="workspace", authorized=True)
            transactions.apply(proj, tx["id"], {
                pdp_rel: plan_fix["patched_files"][pdp_rel],
                card_rel: plan_fix["patched_files"][card_rel],
                tsx_rel: plan_fix["patched_files"][tsx_rel],
            })

            # Validar contratos comerciales, tokens y Liquid intactos tras aplicar
            pdp_applied = (root / pdp_rel).read_text(encoding="utf-8")
            for contract in ("--color-brand: #0b2239", "action='/cart/add'", "js-product-form", "data-store='product-form'", "js-add-to-cart", "js-cart-drawer", "{{ product.featured_image | image_url }}"):
                self.assertIn(contract, pdp_applied)
            self.assertNotIn("/ alt=", pdp_applied)
            self.assertNotIn("/ aria-label=", pdp_applied)
            self.assertTrue(html_liquid.parse_structural_document(pdp_rel, pdp_applied).balanced)

            # 4. Verificación posterior
            diag_after = model.audit_better_accessibility({pdp_rel: pdp_applied}, framework="shopify-liquid")
            self.assertLess(diag_after["counts"]["wcag_violations_hypothesis"], 2)

            # 5. Reversión exacta byte a byte
            rev = transactions.finish(proj, tx["id"], accept=False)
            self.assertEqual(rev["status"], "reverted")
            for rel, h in hashes_before.items():
                self.assertEqual(_sha256((root / rel).read_text(encoding="utf-8")), h)

    def test_09_security_and_council_policy_preserved(self):
        models_cfg = read_json(ROOT / "tools/ipanema/orchestration/models.json")
        self.assertEqual(models_cfg["council"]["members"], ["claude", "codex"])
        self.assertIn("commandcode", models_cfg["council"]["disabled"])
        self.assertNotIn("antigravity", models_cfg["council"]["members"])
        self.assertEqual(len(EXTERNAL_SKILLS), 7)


if __name__ == "__main__":
    unittest.main()
