# Productos destacados

**Identificador:** `sections:product-list` · **Tipo:** sections · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [sections/product-list.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/product-list.tpl:1>). **Schema:** [sections/product-list.tpl:79](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/product-list.tpl:79>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Productos destacados; unidad product-list de sections; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | templates/pages/404.json, templates/pages/home.json |
| Instancias guardadas | templates/pages/404.json#/featured_products, templates/pages/home.json#/featured_products_1, templates/pages/home.json#/featured_products_2 |
| Dependencias | blocks/ (twig-dynamic-prefix, L69) |
| Restricciones | {"class": "section section-product-list"} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#sections-product-list-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | `--section-horizontal-padding` |
| Hooks JS | js-products-list-slider |
| Referencias store.js | L165, L196 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | alignment, container, d-flex, endif, flex-column, full_width, if, js-products-list-slider, section-featured-home, section-full-width, text- |
| Atributos data | section-id, store |
| Semántica directa | no disponible (puede provenir de includes); excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 2 registros de crawl para este tipo de sección; ver runtime-page-audit |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "product-list" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
