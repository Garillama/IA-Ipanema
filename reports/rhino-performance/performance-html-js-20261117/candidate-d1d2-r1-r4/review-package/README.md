# Corrección local D1/D2 y fallbacks responsive

Estado: **candidato aislado; `needs_evidence`; sin revisión independiente ni validación nativa**.

## Identidad

- Candidato anterior preservado: `e6d7edd9bb3590b0909cd71a9245bf5a92cbd7034f24fc57bb00389d0ec3f841`.
- Diff incremental (dos archivos) SHA256: `ff73a41106aa153e30f0b84bf018ce89f80d693a68551eb39ab021ce1c09406b`.
- Archivos: `sections/hero.tpl`, `snippets/image.tpl`.
- El checkout del tema permaneció en el hash del candidato anterior; no se editó durante esta corrección.
- Manifiesto de integridad: `manifest.json`.

## Reproducción y cambios

La reproducción source-level (`tests/reproduction-results.json`) confirma D1 en la rama de hero con imagen móvil únicamente: el candidato anterior usaba el placeholder como recurso desktop. Confirma D2 en la rama helper: una referencia móvil `@media-lib:` presente pero no resuelta podía llegar al markup como valor de `srcset`. No hubo solicitudes de red en esta reproducción.

El candidato nuevo:

- Valida por separado referencias `@media-lib:` resueltas, tipo `image`, `sourceUrl` HTTP(S) y URLs directas con host sintácticamente válido.
- Si solo hay imagen móvil válida, usa ese medio como una sola imagen a cualquier ancho. No añade el placeholder y solo prioriza si la hero es prioritaria.
- Si ninguna alternativa es válida, conserva el placeholder nativo ya existente; no genera una ruta nueva.
- Si una referencia está huérfana o devuelve un tipo distinto de imagen, no emite ese valor como `src`/`srcset`; aprovecha la otra variante válida cuando existe.
- El fallback original de mobile y desktop conserva descriptores `srcSets` cuando Tiendanube los entrega; AVIF/WebP siguen basados exclusivamente en `srcSets`.
- Conserva alt y dimensiones disponibles; el alt en art-direction sigue siendo único, por lo que ambas imágenes deben comunicar el mismo significado accesible.

## Pruebas ejecutadas

- Reproducción estática previa: D1 y D2 reproducidos; renderer Twig no disponible.
- Matriz de navegador sintético: 60 casos, 13 aserciones de fuente. Viewports 360, 390, 412, 767, 768, 1024, 1440 y 1920; incluye imágenes distintas, solo desktop, solo móvil, ninguna, referencias inválidas, tipo video, prioridad inicial y lazy posterior. Cada fixture observó una solicitud efectiva y CLS 0 dentro de ese markup sintético.
- Evidencia completa: `tests/hero-responsive-fallback-results.json`.

**Límite importante:** el harness selecciona salida desde una tabla/modelo que representa las ramas del template; no ejecuta `sections/hero.tpl` o `snippets/image.tpl` con el renderer de Tiendanube. Por tanto, 60 casos y CLS 0 no prueban el HTML real, `resolve_media`, conversión AVIF/WebP, selección real de `currentSrc`, ni ausencia de CLS en la tienda publicada.

## R1/R4, accesibilidad y estabilidad

- R1: un medio desktop inválido no impide mantener el medio móvil válido y no produce un `<picture>` vacío en la ruta de imagen única.
- R4: fallback original usa los `srcSets` suministrados; si no existen, conserva la URL fuente disponible. No construye URLs ni descriptores nuevos.
- Las dimensiones se copian del medio resuelto cuando están presentes y se emiten en las fuentes responsivas. El comportamiento del renderer y el ratio con `auto_height` no se puede certificar sin salida real de Tiendanube.
- Hay un `alt` único para `<picture>`. Si mobile y desktop no son semánticamente equivalentes, el editor debe usar una descripción que represente ambas variantes; esto requiere revisión de contenido/configuración, no se infiere por el fixture.

## Riesgos / pendientes

1. Revisión independiente del diff nuevo (no ejecutada; esta autorización la prohibió automáticamente).
2. Validación del parser/renderer Twig de Tiendanube y de `resolve_media` para huérfanos/tipos incompatibles.
3. Verificar HTML inicial, `currentSrc`, solicitudes, prioridad y LazySizes con assets reales.
4. Verificar dimensiones/ratio, `auto_height`, alt en ambas variantes y CLS real.
5. Validación visual y rendimiento posterior; no se hicieron solicitudes a Rhino ni Lighthouse.

La cadena de validación no está cerrada: **no integrar ni publicar este candidato todavía**.
