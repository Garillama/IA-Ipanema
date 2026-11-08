# Hero

**Identificador:** `sections:hero` · **Tipo:** sections · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [sections/hero.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/hero.tpl:1>). **Schema:** [sections/hero.tpl:117](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/hero.tpl:117>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Hero; unidad hero de sections; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | templates/pages/home.json |
| Instancias guardadas | templates/pages/home.json#/hero |
| Dependencias | snippets/image.tpl (twig-literal, L53), snippets/image.tpl (twig-literal, L67), snippets/image.tpl (twig-literal, L82), blocks/ (twig-dynamic-prefix, L106) |
| Restricciones | {"class": "section section-hero"} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#sections-hero-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | use_mobile_image, image_mobile |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | `--media-overlay-color`, `--media-overlay-opacity` |
| Hooks JS | js-hero-parallax |
| Referencias store.js | L3967, L3988 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | auto_height, content_animation, content_position_class, d-md-block, d-md-none, d-none, endif, has_responsive_images, hero, hero-parallax, if, js-hero-parallax, link, media, media-auto, media-content, media-content-animate, media-content-animate-, media-content-floating, media-content-linked, media-full-width, media-link, media-overlay, media-visual, none, parallax, placeholder, placeholder-fade, section-full-width |
| Atributos data | no disponible |
| Semántica directa | a: 1; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 3 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 1 registros de crawl para este tipo de sección; ver runtime-page-audit |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "hero" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
