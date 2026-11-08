# Mis pedidos

**Identificador:** `sections:main-account-orders` · **Tipo:** sections · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [sections/main-account-orders.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-account-orders.tpl:1>). **Schema:** [sections/main-account-orders.tpl:198](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-account-orders.tpl:198>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Mis pedidos; unidad main-account-orders de sections; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | templates/pages/account/orders.json |
| Instancias guardadas | templates/pages/account/orders.json#/account_orders |
| Dependencias | snippets/subscriptions/subscription-list.tpl (twig-literal, L89), snippets/card.tpl (twig-literal, L108), snippets/modals/cancel-order-modal.tpl (twig-literal, L171), nubesdk-slot (platform-component, L19), nubesdk-slot (platform-component, L106), nubesdk-slot (platform-component, L175), nubesdk-slot (platform-component, L190) |
| Restricciones | {"class": "section section-main-account-orders", "limit": 1, "enabled_on": {"page_templates": ["account/orders"]}} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#sections-main-account-orders-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-card-collapse-toggle |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | account-info-details, account-logout-container, account-order-body, account-order-card, account-order-date, account-order-detail-link, account-order-header-content, account-order-number, account-order-status-container, account-order-status-value, account-order-total, account-orders-empty, account-orders-empty-icon, account-orders-empty-text, account-orders-grid, account-orders-heading, account-orders-section, account-orders-sidebar, account-page-content, account-page-sidebar-wide, account-section-header, account-section-title, alert, alert-danger, alert-success, btn, btn-link, btn-medium, btn-primary, card-img-pill, container, icon-inline, info_spacing, js-card-collapse-toggle, ml-4, order, order-item-image-container, payment_status, status_classes, status_icon_classes |
| Atributos data | store |
| Semántica directa | h6: 2, a: 4; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D, E; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "main-account-orders" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
