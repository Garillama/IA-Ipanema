# _cart-item

**Identificador:** `snippets:cart:_cart-item` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/cart/_cart-item.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/cart/_cart-item.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | _cart-item; unidad _cart-item de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | sections/main-cart.tpl:L51, snippets/cart/cart-panel.tpl:L12 |
| Ubicaciones posibles por grafo | templates/layout/cart_drawer.json, templates/pages/cart.json |
| Instancias guardadas | no disponible |
| Dependencias | snippets/image.tpl (twig-literal, L19), snippets/modals/modal.tpl (twig-literal, L45), snippets/product/kit-products.tpl (twig-literal, L60), snippets/cart/cart-labels.tpl (twig-literal, L68), snippets/forms/form-input.tpl (twig-literal, L91), nubesdk-slot (platform-component, L11) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-cart-input-spinner, js-cart-item, js-cart-item-non-shippable, js-cart-item-remove, js-cart-item-shippable, js-cart-item-subtotal, js-cart-item-subtotal-compare-price, js-cart-item-subtotal-compare-price-container, js-cart-item-unit-price, js-cart-item-unit-price-compare-price, js-cart-item-unit-price-compare-price-container, js-cart-quantity-btn, js-cart-quantity-input, js-cart-quantity-minus, js-cart-quantity-plus, js-modal-open-private, js-quantity |
| Referencias store.js | L2729, L2730, L2734, L2735, L2795, L2817, L3492, L3580, L3603, L3609, L3612, L3614, L3620, L3627, L3631, L3700 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | align-items-center, btn, btn-link, cart-compare-price-container, cart-item, cart-item-delete, cart-item-delete-button, cart-item-discount-badge, cart-item-image-container, cart-item-info-container, cart-item-kit-link, cart-item-name, cart-item-name-container, cart-item-product-info, cart-item-quantity, cart-item-spinner, cart-item-subtotal, cart-item-totals-container, cart-item-unit-price, cart-item-variant, cart-quantity-btn, cart_page, cart_page_price_class, d-md-block, d-md-none, d-none, endif, grid, grid-3-auto, grid-no-gap, icon-inline, icon-loading, if, item_page_classes, item_type_classes, js-cart-input-spinner, js-cart-item, js-cart-item-remove, js-cart-item-subtotal, js-cart-item-subtotal-compare-price, js-cart-item-subtotal-compare-price-container, js-cart-item-unit-price, js-cart-item-unit-price-compare-price, js-cart-item-unit-price-compare-price-container, js-cart-quantity-btn, js-cart-quantity-minus, js-cart-quantity-plus, js-modal-open-private, price-compare |
| Atributos data | cart-ajax, component, component-value, confirm-remove, gift, item-id, line-item-id, modal-url, store, target |
| Semántica directa | a: 2, button: 3; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 1 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D, E; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/cart/_cart-item.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
