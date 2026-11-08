# Productos

**Identificador:** `sections:main-products-grid` · **Tipo:** sections · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [sections/main-products-grid.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-products-grid.tpl:1>). **Schema:** [sections/main-products-grid.tpl:175](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-products-grid.tpl:175>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Productos; unidad main-products-grid de sections; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | templates/pages/category.json, templates/pages/search.json |
| Instancias guardadas | templates/pages/category.json#/product_list, templates/pages/search.json#/product_list |
| Dependencias | snippets/product-list/filters/filters-modals.tpl (twig-literal, L70), snippets/product-list/filters/filters-controls.tpl (twig-literal, L77), snippets/product-list/filters/sort-by.tpl (twig-literal, L101), snippets/product-list/product-item/item.tpl (twig-literal, L115), snippets/product-list/pagination.tpl (twig-literal, L122), snippets/product-list/pagination.tpl (twig-literal, L124), snippets/product-list/product-item/item.tpl (twig-literal, L154) |
| Restricciones | {"class": "section section-main-products-grid", "limit": 1, "enabled_on": {"page_templates": ["category", "search"]}, "deletable": false} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#sections-main-products-grid-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | columns_mobile |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | `--section-horizontal-padding` |
| Hooks JS | js-product-table, js-products-list-slider, js-products-list-slider-container, js-products-list-swiper, js-swiper-products-list-next, js-swiper-products-list-pagination, js-swiper-products-list-prev, js-swiper-products-slider |
| Referencias store.js | L165, L166, L168, L196, L211, L212, L215, L1623, L1627 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | and, container, d-md-inline-block, d-none, display_products, endif, flex-nowrap, grid, grid-md-auto-4, grid_desktop_class, grid_mobile_class, has_filters_available, icon-inline, if, js-product-table, js-products-list-slider, js-products-list-slider-container, js-products-list-swiper, js-swiper-products-list-next, js-swiper-products-list-pagination, js-swiper-products-list-prev, js-swiper-products-slider, product-list-sort-by, products-grid, products-grid-empty-message, products-grid-header, products-grid-search-heading, products-grid-search-suggestion, py-4, search-featured-products, section-main-products-grid, slider-arrow, slider-arrow-prev, swiper-button-next, swiper-button-outside, swiper-button-prev, swiper-container, swiper-pagination, swiper-pagination-bullets, swiper-pagination-outside, swiper-products-slider, swiper-wrapper, text-right, w-100 |
| Atributos data | component, desktop-columns, mobile-columns, store, vap-enabled, vap-next |
| Semántica directa | h2: 1, button: 2; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 8 registros de crawl para este tipo de sección; ver runtime-page-audit |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "main-products-grid" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
