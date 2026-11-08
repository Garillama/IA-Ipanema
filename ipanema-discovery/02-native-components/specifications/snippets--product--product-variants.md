# product-variants

**Identificador:** `snippets:product:product-variants` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/product/product-variants.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/product/product-variants.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | product-variants; unidad product-variants de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | snippets/product/product-form.tpl:L258, snippets/product-list/product-item/item.tpl:L214 |
| Ubicaciones posibles por grafo | templates/pages/404.json, templates/pages/category.json, templates/pages/home.json, templates/pages/product.json, templates/pages/search.json |
| Instancias guardadas | no disponible |
| Dependencias | snippets/forms/form-select.tpl (twig-literal, L40), snippets/forms/form-select.tpl (twig-literal, L48), snippets/image.tpl (twig-literal, L63), snippets/image.tpl (twig-literal, L74), snippets/modals/modal.tpl (twig-literal, L104) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-color-variants-container, js-insta-variation-label, js-modal-open-private, js-product-quickshop-variants, js-product-variants, js-product-variants-group, js-refresh-installment-data, js-variant-button, js-variation-option |
| Referencias store.js | L1693, L2196, L2197, L2316, L2318, L2333, L2686, L2690, L2703, L2705, L2708, L2765 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | Color, Cor, align-items-center, and, as, btn, btn-link, btn-variant, btn-variant-color, btn-variant-content, btn-variant-content-square, custom_data, default_options, endif, form-label, grid, grid-2, id, if, in, is, js-color-variants-container, js-insta-variation-label, js-modal-open-private, js-product-quickshop-variants, js-product-variants, js-product-variants-group, js-variant-button, name, not, option, or, product, product-detail-variants, product-detail-variants-group, quickshop, same, selected, size-guide, size-guide-label, use_bullet_variants, use_image_color_variants, user-content, variants_group_spacing, variation |
| Atributos data | component, modal-url, name, option, target, variation-id |
| Semántica directa | a: 2; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 2 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/product/product-variants.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
