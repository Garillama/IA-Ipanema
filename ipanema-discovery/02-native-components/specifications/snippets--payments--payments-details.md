# payments-details

**Identificador:** `snippets:payments:payments-details` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/payments/payments-details.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/payments/payments-details.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | payments-details; unidad payments-details de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | snippets/product/product-payment-details.tpl:L19 |
| Ubicaciones posibles por grafo | templates/pages/product.json |
| Instancias guardadas | no disponible |
| Dependencias | snippets/payments/payments-info-banks.tpl (twig-literal, L45), snippets/payments/payments-info.tpl (twig-literal, L50) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-gw-tab-pane, js-installment-amount, js-installment-price, js-installments-gw-tab, js-modal-tab-discount, js-payments-tab-group, js-refresh-installment-data, js-tab, js-tab-container, js-tab-link, js-tab-panel, js-tabs-content |
| Referencias store.js | L2428, L2429 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | active, endif, first, if, js-gw-tab-pane, js-installment-amount, js-installment-price, js-installments-gw-tab, js-modal-tab-discount, js-payments-tab-group, js-refresh-installment-data, js-tab, js-tab-container, js-tab-link, js-tab-panel, js-tabs-content, loop, payments-discount-badge, tab, tab-content, tab-group, tab-link, tab-panel |
| Atributos data | code, nosnippet |
| Semántica directa | ul: 1, li: 1, a: 1; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/payments/payments-details.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
