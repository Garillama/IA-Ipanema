# Ícono y texto

**Identificador:** `blocks:nav-icon-text-item` · **Tipo:** blocks · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [blocks/nav-icon-text-item.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/nav-icon-text-item.tpl:1>). **Schema:** [blocks/nav-icon-text-item.tpl:48](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/nav-icon-text-item.tpl:48>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Ícono y texto; unidad nav-icon-text-item de blocks; seguir consumidores para su papel en la página |
| Consumidores literales | blocks/nav-icon-text-group.tpl:L15, blocks/nav-icon-text-group.tpl:L23 |
| Ubicaciones posibles por grafo | templates/layout/header.json |
| Instancias guardadas | no disponible |
| Dependencias | snippets/image.tpl (twig-literal, L22), snippets/icon.tpl (twig-literal, L29) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#blocks-nav-icon-text-item-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | no disponible en marcado directo |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | secondary-menu-item, wrapper_class |
| Atributos data | no disponible |
| Semántica directa | li: 1, a: 1; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 1 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "nav-icon-text-item" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
