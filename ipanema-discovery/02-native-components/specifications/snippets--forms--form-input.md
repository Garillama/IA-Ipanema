# form-input

**Identificador:** `snippets:forms:form-input` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/forms/form-input.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/forms/form-input.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | form-input; unidad form-input de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | sections/main-account-address.tpl:L29, sections/main-account-address.tpl:L43, sections/main-account-address.tpl:L52, sections/main-account-address.tpl:L60, sections/main-account-address.tpl:L68, sections/main-account-address.tpl:L77, sections/main-account-address.tpl:L85, sections/main-account-address.tpl:L93, sections/main-account-address.tpl:L110, sections/main-account-info.tpl:L24, sections/main-account-info.tpl:L32, sections/main-account-info.tpl:L42, sections/main-contact.tpl:L145, sections/main-contact.tpl:L148, sections/main-contact.tpl:L152, sections/main-contact.tpl:L155, sections/main-newpass.tpl:L46, sections/main-newpass.tpl:L49, sections/main-password.tpl:L24, sections/main-reset.tpl:L28, snippets/cart/_cart-item.tpl:L91, snippets/product/product-quantity.tpl:L9, snippets/subscriptions/subscription-address-form.tpl:L22, snippets/subscriptions/subscription-address-form.tpl:L37, snippets/subscriptions/subscription-address-form.tpl:L51, snippets/subscriptions/subscription-address-form.tpl:L66, snippets/subscriptions/subscription-address-form.tpl:L76, snippets/subscriptions/subscription-address-form.tpl:L90, snippets/subscriptions/subscription-address-form.tpl:L105, snippets/subscriptions/subscription-product-form.tpl:L54 |
| Ubicaciones posibles por grafo | templates/layout/cart_drawer.json, templates/pages/404.json, templates/pages/account/address.json, templates/pages/account/info.json, templates/pages/account/newpass.json, templates/pages/account/reset.json, templates/pages/account/subscription-address.json, templates/pages/account/subscription-product.json, templates/pages/cart.json, templates/pages/category.json, templates/pages/contact.json, templates/pages/home.json, templates/pages/password.json, templates/pages/product.json, templates/pages/search.json |
| Instancias guardadas | no disponible |
| Dependencias | no disponible como literal |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-password-hidden, js-password-input, js-password-toggle, js-password-visible |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | btn-link, endif, form-control, form-control-area, form-control-container, form-control-disabled, form-control-inline, form-group, form-input-help, form-label, form_control_container_custom_class, icon-inline, if, input_append_content, input_custom_class, input_disabled, input_group_custom_class, input_label_custom_class, input_link_class, js-password-hidden, js-password-input, js-password-toggle, js-password-visible, password-toggle, password-toggle-hide, password-toggle-icon, password-toggle-show, type_password |
| Atributos data | component |
| Semántica directa | input: 1, a: 2; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/forms/form-input.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
