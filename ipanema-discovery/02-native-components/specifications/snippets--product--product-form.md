# product-form

**Identificador:** `snippets:product:product-form` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/product/product-form.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/product/product-form.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | product-form; unidad product-form de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | blocks/product-info.tpl:L15, sections/featured-product.tpl:L54 |
| Ubicaciones posibles por grafo | templates/pages/product.json |
| Instancias guardadas | no disponible |
| Dependencias | snippets/breadcrumbs.tpl (twig-literal, L26), snippets/promotions/compare-price-saved-amount.tpl (twig-literal, L106), snippets/promotions/price-discount-disclaimer.tpl (twig-literal, L111), snippets/product/price-without-taxes.tpl (twig-literal, L115), snippets/payments/payment-discount-price.tpl (twig-literal, L120), snippets/subscriptions/subscription-price.tpl (twig-literal, L131), snippets/payments/installments.tpl (twig-literal, L156), snippets/promotions/gift-promotion-message.tpl (twig-literal, L201), snippets/promotions/promotions-details.tpl (twig-literal, L249), snippets/product/product-variants.tpl (twig-literal, L258), snippets/product/kit-products.tpl (twig-literal, L266), snippets/product/product-quantity.tpl (twig-literal, L289), snippets/subscriptions/subscription-selector.tpl (twig-literal, L292), snippets/placeholders/button-placeholder.tpl (twig-literal, L308), snippets/shipping/shipping-calculator.tpl (twig-literal, L338), snippets/shipping/branches.tpl (twig-literal, L344), snippets/product/product-payment-details.tpl (twig-literal, L357), nubesdk-slot (platform-component, L57), nubesdk-slot (platform-component, L61), nubesdk-slot (platform-component, L69), promotional-price-details (platform-component, L91), nubesdk-slot (platform-component, L144), nubesdk-slot (platform-component, L150), nubesdk-slot (platform-component, L188), nubesdk-slot (platform-component, L192), nubesdk-slot (platform-component, L323), nubesdk-slot (platform-component, L330), nubesdk-slot (platform-component, L350) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | `--stock-color` |
| Hooks JS | js-added-to-cart-product-message, js-addtocart, js-compare-price-display, js-free-shipping-discount-not-combinable, js-free-shipping-minimum-message, js-fullscreen-modal-open, js-kit-selections, js-last-product, js-latest-products-available, js-modal-open-private, js-offer-label, js-offer-percentage, js-payment-discount-installments, js-price-container, js-price-display, js-prod-submit-form, js-product-discount-container, js-product-discount-disclaimer, js-product-form, js-product-name, js-product-payments-container, js-product-sku, js-product-stock, js-ship-free-min-price, js-shipping-minimum-label |
| Referencias store.js | L1701, L2410, L2416, L2446, L2515, L2527, L2532, L2536, L2549, L2553, L2556, L2559, L2561, L2565, L2602, L2614, L2616, L2619, L2755, L2766, L2776, L2777, L2778, L2779, L2797, L2799, L2821, L3050, L3102 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | accent_label_classes, and, btn, btn-big, btn-block, btn-link, btn-primary, buy-button-container, endif, free-shipping-icon, free-shipping-message, grid, grid-auto-1, icon-inline, if, installments_info, isSubscribable, is_kit, js-added-to-cart-product-message, js-addtocart, js-compare-price-display, js-free-shipping-discount-not-combinable, js-free-shipping-minimum-message, js-fullscreen-modal-open, js-kit-selections, js-last-product, js-latest-products-available, js-modal-open-private, js-offer-label, js-offer-percentage, js-payment-discount-installments, js-price-container, js-price-display, js-prod-submit-form, js-product-discount-container, js-product-discount-disclaimer, js-product-form, js-product-name, js-product-payments-container, js-product-sku, js-product-stock, js-ship-free-min-price, js-shipping-minimum-label, list, not, or, product, product-actions, product-added-icon, product-added-message, product-added-message-link, product-added-message-text, product-content, product-form, product-free-shipping, product-free-shipping-body, product-free-shipping-icon, product-free-shipping-inner, product-free-shipping-notice, product-name, product-offer-label, product-payment-discount, product-payment-discount-disclaimer, product-payments-info, product-payments-link, product-price, product-price-compare, product-price-display, product-price-main, product-price-row, product-shipping-calculator, product-shipping-wrapper, product-sku, product-sold-count, product-stock-alert, product-subscription-container, shipping-wrapper, show_product_quantity, state, text-accent, text-stock, variations |
| Atributos data | add-to-cart-label, adding-text, component, contact-label, contact-url, editable-ajax-cart, free-label, kit-class-buyable, kit-label-buyable, kit-label-nostock, limit, no-stock-label, no-stock-text, nosnippet, product-price, shipping-url, store, target, text-plural, text-singular |
| Semántica directa | h2: 1, h1: 1, a: 2, form: 1, input: 3; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D, E; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/product/product-form.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
