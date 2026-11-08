# Logo

**Identificador:** `blocks:header-logo` · **Tipo:** blocks · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [blocks/header-logo.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/header-logo.tpl:1>). **Schema:** [blocks/header-logo.tpl:24](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/header-logo.tpl:24>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Logo; unidad header-logo de blocks; seguir consumidores para su papel en la página |
| Consumidores literales | sections/header.tpl:L138 |
| Ubicaciones posibles por grafo | templates/layout/header.json |
| Instancias guardadas | templates/layout/header.json#/header/logo |
| Dependencias | snippets/logo/logo-img.tpl (twig-literal, L6), snippets/logo/logo-text.tpl (twig-literal, L8), snippets/image.tpl (twig-literal, L14) |
| Restricciones | {"limit": 1} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#blocks-header-logo-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | use_different_mobile_height, height_mobile |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | no disponible en marcado directo |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | endif, has-transparent-logo, if, logo-container, logo-default, logo-transparent, transparent_logo |
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
| Ejemplo de localización | `rg -n --fixed-strings "header-logo" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
