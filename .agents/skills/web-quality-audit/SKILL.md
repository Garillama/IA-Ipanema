---
name: web-quality-audit
description: Ejecutar auditorías integrales de calidad web basadas en evidencia (rendimiento, accesibilidad, SEO técnico, buenas prácticas, HTML renderizado, navegación e interacción) en Shopify Liquid, Hydrogen/Remix, React y Tiendanube/Ipanema sin duplicar mediciones de rendimiento.
---

# Web Quality Audit (`web-quality-audit`)

Módulo de auditoría integral de calidad web que combina evidencia real de navegador/laboratorio/campo con inspección de código fuente. Integra y adapta la skill oficial de Addy Osmani (`https://github.com/addyosmani/web-quality-skills`, directorio `skills/web-quality-audit`, commit `afa8da942115f2961fdbfa80807ea0b232ff6c00`, `SKILL.md` SHA1 `581ec7c5e8e05e6ac93d99d872906595581efc42`, `scripts/analyze.sh` SHA1 `62b066467d30ed5fa52fc36130a05699e09dd2bb`, licencia `MIT`) bajo las reglas de seguridad, permisos y verificación de [AGENTS.md](../../../AGENTS.md).

## Coordinación y no duplicación

1. **Reutilización del motor de rendimiento**: Esta skill **no duplica** la recolección ni el cálculo de Core Web Vitals, recursos de red o trazas. Reutiliza directamente el motor de [cloudflare-web-perf](../cloudflare-web-perf/SKILL.md) (`diagnose_web_perf` en [model.py](../../../tools/ipanema/performance/model.py)) y el [servicio integrado de rendimiento](../../../reports/performance/README.md) (`PageSpeed`, `CrUX`, `CrUX History`, `Lighthouse local` y `chrome-devtools-mcp@1.12.0`).
2. **Selección por objetivo sin carga redundante**:
   - Si la solicitud trata **exclusivamente de rendimiento** (LCP, CLS, INP, TTFB, FCP, TBT, cascadas de red o bundles), el coordinador selecciona únicamente `cloudflare-web-perf` como skill principal.
   - Si la solicitud pide una **auditoría completa de página, revisión general de calidad web, diagnóstico técnico integral, evaluación multi-categoría de Lighthouse/buenas prácticas o revisión integral de interfaz**, el coordinador selecciona `web-quality-audit` y reutiliza internamente los diagnósticos de rendimiento sin cargar ambas skills en el prompt.
3. **Coordinación con especialidades locales**:
   - Coordinadora general: [ipanema-storefront](../ipanema-storefront/SKILL.md)
   - Rendimiento Ipanema: [ipanema-performance](../ipanema-performance/SKILL.md)
   - SEO y datos estructurados: [ipanema-seo-expert](../ipanema-seo-expert/SKILL.md)
   - QA visual y accesibilidad en navegador: [ipanema-visual-qa](../ipanema-visual-qa/SKILL.md)

## Seguridad y mapeo de herramientas autorizadas

- **Sin ejecución de scripts externos ni instalación no verificada**: El script upstream `scripts/analyze.sh` (dependiente de `jq` y bash externo) no se ejecuta directamente; su inspección de humo de HTML/fuente está integrada de forma segura en Python puro dentro de `audit_web_quality` en [model.py](../../../tools/ipanema/performance/model.py).
- **Sin `evaluate_script` arbitrario en tiendas remotas**: El gateway [devtools.py](../../../tools/ipanema/access/devtools.py) mantiene `--no-javascript-evaluation` y `--redact-network-headers`. Para inspeccionar semántica renderizada, red, consola y trazas, utiliza las herramientas autorizadas del gateway y los colectores locales.

| Necesidad de auditoría | Herramienta preferida en nuestro agente | Alternativa / Fallback |
|---|---|---|
| Rendimiento y Core Web Vitals | `devtools_trace` + `devtools_insight` y `diagnose_web_perf` en [model.py](../../../tools/ipanema/performance/model.py) | `python3 tools/ia.py performance local` o `pagespeed` (`--allow-network`) |
| Rendimiento de usuarios reales (campo) | `python3 tools/ia.py performance crux` / `crux_query_record` (`PHONE`/`DESKTOP`) | `performance history` (series temporales sin inferir causalidad inmediata) |
| Accesibilidad, SEO, Buenas Prácticas y Calidad General | `python3 tools/ia.py performance pagespeed --category performance --category accessibility --category best-practices --category seo` o `qa --suite page --lighthouse` | `python3 tools/ia.py performance quality-audit <report.json>` sobre evidencia capturada |
| Semántica renderizada, consola e interacción | `devtools_open` + `devtools_snapshot` + `devtools_console` + `devtools_network` / [page_collectors.mjs](../../../tools/page_collectors.mjs) | Suite de fixtures locales `python3 tools/ia.py qa --suite fixtures` |
| Inspección estática / smoke test de código fuente | `python3 tools/ia.py performance quality-audit <report.json> --source-file <archivo>` / [audit_source.py](../../../tools/audit_source.py) | Inspección directa del repositorio o tema local |

