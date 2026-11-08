# Barra de anuncio

**Identificador:** `sections:announcement-bar` · **Tipo:** sections · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [sections/announcement-bar.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/announcement-bar.tpl:1>). **Schema:** [sections/announcement-bar.tpl:92](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/announcement-bar.tpl:92>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Barra de anuncio; unidad announcement-bar de sections; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | no disponible |
| Instancias guardadas | no disponible |
| Dependencias | no disponible como literal |
| Restricciones | {"class": "section-announcement-bar", "limit": 3, "enabled_on": {"layout_templates": ["header"]}} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#sections-announcement-bar-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | use_different_mobile_spacing, mobile_vertical_padding, mobile_horizontal_padding |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | `--adbar-mobile-px`, `--adbar-mobile-py`, `--adbar-px`, `--adbar-py` |
| Hooks JS | js-adbar-item, js-adbar-marquee, js-adbar-marquee-content, js-adbar-slide, js-adbar-slider, js-adbar-slider-next, js-adbar-slider-prev |
| Referencias store.js | L918, L920, L942, L959, L963, L964, L966 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | adbar, adbar-item, adbar-marquee, adbar-marquee-content, adbar-slider, adbar-slider-has-nav, adbar-static, align-items-center, container, d-flex, endif, has_multiple_announcements, if, is_marquee, js-adbar-item, js-adbar-marquee, js-adbar-marquee-content, js-adbar-slide, js-adbar-slider, js-adbar-slider-next, js-adbar-slider-prev, justify-content-center, swiper-button-next, swiper-button-prev, swiper-container, swiper-slide, swiper-wrapper, text-center |
| Atributos data | autoplay, direction, section-id, section-type, speed, store |
| Semántica directa | a: 1, button: 2; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "announcement-bar" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
