# payments-info-methods

**Identificador:** `snippets:payments:payments-info-methods` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/payments/payments-info-methods.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/payments/payments-info-methods.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | payments-info-methods; unidad payments-info-methods de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | snippets/payments/payments-info-banks.tpl:L185, snippets/payments/payments-info.tpl:L166 |
| Ubicaciones posibles por grafo | templates/pages/product.json |
| Instancias guardadas | no disponible |
| Dependencias | snippets/image.tpl (twig-literal, L22), snippets/image.tpl (twig-literal, L119) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-compare-price-display, js-discount-disclaimer, js-discount-explanation, js-info-payment-method, js-info-payment-method-container, js-installment-amount, js-installment-price, js-installment-total-price, js-installments-no-discount, js-installments-one-payment, js-payment-discount-installments, js-payment-method-, js-payment-method-discount, js-payment-method-installments-table-title, js-payment-method-title, js-payment-method-title-, js-payment-method-total, js-payment-provider-installments-row, js-payments-table, js-price-with-discount |
| Referencias store.js | L2428, L2429, L2430, L2453, L2461, L2505, L2536, L2559 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | id, info_payment_method_classes, js-compare-price-display, js-discount-disclaimer, js-discount-explanation, js-info-payment-method, js-installment-amount, js-installment-price, js-installment-total-price, js-installments-no-discount, js-installments-one-payment, js-payment-discount-installments, js-payment-method-, js-payment-method-discount, js-payment-method-installments-table-title, js-payment-method-title, js-payment-method-title-, js-payment-method-total, js-payment-provider-installments-row, js-payments-table, js-price-with-discount, paymentMethod, payments-additional-info, payments-disclaimer, payments-explanation, payments-installment-highlight, payments-installments-title, payments-logos, payments-logos-group, payments-method-discount, payments-section-title, payments-table, payments-table-total, payments-total-label, price-compare, table |
| Atributos data | minimum-installment-value, nosnippet, payment-discount |
| Semántica directa | no disponible (puede provenir de includes); excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 2 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/payments/payments-info-methods.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
