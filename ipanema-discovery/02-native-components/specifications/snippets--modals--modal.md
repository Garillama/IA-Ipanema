# modal

**Identificador:** `snippets:modals:modal` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/modals/modal.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/modals/modal.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | modal; unidad modal de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | snippets/cart/_cart-item.tpl:L45, snippets/cart/add-to-cart-recommendations.tpl:L9, snippets/cart/add-to-cart-recommendations.tpl:L35, snippets/cart/cart-modal.tpl:L5, snippets/header/header-nav-modals.tpl:L5, snippets/header/header-nav-modals.tpl:L32, snippets/header/header-nav-modals.tpl:L55, snippets/modals/cancel-order-modal.tpl:L9, snippets/modals/quick-shop-modal.tpl:L3, snippets/navigation/navigation-list-hamburger.tpl:L33, snippets/product/product-payment-details.tpl:L4, snippets/product/product-variants.tpl:L104, snippets/product-list/filters/filters-modals.tpl:L41, snippets/product-list/filters/filters-modals.tpl:L66, snippets/promotional-modal.tpl:L26, snippets/shipping/_shipping-suboptions.tpl:L16, snippets/shipping/shipping-calculator.tpl:L106, snippets/subscriptions/subscription-cancel-modal.tpl:L25, snippets/subscriptions/subscription-product-confirm-modal.tpl:L8, snippets/subscriptions/subscription-skip-modal.tpl:L16 |
| Ubicaciones posibles por grafo | templates/layout/cart_drawer.json, templates/layout/header.json, templates/pages/404.json, templates/pages/account/order.json, templates/pages/account/orders.json, templates/pages/account/subscription-product.json, templates/pages/cart.json, templates/pages/category.json, templates/pages/home.json, templates/pages/product.json, templates/pages/search.json |
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
| Hooks JS | js-modal-close-all-private, js-modal-close-private, js-modal-overlay-private, js-modal-private |
| Referencias store.js | L854, L1754, L2934, L2956, L3059, L3066 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | back_button, back_icon, body, close_button, close_icon, footer, form, header, icon-flip-horizontal, js-modal-close-private, js-modal-overlay-private, js-modal-private, modal, modal-, modal-back, modal-body, modal-close, modal-close-icon, modal-footer, modal-form, modal-header, modal-md-width-, modal-overlay, modal-title, modal-width-, modal_classes, modal_close_all_classes, modal_md_position_classes, overlay, position_class, title, width_class, width_md_class |
| Atributos data | component, modal-url, overlay-id, store, target, url |
| Semántica directa | form: 1, button: 3; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/modals/modal.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
