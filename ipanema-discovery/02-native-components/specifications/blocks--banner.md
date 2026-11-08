# Banner

**Identificador:** `blocks:banner` · **Tipo:** blocks · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [blocks/banner.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/banner.tpl:1>). **Schema:** [blocks/banner.tpl:155](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/banner.tpl:155>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Banner; unidad banner de blocks; seguir consumidores para su papel en la página |
| Consumidores literales | sections/banners.tpl:L68 |
| Ubicaciones posibles por grafo | templates/pages/home.json |
| Instancias guardadas | templates/pages/home.json#/banners_4_grid/banner_1, templates/pages/home.json#/banners_4_grid/banner_2, templates/pages/home.json#/banners_4_grid/banner_3, templates/pages/home.json#/banners_4_grid/banner_4, templates/pages/home.json#/banner_full_1/banner_1, templates/pages/home.json#/banners_6_grid/banner_1, templates/pages/home.json#/banners_6_grid/banner_2, templates/pages/home.json#/banners_6_grid/banner_3, templates/pages/home.json#/banners_6_grid/banner_4, templates/pages/home.json#/banners_6_grid/banner_5, templates/pages/home.json#/banners_6_grid/banner_6, templates/pages/home.json#/banner_full_2/banner_1, templates/pages/home.json#/banners_3_text_outside/banner_1, templates/pages/home.json#/banners_3_text_outside/banner_2, templates/pages/home.json#/banners_3_text_outside/banner_3, templates/pages/home.json#/banner_full_3/banner_1, templates/pages/home.json#/banners_2_text_inside/banner_1, templates/pages/home.json#/banners_2_text_inside/banner_2 |
| Dependencias | snippets/image.tpl (twig-literal, L83), snippets/image.tpl (twig-literal, L100), snippets/image.tpl (twig-literal, L117), blocks/ (twig-dynamic-prefix, L148) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#blocks-banner-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | use_mobile_image, image_mobile |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | `--aspect-padding`, `--aspect-padding-md`, `--banner-gap`, `--banner-hpadding`, `--banner-vpadding`, `--media-overlay-color`, `--media-overlay-opacity` |
| Hooks JS | no disponible en marcado directo |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | banner-block, banner-image-container, banner-link-overlay, base_class, content_position_class, crop_class, d-md-block, d-md-none, d-none, else, endif, has_link, has_responsive_images, if, media-content, media-content-floating, media-content-linked, media-link, media-overlay, media-visual, placeholder, placeholder-fade, position-relative, text_alignment_class, text_outside, text_over_image |
| Atributos data | store |
| Semántica directa | a: 1; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 3 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "banner" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
