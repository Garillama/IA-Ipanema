# Diapositiva

**Identificador:** `blocks:slide` · **Tipo:** blocks · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [blocks/slide.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/slide.tpl:1>). **Schema:** [blocks/slide.tpl:130](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/slide.tpl:130>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Diapositiva; unidad slide de blocks; seguir consumidores para su papel en la página |
| Consumidores literales | sections/slideshow.tpl:L55 |
| Ubicaciones posibles por grafo | no disponible |
| Instancias guardadas | no disponible |
| Dependencias | snippets/image.tpl (twig-literal, L52), snippets/image.tpl (twig-literal, L70), snippets/image.tpl (twig-literal, L89), blocks/ (twig-dynamic-prefix, L123) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#blocks-slide-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | use_mobile_image, image_mobile |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | `--media-overlay-color`, `--media-overlay-opacity` |
| Hooks JS | no disponible en marcado directo |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | content_animation, content_position_class, d-md-block, d-md-none, d-none, else, endif, has_image, has_link, has_responsive_images, if, media, media-auto, media-content, media-content-animate, media-content-animate-, media-content-floating, media-content-linked, media-link, media-overlay, media-visual, no_image_classes, none, or, placeholder, placeholder-fade, show_placeholder, slide_auto_height, swiper-slide |
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
| Ejemplo de localización | `rg -n --fixed-strings "slide" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
