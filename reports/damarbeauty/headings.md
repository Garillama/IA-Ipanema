# Encabezados de Damar: corrección local

Fecha: 2026-11-09T17:07:33.090533+00:00. Alcance: navegación compartida y espacio del H1 de home.

Se conservaron los H2 de secciones/footer y H3 de subsecciones. Se convirtieron etiquetas y textos de menú a p/div, manteniendo sus clases, nombres accesibles y comportamiento. La jerarquía de una página no se corrige borrando todos los encabezados.

## Archivos modificados

- `snippets/navigation/damar-mega-desktop.tpl`
- `snippets/navigation/damar-nav-mobile.tpl`
- `static/css/damar-navigation-desktop.css`
- `sections/damar-home-hero.tpl`

Cambios anteriores de layout/logo y modificación ajena de `.nuvem` preservados. Sin cambios de JSON-LD, contenido comercial, datos ni sincronización.

## Orden resultante esperado de la home

**Fuente:** HTML público histórico de 8-11-2026, alineado con la retirada local del H1 oculto y transformación de las etiquetas de navegación. No es una captura del storefront actual ni render del Twig.

En ese documento, los menús aportaban 92 encabezados (10 H2 y 82 H3). Después de la transformación quedan 1 H1, 13 H2 y 15 H3 de contenido/footer. La cantidad no es un objetivo de SEO por sí misma.

| Orden | Etiqueta | Texto |
|---:|---|---|
| 1 | H1 | Beauty que vale el hype. |
| 2 | H2 | Empieza por un favorito |
| 3 | H2 | Todo lo que te gusta de Damar |
| 4 | H3 | Tus próximos favoritos, más cerca. |
| 5 | H3 | Ese producto que tienes en mente. |
| 6 | H3 | Beauty también es lo que llevas contigo. |
| 7 | H2 | Sigue tu beauty mood |
| 8 | H3 | Labios |
| 9 | H3 | Rubores |
| 10 | H3 | Skincare |
| 11 | H3 | Minis |
| 12 | H2 | Dos texturas. Tu manera de llevarlas. |
| 13 | H2 | Del color al último paso |
| 14 | H2 | Pequeños formatos. Grandes descubrimientos. |
| 15 | H2 | The Damar Edit |
| 16 | H3 | Un lip combo que va contigo. |
| 17 | H3 | Tu rutina, a tu ritmo. |
| 18 | H3 | Pequeños favoritos. Grandes planes. |
| 19 | H2 | Encuentra tu textura |
| 20 | H2 | Beauty que eliges con confianza. |
| 21 | H3 | ¿Qué significa sobre pedido? |
| 22 | H3 | ¿Cómo elijo entre dos tonos? |
| 23 | H3 | ¿Dónde consulto la entrega? |
| 24 | H3 | ¿Quieres reunir varias compras? |
| 25 | H3 | ¿No encuentras tu favorito? |
| 26 | H2 | Beauty con atención cercana. |
| 27 | H2 | Lo próximo que vas a querer probar. |
| 28 | H2 | Te ayudamos |
| 29 | H2 | Encuéntranos |

## Verificación

- Revisión estática por agente separado: enlaces, IDs, hooks data-*, ARIA y tabindex preservados; listas desktop con aria-label agregado. Declaraciones CSS conservadas bajo selectores de clase. JS existente sin cambios.
- Chrome offline: 360, 390, 768, 1024, 1279, 1280, 1440 y 1920 px. Geometría idéntica en ocho casos; mismos enlaces; menú desktop con teclado/Escape; menú mobile con drill-in, regreso, foco y nombre del diálogo.
- El cierre nativo de la modal se sustituye por un handler mínimo SOLO en el fixture, porque no se ejecuta la plataforma. La navegación custom usa los scripts reales sin modificar. Recursos externos e imágenes/fuentes remotas bloqueados; por ello las capturas no prueban el aspecto completo de la tienda.
- Comparación visual: ocho pares aprobados, cero píxeles distintos por encima de umbral de canal12, tolerancia de área0,005 y sin máscaras. Geometría calculada idéntica.
- Inventario fuente posterior sin errores JSON/schema; git diff --check aprobado.

## Evidencia y límites

Run local ignorado: `/home/alanrichard/Escritorio/IA inversa/reports/runs/damarbeauty/20261109T170419-heading-cleanup-b8a76c05`. `changes.patch`, `plan.json`, `browser/comparison.json`, `browser/heading-outline.json`, capturas antes/después y `source-after/`. La transacción conserva backup propio y hashes.

No se ejecutó una nueva solicitud al origen previamente bloqueado por403. Render Twig/editor, fuentes/imágenes reales y prueba final del storefront siguen pendientes. Los dos H1 responsive de PDP requieren revisión específica del layout y no se modificaron al corregir el informe de home.

Criterio semántico: [W3C, Headings](https://www.w3.org/WAI/tutorials/page-structure/headings/). W3C permite títulos de navegación antes del H1; esta depuración diferencia etiquetas de interfaz repetidas de encabezados de contenido.
