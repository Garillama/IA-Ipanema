# price-filter

**Identificador:** `snippets:product-list:filters:price-filter` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/product-list/filters/price-filter.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/product-list/filters/price-filter.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | price-filter; unidad price-filter de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | snippets/product-list/filters/property-filters.tpl:L12 |
| Ubicaciones posibles por grafo | templates/pages/category.json, templates/pages/search.json |
| Instancias guardadas | no disponible |
| Dependencias | no disponible como literal |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-filter-input-price-container, js-price-filter-btn, js-price-filter-container, js-price-filter-empty, js-price-filter-input |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | accordion, btn, btn-inline, disabled, filter-accordion, filter-input-price, filter-input-price-container, filters-title, form-control, form-group, form-label, icon-inline, input-clear-content, js-filter-input-price-container, js-price-filter-btn, js-price-filter-container, js-price-filter-empty, js-price-filter-input, price-filter-btn, price-filter-btn-icon, price-filter-container, price-filter-label |
| Atributos data | component, store |
| Semántica directa | form: 1, input: 2, a: 2, button: 1; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/product-list/filters/price-filter.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
