# Información del producto

**Identificador:** `sections:main-product` · **Tipo:** sections · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [sections/main-product.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-product.tpl:1>). **Schema:** [sections/main-product.tpl:35](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-product.tpl:35>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Información del producto; unidad main-product de sections; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | templates/pages/product.json |
| Instancias guardadas | templates/pages/product.json#/main_product |
| Dependencias | blocks/product-media.tpl (twig-literal, L23), blocks/product-info.tpl (twig-literal, L25) |
| Restricciones | {"class": "section section-main-product section-margin", "limit": 1, "enabled_on": {"page_templates": ["product"]}, "deletable": false, "hideable": false, "locked_blocks": true} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#sections-main-product-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-has-new-shipping, js-product-container, js-product-detail, js-shipping-calculator-container |
| Referencias store.js | L2384, L2762, L3285, L3461, L3470, L3704 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | container, endif, full_width, if, js-has-new-shipping, js-product-container, js-product-detail, js-shipping-calculator-container, product-columns, section-full-width |
| Atributos data | section-id, store, variants |
| Semántica directa | section: 1; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 17 registros de crawl para este tipo de sección; ver runtime-page-audit |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "main-product" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
