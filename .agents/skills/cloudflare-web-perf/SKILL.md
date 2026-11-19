---
name: cloudflare-web-perf
description: Diagnosticar y optimizar rendimiento web, Core Web Vitals (LCP, CLS, INP), TTFB, FCP, TBT, trazas DevTools, cascadas de red, recursos bloqueantes, JS, CSS, imágenes y bundlers en Shopify, Hydrogen, React, Liquid y Tiendanube/Ipanema.
---

# Cloudflare Web Performance (`cloudflare-web-perf`)

Skill principal del agente para diagnóstico, auditoría y optimización de rendimiento web. Integra y adapta la especificación oficial de Cloudflare Web Performance (`https://github.com/cloudflare/skills`, `skills/web-perf/SKILL.md`, commit `5108325ecceabc899c761e07aa617b09c02445ee`, SHA1 `9c70b7079aef1fbac9af3669bd38d5dfb712f4b7`, licencia `Apache-2.0`) a la arquitectura de seguridad, permisos y evidencia verificable definida en [AGENTS.md](../../../AGENTS.md).

Coordina sus mediciones con [ipanema-storefront](../ipanema-storefront/SKILL.md), [ipanema-performance](../ipanema-performance/SKILL.md) y el [motor integrado de rendimiento](../../../reports/performance/README.md) para compartir evidencia y evitar auditorías redundantes.

## Fuentes de consulta vigentes

Prioriza evidencia medida y documentación oficial vigente sobre supuestos de pre-entrenamiento:

| Fuente | URL oficial | Uso |
|---|---|---|
| web.dev Core Web Vitals | `https://web.dev/articles/vitals` | Definiciones y umbrales oficiales de LCP, CLS e INP |
| Chrome DevTools Performance | `https://developer.chrome.com/docs/devtools/performance` | Análisis de trazas, insights y cascadas de red |
| Lighthouse Performance Scoring | `https://developer.chrome.com/docs/lighthouse/performance/performance-scoring` | Pesos y umbrales de métricas de laboratorio |
| Motor local de rendimiento | [reports/performance/README.md](../../../reports/performance/README.md) | Contratos locales de PageSpeed, CrUX, History, Lighthouse y comparación |

## Seguridad y mapeo de herramientas autorizadas

1. **Prohibido instalar o ejecutar paquetes externos no fijados**: No ejecutes `npx -y chrome-devtools-mcp@latest` ni scripts remotos. El sistema utiliza exclusivamente el servidor DevTools fijado (`chrome-devtools-mcp@1.12.0` con integridad SHA-512 verificada en [devtools.py](../../../tools/ipanema/access/devtools.py)) a través del gateway MCP [gateway.py](../../../tools/ipanema/access/gateway.py) y el CLI [tools/ia.py](../../../tools/ia.py).
2. **Control de origen y parada ante bloqueos**: Toda lectura remota requiere `--allow-network` y URL perteneciente al origen HTTPS registrado del proyecto (o loopback en fixtures locales). Detén inmediatamente ante HTTP `403` o `429` sin reintentos ni evasión.
3. **Redacción de datos sensibles**: Nunca almacenes cabeceras HTTP crudas, cookies, tokens, parámetros secretos ni fragmentos de formularios privados en la evidencia. Por política de seguridad, `get_network_request` con cuerpos o cabeceras crudas no se expone; usa los colectores saneados.

### Correspondencia entre acciones `web-perf` y herramientas del agente

