# Carrusel

**Identificador:** `sections:slideshow` · **Tipo:** sections · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [sections/slideshow.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/slideshow.tpl:1>). **Schema:** [sections/slideshow.tpl:84](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/slideshow.tpl:84>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Carrusel; unidad slideshow de sections; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | no disponible |
| Instancias guardadas | no disponible |
| Dependencias | blocks/slide.tpl (twig-literal, L55) |
| Restricciones | {"class": "section section-slideshow", "max_blocks": 10} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#sections-slideshow-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-slideshow, js-slideshow-container, js-swiper-slideshow-next, js-swiper-slideshow-pagination, js-swiper-slideshow-pagination-bullets, js-swiper-slideshow-prev |
| Referencias store.js | L92, L101, L103, L104, L105, L106, L107, L108 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | container, endif, full_width, icon-inline, if, js-slideshow, js-slideshow-container, js-swiper-slideshow-next, js-swiper-slideshow-pagination, js-swiper-slideshow-pagination-bullets, js-swiper-slideshow-prev, position-relative, section-full-width, slider-arrow, slider-arrow-prev, swiper-button-next, swiper-button-prev, swiper-container, swiper-fractions, swiper-pagination, swiper-pagination-bullets, swiper-pagination-current, swiper-pagination-outside, swiper-pagination-total, swiper-wrapper |
| Atributos data | autoplay, priority, section-id, speed, store |
| Semántica directa | button: 2; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "slideshow" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
