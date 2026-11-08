# Controles del editor

Fecha: 2026-11-08. Se extrajeron **708 definiciones** del schema global y schemas inline. Incluyen settings privados anidados del padre; no son 708 campos visibles a la vez. Sus IDs, etiquetas es-MX, defaults, opciones, rangos, `visible_if`, `disabled_if` y valores verticales están en la [matriz única](../02-native-components/settings-matrix.md). El Admin real no fue abierto.

El editor refleja archivos JSON y schemas; no es una herramienta de CSS libre para cada propiedad. La [documentación Brand Editor](https://tiendanube.dev/themes/sectionable-themes/brand-editor) confirma su correspondencia con `order`, `block_order`, `disabled` y settings. La presencia de una condición en schema prueba la intención del control, no que se haya pulsado en esta auditoría.

| Propiedad solicitada | Encontrado | Alcance real |
|---|---|---|
| Padding vertical/horizontal | 121 definiciones relacionadas; `vertical_padding`, `horizontal_padding`, variantes mobile | Generalmente aplica pares de lados mediante style; no se encontraron IDs de cuatro lados independientes |
| Márgenes | Ningún ID con margin | Existen márgenes CSS/clases; no un control universal declarado |
| Gap/column gap | 48 definiciones relacionadas | Por sección/grupo; no variable universal del editor para cada breakpoint |
| Ancho/maximum | section_width, width, page_width | Ancho de página global y selección full/page/fit/fill según componente; no max-width libre en todos |
| Altura/autoheight | 12 definiciones relacionadas | Hero/slideshow/logo/banners tienen modelos distintos, px/vh/ratio; no confundir el `%` mostrado con un porcentaje del padre |
| Flex/grid/alineación | direction, alignment, format, columns y variantes | Solo donde el schema lo declara; `alignment` puede producir también un valor vertical |
| Tipografía | Familias globales, tamaños y overrides de títulos | Overrides pueden agregar familias y peticiones; no equivalen a etiquetas H1-H6 |
| Colores/fondo | 115 controles tipo color | Incluye referencias default_setting a identidad global |
| Gradientes | Ningún ID gradient | No disponible como control dedicado en lo inspeccionado; CSS permitiría un diseño autorizado |
| Bordes/radios | Configuración de botones/labels, tokens y bloques | No un panel universal de borde por sección |
| Sombras | Ningún ID shadow declarado | `card_shadow` existe como valor guardado, pero no demuestra un control vigente en el schema |
| Opacidad | overlay_opacity en seis definiciones | Overlay de medios; no opacidad general de cualquier elemento |
| Hover/transiciones | product_hover y estilos nativos | No se encontraron controles universales de transición |
| Motion | animation/animation_speed/content_animation; parallax | Tipos concretos, no constructor libre de animaciones |
| Ocultar por dispositivo | show_on_mobile y controles selectivos | No universal; distinguir `disabled` de ocultamiento responsive |
| Tablet independiente | Ningún setting identificado como tablet | Hay media queries tablet/intermedias en CSS |

Método: búsqueda de IDs y tipos en [settings.json](../13-evidence/measurements/source-baseline/settings.json), contrastada con su consumo en Twig para los casos descritos. Las coincidencias cuentan definiciones, no capacidades independientes. Los defaults del schema, los valores guardados y los fallbacks Twig pueden diferir: evaluar los tres antes de editar.
