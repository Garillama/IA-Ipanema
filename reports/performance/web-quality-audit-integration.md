# Integración Etapa 2 — Web Quality Audit (`web-quality-audit`)

Fecha: 2026-11-18  
Estado: **`integrated_and_verified`**  
Rama de trabajo: `feat/web-quality-audit` (creada desde `feat/cloudflare-web-perf`, commit base `8787086`)

## 1. Procedencia y análisis de origen (Etapa A)

- **Repositorio original**: `https://github.com/addyosmani/web-quality-skills`
- **Directorio**: `skills/web-quality-audit`
- **Commit verificado**: `afa8da942115f2961fdbfa80807ea0b232ff6c00` (`2026-08-24T21:07:33Z`)
- **Licencia**: `MIT`
- **Archivos auditados del origen**:
  - `SKILL.md` (`10,450` bytes, SHA1 `581ec7c5e8e05e6ac93d99d872906595581efc42`)
  - `scripts/analyze.sh` (`3,864` bytes, SHA1 `62b066467d30ed5fa52fc36130a05699e09dd2bb`)
- **Dependencias nuevas instaladas**: `0` (sin paquetes externos añadidos).

## 2. Evaluación de seguridad y no duplicación (Etapa B)

1. **No ejecución ni empaquetado de `scripts/analyze.sh`**: El script upstream requiere `jq` (`brew install jq`), ejecuta un shell externo y marca como inseguros esquemas `http://` de namespaces estándar (`http://www.w3.org/2000/svg`, `http://schema.org`). Su lógica de smoke test estático se reimplementó en Python puro dentro de `audit_web_quality` en [model.py](../../tools/ipanema/performance/model.py), clasificando estrictamente todo hallazgo estático como `code_hypothesis` y nunca como fallo medido en tiempo de ejecución.
2. **Restricción de `evaluate_script` y confinamiento de archivos**: Nuestro gateway [devtools.py](../../tools/ipanema/access/devtools.py) mantiene `--no-javascript-evaluation` y `--redact-network-headers`. Además, el subcomando CLI `performance quality-audit --source-file` valida con `beneath` que cualquier archivo inspeccionado pertenezca a `project.root` o `project.theme_root`.
3. **Cero duplicación con Cloudflare Web Performance (`cloudflare-web-perf`)**:
   - En enrutamiento ([coordinator.py](../../tools/ipanema/coordinator.py)): las peticiones exclusivas de rendimiento activan `cloudflare-web-perf` sin cargar `web-quality-audit`. Las peticiones de auditoría general de calidad web activan `web-quality-audit` sin cargar `cloudflare-web-perf` de forma redundante en el prompt.
   - En ejecución ([model.py](../../tools/ipanema/performance/model.py)): `audit_web_quality` invoca directamente `diagnose_web_perf` (`reused_engine: "cloudflare-web-perf"`), reutilizando íntegramente el análisis de LCP, CLS, INP, TTFB, FCP, TBT, recursos bloqueantes, cascadas de red e imágenes responsivas.

## 3. Capacidades integradas (Etapa C)

- **Skill registrada**: [.agents/skills/web-quality-audit/SKILL.md](../../.agents/skills/web-quality-audit/SKILL.md).
- **Cobertura en 5 categorías**:
  1. **Rendimiento web**: Delegado en `diagnose_web_perf` (`cloudflare-web-perf`).
  2. **Accesibilidad**: `<html lang>`, `<img alt>`, `<label>`/`aria-label` en formularios, violaciones `axe-core` y scores de Lighthouse.
  3. **SEO técnico y on-page**: `<title>`, `<meta name="description">`, `<link rel="canonical">`, detección crítica de `noindex`, jerarquía `<h1>`, textos de enlace genéricos (`click here` / `leer más`) y validación sintáctica de `JSON-LD`.
  4. **Buenas prácticas y errores de implementación**: Errores de consola (`console_messages`), recursos HTTP inseguros (contenido mixto), source maps `.map` expuestos en producción, `<!doctype html>`, `charset="utf-8"`, `viewport` y `document.write()`.
  5. **Calidad de navegación, interacción y Agentic Browsing**: Desbordamiento horizontal (`scrollWidth > innerWidth`) y enlaces/controles interactivos sin nombre accesible.
- **Separación explícita de evidencia vs. hipótesis**:
  - `verified_issues` (`evidence_type: "verified_by_tool"`): Fallos confirmados en CrUX, Lighthouse/PSI, red, consola o DOM renderizado.
  - `code_hypotheses` (`evidence_type: "code_hypothesis"`): Hallazgos estáticos en plantillas/código fuente pendientes de verificación en navegador.
- **Soporte multi-framework**: `shopify-liquid`, `shopify-hydrogen`, `react-web` y `tiendanube-ipanema` con mapeo de archivos candidatos (`FRAMEWORK_CANDIDATES`).
- **Subcomando CLI**: `python3 tools/ia.py performance quality-audit <report.json> [--rendered <rendered.json>] [--source-file <archivo>] [--framework <fw>]` en [cli.py](../../tools/ipanema/performance/cli.py).

## 4. Pruebas y verificación (Etapas D y E)

- Suite unitaria específica: [tests/unit/test_web_quality_audit.py](../../tests/unit/test_web_quality_audit.py) (10 pruebas obligatorias).
- Suite Etapa 1 sin regresión: [tests/unit/test_cloudflare_web_perf.py](../../tests/unit/test_cloudflare_web_perf.py) (6 pruebas).
- Suite integral del agente: `python3 tools/ia.py qa --suite quick`.
