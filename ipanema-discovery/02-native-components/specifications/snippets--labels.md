# labels

**Identificador:** `snippets:labels` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/labels.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/labels.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | labels; unidad labels de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | snippets/product/product-image.tpl:L31, snippets/product-list/product-item/item-image.tpl:L153, snippets/product-list/product-item/item.tpl:L159 |
| Ubicaciones posibles por grafo | templates/pages/404.json, templates/pages/category.json, templates/pages/home.json, templates/pages/product.json, templates/pages/search.json |
| Instancias guardadas | no disponible |
| Dependencias | snippets/promotions/promotion-label-text.tpl (twig-literal, L97) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-free-shipping-combines-config, js-free-shipping-minimum-label, js-offer-label-private, js-offer-percentage, js-promotion-label-private, js-shipping-label-private, js-stock-label-private |
| Referencias store.js | L2549, L2590 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | endif, free_shipping, group, hidden, icon-inline, if, js-free-shipping-combines-config, js-free-shipping-minimum-label, js-offer-label-private, js-offer-percentage, js-promotion-label-private, js-shipping-label-private, js-stock-label-private, label, label-icon, label-offer-percentage, label-offer-percentage-text, label-shipping-text, labels, labels_classes, no_stock, not, offer, offer_percentage, offer_percentage_text, product, promotion, shipping, shipping_icon, shipping_text |
| Atributos data | combines, label, nosnippet, promotion-type, store |
| Semántica directa | no disponible (puede provenir de includes); excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/labels.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
