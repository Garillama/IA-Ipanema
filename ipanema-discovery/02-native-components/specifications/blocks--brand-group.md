# Marcas

**Identificador:** `blocks:brand-group` · **Tipo:** blocks · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [blocks/brand-group.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/brand-group.tpl:1>). **Schema:** [blocks/brand-group.tpl:41](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/brand-group.tpl:41>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Marcas; unidad brand-group de blocks; seguir consumidores para su papel en la página |
| Consumidores literales | sections/featured-brands.tpl:L54 |
| Ubicaciones posibles por grafo | no disponible |
| Instancias guardadas | no disponible |
| Dependencias | blocks/brand-logo.tpl (twig-literal, L24) |
| Restricciones | {"limit": 1, "deletable": false} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#blocks-brand-group-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | `--brand-logo-gap` |
| Hooks JS | js-carousel-next, js-carousel-prev, js-carousel-slider |
| Referencias store.js | L265, L278, L279, L3905, L3907 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | brand-logo-slide, icon-inline, js-carousel-next, js-carousel-prev, js-carousel-slider, overflow-hidden, position-relative, slider-arrow, slider-arrow-prev, swiper, swiper-button-next, swiper-button-outside, swiper-button-prev, swiper-slide, swiper-wrapper, w-100 |
| Atributos data | center-slides, columns-mode, slide-gap |
| Semántica directa | button: 2; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "brand-group" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
