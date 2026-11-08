# products-section

**Identificador:** `snippets:product-list:products-section` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/product-list/products-section.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/product-list/products-section.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | products-section; unidad products-section de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | blocks/product-recommendations.tpl:L12, blocks/timer-products.tpl:L25, snippets/product/_related-products-notifications.tpl:L21 |
| Ubicaciones posibles por grafo | templates/pages/product.json |
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
| Hooks JS | no disponible en marcado directo |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | container, icon-inline, products-section, products-section-container, products-section-next-container, products-section-prev-container, products-section-slider-container, products-section-slider-control, products-section-slider-control-next, products-section-slider-control-prev, products-section-slider-controls-container, products-section-slider-controls-pagination, products-section-slider-direction-controls-container, products-section-slider-wrapper, products-section-title, products-section-title-container, products_container, section, section_classes, slider-arrow, slider-arrow-prev, slider_container, slider_control_next, slider_control_next_container, slider_control_pagination, slider_control_prev, slider_control_prev_container, slider_controls_container, slider_direction_controls_container, slider_wrapper, title, title_container |
| Atributos data | component, related-amount, store |
| Semántica directa | section: 1, h2: 1; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/product-list/products-section.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
