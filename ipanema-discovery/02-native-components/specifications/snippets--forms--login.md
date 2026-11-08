# login

**Identificador:** `snippets:forms:login` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/forms/login.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/forms/login.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | login; unidad login de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | sections/main-login.tpl:L29 |
| Ubicaciones posibles por grafo | templates/pages/account/login.json |
| Instancias guardadas | no disponible |
| Dependencias | snippets/forms/alert.tpl (twig-literal, L8), snippets/forms/alert.tpl (twig-literal, L14), snippets/forms/alert.tpl (twig-literal, L32), snippets/forms/alert.tpl (twig-literal, L38), snippets/icon.tpl (twig-literal, L83), snippets/forms/alert.tpl (twig-literal, L94) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-account-input, js-account-validation-expired, js-account-validation-pending, js-account-validation-success, js-form, js-form-spinner, js-login-general-error, js-password-hidden, js-password-input, js-password-toggle, js-password-visible, js-resend-validation-error, js-resend-validation-link, js-resend-validation-success, js-too-many-attempts, js-too-many-attempts-countdown |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | alert, alert-danger, btn, btn-big, btn-block, btn-link, btn-primary, form, form-alert-compact, form-alert-spaced, form-control, form-group, form-label, form-login-help, form-login-help-link, form-spinner, form-validation-help, form-validation-link, icon-inline, js-account-input, js-account-validation-pending, js-form, js-form-spinner, js-password-hidden, js-password-input, js-password-toggle, js-password-visible, js-resend-validation-error, js-resend-validation-link, js-resend-validation-success, js-too-many-attempts, js-too-many-attempts-countdown, login-password-help, login-password-help-link, password-toggle, password-toggle-hide, password-toggle-icon, password-toggle-show |
| Atributos data | customer-email, store |
| Semántica directa | button: 3, form: 1, input: 2, a: 3; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/forms/login.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
