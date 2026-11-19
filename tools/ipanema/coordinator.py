"""Selección explicable de capacidades; el runtime de IA investiga y decide."""
from __future__ import annotations

import re

from .core import Project, now
from .knowledge import Knowledge, normal


SPECIALTIES = {
    "architect": {"terms": ["arquitectura", "dependencia", "consumidor", "version", "fork", "global", "compartido"],
                  "docs": ["01-architecture/dependency-map.md", "01-architecture/platform-limitations.md"]},
    "component-builder": {"terms": ["hero", "seccion", "bloque", "componente", "snippet", "schema", "tarjeta", "card", "carrusel"],
                          "docs": ["02-native-components/component-inventory.md", "12-playbooks/build-new-section.md"]},
    "seo-expert": {"terms": ["seo", "seo-audit", "google", "rastre", "index", "noindex", "nofollow", "canonical", "h1",
                             "heading", "enlace", "sitemap", "robots", "hreflang", "meta description", "meta title",
                             "title tag", "redireccion", "redirect", "paginacion", "pagination", "canibalizacion",
                             "cannibalization", "thin content", "contenido duplicado", "duplicate content", "faceted",
                             "parametro", "json-ld", "jsonld", "schema.org", "estructurad", "productgroup", "merchant",
                             "search console", "analytics", "ctr", "blogposting", "breadcrumb"],
                   "docs": ["04-seo/seo-engine.md", "04-seo/structured-data.md"]},
    "performance": {"terms": ["rendimiento", "performance", "web-perf", "lento", "velocidad", "core web vitals", "cwv",
                              "lcp", "cls", "tbt", "inp", "ttfb", "fcp", "speed index", "lighthouse", "pagespeed", "crux",
                              "render-blocking", "bloqueante", "waterfall", "preload", "preconnect", "fetchpriority",
                              "currentsrc", "srcset", "bundle", "tree-shaking", "polyfill", "imagen", "descarg", "recurso",
                              "fuente", "javascript"],
                    "docs": ["05-performance/image-loading.md", "05-performance/core-web-vitals.md"]},
    "responsive": {"terms": ["responsive", "mobile", "movil", "desktop", "tablet", "overflow", "breakpoint", "layout", "espaciado", "columna", "tarjeta", "card"],
                   "docs": ["03-editor/responsive-controls.md", "08-design-system/responsive-system.md"]},
    "motion": {"terms": ["animacion", "animaciones", "motion", "parallax", "reveal", "transicion", "microinteraccion"],
               "docs": ["06-motion/performant-patterns.md", "06-motion/motion-accessibility.md"]},
    "visual-qa": {"terms": ["captura", "regresion", "visual", "comparar", "solap", "recort"],
                  "docs": ["10-quality/testing-matrix.md", "10-quality/accessibility.md"]},
    "commerce": {"terms": ["tarjeta", "card", "pdp", "variante", "precio", "stock", "carrito", "checkout", "compra", "descuento"],
                 "docs": ["07-commerce/product-cards.md", "07-commerce/cart.md"]},
}

