# notification

**Identificador:** `snippets:notification` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/notification.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/notification.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | notification; unidad notification de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | layouts/layout.tpl:L79, sections/header.tpl:L176, sections/header.tpl:L183, snippets/cart/add-to-cart-recommendations.tpl:L24 |
| Ubicaciones posibles por grafo | templates/layout/header.json |
| Instancias guardadas | no disponible |
| Dependencias | snippets/image.tpl (twig-literal, L48) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-acknowledge-cookies-private, js-alert-add-to-cart-private, js-cart-counts-plural-private, js-cart-counts-singular-private, js-cart-notification-close-private, js-cart-notification-discount-label, js-cart-notification-discount-percentage, js-cart-notification-item-image-private, js-cart-notification-item-name-private, js-cart-notification-item-price-private, js-cart-notification-item-private, js-cart-notification-item-quantity-private, js-cart-notification-item-variant-container-private, js-cart-notification-item-variant-private, js-cart-total-private, js-cart-widget-amount, js-cart-widget-total, js-modal-close-private, js-notification-cart, js-notification-close-private, js-notification-cookie-private, js-notification-private, js-notification-status-page-close-private, js-notification-status-page-private, js-open-cart-modal |
| Referencias store.js | L854, L1754, L2887, L2891, L2892, L2893, L2899, L2903, L2907, L2908, L2918, L2921, L2934, L2956, L2969, L2987, L2992, L3066, L3520, L3525, L3598, L3768, L3795, L3804, L3818 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | btn, btn-block, btn-link, btn-primary, cart_image_container_classes, cart_item_classes, d-md-grid, grid-1-auto, icon-inline, js-acknowledge-cookies-private, js-alert-add-to-cart-private, js-cart-counts-plural-private, js-cart-counts-singular-private, js-cart-notification-close-private, js-cart-notification-discount-label, js-cart-notification-discount-percentage, js-cart-notification-item-name-private, js-cart-notification-item-price-private, js-cart-notification-item-private, js-cart-notification-item-quantity-private, js-cart-notification-item-variant-container-private, js-cart-notification-item-variant-private, js-cart-total-private, js-cart-widget-amount, js-cart-widget-total, js-modal-close-private, js-notification-cart, js-notification-close-private, js-notification-cookie-private, js-notification-private, js-notification-status-page-close-private, js-notification-status-page-private, js-open-cart-modal, notification, notification-accept-btn, notification-cart-container, notification-cart-discount-badge, notification-cart-discount-label, notification-cart-image-container, notification-cart-inline, notification-cart-item, notification-cart-success, notification-cart-total, notification-close, notification-close-icon, notification-content-wrapper, notification-fixed, notification-fixed-bottom, notification-fixed-md-right, notification-hidden, notification-info-compact, notification-info-container, notification-info-line, notification-link, notification-message, notification-order, pr-3, related_products |
| Atributos data | amplitude-event-name, store, target, url |
| Semántica directa | button: 4, a: 2; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 1 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/notification.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
