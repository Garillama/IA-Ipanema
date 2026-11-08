# Encabezado

**Identificador:** `sections:page-header` · **Tipo:** sections · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [sections/page-header.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/page-header.tpl:1>). **Schema:** [sections/page-header.tpl:111](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/page-header.tpl:111>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Encabezado; unidad page-header de sections; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | templates/pages/account/address.json, templates/pages/account/addresses.json, templates/pages/account/info.json, templates/pages/account/login.json, templates/pages/account/newpass.json, templates/pages/account/order.json, templates/pages/account/orders.json, templates/pages/account/register.json, templates/pages/account/reset.json, templates/pages/account/subscription-address.json, templates/pages/account/subscription-product.json, templates/pages/blog-post.json, templates/pages/blog.json, templates/pages/cart.json, templates/pages/category.json, templates/pages/contact.json, templates/pages/page.json, templates/pages/search.json |
| Instancias guardadas | templates/pages/account/address.json#/heading, templates/pages/account/addresses.json#/heading, templates/pages/account/info.json#/heading, templates/pages/account/login.json#/heading, templates/pages/account/newpass.json#/heading, templates/pages/account/order.json#/heading, templates/pages/account/orders.json#/heading, templates/pages/account/register.json#/heading, templates/pages/account/reset.json#/heading, templates/pages/account/subscription-address.json#/heading, templates/pages/account/subscription-product.json#/heading, templates/pages/blog-post.json#/heading, templates/pages/blog.json#/heading, templates/pages/cart.json#/heading, templates/pages/category.json#/heading, templates/pages/contact.json#/heading, templates/pages/page.json#/heading, templates/pages/search.json#/heading |
| Dependencias | snippets/breadcrumbs.tpl (twig-literal, L30), nubesdk-slot (platform-component, L16), nubesdk-slot (platform-component, L107) |
| Restricciones | {"class": "section section-page-header", "limit": 1, "enabled_on": {"page_templates": ["category", "search", "contact", "blog", "blog-post", "page", "cart", "account/login", "account/register", "account/reset", "account/newpass", "account/orders", "account/order", "account/info", "account/addresses", "account/address", "account/subscription-address"]}, "deletable": false} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#sections-page-header-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-passwordless-login-header-title |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | blog-post, container, container-narrow, d-block, d-md-none, endif, if, js-passwordless-login-header-title, page-header, page-header-count, page-header-description, page-header-title, page-header-title-inner, page-header-title-row, passwordless_template, template |
| Atributos data | store |
| Semántica directa | h1: 1; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D, E; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 28 registros de crawl para este tipo de sección; ver runtime-page-audit |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "page-header" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
