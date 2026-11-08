# Formulario de carrito

**Identificador:** `sections:main-cart` · **Tipo:** sections · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [sections/main-cart.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-cart.tpl:1>). **Schema:** [sections/main-cart.tpl:97](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-cart.tpl:97>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Formulario de carrito; unidad main-cart de sections; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | templates/pages/cart.json |
| Instancias guardadas | templates/pages/cart.json#/cart_form |
| Dependencias | snippets/forms/alert.tpl (twig-literal, L22), snippets/cart/_cart-item.tpl (twig-literal, L51), snippets/promotions/gift-promotion-progress.tpl (twig-literal, L60), snippets/shipping/shipping-free-rest.tpl (twig-literal, L65), snippets/cart/cart-fulfillment.tpl (twig-literal, L72), snippets/cart/cart-summary.tpl (twig-literal, L79), nubesdk-slot (platform-component, L46), nubesdk-slot (platform-component, L56), nubesdk-slot (platform-component, L69), nubesdk-slot (platform-component, L75) |
| Restricciones | {"class": "section section-main-cart", "limit": 1, "enabled_on": {"page_templates": ["cart"]}} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#sections-main-cart-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-ajax-cart-list, js-visible-on-cart-filled |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | alert, alert-info, alert-warning, btn-link, cart-form, cart-page-content, cart-page-fulfillment, cart-page-items-list, cart-page-products, cart-page-summary, cart-page-table-header, cart-page-table-header-totals, cart-stock-alert, cart-stock-link, container, d-md-grid, d-md-none, d-none, js-ajax-cart-list, js-visible-on-cart-filled, text-center |
| Atributos data | component, minimum, store |
| Semántica directa | form: 1, a: 1; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D, E; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 1 registros de crawl para este tipo de sección; ver runtime-page-audit |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "main-cart" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
