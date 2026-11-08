# newsletter

**Identificador:** `snippets:forms:newsletter` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/forms/newsletter.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/forms/newsletter.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | newsletter; unidad newsletter de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | blocks/newsletter-form.tpl:L7, snippets/promotional-modal.tpl:L84 |
| Ubicaciones posibles por grafo | templates/pages/home.json |
| Instancias guardadas | no disponible |
| Dependencias | snippets/icon.tpl (twig-literal, L48) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-newsletter-error-alert, js-newsletter-form-ajax, js-newsletter-form-spinner, js-newsletter-form-submit, js-newsletter-form-submit-label, js-newsletter-success-alert |
| Referencias store.js | L859, L862, L863, L864, L865 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | ajax_submit, alert, alert-danger, alert-success, endif, form-control, form-spinner, if, input-append, js-newsletter-error-alert, js-newsletter-form-ajax, js-newsletter-form-spinner, js-newsletter-form-submit, js-newsletter-form-submit-label, js-newsletter-success-alert, newsletter-form, newsletter-form-alert, newsletter-form-input, newsletter-form-wrapper, submit_classes, winnie-pooh |
| Atributos data | store |
| Semántica directa | form: 1, input: 5, button: 1; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/forms/newsletter.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