EXTERNAL_SKILLS = {
    "cloudflare-web-perf": {
        "name": "cloudflare-web-perf",
        "domain": "performance",
        "role": "primary",
        "source_repo": "https://github.com/cloudflare/skills",
        "source_path": "skills/web-perf/SKILL.md",
        "source_commit": "5108325ecceabc899c761e07aa617b09c02445ee",
        "source_sha1": "9c70b7079aef1fbac9af3669bd38d5dfb712f4b7",
        "license": "Apache-2.0",
        "skill_path": ".agents/skills/cloudflare-web-perf/SKILL.md",
    },
    "web-quality-audit": {
        "name": "web-quality-audit",
        "domain": "quality-audit",
        "role": "primary",
        "source_repo": "https://github.com/addyosmani/web-quality-skills",
        "source_path": "skills/web-quality-audit/SKILL.md",
        "source_commit": "afa8da942115f2961fdbfa80807ea0b232ff6c00",
        "source_sha1": "581ec7c5e8e05e6ac93d99d872906595581efc42",
        "script_sha1": "62b066467d30ed5fa52fc36130a05699e09dd2bb",
        "license": "MIT",
        "skill_path": ".agents/skills/web-quality-audit/SKILL.md",
        "reuses": ["cloudflare-web-perf"],
    },
    "seo-audit": {
        "name": "seo-audit",
        "domain": "seo",
        "role": "primary",
        "source_repo": "https://github.com/coreyhaines31/marketingskills",
        "source_path": "skills/seo-audit/SKILL.md",
        "source_commit": "73573e94a06a39965978b3fa1f9c1eace8cebc7c",
        "source_sha1": "b33eecef416f2c5e5e2ae49eeafc3c81f88f445e",
        "license": "MIT",
        "skill_path": ".agents/skills/seo-audit/SKILL.md",
        "reuses": ["ipanema-seo-expert", "web-quality-audit"],
    },
    "schema": {
        "name": "schema",
        "domain": "schema",
        "role": "primary",
        "source_repo": "https://github.com/coreyhaines31/marketingskills",
        "source_path": "skills/schema/SKILL.md",
        "source_commit": "73573e94a06a39965978b3fa1f9c1eace8cebc7c",
        "source_sha1": "a152e5e59496740caf18ba0f0c74f4ef0e383c39",
        "references_sha1": {"schema-examples.md": "014b5292ce46184a5cde223d3a528b3e48397b8f"},
        "evals_sha1": {"evals.json": "c679cb253c26f81166b068b4e52cf04acd0cb093"},
        "license": "MIT",
        "skill_path": ".agents/skills/schema/SKILL.md",
        "reuses": ["ipanema-seo-expert", "seo-audit"],
    },
    "vercel-react-best-practices": {
        "name": "vercel-react-best-practices",
        "domain": "react",
        "role": "primary",
        "source_repo": "https://github.com/vercel-labs/agent-skills",
        "source_path": "skills/react-best-practices/SKILL.md",
        "source_commit": "1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62",
        "source_sha1": "237988de4a66dd8a71d30a2c24ebe1a86b58d04e",
        "metadata_sha1": "3bec38b176cc71d105895ec4678bbe79305dcb4c",
        "readme_sha1": "f283e1c0c21c5b13c848452528c3949ff544846c",
        "compiled_agents_sha1": "4e340a50684a8e7811d5bfa4df48bd9989d0fd87",
        "license": "MIT",
        "skill_path": ".agents/skills/vercel-react-best-practices/SKILL.md",
        "reuses": ["cloudflare-web-perf"],
    },
    "web-design-guidelines": {
        "name": "web-design-guidelines",
        "domain": "ui-ux-design",
        "role": "primary",
        "source_repo": "https://github.com/vercel-labs/agent-skills",
        "source_path": "skills/web-design-guidelines/SKILL.md",
        "source_commit": "1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62",
        "source_sha1": "ceae92ab319216a68274168fba9b63b998b65997",
        "source_sha256": "f4647ca866a3accf763777f83e7682954f0187cd6bea7eea0399796652414e8f",
        "rules_repo": "https://github.com/vercel-labs/web-interface-guidelines",
        "rules_path": "command.md",
        "rules_commit": "434b7f91364665f2f733b310ec54809bf8f37937",
        "rules_sha1": "3eb3a212b7b89493922ea418489d4c6f67ae8bd5",
        "rules_sha256": "d246b026f4f29b5823a9cc857f9edf3d2507002e055e32040cadeaf3b38e0234",
        "dynamic_fetch_enabled": False,
        "license": "MIT",
        "skill_path": ".agents/skills/web-design-guidelines/SKILL.md",
        "reuses": ["web-quality-audit", "better-accessibility", "ipanema-responsive", "ipanema-visual-qa"],
    },
    "better-accessibility": {
        "name": "better-accessibility",
        "domain": "accessibility",
        "role": "primary",
        "source_repo": "https://github.com/jakubkrehel/skills",
        "source_path": "skills/better-accessibility/SKILL.md",
        "source_commit": "547d415dc10a23e66088eba5aa6664e6e772432c",
        "source_sha1": "b5293ecc20e4356a50a55e1a1eadd3db9a0019a7",
        "source_sha256": "6a6465c044783968bae9896fd9e2e78437b90578fe3309b6dee6ef6a920e45f9",
        "agents_yaml_sha1": "36b942fb8e5b86916b006c2fe4e07fdbde24a112",
        "references_sha1": {
            "focus-and-keyboard.md": "361ad8e51c83249d9dc16a97b4ae01883de08131",
            "forms.md": "8f960cbb59f6dfd27cb47f6a962198659ff66dcd",
            "hit-areas.md": "9f9aa538683a0ba68b6164a8508164dd6109ca42",
            "motion-and-zoom.md": "e184315a5060f86107d4fb2951e884bf697cc399",
            "reporting.md": "46d221bad48a6e0992d13377a285ed6f9002f794",
            "screen-readers.md": "7da1b74995ee8bb6374e2aa17e694e7d55dc21bd",
            "semantics-and-aria.md": "24ab05c1d7fbdbd5900b5e7758bae23d06e91866",
        },
        "license": "MIT",
        "skill_path": ".agents/skills/better-accessibility/SKILL.md",
        "reuses": ["web-quality-audit", "web-design-guidelines", "ipanema-visual-qa"],
    },
}

