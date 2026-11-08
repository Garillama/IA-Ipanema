# Formulario de contacto

**Identificador:** `sections:main-contact` · **Tipo:** sections · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [sections/main-contact.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-contact.tpl:1>). **Schema:** [sections/main-contact.tpl:168](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-contact.tpl:168>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Formulario de contacto; unidad main-contact de sections; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | templates/pages/contact.json |
| Instancias guardadas | templates/pages/contact.json#/contact_form |
| Dependencias | snippets/social/contact-links.tpl (twig-literal, L87), snippets/image.tpl (twig-literal, L96), snippets/forms/form.tpl (twig-literal, L131), snippets/forms/form-input.tpl (twig-literal, L145), snippets/forms/form-input.tpl (twig-literal, L148), snippets/forms/form-input.tpl (twig-literal, L152), snippets/forms/form-input.tpl (twig-literal, L155) |
| Restricciones | {"class": "section section-main-contact", "limit": 1, "enabled_on": {"page_templates": ["contact"]}} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#sections-main-contact-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-winnie-pooh-form |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | alert, alert-danger, alert-success, btn-link, contact-cancellation-disclaimer, contact-cancellation-intro, contact-disclaimer, contact-divider, contact-form-container, contact-form-section, contact-info-container, contact-intro, contact-other-problems, contact-product-card, contact-product-info, contact-success-followup, container, d-grid, divider, grid-md-2, hidden, icon_classes, list, list-unstyled, list_classes, list_with_icons_classes, winnie-pooh |
| Atributos data | component, store |
| Semántica directa | ul: 1, li: 5, a: 5, h5: 1, input: 4; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 1 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 1 registros de crawl para este tipo de sección; ver runtime-page-audit |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "main-contact" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
