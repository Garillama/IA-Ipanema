# promotional-modal

**Identificador:** `snippets:promotional-modal` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/promotional-modal.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/promotional-modal.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | promotional-modal; unidad promotional-modal de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | layouts/layout.tpl:L107 |
| Ubicaciones posibles por grafo | no disponible |
| Instancias guardadas | no disponible |
| Dependencias | snippets/modals/modal.tpl (twig-literal, L26), snippets/image.tpl (twig-literal, L51), snippets/image.tpl (twig-literal, L59), snippets/forms/newsletter.tpl (twig-literal, L84) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-newsletter-form-wrapper |
| Referencias store.js | L875 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | align-self-, alignment, btn, btn-primary, btn_align, description_size_class, endif, if, image_right, js-newsletter-form-wrapper, media-grid, media-grid-align-start, media-grid-content-left, media-grid-md-horizontal, media-visual, promotional-modal-content, promotional-modal-description, promotional-modal-image-link, promotional-modal-title, text-, title_style, title_style_mobile |
| Atributos data | no disponible |
| Semántica directa | a: 2; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 2 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/promotional-modal.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
