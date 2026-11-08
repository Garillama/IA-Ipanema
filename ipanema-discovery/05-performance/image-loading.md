# Selección y carga de imágenes

Fecha: 2026-11-08. Fuente principal: [snippets/image.tpl](/home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/image.tpl:17), callers hero/slide/item-image/product-image. Rendimiento de cada componente requiere Network del contexto correcto.

El helper admite objetos de producto/categoría/post, URL y referencias `@media-lib`. Para media procesada construye picture y sources por formato, incluido AVIF/WebP cuando los entrega resolve_media; no transforma por sí mismo todo archivo remoto a AVIF. Conserva srcset original y atributos sizes si el caller los pasa. Para otras imágenes puede emitir img normal. Dimensiones, ratio, alt y prioridad se resuelven según argumentos y metadatos.

`image_priority_high` agrega fetchpriority high y desactiva lazy. El flag `image_lazy` tiene una comparación particular contra la cadena `'false'`: no asumir que pasar un boolean false equivale al contrato documentado por el caller. La rama de lazy JS usa data-src/data-srcset y puede dejar un placeholder; necesita motor. Se debe verificar cómo se compila Twig antes de cambiar una semántica de valores.

## Por qué pueden descargarse variantes ocultas

Un `<img src>` separado puede ser solicitado por el preload scanner antes de que la cascada lo oculte. `display:none` no es una regla general de «no descargar» para imágenes. Un elemento que aún solo tiene data-src puede no pedir nada hasta que su loader lo active. Ese loader, su política de elementos ocultos y su margen de precarga cambian el resultado.

Hero y slide generan imágenes desktop/mobile separadas cuando hay alternativa. En la primera sección prioritaria, la imagen mobile puede recibir src y prioridad alta aunque el viewport sea desktop; desktop queda lazy. Slideshow quita `swiper-lazy` a imágenes con display none antes de iniciar. La configuración minificada de lazysizes contiene `loadHidden: true`. **El código confirma el riesgo, no la descarga simultánea de todas las variantes en cada componente.** No se encontró una tercera imagen tablet dedicada como regla del hero.

Para selección exclusiva de arte por dispositivo se propone extender el helper existente a un solo picture con sources condicionados por media, cuando las capacidades de resolve_media lo permitan. Esto deja la elección al navegador y evita dos imágenes eager. El helper actual usa picture para formatos, no necesariamente para art direction. [Semántica de picture](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/picture). No se implementó esa extensión.

| Estado | Cómo comprobarlo |
|---|---|
| Recurso anunciado | HTML inicial, preload, srcset/data-srcset |
| Solicitud iniciada | Network requestWillBeSent o waterfall |
| Transferencia completada | loadingFinished/bytes; distinguir caché, 304 y cancelación |
| Decodificación | Eventos/profiling y naturalWidth como indicio; no deducir tiempo de decode solo de bytes |
| Renderizado | currentSrc, dimensiones y rectángulos |
| Visibilidad | Viewport, display/visibility, opacidad, ancestros y oclusión; un rectángulo no prueba visibilidad total |

Los JSON del auditor registran `visible` como heurística de rectángulo en viewport: no comprueba oclusión ni todos los estilos de ancestros. La selección de tamaños depende de DPR y tamaño CSS. En cards, el 50vw desktop merece ajuste por columnas y ancho de contenedor; en hero, la prioridad se basa en index de sección, que puede diferir del LCP real.

Una imagen LCP debe estar disponible en HTML y reservar espacio; diferirla por primer clic perjudica descubrimiento/carga. Imágenes secundarias y fuera del primer viewport pueden usar lazy. No precargar todas las variantes ni usar fetchpriority high en cada tarjeta. Verificar caché fría/caliente y al menos DPR 1/2 antes de fijar ahorro.
