# Banners

**Identificador:** `sections:banners` · **Tipo:** sections · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [sections/banners.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/banners.tpl:1>). **Schema:** [sections/banners.tpl:103](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/banners.tpl:103>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Banners; unidad banners de sections; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | templates/pages/home.json |
| Instancias guardadas | templates/pages/home.json#/banners_4_grid, templates/pages/home.json#/banner_full_1, templates/pages/home.json#/banners_6_grid, templates/pages/home.json#/banner_full_2, templates/pages/home.json#/banners_3_text_outside, templates/pages/home.json#/banner_full_3, templates/pages/home.json#/banners_2_text_inside |
| Dependencias | blocks/banner.tpl (twig-literal, L68) |
| Restricciones | {"class": "section section-banners", "enabled_on": {"page_templates": "all", "layout_templates": ["footer"]}} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#sections-banners-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | use_different_mobile_format, format_mobile, columns_mobile, use_different_mobile_aspect_ratio, banner_aspect_ratio_mobile, banner_aspect_ratio_mobile_height |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | `--cols`, `--cols-md`, `--grid-gap`, `--section-horizontal-padding` |
| Hooks JS | js-banners-slider, js-banners-slider-container, js-swiper-banners-next, js-swiper-banners-pagination, js-swiper-banners-prev |
| Referencias store.js | L311, L314, L326, L355, L356 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | banner-item, banners-section, banners-section-full-width, banners-slider-wrapper, container, endif, full_width, icon-inline, if, js-banners-slider, js-banners-slider-container, js-swiper-banners-next, js-swiper-banners-pagination, js-swiper-banners-prev, position-relative, section-full-width, section_arrows_visibility, section_pagination_visibility, section_wrapper_classes, slider-arrow, slider-arrow-prev, swiper-button-next, swiper-button-outside, swiper-button-prev, swiper-container, swiper-pagination, swiper-pagination-bullets, swiper-pagination-outside, swiper-slide, use_slider |
| Atributos data | columns-desktop, columns-mobile, desktop-format, gap-horizontal, mobile-format, section-id, store |
| Semántica directa | button: 2; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 1 registros de crawl para este tipo de sección; ver runtime-page-audit |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "banners" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
