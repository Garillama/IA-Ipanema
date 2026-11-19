# Corrección aislada de la hero responsive — H1/S1 + T1

**Estado:** `needs_evidence`  
**Alcance:** copia local aislada del candidato; sin integración, publicación, acceso a producción ni llamadas a proveedores. El último cambio resuelve solo T1 moviendo un comentario; no cambia la lógica.

## Identidad

La base de esta corrección son exactamente los dos archivos del candidato D1/D2/R1/R4 revisado como diff `ff73a41106aa153e30f0b84bf018ce89f80d693a68551eb39ab021ce1c09406b`:

| Archivo | SHA256 base | SHA256 corregido |
|---|---|---|
| `sections/hero.tpl` | `1e70c54c4c5bc38711272284843d8881c4354ac7725e9de56c0223b599c3e65d` | H1/S1: `e7353ebcac1ac0dfe50b965456f89de7168d18bf0a003214c8629a112f13067f`; tras T1: `06dded46e359d68648c05253eff315e5c124e9c1d30313b0ea0b8e2c7ac7062c` |
| `snippets/image.tpl` | `e4e622e0c561c4450138e7717a1e5af95cf19d0184aee5cbcb89990f7ada767e` | `447a9b23e2cbe7ac752f804a754d8e99ad87cd32449c41aa658fa919e18a32b5` (sin cambio por T1) |

El diff H1/S1 sobre esa base tiene SHA256 `dca0f052f3278214d81daf0f0e8798515250a7c698350d549a20f8e230ce07a6`. La corrección T1, aplicada sobre H1/S1, es `candidate-t1.patch`, SHA256 `b6c8e1f55d1fa63ea1e0e644b79648ba553d46d81ec9685cc70e3d8b5cd071fc`. El manifiesto actualizado está en `manifest.json`; su SHA256 se registra en `manifest.sha256`.

La comparación estructural en `t1-structural-check.json` confirma que, al quitar la línea del comentario en ambos archivos, el contenido restante coincide byte por byte: únicamente se trasladó el comentario. El objeto del include ya no contiene comentarios Twig y el orden y valores de parámetros no cambiaron. No se repitieron Chromium ni Lighthouse porque T1 no cambia lógica. El resultado anterior de H1/S1 es histórico y corresponde al archivo previo, no es una prueba nueva de esta variante.

## Cambios

1. En la rama de art direction de `sections/hero.tpl`, se elimina la clase `lazyload` y también `fade-in`. Se conserva `image_lazy: not is_priority_section` y `image_lazy_js: false`, por lo que la hero secundaria usa `loading="lazy"` nativo desde el helper. La hero prioritaria conserva su ruta y prioridad.
2. Se elimina el hermano `.placeholder.placeholder-fade` únicamente de esa rama. Así no depende de `.lazyloaded` para desaparecer y no queda animándose tras una carga nativa.
3. En `snippets/image.tpl`, se evita crear el `srcset` de anchos nominales cuando art direction usa una URL directa validada sin variantes de Tiendanube. Una referencia resuelta por `resolve_media` sigue utilizando sus `srcSets` AVIF/WebP y original.

La condición S1 es acotada a art direction: la generación preexistente de `srcset` en otros consumidores de URL directa queda como deuda heredada, fuera de este cambio.

### A1: texto alternativo

El `<picture>` mantiene un único `<img>` y un solo `alt`. Si desktop y móvil expresan el mismo mensaje visual, la descripción compartida es adecuada. Si son imágenes con significado distinto, el `alt` calculado desde la imagen desktop no puede variar según `<source>`; la limitación debe resolverse editorialmente usando variantes equivalentes o un alt común que describa el contenido significativo de ambas. No se añade un segundo `<img>`.

## Prueba focalizada ejecutada

Comando ejecutado una sola vez:

```bash
node reports/rhino-performance/performance-html-js-20261117/candidate-d1d2-r1-r4/final-correction-isolated-20261118/tests/focused-h1-s1.browser.mjs
```

Resultado: **exit 0**, 12 aserciones estáticas y dos casos Chromium (412 px y 1440 px). Se usó el fragmento real de estados de carga de `style-critical.css`, fijado en `tests/style-critical-excerpt.css` (origen SHA256 `25194781ceb4181689a88d76c0d9ab5ca35614d6cc97902ecf1af568a389c845`). Las imágenes fueron SVG sintéticos servidos solo desde `127.0.0.1`; no se contactó producción ni un host externo.

