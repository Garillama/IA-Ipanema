# subscription-selector

**Identificador:** `snippets:subscriptions:subscription-selector` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/subscriptions/subscription-selector.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/subscriptions/subscription-selector.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | subscription-selector; unidad subscription-selector de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | snippets/product/product-form.tpl:L292 |
| Ubicaciones posibles por grafo | templates/pages/product.json |
| Instancias guardadas | no disponible |
| Dependencias | snippets/subscriptions/subscription-options.tpl (twig-literal, L40), snippets/forms/radio-button.tpl (twig-literal, L103), snippets/forms/radio-button.tpl (twig-literal, L152), snippets/subscriptions/subscription-alerts.tpl (twig-literal, L172) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-price-display, js-purchase-option-item-private, js-purchase-option-private, js-purchase-options-container-private, js-subscription-frequencies-private, js-subscription-main-option-discount-private, js-subscription-main-option-discount-value-private, js-subscription-main-option-price-private, js-subscription-only-container |
| Referencias store.js | L2515, L2527, L2532, L2799, L2821 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | d-grid, else, endif, grid-1-auto, if, is_subscription, js-price-display, js-purchase-option-item-private, js-purchase-option-private, js-purchase-options-container-private, js-subscription-frequencies-private, js-subscription-main-option-discount-private, js-subscription-main-option-discount-value-private, js-subscription-main-option-price-private, js-subscription-only-container, label, label-primary, label-small, purchase-option-discount, purchase-option-discount-value, purchase-option-info-container, purchase-option-name, purchase-option-price, purchase-options-container, radio-button-container, radio-button-text, subscription-only-container, subscription-option-single |
| Atributos data | buy-wording, buying-wording, combines-with-app-discounts, combines-with-cart-amount-discounts, combines-with-free-shipping, combines-with-price-discounts, combines-with-quantity-discounts, component, payments-wording, product-price, product-status, product-stock, purchase-type, subscription-default-discount, subscription-default-frequency, subscription-default-frequency-option-id, subscription-default-frequency-type, subscription-discount, subscription-only |
| Semántica directa | input: 6; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/subscriptions/subscription-selector.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
