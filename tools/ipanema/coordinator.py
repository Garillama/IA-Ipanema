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
}

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
    if any(t in text for t in ("hydrogen", "remix")):
        framework = "shopify-hydrogen"
    elif any(t in text for t in ("shopify", "liquid")):
        framework = "shopify-liquid"
    elif any(t in text for t in ("nextjs", "next.js", "react", "vite", "webpack", "rollup", "esbuild", "astro")):
        framework = "react-web"
    elif any(t in text for t in ("ipanema", "tiendanube", "nuvemshop")):
        framework = "tiendanube-ipanema"
    elif project and project.theme_root and (project.theme_root / "layouts/layout.tpl").is_file():
        framework = "tiendanube-ipanema"
    elif project and project.theme_root and (project.theme_root / "layout/theme.liquid").is_file():
        framework = "shopify-liquid"
    else:
        framework = "tiendanube-ipanema" if project else "generic-web"
    return {"framework": framework, "on_demand_loading": True}


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
            r"(?<![\w-])(?:seo-audit|hreflang|sitemap|robots|noindex|nofollow|rastre|indexa|meta description|meta title|title tag)",
            text,
        )
        or ("seo" in text and not schema_matches)
    )
    seo_scoped = general_seo_scoped or bool(schema_matches) or ("canonical" in text)
    perf_scoped = bool(re.search(r"(?<![\w-])(?:rendimiento|performance|web-perf|lcp|cls|tbt|inp|ttfb|fcp|cwv|core web vitals)", text))
    quality_matches = explicit_quality + ([] if (seo_scoped or perf_scoped) and not explicit_quality else general_quality)
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
        matches = [t for t in spec["terms"] if re.search(r"(?<![\w-])" + re.escape(t) + (r"\b" if len(t) <= 3 else ""), text)]
        if matches:
            selected.append(key)
            reasons[key] = matches
    if "motion" in selected and "performance" not in selected:
        selected.append("performance")
        reasons["performance"] = ["coste de animación"]
    if schema_matches and "seo-expert" not in selected:
        selected.append("seo-expert")
        reasons["seo-expert"] = schema_matches
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
    for s in selected:
        if s == "performance" and not quality_matches:
            skills.append("cloudflare-web-perf")
            primary_skills["performance"] = "cloudflare-web-perf"
            external_active.append(EXTERNAL_SKILLS["cloudflare-web-perf"])
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
