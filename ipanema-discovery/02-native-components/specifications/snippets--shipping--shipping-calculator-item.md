# shipping-calculator-item

**Identificador:** `snippets:shipping:shipping-calculator-item` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/shipping/shipping-calculator-item.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/shipping/shipping-calculator-item.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | shipping-calculator-item; unidad shipping-calculator-item de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | snippets/shipping/_shipping-options.tpl:L72, snippets/shipping/_shipping-options.tpl:L82, snippets/shipping/_shipping-options.tpl:L120, snippets/shipping/_shipping-options.tpl:L130 |
| Ubicaciones posibles por grafo | no disponible |
| Instancias guardadas | no disponible |
| Dependencias | snippets/shipping/_shipping-suboptions.tpl (twig-literal, L61) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-pickup-option, js-shipping-list-item, js-shipping-method, js-shipping-method-hidden, js-shipping-radio |
| Referencias store.js | L3397, L3411, L3415, L3728, L3733, L3736, L3745, L3746 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | alert, alert-warning, box, cart-compare-price-container, checked, cost, d-block, d-grid, endif, featured_option, grid-auto-1, if, js-pickup-option, js-shipping-list-item, js-shipping-method, js-shipping-method-hidden, js-shipping-radio, list-item, not, option, pickup, price-compare, radio-button, radio-button-content, radio-button-icon, radio-button-icons, radio-button-icons-container, radio-button-item, radio-button-label, radio-button-text, shipping-method, shipping-option-branch-extra, shipping-option-date, shipping-option-details, shipping-option-pickup-hours, shipping-option-price, shipping-option-price-free, shipping-option-warning, unchecked, value |
| Atributos data | code, component, cost, loop, name, original-cost, price, shipping-discount, shipping-type, store |
| Semántica directa | li: 2, input: 1, ul: 1; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/shipping/shipping-calculator-item.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
