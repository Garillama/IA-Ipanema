# Pie de página

**Identificador:** `sections:footer` · **Tipo:** sections · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [sections/footer.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/footer.tpl:1>). **Schema:** [sections/footer.tpl:79](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/footer.tpl:79>).

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | Pie de página; unidad footer de sections; seguir consumidores para su papel en la página |
| Consumidores literales | Inclusión dinámica, JSON o no disponible |
| Ubicaciones posibles por grafo | templates/layout/footer.json |
| Instancias guardadas | templates/layout/footer.json#/footer |
| Dependencias | blocks/ (twig-dynamic-prefix, L61), snippets/footer/footer-country-selector.tpl (twig-literal, L65), snippets/footer/footer-legal.tpl (twig-literal, L70), nubesdk-slot (platform-component, L47), nubesdk-slot (platform-component, L77) |
| Restricciones | {"class": "section-footer", "limit": 1, "enabled_on": {"layout_templates": ["footer"]}} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | [Matriz exacta](../settings-matrix.md#sections-footer-tpl) |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | `--footer-background`, `--footer-foreground`, `--footer-foreground-opacity-10`, `--footer-foreground-opacity-20`, `--footer-foreground-opacity-40`, `--footer-foreground-opacity-60` |
| Hooks JS | js-hide-footer-while-scrolling |
| Referencias store.js | L1630 |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | container, endif, footer-content, footer-main-info, footer-secondary-info, footer_main_toggle_classes, full_width, if, js-hide-footer-while-scrolling, section-full-width |
| Atributos data | section-id, store |
| Semántica directa | no disponible (puede provenir de includes); excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | A, B, C, F, D, E; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 47 registros de crawl para este tipo de sección; ver runtime-page-audit |
| Personalización recomendada | Configurar tipo/padre existente; tokens globales solo para alcance global |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "footer" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