En ambos viewports se verificó: una sola solicitud de imagen correspondiente al breakpoint, `loading="lazy"`, clase vacía, opacidad computada `1`, cero placeholders, un único alt compartido y ningún layout shift observado en la fixture. La salida íntegra está en `tests/focused-h1-s1-results.json`.

Las 12 aserciones también comprueban que sigan presentes los contratos de D1/D2/R1/R4, la prioridad de la primera hero y los caminos de AVIF/WebP/srcset originales. No se repitió la matriz sintética previa de 60 casos.

## Límites y riesgos pendientes

| Área | Evidencia actual | Pendiente |
|---|---|---|
| H1 | CSS real + markup representativo en Chromium; imagen visible, sin placeholder y una solicitud por viewport | Render Twig de Tiendanube y carga nativa en la página real |
| S1 | Aserción estática sobre la rama de URL directa; evita descriptores inventados en art direction | Confirmar las URLs y formatos reales que entregue Tiendanube |
| D1/D2/R1/R4 | Código preservado y aserciones de contrato focalizadas; sus pruebas históricas no se repitieron | Renderer y `resolve_media` reales |
| LazySizes | La rama responsive corregida ya no solicita sus clases ni estado `.lazyloaded`; otros caminos de hero se conservaron | Comprobar la salida final del renderer y que los otros caminos sigan su flujo publicado |
| CLS/dimensiones | Fixture con proporciones mobile/desktop y dimensiones en `<source>`/`<img>` no observó shifts | `auto_height`, editor y geometría de Tiendanube; la prueba sintética no certifica su implementación |
| A1 | Un solo `<img alt>`; variante móvil-only conserva alt móvil por la rama D1 | Confirmar que las dos creatividades conserven el mismo significado o aprobar un alt compartido editorialmente |
| Rendimiento/LCP | La prioridad de la primera hero no cambió | No se midió LCP ni Lighthouse después; hace falta autorización y validación posterior en Tiendanube |
| Compatibilidad del helper | El cambio a `srcset` está condicionado a `has_art_direction && image_raw_url_valid` | El helper es compartido; revisar consumidores y validar render antes de integración |

La segunda evaluación externa del candidato original tuvo acceso al historial de la primera y **no se considera ciega**. Esta corrección no cuenta con nueva revisión externa independiente.

## Validación nativa posterior

Antes de cualquier integración habría que solicitar autorización específica para validar, sin persistir, solo `sections/hero.tpl` y `snippets/image.tpl` mediante el mecanismo nativo existente. Verificar:

- Render real con ambos banners, solo móvil, solo desktop, medios no válidos y sin imagen.
- `<picture>`, `srcset`, `sizes`, AVIF/WebP/original, ausencia de `@media-lib:` literal y `currentSrc`/Network en 412 y 1440 px.
- Hero inicial con prioridad alta y heroes posteriores con `loading="lazy"`, sin `lazyload`, fade bloqueado ni placeholder persistente en esta rama.
- Variantes, proporciones, `auto_height`, alt, editor Ipanema y consumidores conocidos del helper.
- Luego, si la validación es correcta, una autorización separada para integrar; después QA visual/performance comparable y autorización distinta para publicar.

## Reversión propuesta

La reversión local consiste en descartar únicamente este candidato aislado y conservar la base intacta. Para una futura integración, restaurar las dos preimágenes exactas de la tabla si sus hashes actuales coinciden con los hashes corregidos; si alguno difiere, detenerse y revisar el cambio ajeno. No se ha aplicado ningún archivo al tema.

## Archivos de esta entrega

- `candidate-incremental.patch`: diff exacto.
- `candidate-t1.patch`: traslado exacto del comentario sobre H1/S1.
- `baseline/sections/hero.tpl`, `baseline/snippets/image.tpl`: preimágenes congeladas.
- `candidate/sections/hero.tpl`, `candidate/snippets/image.tpl`: candidato corregido.
- `prior-h1-s1/`: snapshot exacto del candidato inmediatamente anterior a T1.
- `t1-structural-check.json`: comparación estructural del traslado.
- `tests/focused-h1-s1.browser.mjs`, `tests/focused-h1-s1-results.json`: prueba y resultado.
- `tests/style-critical-excerpt.css`: CSS real relevante, extraído del archivo identificado por hash en el manifiesto.
- `manifest.json`, `manifest.sha256`: inventario verificable.

**Dictamen de esta fase:** T1 queda corregido en la copia aislada y verificado estructuralmente; las pruebas H1/S1 permanecen como evidencia histórica del candidato anterior. La plataforma real no está validada. Se mantiene `needs_evidence`.
