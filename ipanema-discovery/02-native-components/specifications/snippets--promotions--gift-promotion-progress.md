# gift-promotion-progress

**Identificador:** `snippets:promotions:gift-promotion-progress` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/promotions/gift-promotion-progress.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/promotions/gift-promotion-progress.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | gift-promotion-progress; unidad gift-promotion-progress de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | sections/main-cart.tpl:L60, snippets/cart/cart-summary.tpl:L4, snippets/cart/cart-summary.tpl:L34 |
| Ubicaciones posibles por grafo | templates/layout/cart_drawer.json, templates/pages/cart.json |
| Instancias guardadas | no disponible |
| Dependencias | snippets/progress-bar.tpl (twig-literal, L31) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-gift-progress-desc-accumulation-another, js-gift-progress-desc-accumulation-down-many, js-gift-progress-desc-accumulation-down-one, js-gift-progress-desc-accumulation-down-one-many, js-gift-progress-desc-accumulation-more, js-gift-progress-desc-replacement-down-one, js-gift-progress-desc-replacement-down-one-many, js-gift-progress-desc-replacement-stay, js-gift-progress-desc-replacement-stay-many, js-gift-progress-desc-replacement-up, js-gift-progress-desc-replacement-up-many, js-gift-progress-title-accumulation-all-gifts, js-gift-progress-title-accumulation-all-gifts-one, js-gift-progress-title-accumulation-down-many, js-gift-progress-title-accumulation-down-one, js-gift-progress-title-accumulation-down-one-many, js-gift-progress-title-accumulation-many-gifts, js-gift-progress-title-accumulation-no-gifts, js-gift-progress-title-accumulation-no-gifts-many, js-gift-progress-title-accumulation-one-gift, js-gift-progress-title-accumulation-up, js-gift-progress-title-replacement-all-gifts, js-gift-progress-title-replacement-all-gifts-many, js-gift-progress-title-replacement-down-many, js-gift-progress-title-replacement-down-many-many, js-gift-progress-title-replacement-down-one, js-gift-progress-title-replacement-down-one-many, js-gift-progress-title-replacement-no-gifts, js-gift-progress-title-replacement-no-gifts-many, js-gift-progress-title-replacement-stay, js-gift-progress-title-replacement-stay-many, js-gift-progress-title-replacement-up, js-gift-progress-title-replacement-up-many, js-gift-promotion-progress, js-gift-promotion-progress-amount, js-visible-on-cart-filled |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | box, container_class, gift-promotion-progress, gift-promotion-progress-description, gift-promotion-progress-title, js-gift-progress-desc-accumulation-another, js-gift-progress-desc-accumulation-down-many, js-gift-progress-desc-accumulation-down-one, js-gift-progress-desc-accumulation-down-one-many, js-gift-progress-desc-accumulation-more, js-gift-progress-desc-replacement-down-one, js-gift-progress-desc-replacement-down-one-many, js-gift-progress-desc-replacement-stay, js-gift-progress-desc-replacement-stay-many, js-gift-progress-desc-replacement-up, js-gift-progress-desc-replacement-up-many, js-gift-progress-title-accumulation-all-gifts, js-gift-progress-title-accumulation-all-gifts-one, js-gift-progress-title-accumulation-down-many, js-gift-progress-title-accumulation-down-one, js-gift-progress-title-accumulation-down-one-many, js-gift-progress-title-accumulation-many-gifts, js-gift-progress-title-accumulation-no-gifts, js-gift-progress-title-accumulation-no-gifts-many, js-gift-progress-title-accumulation-one-gift, js-gift-progress-title-accumulation-up, js-gift-progress-title-replacement-all-gifts, js-gift-progress-title-replacement-all-gifts-many, js-gift-progress-title-replacement-down-many, js-gift-progress-title-replacement-down-many-many, js-gift-progress-title-replacement-down-one, js-gift-progress-title-replacement-down-one-many, js-gift-progress-title-replacement-no-gifts, js-gift-progress-title-replacement-no-gifts-many, js-gift-progress-title-replacement-stay, js-gift-progress-title-replacement-stay-many, js-gift-progress-title-replacement-up, js-gift-progress-title-replacement-up-many, js-gift-promotion-progress, js-gift-promotion-progress-amount, js-visible-on-cart-filled |
| Atributos data | gift-progress, gift-units-won, mode, next-tier-gift-units, progress-percentage, reached-tier-count, state, transition |
| Semántica directa | no disponible (puede provenir de includes); excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/promotions/gift-promotion-progress.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
