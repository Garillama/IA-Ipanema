# shipping-calculator

**Identificador:** `snippets:shipping:shipping-calculator` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/shipping/shipping-calculator.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/shipping/shipping-calculator.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | shipping-calculator; unidad shipping-calculator de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | snippets/cart/cart-fulfillment.tpl:L27, snippets/product/product-form.tpl:L338 |
| Ubicaciones posibles por grafo | templates/layout/cart_drawer.json, templates/pages/cart.json, templates/pages/product.json |
| Instancias guardadas | no disponible |
| Dependencias | snippets/icon.tpl (twig-literal, L46), snippets/placeholders/shipping-placeholder.tpl (twig-literal, L93), snippets/modals/modal.tpl (twig-literal, L106) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-calculate-shipping, js-calculate-shipping-wording, js-calculating-shipping-wording, js-cart-saved-zipcode, js-country-select, js-modal-open-private, js-modal-shipping-country, js-save-shipping-country, js-ship-calculator-common-error, js-ship-calculator-error, js-ship-calculator-external-error, js-shipping-calculator-change-zipcode, js-shipping-calculator-current-zip, js-shipping-calculator-form, js-shipping-calculator-head, js-shipping-calculator-response, js-shipping-calculator-spinner, js-shipping-calculator-with-zipcode, js-shipping-input, js-shipping-zipcode-help |
| Referencias store.js | L2384, L2632, L2633, L3258, L3263, L3268, L3269, L3272, L3277, L3306, L3314, L3322, L3323, L3337, L3343, L3349, L3357, L3358, L3359, L3360, L3368, L3422, L3427, L3430, L3444, L3449, L3457, L3666, L3682, L3687, L3691, L3706 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | alert, alert-danger, align-items-center, branches, btn, btn-inline, btn-link, btn-medium, btn-outline, btn-primary, cart_zipcode, d-grid, d-inline-block, else, endif, font-small, form-control, form-group, form-label, form-select, form-select-arrow, form-select-icon, form-swap, form-swap-input, form-swap-value, form-swap-value-label, free_shipping_messages_visible, grid-1-auto, icon-inline, if, input-append, invalid-zipcode, js-calculate-shipping, js-calculate-shipping-wording, js-calculating-shipping-wording, js-cart-saved-zipcode, js-country-select, js-modal-open-private, js-save-shipping-country, js-ship-calculator-common-error, js-ship-calculator-error, js-ship-calculator-external-error, js-shipping-calculator-change-zipcode, js-shipping-calculator-current-zip, js-shipping-calculator-form, js-shipping-calculator-head, js-shipping-calculator-response, js-shipping-calculator-spinner, js-shipping-calculator-with-zipcode, js-shipping-input, js-shipping-zipcode-help, list, loading, product_detail, radio-buttons-group, shipping-calculator, shipping-calculator-alerts, shipping-calculator-response, shipping-calculator-response-spaced, store, transition-up, transition-up-active, with-form, with-free-shipping, with-zip |
| Atributos data | country-url, store, target |
| Semántica directa | a: 3, input: 2, button: 2, select: 1; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/shipping/shipping-calculator.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
