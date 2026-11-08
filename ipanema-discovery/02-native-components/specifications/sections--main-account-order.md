# Detalle de pedido

**Identificador:** `sections:main-account-order` · **Tipo:** sections · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [sections/main-account-order.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-account-order.tpl:1>). **Schema:** [sections/main-account-order.tpl:182](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-account-order.tpl:182>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Detalle de pedido; unidad main-account-order de sections; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | templates/pages/account/order.json |
| Instancias guardadas | templates/pages/account/order.json#/account_order |
| Dependencias | snippets/subscriptions/subscription-detail.tpl (twig-literal, L20), snippets/subscriptions/subscription-summary.tpl (twig-literal, L89), snippets/modals/cancel-order-modal.tpl (twig-literal, L91), nubesdk-slot (platform-component, L23), nubesdk-slot (platform-component, L25), nubesdk-slot (platform-component, L95), nubesdk-slot (platform-component, L127), nubesdk-slot (platform-component, L171), nubesdk-slot (platform-component, L173) |
| Restricciones | {"class": "section section-main-account-order", "limit": 1, "enabled_on": {"page_templates": ["account/order"]}} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#sections-main-account-order-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | no disponible en marcado directo |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | account-order-section, account-page-content, alert, alert-info, bottom-line, btn, btn-big, btn-primary, container, d-inline-block, d-md-block, d-md-grid, d-md-none, d-none, font-weight-bold, icon-inline, order-detail, order-detail-address, order-detail-icon, order-detail-info, order-detail-items-container, order-detail-line, order-detail-line-compact, order-item, order-item-image-container, order-item-main, order-item-name, order-items-header, order-items-header-center, order-items-header-total, order-total, order-totals-container, totals_text_classes, w-100 |
| Atributos data | store |
| Semántica directa | h4: 1, a: 1; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, E; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "main-account-order" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
