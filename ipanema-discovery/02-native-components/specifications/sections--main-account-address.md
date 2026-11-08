# Dirección

**Identificador:** `sections:main-account-address` · **Tipo:** sections · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [sections/main-account-address.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-account-address.tpl:1>). **Schema:** [sections/main-account-address.tpl:129](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-account-address.tpl:129>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Dirección; unidad main-account-address de sections; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | templates/pages/account/address.json |
| Instancias guardadas | templates/pages/account/address.json#/account_address |
| Dependencias | snippets/forms/form.tpl (twig-literal, L27), snippets/forms/form-input.tpl (twig-literal, L29), snippets/forms/form-input.tpl (twig-literal, L43), snippets/forms/form-input.tpl (twig-literal, L52), snippets/forms/form-input.tpl (twig-literal, L60), snippets/forms/form-input.tpl (twig-literal, L68), snippets/forms/form-input.tpl (twig-literal, L77), snippets/forms/form-input.tpl (twig-literal, L85), snippets/forms/form-input.tpl (twig-literal, L93), snippets/forms/form-select.tpl (twig-literal, L101), snippets/forms/form-input.tpl (twig-literal, L110), nubesdk-slot (platform-component, L19), nubesdk-slot (platform-component, L121) |
| Restricciones | {"class": "section section-main-account-address", "limit": 1, "enabled_on": {"page_templates": ["account/address"]}} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#sections-main-account-address-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | no disponible en marcado directo |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | account-address-section, account-form-container, alert, alert-info, container, notification-danger, notification-left |
| Atributos data | no disponible |
| Semántica directa | no disponible (puede provenir de includes); excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, E; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "main-account-address" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
