# cart-totals

**Identificador:** `snippets:cart:cart-totals` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/cart/cart-totals.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/cart/cart-totals.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | cart-totals; unidad cart-totals de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | snippets/cart/cart-summary.tpl:L47 |
| Ubicaciones posibles por grafo | templates/layout/cart_drawer.json, templates/pages/cart.json |
| Instancias guardadas | no disponible |
| Dependencias | snippets/product/price-without-taxes.tpl (twig-literal, L30), snippets/payments/payment-discount-price.tpl (twig-literal, L145), snippets/payments/installments.tpl (twig-literal, L154), nubesdk-slot (platform-component, L126) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-ajax-cart-total, js-calculating-shipping-cost, js-cart-discount-automatic, js-cart-discount-with-coupon, js-cart-saved-shipping, js-cart-subtotal, js-cart-total, js-cart-total-container, js-coupon-discount-amount, js-coupon-discount-row, js-free-shipping-achieved, js-fulfillment-info, js-promo-all, js-promo-buying, js-promo-discount, js-promo-in, js-promo-units-or-more, js-shipping-cost-empty, js-shipping-cost-table, js-shipping-discount-amount, js-shipping-discount-row, js-subtotal-price, js-total-promotions, js-total-promotions-detail-row, js-visible-on-cart-filled |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | cart, cart-subtotals-container, cart-totals-hint, cart-totals-promotions, cart-totals-row, cart-totals-shipping, cart-totals-subtotal, cart-totals-total, cart_has_free_shipping, endif, free_shipping, hidden, if, js-ajax-cart-total, js-calculating-shipping-cost, js-cart-discount-automatic, js-cart-discount-with-coupon, js-cart-saved-shipping, js-cart-subtotal, js-cart-total, js-cart-total-container, js-coupon-discount-amount, js-coupon-discount-row, js-free-shipping-achieved, js-fulfillment-info, js-promo-all, js-promo-buying, js-promo-discount, js-promo-in, js-promo-units-or-more, js-shipping-cost-empty, js-shipping-cost-table, js-shipping-discount-amount, js-shipping-discount-row, js-subtotal-price, js-total-promotions, js-total-promotions-detail-row, js-visible-on-cart-filled, selected, shipping_data, subtotal-price, total-price |
| Atributos data | component, component-value, coupon-row, free-shipping-wording, priceraw, store |
| Semántica directa | no disponible (puede provenir de includes); excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D, E; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/cart/cart-totals.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
