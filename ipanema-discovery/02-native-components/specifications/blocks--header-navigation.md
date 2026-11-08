# Navegación

**Identificador:** `blocks:header-navigation` · **Tipo:** blocks · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [blocks/header-navigation.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/header-navigation.tpl:1>). **Schema:** [blocks/header-navigation.tpl:167](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/header-navigation.tpl:167>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Navegación; unidad header-navigation de blocks; seguir consumidores para su papel en la página |
| Consumidores literales | sections/header.tpl:L141, sections/header.tpl:L170 |
| Ubicaciones posibles por grafo | templates/layout/header.json |
| Instancias guardadas | templates/layout/header.json#/header/navigation |
| Dependencias | blocks/navigation-banner.tpl (twig-literal, L128), snippets/header/header-language.tpl (twig-literal, L155), snippets/header/header-language.tpl (twig-literal, L160) |
| Restricciones | {"limit": 1} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#blocks-header-navigation-tpl) |
| Desktop dedicado por ID | nav_type_desktop, nav_alignment_desktop |
| Mobile dedicado por ID | show_mobile_categories |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-desktop-dropdown, js-desktop-main-categories-col, js-desktop-nav-col, js-desktop-secondary-nav-col, js-nav-desktop-container, js-nav-desktop-list, js-nav-desktop-list-arrow, js-nav-desktop-list-arrow-left, js-nav-desktop-list-arrow-right |
| Referencias store.js | L1273, L1276, L1282, L1296, L1297, L1335, L1337, L1350 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | and, container, desktop-dropdown, desktop-dropdown-container, desktop-list-subitems, disable, endif, featured_link_color, has_dropdown, icon-flip-horizontal, icon-inline, if, is_featured, js-desktop-dropdown, js-desktop-main-categories-col, js-desktop-nav-col, js-desktop-secondary-nav-col, js-nav-desktop-container, js-nav-desktop-list, js-nav-desktop-list-arrow, js-nav-desktop-list-arrow-left, js-nav-desktop-list-arrow-right, list-subitems, list-unstyled, nav-arrow-icon, nav-desktop, nav-desktop-banners, nav-desktop-container, nav-desktop-grid-categories, nav-desktop-grid-main, nav-desktop-list, nav-desktop-list-arrow, nav-desktop-list-arrow-left, nav-desktop-list-arrow-right, nav-desktop-secondary, nav-desktop-secondary-list, nav-dropdown, nav-dropdown-content, nav-item, nav-list-link, nav-list-link-featured, nav-list-link-featured-color, nav-list-link-heading, nav-list-link-icon, nav-main-item, nav_desktop_grid_class, nav_desktop_text_class, nav_inline, nav_type_desktop_class, not, page_width, position-relative, secondary-menu-item, secondary-menu-link |
| Atributos data | no disponible |
| Semántica directa | nav: 2, ul: 7, li: 7, a: 7, button: 2; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "header-navigation" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
