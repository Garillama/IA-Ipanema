# Paquete de revisión — primera corrección LCP hero

Candidato: SHA256 patch `e6d7edd9bb3590b0909cd71a9245bf5a92cbd7034f24fc57bb00389d0ec3f841`. Diff exacto: [`candidate.patch`](candidate.patch). Archivos: `sections/hero.tpl`, `snippets/image.tpl`. Base/candidato y respaldos: [`README`](README.md#diff-hashes-y-respaldo).

## Evidencia factual

La captura autorizada desktop de `https://rhino-performance.com/` devolvió HTTP200, HTML UTF-8 Brotli. El HTML tenía dos `<img>` de hero: desktop con GIF placeholder y `data-srcset` sin prioridad; mobile con `srcset` activo y `fetchpriority=high` pese a `d-md-none`. En esa única navegación desktop el navegador transfirió 31,760 bytes del AVIF1920 y 32,237 bytes del AVIF820, ambos distintos; desktop LCP 1,676ms; request de imagen desktop inició 1,216.9ms después del documento. Cinco trazas Lighthouse previas describen late discovery desktop en 5/5. No se concluye mejora de Lighthouse a partir de esta captura.

La instancia home usa sección tipo `hero` primera en `templates/pages/home.json`; el archivo sigue sin cambios (SHA `960f96de25d81f54fba64f40e796157bb559b478b51a3271cb7c2c06cb2a6bb3`). En la captura ambas variantes tenían `alt="Hero"`.

## Cambios propuestos

- Con alternativa móvil: un `<picture>` de art direction con media query 767.98px; mobile sources antes del desktop fallback; formatos media AVIF/WebP conservados desde `resolve_media`; un `<img>`/alt. Desktop-only sigue usando desktop; mobile-only mantiene placeholder desktop; sin imagen conserva su placeholder original.
- Prioridad alta solo cuando `is_priority_section`; hero posterior usa carga nativa diferida. Sin JS para elegir la imagen; no hay segundo `<img>` ni preload.
- El helper compartido solo activa la nueva rama si se pasa `image_mobile_src`; consumidores actuales no pasan ese parámetro. Revisar este contrato y su compatibilidad, y confirmar qué hace `resolve_media` ante medios no procesados.
- Las dimensiones responsive se declaran por `<source>`; rama art direction omite width/height desktop en `<img>`. HTML Standard/MDN documentan esa API de `<picture><source>`.

## QA disponible y límites

- Browser fixture local con 32 escenarios/231 aserciones en siete anchos; intercepted `fixtures.invalid` únicamente; un request para el `currentSrc` elegido; ratio móvil/desktop reservado y sin CLS sintético; LazySizes local en caso lazy; primera prioridad/hero posterior lazy.
- JSON home parseado, `node --check`, `git diff --check` pasaron.
- Fixture no renderiza Twig. No valida HTML final de Tiendanube, ni `resolve_media` real en el renderer, ni red real o LCP posterior. No hay revisión Claude/Codex de este patch.

## Preguntas a revisores

1. ¿La nueva rama opt-in del helper preserva sin cambios la salida de todos los otros consumidores?
2. ¿El orden de fuentes mobile AVIF/WebP/original seguido de desktop AVIF/WebP/original garantiza que solo se descarga una alternativa según media, incluidos fallos de formato?
3. ¿`image_priority_high`, `image_lazy`, `image_lazy_js`, LazySizes y `loadHidden:true` interactúan correctamente con el `<picture>` y el placeholder de la hero posterior?
4. ¿Las dimensiones en `<source>` reservan la proporción para los dos art directions en renderer/Chrome objetivo y preservan `media-auto`?
5. ¿Qué incompatibilidades de Ipanema/Tiendanube, escape Twig, unresolved `@media-lib`, alt, `image_thumbs:false` o `sizes` no cubre el fixture?
6. ¿La modificación corresponde al helper común como opción explícita o requiere una abstracción hero-only para reducir el riesgo a los otros consumidores?
7. ¿Hay defectos concretos en los casos solo desktop, solo móvil, sin imagen, primera imagen y banners posteriores?

No aprobar despliegue. Clasificar hechos frente a inferencias y dar pruebas específicas que faltan.

## Restricción del controlador

El orquestador ejecuta QA central antes de cualquier deliberación: `scope=workspace` lanza toda la suite `tests/unit`; `scope=theme` ejecuta auditoría estática de todo el tema. No existe selector de QA focalizado en la CLI actual. Como se solicitó no ejecutar QA general y no modificar políticas, el consejo no se ejecutó. Se mantiene `needs_evidence`; ninguna respuesta histórica aplica a este hash.
