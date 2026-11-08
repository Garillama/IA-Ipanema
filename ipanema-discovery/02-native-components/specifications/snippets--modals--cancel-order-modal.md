# cancel-order-modal

**Identificador:** `snippets:modals:cancel-order-modal` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/modals/cancel-order-modal.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/modals/cancel-order-modal.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | cancel-order-modal; unidad cancel-order-modal de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | sections/main-account-order.tpl:L91, sections/main-account-orders.tpl:L171 |
| Ubicaciones posibles por grafo | templates/pages/account/order.json, templates/pages/account/orders.json |
| Instancias guardadas | no disponible |
| Dependencias | snippets/modals/modal.tpl (twig-literal, L9), snippets/forms/form-select.tpl (twig-literal, L42) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-modal-close-private, js-modal-open-private |
| Referencias store.js | L854, L1754, L2934, L2956, L3066 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | btn, btn-block, btn-link, btn-medium, btn-primary, btn-secondary, cancel-order-form, form-actions, form-description, js-modal-close-private, js-modal-open-private |
| Atributos data | target |
| Semántica directa | button: 3, form: 1, input: 2; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/modals/cancel-order-modal.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