ACCESSIBILITY_TERMS = (
    "better-accessibility",
    "accesibilidad",
    "accessibility",
    "wcag",
    "a11y",
    "lector de pantalla",
    "lectores de pantalla",
    "screen reader",
    "screen readers",
    "tecnologia de asistencia",
    "assistive technology",
    "navegacion por teclado",
    "keyboard navigation",
    "solo teclado",
    "teclado",
    "keyboard",
    "tabindex",
    "atributos aria",
    "nombre accesible",
    "nombres accesibles",
    "accessible name",
    "aria-label",
    "aria-labelledby",
    "aria-describedby",
    "aria-live",
    "live region",
    "skip link",
    "saltar al contenido",
    "gestion de foco",
    "gestion del foco",
    "trampa de foco",
    "atrapamiento de foco",
    "focus trap",
    "reflow",
    "320px",
    "zoom 200",
    "2.5.8",
    "2.4.7",
    "4.1.2",
)

WEB_DESIGN_GUIDELINES_TERMS = (
    "web-design-guidelines",
    "web interface guidelines",
    "review my ui",
    "audit design",
    "review ux",
    "auditoria de diseno",
    "revision de diseno",
    "revisa el diseno",
    "revisar el diseno",
    "evaluacion de ux",
    "jerarquia visual",
    "consistencia visual",
    "estados interactivos",
    "focus-visible",
    "tabular-nums",
    "overscroll-behavior",
    "problemas visuales",
    "claridad de cta",
)

REACT_PATTERN_TERMS = (
    "vercel-react-best-practices",
    "useeffect",
    "usestate",
    "usememo",
    "usecallback",
    "usetransition",
    "usedeferredvalue",
    "useref",
    "hooks",
    "hook",
    "rerender",
    "re-render",
    "renderizados innecesarios",
    "hidratacion",
    "hydration",
    "react.lazy",
    "next/dynamic",
    "suspense",
    "server action",
    "server component",
    "rsc",
    "barrel",
    "promise.all",
    "carga secuencial",
    "secuencial de datos",
    "componente react",
    "componentes react",
    "react component",
    "reduccion de javascript",
    "reducir javascript",
)

SCHEMA_MARKUP_TERMS = (
    "json-ld",
    "jsonld",
    "application/ld+json",
    "schema.org",
    "datos estructurados",
    "structured data",
    "schema markup",
    "productgroup",
    "aggregateoffer",
    "aggregaterating",
    "merchantreturnpolicy",
    "offershippingdetails",
    "breadcrumblist",
    "blogposting",
    "localbusiness",
    "faqpage",
    "searchaction",
    "microdata",
    "rdfa",
    "rich results",
    "resultados enriquecidos",
)

EXPLICIT_QUALITY_TERMS = (
    "web-quality-audit",
    "calidad web",
    "web quality",
    "page quality",
    "calidad de pagina",
    "calidad de la pagina",
    "buenas practicas",
    "best practices",
    "best-practices",
    "agentic browsing",
    "audit my site",
    "check page quality",
    "evaluacion de lighthouse",
    "auditoria de lighthouse",
    "lighthouse audit",
)

GENERAL_AUDIT_TERMS = (
    "auditoria completa",
    "auditoria integral",
    "auditoria general",
    "revision general",
    "revision integral",
    "diagnostico tecnico",
    "diagnostico integral",
)

QUALITY_AUDIT_TERMS = EXPLICIT_QUALITY_TERMS + GENERAL_AUDIT_TERMS

AUTHORIZED_SKILLS = frozenset([
    "ipanema-storefront",
    *(f"ipanema-{k}" for k in SPECIALTIES),
    *EXTERNAL_SKILLS.keys(),
])


