# Íconos informativos

**Identificador:** `blocks:purchase-info` · **Tipo:** blocks · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [blocks/purchase-info.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/purchase-info.tpl:1>). **Schema:** [blocks/purchase-info.tpl:29](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/purchase-info.tpl:29>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Íconos informativos; unidad purchase-info de blocks; seguir consumidores para su papel en la página |
| Consumidores literales | blocks/product-info.tpl:L20 |
| Ubicaciones posibles por grafo | templates/pages/product.json |
| Instancias guardadas | templates/pages/product.json#/main_product/product_info/purchase_info |
| Dependencias | blocks/icon-text-item.tpl (twig-literal, L24) |
| Restricciones | {"limit": 2} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#blocks-purchase-info-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | custom_title_mobile, custom_title_mobile_size |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | `--section-icon-color` |
| Hooks JS | no disponible en marcado directo |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | product-purchase-info |
| Atributos data | store |
| Semántica directa | no disponible (puede provenir de includes); excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "purchase-info" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
