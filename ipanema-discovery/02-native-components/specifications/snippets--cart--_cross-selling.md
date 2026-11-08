# _cross-selling

**Identificador:** `snippets:cart:_cross-selling` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/cart/_cross-selling.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/cart/_cross-selling.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | _cross-selling; unidad _cross-selling de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | no disponible |
| Instancias guardadas | no disponible |
| Dependencias | snippets/image.tpl (twig-literal, L28), snippets/placeholders/button-placeholder.tpl (twig-literal, L79) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-addtocart, js-cross-selling-add-to-cart, js-cross-selling-container, js-cross-selling-option-value-, js-cross-selling-original-price, js-cross-selling-prices-container, js-cross-selling-product-image, js-cross-selling-product-name, js-cross-selling-promo-price, js-product-container |
| Referencias store.js | L2565, L2755, L2762, L2766, L2772, L2776, L2777, L2778, L2779, L2806, L2809, L2811, L3016 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | btn, btn-primary, cross-selling-label, cross-selling-original-price, cross-selling-price-item, cross-selling-prices, cross-selling-product-name, cross-selling-promo-price, cross-selling-submit, form-group, form-label, form-select, form-select-arrow, form-select-icon, icon-inline, js-addtocart, js-cross-selling-add-to-cart, js-cross-selling-container, js-cross-selling-original-price, js-cross-selling-prices-container, js-cross-selling-product-name, js-cross-selling-promo-price, js-product-container, label, label-primary, label-top-left, m-auto, position-absolute, position-relative, price-compare, price-container, px-4, py-3 |
| Atributos data | add-to-cart-translation, discount-percentage, not-available-translation, product-id, promotion-id, quantity, variants |
| Semántica directa | h5: 1, h3: 1, form: 1, input: 4, select: 1; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 1 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/cart/_cross-selling.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
