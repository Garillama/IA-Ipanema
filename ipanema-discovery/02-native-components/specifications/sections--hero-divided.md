# Hero dividido

**Identificador:** `sections:hero-divided` · **Tipo:** sections · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [sections/hero-divided.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/hero-divided.tpl:1>). **Schema:** [sections/hero-divided.tpl:170](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/hero-divided.tpl:170>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Hero dividido; unidad hero-divided de sections; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | no disponible |
| Instancias guardadas | no disponible |
| Dependencias | snippets/image.tpl (twig-literal, L59), snippets/image.tpl (twig-literal, L74), snippets/image.tpl (twig-literal, L90), snippets/image.tpl (twig-literal, L112), snippets/image.tpl (twig-literal, L124), snippets/image.tpl (twig-literal, L137), blocks/ (twig-dynamic-prefix, L159) |
| Restricciones | {"class": "section section-hero"} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#sections-hero-divided-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | use_mobile_image, image_mobile, use_mobile_image_2, image_mobile_2 |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | `--media-overlay-color`, `--media-overlay-opacity` |
| Hooks JS | js-hero-parallax |
| Referencias store.js | L3967, L3988 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | content_animation, content_position_class, d-md-block, d-md-none, d-none, endif, has_responsive_images_1, has_responsive_images_2, hero, hero-divided, hero-divided-image, hero-divided-visual, hero-parallax, if, js-hero-parallax, link, media-content, media-content-animate, media-content-animate-, media-content-floating, media-content-linked, media-link, media-overlay, none, parallax, placeholder, placeholder-fade, section-full-width |
| Atributos data | no disponible |
| Semántica directa | a: 1; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 6 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "hero-divided" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
