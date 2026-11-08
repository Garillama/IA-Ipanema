# Descripción del producto

**Identificador:** `blocks:description` · **Tipo:** blocks · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [blocks/description.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/description.tpl:1>). **Schema:** [blocks/description.tpl:26](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/description.tpl:26>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Descripción del producto; unidad description de blocks; seguir consumidores para su papel en la página |
| Consumidores literales | blocks/product-info.tpl:L22 |
| Ubicaciones posibles por grafo | templates/pages/product.json |
| Instancias guardadas | templates/pages/product.json#/main_product/product_info/description |
| Dependencias | snippets/social/social-share.tpl (twig-literal, L21), nubesdk-slot (platform-component, L9), nubesdk-slot (platform-component, L18) |
| Restricciones | {"limit": 1, "deletable": false} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#blocks-description-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | js-product-description |
| Referencias store.js | L3164 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | js-product-description, product-description-content, product-description-heading, product-info-description, user-content |
| Atributos data | store |
| Semántica directa | h3: 1; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D, E; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "description" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
