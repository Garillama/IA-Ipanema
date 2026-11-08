# Página no encontrada

**Identificador:** `sections:main-404` · **Tipo:** sections · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [sections/main-404.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-404.tpl:1>). **Schema:** [sections/main-404.tpl:31](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-404.tpl:31>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Página no encontrada; unidad main-404 de sections; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | templates/pages/404.json |
| Instancias guardadas | templates/pages/404.json#/main_404 |
| Dependencias | snippets/breadcrumbs.tpl (twig-literal, L20) |
| Restricciones | {"class": "section section-main-404", "limit": 1, "enabled_on": {"page_templates": ["404"]}} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#sections-main-404-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | no disponible en marcado directo |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | container, error-page-container, error-page-header, error-page-subtitle, error-page-title, page-header |
| Atributos data | store |
| Semántica directa | section: 1, h1: 1, h2: 1; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 1 registros de crawl para este tipo de sección; ver runtime-page-audit |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "main-404" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