def detect_context(request: str, project: Project | None = None) -> dict:
    text = normal(request)
    if "hydrogen" in text:
        framework = "shopify-hydrogen"
    elif "remix" in text:
        framework = "remix"
    elif any(t in text for t in ("nextjs", "next.js", "next/dynamic", "next/server", "app router")):
        framework = "nextjs"
    elif any(
        t in text
        for t in (
            "react", "vite", "webpack", "rollup", "esbuild", "astro",
            "jsx", "tsx", "useeffect", "usestate", "usememo", "usecallback",
            "usetransition", "usedeferredvalue",
        )
    ):
        framework = "react-web"
    elif any(t in text for t in ("shopify", "liquid")):
        framework = "shopify-liquid"
    elif any(t in text for t in ("ipanema", "tiendanube", "nuvemshop")):
        framework = "tiendanube-ipanema"
    elif project and project.theme_root and (project.theme_root / "layouts/layout.tpl").is_file():
        framework = "tiendanube-ipanema"
    elif project and project.theme_root and (project.theme_root / "layout/theme.liquid").is_file():
        framework = "shopify-liquid"
    else:
        framework = "tiendanube-ipanema" if project else "generic-web"
    return {"framework": framework, "on_demand_loading": True}


def _detect_react_matches(text: str, *, quality_matches: list, seo_scoped: bool, schema_matches: list) -> list[str]:
    if "vercel-react-best-practices" in text:
        return ["vercel-react-best-practices"]
    # Never activate React skill on Shopify Liquid or Tiendanube unless React/Hydrogen/Remix/Next.js/hooks are explicitly mentioned
    has_react_ecosystem = any(
        re.search(r"(?<![\w-])" + re.escape(t) + (r"\b" if len(t) <= 4 else ""), text)
        for t in ("react", "hydrogen", "remix", "nextjs", "next.js", "jsx", "tsx", "useeffect", "usestate", "usememo", "usecallback", "usetransition", "usedeferredvalue", "hooks", "hook", "rerender", "re-render")
    )
    pattern_hits = [
        t for t in REACT_PATTERN_TERMS
        if re.search(r"(?<![\w-])" + re.escape(t) + (r"\b" if len(t) <= 4 else ""), text)
    ]
    if not has_react_ecosystem and not any(t in text for t in ("carga secuencial", "secuencial de datos", "reduccion de javascript", "reducir javascript", "renderizados innecesarios", "barrel", "promise.all")):
        return []
    if quality_matches or seo_scoped or schema_matches:
        return pattern_hits
    if pattern_hits:
        return pattern_hits
    if has_react_ecosystem and any(
        t in text
        for t in (
            "optimiz", "rendimiento", "performance", "refactor", "bundle",
            "waterfall", "fetching", "loader", "defer", "lazy", "javascript",
            "codigo", "componente", "patron",
        )
    ):
        return ["react-optimization"]
    return []


TRUNCATED_SPECIALTY_STEMS = frozenset({
    "rastre", "index", "estructurad", "descarg", "solap", "recort", "compartid",
})

ACCESSIBILITY_SYMPTOM_PATTERNS = (
    ("focus-trap-symptom", re.compile(r"\b(?:no\s+atrapa|sin\s+trampa|atrapa\w*|pierde)\s+(?:el\s+)?foco\b")),
    ("no-mouse-symptom", re.compile(r"\b(?:no\s+funciona\s+(?:sin\s+raton|con\s+teclado)|sin\s+raton|without\s+mouse)\b")),
    ("div-onclick-symptom", re.compile(r"\b(?:div|span)\s+(?:con\s+)?onclick\b")),
    ("focus-obscured-symptom", re.compile(r"\bfoco\s+(?:queda\s+)?oculto\b")),
    ("missing-alt-symptom", re.compile(r"\bsin\s+(?:texto\s+alternativo|atributo\s+alt|aria-label|nombre\s+accesible)\b")),
    ("paste-or-zoom-blocked-symptom", re.compile(r"\b(?:impide|bloquea)\s+(?:el\s+)?(?:zoom|pegado|pegar)\b")),
    ("reflow-320-symptom", re.compile(r"\bscroll\s+horizontal\s+en\s+320\b")),
)


def _match_specialty_term(term: str, text: str) -> bool:
    escaped = re.escape(term)
    if term in TRUNCATED_SPECIALTY_STEMS or term == "compartido":
        stem = "compartid" if term == "compartido" else term
        return bool(re.search(r"(?<![\w-])" + re.escape(stem), text))
    if len(term) <= 3:
        return bool(re.search(r"(?<![\w-])" + escaped + r"\b", text))
    if term == "compra":
        return bool(re.search(r"(?<![\w-])compra(?:r|s)?\b", text))
    return bool(re.search(r"(?<![\w-])" + escaped + r"(?:s|es)?\b", text))


