# Título

**Identificador:** `blocks:heading` · **Tipo:** blocks · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [blocks/heading.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/heading.tpl:1>). **Schema:** [blocks/heading.tpl:43](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/heading.tpl:43>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Título; unidad heading de blocks; seguir consumidores para su papel en la página |
| Consumidores literales | sections/featured-categories.tpl:L113 |
| Ubicaciones posibles por grafo | templates/pages/404.json, templates/pages/home.json, templates/pages/product.json |
| Instancias guardadas | templates/pages/404.json#/featured_products/heading, templates/pages/home.json#/hero/heading, templates/pages/home.json#/banners_4_grid/banner_1/heading, templates/pages/home.json#/banners_4_grid/banner_2/heading, templates/pages/home.json#/banners_4_grid/banner_3/heading, templates/pages/home.json#/banners_4_grid/banner_4/heading, templates/pages/home.json#/banner_full_1/banner_1/heading, templates/pages/home.json#/editorial_1/outer_group/inner_group/heading, templates/pages/home.json#/featured_categories_pills/heading, templates/pages/home.json#/banners_6_grid/banner_1/heading, templates/pages/home.json#/banners_6_grid/banner_2/heading, templates/pages/home.json#/banners_6_grid/banner_3/heading, templates/pages/home.json#/banners_6_grid/banner_4/heading, templates/pages/home.json#/banners_6_grid/banner_5/heading, templates/pages/home.json#/banners_6_grid/banner_6/heading, templates/pages/home.json#/banner_full_2/banner_1/heading, templates/pages/home.json#/banners_3_text_outside/banner_1/heading, templates/pages/home.json#/banners_3_text_outside/banner_2/heading, templates/pages/home.json#/banners_3_text_outside/banner_3/heading, templates/pages/home.json#/banner_full_3/banner_1/heading, templates/pages/home.json#/banners_2_text_inside/banner_1/group/heading, templates/pages/home.json#/banners_2_text_inside/banner_2/group/heading, templates/pages/home.json#/editorial_2/outer_group/inner_group/heading, templates/pages/home.json#/newsletter/heading, templates/pages/product.json#/complementary_products/complementary_heading, templates/pages/product.json#/alternative_products/alternative_heading |
| Dependencias | no disponible como literal |
| Restricciones | {"tags": ["general"], "category": "basic"} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#blocks-heading-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | mobile_font_size, mobile_size, custom_mobile_font_size |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | `--block-font`, `--block-font-size`, `--block-mobile-font-size` |
| Hooks JS | no disponible en marcado directo |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | heading_class |
| Atributos data | store |
| Semántica directa | no disponible (puede provenir de includes); excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "heading" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