| Acción conceptual (`web-perf`) | Herramienta autorizada (MCP / CLI / Motor) | Alcance y garantías |
|---|---|---|
| `navigate_page(url)` | `devtools_open` / `python3 tools/ia.py qa --suite page` | Abre URL del origen registrado en perfil efímero aislado |
| `performance_start_trace(autoStop: true, reload: true)` | `devtools_trace` / `python3 tools/ia.py performance local` | Traza de carga en frío con recarga y parada automática |
| `performance_analyze_insight(insightSetId, insightName)` | `devtools_insight` / `lighthouseEvidence` en [performance_evidence.mjs](../../../tools/performance_evidence.mjs) | Extrae `LCPBreakdown`, `CLSCulprits`, `RenderBlocking`, `DocumentLatency`, `NetworkRequestsDepGraph` |
| `list_network_requests(resourceTypes)` | `devtools_network` / `createNetworkRecorder` en [performance_evidence.mjs](../../../tools/performance_evidence.mjs) | Registra solicitudes, tipos, saltos de redirección (`redirect_hop`) y `encoded_bytes` con cabeceras redactadas |
| `take_snapshot(verbose: true)` | `devtools_snapshot` / `collectRendered` en [page_collectors.mjs](../../../tools/page_collectors.mjs) | Árbol accesible, imágenes renderizadas (`currentSrc`, `srcset`, `sizes`, `loading`, `fetchPriority`) y recursos |
| Datos de campo (usuarios reales) | `crux_query_record`, `crux_query_history` / `python3 tools/ia.py performance crux` | LCP, INP, CLS y FCP p75 reales por URL u origen (`PHONE`/`DESKTOP`), sin fallback silencioso |
| Datos de laboratorio y comparación | `psi_run_pagespeed` / `python3 tools/ia.py performance pagespeed`, `local`, `audit`, `compare` | LCP, FCP, CLS, TBT y Speed Index bajo perfil controlado y comparación estricta antes/después |
| Diagnóstico estructurado CWV/Red | `diagnose_web_perf` en [model.py](../../../tools/ipanema/performance/model.py) | Clasifica umbrales CWV, recursos bloqueantes, duplicados, preconnects sin uso, cadenas críticas e imágenes |

## Principios operativos

- **Verifica antes de recomendar**: Confirma en las solicitudes de red (`devtools_network` / `navigation_network`), en el DOM renderizado (`currentSrc`) y en el código fuente antes de afirmar un problema. La presencia en el DOM no prueba descarga ni decodificación.
- **Distingue campo de laboratorio**: Nunca llames INP al TBT de laboratorio. INP requiere datos de campo (CrUX) o medición de interacciones reales; TBT es una métrica de bloqueo del hilo principal en laboratorio.
- **Cuantifica el impacto y omite no-problemas**: Prioriza según el ahorro estimado en milisegundos o bytes transferidos. Si un recurso bloqueante tiene `0 ms` de impacto estimado, regístralo como observación sin impacto (`0 ms`) y no recomiendes cambios innecesarios.
- **Sé específico**: Indica el archivo, selector o recurso exacto, su peso observado y la transformación concreta (por ejemplo, ajustar `sizes`, retirar `loading="lazy"` del elemento LCP o diferir un script específico).
- **Prioriza con criterio**: Si un sitio ya presenta LCP, CLS e INP en rango óptimo (`good`), infórmalo con claridad sin forzar micro-optimizaciones riesgosas.

## Flujo de diagnóstico y optimización (Fases 1 a 6)

```text
Progreso de Auditoría Web Performance:
- [ ] Fase 1: Línea base y traza de rendimiento (campo + laboratorio + traza)
- [ ] Fase 2: Análisis de Core Web Vitals y descomposición de insights
- [ ] Fase 3: Análisis de red, recursos bloqueantes, cascadas e imágenes
- [ ] Fase 4: Snapshot de accesibilidad en carga
- [ ] Fase 5: Análisis de código fuente según plataforma/framework (Shopify, Hydrogen, React, Ipanema)
- [ ] Fase 6: Cambios reversibles autorizados, verificación y comparación antes/después
```

### Fase 1: Línea base y traza de rendimiento

1. Identifica las herramientas y permisos disponibles (`python3 tools/ia.py doctor` y `performance doctor`).
2. Si el acceso de red está autorizado (`--allow-network`) sobre el origen registrado:
   - Captura datos de campo y laboratorio con `python3 tools/ia.py performance audit --all-sources --device mobile --runs 3 --allow-network` o la suite local/remota aplicable.
   - Para diagnóstico interactivo por traza DevTools MCP:
     1. `devtools_open(url: "<target-url-autorizada>")`
     2. `devtools_trace()` (ejecuta `performance_start_trace` con `reload: true, autoStop: true`).
