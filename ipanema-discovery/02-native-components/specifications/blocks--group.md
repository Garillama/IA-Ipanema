# Grupo

**Identificador:** `blocks:group` · **Tipo:** blocks · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [blocks/group.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/group.tpl:1>). **Schema:** [blocks/group.tpl:68](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/group.tpl:68>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Grupo; unidad group de blocks; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | templates/pages/404.json, templates/pages/home.json, templates/pages/product.json |
| Instancias guardadas | templates/pages/home.json#/editorial_1/outer_group, templates/pages/home.json#/editorial_1/outer_group/inner_group, templates/pages/home.json#/banners_2_text_inside/banner_1/group, templates/pages/home.json#/banners_2_text_inside/banner_2/group, templates/pages/home.json#/editorial_2/outer_group, templates/pages/home.json#/editorial_2/outer_group/inner_group |
| Dependencias | blocks/ (twig-dynamic-prefix, L62) |
| Restricciones | {"tags": ["general"], "category": "layout"} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#blocks-group-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | mobile_direction_enabled, mobile_direction |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | no disponible en marcado directo |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | align_class, block-fill, block_width, content_class, d-flex, direction_class, endif, fill, group-block, group-content, if, vertical_align_class |
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
| Ejemplo de localización | `rg -n --fixed-strings "group" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
