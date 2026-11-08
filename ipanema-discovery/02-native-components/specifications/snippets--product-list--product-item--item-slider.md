# item-slider

**Identificador:** `snippets:product-list:product-item:item-slider` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/product-list/product-item/item-slider.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/product-list/product-item/item-slider.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | item-slider; unidad item-slider de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | snippets/product-list/product-item/item-image.tpl:L118 |
| Ubicaciones posibles por grafo | templates/pages/404.json, templates/pages/category.json, templates/pages/home.json, templates/pages/search.json |
| Instancias guardadas | no disponible |
| Dependencias | snippets/image.tpl (twig-literal, L21), snippets/image.tpl (twig-literal, L28), snippets/image.tpl (twig-literal, L41) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-product-item-next-container-private, js-product-item-prev-container-private, js-product-item-secondary-image-private, js-product-item-slider-container-private, js-product-item-slider-direction-controls-container, js-product-item-slider-pagination-container-private, js-product-item-slider-pagination-private, js-product-item-slider-slide-private |
| Referencias store.js | L1787, L1789 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | icon-inline, js-product-item-next-container-private, js-product-item-prev-container-private, js-product-item-slider-container-private, js-product-item-slider-direction-controls-container, js-product-item-slider-pagination-container-private, js-product-item-slider-pagination-private, js-product-item-slider-slide-private, placeholder, product-item-next-container, product-item-prev-container, product-item-slider-container, product-item-slider-control, product-item-slider-control-next, product-item-slider-control-prev, product-item-slider-controls-container, product-item-slider-direction-controls-container, product-item-slider-pagination, product-item-slider-pagination-container, product-item-slider-pagination-private, product-item-slider-slide, product-item-slider-wrapper, product_item_image_classes, slider-arrow, slider-arrow-prev, slider_container, slider_control_next_container, slider_control_pagination, slider_control_pagination_container, slider_control_prev_container, slider_controls_container, slider_direction_controls_container, slider_slide, slider_wrapper |
| Atributos data | append-images, image, image-position, images-count, initial-slides, item-slider-id, max-slides |
| Semántica directa | button: 2; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 3 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/product-list/product-item/item-slider.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