def _detect_accessibility_matches(text: str, *, quality_matches: list, seo_scoped: bool, perf_scoped: bool) -> list[str]:
    if "better-accessibility" in text:
        return ["better-accessibility"]
    symptom_hits = [name for name, pat in ACCESSIBILITY_SYMPTOM_PATTERNS if pat.search(text)]
    if quality_matches or seo_scoped or perf_scoped:
        explicit_a11y = [
            t for t in ("wcag", "lector de pantalla", "lectores de pantalla", "screen reader", "navegacion por teclado", "keyboard navigation")
            if t in text
        ]
        return list(dict.fromkeys(explicit_a11y + symptom_hits))
    hits = [
        t for t in ACCESSIBILITY_TERMS
        if re.search(r"(?<![\w-])" + re.escape(t) + (r"\b" if len(t) <= 4 else ""), text)
    ]
    if re.search(r"(?<![\w-])aria\b", text):
        hits.append("aria")
    if "prefers-reduced-motion" in text or ("reduced motion" in text) or ("movimiento reducido" in text):
        hits.append("prefers-reduced-motion")
    if (hits or symptom_hits) and re.search(r"(?<![\w-])foco\b", text):
        hits.append("foco")
    return list(dict.fromkeys(hits + symptom_hits))


def _detect_web_design_matches(
    text: str,
    *,
    quality_matches: list,
    seo_scoped: bool,
    perf_scoped: bool,
    accessibility_matches: list | None = None,
) -> list[str]:
    if "web-design-guidelines" in text or "web interface guidelines" in text:
        return ["web-design-guidelines"]
    design_text = re.sub(
        r"\b(?:manteniendo|conservando|preservando|sin cambiar|sin alterar|respetando)\s+(?:el\s+)?diseno\b",
        "",
        text,
    )
    hits = [t for t in WEB_DESIGN_GUIDELINES_TERMS if t in design_text]
    if hits:
        return hits
    if accessibility_matches and not any(
        t in design_text for t in ("diseno ui", "diseno ux", "ui/ux", "ux/ui", "revisa el diseno", "audita el diseno", "jerarquia visual", "consistencia visual")
    ):
        return []
    # Avoid activating on pure general quality audit ("revisión integral de una interfaz React" -> web-quality-audit)
    if quality_matches and not any(t in design_text for t in ("diseno", "ux", "jerarquia", "cta", "hover", "focus", "foco")):
        return []
    if seo_scoped or perf_scoped:
        return []
    # Do not activate on legacy Case G ("cambiar el diseño del carrito conservando lógica nativa")
    if "cambiar el diseno del carrito conservando logica nativa" in design_text:
        return []
    has_review_or_improve = any(
        t in design_text
        for t in ("revisa", "revisar", "revision", "audita", "auditar", "auditoria", "evalua", "evaluar", "evaluacion", "mejora", "mejorar", "analiza", "analizar", "corrige", "corregir")
    )
    has_ui_design_target = any(
        re.search(r"(?<![\w-])" + re.escape(t) + (r"\b" if len(t) <= 3 else ""), design_text)
        for t in ("diseno", "ux", "ui", "interfaz", "jerarquia", "cta", "formulario", "formularios", "navegacion", "hover", "focus", "foco", "interactivo", "interactivos", "consistencia")
    )
    if has_review_or_improve and has_ui_design_target:
        return ["ui-ux-design-review"]
    return []


def _detect_schema_matches(text: str) -> list[str]:
    if "en el editor" in text or "settings_schema" in text:
        return []
    matches = [t for t in SCHEMA_MARKUP_TERMS if t in text]
    if "schema" in text and any(
        t in text
        for t in (
            "product", "producto", "offer", "oferta", "blog", "article", "articulo",
            "organization", "website", "webpage", "breadcrumb", "review", "rating",
            "variant", "variante", "markup", "marcado", "duplicad", "shopify",
            "hydrogen", "pdp", "json", "localbusiness",
        )
    ):
        matches.append("schema")
    return list(dict.fromkeys(matches))


