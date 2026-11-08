# subscription-product-form

**Identificador:** `snippets:subscriptions:subscription-product-form` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/subscriptions/subscription-product-form.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/subscriptions/subscription-product-form.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | subscription-product-form; unidad subscription-product-form de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | sections/main-account-subscription-product.tpl:L20 |
| Ubicaciones posibles por grafo | templates/pages/account/subscription-product.json |
| Instancias guardadas | no disponible |
| Dependencias | snippets/forms/form-select.tpl (twig-literal, L36), snippets/forms/form-input.tpl (twig-literal, L54), snippets/subscriptions/subscription-product-confirm-modal.tpl (twig-literal, L118) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-modal-open-private, js-quantity, js-quantity-down, js-quantity-input, js-quantity-up, js-subscription-product-container-private, js-subscription-product-discount, js-subscription-product-price, js-subscription-product-price-quantity, js-subscription-product-shipping-note, js-subscription-product-submit, js-subscription-product-summary, js-subscription-product-summary-container, js-subscription-product-total, js-subscription-product-variant-id, js-variation-option |
| Referencias store.js | L1693, L2318, L2703, L2729, L2730, L2734, L2735, L2765, L2795, L2817, L3612, L3614 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | account-section-title, align-items-center, btn, btn-block, btn-primary, font-weight-bold, form-actions, form-label, form-quantity, form-quantity-icon, grid, grid-3-auto, grid-md-2, grid-md-3, grid-no-gap, icon-45px, icon-inline, js-modal-open-private, js-quantity-down, js-quantity-up, js-subscription-product-container-private, js-subscription-product-discount, js-subscription-product-price, js-subscription-product-price-quantity, js-subscription-product-shipping-note, js-subscription-product-submit, js-subscription-product-summary, js-subscription-product-summary-container, js-subscription-product-total, js-subscription-product-variant-id, length, order-detail-icon, order-detail-info, order-detail-line, order-item-image-container, order-item-main, order-item-name, order-total, order-totals-line, product, subscription-product-form, variations |
| Atributos data | component, discount, out-of-stock-label, submit-label, target, unavailable-label, variants |
| Semántica directa | form: 1, input: 2, button: 3, h6: 1; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/subscriptions/subscription-product-form.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
