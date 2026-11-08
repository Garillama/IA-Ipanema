# Productos

**Identificador:** `blocks:products` · **Tipo:** blocks · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [blocks/products.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/products.tpl:1>). **Schema:** [blocks/products.tpl:86](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/products.tpl:86>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Productos; unidad products de blocks; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | templates/pages/404.json, templates/pages/home.json |
| Instancias guardadas | templates/pages/404.json#/featured_products/products, templates/pages/home.json#/featured_products_1/products, templates/pages/home.json#/featured_products_2/products |
| Dependencias | snippets/product-list/product-item/item.tpl (twig-literal, L66) |
| Restricciones | {"limit": 1, "deletable": false} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#blocks-products-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | use_different_mobile_format, format_mobile, columns_mobile |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-products-list-slider-container, js-products-list-swiper, js-swiper-products-list-next, js-swiper-products-list-pagination, js-swiper-products-list-prev, js-swiper-products-slider |
| Referencias store.js | L166, L168, L196, L211, L212, L215 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | endif, format_mobile, grid, grid_desktop_class, grid_mobile_class, icon-inline, if, js-products-list-slider-container, js-products-list-swiper, js-swiper-products-list-next, js-swiper-products-list-pagination, js-swiper-products-list-prev, not, products-list-slider, section_arrows_visibility_classes, section_pagination_visibility_classes, section_slider_classes, slider-arrow, slider-arrow-prev, slider_both, swiper-button-next, swiper-button-outside, swiper-button-prev, swiper-container, swiper-pagination, swiper-pagination-bullets, swiper-pagination-outside, swiper-wrapper, use_slider, w-100 |
| Atributos data | desktop-columns, desktop-format, mobile-columns, mobile-format |
| Semántica directa | button: 2; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "products" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
