# Lista de testimonios

**Identificador:** `blocks:testimonial-group` · **Tipo:** blocks · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [blocks/testimonial-group.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/testimonial-group.tpl:1>). **Schema:** [blocks/testimonial-group.tpl:56](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/testimonial-group.tpl:56>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Lista de testimonios; unidad testimonial-group de blocks; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | no disponible |
| Instancias guardadas | no disponible |
| Dependencias | blocks/ (twig-dynamic-prefix, L31) |
| Restricciones | {"limit": 1, "deletable": false} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#blocks-testimonial-group-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | `--cols`, `--cols-md`, `--grid-gap` |
| Hooks JS | js-swiper-testimonials-next, js-swiper-testimonials-pagination, js-swiper-testimonials-prev, js-testimonials-slider, js-testimonials-slider-container |
| Referencias store.js | L231, L236, L237, L251, L252 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | alignment, center, endif, flex-grid, icon-inline, if, js-swiper-testimonials-next, js-swiper-testimonials-pagination, js-swiper-testimonials-prev, js-testimonials-slider, js-testimonials-slider-container, justify-items-center, justify-items-end, right, slider-arrow, slider-arrow-prev, swiper-button-next, swiper-button-outside, swiper-button-prev, swiper-container, swiper-pagination, swiper-pagination-outside, swiper-slide, swiper-testimonials-pagination, swiper-wrapper, testimonial-group, testimonials-slider-wrapper, text- |
| Atributos data | columns-desktop, gap, store |
| Semántica directa | button: 2; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "testimonial-group" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
