# Ícono y texto

**Identificador:** `blocks:icon-text-item` · **Tipo:** blocks · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [blocks/icon-text-item.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/icon-text-item.tpl:1>). **Schema:** [blocks/icon-text-item.tpl:71](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/icon-text-item.tpl:71>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Ícono y texto; unidad icon-text-item de blocks; seguir consumidores para su papel en la página |
| Consumidores literales | blocks/purchase-info.tpl:L24 |
| Ubicaciones posibles por grafo | templates/pages/home.json, templates/pages/product.json |
| Instancias guardadas | templates/pages/home.json#/icon_text/icon_text_group/item_1, templates/pages/home.json#/icon_text/icon_text_group/item_2, templates/pages/home.json#/icon_text/icon_text_group/item_3, templates/pages/home.json#/icon_text/icon_text_group/item_4, templates/pages/product.json#/main_product/product_info/purchase_info/icon_returns, templates/pages/product.json#/main_product/product_info/purchase_info/icon_security |
| Dependencias | snippets/image.tpl (twig-literal, L32), snippets/icon.tpl (twig-literal, L40) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#blocks-icon-text-item-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | `--block-font`, `--block-font-size`, `--block-mobile-font-size` |
| Hooks JS | no disponible en marcado directo |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | description_size_class, flex-shrink-0, icon-text-item, icon-text-item-content, icon-text-item-description, icon-text-item-icon, item_class, title_class |
| Atributos data | no disponible |
| Semántica directa | a: 1; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 1 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "icon-text-item" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