## Flujo de ejecución de la auditoría integral (9 pasos)

1. **Identificar el sitio, páginas objetivo y framework**: Determinar URLs representativas (home, colección/categoría, producto/PDP, carrito), alcance mobile/desktop y plataforma (`shopify-liquid`, `shopify-hydrogen`, `react-web`, `tiendanube-ipanema`).
2. **Determinar herramientas disponibles**: Comprobar `python3 tools/ia.py doctor` y `performance doctor`. Si no hay autorización de red (`--allow-network`), trabajar sobre evidencia local, fixtures o código fuente documentando la limitación.
3. **Recopilar evidencia real autorizada**: Ejecutar o reutilizar capturas de `performance`, `qa_browser.mjs` o DevTools MCP sin repetir auditorías equivalentes ya recolectadas en la misma sesión.
4. **Clasificar problemas por gravedad, impacto y confianza**: Separar estrictamente:
   - **`verified_by_tool`**: Problemas medidos en tiempo de ejecución (CrUX, Lighthouse/PSI, traza DevTools, red capturada, consola o DOM renderizado con axe/colectores).
   - **`code_hypothesis`**: Problemas detectados únicamente mediante análisis estático de plantillas o código fuente sin confirmación en página renderizada.
5. **Asociar problemas con archivos candidatos según el framework**:
   - **Shopify Liquid**: `layout/theme.liquid`, `sections/*.liquid`, `snippets/*.liquid`, `config/settings_schema.json`.
   - **Shopify Hydrogen / Remix**: `app/root.tsx`, `app/routes/*.tsx`, `vite.config.*`, `package.json`.
   - **React / Web**: `index.html`, `src/**`, `vite.config.*`, `webpack.config.*`.
   - **Tiendanube / Ipanema**: `layouts/layout.tpl`, `sections/*.tpl`, `snippets/image.tpl`, `config/settings_schema.json`.
6. **Proponer correcciones concretas**: Especificar archivo, selector/línea y cambio exacto.
7. **Implementar cambios dentro del alcance autorizado**: Usar transacciones reversibles (`attempt begin/apply/verify/accept`) cuando exista autorización de Nivel 1.
8. **Ejecutar pruebas funcionales y de regresión**: Validar con `python3 tools/ia.py qa --suite quick` y suites de página/componente.
9. **Comparar resultados antes y después**: Usar `python3 tools/ia.py performance compare` o `compare metrics/visual` bajo idéntico perfil. Nunca declarar que una página mejoró sin evidencia comparativa medida.

## Categorías de auditoría integral

### 1. Rendimiento Web (delegado en `cloudflare-web-perf`)
- **Core Web Vitals**: LCP `< 2500 ms`, INP `< 200 ms` (exclusivamente en campo/interacción), CLS `< 0.1`, más métricas diagnósticas TTFB `< 800 ms`, FCP `< 1800 ms` y TBT `< 200 ms` (laboratorio).
- **Optimización de recursos y carga**: Recursos bloqueantes con impacto `> 0 ms`, cadenas críticas de red, imágenes responsivas (`currentSrc`, `srcset`, `sizes`, `fetchpriority="high"` en LCP sin `loading="lazy"`), duplicados y `preconnect` verificados.

### 2. Accesibilidad
- **Perceptible**: Atributo `alt` significativo en `<img>` (`alt=""` en decorativas), contraste de color mínimo WCAG AA (`4.5:1` texto normal, `3:1` texto grande) cuando es medido por axe/Lighthouse.
- **Operable**: Navegación completa por teclado, sin trampas de foco, indicador de foco visible y controles con tamaño táctil adecuado.
- **Comprensible**: Atributo `lang` válido en `<html lang="...">`, etiquetas `<label>` o `aria-label` asociadas en todos los controles de formulario (`input`, `select`, `textarea`).
- **Robusto**: Sin IDs duplicados en el DOM, roles ARIA válidos y nombres accesibles en botones/enlaces.
- *(Nota: La ausencia de errores automatizados en axe/Lighthouse no certifica cumplimiento total WCAG AA; requiere verificación manual y de teclado).*

