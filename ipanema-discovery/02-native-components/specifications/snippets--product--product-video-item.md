# product-video-item

**Identificador:** `snippets:product:product-video-item` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/product/product-video-item.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/product/product-video-item.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | product-video-item; unidad product-video-item de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | snippets/product/product-video.tpl:L18, snippets/product/product-video.tpl:L25, snippets/product/product-video.tpl:L27 |
| Ubicaciones posibles por grafo | templates/pages/product.json |
| Instancias guardadas | no disponible |
| Dependencias | snippets/image.tpl (twig-literal, L20), snippets/image.tpl (twig-literal, L60), snippets/image.tpl (twig-literal, L71) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-external-video-iframe-container, js-play-button, js-play-native-button, js-product-video-link, js-product-video-modal, js-video, js-video-iframe, js-video-image, js-video-native-image, js-video-product |
| Referencias store.js | L573, L581, L582, L583, L584, L585, L1970, L1973, L2124, L2147, L2153, L2181 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | d-block, d-md-none, d-none, embed-responsive, embed-responsive-16by9, endif, home_main_product, icon-inline, if, is_external_video, is_native_video_home, is_standalone_video, js-external-video-iframe-container, js-play-button, js-product-video-link, js-product-video-modal, js-video, js-video-iframe, js-video-image, js-video-native-image, js-video-product, not, play_button_class, play_visibility_class, product-native-video-container, product-native-video-home, product-video, product-video-embed, product-video-modal, product_native_video, video-image, video-play-icon, video-player, video-player-icon, video-player-icon-small, w-100 |
| Atributos data | fancybox, video-color, video-url, video_uid |
| Semántica directa | a: 2; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 3 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/product/product-video-item.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
