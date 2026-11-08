# branches

**Identificador:** `snippets:shipping:branches` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/shipping/branches.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/shipping/branches.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | branches; unidad branches de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | snippets/cart/cart-fulfillment.tpl:L33, snippets/product/product-form.tpl:L344 |
| Ubicaciones posibles por grafo | templates/layout/cart_drawer.json, templates/pages/cart.json, templates/pages/product.json |
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
| Hooks JS | js-accordion-private-container, js-accordion-private-content, js-accordion-private-toggle, js-accordion-private-toggle-active, js-accordion-private-toggle-inactive, js-branch-method, js-branch-radio, js-product-branches-container, js-selected-shipping-method, js-shipping-radio, js-toggle-branches |
| Referencias store.js | L3294, L3411, L3717, L3719, L3728, L3729, L3731, L3733, L3736 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | box, branch, branches, branches-header, branches-item, branches-item-name, branches-item-price, branches-toggle-icon, btn, btn-link, cart, checked, code, d-block, d-grid, else, endif, font-small, form-label, grid-auto-1, icon-inline, if, js-accordion-private-container, js-accordion-private-content, js-accordion-private-toggle, js-accordion-private-toggle-active, js-accordion-private-toggle-inactive, js-branch-method, js-branch-radio, js-product-branches-container, js-selected-shipping-method, js-shipping-radio, js-toggle-branches, length, list-item, list-item-content, list-item-small, list-unstyled, product_detail, radio-button, radio-button-container, radio-button-content, radio-button-icon, radio-button-icons, radio-button-icons-container, radio-button-item, radio-button-label, radio-buttons-group, selected, shipping-method, shipping_data, store, unchecked |
| Atributos data | code, cost, loop, name, price, store |
| Semántica directa | button: 1, ul: 1, li: 1, input: 1; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/shipping/branches.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
