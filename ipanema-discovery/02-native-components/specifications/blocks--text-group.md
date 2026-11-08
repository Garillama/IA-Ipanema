# Texto

**Identificador:** `blocks:text-group` · **Tipo:** blocks · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [blocks/text-group.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/text-group.tpl:1>). **Schema:** [blocks/text-group.tpl:53](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/text-group.tpl:53>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Texto; unidad text-group de blocks; seguir consumidores para su papel en la página |
| Consumidores literales | blocks/image-with-text.tpl:L56, sections/video-with-text.tpl:L65 |
| Ubicaciones posibles por grafo | no disponible |
| Instancias guardadas | no disponible |
| Dependencias | blocks/ (twig-dynamic-prefix, L47) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#blocks-text-group-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | no disponible en marcado directo |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | align_class, d-flex, flex-column, group-block, group-content, text_align_class, vertical_align_class |
| Atributos data | store |
| Semántica directa | no disponible (puede provenir de includes); excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "text-group" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
