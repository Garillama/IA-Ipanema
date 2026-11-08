# Barra de navegación

**Identificador:** `sections:navigation-bar` · **Tipo:** sections · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [sections/navigation-bar.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/navigation-bar.tpl:1>). **Schema:** [sections/navigation-bar.tpl:74](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/navigation-bar.tpl:74>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Barra de navegación; unidad navigation-bar de sections; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | templates/layout/header.json |
| Instancias guardadas | templates/layout/header.json#/navigation_bar_top, templates/layout/header.json#/navigation_bar_bottom |
| Dependencias | blocks/ (twig-dynamic-prefix, L48), blocks/ (twig-dynamic-prefix, L66) |
| Restricciones | {"class": "section-navigation-bar", "limit": 3, "enabled_on": {"layout_templates": ["header"]}, "max_blocks": 3} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#sections-navigation-bar-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | mobile_placement, use_different_mobile_spacing, mobile_vertical_padding, mobile_horizontal_padding |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | `--navbar-bg`, `--navbar-gap`, `--navbar-mobile-px`, `--navbar-mobile-py`, `--navbar-px`, `--navbar-py` |
| Hooks JS | js-navigation-bar, js-navigation-bar-arrow-left, js-navigation-bar-arrow-right, js-navigation-bar-list, js-navigation-bar-mobile |
| Referencias store.js | L1372, L1375, L1380, L1381, L1382, L1392, L1398 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | block, container, d-md-block, d-none, disable, endif, icon-flip-horizontal, icon-inline, if, js-navigation-bar, js-navigation-bar-arrow-left, js-navigation-bar-arrow-right, js-navigation-bar-list, js-navigation-bar-mobile, menu, mobile_placement, nav-arrow-icon, nav-desktop-list-arrow, nav-desktop-list-arrow-left, nav-desktop-list-arrow-right, nav-secondary, navigation-bar, navigation-bar-group, navigation-bar-group-, navigation-bar-inner, navigation-bar-list, type |
| Atributos data | section-id, section-type |
| Semántica directa | button: 2; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 47 registros de crawl para este tipo de sección; ver runtime-page-audit |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "navigation-bar" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
