# Producto principal

**Identificador:** `sections:featured-product` · **Tipo:** sections · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [sections/featured-product.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/featured-product.tpl:1>). **Schema:** [sections/featured-product.tpl:78](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/featured-product.tpl:78>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Producto principal; unidad featured-product de sections; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | no disponible |
| Instancias guardadas | no disponible |
| Dependencias | snippets/product/product-image.tpl (twig-literal, L51), snippets/product/product-form.tpl (twig-literal, L54) |
| Restricciones | {"class": "section section-featured-product", "limit": 1} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#sections-featured-product-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-product-container, js-product-description, js-product-images, js-product-info, js-view-description, js-view-less, js-view-more |
| Referencias store.js | L1878, L1879, L1934, L1959, L1968, L2008, L2048, L2102, L2762, L3164, L3165, L3176, L3177 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | btn-link, container, endif, full_width, if, js-product-container, js-product-description, js-product-images, js-product-info, js-view-description, js-view-less, js-view-more, product-columns, product-description, product-featured-description, product-featured-description-text, product-images, product-info, section-featured-product, section-full-width, user-content |
| Atributos data | section-id, store, variants |
| Semántica directa | button: 1; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "featured-product" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