3. Si las herramientas de traza o red no están disponibles o el análisis es offline, continúa con la evidencia local, fixtures o análisis estático del código e informa explícitamente qué mediciones no se recolectaron.

### Fase 2: Análisis de Core Web Vitals y umbrales

Analiza las métricas recolectadas y los insights de la traza con `devtools_insight` (`performance_analyze_insight`) o `lighthouseEvidence` / `diagnose_web_perf`:

| Métrica / Área | Insight DevTools / Auditoría Lighthouse | Qué inspeccionar |
|---|---|---|
| LCP | `LCPBreakdown` / `lcp-breakdown-insight`, `largest-contentful-paint-element` | Sub-partes del LCP: TTFB, retraso de carga del recurso, duración de carga y retraso de renderizado del elemento |
| CLS | `CLSCulprits` / `layout-shift-elements`, `unsized-images` | Elementos que desplazan el layout: imágenes/iframes sin dimensiones, contenido inyectado tardíamente, intercambio de fuentes |
| Bloqueo de renderizado | `RenderBlocking` / `render-blocking-resources`, `render-blocking-insight` | Hojas CSS y scripts síncronos en `<head>` que retrasan el FCP/LCP |
| Latencia del documento | `DocumentLatency` / `server-response-time` | TTFB elevado, redirecciones iniciales o falta de compresión en la respuesta HTML |
| Dependencias de red | `NetworkRequestsDepGraph` / `critical-request-chains`, `lcp-discovery-insight` | Cadenas críticas donde un recurso clave se descubre tarde por depender de otro (CSS `@import`, fuentes o imágenes cargadas desde JS) |

**Umbrales oficiales de referencia (`good` / `needs-improvement` / `poor`):**

- **TTFB**: `< 800 ms` / `800–1800 ms` / `> 1800 ms`
- **FCP**: `< 1800 ms` / `1800–3000 ms` / `> 3000 ms`
- **LCP**: `< 2500 ms` / `2500–4000 ms` / `> 4000 ms`
- **INP** *(campo / interacción)*: `< 200 ms` / `200–500 ms` / `> 500 ms`
- **TBT** *(laboratorio)*: `< 200 ms` / `200–600 ms` / `> 600 ms`
- **CLS**: `< 0.1` / `0.1–0.25` / `> 0.25`
- **Speed Index**: `< 3400 ms` / `3400–5800 ms` / `> 5800 ms`

### Fase 3: Análisis de red, recursos e imágenes responsivas

Inspecciona las solicitudes registradas (`devtools_network`, `navigation_network` o `network-requests`):

1. **Recursos bloqueantes de renderizado**: Scripts y hojas CSS en `<head>` sin `defer`, `async` o atributo `media` pertinente. Ignora aquellos con `0 ms` de ahorro estimado.
2. **Cadenas de dependencias de red (waterfalls)**: Recursos críticos descubiertos tardíamente (por ejemplo, `@import` en CSS, imágenes LCP inyectadas por JavaScript o fuentes referenciadas tras múltiples saltos).
3. **Prioridades de carga e imágenes responsivas**:
   - Comprueba que el elemento LCP real no tenga `loading="lazy"` y cuente con `fetchpriority="high"` (y `<link rel="preload">` solo cuando el recurso no sea descubrible directamente en el HTML inicial).
   - Contrasta `currentSrc`, `srcset`, `sizes`, `naturalWidth` y ancho visible por viewport (`390 px` mobile, `1440 px` desktop) para detectar descargas sobredimensionadas o dobles descargas mobile/desktop.
4. **Solicitudes innecesarias y recursos duplicados**: Detecta URLs descargadas más de una vez, librerías duplicadas o saltos de redirección evitables (`redirect_hop > 0`).
5. **Verificación de `preconnect`**: Si se reporta un `<link rel="preconnect">` sin usar, comprueba si hubo **cero solicitudes** hacia ese origen en la captura de red. Si hubo 0 solicitudes, recomienda eliminarlo; si hubo solicitudes pero tardías, evalúa si el `preconnect` sigue siendo útil.
6. **Payloads y caché**: Identifica bundles JS/CSS sobredimensionados o sin comprimir y activos estáticos sin política de caché efectiva.

