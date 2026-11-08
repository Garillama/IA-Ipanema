# navigation-list-hamburger

**Identificador:** `snippets:navigation:navigation-list-hamburger` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/navigation/navigation-list-hamburger.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/navigation/navigation-list-hamburger.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | navigation-list-hamburger; unidad navigation-list-hamburger de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | snippets/navigation/navigation-list-hamburger.tpl:L68, snippets/navigation/navigation-panel.tpl:L8 |
| Ubicaciones posibles por grafo | templates/layout/header.json |
| Instancias guardadas | no disponible |
| Dependencias | snippets/modals/modal.tpl (twig-literal, L33), snippets/navigation/navigation-list-hamburger.tpl (twig-literal, L68), blocks/navigation-banner.tpl (twig-literal, L72) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-close-all-nav-modals, js-modal-open-private |
| Referencias store.js | L1192 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | current, icon-inline, item, item-with-subitems, js-modal-open-private, nav-item, nav-list-arrow, nav-list-link, nav-mobile-banner-item, selected |
| Atributos data | component, modal-url, target |
| Semántica directa | button: 1, a: 2; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/navigation/navigation-list-hamburger.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