def route(request: str):
    text = normal(request)
    selected, reasons = [], {}
    explicit_quality = [t for t in EXPLICIT_QUALITY_TERMS if t in text]
    general_quality = [t for t in GENERAL_AUDIT_TERMS if t in text]
    schema_matches = _detect_schema_matches(text)
    general_seo_scoped = bool(
        re.search(
            r"(?<![\w-])(?:seo-audit|seo\s+tecnico|seo\s+on-page|on-page|hreflang|sitemap|robots|noindex|nofollow|rastre|indexa|meta description|meta title|title tag)",
            text,
        )
        or (
            re.search(r"(?<![\w-])seo\b", text)
            and (
                not schema_matches
                or bool(re.search(r"\b(?:audita\w*|revisa\w*|evalua\w*|diagnostica\w*)\s+(?:el\s+)?seo\b", text))
            )
        )
    )
    seo_scoped = general_seo_scoped or bool(schema_matches) or ("canonical" in text)
    perf_scoped = bool(re.search(r"(?<![\w-])(?:rendimiento|performance|web-perf|lcp|cls|tbt|inp|ttfb|fcp|cwv|core web vitals)", text))
    measured_perf_scoped = bool(
        re.search(
            r"(?<![\w-])(?:web-perf|lcp|cls|tbt|inp|ttfb|fcp|cwv|core web vitals|speed index|lighthouse|pagespeed|crux|render-blocking|bloqueante|traza|trace|preconnect|preload|fetchpriority|currentsrc|srcset)",
            text,
        )
    )
    quality_matches = explicit_quality + ([] if (seo_scoped or perf_scoped) and not explicit_quality else general_quality)
    react_matches = _detect_react_matches(
        text,
        quality_matches=quality_matches,
        seo_scoped=seo_scoped,
        schema_matches=schema_matches,
    )
    accessibility_matches = _detect_accessibility_matches(
        text,
        quality_matches=quality_matches,
        seo_scoped=seo_scoped,
        perf_scoped=perf_scoped,
    )
    design_matches = _detect_web_design_matches(
        text,
        quality_matches=quality_matches,
        seo_scoped=seo_scoped,
        perf_scoped=perf_scoped,
        accessibility_matches=accessibility_matches,
    )
    ui_commerce_explicit = any(t in text for t in ("carrito", "checkout", "compra", "descuento", "tarjeta", "card"))
    ui_component_explicit = any(t in text for t in ("hero", "seccion", "bloque", "componente", "snippet", "tarjeta", "card", "carrusel"))
    for key, spec in SPECIALTIES.items():
        if key == "performance" and quality_matches and not any(
            t in text for t in ("cloudflare-web-perf", "lcp", "cls", "tbt", "inp", "ttfb", "fcp", "cwv", "core web vitals")
        ):
            continue
        if schema_matches and key == "commerce" and not ui_commerce_explicit:
            continue
        if schema_matches and key == "component-builder" and not ui_component_explicit:
            continue
        if react_matches and key == "component-builder" and not any(t in text for t in ("hero", "seccion", "bloque", "snippet", "tarjeta", "card", "carrusel")):
            continue
        if (design_matches or accessibility_matches) and key == "seo-expert" and not seo_scoped:
            continue
        if accessibility_matches and key in ("performance", "motion") and not perf_scoped:
            continue
        matches = [t for t in spec["terms"] if _match_specialty_term(t, text)]
        if matches:
            selected.append(key)
            reasons[key] = matches
    if "motion" in selected and "performance" not in selected:
        selected.append("performance")
        reasons["performance"] = ["coste de animación"]
    if schema_matches and "seo-expert" not in selected:
        selected.append("seo-expert")
        reasons["seo-expert"] = schema_matches
    if react_matches and "performance" not in selected:
        selected.append("performance")
        reasons["performance"] = react_matches
    if accessibility_matches and "visual-qa" not in selected:
        selected.append("visual-qa")
        reasons["visual-qa"] = accessibility_matches
    elif design_matches and "visual-qa" not in selected and "responsive" not in selected:
        selected.append("visual-qa")
        reasons["visual-qa"] = design_matches
    if any(t in text for t in ("tarjeta", "card")) and "architect" not in selected:
        selected.append("architect")
        reasons["architect"] = ["consumidores de tarjeta compartida"]
    if quality_matches and not selected:
        selected = ["performance", "seo-expert", "visual-qa"]
        reasons["performance"] = quality_matches
        reasons["seo-expert"] = ["auditoría técnica de calidad web"]
        reasons["visual-qa"] = ["accesibilidad e interacción de calidad web"]
    if not selected:
        selected, reasons = ["architect"], {"architect": ["alcance desconocido: investigar antes de afirmar"]}
    skills = []
    primary_skills = {}
    external_active = []
    reused_engines = []
    if quality_matches:
        skills.append("web-quality-audit")
        primary_skills["quality-audit"] = "web-quality-audit"
        external_active.append(EXTERNAL_SKILLS["web-quality-audit"])
        reused_engines.append("cloudflare-web-perf")
        if "cloudflare-web-perf" in text:
            skills.append("cloudflare-web-perf")
            primary_skills["performance"] = "cloudflare-web-perf"
            external_active.append(EXTERNAL_SKILLS["cloudflare-web-perf"])
        if "seo-audit" in text:
            skills.append("seo-audit")
            primary_skills["seo"] = "seo-audit"
            external_active.append(EXTERNAL_SKILLS["seo-audit"])
        if "schema" in schema_matches and "schema" in text:
            skills.append("schema")
            primary_skills["schema"] = "schema"
            external_active.append(EXTERNAL_SKILLS["schema"])
        if design_matches:
            skills.append("web-design-guidelines")
            primary_skills["ui-ux-design"] = "web-design-guidelines"
            external_active.append(EXTERNAL_SKILLS["web-design-guidelines"])
        if accessibility_matches:
            skills.append("better-accessibility")
            primary_skills["accessibility"] = "better-accessibility"
            external_active.append(EXTERNAL_SKILLS["better-accessibility"])
            reused_engines.append("web-quality-audit")
    else:
        if accessibility_matches:
            skills.append("better-accessibility")
            primary_skills["accessibility"] = "better-accessibility"
            external_active.append(EXTERNAL_SKILLS["better-accessibility"])
            reused_engines.extend(["web-quality-audit", "ipanema-visual-qa"])
        if design_matches:
            skills.append("web-design-guidelines")
            primary_skills["ui-ux-design"] = "web-design-guidelines"
            external_active.append(EXTERNAL_SKILLS["web-design-guidelines"])
            reused_engines.extend(["web-quality-audit", "ipanema-responsive", "ipanema-visual-qa"])
            if accessibility_matches:
                reused_engines.append("better-accessibility")
    for s in selected:
        if s == "performance" and not quality_matches:
            if react_matches and not measured_perf_scoped:
                skills.append("vercel-react-best-practices")
                primary_skills["react"] = "vercel-react-best-practices"
                external_active.append(EXTERNAL_SKILLS["vercel-react-best-practices"])
                reused_engines.append("cloudflare-web-perf")
            else:
                skills.append("cloudflare-web-perf")
                primary_skills["performance"] = "cloudflare-web-perf"
                external_active.append(EXTERNAL_SKILLS["cloudflare-web-perf"])
                if react_matches:
                    skills.append("vercel-react-best-practices")
                    primary_skills["react"] = "vercel-react-best-practices"
                    external_active.append(EXTERNAL_SKILLS["vercel-react-best-practices"])
                    reused_engines.append("cloudflare-web-perf")
        if s == "seo-expert" and not quality_matches:
            if schema_matches and not general_seo_scoped:
                skills.append("schema")
                primary_skills["schema"] = "schema"
                external_active.append(EXTERNAL_SKILLS["schema"])
                reused_engines.extend(["ipanema-seo-expert", "seo-audit"])
            else:
                skills.append("seo-audit")
                primary_skills["seo"] = "seo-audit"
                external_active.append(EXTERNAL_SKILLS["seo-audit"])
                reused_engines.append("ipanema-seo-expert")
                if schema_matches:
                    skills.append("schema")
                    primary_skills["schema"] = "schema"
                    external_active.append(EXTERNAL_SKILLS["schema"])
                    reused_engines.append("seo-audit")
        skills.append("ipanema-" + s)
    ctx = detect_context(request)
    return {"skills": skills, "primary_skills": primary_skills, "external_skills": external_active,
            "reused_engines": list(dict.fromkeys(reused_engines)), "framework": ctx["framework"], "reasons": reasons,
            "selection_method": "deterministic_assistance", "parallel_agents_invoked": False}


