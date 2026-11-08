# icon

**Identificador:** `snippets:icon` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/icon.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/icon.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | icon; unidad icon de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | blocks/accordion.tpl:L13, blocks/accordion.tpl:L18, blocks/header-utilities.tpl:L26, blocks/icon-text-item.tpl:L40, blocks/nav-icon-text-item.tpl:L29, snippets/forms/login.tpl:L83, snippets/forms/newsletter.tpl:L48, snippets/forms/register.tpl:L124, snippets/header/search-form.tpl:L13, snippets/progress-bar.tpl:L13, snippets/promotions/coupon-input.tpl:L65, snippets/promotions/coupon-input.tpl:L96, snippets/shipping/_shipping-options.tpl:L63, snippets/shipping/_shipping-options.tpl:L111, snippets/shipping/_shipping-suboptions.tpl:L41, snippets/shipping/shipping-calculator.tpl:L46, snippets/social/whatsapp-chat.tpl:L11 |
| Ubicaciones posibles por grafo | templates/layout/cart_drawer.json, templates/layout/header.json, templates/pages/account/login.json, templates/pages/account/register.json, templates/pages/cart.json, templates/pages/home.json, templates/pages/product.json |
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
| Hooks JS | no disponible en marcado directo |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | endif, icon-inline, icon_class, if |
| Atributos data | no disponible |
| Semántica directa | no disponible (puede provenir de includes); excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/icon.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
