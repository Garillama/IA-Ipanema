# Utilidades

**Identificador:** `blocks:header-utilities` · **Tipo:** blocks · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [blocks/header-utilities.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/header-utilities.tpl:1>). **Schema:** [blocks/header-utilities.tpl:101](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/header-utilities.tpl:101>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Utilidades; unidad header-utilities de blocks; seguir consumidores para su papel en la página |
| Consumidores literales | sections/header.tpl:L144 |
| Ubicaciones posibles por grafo | templates/layout/header.json |
| Instancias guardadas | templates/layout/header.json#/header/utilities |
| Dependencias | snippets/icon.tpl (twig-literal, L26), snippets/header/search-form.tpl (twig-literal, L32), snippets/header/header-language.tpl (twig-literal, L39) |
| Restricciones | {"limit": 1} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#blocks-header-utilities-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | use_different_mobile_search, search_type_mobile, use_different_mobile_size, icon_size_mobile, show_account_mobile |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-cart-container, js-cart-widget-amount, js-cart-widget-total, js-header-dropdown, js-header-dropdown-content, js-modal-open-private, js-search-container, js-search-expand-form, js-search-trigger |
| Referencias store.js | L1317, L1318, L1516, L1522, L1526, L1528, L1546, L1547, L1550, L1551, L1560, L1563, L1564, L2907, L2908, L3520, L3525, L3773 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | badge, badge-bottom, bag, cart_icon, d-md-grid, d-md-inline, d-md-inline-block, d-none, desktop-dropdown, desktop-dropdown-small, endif, header-account, header-account-label, header-cart, header-cart-text, header-dropdown-link, header-dropdown-link-featured, header-icon, header-utility, icon-inline, if, js-cart-container, js-cart-widget-amount, js-cart-widget-total, js-header-dropdown, js-header-dropdown-content, js-modal-open-private, js-search-container, js-search-expand-form, js-search-trigger, menu-container, menu-text, nav-dropdown, nav-dropdown-content, nav-dropdown-icon, not, search-container, search-floating-container, search-text, search-trigger, show_account_mobile, utilities-group, utilities-language-desktop, utility-icon, utility-text |
| Atributos data | block-id, block-type, component, modal-url, priceraw, target |
| Semántica directa | button: 3, a: 6; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "header-utilities" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