def safety(action: str, authorized_local=False):
    levels = {"read": 0, "local-change": 1, "environment": 2, "production": 3}
    level = levels[action]
    allowed = level == 0 or (level == 1 and authorized_local)
    return {"action": action, "level": level, "allowed": allowed,
            "reason": "Lectura autorizada o implementación local expresamente solicitada." if allowed else
                      "Hace falta autorización aplicable; este ejecutor no publica ni sincroniza tiendas.",
            "remote_mutation_executor": False}


def plan(project: Project, request: str, action="read", authorized_local=False):
    selection = route(request)
    k = Knowledge(project)
    context = k.retrieve(request, 3)
    docs = list(dict.fromkeys("ipanema-discovery/" + doc for s in selection["reasons"] for doc in SPECIALTIES[s]["docs"]))
    text = normal(request)
    tests = ["Comparar fuente actual y consumidores antes de editar.", "QA del componente y diff local."]
    if "seo-expert" in selection["reasons"]:
        tests += ["HTML inicial y DOM: encabezados, enlaces href, canonical, robots y JSON-LD.",
                  "Sin JavaScript; no interpretar HTML como indexación comprobada.",
                  "seo audit: sintaxis, vocabulario acotado, reglas Google fechadas y consistencia con catálogo/CMS autorizado.",
                  "Consultar entidades nativas antes de generar; no inventar precio, disponibilidad, reviews o políticas."]
    if "performance" in selection["reasons"]:
        tests += ["Capturar solicitudes/bytes y currentSrc; DOM no equivale a descarga.",
                  "Lighthouse antes/después, mismo perfil; TBT no es INP de usuarios.",
                  "cloudflare-web-perf: analizar LCP/CLS/INP (campo) y TTFB/FCP/TBT (laboratorio), recursos bloqueantes (>0 ms), cadenas de red e imágenes responsivas."]
    if "responsive" in selection["reasons"]:
        tests += ["360, 390, 768, 1024, 1440 y 1920 px; overflow y orden de lectura sin duplicar contenido."]
    if "commerce" in selection["reasons"]:
        tests += ["Preservar LS, js-*, data-store, variantes/precio/stock y formularios nativos.",
                  "No enviar carrito, checkout ni formularios comerciales sin autorización específica."]
    if "motion" in selection["reasons"]:
        tests += ["prefers-reduced-motion, foco/teclado, layout/paint/composite y CLS; transform/opacity no son gratis."]
    investigation = ["Confirmar componente/configuración y estado actuales del proyecto."]
    if "h1" in text:
        investigation += ["Localizar el H1 y sus ancestros: contenido editable/user-content frente a plantilla; no ocultarlo con CSS."]
    if "carrusel" in text and any(t in text for t in ("google", "seo", "rastre", "enlace")):
        investigation += ["Inspeccionar <a href> y slides en HTML inicial/DOM, enlaces de categoría y navegación sin JS; separar descubrimiento, rastreo e indexación."]
    alternatives = ["Configuración nativa", "Composición existente", "Tokens/variables", "Modificar componente compartido",
                    "Extensión controlada", "Nuevo componente", "Biblioteca externa justificada"]
    components = context["components"]
    required_checks = ["native-consumers", "permission-gate"]
    if "seo-expert" in selection["reasons"]:
        required_checks += ["initial-html", "no-js"]
    if "h1" in text:
        required_checks += ["heading-origin"]
    if "performance" in selection["reasons"]:
        required_checks += ["network-images", "performance-lab"]
    if "responsive" in selection["reasons"]:
        required_checks += ["responsive"]
    if "commerce" in selection["reasons"]:
        required_checks += ["commerce-contracts"]
    if "motion" in selection["reasons"]:
        required_checks += ["reduced-motion"]
    return {"agent_version": "2.0.0", "at": now(), "project": project.id, "objective": request,
            "context": detect_context(request, project),
            "problem": "Confirmar la causa en la implementación real; la petición sola no demuestra un defecto.",
            "selection": selection, "permission": safety(action, authorized_local),
            "investigation": investigation, "evidence": context,
            "native_component_candidates": [c["path"] for c in components],
            "alternatives_in_order": alternatives,
            "decision": "Investigar la alternativa nativa mínima antes de implementar; no se autoriza ni ejecuta una publicación.",
            "affected_files_candidates": [c["path"] for c in components],
            "consumers": {c["path"]: c["consumers"] for c in components},
            "risks": ["La evidencia puede estar desactualizada o corresponder a otra tienda.",
                      "Un cambio global altera todos los consumidores; revisar contratos de plataforma."],
            "impact": {"responsive": "Comprobar cascada por dispositivo y orden semántico.",
                       "seo": "Conservar contenido inicial, href y datos estructurados existentes.",
                       "performance": "Medir antes/después con condiciones comparables.",
                       "accessibility": "Conservar foco, nombres, teclado y reduced motion."},
            "tests": tests, "required_checks": required_checks, "knowledge_to_load": docs,
            "rollback": "Usar una transacción local de archivos explícitos; revertir solo si el hash coincide con el propio intento. Nunca reset --hard/clean.",
            "status": "plan_requires_source_investigation", "implementation_executed": False}
