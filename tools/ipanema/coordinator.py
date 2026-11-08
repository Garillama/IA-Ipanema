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
    "seo-expert": {"terms": ["seo", "google", "rastre", "index", "canonical", "h1", "heading", "enlace", "sitemap", "robots", "json-ld", "jsonld", "schema.org", "estructurad", "productgroup", "merchant", "search console", "analytics", "ctr", "blogposting", "breadcrumb"],
                   "docs": ["04-seo/seo-engine.md", "04-seo/structured-data.md"]},
    "performance": {"terms": ["rendimiento", "lento", "velocidad", "lcp", "cls", "tbt", "inp", "imagen", "descarg", "recurso", "fuente", "javascript"],
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


def route(request: str):
    text = normal(request)
    selected, reasons = [], {}
    for key, spec in SPECIALTIES.items():
        matches = [t for t in spec["terms"] if re.search(r"(?<![\w-])" + re.escape(t) + (r"\b" if len(t) <= 3 else ""), text)]
        if matches:
            selected.append(key)
            reasons[key] = matches
    if "motion" in selected and "performance" not in selected:
        selected.append("performance")
        reasons["performance"] = ["coste de animación"]
    if 'schema' in text and any(t in text for t in ('product','offer','blog','article','organization','webpage')) and 'seo-expert' not in selected:
        selected.append('seo-expert')
        reasons['seo-expert']=['schema de una entidad comercial/editorial; comprobar si es datos estructurados o schema de editor']
    if any(t in text for t in ("tarjeta", "card")) and "architect" not in selected:
        selected.append("architect")
        reasons["architect"] = ["consumidores de tarjeta compartida"]
    if not selected:
        selected, reasons = ["architect"], {"architect": ["alcance desconocido: investigar antes de afirmar"]}
    return {"skills": ["ipanema-" + s for s in selected], "reasons": reasons,
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
                  "Lighthouse antes/después, mismo perfil; TBT no es INP de usuarios."]
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
