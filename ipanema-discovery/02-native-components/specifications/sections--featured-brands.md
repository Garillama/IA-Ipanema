# Marcas destacadas

**Identificador:** `sections:featured-brands` · **Tipo:** sections · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [sections/featured-brands.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/featured-brands.tpl:1>). **Schema:** [sections/featured-brands.tpl:66](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/featured-brands.tpl:66>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Marcas destacadas; unidad featured-brands de sections; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | no disponible |
| Instancias guardadas | no disponible |
| Dependencias | blocks/brand-group.tpl (twig-literal, L54), blocks/ (twig-dynamic-prefix, L56) |
| Restricciones | {"class": "section section-featured-brands", "max_blocks": 20} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#sections-featured-brands-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | use_different_mobile_alignment, text_alignment_mobile |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | `--carousel-section-edge`, `--gutter-container`, `--section-horizontal-padding` |
| Hooks JS | js-carousel-section |
| Referencias store.js | L268 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | align-items-, align-items-md-, align_items_desktop, align_items_mobile, carousel-section-edge, container, d-flex, endif, featured-brands-section, flex-column, if, js-carousel-section, not, page_width, position-relative, section-full-width, section-title-content, text-, text-md-, text_alignment, text_alignment_mobile |
| Atributos data | section-id, store |
| Semántica directa | no disponible (puede provenir de includes); excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "featured-brands" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
