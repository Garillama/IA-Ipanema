# subscription-price

**Identificador:** `snippets:subscriptions:subscription-price` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/subscriptions/subscription-price.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/subscriptions/subscription-price.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | subscription-price; unidad subscription-price de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | snippets/product/product-form.tpl:L131, snippets/product-list/product-item/item.tpl:L123 |
| Ubicaciones posibles por grafo | templates/pages/404.json, templates/pages/category.json, templates/pages/home.json, templates/pages/product.json, templates/pages/search.json |
| Instancias guardadas | no disponible |
| Dependencias | snippets/product/price-without-taxes.tpl (twig-literal, L103) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-price-display, js-subscription-discount-private, js-subscription-discount-value-private, js-subscription-price-container-private, js-subscription-price-discount-private, js-subscription-price-original-private, js-subscription-price-private, js-subscription-price-without-taxes |
| Referencias store.js | L2515, L2527, L2532, L2799, L2821 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | container, discount, discount_container, discount_label, discount_value, endif, hidden-important, if, js-subscription-discount-private, js-subscription-discount-value-private, js-subscription-price-container-private, js-subscription-price-discount-private, js-subscription-price-original-private, price_compare, prices_container, should_hide_initially, subscription-price-compare, subscription-price-container, subscription-price-discount, subscription-price-discount-container, subscription-price-discount-label, subscription-price-discount-value, subscription_classes, subscription_price_classes |
| Atributos data | component, product-price |
| Semántica directa | h2: 1; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/subscriptions/subscription-price.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
