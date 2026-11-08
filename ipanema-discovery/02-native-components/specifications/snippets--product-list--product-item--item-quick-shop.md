# item-quick-shop

**Identificador:** `snippets:product-list:product-item:item-quick-shop` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/product-list/product-item/item-quick-shop.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/product-list/product-item/item-quick-shop.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | item-quick-shop; unidad item-quick-shop de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | snippets/product-list/product-item/item.tpl:L237 |
| Ubicaciones posibles por grafo | templates/pages/404.json, templates/pages/category.json, templates/pages/home.json, templates/pages/search.json |
| Instancias guardadas | no disponible |
| Dependencias | snippets/placeholders/button-placeholder.tpl (twig-literal, L39) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-addtocart, js-item-submit-container, js-modal-open-private, js-open-quickshop-wording, js-prod-submit-form, js-product-form, js-product-item-subscription-quickshop-link, js-quickshop-modal-open, js-quickshop-slide |
| Referencias store.js | L1701, L1740, L1744, L2565, L2755, L2766, L2775, L2776, L2777, L2778, L2779, L3102 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | btn, btn-primary, btn-small, item-submit-container, js-addtocart, js-item-submit-container, js-open-quickshop-wording, js-prod-submit-form, js-product-form, js-product-item-subscription-quickshop-link, position-relative, product-item-quick-shop-container, product-item-quick-shop-modal-trigger, quick_shop_trigger_class, state |
| Atributos data | component, component-value |
| Semántica directa | a: 1, form: 1, input: 2; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/product-list/product-item/item-quick-shop.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
