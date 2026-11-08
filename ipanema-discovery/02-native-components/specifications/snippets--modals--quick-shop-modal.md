# quick-shop-modal

**Identificador:** `snippets:modals:quick-shop-modal` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/modals/quick-shop-modal.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/modals/quick-shop-modal.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | quick-shop-modal; unidad quick-shop-modal de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | layouts/layout.tpl:L95 |
| Ubicaciones posibles por grafo | no disponible |
| Instancias guardadas | no disponible |
| Dependencias | snippets/modals/modal.tpl (twig-literal, L3), snippets/image.tpl (twig-literal, L25), snippets/payments/payment-discount-price.tpl (twig-literal, L39) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-compare-price-display, js-item-name, js-item-product, js-item-variants, js-price-display, js-product-container, js-product-item-image-private, js-product-item-private, js-quickshop-container, js-quickshop-image-padding, js-quickshop-img, js-quickshop-spinner |
| Referencias store.js | L1685, L1705, L1712, L1731, L1745, L1775, L1779, L1782, L1831, L1838, L2308, L2311, L2365, L2515, L2527, L2532, L2536, L2559, L2699, L2709, L2713, L2762, L2771, L2799, L2819, L2821 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | font-family-body, grid, grid-md-2, icon-inline, icon-loading, js-compare-price-display, js-item-name, js-item-product, js-item-variants, js-price-display, js-product-container, js-product-item-private, js-quickshop-container, js-quickshop-image-padding, js-quickshop-spinner, price-compare, price-container, quickshop-details, quickshop-form, quickshop-form-container, quickshop-image-container, quickshop-name, quickshop-price, quickshop-price-container, quickshop-price-row, quickshop-spinner |
| Atributos data | product-id, quickshop-id, store, variants |
| Semántica directa | no disponible (puede provenir de includes); excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 1 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/modals/quick-shop-modal.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
