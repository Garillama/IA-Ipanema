# Anuncio

**Identificador:** `blocks:announcement` · **Tipo:** blocks · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [blocks/announcement.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/announcement.tpl:1>). **Schema:** [blocks/announcement.tpl:29](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/announcement.tpl:29>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Anuncio; unidad announcement de blocks; seguir consumidores para su papel en la página |
| Consumidores literales | blocks/nav-announcements.tpl:L12, blocks/nav-announcements.tpl:L20 |
| Ubicaciones posibles por grafo | templates/layout/header.json |
| Instancias guardadas | templates/layout/header.json#/navigation_bar_top/nav_announcements/announcement_1, templates/layout/header.json#/navigation_bar_top/nav_announcements/announcement_2, templates/layout/header.json#/navigation_bar_bottom/nav_announcements/announcement_1, templates/layout/header.json#/navigation_bar_bottom/nav_announcements/announcement_2, templates/layout/header.json#/navigation_bar_bottom/nav_announcements/announcement_3, templates/layout/header.json#/navigation_bar_bottom/nav_announcements/announcement_4 |
| Dependencias | no disponible como literal |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#blocks-announcement-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | no disponible en marcado directo |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | announcement, link_class, secondary-menu-item |
| Atributos data | no disponible |
| Semántica directa | li: 1, a: 1; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "announcement" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
