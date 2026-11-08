# register

**Identificador:** `snippets:forms:register` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/forms/register.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/forms/register.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | register; unidad register de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | sections/main-register.tpl:L25 |
| Ubicaciones posibles por grafo | templates/pages/account/register.json |
| Instancias guardadas | no disponible |
| Dependencias | snippets/forms/alert.tpl (twig-literal, L18), snippets/forms/alert.tpl (twig-literal, L26), snippets/icon.tpl (twig-literal, L124), snippets/forms/recaptcha-script.tpl (twig-literal, L138), nubesdk-slot (platform-component, L39), nubesdk-slot (platform-component, L113), nubesdk-slot (platform-component, L119), nubesdk-slot (platform-component, L128) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-account-input, js-account-validation-pending, js-form, js-form-spinner, js-password-hidden, js-password-input, js-password-toggle, js-password-visible, js-recaptcha-button, js-resend-validation-error, js-resend-validation-link, js-resend-validation-success |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | alert, btn, btn-big, btn-block, btn-link, btn-primary, form, form-alert-compact, form-control, form-group, form-label, form-login-help, form-login-help-link, form-spinner, form-validation-help, form-validation-link, form-validation-text, form-validation-title, g-recaptcha, icon-inline, js-account-input, js-account-validation-pending, js-form, js-form-spinner, js-password-hidden, js-password-input, js-password-toggle, js-password-visible, js-recaptcha-button, js-resend-validation-error, js-resend-validation-link, js-resend-validation-success, notification-danger, notification-left, password-toggle, password-toggle-hide, password-toggle-icon, password-toggle-show |
| Atributos data | callback, customer-email, sitekey, store |
| Semántica directa | h5: 1, button: 2, form: 1, input: 5, a: 3; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D, E; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/forms/register.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
