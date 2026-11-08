# Newsletter

**Identificador:** `sections:newsletter` · **Tipo:** sections · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [sections/newsletter.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/newsletter.tpl:1>). **Schema:** [sections/newsletter.tpl:143](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/newsletter.tpl:143>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Newsletter; unidad newsletter de sections; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | templates/pages/home.json |
| Instancias guardadas | templates/pages/home.json#/newsletter |
| Dependencias | snippets/image.tpl (twig-literal, L54), snippets/image.tpl (twig-literal, L70), blocks/ (twig-dynamic-prefix, L95), snippets/image.tpl (twig-literal, L113), blocks/ (twig-dynamic-prefix, L132) |
| Restricciones | {"class": "section section-newsletter", "enabled_on": {"page_templates": "all", "layout_templates": ["footer"]}} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#sections-newsletter-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | use_mobile_image, image_mobile |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | `--media-overlay-color`, `--media-overlay-opacity` |
| Hooks JS | no disponible en marcado directo |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | and, background_layout, container, content_left, d-md-block, d-md-none, d-none, elseif, endif, has_responsive_images, if, image, media, media-auto, media-content, media-content-center, media-content-floating, media-content-newsletter, media-full-width, media-grid, media-grid-content-left, media-grid-md-horizontal, media-overlay, media-visual, newsletter-align-, newsletter-section, not, page_width, placeholder, placeholder-fade, section-full-width, settings, text-, text_alignment |
| Atributos data | section-id, store |
| Semántica directa | no disponible (puede provenir de includes); excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 3 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 1 registros de crawl para este tipo de sección; ver runtime-page-audit |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "newsletter" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
