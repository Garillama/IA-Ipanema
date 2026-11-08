# Lista de íconos

**Identificador:** `blocks:icon-text-group` · **Tipo:** blocks · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [blocks/icon-text-group.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/icon-text-group.tpl:1>). **Schema:** [blocks/icon-text-group.tpl:56](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/icon-text-group.tpl:56>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Lista de íconos; unidad icon-text-group de blocks; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | templates/pages/home.json |
| Instancias guardadas | templates/pages/home.json#/icon_text/icon_text_group |
| Dependencias | blocks/ (twig-dynamic-prefix, L37) |
| Restricciones | {"limit": 1, "deletable": false} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#blocks-icon-text-group-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | mobile_format, custom_title_mobile, custom_title_mobile_size |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | `--cols-md`, `--grid-gap` |
| Hooks JS | js-icon-text-slider, js-icon-text-slider-container, js-swiper-icon-text-pagination |
| Referencias store.js | L369, L373, L374 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | alignment, d-flex, d-md-none, icon-text-grid, icon-text-group, icon-text-slider-wrapper, js-icon-text-slider, js-icon-text-slider-container, js-swiper-icon-text-pagination, justify-content-center, justify_class, position-relative, swiper-container, swiper-pagination, swiper-pagination-outside, swiper-slide, swiper-wrapper, text-, w-100 |
| Atributos data | gap, store |
| Semántica directa | no disponible (puede provenir de includes); excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "icon-text-group" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