### 3. SEO Técnico y On-Page
- **Rastreabilidad**: `robots.txt` y sitemap válidos, `<link rel="canonical">` consistente y ausencia de `noindex` accidental en páginas indexables.
- **On-Page**: `<title>` único y descriptivo, `<meta name="description">` presente, jerarquía lógica de encabezados (`<h1>` descriptivo; no marcar HTML válido como roto solo por existir más de un `<h1>` si la estructura semántica lo justifica, pero auditar duplicados involuntarios de plantilla vs. contenido editable), textos de enlace descriptivos (evitar `"clic aquí"` / `"ver más"` / `"click here"` / `"read more"`).
- **Técnico**: HTTPS activo, `<meta name="viewport">` configurado y JSON-LD sin errores de sintaxis ni datos inventados.

### 4. Buenas Prácticas y Errores de Implementación
- **Seguridad y transporte**: HTTPS en todos los recursos (sin contenido mixto `http://` en activos ejecutables o multimedia), ausencia de source maps expuestos en producción (`.map`) y sin credenciales o tokens en URLs.
- **Estándares modernos**: `<!DOCTYPE html>` válido, `<meta charset="UTF-8">` al inicio de `<head>`, ausencia de errores en consola del navegador (`devtools_console`) y sin APIs obsoletas (`document.write`, XHR síncrono).
- **Patrones UX**: Sin intersticiales intrusivos ni botones engañosos.

### 5. Calidad de Navegación, Interacción y Agentic Browsing
- **Estabilidad de layout e interacción**: Ausencia de desbordamiento horizontal (`scrollWidth <= innerWidth`), controles interactivos expuestos en el árbol de accesibilidad con nombre, rol y estado claros.
- **Separación conceptual**: La legibilidad para agentes/asistentes (Agentic Browsing / `llms.txt`) es una señal técnica de estructura semántica, nunca evidencia de indexación ni de posicionamiento en buscadores.

## Niveles de severidad

| Nivel | Descripción | Acción recomendada |
|---|---|---|
| **Critical** | Fallos completos de renderizado/interacción, contenido mixto ejecutable, `noindex` accidental en home/catálogo o vulnerabilidades | Corregir de inmediato |
| **High** | Fallos severos de Core Web Vitals (`poor`), barreras mayores de accesibilidad (controles sin nombre/etiqueta, falta de `lang`), errores JS en consola | Corregir antes de publicar |
| **Medium** | Oportunidades de rendimiento (`needs-improvement`), metadatos SEO incompletos (`canonical`, `description`), imágenes sobredimensionadas | Planificar en la iteración actual |
| **Low** | Mejoras menores de código, advertencias estáticas sin impacto medido en runtime | Corregir cuando sea oportuno |

## Formato de salida de la auditoría

```markdown
## Resultados de Auditoría de Calidad Web (`web-quality-audit`)

### 1. Contexto y Evidencia Recolectada
| Señal / Categoría | Alcance / Condiciones | Resultado | Fuente | Tipo de Evidencia |
|---|---|---|---|---|
| Framework detectado | Inspección de proyecto/petición | `shopify-liquid` / `tiendanube-ipanema` | Coordinador | Verificado |
| LCP / CLS / INP | Móvil / Campo o Laboratorio | Valor + Rating | CrUX / Lighthouse | `verified_by_tool` |
| Accesibilidad / SEO / Best Practices | Móvil / Navegador | Score + Hallazgos | Lighthouse / DOM / axe | `verified_by_tool` |

### 2. Problemas Verificados por Herramientas (`verified_by_tool`)
- **[Severidad] [Categoría]** Descripción del problema (`ID`).
  - **Impacto**: Efecto medido en experiencia, accesibilidad, SEO o estabilidad.
  - **Evidencia**: Métrica, nodo DOM, solicitud de red o mensaje de consola observado.
  - **Archivos candidatos**: `ruta/al/archivo:línea`
  - **Corrección propuesta**: Cambio concreto y reversible.

### 3. Hipótesis Detectadas en Código (`code_hypothesis`)
- **[Severidad] [Categoría]** Patrón detectado en plantilla/código pendiente de confirmar en runtime.

### 4. Resumen por Categoría y Verificación
- **Performance**: Estado y hallazgos (vía `cloudflare-web-perf`).
- **Accessibility**: Estado automatizado y comprobaciones manuales pendientes.
- **SEO**: Estado técnico/on-page (sin afirmar indexación sin GSC).
- **Best Practices & Interacción**: Estado de consola, HTML, transporte y navegación.
```
