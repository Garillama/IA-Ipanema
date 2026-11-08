# Video

**Identificador:** `sections:video` · **Tipo:** sections · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [sections/video.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/video.tpl:1>). **Schema:** [sections/video.tpl:148](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/video.tpl:148>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Video; unidad video de sections; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | no disponible |
| Instancias guardadas | no disponible |
| Dependencias | snippets/image.tpl (twig-literal, L76), snippets/image.tpl (twig-literal, L104), blocks/ (twig-dynamic-prefix, L136) |
| Restricciones | {"class": "section section-video"} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#sections-video-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | format_mobile |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | `--media-overlay-color`, `--media-overlay-opacity` |
| Hooks JS | js-video-block, js-video-iframe, js-video-pause-button, js-video-play-button, js-video-section, js-video-thumbnail |
| Referencias store.js | L573, L581, L582, L583, L584, L585, L1973 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | and, autoplay, base_ratio, content_position_class, desktop_ratio, else, embed-responsive, embed-responsive-, embed-responsive-desktop-, endif, icon-inline, if, js-video-block, js-video-iframe, js-video-pause-button, js-video-play-button, js-video-section, js-video-thumbnail, link, media, media-content, media-content-floating, media-content-linked, media-full-width, media-link, media-overlay, media-visual, placeholder, placeholder-fade, placeholder-shine, position-relative, section-full-width, settings, video-block, video-block-autoplay, video-block-hide-controls, video-block-iframe, video-block-thumbnail, video-block-thumbnail-autoplay, video-play-icon, video-player, video-player-icon, video-section, video-section-background, video-section-play, video_type |
| Atributos data | priority, section-id, store, video-id, video-provider, video-type |
| Semántica directa | a: 3; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 2 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "video" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
