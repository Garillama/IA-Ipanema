# Encabezado

**Identificador:** `sections:header` · **Tipo:** sections · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [sections/header.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/header.tpl:1>). **Schema:** [sections/header.tpl:190](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/header.tpl:190>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Encabezado; unidad header de sections; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | templates/layout/header.json |
| Instancias guardadas | templates/layout/header.json#/header |
| Dependencias | blocks/header-logo.tpl (twig-literal, L138), blocks/header-navigation.tpl (twig-literal, L141), blocks/header-utilities.tpl (twig-literal, L144), blocks/header-navigation.tpl (twig-literal, L170), snippets/notification.tpl (twig-literal, L176), snippets/notification.tpl (twig-literal, L183), snippets/header/header-nav-modals.tpl (twig-literal, L188) |
| Restricciones | {"class": "section-header", "limit": 1, "enabled_on": {"layout_templates": ["header"]}, "locked_blocks": true} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#sections-header-tpl) |
| Desktop dedicado por ID | logo_position_desktop, nav_position_desktop, head_fix_desktop |
| Mobile dedicado por ID | use_different_mobile_position, logo_position_mobile, use_different_mobile_padding, vertical_padding_mobile, horizontal_padding_mobile |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | `--header-background`, `--header-badge-background`, `--header-badge-foreground`, `--header-desktop-nav-background`, `--header-desktop-nav-foreground`, `--header-featured-link-foreground`, `--header-foreground`, `--header-foreground-opacity-10`, `--header-foreground-opacity-20`, `--header-nav-divider-color`, `--header-padding-x`, `--header-padding-x-mobile`, `--header-utilities-foreground`, `--header-vertical-padding`, `--header-vertical-padding-mobile`, `--logo-height-desktop`, `--logo-height-mobile`, `--nav-item-horizontal-padding`, `--nav-item-vertical-padding`, `--utility-icon-size`, `--utility-icon-size-mobile`, `--utility-items-gap` |
| Hooks JS | js-head-main |
| Referencias store.js | L1002, L1336, L1413, L1445, L1647 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | container, d-md-none, endif, head-main, head-row, head-transparent-active, head-transparent-page, header_logo_classes, header_logo_md_classes, header_nav_inline_class, header_search_icon_class, header_search_icon_mobile_class, header_with_categories_classes, if, is_transparent_eligible, js-head-main, list-horizontal, list-item, list-unstyled, main-categories-container, nav-categories-mobile, nav-item, nav-list-link, nav_uppercase, not, page_width, show_text, text-uppercase, utilities-icons |
| Atributos data | normal-style, section-id, section-type, sticky-header, store, transparent-header |
| Semántica directa | ul: 1, li: 1, a: 1; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 47 registros de crawl para este tipo de sección; ver runtime-page-audit |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "header" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
