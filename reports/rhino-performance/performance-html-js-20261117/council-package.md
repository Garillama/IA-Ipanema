# Paquete de revisión dual incremental — captura HTML y hero

## Alcance

Revisión factual de la evidencia de las dos capturas ya autorizadas y recomendación de corrección candidata. Solo lectura, sin red, edición ni publicación. No tocar paginación, `store.js`, catálogo, tags ni Google Reviews. No repetir Lighthouse.

## HTML desktop y colección

La respuesta desktop es HTTP200 para `https://rhino-performance.com/`, `Content-Type: text/html; charset=UTF-8`, `Content-Encoding: br`, sin `Content-Length`. Cuerpo UTF-8 guardado: 1,174,783 bytes; CDP encoded document length al completar: 111,853 bytes. No confundir tamaño de fragmentos sin comprimir con bytes Brotli transferidos.

La navegación móvil fue 412×823 DPR1.75 y desktop 1440×900 DPR1. El cuerpo móvil se conservó, pero el script falló antes de registrar status/headers/network; no se repitió. Por tanto, el waterfall de imágenes y transferencia descritos aquí son desktop solamente.

HTML inicial: 8,367 nodos (incluye text/comment), 3,218 elementos, profundidad22, 66 scripts (51 inline/235,772B), 21 JSON/JSON-LD (23,468B), 22 forms globales. DOM post-init: 9,056 nodos, 3,620 elementos, profundidad22; 83 scripts (55 inline/342,291B), 23 JSON (128,000B). Dos application/json agregados suman104,532B; no atribuirlos sin evidencia a la colección.

Colección Rhino tiene seis paneles SSR: Todos6, Presoterapia3, Pistolas de masaje2, Terapia fría1, Compresión frío/calor3, Accesorios4. Total19 apariciones/13 productos únicos; seis apariciones repetidas de tarjetas entre panel «Todos» y su pestaña categoría. Los subárboles suman566,740B UTF-8 y copias exactas extra185,845B. 19 payloads `data-variants` suman166,960B, duplicados exactos por misma entidad57,192B. 19 forms,13 productos únicos; forms exactos repetidos18,897B. 19 Product JSON-LD suman21,664B, copias exactas extra6,869B. Valores anidados en las tarjetas; no sumar como ahorro separado ni transferido.

Hay IDs repetidos en respuesta: `variation_1`×11, `ns-block-navigation`×2, `ns-block-main-product-item_3k1e`×3. DOM posterior añade cuatro IDs de anuncios repetidos seis veces cada uno por expansión/clonado. Aún no se demostró fallo funcional.

`featured-collection.js` alterna paneles existentes; las tarjetas están en SSR bajo paneles inactivos hidden. Una solución no debe borrar paneles, productos, variantes, forms ni marcado sin conservar descubribilidad HTML, interacción/compra rápida, teclado y accesibilidad.

## Hero: hallazgo y propuesta a cuestionar

HTML inicial desktop contiene dos imágenes separadas:

- Hero desktop: `src` GIF transparente, `data-srcset` inerte en `img` y `source`, sin `fetchpriority`, clase `lazyload d-none d-md-block`.
- Hero mobile: `srcset` activo, `fetchpriority="high"`, clase `d-md-none` aunque esté oculta en viewport desktop.

Desktop network descargó ambas variantes: mobile AVIF820 32,237 bytes y desktop AVIF1920 31,760 bytes. Request desktop a1,216.9ms del request del documento; LCP=desktop AVIF1920 a1,676ms. Imagen decodificada1440×675, rect1440×720. Lighthouse desktop histórico (5 muestras) reportó LCP no descubrible/no alta prioridad, delay839–1921ms. Captura actual única sin throttling: no se infiere mejora de score.

Código local relevante y SHA256 local (no son hashes actuales del archivo remoto):
- `sections/hero.tpl`: `36b7f21aed77378f5b5b378c74dd7768bd2717159a1f1d80ae70079fa80b5542`
- `snippets/image.tpl`: `9e6b1624ee75d6d0a9899d7af25cd799b1e59bde31962c98e4fea3aca404ed3b`
- `sections/featured-collection.tpl`: `4dc61693332ed2eb500af7a8443882226bb162af404458e1d26b3a658db7ee56`
- `blocks/featured-collection-tab.tpl`: `6d0f5a1db90d1ad86c3a8b102361613e0fa1c9ca1206b3edc6572d0f232a3357`
- `static/js/featured-collection.js`: `b38ab728dfcab5311f938065655aa25a60279be900e05e592cd7bb4d6627b058`
- `snippets/product-list/product-item/item.tpl`: `daa3928d4c256ed94de9d8e7bd536e3143945a6461cef4e628cef0892c9ac3fd`

Local source hashes are not remote file hashes; no admin API was used/read. The exact activation mechanism for desktop `data-srcset` remains to be proven from code/trace; network `initiator=parser` is not conclusive about what activated lazy attributes.

Question: can an existing Ipanema contract represent two image objects in a single responsive HTML selection (`picture`/`source media` or equivalent) so only one variant is fetched, the correct image is discovered in initial HTML, and only that image gets high priority? Determine whether this belongs to `hero.tpl` or reusable image helper, check helper consumers, editor compatibility, aspect ratio/CLS, six viewport widths, `currentSrc`, no-JS selection and no duplicate download. Do not add preload for both variants. If a low-risk compatible construction is not evidenced, return `needs_evidence`; do not invent theme parameters.

## Other evidence

Historic Lighthouse medians (5/device): score52 mobile/54 desktop; LCP4.41s/2.51s; TBT2751/771ms; FCP1.91s/0.60s; CLS0.000329/0.052716; SpeedIndex4.18s/2.38s; weight2.315/2.542MB; server variance noted. Prior traces show long work from GTM/gtag, Meta, TikTok, Clarity/platform, but no duplicated event proof. Current desktop log:94 entries,76 GET,18 POST blocked locally; no response/transfer for those POSTs. `p.clarity.ms` and `apps-resources.b-cdn.net` blocked by the local allowlist. This does not validate conversions.

Google Reviews candidate remains untouched: patch SHA `2c88fb0d3e619b5d08c8e217eecb9e104d9d402dbe47997c95b91f0e4b1c8d32`, file `sections/google-reviews.tpl`, base local hash `75a487600c5d71001fa2e0970dad1cb943f80d399f1af89db559bffc3253fd30`, candidate hash `e6f79c2fd59376efe955662adff44d13329300360a118249c88480d59dde3cd3`. Prior 163 isolated checks and non-persisting Tiendanube validation; no Lighthouse benefit demonstrated. Not the chosen LCP correction.

## Review request

Give an independent technical assessment of:
1. Which conclusions are directly evidenced vs inferred.
2. Whether responsive hero selection is a viable first candidate and correct file boundary.
3. Risks to native Ipanema image contracts, accessibility, visual crop, CLS, no-JS, network double-download.
4. Whether collection duplicate markup is a separate opportunity or should remain unchanged pending redesign/causal measurements.
5. Minimal tests required before preparing a publication package.

Do not approve deployment. There is no candidate diff yet. No new production requests or file edits are allowed in this review.
