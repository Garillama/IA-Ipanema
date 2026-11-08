# kit-product-variants

**Identificador:** `snippets:product:kit-product-variants` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/product/kit-product-variants.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/product/kit-product-variants.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | kit-product-variants; unidad kit-product-variants de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | snippets/product/kit-products.tpl:L43 |
| Ubicaciones posibles por grafo | templates/layout/cart_drawer.json, templates/pages/cart.json, templates/pages/product.json |
| Instancias guardadas | no disponible |
| Dependencias | snippets/image.tpl (twig-literal, L32) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-kit-component-variant, js-kit-component-variation-select, js-kit-variation-label |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | and, btn, btn-variant, btn-variant-color, btn-variant-content, btn-variant-content-square, custom_data, d-none, endif, form-group, form-label, form-select, form-select-arrow, form-select-icon, icon-inline, id, if, is_button_variant, is_color, js-kit-component-variant, js-kit-component-variation-select, js-kit-variation-label, option, or, product-kit-variation-group, product-kit-variations, selected, selected_id, use_image_color_variants |
| Atributos data | component, component-value, kit-component-index, name, option, variation-id |
| Semántica directa | select: 1, a: 1; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 1 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/product/kit-product-variants.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