### Fase 4: Snapshot de accesibilidad en carga

Captura un snapshot del árbol de accesibilidad (`devtools_snapshot` / `collectRendered`) para identificar brechas de alto nivel observables durante la carga:

- IDs ARIA duplicados o referencias rotas.
- Elementos interactivos sin nombre accesible.
- Problemas evidentes de contraste o pérdida de foco inicial.

*(Nota: Este chequeo rápido no sustituye una auditoría WCAG 2.2 completa ni certifica cumplimiento AA).*

### Fase 5: Análisis de código fuente por plataforma y bundler

Omite esta fase únicamente si se audita un sitio externo sin acceso al código fuente. Cuando exista código local, detecta primero la plataforma y el sistema de construcción:

| Plataforma / Bundler | Archivos e indicadores de detección | Focos principales de optimización |
|---|---|---|
| **Shopify Liquid** | `layout/theme.liquid`, `sections/*.liquid`, `snippets/*.liquid`, `config/settings_schema.json` | Filtros `image_url` / `image_tag` con `widths`, `sizes`, `loading` y `fetchpriority`; scripts de apps en `content_for_header`; CSS crítico por sección; evitar cargar sliders/modales pesados en todas las plantillas |
| **Shopify Hydrogen / Remix** | `package.json` (`@shopify/hydrogen`, `@remix-run/*`), `vite.config.*`, `app/routes/*` | Paralelización de consultas Storefront API en `loader` (`Promise.all`), streaming con `defer`, política de caché (`CacheShort`/`CacheLong`), componente `<Image />` de Hydrogen, reducción de hidratación cliente |
| **Tiendanube / Ipanema** | `layouts/layout.tpl`, `sections/*.tpl`, `snippets/image.tpl`, `config/settings_schema.json` | Reutilización de [image-loading](../../../ipanema-discovery/05-performance/image-loading.md), [javascript](../../../ipanema-discovery/05-performance/javascript.md) y [performance-budgets](../../../ipanema-discovery/05-performance/performance-budgets.md); preservar `LS`, `js-*`, `data-store` y slots del editor |
| **React / Next.js / Vite / Webpack / Rollup / esbuild / Astro** | `webpack.config.*`, `vite.config.*`, `rollup.config.*`, `next.config.*`, `astro.config.*`, `package.json` | Tree-shaking (`mode: 'production'`, `sideEffects`), eliminación de barrel files (`index.js` masivos) e imports completos (`lodash`, `moment`), code-splitting con `import()`, extracción de CSS estático, ajuste de `browserslist`/`core-js` y desactivación de source maps públicos pesados |

### Fase 6: Implementación reversible y comparación antes/después

Cuando la tarea autorice implementar mejoras locales (Nivel 1 en [AGENTS.md](../../../AGENTS.md)):

1. Registra o prepara el plan y la transacción reversible con `python3 tools/ia.py attempt begin --file <archivo> --authorize-local`.
2. Aplica cambios mínimos, seguros y reversibles preservando contratos de comercio, SEO y accesibilidad.
3. Ejecuta las pruebas funcionales y de regresión (`python3 tools/ia.py qa --suite quick` o suite de página/componente).
4. Repite la medición con el **mismo perfil** (`python3 tools/ia.py performance compare ANTES.json DESPUES.json --source lighthouse_local` o `compare metrics`).

## Formato de entrega

Estructura siempre el informe de rendimiento en cuatro bloques verificables:

1. **Resumen de Core Web Vitals y Métricas**: Tabla separando **Campo (CrUX)** y **Laboratorio (Lighthouse/PSI/Traza)** con valor observado, unidad y calificación (`good`, `needs-improvement`, `poor`, `not_measured`).
2. **Problemas Principales Priorizados**: Lista ordenada por impacto cuantificado (alto/medio/bajo en `ms` o `KB`), separando hipótesis de causas confirmadas.
3. **Cambios Implementados o Recomendaciones Accionables**: Archivos exactos, diff aplicado (si fue autorizado) o cambio específico de código/configuración.
4. **Verificación y Comparación Antes/Después**: Pruebas ejecutadas, deltas medidos bajo el mismo perfil y limitaciones o pendientes.
