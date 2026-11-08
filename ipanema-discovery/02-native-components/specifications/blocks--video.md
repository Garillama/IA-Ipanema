# Video

**Identificador:** `blocks:video` · **Tipo:** blocks · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [blocks/video.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/video.tpl:1>). **Schema:** [blocks/video.tpl:82](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/video.tpl:82>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Video; unidad video de blocks; seguir consumidores para su papel en la página |
| Consumidores literales | sections/video-with-text.tpl:L58 |
| Ubicaciones posibles por grafo | no disponible |
| Instancias guardadas | no disponible |
| Dependencias | snippets/image.tpl (twig-literal, L59) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#blocks-video-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | use_different_mobile_format, format_mobile |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-video-block, js-video-iframe, js-video-pause-button, js-video-play-button, js-video-thumbnail |
| Referencias store.js | L573, L581, L582, L584, L585, L1973 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | and, autoplay, base_ratio, d-block, d-md-none, desktop_ratio, else, embed-responsive, embed-responsive-, embed-responsive-desktop-, endif, icon-inline, if, js-video-block, js-video-iframe, js-video-pause-button, js-video-play-button, js-video-thumbnail, placeholder, placeholder-fade, placeholder-shine, position-relative, show_mobile_only, video-block, video-block-autoplay, video-block-hide-controls, video-block-iframe, video-block-overlay, video-block-thumbnail, video-block-thumbnail-autoplay, video-play-icon, video-player, video-player-icon, video_id, video_type |
| Atributos data | priority, store, video-id, video-provider, video-type |
| Semántica directa | a: 2; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 1 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "video" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
