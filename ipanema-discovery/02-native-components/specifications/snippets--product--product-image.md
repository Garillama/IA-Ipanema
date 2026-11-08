# product-image

**Identificador:** `snippets:product:product-image` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/product/product-image.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/product/product-image.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | product-image; unidad product-image de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | blocks/product-media.tpl:L4, sections/featured-product.tpl:L51 |
| Ubicaciones posibles por grafo | templates/pages/product.json |
| Instancias guardadas | no disponible |
| Dependencias | snippets/labels.tpl (twig-literal, L31), snippets/image.tpl (twig-literal, L58), snippets/product/product-video.tpl (twig-literal, L80), snippets/product/product-video.tpl (twig-literal, L85), snippets/product/product-image-thumbs.tpl (twig-literal, L109), snippets/product/product-video.tpl (twig-literal, L115), nubesdk-slot (platform-component, L26), nubesdk-slot (platform-component, L39), nubesdk-slot (platform-component, L130) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | `--product-images-grid-gap` |
| Hooks JS | js-product-images-thumbs, js-product-slide, js-product-slide-img, js-product-slide-link, js-product-slider, js-product-slider-next, js-product-slider-pagination, js-product-slider-prev, js-product-slider-thumbs, js-product-slider-thumbs-next, js-product-slider-thumbs-prev |
| Referencias store.js | L1931, L1935, L1936, L1947, L1994, L1996, L2005, L2008, L2026, L2027, L2049, L2103, L2647, L2656, L2665, L2668, L2783, L2784 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | bottom, columns_class, else, endif, grid_desktop_hidden_class, icon-inline, if, is_grid, js-product-images-thumbs, js-product-slide, js-product-slide-link, js-product-slider, js-product-slider-next, js-product-slider-pagination, js-product-slider-prev, js-product-slider-thumbs, js-product-slider-thumbs-next, js-product-slider-thumbs-prev, order-md-first, order-md-last, placeholder, placeholder-fade, product-images-grid, product-images-grid-columns-, product-images-slider, product-images-thumbs, product-images-thumbs-horizontal, product-slide-link, product-slider-thumbs, product-thumb-container, slider-arrow, slider-arrow-inline, slider-arrow-prev, slider-slide, swiper-button-inline, swiper-button-next, swiper-button-prev, swiper-container, swiper-fractions, swiper-product-arrow, swiper-product-arrow-next, swiper-product-arrow-prev, swiper-product-thumb, swiper-slide, swiper-wrapper, text-md-center, text-right, thumb-arrow-next, thumb-arrow-prev, thumbnail_position, w-100 |
| Atributos data | direction, fancybox, gallery-format, image, image-position, initial-slide, product-images-amount |
| Semántica directa | a: 1, button: 4; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 1 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D, E; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/product/product-image.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
