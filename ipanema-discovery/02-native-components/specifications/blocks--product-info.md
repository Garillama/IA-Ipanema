# Información de compra

**Identificador:** `blocks:product-info` · **Tipo:** blocks · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [blocks/product-info.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/product-info.tpl:1>). **Schema:** [blocks/product-info.tpl:30](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/product-info.tpl:30>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Información de compra; unidad product-info de blocks; seguir consumidores para su papel en la página |
| Consumidores literales | sections/main-product.tpl:L25 |
| Ubicaciones posibles por grafo | templates/pages/product.json |
| Instancias guardadas | templates/pages/product.json#/main_product/product_info |
| Dependencias | snippets/product/product-form.tpl (twig-literal, L15), blocks/purchase-info.tpl (twig-literal, L20), blocks/description.tpl (twig-literal, L22), blocks/ (twig-dynamic-prefix, L24) |
| Restricciones | {"limit": 1} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#blocks-product-info-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-product-info |
| Referencias store.js | L1879 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | d-flex, flex-column, js-product-info, product-info |
| Atributos data | store |
| Semántica directa | no disponible (puede provenir de includes); excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "product-info" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
