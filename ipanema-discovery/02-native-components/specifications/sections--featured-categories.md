# Categorías destacadas

**Identificador:** `sections:featured-categories` · **Tipo:** sections · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [sections/featured-categories.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/featured-categories.tpl:1>). **Schema:** [sections/featured-categories.tpl:160](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/featured-categories.tpl:160>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Categorías destacadas; unidad featured-categories de sections; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | templates/pages/home.json |
| Instancias guardadas | templates/pages/home.json#/featured_categories_pills |
| Dependencias | blocks/heading.tpl (twig-literal, L113), blocks/category-item.tpl (twig-literal, L129) |
| Restricciones | {"class": "section section-featured-categories", "locked_blocks": {"reorderable": true}, "max_blocks": 20} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#sections-featured-categories-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | use_different_mobile_orientation, orientation_mobile |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | `--carousel-section-edge`, `--category-bg-color`, `--category-border-color`, `--category-image-border-color`, `--category-image-size`, `--category-text-color`, `--gutter-container`, `--section-horizontal-padding`, `--slide-gap` |
| Hooks JS | js-carousel-next, js-carousel-prev, js-carousel-section, js-carousel-slider |
| Referencias store.js | L265, L268, L278, L279, L3905, L3907 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | carousel-section-edge, center_slides, container, d-flex, desktop_direction, endif, featured-categories-section, flex-grow-1, flex-shrink-0, format_class, gap, heading-column, heading-column-safe-spacing, horizontal, icon-inline, if, js-carousel-next, js-carousel-prev, js-carousel-section, js-carousel-slider, mobile_direction, not, orientation, overflow-hidden, page_width, position-relative, position_class, section-full-width, slider-arrow, slider-arrow-prev, swiper, swiper-button-next, swiper-button-outside, swiper-button-prev, swiper-center-slides, swiper-slide, swiper-wrapper, text-, text_alignment, type_class, w-auto |
| Atributos data | center-slides, columns-mode, section-id, slide-gap, store |
| Semántica directa | button: 2; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 1 registros de crawl para este tipo de sección; ver runtime-page-audit |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "featured-categories" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
