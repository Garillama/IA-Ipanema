# Integración Skill 1 — Cloudflare Web Performance (`cloudflare-web-perf`)

Fecha: 2026-11-18  
Estado: **`integrated_and_verified`**  
Rama de trabajo: `feat/cloudflare-web-perf`

## Etapa A — Análisis de origen y arquitectura

- **Repositorio de origen**: `https://github.com/cloudflare/skills`
- **Archivo principal**: `skills/web-perf/SKILL.md` (SHA1: `9c70b7079aef1fbac9af3669bd38d5dfb712f4b7`)
- **Commit verificado**: `5108325ecceabc899c761e07aa617b09c02445ee` (`2026-11-17T15:55:49Z`)
- **Licencia**: `Apache-2.0`
- **Dependencias adicionales instaladas**: Ninguna (`0` paquetes externos añadidos).
- **Reutilización vs. incorporación**:
  - **Reutilizado**: Motor de rendimiento existente ([tools/ipanema/performance/model.py](../../tools/ipanema/performance/model.py), [service.py](../../tools/ipanema/performance/service.py), [cli.py](../../tools/ipanema/performance/cli.py)), colectores de navegador y Lighthouse ([tools/performance_evidence.mjs](../../tools/performance_evidence.mjs), [tools/page_collectors.mjs](../../tools/page_collectors.mjs)) y gateway MCP fijado `chrome-devtools-mcp@1.12.0` ([tools/ipanema/access/devtools.py](../../tools/ipanema/access/devtools.py), [gateway.py](../../tools/ipanema/access/gateway.py)).
  - **Incorporado**:
    1. Skill estructurada [.agents/skills/cloudflare-web-perf/SKILL.md](../../.agents/skills/cloudflare-web-perf/SKILL.md) como skill principal para tareas de rendimiento web.
    2. Registro de skills externas (`EXTERNAL_SKILLS`, `AUTHORIZED_SKILLS`) y detector de contexto/framework (`detect_context`: `shopify-liquid`, `shopify-hydrogen`, `react-web`, `tiendanube-ipanema`, `generic-web`) en [tools/ipanema/coordinator.py](../../tools/ipanema/coordinator.py).
    3. Carga bajo demanda en el orquestador ([tools/ipanema/orchestration/engine.py](../../tools/ipanema/orchestration/engine.py) y [planner.py](../../tools/ipanema/orchestration/planner.py)).
    4. Motor de diagnóstico `diagnose_web_perf`, umbrales oficiales `CWV_THRESHOLDS` (`ttfb`, `fcp`, `lcp`, `inp`, `tbt`, `cls`, `speed_index`), clasificador `rate_metric` y subcomando CLI `python3 tools/ia.py performance diagnose`.

## Etapa B — Evaluación de seguridad

1. **Bloqueo de ejecución remota no fijada (`npx -y chrome-devtools-mcp@latest`)**: El archivo upstream sugiere ejecutar `npx -y chrome-devtools-mcp@latest`. En nuestra adaptación se prohíbe expresamente y se redirige al gateway MCP local fijado (`chrome-devtools-mcp@1.12.0` con integridad SHA-512 verificada y perfil efímero aislado).
2. **Restricción de `get_network_request` en crudo**: Para evitar exposición de cabeceras de sesión, cookies o cuerpos privados, las inspecciones de red utilizan `devtools_network` (`--redact-network-headers`) y `createNetworkRecorder` con redacción automática de parámetros sensibles.
3. **Eliminación de publicación externa de issues (`references/skill-feedback.md`)**: No se incorpora el flujo de `gh issue create --repo cloudflare/skills` para impedir envíos externos no autorizados.
4. **Separación estricta entre campo y laboratorio**: Se mantiene la prohibición de sustituir INP de campo por TBT de laboratorio o asumir descarga de imágenes solo por presencia en el DOM.

## Etapa C — Integración en la arquitectura

- **Ubicación**: [.agents/skills/cloudflare-web-perf/SKILL.md](../../.agents/skills/cloudflare-web-perf/SKILL.md).
- **Coordinación**: [.agents/skills/ipanema-storefront/SKILL.md](../../.agents/skills/ipanema-storefront/SKILL.md) y [.agents/skills/ipanema-performance/SKILL.md](../../.agents/skills/ipanema-performance/SKILL.md) referencian a `cloudflare-web-perf` como skill principal de rendimiento web sin duplicar auditorías.
- **Reversibilidad**: Puede deshabilitarse o revertirse retirando su entrada en `EXTERNAL_SKILLS` y su archivo `SKILL.md` sin afectar las 9 skills existentes de Ipanema.

## Etapa D y E — Pruebas ejecutadas y resultados

- Suite unitaria específica: [tests/unit/test_cloudflare_web_perf.py](../../tests/unit/test_cloudflare_web_perf.py) (6 pruebas cubriendo estructura, activación multi-framework, carga bajo demanda, umbrales CWV y separación campo/laboratorio, regresión/comparación/CLI y controles de seguridad).
- Suite general del agente: `python3 tools/ia.py qa --suite quick` (`repository`, `unit-tests`, `integration-tests`, `coordinator-evals`, `seo-action-evals`, `sources-stable-during-qa`).
