# footer-legal

**Identificador:** `snippets:footer:footer-legal` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/footer/footer-legal.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/footer/footer-legal.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | footer-legal; unidad footer-legal de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | sections/footer.tpl:L70 |
| Ubicaciones posibles por grafo | templates/layout/footer.json |
| Instancias guardadas | no disponible |
| Dependencias | snippets/footer/payment-shipping-logos.tpl (twig-literal, L17), snippets/footer/payment-shipping-logos.tpl (twig-literal, L26), snippets/image.tpl (twig-literal, L54), snippets/footer/claim-info.tpl (twig-literal, L80), nubesdk-slot (platform-component, L72), nubesdk-slot (platform-component, L77) |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | no disponible en marcado directo |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | afip, custom-seal, custom-seal-code, ebit, footer-copyright, footer-legal-container, footer-logo, footer-logos-wrapper, footer-payment-group, footer-payments-shipping-container, footer-powered-by, footer-seals-container, payment_shipping_title_classes, seal-afip, seal-ebit |
| Atributos data | no disponible |
| Semántica directa | a: 1; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 1 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G, E; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/footer/footer-legal.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
