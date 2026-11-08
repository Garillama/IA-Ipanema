# _shipping-options

**Identificador:** `snippets:shipping:_shipping-options` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/shipping/_shipping-options.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/shipping/_shipping-options.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | _shipping-options; unidad _shipping-options de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | no disponible |
| Instancias guardadas | no disponible |
| Dependencias | snippets/icon.tpl (twig-literal, L63), snippets/shipping/shipping-calculator-item.tpl (twig-literal, L72), snippets/shipping/shipping-calculator-item.tpl (twig-literal, L82), snippets/icon.tpl (twig-literal, L111), snippets/shipping/shipping-calculator-item.tpl (twig-literal, L120), snippets/shipping/shipping-calculator-item.tpl (twig-literal, L130) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-other-pickup-options, js-other-shipping-options, js-product-shipping-label, js-shipping-see-less, js-shipping-see-more, js-show-more-shipping-options, js-show-other-pickup-options, js-toggle-more-shipping-options |
| Referencias store.js | L3374, L3379, L3380, L3388, L3389, L3747, L3750, L3754, L3757 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | alert, alert-warning, and, btn-link, cart, cart_has_free_shipping, endif, font-small, free_shipping, if, items_count, js-other-pickup-options, js-other-shipping-options, js-product-shipping-label, js-shipping-see-less, js-shipping-see-more, js-show-more-shipping-options, js-show-other-pickup-options, js-toggle-more-shipping-options, list-unstyled, not, radio-button-container, shipping-add-product-notice, shipping-emergency-container, shipping-hidden-options, shipping-options, shipping-options-heading, shipping-toggle-more |
| Atributos data | no disponible |
| Semántica directa | ul: 2, a: 2, input: 2; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/shipping/_shipping-options.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
