# item

**Identificador:** `snippets:product-list:product-item:item` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/product-list/product-item/item.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/product-list/product-item/item.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | item; unidad item de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | blocks/products.tpl:L66, sections/main-products-grid.tpl:L115, sections/main-products-grid.tpl:L154, snippets/product-list/_product-grid.tpl:L9 |
| Ubicaciones posibles por grafo | templates/pages/404.json, templates/pages/category.json, templates/pages/home.json, templates/pages/search.json |
| Instancias guardadas | no disponible |
| Dependencias | snippets/product-list/product-item/item-image.tpl (twig-literal, L102), snippets/subscriptions/subscription-price.tpl (twig-literal, L123), snippets/payments/installments.tpl (twig-literal, L144), snippets/labels.tpl (twig-literal, L159), snippets/payments/payment-discount-price.tpl (twig-literal, L171), snippets/subscriptions/subscription-message.tpl (twig-literal, L180), snippets/product-list/product-item/item-colors.tpl (twig-literal, L199), snippets/product/product-variants.tpl (twig-literal, L214), snippets/product/product-quantity.tpl (twig-literal, L225), snippets/placeholders/button-placeholder.tpl (twig-literal, L229), snippets/product-list/product-item/item-quick-shop.tpl (twig-literal, L237), snippets/structured-data/structured-data.tpl (twig-literal, L247), nubesdk-slot (platform-component, L113), nubesdk-slot (platform-component, L117), nubesdk-slot (platform-component, L119), nubesdk-slot (platform-component, L155), nubesdk-slot (platform-component, L221) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-addtocart, js-compare-price-display, js-item-name, js-item-product, js-item-slide, js-item-variants, js-last-product, js-latest-products-available, js-offer-percentage, js-price-display, js-prod-submit-form, js-product-container, js-product-form, js-product-item-private, js-product-stock |
| Referencias store.js | L1685, L1687, L1701, L1705, L1745, L1747, L1775, L1779, L1831, L2308, L2311, L2416, L2515, L2527, L2532, L2536, L2549, L2559, L2565, L2614, L2616, L2619, L2699, L2709, L2755, L2762, L2766, L2771, L2776, L2777, L2778, L2779, L2799, L2819, L2821, L3102 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | btn, btn-primary, buy-button-container, discount_rate, endif, grid, grid-auto-1, hidden, if, information, item, js-addtocart, js-compare-price-display, js-item-name, js-item-variants, js-last-product, js-latest-products-available, js-offer-percentage, js-price-display, js-prod-submit-form, js-product-form, js-product-item-private, js-product-stock, link, price_compare, price_container, product, product-item, product-item-information, product-item-link, product-item-name, product-item-price, product-item-price-compare, product-item-price-container, product-item-stock-notice, product_item_classes, quickshop-actions, show_product_quantity, state, variations, w-100 |
| Atributos data | add-to-cart-label, adding-text, component, component-value, contact-label, editable-ajax-cart, limit, no-stock-label, no-stock-text, nosnippet, product-id, product-type, quickshop-id, store, target, vap-carrier-ref, variants |
| Semántica directa | a: 1, form: 1, input: 2; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D, E; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/product-list/product-item/item.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
