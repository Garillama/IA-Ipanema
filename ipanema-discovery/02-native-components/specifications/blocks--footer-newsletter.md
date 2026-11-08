# Newsletter

**Identificador:** `blocks:footer-newsletter` · **Tipo:** blocks · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [blocks/footer-newsletter.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/footer-newsletter.tpl:1>). **Schema:** [blocks/footer-newsletter.tpl:35](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/footer-newsletter.tpl:35>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Newsletter; unidad footer-newsletter de blocks; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | templates/layout/footer.json |
| Instancias guardadas | templates/layout/footer.json#/footer/newsletter |
| Dependencias | no disponible como literal |
| Restricciones | {"limit": 1, "disabled_on": {"templates": ["password"]}, "deletable": false} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#blocks-footer-newsletter-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | no disponible en marcado directo |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | alert, alert-danger, alert-success, btn, btn-inline, btn-outline, footer-newsletter-container, footer-newsletter-description, footer-newsletter-form, footer-newsletter-title, form-control, input-append, newsletter-form, newsletter-form-alert, newsletter-form-button, newsletter-form-input, newsletter-form-wrapper, user-content, winnie-pooh |
| Atributos data | store |
| Semántica directa | form: 1, input: 6; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "footer-newsletter" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
