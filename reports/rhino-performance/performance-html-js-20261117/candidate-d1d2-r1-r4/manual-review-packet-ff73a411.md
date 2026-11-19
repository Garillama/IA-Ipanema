# Rhino Performance — paquete autocontenido para revisión manual de la hero responsive

**Candidato incremental SHA256:** `ff73a41106aa153e30f0b84bf018ce89f80d693a68551eb39ab021ce1c09406b`

**Estado:** `needs_evidence`. Este documento no es una aprobación, no ejecuta revisores y no autoriza integración ni publicación.

## Guía independiente para los revisores

Revisen el diff y el código candidato de forma independiente. El candidato es exclusivamente `sections/hero.tpl` y `snippets/image.tpl`; las demás plantillas son contexto de solo lectura. Analicen D1, D2, R1 y R4, resolución de medios, URL validation, `<picture>`, LazySizes, prioridad LCP, consumidores del helper, dimensiones/CLS, `auto_height`, `alt`, accesibilidad y compatibilidad Twig/Tiendanube. Citen cada observación con ruta y fragmento concreto. Distingan defectos demostrados estáticamente, hipótesis y requisitos de validación de plataforma. No traten resultados sintéticos ni revisiones históricas como validación del candidato actual.

## Separación de evidencia

- **Código candidato:** los dos archivos completos, marcados como candidatos.
- **Diff:** parche incremental completo contra la base de referencia registrada en el paquete.
- **Contexto:** siete dependencias completas y de solo lectura.
- **Producción histórica:** captura autorizada del 17-11-2026, limitada a metadatos, tags exactos de hero, solicitudes de imagen y eventos LCP pertinentes. No se repitió la navegación.
- **Pruebas sintéticas:** reproducciones y resultados del paquete; no usan Tiendanube ni la red de producción.
- **Pendiente de Tiendanube:** renderer Twig real, `resolve_media`, Editor/preview, red/currentSrc posterior al cambio, LazySizes real, CLS visual y nueva medición Lighthouse.

## Identidad del paquete y alcance

El paquete fuente congelado es `read-only-review-package-v4/`. Su manifiesto interno declara dos candidatos, siete dependencias de lectura y `write_files=[]`; el manifiesto externo conserva el vínculo con el manifiesto anterior. Ambos manifiestos íntegros se reproducen más abajo. Las verificaciones de origen se hicieron antes de ensamblar este documento: todas las entradas declaradas coincidieron con SHA256. Este archivo es un nuevo artefacto de revisión manual; no altera candidato ni paquete original.

## Diff incremental completo — candidato

- Ruta lógica: `candidate.patch`
- Clasificación: código candidato / diff
- SHA256 del origen: `ff73a41106aa153e30f0b84bf018ce89f80d693a68551eb39ab021ce1c09406b`

````
--- a/sections/hero.tpl
+++ b/sections/hero.tpl
@@ -6,9 +6,19 @@
 {% set hero = section.settings %}
 
 {# Images #}
-{% set has_mobile_image = hero.use_mobile_image and hero.image_mobile %}
-{% set has_responsive_images = hero.image and has_mobile_image %}
-{% set show_placeholder = not hero.image %}
+{% set desktop_is_media_ref = hero.image and hero.image starts with '@media-lib:' %}
+{% set desktop_media = desktop_is_media_ref ? (hero.image | resolve_media) : null %}
+{% set desktop_media_url_valid = desktop_media and desktop_media.type == 'image' and desktop_media.sourceUrl matches '#^https?://(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?[.])*[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?::[0-9]{1,5})?(?:/|[?#]|$)#' %}
+{% set desktop_url_valid = hero.image and not desktop_is_media_ref and hero.image matches '#^https?://(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?[.])*[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?::[0-9]{1,5})?(?:/|[?#]|$)#' %}
+{% set has_desktop_image = desktop_media_url_valid or desktop_url_valid %}
+
+{% set mobile_is_media_ref = hero.use_mobile_image and hero.image_mobile and hero.image_mobile starts with '@media-lib:' %}
+{% set mobile_media = mobile_is_media_ref ? (hero.image_mobile | resolve_media) : null %}
+{% set mobile_media_url_valid = mobile_media and mobile_media.type == 'image' and mobile_media.sourceUrl matches '#^https?://(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?[.])*[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?::[0-9]{1,5})?(?:/|[?#]|$)#' %}
+{% set mobile_url_valid = hero.use_mobile_image and hero.image_mobile and not mobile_is_media_ref and hero.image_mobile matches '#^https?://(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?[.])*[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?::[0-9]{1,5})?(?:/|[?#]|$)#' %}
+{% set has_mobile_image = mobile_media_url_valid or mobile_url_valid %}
+{% set has_responsive_images = has_desktop_image and has_mobile_image %}
+{% set show_placeholder = not has_desktop_image and not has_mobile_image %}
 {% set image_alt = hero.image | media_alt | default('accessibility.hero' | t) %}
 {% set image_mobile_alt = hero.image_mobile | media_alt | default('accessibility.hero' | t) %}
 
@@ -48,18 +58,20 @@
   {% set is_priority_section = section.index <= (template in ['home', 'product'] ? 1 : 2) %}
   <div class="{% if parallax %}js-hero-parallax{% endif %} media-visual">
     {# A mobile art-directed image is emitted as one picture so the browser selects only one source. #}
-    {% if has_mobile_image %}
-      {% set desktop_image = hero.image ? hero.image : ('images/placeholders/hero/hero.webp' | static_url) %}
+    {% if has_responsive_images %}
       {% include 'snippets/image.tpl' with {
-        image_src: desktop_image,
+        image_src: hero.image,
+        image_resolved_media: desktop_media_url_valid ? desktop_media : null,
         image_mobile_src: hero.image_mobile,
+        image_mobile_resolved_media: mobile_media_url_valid ? mobile_media : null,
         image_mobile_media_query: '(max-width: 767.98px)',
-        image_alt: hero.image ? image_alt : image_mobile_alt,
+        image_alt: image_alt,
+        image_mobile_alt: image_mobile_alt,
         image_classes: not is_priority_section ? 'fade-in lazyload',
         image_priority_high: is_priority_section,
         image_lazy: not is_priority_section,
         image_lazy_js: false,
-        image_thumbs: not hero.image ? false : null,
+        image_sizes: '100vw',
         image_width: hero.image ? hero.image_width : 1280,
         image_height: hero.image ? hero.image_height : 700,
         image_mobile_width: hero.image_mobile_width,
@@ -69,11 +81,12 @@
       {% if not is_priority_section %}
         <div class="placeholder placeholder-fade"></div>
       {% endif %}
-    {% elseif hero.image %}
+    {% elseif has_desktop_image %}
       {# Preserve the current single-image path when no mobile alternative is configured. #}
       {% set desktop_lazy = not is_priority_section %}
       {% include 'snippets/image.tpl' with {
         image_src: hero.image,
+        image_resolved_media: desktop_media_url_valid ? desktop_media : null,
         image_alt: image_alt,
         image_classes: desktop_lazy ? 'fade-in',
         image_priority_high: is_priority_section,
@@ -83,6 +96,25 @@
         image_aspect_ratio: hero.image_width and hero.image_height,
       } %}
       {% if desktop_lazy %}
+        <div class="placeholder placeholder-fade"></div>
+      {% endif %}
+    {% elseif has_mobile_image %}
+      {# With no valid desktop image, reuse the mobile asset at every width. #}
+      {% set mobile_lazy = not is_priority_section %}
+      {% include 'snippets/image.tpl' with {
+        image_src: hero.image_mobile,
+        image_resolved_media: mobile_media_url_valid ? mobile_media : null,
+        image_alt: image_mobile_alt,
+        image_classes: mobile_lazy ? 'fade-in',
+        image_priority_high: is_priority_section,
+        image_lazy: mobile_lazy,
+        image_lazy_js: false,
+        image_thumbs: mobile_media_url_valid ? null : false,
+        image_width: hero.image_mobile_width,
+        image_height: hero.image_mobile_height,
+        image_aspect_ratio: hero.image_mobile_width and hero.image_mobile_height,
+      } %}
+      {% if mobile_lazy %}
         <div class="placeholder placeholder-fade"></div>
       {% endif %}
     {% elseif show_placeholder %}
--- a/snippets/image.tpl
+++ b/snippets/image.tpl
@@ -25,18 +25,49 @@
 {% endif %}
 
 {# Resolve media library references (theme editor image_picker settings or product metafields) into image data with srcsets #}
-{% set media = image_src is defined and image_src starts with '@media-lib:' ? (image_src | resolve_media) : null %}
-
-{# Optional art direction for one responsive <picture>. This path is opt-in; callers
-   without image_mobile_src keep the existing markup below unchanged. #}
-{% set mobile_media = image_mobile_src is defined and image_mobile_src starts with '@media-lib:' ? (image_mobile_src | resolve_media) : null %}
-{% set has_art_direction = image_mobile_src is defined and image_mobile_src and (not mobile_media or mobile_media.type == 'image') %}
-{% if mobile_media and mobile_media.type == 'image' %}
-	{% set image_mobile_src = mobile_media.sourceUrl %}
+{# Resolve editor media once in the section and pass the result when available. #}
+{% set image_src_is_media_ref = image_src is defined and image_src and image_src starts with '@media-lib:' %}
+{% set media = image_resolved_media is defined ? image_resolved_media : (image_src_is_media_ref ? (image_src | resolve_media) : null) %}
+{% set image_media_url_valid = media and media.type == 'image' and media.sourceUrl matches '#^https?://(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?[.])*[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?::[0-9]{1,5})?(?:/|[?#]|$)#' %}
+{% set image_raw_url_valid = image_src is defined and image_src and not image_src_is_media_ref and image_src matches '#^https?://(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?[.])*[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?::[0-9]{1,5})?(?:/|[?#]|$)#' %}
+{% set image_art_direction_requested = image_mobile_src is defined and image_mobile_src %}
+{% set image_desktop_url_valid = image_media_url_valid or (image_art_direction_requested and image_raw_url_valid) %}
+{% set image_source_invalid = image_src_is_media_ref and not image_media_url_valid %}
+
+{# The mobile input is accepted only as a resolved image or an absolute HTTP(S) URL. #}
+{% set mobile_src_is_media_ref = image_mobile_src is defined and image_mobile_src and image_mobile_src starts with '@media-lib:' %}
+{% set mobile_media = image_mobile_resolved_media is defined ? image_mobile_resolved_media : (mobile_src_is_media_ref ? (image_mobile_src | resolve_media) : null) %}
+{% set mobile_media_url_valid = mobile_media and mobile_media.type == 'image' and mobile_media.sourceUrl matches '#^https?://(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?[.])*[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?::[0-9]{1,5})?(?:/|[?#]|$)#' %}
+{% set mobile_raw_url_valid = image_mobile_src is defined and image_mobile_src and not mobile_src_is_media_ref and image_mobile_src matches '#^https?://(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?[.])*[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?::[0-9]{1,5})?(?:/|[?#]|$)#' %}
+{% set mobile_source_url_valid = mobile_media_url_valid or mobile_raw_url_valid %}
+{% set image_mobile_src = mobile_media_url_valid ? mobile_media.sourceUrl : (mobile_raw_url_valid ? image_mobile_src : null) %}
+{% if mobile_media_url_valid %}
 	{% if not image_mobile_width %}{% set image_mobile_width = mobile_media.sourceWidth %}{% endif %}
 	{% if not image_mobile_height %}{% set image_mobile_height = mobile_media.sourceHeight %}{% endif %}
 	{% if not image_mobile_alt and mobile_media.altText %}{% set image_mobile_alt = mobile_media.altText %}{% endif %}
 {% endif %}
+
+{# If desktop is unavailable, use the valid mobile image alone at every width. #}
+{% if image_art_direction_requested and not image_desktop_url_valid and mobile_source_url_valid %}
+	{% set image_src = image_mobile_src %}
+	{% set media = mobile_media_url_valid ? mobile_media : null %}
+	{% set image_width = image_mobile_width %}
+	{% set image_height = image_mobile_height %}
+	{% set image_alt = image_mobile_alt is defined and image_mobile_alt ? image_mobile_alt : image_alt %}
+	{% set image_thumbs = mobile_media_url_valid ? image_thumbs : false %}
+	{% set image_source_invalid = false %}
+	{% set image_mobile_src = null %}
+{% elseif image_art_direction_requested and not image_desktop_url_valid %}
+	{% set image_src = null %}
+	{% set media = null %}
+	{% set image_source_invalid = true %}
+{% elseif image_media_url_valid %}
+	{% set image_src = media.sourceUrl %}
+{% elseif image_source_invalid %}
+	{% set image_src = null %}
+{% endif %}
+
+{% set has_art_direction = image_art_direction_requested and image_desktop_url_valid and mobile_source_url_valid %}
 
 {% if media %}
 	{% set image_src = media.sourceUrl %}
@@ -144,13 +175,23 @@
 	{% set image_aspect_ratio = true %}
 {% endif %}
 
+{# Preserve Tiendanube's original responsive widths for the mobile art-direction fallback. #}
+{% set mobile_original_srcset = '' %}
+{% if has_art_direction and mobile_media_url_valid %}
+	{% for srcSet in mobile_media.srcSets if srcSet.format == 'original' %}
+		{% for size in srcSet.sizes %}
+			{% set mobile_original_srcset = mobile_original_srcset ~ (mobile_original_srcset ? ', ' : '') ~ srcSet.baseUrl ~ size.w ~ '.' ~ mobile_media.extension ~ ' ' ~ size.w ~ 'w' %}
+		{% endfor %}
+	{% endfor %}
+{% endif %}
+
 {# Resolve data-src fallback for non-media images #}
 {% set data_src = image_src ? image_src : default_image_url %}
 
 {# @media-lib references with processed thumbnails get <picture> with AVIF/WebP <source> elements.
    Everything else (products, categories, blog, or images still processing) uses a plain <img>.
    Bail when a @media-lib ref resolves to non-image media (e.g. video or orphan uuid from a metafield). #}
-{% if not media or media.type == 'image' %}
+{% if (not media or media.type == 'image') and not image_source_invalid %}
 	{% if has_art_direction %}
 		<picture>
 			{# Sources are ordered mobile-first and only the matching media source is eligible. #}
@@ -171,7 +212,8 @@
 				{% endfor %}
 				<source
 					media="{{ image_mobile_media_query | default('(max-width: 767.98px)') }}"
-					{% if image_lazy_js %}data-{% endif %}srcset="{{ image_mobile_src }}"
+					{% if image_lazy_js %}data-{% endif %}srcset="{{ mobile_original_srcset ? mobile_original_srcset : image_mobile_src }}"
+					{% if image_sizes %}sizes="{{ image_sizes }}"{% endif %}
 					{% if image_mobile_width %}width="{{ image_mobile_width }}"{% endif %}
 					{% if image_mobile_height %}height="{{ image_mobile_height }}"{% endif %}
 				/>
@@ -179,6 +221,7 @@
 				<source
 					media="{{ image_mobile_media_query | default('(max-width: 767.98px)') }}"
 					{% if image_lazy_js %}data-{% endif %}srcset="{{ image_mobile_src }}"
+					{% if image_sizes %}sizes="{{ image_sizes }}"{% endif %}
 					{% if image_mobile_width %}width="{{ image_mobile_width }}"{% endif %}
 					{% if image_mobile_height %}height="{{ image_mobile_height }}"{% endif %}
 				/>
@@ -199,7 +242,8 @@
 				{% endfor %}
 			{% endif %}
 			<source
-				{% if image_lazy_js %}data-{% endif %}srcset="{{ media ? media.sourceUrl : image_src }}"
+				{% if image_lazy_js %}data-{% endif %}srcset="{{ media and srcset ? srcset : image_src }}"
+				{% if image_sizes %}sizes="{{ image_sizes }}"{% endif %}
 				{% if image_width %}width="{{ image_width }}"{% endif %}
 				{% if image_height %}height="{{ image_height }}"{% endif %}
 			/>
````

## Evidencia histórica de producción — captura del 17-11-2026

La única navegación autorizada fue desktop, 1440×900, DPR 1, a la home publicada. La captura informa HTTP 200, `content-encoding: br` y conserva el cuerpo como artefacto con SHA256. Los valores de tamaño de CDP se presentan con sus nombres exactos; no se reinterpretan como tamaño Brotli efectivo porque los campos del recibo no son consistentes entre sí. `browserResponseBufferBytes` describe el buffer del cuerpo capturado, no se presenta como bytes transferidos comprimidos.

La evidencia directa muestra dos variantes de hero en el HTML recibido. En la captura de red se registraron como completadas dos imágenes AVIF distintas: móvil 820 (`encodedDataLength` 32.237) y desktop 1920 (31.760), ambas iniciadas por parser y HTTP 200. El LCP desktop observado fue el AVIF desktop a 1.676 ms; el HTML inicial desktop usaba placeholder GIF en `src` y `data-srcset`, mientras el `<img>` móvil tenía `srcset` activo y `fetchpriority="high"` aunque estaba marcado `d-md-none`. Esto acredita doble transferencia en esa sesión y descubrimiento diferido de desktop en esa sesión; no demuestra que cada visita o dispositivo repita el patrón.

El cuerpo completo capturado mide 1.174.783 bytes como buffer conservado, SHA256 indicado en los metadatos; no se reproduce entero aquí porque el dato decisivo para esta revisión son los tags exactos de hero y registros de red que se incluyen literalmente.

## Metadatos y registros pertinentes de captura

- Ruta lógica: `reports/runs/rhino-performance/20261117T-html-capture-authorized-03/desktop-analysis.json (extracto estructurado exacto)`
- Clasificación: evidencia histórica de producción
- SHA256 del origen: `2df8c69d91b186048b04f653c2bbf1b6f272fdeb277aabf74e9f14a47850049f`

````
{
  "capture_at": "2026-11-17T19:39:42.681Z",
  "requested_url": "https://rhino-performance.com/",
  "profile": {
    "name": "desktop",
    "width": 1440,
    "height": 900,
    "dpr": 1,
    "isMobile": false
  },
  "main_response": {
    "status": 200,
    "finalURL": "https://rhino-performance.com/",
    "headers": {
      "contentType": "text/html; charset=UTF-8",
      "contentEncoding": "br",
      "contentLength": null,
      "transferEncoding": null,
      "cacheControl": "public, s-maxage=86400, no-store"
    },
    "browserResponseBufferBytes": 1174783,
    "sha256": "7da336fc86f03ba9d618000d3d4ea56125e2b1cc4957f8495a91b671f1852fc8",
    "encodedDataLengthCDP": 111853,
    "responseEncodedDataLengthCDP": 18739
  },
  "network_request_count": 94,
  "navigation_records": [
    {
      "url": "https://rhino-performance.com/",
      "method": "GET",
      "frameId": "556EDEEFF2CAB935692586FE012B376C"
    }
  ],
  "hero_image_requests": [
    {
      "url": "https://acdn-us.mitiendanube.com/stores/007/400/935/media/fc9598f3-rhino-performance-bfm/avif/820.avif",
      "status": 200,
      "initiator": "parser",
      "encodedDataLength": 32237,
      "fromDiskCache": false,
      "failed": null
    },
    {
      "url": "https://acdn-us.mitiendanube.com/stores/007/400/935/media/95cbfc17-rhino-performance-bf/avif/1920.avif",
      "status": 200,
      "initiator": "parser",
      "encodedDataLength": 31760,
      "fromDiskCache": false,
      "failed": null
    }
  ],
  "hero_lcp_entries": [
    {
      "startTime": 1676,
      "renderTime": 1676,
      "loadTime": 1300.699999999255,
      "size": 1036800,
      "url": "https://acdn-us.mitiendanube.com/stores/007/400/935/media/95cbfc17-rhino-performance-bf/avif/1920.avif",
      "tag": "IMG",
      "id": "",
      "className": "d-none d-md-block fade-in lazyloaded"
    }
  ]
}
````

## Tags exactos de la respuesta HTML inicial

- Ruta lógica: `reports/runs/rhino-performance/20261117T-html-capture-authorized-03/desktop-response-body.html (tags hero extraídos literalmente)`
- Clasificación: evidencia histórica de producción; extracto verbatim
- SHA256 del origen: `7da336fc86f03ba9d618000d3d4ea56125e2b1cc4957f8495a91b671f1852fc8`

````
<img
							width="1920"
				height="900"
					class="lazyload d-none d-md-block fade-in"
						alt="Hero"

							src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="									data-srcset="https://acdn-us.mitiendanube.com/stores/007/400/935/media/95cbfc17-rhino-performance-bf/original/50.jpg 50w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/95cbfc17-rhino-performance-bf/original/100.jpg 100w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/95cbfc17-rhino-performance-bf/original/240.jpg 240w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/95cbfc17-rhino-performance-bf/original/320.jpg 320w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/95cbfc17-rhino-performance-bf/original/480.jpg 480w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/95cbfc17-rhino-performance-bf/original/640.jpg 640w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/95cbfc17-rhino-performance-bf/original/1024.jpg 1024w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/95cbfc17-rhino-performance-bf/original/1400.jpg 1400w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/95cbfc17-rhino-performance-bf/original/1920.jpg 1920w"
														style="aspect-ratio: 1920 / 900"
					/>

<img
						fetchpriority="high"
				width="820"
				height="1000"
					class=" image-priority-high d-md-none "
						alt="Hero"

							src="https://acdn-us.mitiendanube.com/stores/007/400/935/media/fc9598f3-rhino-performance-bfm/source.jpg"
				srcset="https://acdn-us.mitiendanube.com/stores/007/400/935/media/fc9598f3-rhino-performance-bfm/original/50.jpg 50w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/fc9598f3-rhino-performance-bfm/original/100.jpg 100w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/fc9598f3-rhino-performance-bfm/original/240.jpg 240w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/fc9598f3-rhino-performance-bfm/original/320.jpg 320w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/fc9598f3-rhino-performance-bfm/original/480.jpg 480w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/fc9598f3-rhino-performance-bfm/original/640.jpg 640w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/fc9598f3-rhino-performance-bfm/original/820.jpg 820w"										style="aspect-ratio: 820 / 1000"
					/>
````

## Evidencia histórica de trazas y Lighthouse

La traza previa proporciona observaciones de LCP para mobile y desktop bajo perfiles de laboratorio distintos. No se usa como medición posterior al candidato. El CSV conserva diez muestras Lighthouse de 13-11-2026; su variabilidad de benchmark impide una atribución estable de cambios. Se adjuntan literalmente datos y perfiles, no para afirmar que este candidato ya mejoró.

## Extracto de LCP móvil/escritorio

- Ruta lógica: `reports/rhino-performance/performance-first-correction-20261113T180949/trace-findings.json`
- Clasificación: evidencia histórica
- SHA256 del origen: `3df402f0d0153e45edb1a21d235607d3bf92b11a3d5085854a435e66d24458b1`

````
[
  {
    "device": "mobile",
    "profile": {
      "width": 412,
      "height": 823,
      "DPR": 1.75,
      "cpu_rate": 4,
      "latency_ms": 150,
      "throughput_kbps": 1638.4,
      "cache": "disabled",
      "consent": "fresh/no choice",
      "trace_window": "20s after DOMContentLoaded; coverage/profiler instrumentation enabled"
    },
    "lcp_observed": {
      "start": 2100,
      "duration": 0,
      "url": "https://acdn-us.mitiendanube.com/stores/007/400/935/media/fc9598f3-rhino-performance-bfm/avif/820.avif",
      "tag": "IMG",
      "classes": " image-priority-high d-md-none ",
      "outer": "<img fetchpriority=\"high\" width=\"820\" height=\"1000\" class=\" image-priority-high d-md-none \" alt=\"Hero\" src=\"https://acdn-us.mitiendanube.com/stores/007/400/935/media/fc9598f3-rhino-performance-bfm/source.jpg\" srcset=\"https://acdn-us.mitiendanube.com/stores/007/400/935/media/fc9598f3-rhino-performance-bfm/original/50.jpg 50w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/fc9598f3-rhino-performance-bfm/original/100.jpg 100w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/fc9598f3-rhino-performance-bfm/original/240.jpg 240w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/fc9598f3-rhino-performance-bfm/original/320.jpg 320w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/fc9598f3-rhino-performance-bfm/original/480.jpg 480w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/fc9598f3-rhino-performance-bfm/original/640.jpg 640w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/fc9598f3-rhino-performance-bfm/original/820.jpg 820w\" style=\"aspect-ratio: 820 / 1000\">"
    }
  },
  {
    "device": "desktop",
    "profile": {
      "width": 1440,
      "height": 900,
      "DPR": 1,
      "cpu_rate": 1,
      "latency_ms": 40,
      "throughput_kbps": 10240,
      "cache": "disabled",
      "consent": "fresh/no choice",
      "trace_window": "20s after DOMContentLoaded; coverage/profiler instrumentation enabled"
    },
    "lcp_observed": {
      "start": 1880,
      "duration": 0,
      "url": "https://acdn-us.mitiendanube.com/stores/007/400/935/media/95cbfc17-rhino-performance-bf/avif/1920.avif",
      "tag": "IMG",
      "classes": "d-none d-md-block fade-in lazyloaded",
      "outer": "<img width=\"1920\" height=\"900\" class=\"d-none d-md-block fade-in lazyloaded\" alt=\"Hero\" src=\"data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==\" data-srcset=\"https://acdn-us.mitiendanube.com/stores/007/400/935/media/95cbfc17-rhino-performance-bf/original/50.jpg 50w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/95cbfc17-rhino-performance-bf/original/100.jpg 100w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/95cbfc17-rhino-performance-bf/original/240.jpg 240w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/95cbfc17-rhino-performance-bf/original/320.jpg 320w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/95cbfc17-rhino-performance-bf/original/480.jpg 480w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/95cbfc17-rhino-performance-bf/original/640.jpg 640w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/95cbfc17-rhino-performance-bf/original/1024.jpg 1024w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/95cbfc17-rhino-performance-bf/original/1400.jpg 1400w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/95cbfc17-rhino-performance-bf/original/1920.jpg 1920w\" style=\"aspect-ratio: 1920 / 900\" srcset=\"https://acdn-us.mitiendanube.com/stores/007/400/935/media/95cbfc17-rhino-performance-bf/original/50.jpg 50w, https://acdn-us.mitiendanube.com/stores/007/400/935/media/95cbfc17-rhino-performance-bf/original/100.jpg 100w, https://acdn-us.mitiendanube.com/stores/007/400/935/med"
    }
  }
]
````

## Diez muestras Lighthouse conservadas (CSV íntegro)

- Ruta lógica: `reports/rhino-performance/performance-first-correction-20261113T180949/lighthouse-ten-samples.csv`
- Clasificación: evidencia histórica
- SHA256 del origen: `65690c16172b323225e71b76743c682682891fb00eb07080293c935dbcf921a7`

````
lcp,fcp,cls,tbt,speed_index,device,sample,performance,bytes_transferred,bootup_ms,benchmark_index,measured_at,raw_sample,raw_sha256,bytes_total,bytes_script,bytes_image,bytes_stylesheet,bytes_document,bytes_other,bytes_font,bytes_media,bytes_third-party
4557.451999999999,2033.911,0.0003354122826859878,2295.000000000001,4181.4465716754485,mobile,1,52,2315615,5097.175999999973,1977,2026-11-13T18:13:53.993Z,reports/runs/rhino-performance/20261113T181340-lighthouse-job-385201fb/browser/sample-1.json,755cab89d4f3c5d340eeb4a95a4aefe24295728f6abfef77e9ac1695dca82ae1,2315615,1439074,530961,140649,117434,56085,31412,0,2199380
2028.2775,440.337,0.06802784767825351,169.40225000000032,1412.3152945484321,desktop,1,84,2543591,982.6640000000025,1862.5,2026-11-13T18:14:27.587Z,reports/runs/rhino-performance/20261113T181413-lighthouse-job-bd52f7b0/browser/sample-1.json,9051c47dd3365eae6f23a1c487ed8d59cb0ef9f95485658c1d9dad057f15f774,2543591,1439066,758153,141043,117440,56477,31412,0,2427359
3214.034,1908.683,0.0003292308063223839,2751.0,3924.436305725977,mobile,2,61,1842889,4939.455999999995,1915,2026-11-13T18:15:04.030Z,reports/runs/rhino-performance/20261113T181448-lighthouse-job-0a9419a9/browser/sample-1.json,f32b391bbdda10bd06e76f9b5acbfb048a0e234e9a73fd6a26cdcd1894c2d56b,1842889,1154090,437273,58637,117431,44046,31412,0,1726663
3084.721499999999,967.1509999999998,0.06132673197034702,247.50000000000045,2267.792716584455,desktop,2,67,2491630,1081.9640000000043,1870,2026-11-13T18:15:42.841Z,reports/runs/rhino-performance/20261113T181530-lighthouse-job-a236fb70/browser/sample-1.json,a64c58d05ef4f6c2f3bb032e34faa1710d0eaff5d055c2109925b3806e046101,2491630,1438213,719478,140599,117438,44490,31412,0,2375401
3641.201,1758.888,0.0003354122826859878,2522.5,3712.559127595664,mobile,3,59,2314959,4936.3559999999725,1792.5,2026-11-13T18:16:18.061Z,reports/runs/rhino-performance/20261113T181604-lighthouse-job-345e6d04/browser/sample-1.json,402039282e8d6e3a15ffe455cbc9284e8e95a009fecd4b76dab4e05a27908c13,2314959,1438148,530928,140421,117428,56622,31412,0,2198735
2513.433,603.884,0.05271552403467297,771.0,2435.090403105487,desktop,3,54,2542119,1859.121999999997,1530.5,2026-11-13T18:16:58.658Z,reports/runs/rhino-performance/20261113T181641-lighthouse-job-db7a18c0/browser/sample-1.json,1d672af49986bc502e97cd012332e83dfb7e53e72468e218e9cfb81eb9d5a362,2542119,1438464,758333,140394,117434,56082,31412,0,2425868
4414.8895,1766.87,0.0003292308063223839,4107.999999999999,4219.906117502567,mobile,4,52,2315269,7395.743999999983,1009,2026-11-13T18:17:45.537Z,reports/runs/rhino-performance/20261113T181727-lighthouse-job-f7ac2535/browser/sample-1.json,904022f44eb9f8311cf85c302c5698c4c12b3878a9d55bf9ac11a0cb0932a020,2315269,1438718,531264,140396,117370,56109,31412,0,2199094
2309.61725,551.009,0.05271552403467297,986.3192499999996,2436.71584070894,desktop,4,53,2070023,2039.757999999996,927.5,2026-11-13T18:18:28.503Z,reports/runs/rhino-performance/20261113T181812-lighthouse-job-195ef9ef/browser/sample-1.json,974f648bb05b67198f85d723db9b4abfe26ef1e411fd7cef0d64e988abd877e3,2070023,1154135,664505,58634,117441,43896,31412,0,1953777
4714.1525,2203.7920000000004,0.0003292308063223839,6011.156000000002,5194.956278436177,mobile,5,47,2315040,8647.067999999968,842,2026-11-13T18:19:14.889Z,reports/runs/rhino-performance/20261113T181858-lighthouse-job-a7958a67/browser/sample-1.json,6e4a9769479211627516b150c12a142163bf74d703e12e18ffb3007cc4b8fb49,2315040,1438024,530994,140604,117446,56560,31412,0,2198798
3351.5260000000007,927.8800000000001,0.05271552403467297,1003.0357499999998,2381.883979805194,desktop,5,46,2542161,2137.854999999988,848.5,2026-11-13T18:19:56.397Z,reports/runs/rhino-performance/20261113T181943-lighthouse-job-d53974f5/browser/sample-1.json,cdf1001559d8a8bd348b74afb92acce97637dd0b77cc44f0cc487e2b2dd94831,2542161,1438348,758365,140524,117433,56079,31412,0,2425931
````

## Estado sintético actual de D1/D2/R1/R4

| Hallazgo | Comportamiento que afirman los fixtures actuales | Límite |
|---|---|---|
| D1 solo móvil | Una imagen móvil se usa como único recurso en anchos móvil y desktop; sin placeholder adicional. | Tabla de decisión sintética; falta renderer real. |
| D2 referencia interna no resuelta | Se excluye `@media-lib:` inválida de `src/srcset`; variantes desktop/móvil opuestas se conservan si la otra es válida. | `resolve_media` real no se ejecuta en la prueba. |
| R1 medio desktop tipo video | Se conserva la imagen móvil válida y una sola imagen efectiva; caso inverso conserva desktop si el medio móvil no es imagen. | Tipos de medio del CMS deben comprobarse en Tiendanube. |
| R4 fallback responsive | Se preservan `srcset` original móvil y desktop cuando están disponibles; AVIF/WebP salen de `srcSets`. | Verificación de estructura fuente/fixture, no del servicio real. |

## Reproducciones sintéticas D1/D2

- Ruta lógica: `tests/reproduction-results.json`
- Clasificación: prueba sintética; no es salida de Tiendanube
- SHA256 del origen: `01ae1b2e0cd4a1240db9253e01a35c0db07af859c6447cdecf30a4348d59fe3f`

````
{
  "kind": "static-template-reproduction",
  "network": "none",
  "reproduced": [
    "D1",
    "D2"
  ],
  "limitations": [
    "Source-level reproduction; no Tiendanube Twig renderer available."
  ],
  "cases": [
    {
      "input": {
        "desktop": null,
        "mobile": "@media-lib:valid-mobile"
      },
      "priorDesktopSource": "images/placeholders/hero/hero.webp",
      "expected": "mobile image at both viewport classes"
    },
    {
      "input": {
        "mobile": "@media-lib:orphan",
        "resolve_media": null
      },
      "priorGuard": true,
      "priorMarkup": "<source srcset=\"@media-lib:orphan\">",
      "expected": "reject internal ref and emit no invalid URL"
    }
  ]
}
````

## Resultados sintéticos responsive — 60 casos

- Ruta lógica: `tests/hero-responsive-fallback-results.json`
- Clasificación: prueba sintética; no es salida de Tiendanube
- SHA256 del origen: `8779906519c499f55504e6d166f54f1040a3ae31e4f383f7484b2bce319fcc56`

````
{
  "kind": "synthetic-browser-fallback-fixture",
  "network": "only intercepted fixtures.invalid; no external network",
  "widths": [
    360,
    390,
    412,
    767,
    768,
    1024,
    1440,
    1920
  ],
  "cases": 60,
  "sourceAssertions": 13,
  "checks": [
    "hero valida por separado ambas variantes y exige medio de imagen con URL HTTP(S)",
    "URL directa exige esquema y host con etiquetas válidas, no cualquier cadena",
    "si solo la imagen móvil es válida se usa como única imagen en ambos anchos",
    "el placeholder de hero queda limitado al caso sin ninguna imagen válida",
    "el helper no renderiza referencias internas de medios sin resolver",
    "la alternativa móvil distingue referencia resuelta de URL externa validada",
    "el helper rechaza texto arbitrario e identificadores internos no resueltos en art direction",
    "fallback original móvil conserva srcset responsive cuando Tiendanube lo entrega",
    "fallback original desktop conserva srcset responsive cuando Tiendanube lo entrega",
    "formatos AVIF/WebP siguen procediendo exclusivamente de srcSets",
    "dimensiones disponibles se conservan para sources y fallback",
    "hero solo móvil usa su texto alternativo propio",
    "la hero existente permanece como primera sección; home.json no requiere cambio"
  ],
  "results": [
    {
      "label": "both",
      "width": 360,
      "mode": "picture",
      "currentSrc": "https://fixtures.invalid/mobile-webp-640.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "desktop-only",
      "width": 360,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/desktop-480.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "mobile-only-D1",
      "width": 360,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/mobile-640.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero móvil",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "both",
      "width": 390,
      "mode": "picture",
      "currentSrc": "https://fixtures.invalid/mobile-webp-640.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "desktop-only",
      "width": 390,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/desktop-480.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "mobile-only-D1",
      "width": 390,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/mobile-640.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero móvil",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "both",
      "width": 412,
      "mode": "picture",
      "currentSrc": "https://fixtures.invalid/mobile-webp-820.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero",
      "cls": 0,
      "priority": "high",
      "loading": null
    },
    {
      "label": "desktop-only",
      "width": 412,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/desktop-1024.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "mobile-only-D1",
      "width": 412,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/mobile-820.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero móvil",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "both",
      "width": 767,
      "mode": "picture",
      "currentSrc": "https://fixtures.invalid/mobile-webp-820.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "desktop-only",
      "width": 767,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/desktop-1024.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "mobile-only-D1",
      "width": 767,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/mobile-820.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero móvil",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "both",
      "width": 768,
      "mode": "picture",
      "currentSrc": "https://fixtures.invalid/desktop-1024.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "desktop-only",
      "width": 768,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/desktop-1024.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "mobile-only-D1",
      "width": 768,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/mobile-820.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero móvil",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "both",
      "width": 1024,
      "mode": "picture",
      "currentSrc": "https://fixtures.invalid/desktop-1024.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "desktop-only",
      "width": 1024,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/desktop-1024.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "mobile-only-D1",
      "width": 1024,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/mobile-820.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero móvil",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "both",
      "width": 1440,
      "mode": "picture",
      "currentSrc": "https://fixtures.invalid/desktop-1920.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "desktop-only",
      "width": 1440,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/desktop-1920.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "mobile-only-D1",
      "width": 1440,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/mobile-820.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero móvil",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "both",
      "width": 1920,
      "mode": "picture",
      "currentSrc": "https://fixtures.invalid/desktop-1920.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "desktop-only",
      "width": 1920,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/desktop-1920.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "mobile-only-D1",
      "width": 1920,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/mobile-820.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero móvil",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "unresolved-mobile-D2-desktop-survives",
      "width": 412,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/desktop-1024.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "unresolved-desktop-D2-mobile-survives",
      "width": 412,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/mobile-820.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero móvil",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "video-desktop-R1-mobile-survives",
      "width": 412,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/mobile-820.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero móvil",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "video-mobile-desktop-survives",
      "width": 412,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/desktop-1024.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "arbitrary-desktop-rejected-mobile-survives",
      "width": 412,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/mobile-820.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero móvil",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "arbitrary-mobile-rejected-desktop-survives",
      "width": 412,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/desktop-1024.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "unresolved-mobile-D2-desktop-survives",
      "width": 767,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/desktop-1024.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "unresolved-desktop-D2-mobile-survives",
      "width": 767,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/mobile-820.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero móvil",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "video-desktop-R1-mobile-survives",
      "width": 767,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/mobile-820.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero móvil",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "video-mobile-desktop-survives",
      "width": 767,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/desktop-1024.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "arbitrary-desktop-rejected-mobile-survives",
      "width": 767,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/mobile-820.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero móvil",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "arbitrary-mobile-rejected-desktop-survives",
      "width": 767,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/desktop-1024.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "unresolved-mobile-D2-desktop-survives",
      "width": 768,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/desktop-1024.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "unresolved-desktop-D2-mobile-survives",
      "width": 768,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/mobile-820.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero móvil",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "video-desktop-R1-mobile-survives",
      "width": 768,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/mobile-820.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero móvil",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "video-mobile-desktop-survives",
      "width": 768,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/desktop-1024.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "arbitrary-desktop-rejected-mobile-survives",
      "width": 768,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/mobile-820.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero móvil",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "arbitrary-mobile-rejected-desktop-survives",
      "width": 768,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/desktop-1024.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "unresolved-mobile-D2-desktop-survives",
      "width": 1440,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/desktop-1920.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "unresolved-desktop-D2-mobile-survives",
      "width": 1440,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/mobile-820.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero móvil",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "video-desktop-R1-mobile-survives",
      "width": 1440,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/mobile-820.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero móvil",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "video-mobile-desktop-survives",
      "width": 1440,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/desktop-1920.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "arbitrary-desktop-rejected-mobile-survives",
      "width": 1440,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/mobile-820.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero móvil",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "arbitrary-mobile-rejected-desktop-survives",
      "width": 1440,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/desktop-1920.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "unresolved-mobile-D2-desktop-survives",
      "width": 1920,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/desktop-1920.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "unresolved-desktop-D2-mobile-survives",
      "width": 1920,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/mobile-820.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero móvil",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "video-desktop-R1-mobile-survives",
      "width": 1920,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/mobile-820.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero móvil",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "video-mobile-desktop-survives",
      "width": 1920,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/desktop-1920.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "arbitrary-desktop-rejected-mobile-survives",
      "width": 1920,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/mobile-820.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero móvil",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "arbitrary-mobile-rejected-desktop-survives",
      "width": 1920,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/desktop-1920.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "none-placeholder",
      "width": 412,
      "mode": "placeholder",
      "currentSrc": "https://fixtures.invalid/placeholder-1280.svg",
      "requests": 1,
      "ratio": 1.8286,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "none-placeholder",
      "width": 768,
      "mode": "placeholder",
      "currentSrc": "https://fixtures.invalid/placeholder-1280.svg",
      "requests": 1,
      "ratio": 1.8286,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "none-placeholder",
      "width": 1440,
      "mode": "placeholder",
      "currentSrc": "https://fixtures.invalid/placeholder-1280.svg",
      "requests": 1,
      "ratio": 1.8286,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    },
    {
      "label": "first-priority-mobile-only",
      "width": 1440,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/mobile-820.svg",
      "requests": 1,
      "ratio": 0.82,
      "alt": "Hero móvil",
      "cls": 0,
      "priority": "high",
      "loading": null
    },
    {
      "label": "later-lazy-responsive",
      "width": 1440,
      "mode": "picture",
      "currentSrc": "https://fixtures.invalid/desktop-1920.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": "lazy"
    },
    {
      "label": "direct-absolute-url-accepted",
      "width": 1440,
      "mode": "single",
      "currentSrc": "https://fixtures.invalid/custom-desktop.svg",
      "requests": 1,
      "ratio": 2.1333,
      "alt": "Hero",
      "cls": 0,
      "priority": null,
      "loading": null
    }
  ],
  "limitations": [
    "The harness models the validated template decision table and markup; it does not render Twig or execute Tiendanube resolve_media.",
    "AVIF/WebP preservation is checked in template source and source-set data, not decoded from platform-served media.",
    "Real renderer, lazy-load timing, visual editor, production currentSrc and Lighthouse remain pending."
  ]
}
````

### Fuente del harness sintético

El paquete v4 conserva resultados sintéticos íntegros, pero no incorpora su script de ejecución. Se comprobó el hash del harness histórico suplementario: `aa60ad6ea7807eec6d5e438f766320e6a00b99515f8574282b9ea76ddcea69e0`. No se reejecutó. El script no se copia aquí porque incluye una ruta absoluta local de instalación; el JSON de resultados y la reproducción se incluyen íntegros y el hash queda registrado en el índice.

## Estado y límites del paquete v4

- Ruta lógica: `README.md`
- Clasificación: documentación del paquete
- SHA256 del origen: `e9074c43f3788fe85d4f2860fd00722cd9c19335be41ad039ab68ea39f4ea353`

````text
# Preflight actualizado de revisión read-only — hero D1/D2/R1/R4

Estado: **`needs_evidence`; Claude y Codex no fueron invocados.**

Este paquete conserva el candidato, dependencias y recibos históricos. El paquete v3 original permanece intacto. El nuevo preflight documenta la copia aislada del controlador con contrato tipado v2.

## Identidad del candidato

- `sections/hero.tpl`: `1e70c54c4c5bc38711272284843d8881c4354ac7725e9de56c0223b599c3e65d`
- `snippets/image.tpl`: `e4e622e0c561c4450138e7717a1e5af95cf19d0184aee5cbcb89990f7ada767e`
- Diff incremental: `ff73a41106aa153e30f0b84bf018ce89f80d693a68551eb39ab021ce1c09406b`
- Manifiesto externo v3 recibido/verificado: `33908cf593d8e327319746b13c7f9feed800a75adb0fb7999ebfa2874882b0ab`

## Contrato de revisión

**Candidatos:** `sections/hero.tpl`, `snippets/image.tpl`.

**Contexto de solo lectura:** `blocks/slide.tpl`, `blocks/banner.tpl`, `blocks/image.tpl`, `sections/hero-divided.tpl`, `sections/category-hero.tpl`, `layouts/layout.tpl`, `static/js/libraries-standalone.js`. Las rutas lógicas y sus hashes están en `manifest.json`.

**Escritura:** `write_files=[]`; las dos tareas tienen `task.allowed_files=[]`. Ambas leen los nueve archivos. `analysis.files` y los archivos del ADR se limitan a los dos candidatos. Una dependencia puede citarse como `source:<ruta>` si su recibo corresponde al ledger, run y hash, pero no declararse como archivo afectado ni escribible.

El tamaño conjunto de las nueve fuentes es **194.145 bytes**, dentro del límite de lectura de fuente de 300.000 bytes del controlador. Los contenidos están bajo `candidate/` y `context/`; el contrato usa las rutas lógicas sin prefijo.

La verificación v3 encontró coincidencia del manifiesto externo y de las 22 entradas declaradas; no hay discrepancias. El snapshot v3 no se modificó.

## Preflight local

**125 pruebas focalizadas pasaron; 0 fallos y 0 errores.** Casos: 2 candidatos + 7 contextos; subconjunto de escritura; cita de dependencia como evidencia; rechazo de contexto como diff; refs válidas, inexistentes y de otro run/candidato; read-only; dual council; agregación; recibos históricos. Sin proveedores, red ni producción. Log y resumen en `tests/controller-contract-focused-tests.*`.

Esto prueba la copia aislada; no constituye revisión independiente ni integración del controlador.

## Límite del sello de plan

`file_contract_sha256` detecta modificaciones si no se recalcula, pero es un hash no autenticado. No es una firma ni autorización y no evita que quien puede editar el JSON vuelva a sellarlo. El plan exacto debe revisarse antes de ejecución. No se añadió un sistema paralelo de permisos.

## Comando de planificación preparado (no ejecutado)

Después de revisar e integrar la adaptación, el plan se generaría con:

```bash
python3 tools/ia.py --project rhino-performance orchestrate plan "Revisión independiente read-only de la hero responsive D1/D2/R1/R4" --scope theme --read-only --council full \
  --candidate-file sections/hero.tpl \
  --candidate-file snippets/image.tpl \
  --context-file blocks/slide.tpl \
  --context-file blocks/banner.tpl \
  --context-file blocks/image.tpl \
  --context-file sections/hero-divided.tpl \
  --context-file sections/category-hero.tpl \
  --context-file layouts/layout.tpl \
  --context-file static/js/libraries-standalone.js
```

No se incluye `--write-file`; ambas tareas deben terminar con `allowed_files=[]`. El comando no se ejecutó porque el controlador operativo no se modificó y planificar releería la información local del proyecto. Una llamada posterior al consejo requiere autorización separada.
````

El contrato se conserva completo salvo la ruta absoluta de workspace, reemplazada por un marcador para no divulgar una ubicación local ajena; no cambia el texto técnico.

## Contrato conservado del helper de imágenes

- Ruta lógica: `reference/image-loading-contract.md`
- Clasificación: contexto/contrato; una ruta local redacted
- SHA256 del origen: `0cdb4b384a3c2162173d46284d864d22e73128a96efe895d6ce2cd7b5e4f23fd`

````text
# Selección y carga de imágenes

Fecha: 2026-11-08. Fuente principal: [snippets/image.tpl]([ruta local de workspace omitida]/snippets/image.tpl:17), callers hero/slide/item-image/product-image. Rendimiento de cada componente requiere Network del contexto correcto.

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
````

## Hallazgos D1/D2/R1/R4 y revisión histórica

El paquete v4 contiene los resultados sintéticos actuales que afirman cubrir D1/D2/R1/R4. La revisión de Claude reproducida abajo es anterior y corresponde al candidato previo, no al SHA actual; sirve como historial de objeciones y explica por qué se prepararon las correcciones. No es aprobación ni dictamen del candidato `ff73…`.

## Extracto de hipótesis relevantes de la revisión anterior

- Ruta lógica: `reference/previous-claude-review.json (campos response/analysis preservados)`
- Clasificación: revisión histórica de candidato anterior
- SHA256 del origen: `b7b4eb9fdfa2c592e2cdd2d62452141e7ecb7f19f24b479164a453ba474a0c9c`

````
{
  "requested_agent": "claude",
  "effective_agent": "claude",
  "round": 0,
  "decision": "changes_requested",
  "summary": "El enfoque es correcto: un solo <picture> con fuentes por media, con un único img y alt, y opt-in en el helper. Así se evita la doble descarga, y la rama sin imagen móvil queda igual a la original. Pido cambios por dos defectos concretos y un riesgo. D1, solo imagen móvil: en escritorio ahora se muestra y se descarga con prioridad el placeholder genérico, cuando antes se veía la imagen móvil. D2: la guarda de image.tpl no impide emitir '@media-lib:' como srcset si resolve_media devuelve null. R1: si el medio de escritorio no es una imagen, tampoco se muestra la móvil. Faltan las pruebas de plataforma: Twig real, filtro resolve_media, red/currentSrc y Lighthouse.",
  "historical_hypotheses": [
    "D1 (defecto, hero.tpl rama has_mobile_image): sin hero.image, desktop_image pasa a ser el placeholder estático con image_priority_high. Antes, el placeholder era lazy y la imagen móvil se pintaba sin d-md-none en todos los anchos. Ahora, en escritorio con 768 px o más se ve y se descarga con prioridad alta el placeholder genérico, en lugar de la imagen del comerciante.",
    "D2 (defecto condicional al contrato, image.tpl has_art_direction): con una referencia '@media-lib:' huérfana, si resolve_media devuelve null, 'not mobile_media' es true. En ese caso, la rama else emite <source srcset=\"@media-lib:...\">. La guarda debe distinguir 'no es media-lib' de 'media-lib no resuelta'.",
    "R1 (riesgo, image.tpl): si media (escritorio) no es de tipo image, el bloque externo 'if not media or media.type == image' omite todo el picture, incluida la imagen móvil válida. Antes, la imagen móvil se pintaba de forma independiente. Con image_picker es poco probable, pero conviene un fallback.",
    "R2 (riesgo): el include sin 'only' hereda el contexto del padre. Si algún consumidor (slide, banner, hero-divided, category-hero) define image_mobile_src o image_mobile_media_query en su contexto, activaría art direction sin querer. Hay que comprobarlo con rg.",
    "R3 (riesgo, alt): el único img usa image_alt de escritorio. En móvil se pierde el alt propio de la imagen móvil, y image_mobile_alt se calcula en el snippet pero no se usa en la salida (código muerto). Es una limitación inherente a picture; hay que documentarla.",
    "R4 (riesgo, rendimiento heredado): la fuente final sin type usa media.sourceUrl, una URL única a tamaño original sin descriptores w. En navegadores sin AVIF/WebP sustituye al srcset original responsive del img, que nunca se usa. Lo mismo ocurre con la fuente original móvil.",
    "R5 (riesgo, CLS con auto_height): el img pierde width/height y aspect-ratio, que pasan a los <source>. Depende de que el navegador soporte width/height en source. Con media-full-width/min-height no afecta, pero con auto_height=true sí.",
    "Observación baja: las secciones posteriores llevan 'fade-in lazyload' sin data-srcset y con loading=lazy nativo. LazySizes puede marcar lazyloaded antes de que termine la carga nativa y hacer el fade-in sobre un hueco. Es solo visual; los fixtures no lo comprueban."
  ]
}
````

## Archivo candidato íntegro — sections/hero.tpl

- Ruta lógica: `sections/hero.tpl`
- Clasificación: código candidato
- SHA256 del origen: `1e70c54c4c5bc38711272284843d8881c4354ac7725e9de56c0223b599c3e65d`

````
{#
  Hero Section
  Displays a full-width hero banner with customizable background image,
  overlay, and content blocks (text, buttons).
#}
{% set hero = section.settings %}

{# Images #}
{% set desktop_is_media_ref = hero.image and hero.image starts with '@media-lib:' %}
{% set desktop_media = desktop_is_media_ref ? (hero.image | resolve_media) : null %}
{% set desktop_media_url_valid = desktop_media and desktop_media.type == 'image' and desktop_media.sourceUrl matches '#^https?://(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?[.])*[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?::[0-9]{1,5})?(?:/|[?#]|$)#' %}
{% set desktop_url_valid = hero.image and not desktop_is_media_ref and hero.image matches '#^https?://(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?[.])*[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?::[0-9]{1,5})?(?:/|[?#]|$)#' %}
{% set has_desktop_image = desktop_media_url_valid or desktop_url_valid %}

{% set mobile_is_media_ref = hero.use_mobile_image and hero.image_mobile and hero.image_mobile starts with '@media-lib:' %}
{% set mobile_media = mobile_is_media_ref ? (hero.image_mobile | resolve_media) : null %}
{% set mobile_media_url_valid = mobile_media and mobile_media.type == 'image' and mobile_media.sourceUrl matches '#^https?://(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?[.])*[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?::[0-9]{1,5})?(?:/|[?#]|$)#' %}
{% set mobile_url_valid = hero.use_mobile_image and hero.image_mobile and not mobile_is_media_ref and hero.image_mobile matches '#^https?://(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?[.])*[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?::[0-9]{1,5})?(?:/|[?#]|$)#' %}
{% set has_mobile_image = mobile_media_url_valid or mobile_url_valid %}
{% set has_responsive_images = has_desktop_image and has_mobile_image %}
{% set show_placeholder = not has_desktop_image and not has_mobile_image %}
{% set image_alt = hero.image | media_alt | default('accessibility.hero' | t) %}
{% set image_mobile_alt = hero.image_mobile | media_alt | default('accessibility.hero' | t) %}

{# Height #}
{% set height = hero.height %}
{% set auto_height = hero.auto_height %}

{# Alignment #}
{% set horizontal_align = hero.alignment | default('center') %}
{% set vertical_align = hero.alignment_vertical | default('center') %}
{% set horizontal_align_class = horizontal_align == 'start' ? 'left' : (horizontal_align == 'end' ? 'right' : 'center') %}
{% set vertical_align_class = vertical_align %}

{% if vertical_align_class == 'center' and horizontal_align_class == 'center' %}
  {% set content_position_class = 'media-content-center' %}
{% else %}
  {% set content_position_class = 'media-content-' ~ vertical_align_class ~ '-' ~ horizontal_align_class %}
{% endif %}

{# Text color #}
{% set text_color = hero.text_color %}

{# Overlay #}
{% set show_overlay = hero.show_overlay %}
{% set overlay_color = hero.overlay_color | default('#000000') %}
{% set overlay_opacity = show_overlay ? ((hero.overlay_opacity | default(30)) / 100) : 0 %}

{# Spacing #}
{% set gap = hero.gap | default(16) %}
{% set vertical_padding = hero.vertical_padding | default(0) %}
{% set horizontal_padding = hero.horizontal_padding | default(0) %}
{% set content_animation = hero.content_animation | default('none') %}
{% set parallax = hero.parallax %}


<div class="hero section-full-width media {{ auto_height ? 'media-auto' : 'media-full-width' }} {% if parallax %}hero-parallax{% endif %}" style="{% if not auto_height %}min-height: {{ height }}vh; {% endif %}{% if show_overlay %}--media-overlay-color: {{ overlay_color }}; --media-overlay-opacity: {{ overlay_opacity }};{% endif %} {% if text_color %}color: {{ text_color }};{% endif %}">
  {% set is_priority_section = section.index <= (template in ['home', 'product'] ? 1 : 2) %}
  <div class="{% if parallax %}js-hero-parallax{% endif %} media-visual">
    {# A mobile art-directed image is emitted as one picture so the browser selects only one source. #}
    {% if has_responsive_images %}
      {% include 'snippets/image.tpl' with {
        image_src: hero.image,
        image_resolved_media: desktop_media_url_valid ? desktop_media : null,
        image_mobile_src: hero.image_mobile,
        image_mobile_resolved_media: mobile_media_url_valid ? mobile_media : null,
        image_mobile_media_query: '(max-width: 767.98px)',
        image_alt: image_alt,
        image_mobile_alt: image_mobile_alt,
        image_classes: not is_priority_section ? 'fade-in lazyload',
        image_priority_high: is_priority_section,
        image_lazy: not is_priority_section,
        image_lazy_js: false,
        image_sizes: '100vw',
        image_width: hero.image ? hero.image_width : 1280,
        image_height: hero.image ? hero.image_height : 700,
        image_mobile_width: hero.image_mobile_width,
        image_mobile_height: hero.image_mobile_height,
        image_aspect_ratio: hero.image ? (hero.image_width and hero.image_height) : true,
      } %}
      {% if not is_priority_section %}
        <div class="placeholder placeholder-fade"></div>
      {% endif %}
    {% elseif has_desktop_image %}
      {# Preserve the current single-image path when no mobile alternative is configured. #}
      {% set desktop_lazy = not is_priority_section %}
      {% include 'snippets/image.tpl' with {
        image_src: hero.image,
        image_resolved_media: desktop_media_url_valid ? desktop_media : null,
        image_alt: image_alt,
        image_classes: desktop_lazy ? 'fade-in',
        image_priority_high: is_priority_section,
        image_lazy_js: desktop_lazy,
        image_width: hero.image_width,
        image_height: hero.image_height,
        image_aspect_ratio: hero.image_width and hero.image_height,
      } %}
      {% if desktop_lazy %}
        <div class="placeholder placeholder-fade"></div>
      {% endif %}
    {% elseif has_mobile_image %}
      {# With no valid desktop image, reuse the mobile asset at every width. #}
      {% set mobile_lazy = not is_priority_section %}
      {% include 'snippets/image.tpl' with {
        image_src: hero.image_mobile,
        image_resolved_media: mobile_media_url_valid ? mobile_media : null,
        image_alt: image_mobile_alt,
        image_classes: mobile_lazy ? 'fade-in',
        image_priority_high: is_priority_section,
        image_lazy: mobile_lazy,
        image_lazy_js: false,
        image_thumbs: mobile_media_url_valid ? null : false,
        image_width: hero.image_mobile_width,
        image_height: hero.image_mobile_height,
        image_aspect_ratio: hero.image_mobile_width and hero.image_mobile_height,
      } %}
      {% if mobile_lazy %}
        <div class="placeholder placeholder-fade"></div>
      {% endif %}
    {% elseif show_placeholder %}
      {% include 'snippets/image.tpl' with {
        image_src: ('images/placeholders/hero/hero.webp') | static_url,
        image_alt: 'accessibility.hero' | t,
        image_classes: 'fade-in',
        image_lazy_js: true,
        image_thumbs: false,
        image_width: 1280,
        image_height: 700,
        image_aspect_ratio: true,
      } %}
      <div class="placeholder placeholder-fade"></div>
    {% endif %}

    {# Overlay #}
    {% if show_overlay %}
      <div class="media-overlay"></div>
    {% endif %}
  </div>

  {# Content #}
  <div class="media-content media-content-floating {{ content_position_class }} {% if hero.link %}media-content-linked{% endif %} {% if content_animation != 'none' %}media-content-animate media-content-animate-{{ content_animation }}{% endif %}" style="gap: {{ gap }}px; padding: {{ vertical_padding }}px {{ horizontal_padding }}px;">
    {% for block in section.blocks %}
      {% include 'blocks/' ~ block.type ~ '.tpl' with { block: block } %}
    {% endfor %}
  </div>

  {# Full section link #}
  {% if hero.link %}
    <a href="{{ hero.link }}" class="media-link" aria-label="{{ 't:names.hero' | t }}"></a>
  {% endif %}
</div>


{% schema %}
{
  "name": "t:names.hero",
  "add_section_order": 1,
  "class": "section section-hero",
  "blocks": [
    { "tags": ["general"] }
  ],
  "settings": [
    {
      "type": "setting",
      "setting_type": "image_picker",
      "id": "image",
      "label": "t:settings.image"
    },
    {
      "type": "setting",
      "setting_type": "toggle",
      "id": "use_mobile_image",
      "label": "t:settings.use_mobile_image",
      "default": false
    },
    {
      "type": "setting",
      "setting_type": "image_picker",
      "id": "image_mobile",
      "label": "t:settings.image_mobile",
      "visible_if": "{{ section.settings.use_mobile_image }}"
    },
    {
      "type": "setting",
      "setting_type": "url",
      "id": "link",
      "label": "t:settings.link"
    },
    {
      "type": "header",
      "content": "t:names.disposition"
    },
    {
      "type": "setting",
      "setting_type": "alignment",
      "id": "alignment",
      "label": "t:settings.alignment",
      "options": [
        { "value": "start", "label": "t:options.left" },
        { "value": "center", "label": "t:options.center" },
        { "value": "end", "label": "t:options.right" }
      ],
      "default": "center",
      "vertical_options": [
        { "value": "top", "label": "t:options.top" },
        { "value": "center", "label": "t:options.center" },
        { "value": "bottom", "label": "t:options.bottom" }
      ],
      "vertical_default": "center"
    },
    {
      "type": "header",
      "content": "t:names.design"
    },
    {
      "type": "setting",
      "setting_type": "range",
      "id": "height",
      "label": "t:settings.height",
      "min": 0,
      "max": 100,
      "step": 5,
      "unit": "%",
      "default": 100,
      "icon": "height",
      "disabled_if": "{{ section.settings.auto_height }}"
    },
    {
      "type": "setting",
      "setting_type": "checkbox",
      "id": "auto_height",
      "label": "t:settings.auto_height",
      "default": false
    },
    {
      "type": "setting",
      "setting_type": "range",
      "id": "gap",
      "label": "t:settings.gap",
      "min": 0,
      "max": 50,
      "step": 4,
      "unit": "px",
      "default": 16,
      "icon": "vertical_spacing"
    },
    {
      "type": "setting",
      "setting_type": "range",
      "id": "vertical_padding",
      "label": "t:settings.vertical_padding",
      "min": 0,
      "max": 120,
      "step": 4,
      "unit": "px",
      "default": 0,
      "icon": "vertical_padding"
    },
    {
      "type": "setting",
      "setting_type": "range",
      "id": "horizontal_padding",
      "label": "t:settings.horizontal_padding",
      "min": 0,
      "max": 120,
      "step": 4,
      "unit": "px",
      "default": 0,
      "icon": "horizontal_padding"
    },
    {
      "type": "header",
      "content": "t:names.colors"
    },
    {
      "type": "setting",
      "setting_type": "color",
      "id": "text_color",
      "label": "t:settings.text",
      "default_setting": "text_color"
    },
    {
      "type": "setting",
      "setting_type": "toggle",
      "id": "show_overlay",
      "label": "t:names.transparent_background",
      "default": false,
      "info": "t:settings.add_overlay",
      "header_toggle": true
    },
    {
      "type": "setting",
      "setting_type": "color",
      "id": "overlay_color",
      "label": "t:settings.color",
      "default": "#000000",
      "visible_if": "{{ section.settings.show_overlay }}"
    },
    {
      "type": "setting",
      "setting_type": "range",
      "id": "overlay_opacity",
      "label": "t:settings.overlay_opacity",
      "min": 0,
      "max": 100,
      "step": 5,
      "unit": "%",
      "default": 30,
      "visible_if": "{{ section.settings.show_overlay }}"
    },
    {
      "type": "header",
      "content": "t:names.animation"
    },
    {
      "type": "setting",
      "setting_type": "select",
      "id": "content_animation",
      "label": "t:settings.content_animation",
      "options": [
        { "value": "none", "label": "t:options.none" },
        { "value": "fade", "label": "t:options.fade" },
        { "value": "slide-up", "label": "t:options.slide_up" },
        { "value": "slide-down", "label": "t:options.slide_down" }
      ],
      "default": "none"
    },
    {
      "type": "setting",
      "setting_type": "toggle",
      "id": "parallax",
      "label": "t:settings.parallax",
      "default": false
    }
  ],
  "presets": [
    {
      "name": "t:names.hero",
      "category": "t:categories.media",
      "settings": {
        "gap": 16,
        "vertical_padding": 32,
        "horizontal_padding": 32
      },
      "blocks": [
        { "type": "heading", "settings": { "title": "t:defaults.hero.heading", "size": "h1" } },
        { "type": "text", "settings": { "text": "t:defaults.hero.description" } },
        { "type": "button", "settings": { "label": "t:defaults.hero.button" } }
      ]
    }
  ]
}
{% endschema %}
````

## Archivo candidato íntegro — snippets/image.tpl

- Ruta lógica: `snippets/image.tpl`
- Clasificación: código candidato
- SHA256 del origen: `e4e622e0c561c4450138e7717a1e5af95cf19d0184aee5cbcb89990f7ada767e`

````
{#
  Image
  Unified responsive image component. Single entry point: image_src.
  Supports product images, category images, post images, theme editor image_picker settings,
  @media-lib references (from image_picker or metafields), and external URLs.
  Renders as <picture> with AVIF/WebP when srcsets are available.

  Usage:
    image_src          - The image to display (image object, @media-lib ref, or URL).
                         Callers handling metafields must unwrap MetafieldItem.value before passing.
    product_image      - true if image_src is a product image object
    category_image     - true if image_src is a category image object
    post_image         - true if image_src is a post/blog image
    image_thumbs       - Array of thumb sizes for srcset, or false to disable srcset entirely
#}

{# Resolve image objects (product/category/post) into URLs, keeping the object for srcset generation #}
{% if (product_image or category_image or post_image) and image_src %}
	{% set image_name = image_src %}
	{% if product_image %}
		{% set image_src = image_src | product_image_url('large') %}
	{% elseif category_image %}
		{% set image_src = image_src | category_image_url('large') %}
	{% endif %}
{% endif %}

{# Resolve media library references (theme editor image_picker settings or product metafields) into image data with srcsets #}
{# Resolve editor media once in the section and pass the result when available. #}
{% set image_src_is_media_ref = image_src is defined and image_src and image_src starts with '@media-lib:' %}
{% set media = image_resolved_media is defined ? image_resolved_media : (image_src_is_media_ref ? (image_src | resolve_media) : null) %}
{% set image_media_url_valid = media and media.type == 'image' and media.sourceUrl matches '#^https?://(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?[.])*[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?::[0-9]{1,5})?(?:/|[?#]|$)#' %}
{% set image_raw_url_valid = image_src is defined and image_src and not image_src_is_media_ref and image_src matches '#^https?://(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?[.])*[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?::[0-9]{1,5})?(?:/|[?#]|$)#' %}
{% set image_art_direction_requested = image_mobile_src is defined and image_mobile_src %}
{% set image_desktop_url_valid = image_media_url_valid or (image_art_direction_requested and image_raw_url_valid) %}
{% set image_source_invalid = image_src_is_media_ref and not image_media_url_valid %}

{# The mobile input is accepted only as a resolved image or an absolute HTTP(S) URL. #}
{% set mobile_src_is_media_ref = image_mobile_src is defined and image_mobile_src and image_mobile_src starts with '@media-lib:' %}
{% set mobile_media = image_mobile_resolved_media is defined ? image_mobile_resolved_media : (mobile_src_is_media_ref ? (image_mobile_src | resolve_media) : null) %}
{% set mobile_media_url_valid = mobile_media and mobile_media.type == 'image' and mobile_media.sourceUrl matches '#^https?://(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?[.])*[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?::[0-9]{1,5})?(?:/|[?#]|$)#' %}
{% set mobile_raw_url_valid = image_mobile_src is defined and image_mobile_src and not mobile_src_is_media_ref and image_mobile_src matches '#^https?://(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?[.])*[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?::[0-9]{1,5})?(?:/|[?#]|$)#' %}
{% set mobile_source_url_valid = mobile_media_url_valid or mobile_raw_url_valid %}
{% set image_mobile_src = mobile_media_url_valid ? mobile_media.sourceUrl : (mobile_raw_url_valid ? image_mobile_src : null) %}
{% if mobile_media_url_valid %}
	{% if not image_mobile_width %}{% set image_mobile_width = mobile_media.sourceWidth %}{% endif %}
	{% if not image_mobile_height %}{% set image_mobile_height = mobile_media.sourceHeight %}{% endif %}
	{% if not image_mobile_alt and mobile_media.altText %}{% set image_mobile_alt = mobile_media.altText %}{% endif %}
{% endif %}

{# If desktop is unavailable, use the valid mobile image alone at every width. #}
{% if image_art_direction_requested and not image_desktop_url_valid and mobile_source_url_valid %}
	{% set image_src = image_mobile_src %}
	{% set media = mobile_media_url_valid ? mobile_media : null %}
	{% set image_width = image_mobile_width %}
	{% set image_height = image_mobile_height %}
	{% set image_alt = image_mobile_alt is defined and image_mobile_alt ? image_mobile_alt : image_alt %}
	{% set image_thumbs = mobile_media_url_valid ? image_thumbs : false %}
	{% set image_source_invalid = false %}
	{% set image_mobile_src = null %}
{% elseif image_art_direction_requested and not image_desktop_url_valid %}
	{% set image_src = null %}
	{% set media = null %}
	{% set image_source_invalid = true %}
{% elseif image_media_url_valid %}
	{% set image_src = media.sourceUrl %}
{% elseif image_source_invalid %}
	{% set image_src = null %}
{% endif %}

{% set has_art_direction = image_art_direction_requested and image_desktop_url_valid and mobile_source_url_valid %}

{% if media %}
	{% set image_src = media.sourceUrl %}
	{% if not image_width and not image_height %}
		{% set image_width = media.sourceWidth %}
		{% set image_height = media.sourceHeight %}
	{% endif %}
	{% if not image_alt and media.altText %}
		{% set image_alt = media.altText %}
	{% endif %}
{% endif %}
{% set has_media_library_srcsets = media and media.srcSets | length > 0 %}

{% set image_thumbs =
	image_thumbs is same as(false) ? false :
	image_thumbs ? image_thumbs :
	product_image ? ['tiny', 'thumb', 'small', 'medium', 'large', 'huge', 'original', '1080p', '1440p', '4k'] :
	category_image ? ['tiny', 'thumb', 'small', 'medium', 'large', 'huge', 'original', '1080p'] :
	['tiny', 'thumb', 'small', 'medium', 'large', 'huge', 'original', 'xlarge', '1080p']
%}

{% set sizes = {
	'tiny': 50,
	'thumb': 100,
	'small': 240,
	'medium': 320,
	'large': 480,
	'huge': 640,
	'original': 1024,
	'xlarge': 1400,
	'1080p': 1920,
	'1440p': 2560,
	'4k': 3840
} %}

{% set default_image_url =
	post_image ? image_name :
	product_image ? image_name | product_image_url('large') :
	category_image ? image_name | category_image_url('large') :
	image_src
%}

{% set src = image_src ? image_src : (image_priority_high ? default_image_url : 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==') %}
{% set srcset = '' %}
{% set image_lazy = image_lazy == 'false' ? false : true %}

{# srcset for non-media-library images (products, categories, blog posts, store logo) #}
{% if image_thumbs is not same as(false) and not media %}
	{% for thumb, size in sizes %}
		{% if thumb in image_thumbs %}
			{% set image_url =
				logo_image ? store.logo(thumb) :
				post_image ? image_name :
				product_image ? image_name | product_image_url(thumb) :
				category_image ? image_name | category_image_url(thumb) :
				image_src
			%}
			{% set srcset = srcset ~ (srcset ? ', ' : '') ~ image_url ~ ' ' ~ size ~ 'w' %}
		{% endif %}
	{% endfor %}
{% endif %}

{% set image_lazy = image_lazy and not image_priority_high %}
{% set image_lazy_js = image_lazy_js and not image_priority_high %}

{# Shared <img> attributes used by both branches #}
{% set img_attrs %}
	{% if image_priority_high %}
		fetchpriority="high"
	{% endif %}
	{% if image_width and not has_art_direction %}
		width="{{ image_width }}"
	{% endif %}
	{% if image_height and not has_art_direction %}
		height="{{ image_height }}"
	{% endif %}
	{% if image_lazy and not image_lazy_js %}
		loading="lazy"
	{% endif %}
	{% if image_classes or image_lazy_js %}
		class="{% if image_swiper_lazy_class %}swiper-lazy{% elseif image_lazy_js %}lazyload{% endif %}{% if image_priority_high %} image-priority-high{% endif %} {{ image_classes }}"
	{% endif %}
	{% if image_sizes %}
		sizes="{{ image_sizes }}"
	{% endif %}
	{% if image_data_expand %}
		data-expand="{{ image_data_expand }}"
	{% endif %}
	{% if image_data_sizes %}
		data-sizes="{{ image_data_sizes }}"
	{% endif %}
	{% if image_data_attributes %}
		{% for attr, value in image_data_attributes %}data-{{ attr }}="{{ value }}" {% endfor %}
	{% endif %}
	alt="{{ image_alt }}"
{% endset %}

{# Build original-format srcset from theme editor image_picker srcsets so both paths share one <img> #}
{% if has_media_library_srcsets %}
	{% for srcSet in media.srcSets if srcSet.format == 'original' %}
		{% for size in srcSet.sizes %}
			{% set srcset = srcset ~ (srcset ? ', ') ~ srcSet.baseUrl ~ size.w ~ '.' ~ media.extension ~ ' ' ~ size.w ~ 'w' %}
		{% endfor %}
	{% endfor %}
	{% set image_aspect_ratio = true %}
{% endif %}

{# Preserve Tiendanube's original responsive widths for the mobile art-direction fallback. #}
{% set mobile_original_srcset = '' %}
{% if has_art_direction and mobile_media_url_valid %}
	{% for srcSet in mobile_media.srcSets if srcSet.format == 'original' %}
		{% for size in srcSet.sizes %}
			{% set mobile_original_srcset = mobile_original_srcset ~ (mobile_original_srcset ? ', ' : '') ~ srcSet.baseUrl ~ size.w ~ '.' ~ mobile_media.extension ~ ' ' ~ size.w ~ 'w' %}
		{% endfor %}
	{% endfor %}
{% endif %}

{# Resolve data-src fallback for non-media images #}
{% set data_src = image_src ? image_src : default_image_url %}

{# @media-lib references with processed thumbnails get <picture> with AVIF/WebP <source> elements.
   Everything else (products, categories, blog, or images still processing) uses a plain <img>.
   Bail when a @media-lib ref resolves to non-image media (e.g. video or orphan uuid from a metafield). #}
{% if (not media or media.type == 'image') and not image_source_invalid %}
	{% if has_art_direction %}
		<picture>
			{# Sources are ordered mobile-first and only the matching media source is eligible. #}
			{% if mobile_media and mobile_media.type == 'image' %}
				{% for srcSet in mobile_media.srcSets if srcSet.format != 'original' %}
					{% set mobile_source_srcset = '' %}
					{% for size in srcSet.sizes %}
						{% set mobile_source_srcset = mobile_source_srcset ~ (mobile_source_srcset ? ', ' : '') ~ srcSet.baseUrl ~ size.w ~ '.' ~ srcSet.format ~ ' ' ~ size.w ~ 'w' %}
					{% endfor %}
					<source
						media="{{ image_mobile_media_query | default('(max-width: 767.98px)') }}"
						type="image/{{ srcSet.format }}"
						{% if image_lazy_js %}data-{% endif %}srcset="{{ mobile_source_srcset }}"
						{% if image_sizes %}sizes="{{ image_sizes }}"{% endif %}
						{% if image_mobile_width %}width="{{ image_mobile_width }}"{% endif %}
						{% if image_mobile_height %}height="{{ image_mobile_height }}"{% endif %}
					/>
				{% endfor %}
				<source
					media="{{ image_mobile_media_query | default('(max-width: 767.98px)') }}"
					{% if image_lazy_js %}data-{% endif %}srcset="{{ mobile_original_srcset ? mobile_original_srcset : image_mobile_src }}"
					{% if image_sizes %}sizes="{{ image_sizes }}"{% endif %}
					{% if image_mobile_width %}width="{{ image_mobile_width }}"{% endif %}
					{% if image_mobile_height %}height="{{ image_mobile_height }}"{% endif %}
				/>
			{% else %}
				<source
					media="{{ image_mobile_media_query | default('(max-width: 767.98px)') }}"
					{% if image_lazy_js %}data-{% endif %}srcset="{{ image_mobile_src }}"
					{% if image_sizes %}sizes="{{ image_sizes }}"{% endif %}
					{% if image_mobile_width %}width="{{ image_mobile_width }}"{% endif %}
					{% if image_mobile_height %}height="{{ image_mobile_height }}"{% endif %}
				/>
			{% endif %}
			{% if has_media_library_srcsets %}
				{% for srcSet in media.srcSets if srcSet.format != 'original' %}
					{% set source_srcset = '' %}
					{% for size in srcSet.sizes %}
						{% set source_srcset = source_srcset ~ (source_srcset ? ', ' : '') ~ srcSet.baseUrl ~ size.w ~ '.' ~ srcSet.format ~ ' ' ~ size.w ~ 'w' %}
					{% endfor %}
					<source
						type="image/{{ srcSet.format }}"
						{% if image_lazy_js %}data-{% endif %}srcset="{{ source_srcset }}"
						{% if image_sizes %}sizes="{{ image_sizes }}"{% endif %}
						{% if image_width %}width="{{ image_width }}"{% endif %}
						{% if image_height %}height="{{ image_height }}"{% endif %}
					/>
				{% endfor %}
			{% endif %}
			<source
				{% if image_lazy_js %}data-{% endif %}srcset="{{ media and srcset ? srcset : image_src }}"
				{% if image_sizes %}sizes="{{ image_sizes }}"{% endif %}
				{% if image_width %}width="{{ image_width }}"{% endif %}
				{% if image_height %}height="{{ image_height }}"{% endif %}
			/>
			<img
				{{ img_attrs }}
				{% if image_lazy_js %}
					{% if image_width and image_height %}src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="{% endif %}
					{% if srcset %}data-srcset="{{ srcset }}"{% else %}data-src="{{ data_src }}"{% endif %}
				{% else %}
					src="{{ src }}"
					{% if srcset %}srcset="{{ srcset }}"{% endif %}
				{% endif %}
				{% if image_aspect_ratio and image_width and image_height and not has_art_direction %}
					style="aspect-ratio: {{ image_width }} / {{ image_height }}"
				{% endif %}
			/>
		</picture>
	{% else %}
	{% if has_media_library_srcsets %}
		<picture>
			{% for srcSet in media.srcSets if srcSet.format != 'original' %}
				{% set source_srcset = '' %}
				{% for size in srcSet.sizes %}
					{% set source_srcset = source_srcset ~ (source_srcset ? ', ') ~ srcSet.baseUrl ~ size.w ~ '.' ~ srcSet.format ~ ' ' ~ size.w ~ 'w' %}
				{% endfor %}
				<source
					type="image/{{ srcSet.format }}"
					{% if image_lazy_js %}data-{% endif %}srcset="{{ source_srcset }}"
					{% if image_sizes %}sizes="{{ image_sizes }}"{% endif %}
					{% if image_data_sizes %}data-sizes="{{ image_data_sizes }}"{% endif %}
				/>
			{% endfor %}
	{% endif %}

		<img
			{{ img_attrs }}
			{% if image_lazy_js %}
				{% if image_width and image_height %}src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="{% endif %}
				{% if srcset %}
					data-srcset="{{ srcset }}"
				{% else %}
					data-src="{{ data_src }}"
				{% endif %}
			{% else %}
				src="{{ src }}"
				{% if srcset %}srcset="{{ srcset }}"{% endif %}
			{% endif %}
			{% if image_aspect_ratio and image_width and image_height %}
				style="aspect-ratio: {{ image_width }} / {{ image_height }}"
			{% endif %}
		/>

	{% if has_media_library_srcsets %}
		</picture>
	{% endif %}
	{% endif %}
{% endif %}
````

## Contexto íntegro — blocks/slide.tpl

- Ruta lógica: `blocks/slide.tpl`
- Clasificación: dependencia de lectura; no es candidata ni escribible
- SHA256 del origen: `ab5e8d97095b36101fe5d4b66b7facbcdfdd87ab03458da5d909b00f9c868a64`

````
{# Slide Block - Private to slideshow section #}

{% set slide = block.settings %}
{% set sectionfy_video = slide.media_type == 'sectionfy_video' %}
{% set has_link = slide.link %}

{# Images #}
{% set has_mobile_image = slide.use_mobile_image and slide.image_mobile %}
{% set has_responsive_images = slide.image and has_mobile_image %}

{# Alignment #}
{% set horizontal_align = slide.alignment | default('center') %}
{% set vertical_align = slide.alignment_vertical | default('center') %}
{% set horizontal_align_class = horizontal_align == 'start' ? 'left' : (horizontal_align == 'end' ? 'right' : 'center') %}
{% set vertical_align_class = vertical_align %}

{% if vertical_align_class == 'center' and horizontal_align_class == 'center' %}
  {% set content_position_class = 'media-content-center' %}
{% else %}
  {% set content_position_class = 'media-content-' ~ vertical_align_class ~ '-' ~ horizontal_align_class %}
{% endif %}

{# Text color #}
{% set text_color = slide.text_color %}

{# Overlay #}
{% set show_overlay = slide.show_overlay %}
{% set overlay_color = slide.overlay_color | default('#000000') %}
{% set overlay_opacity = show_overlay ? ((slide.overlay_opacity | default(30)) / 100) : 0 %}

{# Spacing #}
{% set slide_gap = slide.gap | default(16) %}
{% set slide_vertical_padding = slide.vertical_padding | default(32) %}
{% set slide_horizontal_padding = slide.horizontal_padding | default(32) %}

{% set has_image = slide.image or has_mobile_image %}
{% set show_placeholder = not has_image %}
{% set content_animation = slide_content_animation | default('none') %}

{% set image_alt = slide.image | media_alt | default('accessibility.slide' | t) %}
{% set image_mobile_alt = slide.image_mobile | media_alt | default('accessibility.slide' | t) %}

<div
  class="swiper-slide media {% if slide_auto_height %}media-auto{% endif %}"
  {{ block | block_attributes }}
  data-store="slide-{{ block.id }}"
  {% if sectionfy_video %}
    data-sectionfy-kind="video_banner" {% if template == 'home' %}data-sectionfy-page="home-page"{% endif %}
    data-sectionfy-video-slide
    data-sectionfy-video-endpoint="{{ section.settings.sectionfy_video_endpoint | default('') | escape }}"
    data-sectionfy-video-key="{{ slide.sectionfy_video_key | default('') | escape }}"
    data-sectionfy-token="{{ settings.sectionfy_token | default('') | escape }}"
    data-sectionfy-video-autoplay="{{ slide.sectionfy_video_autoplay ? 'true' : 'false' }}"
  {% endif %}
  style="{{ slide_height_style | default('') }} {% if show_overlay %}--media-overlay-color: {{ overlay_color }}; --media-overlay-opacity: {{ overlay_opacity }};{% endif %} {% if text_color %}color: {{ text_color }};{% endif %}"
>
  <div class="media-visual">
      {# Desktop image: always lazy when mobile variant exists, otherwise follows priority #}
      {% if slide.image %}
        {% set desktop_lazy = has_responsive_images or not is_priority %}
        {% include 'snippets/image.tpl' with {
          image_src: slide.image,
          image_alt: image_alt,
          image_classes: (has_responsive_images ? 'd-none d-md-block ') ~ (desktop_lazy ? 'fade-in'),
          image_priority_high: not has_responsive_images and is_priority,
          image_lazy_js: desktop_lazy,
          image_swiper_lazy_class: desktop_lazy,
          image_width: slide.image_width,
          image_height: slide.image_height,
          image_aspect_ratio: slide.image_width and slide.image_height,
        } %}
        {% if desktop_lazy %}
          <div class="placeholder placeholder-fade {{ has_responsive_images ? 'd-none d-md-block' }}"></div>
        {% endif %}
      {% elseif show_placeholder %}
        {# Fallback placeholder only when no image is configured at all. Cycles slide-1/2/3.jpg by position. #}
        {% set placeholder_num = ((slide_index | default(0)) % 3) + 1 %}
        {% set desktop_lazy = not is_priority %}
        {% include 'snippets/image.tpl' with {
          image_src: ('images/placeholders/carrousel/slide-' ~ placeholder_num ~ '.webp') | static_url,
          image_alt: 'accessibility.slide' | t,
          image_classes: desktop_lazy ? 'fade-in',
          image_priority_high: is_priority,
          image_lazy_js: desktop_lazy,
          image_swiper_lazy_class: desktop_lazy,
          image_thumbs: false,
          image_width: 1280,
          image_height: 700,
          image_aspect_ratio: true,
        } %}
        {% if desktop_lazy %}
          <div class="placeholder placeholder-fade"></div>
        {% endif %}
      {% endif %}

      {# Mobile image: prioritized for LCP on first slide of first section #}
      {% if has_mobile_image %}
        {% include 'snippets/image.tpl' with {
          image_src: slide.image_mobile,
          image_alt: image_mobile_alt,
          image_classes: (has_responsive_images ? 'd-md-none ') ~ (not is_priority ? 'fade-in'),
          image_priority_high: is_priority,
          image_lazy_js: not is_priority,
          image_swiper_lazy_class: not is_priority,
          image_width: slide.image_mobile_width,
          image_height: slide.image_mobile_height,
          image_aspect_ratio: slide.image_mobile_width and slide.image_mobile_height,
        } %}
        {% if not is_priority %}
          <div class="placeholder placeholder-fade {{ has_responsive_images ? 'd-md-none' }}"></div>
        {% endif %}
      {% endif %}

      {# Overlay #}
      {% if show_overlay %}
        <div class="media-overlay"></div>
      {% endif %}
    </div>

      {# Controls are a slide sibling of the link, outside the visual stacking context. #}
      {% if sectionfy_video %}
        <button type="button" class="sectionfy-video-toggle" data-sectionfy-video-toggle
          data-label-play="Reproducir video" data-label-pause="Pausar video"
          aria-label="Reproducir video" hidden>
          <svg data-sectionfy-video-play width="20" height="20" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M8 5v14l11-7z"/></svg>
          <svg data-sectionfy-video-pause width="20" height="20" viewBox="0 0 24 24" aria-hidden="true" focusable="false" hidden><path fill="currentColor" d="M6 4h4v16H6zm8 0h4v16h-4z"/></svg>
        </button>
      {% endif %}

  {# Slide link #}
  {% if has_link %}
    <a href="{{ slide.link }}" class="media-link" aria-label="{{ 't:names.slide' | t }}"></a>
  {% endif %}

  {# Content #}
  {% if block.blocks | length > 0 %}
    {% set no_image_align = horizontal_align == 'center' ? 'center' : (horizontal_align == 'end' ? 'end' : 'start') %}
    {% set no_image_classes = 'd-flex flex-column align-items-' ~ no_image_align ~ ' text-' ~ horizontal_align_class %}
    <div class="{% if has_image or show_placeholder %}media-content media-content-floating {{ content_position_class }}{% else %}{{ no_image_classes }}{% endif %} {% if has_link %}media-content-linked{% endif %} {% if content_animation != 'none' %}media-content-animate media-content-animate-{{ content_animation }}{% endif %}" style="gap: {{ slide_gap }}px; padding: {{ slide_vertical_padding }}px {{ slide_horizontal_padding }}px;">
      {% for child_block in block.blocks %}
        {% if child_block and child_block.type is defined and child_block.type != 'trust-benefit' %}
          {% include 'blocks/' ~ child_block.type ~ '.tpl' with { block: child_block } %}
        {% endif %}
      {% endfor %}
    </div>
  {% endif %}

  {# Trust Benefits Pill Overlay inside slide (Figma Glassmorphism Style) #}
  {% set slide_trust_blocks = [] %}
  {% if block.blocks | length > 0 %}
    {% for cb in block.blocks %}
      {% if cb.type == 'trust-benefit' %}
        {% set slide_trust_blocks = slide_trust_blocks | merge([cb]) %}
      {% endif %}
    {% endfor %}
  {% endif %}
  {% if slide_trust_blocks | length == 0 and section.blocks is defined %}
    {% for sb in section.blocks %}
      {% if sb.type == 'trust-benefit' %}
        {% set slide_trust_blocks = slide_trust_blocks | merge([sb]) %}
      {% endif %}
    {% endfor %}
  {% endif %}

  {% if (section.settings.show_trust_pill is not defined or section.settings.show_trust_pill) and slide_trust_blocks | length > 0 %}
    {% set use_slide_custom_colors = slide.use_custom_trust_colors %}
    {% set pill_bg = use_slide_custom_colors and slide.trust_pill_bg_color ? slide.trust_pill_bg_color : (section.settings.trust_pill_bg_color | default('#ffffff')) %}
    {% set pill_opacity = (use_slide_custom_colors and slide.trust_pill_bg_opacity is defined ? slide.trust_pill_bg_opacity : (section.settings.trust_pill_bg_opacity | default(15))) / 100 %}
    {% set pill_text = use_slide_custom_colors and slide.trust_pill_text_color ? slide.trust_pill_text_color : (section.settings.trust_pill_text_color | default('#ffffff')) %}
    {% set pill_align = section.settings.trust_pill_alignment | default('center') %}
    {% set pill_valign = section.settings.trust_pill_vertical_alignment | default('bottom') %}

    <div class="slider-trust-pill-wrapper slider-trust-align-{{ pill_align }} slider-trust-valign-{{ pill_valign }}" style="--trust-pill-spacing-top: {{ section.settings.trust_pill_spacing_top | default(25) }}px; --trust-pill-spacing-bottom: {{ section.settings.trust_pill_spacing_bottom | default(25) }}px; --trust-pill-spacing-left: {{ section.settings.trust_pill_spacing_left | default(0) }}px; --trust-pill-spacing-right: {{ section.settings.trust_pill_spacing_right | default(0) }}px; --trust-pill-spacing-left-mobile: {{ section.settings.trust_pill_spacing_left_mobile | default(0) }}px; --trust-pill-spacing-right-mobile: {{ section.settings.trust_pill_spacing_right_mobile | default(0) }}px;">
      <div class="{% if section.settings.trust_pill_width | default('page') == 'full' %}slider-trust-pill-full{% else %}container{% endif %}">
        <div class="slider-trust-pill slider-trust-pill-mobile-rotate" style="--trust-bg-hex: {{ pill_bg }}; --trust-bg-opacity: {{ pill_opacity }}; --trust-text-color: {{ pill_text }}; --trust-pill-scale: {{ (section.settings.trust_pill_scale | default(100)) / 100 }}; --trust-pill-scale-mobile: {{ (section.settings.trust_pill_scale_mobile | default(100)) / 100 }};">
          {% for trust_block in slide_trust_blocks %}
            {% include 'blocks/trust-benefit.tpl' with { block: trust_block, trust_index: loop.index } %}
          {% endfor %}
        </div>
      </div>
    </div>
  {% endif %}
</div>

{% schema %}
{
  "name": "t:names.slide",
  "icon": "pictureIcon",
  "blocks": [
    {
      "tags": [
        "general"
      ]
    },
    {
      "type": "trust-benefit"
    }
  ],
  "settings": [
    {
      "type": "setting",
      "setting_type": "select",
      "id": "media_type",
      "label": "Contenido multimedia",
      "options": [
        {
          "value": "image",
          "label": "Foto de Tiendanube"
        },
        {
          "value": "sectionfy_video",
          "label": "Video de Sectionfy con foto de respaldo"
        }
      ],
      "default": "image"
    },
    {
      "type": "setting",
      "setting_type": "text",
      "id": "sectionfy_video_key",
      "label": "Clave de la sección de video en Sectionfy",
      "info": "Opcional si la consulta devuelve un único banner publicado. Si devuelve varios, indica su clave completa.",
      "visible_if": "{{ block.settings.media_type == 'sectionfy_video' }}"
    },
    {
      "type": "setting",
      "setting_type": "toggle",
      "id": "sectionfy_video_autoplay",
      "label": "Reproducción automática del video en escritorio",
      "default": false,
      "info": "En teléfono requiere pulsar Play. Respeta ahorro de datos y movimiento reducido.",
      "visible_if": "{{ block.settings.media_type == 'sectionfy_video' }}"
    },
    {
      "type": "setting",
      "setting_type": "image_picker",
      "id": "image",
      "label": "t:settings.image"
    },
    {
      "type": "setting",
      "setting_type": "toggle",
      "id": "use_mobile_image",
      "label": "t:settings.use_mobile_image",
      "default": false
    },
    {
      "type": "setting",
      "setting_type": "image_picker",
      "id": "image_mobile",
      "label": "t:settings.image_mobile",
      "visible_if": "{{ block.settings.use_mobile_image }}"
    },
    {
      "type": "setting",
      "setting_type": "url",
      "id": "link",
      "label": "t:settings.link"
    },
    {
      "type": "header",
      "content": "t:names.disposition"
    },
    {
      "type": "setting",
      "setting_type": "alignment",
      "id": "alignment",
      "label": "t:settings.alignment",
      "options": [
        {
          "value": "start",
          "label": "t:options.left"
        },
        {
          "value": "center",
          "label": "t:options.center"
        },
        {
          "value": "end",
          "label": "t:options.right"
        }
      ],
      "default": "center",
      "vertical_options": [
        {
          "value": "top",
          "label": "t:options.top"
        },
        {
          "value": "center",
          "label": "t:options.center"
        },
        {
          "value": "bottom",
          "label": "t:options.bottom"
        }
      ],
      "vertical_default": "center"
    },
    {
      "type": "header",
      "content": "t:names.colors"
    },
    {
      "type": "setting",
      "setting_type": "color",
      "id": "text_color",
      "label": "t:settings.text",
      "default_setting": "text_color"
    },
    {
      "type": "setting",
      "setting_type": "toggle",
      "id": "use_custom_trust_colors",
      "label": "t:settings.use_custom_trust_colors",
      "default": false
    },
    {
      "type": "setting",
      "setting_type": "color",
      "id": "trust_pill_bg_color",
      "label": "t:settings.trust_pill_bg_color",
      "default": "#ffffff",
      "visible_if": "{{ block.settings.use_custom_trust_colors }}"
    },
    {
      "type": "setting",
      "setting_type": "range",
      "id": "trust_pill_bg_opacity",
      "label": "t:settings.trust_pill_bg_opacity",
      "min": 0,
      "max": 100,
      "step": 5,
      "unit": "%",
      "default": 15,
      "visible_if": "{{ block.settings.use_custom_trust_colors }}"
    },
    {
      "type": "setting",
      "setting_type": "color",
      "id": "trust_pill_text_color",
      "label": "t:settings.trust_pill_text_color",
      "default": "#ffffff",
      "visible_if": "{{ block.settings.use_custom_trust_colors }}"
    },
    {
      "type": "header",
      "content": "t:names.design"
    },
    {
      "type": "setting",
      "setting_type": "range",
      "id": "gap",
      "label": "t:settings.gap",
      "min": 0,
      "max": 50,
      "step": 4,
      "unit": "px",
      "default": 16,
      "icon": "vertical_spacing"
    },
    {
      "type": "setting",
      "setting_type": "range",
      "id": "vertical_padding",
      "label": "t:settings.vertical_padding",
      "min": 0,
      "max": 120,
      "step": 4,
      "unit": "px",
      "default": 32,
      "icon": "vertical_padding"
    },
    {
      "type": "setting",
      "setting_type": "range",
      "id": "horizontal_padding",
      "label": "t:settings.horizontal_padding",
      "min": 0,
      "max": 120,
      "step": 4,
      "unit": "px",
      "default": 32,
      "icon": "horizontal_padding"
    },
    {
      "type": "setting",
      "setting_type": "toggle",
      "id": "show_overlay",
      "label": "t:names.transparent_background",
      "default": false,
      "info": "t:settings.add_overlay",
      "header_toggle": true
    },
    {
      "type": "setting",
      "setting_type": "color",
      "id": "overlay_color",
      "label": "t:settings.color",
      "default": "#000000",
      "visible_if": "{{ block.settings.show_overlay }}"
    },
    {
      "type": "setting",
      "setting_type": "range",
      "id": "overlay_opacity",
      "label": "t:settings.overlay_opacity",
      "min": 0,
      "max": 100,
      "step": 5,
      "unit": "%",
      "default": 30,
      "visible_if": "{{ block.settings.show_overlay }}"
    }
  ],
  "presets": [
    {
      "name": "t:names.slide",
      "settings": {
        "gap": 16,
        "vertical_padding": 32,
        "horizontal_padding": 32
      },
      "blocks": [
        {
          "type": "heading",
          "settings": {
            "title": "t:defaults.slide.heading",
            "size": "h1"
          }
        },
        {
          "type": "text",
          "settings": {
            "text": "t:defaults.slide.description"
          }
        },
        {
          "type": "button",
          "settings": {
            "label": "t:defaults.slide.button"
          }
        }
      ]
    }
  ]
}
{% endschema %}
````

## Contexto íntegro — blocks/banner.tpl

- Ruta lógica: `blocks/banner.tpl`
- Clasificación: dependencia de lectura; no es candidata ni escribible
- SHA256 del origen: `61bcb60817456a10177723b8a148b9027f130804b3245f1e5698d087d9de906c`

````
{# Banner Block - Private to banners section #}

{% set banner = block.settings %}
{% set has_link = banner.link %}

{# Layout #}
{% set text_outside = banner.text_outside %}
{% set text_over_image = not text_outside %}

{# Alignment → position classes for overlay mode #}
{% set horizontal_align = banner.alignment | default('start') %}
{% set vertical_align = banner.alignment_vertical | default('bottom') %}
{% set horizontal_align_class = horizontal_align == 'start' ? 'left' : (horizontal_align == 'end' ? 'right' : 'center') %}
{% set vertical_align_class = vertical_align %}

{% if vertical_align_class == 'center' and horizontal_align_class == 'center' %}
	{% set content_position_class = 'media-content-center' %}
{% else %}
	{% set content_position_class = 'media-content-' ~ vertical_align_class ~ '-' ~ horizontal_align_class %}
{% endif %}

{# Text alignment class for text-outside mode #}
{% set text_alignment_class = 'media-content-align-' ~ horizontal_align_class %}

{# Text color #}
{% set text_color = banner.text_color %}

{# Overlay #}
{% set show_overlay = banner.show_overlay %}
{% set overlay_color = banner.overlay_color | default('#000000') %}
{% set overlay_opacity = show_overlay ? ((banner.overlay_opacity | default(30)) / 100) : 0 %}

{# Block-level spacing #}
{% set block_gap = banner.gap | default(16) %}
{% set block_vertical_padding = banner.vertical_padding | default(32) %}
{% set block_horizontal_padding = banner.horizontal_padding | default(32) %}

{# Aspect ratio: forces a fixed crop on the banner image unless 'original' #}
{% set is_forced_aspect = (banner_aspect_ratio | default('original')) != 'original' %}
{% set aspect_padding = banner_aspect_ratio == 'custom' ? (banner_aspect_ratio_height | default(100)) : null %}
{% set aspect_ratio_mobile = banner_aspect_ratio_mobile is not null ? banner_aspect_ratio_mobile : banner_aspect_ratio %}
{% set is_forced_aspect_mobile = aspect_ratio_mobile != 'original' %}
{% set aspect_padding_mobile = aspect_ratio_mobile == 'custom' ? ((banner_aspect_ratio_mobile is not null ? banner_aspect_ratio_mobile_height : banner_aspect_ratio_height) | default(100)) : null %}

{% set mobile_differs = aspect_ratio_mobile != banner_aspect_ratio or aspect_padding_mobile != aspect_padding %}

{# Build crop classes independently for mobile and desktop #}
{% set crop_class = is_forced_aspect_mobile ? 'banner-image-container-cropped banner-image-container-cropped-' ~ aspect_ratio_mobile : '' %}
{% if is_forced_aspect and mobile_differs %}
	{% set crop_class = crop_class ~ ' banner-image-container-cropped-md banner-image-container-cropped-md-' ~ banner_aspect_ratio %}
{% elseif is_forced_aspect_mobile and not is_forced_aspect %}
	{% set crop_class = crop_class ~ ' banner-image-container-original-md' %}
{% endif %}

{# CSS variables for 'custom' ratios: predefined ratios (square/horizontal/vertical) use hardcoded class values,
   but 'custom' needs the user-defined percentage passed as a variable read by the CSS class #}
{% set aspect_style = is_forced_aspect_mobile and aspect_ratio_mobile == 'custom' ? '--aspect-padding: ' ~ aspect_padding_mobile ~ '%;' : '' %}
{% if is_forced_aspect and mobile_differs and banner_aspect_ratio == 'custom' %}
	{% set aspect_style = aspect_style ~ '--aspect-padding-md: ' ~ aspect_padding ~ '%;' %}
{% endif %}

{# Base class: media when text overlays image #}
{% set base_class = text_over_image and not is_forced_aspect ? 'media media-auto' %}

{% set has_image = banner.image or banner.image_mobile %}
{% set show_placeholder = not has_image %}

{% set has_responsive_images = banner.image and banner.image_mobile %}
{% set image_alt = banner.image | media_alt | default('accessibility.banner' | t) %}
{% set image_mobile_alt = banner.image_mobile | media_alt | default('accessibility.banner' | t) %}

<div 
	class="{{ base_class }} banner-block position-relative"
	{{ block | block_attributes }}
	data-store="banner-{{ block.id }}"
	style="{% if show_overlay %}--media-overlay-color: {{ overlay_color }}; --media-overlay-opacity: {{ overlay_opacity }};{% endif %} --banner-gap: {{ block_gap }}px; --banner-vpadding: {{ block_vertical_padding }}px; --banner-hpadding: {{ block_horizontal_padding }}px; {% if text_color %}color: {{ text_color }};{% endif %}"
>
	{# Background Image #}
	<div class="{% if text_over_image %}media-visual{% endif %} banner-image-container {{ crop_class }}" {% if aspect_style %}style="{{ aspect_style }}"{% endif %}>
		{# Desktop image: always lazy when mobile variant exists, otherwise follows priority #}
		{% if banner.image %}
			{% set desktop_lazy = has_responsive_images or not is_priority %}
			{% include 'snippets/image.tpl' with {
				image_src: banner.image,
				image_alt: image_alt,
				image_classes: (has_responsive_images ? 'd-none d-md-block ') ~ 'img-fluid' ~ (desktop_lazy ? ' fade-in'),
				image_priority_high: not has_responsive_images and is_priority,
				image_lazy_js: desktop_lazy,
				image_width: banner.image_width,
				image_height: banner.image_height,
				image_aspect_ratio: banner.image_width and banner.image_height,
			} %}
			{% if desktop_lazy %}
				<div class="placeholder placeholder-fade {{ has_responsive_images ? 'd-none d-md-block' }}"></div>
			{% endif %}
		{% elseif show_placeholder %}
			{# Fallback placeholder only when no image is configured at all. Cycles banner-1..6.webp by position. #}
			{% set placeholder_num = ((block_index | default(0)) % 6) + 1 %}
			{% set desktop_lazy = not is_priority %}
			{% include 'snippets/image.tpl' with {
				image_src: ('images/placeholders/banners/banner-' ~ placeholder_num ~ '.webp') | static_url,
				image_alt: 'accessibility.banner' | t,
				image_classes: 'img-fluid' ~ (desktop_lazy ? ' fade-in'),
				image_priority_high: is_priority,
				image_lazy_js: desktop_lazy,
				image_thumbs: false,
				image_width: 1000,
				image_height: 1000,
				image_aspect_ratio: true,
			} %}
			{% if desktop_lazy %}
				<div class="placeholder placeholder-fade"></div>
			{% endif %}
		{% endif %}
		{# Mobile image: prioritized for LCP on first banner of first section #}
		{% if banner.image_mobile %}
			{% include 'snippets/image.tpl' with {
				image_src: banner.image_mobile,
				image_alt: image_mobile_alt,
				image_classes: (has_responsive_images ? 'd-md-none ') ~ 'img-fluid' ~ (not is_priority ? ' fade-in'),
				image_priority_high: is_priority,
				image_lazy_js: not is_priority,
				image_width: banner.image_mobile_width,
				image_height: banner.image_mobile_height,
				image_aspect_ratio: banner.image_mobile_width and banner.image_mobile_height,
			} %}
			{% if not is_priority %}
				<div class="placeholder placeholder-fade {{ has_responsive_images ? 'd-md-none' }}"></div>
			{% endif %}
		{% endif %}
		
		{# Overlay #}
		{% if show_overlay and text_over_image %}
			<div class="media-overlay"></div>
		{% endif %}
	</div>
	
	{# Banner link as overlay #}
	{% if has_link %}
		<a href="{{ banner.link }}" class="{% if text_outside %}banner-link-overlay{% else %}media-link{% endif %}" aria-label="{{ 'general.banner' | t }}"></a>
	{% endif %}
	
	{# Content - Renders sub-blocks #}
	{% if block.blocks | length > 0 %}
		<div class="media-content {% if text_outside %}{{ text_alignment_class }}{% else %}media-content-floating {{ content_position_class }}{% endif %} {% if has_link %}media-content-linked{% endif %}" style="gap: {{ block_gap }}px; padding: {{ block_vertical_padding }}px {{ block_horizontal_padding }}px;">
			{% for child_block in block.blocks %}
				{% if child_block and child_block.type is defined %}
					{% include 'blocks/' ~ child_block.type ~ '.tpl' with { block: child_block } %}
				{% endif %}
			{% endfor %}
		</div>
	{% endif %}
</div>

{% schema %}
{
  "name": "t:names.banner",
  "icon": "pictureIcon",
  "blocks": [
    { "tags": ["general"] }
  ],
  "settings": [
    {
      "type": "setting",
      "setting_type": "image_picker",
      "id": "image",
      "label": "t:settings.image"
    },
    {
      "type": "setting",
      "setting_type": "toggle",
      "id": "use_mobile_image",
      "label": "t:settings.use_mobile_image",
      "default": false
    },
    {
      "type": "setting",
      "setting_type": "image_picker",
      "id": "image_mobile",
      "label": "t:settings.image_mobile",
      "visible_if": "{{ block.settings.use_mobile_image }}"
    },
    {
      "type": "setting",
      "setting_type": "url",
      "id": "link",
      "label": "t:settings.link"
    },
    {
      "type": "header",
      "content": "t:names.disposition"
    },
    {
      "type": "setting",
      "setting_type": "alignment",
      "id": "alignment",
      "label": "t:settings.alignment",
      "options": [
        { "value": "start", "label": "t:options.left" },
        { "value": "center", "label": "t:options.center" },
        { "value": "end", "label": "t:options.right" }
      ],
      "default": "start",
      "vertical_options": [
        { "value": "top", "label": "t:options.top" },
        { "value": "center", "label": "t:options.center" },
        { "value": "bottom", "label": "t:options.bottom" }
      ],
      "vertical_default": "bottom",
      "vertical_disabled_if": "{{ block.settings.text_outside }}"
    },
    {
      "type": "setting",
      "setting_type": "checkbox",
      "id": "text_outside",
      "label": "t:settings.text_outside",
      "default": false
    },
    {
      "type": "header",
      "content": "t:names.colors"
    },
    {
      "type": "setting",
      "setting_type": "color",
      "id": "text_color",
      "label": "t:settings.text",
      "default_setting": "text_color"
    },
    {
      "type": "header",
      "content": "t:names.design"
    },
    {
      "type": "setting",
      "setting_type": "range",
      "id": "gap",
      "label": "t:settings.gap",
      "min": 0,
      "max": 50,
      "step": 4,
      "unit": "px",
      "default": 16,
      "icon": "vertical_spacing"
    },
    {
      "type": "setting",
      "setting_type": "range",
      "id": "vertical_padding",
      "label": "t:settings.vertical_padding",
      "min": 0,
      "max": 120,
      "step": 4,
      "unit": "px",
      "default": 32,
      "icon": "vertical_padding"
    },
    {
      "type": "setting",
      "setting_type": "range",
      "id": "horizontal_padding",
      "label": "t:settings.horizontal_padding",
      "min": 0,
      "max": 120,
      "step": 4,
      "unit": "px",
      "default": 32,
      "icon": "horizontal_padding"
    },
    {
      "type": "setting",
      "setting_type": "toggle",
      "id": "show_overlay",
      "label": "t:names.transparent_background",
      "default": false,
      "info": "t:settings.add_overlay",
      "header_toggle": true,
      "visible_if": "{{ block.settings.text_outside == false }}"
    },
    {
      "type": "setting",
      "setting_type": "color",
      "id": "overlay_color",
      "label": "t:settings.color",
      "default": "#000000",
      "visible_if": "{{ block.settings.show_overlay }}"
    },
    {
      "type": "setting",
      "setting_type": "range",
      "id": "overlay_opacity",
      "label": "t:settings.overlay_opacity",
      "min": 0,
      "max": 100,
      "step": 5,
      "unit": "%",
      "default": 30,
      "visible_if": "{{ block.settings.show_overlay }}"
    }
  ],
  "presets": [
    {
      "name": "t:names.banner",
      "settings": { "gap": 16, "vertical_padding": 32, "horizontal_padding": 32 },
      "blocks": [
        { "type": "heading", "settings": { "title": "t:defaults.banner.heading", "size": "h4" } },
        { "type": "text", "settings": { "text": "t:defaults.banner.description" } },
        { "type": "button", "settings": { "label": "t:defaults.banner.button" } }
      ]
    }
  ]
}
{% endschema %}
````

## Contexto íntegro — blocks/image.tpl

- Ruta lógica: `blocks/image.tpl`
- Clasificación: dependencia de lectura; no es candidata ni escribible
- SHA256 del origen: `ab10579daf74db55eb687b29641947cd67b3145b32a8b65cc7935018789d307f`

````
{# Image Block - Public, can be used anywhere #}

{% set img_settings = block.settings %}
{% set block_width = img_settings.width | default('fill') %}
{% set is_priority = is_priority | default(false) %}

{% set has_mobile_image = img_settings.use_mobile_image and img_settings.image_mobile %}
{% set has_responsive_images = img_settings.image and has_mobile_image %}
{% set has_image = img_settings.image or has_mobile_image %}
{% set show_placeholder = not has_image %}

{% set image_alt = img_settings.image | media_alt | default(store.name) %}
{% set image_mobile_alt = img_settings.image_mobile | media_alt | default(store.name) %}

<div class="image-block {% if block_width == 'fill' %}block-fill{% endif %}" {{ block | block_attributes }}>
	{% if img_settings.image %}
		{% if img_settings.link %}
			<a href="{{ img_settings.link }}" class="d-block">
		{% endif %}
		{% set desktop_lazy = has_responsive_images or not is_priority %}
		{% include 'snippets/image.tpl' with {
			image_src: img_settings.image,
			image_alt: image_alt,
			image_classes: (has_responsive_images ? 'd-none d-md-block ') ~ 'img-fluid' ~ (desktop_lazy ? ' fade-in'),
			image_priority_high: not has_responsive_images and is_priority,
			image_lazy_js: desktop_lazy,
			image_width: img_settings.image_width,
			image_height: img_settings.image_height,
			image_aspect_ratio: img_settings.image_width and img_settings.image_height,
		} %}
		{% if not is_priority %}
			<div class="placeholder placeholder-fade {{ has_responsive_images ? 'd-none d-md-block' }}"></div>
		{% endif %}
		{% if has_mobile_image %}
			{% include 'snippets/image.tpl' with {
				image_src: img_settings.image_mobile,
				image_alt: image_mobile_alt,
				image_classes: (has_responsive_images ? 'd-md-none ') ~ 'img-fluid' ~ (not is_priority ? ' fade-in'),
				image_priority_high: is_priority,
				image_lazy_js: not is_priority,
				image_width: img_settings.image_mobile_width,
				image_height: img_settings.image_mobile_height,
				image_aspect_ratio: img_settings.image_mobile_width and img_settings.image_mobile_height,
			} %}
			{% if not is_priority %}
				<div class="placeholder placeholder-fade {{ has_responsive_images ? 'd-md-none' }}"></div>
			{% endif %}
		{% endif %}
		{% if img_settings.link %}
			</a>
		{% endif %}
	{% elseif show_placeholder %}
		{# Fallback placeholder only when no image is configured at all. #}
		{% set desktop_lazy = not is_priority %}
		{% include 'snippets/image.tpl' with {
			image_src: 'images/placeholders/banners/banner-1.webp' | static_url,
			image_alt: 'accessibility.banner' | t,
			image_classes: 'img-fluid' ~ (desktop_lazy ? ' fade-in'),
			image_priority_high: is_priority,
			image_lazy_js: desktop_lazy,
		} %}
		{% if desktop_lazy %}
			<div class="placeholder placeholder-fade"></div>
		{% endif %}
	{% endif %}
</div>

{% schema %}
{
  "name": "t:names.image",
  "tags": ["general"],
  "category": "basic",
  "settings": [
    {
      "type": "setting",
      "setting_type": "image_picker",
      "id": "image",
      "label": "t:settings.image"
    },
    {
      "type": "setting",
      "setting_type": "toggle",
      "id": "use_mobile_image",
      "label": "t:settings.use_mobile_image",
      "default": false
    },
    {
      "type": "setting",
      "setting_type": "image_picker",
      "id": "image_mobile",
      "label": "t:settings.image_mobile",
      "visible_if": "{{ block.settings.use_mobile_image }}"
    },
    {
      "type": "setting",
      "setting_type": "url",
      "id": "link",
      "label": "t:settings.link"
    },
    {
      "type": "header",
      "content": "t:names.design"
    },
    {
      "type": "setting",
      "setting_type": "radio",
      "id": "width",
      "label": "t:settings.section_width",
      "options": [
        { "value": "fit", "label": "t:options.fit" },
        { "value": "fill", "label": "t:options.fill" }
      ],
      "default": "fill"
    }
  ],
  "presets": [
    {
      "name": "t:names.image",
      "category": "t:categories.media"
    }
  ]
}
{% endschema %}
````

## Contexto íntegro — sections/hero-divided.tpl

- Ruta lógica: `sections/hero-divided.tpl`
- Clasificación: dependencia de lectura; no es candidata ni escribible
- SHA256 del origen: `30a85e7b94e062889794463d9f2138dc69d58d620631631e2ab26b3a7f7cb487`

````
{#
  Hero Divided Section
  Full-width banner split in two halves, each with its own image.
  Desktop: side by side (50%/50%). Mobile: stacked.
#}
{% set hero = section.settings %}
{% set is_priority_section = section.index <= (template in ['home', 'product'] ? 1 : 2) %}

{# Image 1 #}
{% set has_mobile_image_1 = hero.use_mobile_image and hero.image_mobile %}
{% set has_responsive_images_1 = hero.image and has_mobile_image_1 %}
{% set image_alt_1 = hero.image | media_alt | default('accessibility.hero' | t) %}
{% set image_mobile_alt_1 = hero.image_mobile | media_alt | default('accessibility.hero' | t) %}

{# Image 2 #}
{% set has_mobile_image_2 = hero.use_mobile_image_2 and hero.image_mobile_2 %}
{% set has_responsive_images_2 = hero.image_2 and has_mobile_image_2 %}
{% set image_alt_2 = hero.image_2 | media_alt | default('accessibility.hero' | t) %}
{% set image_mobile_alt_2 = hero.image_mobile_2 | media_alt | default('accessibility.hero' | t) %}

{# Height #}
{% set height = hero.height %}

{# Parallax #}
{% set parallax = hero.parallax %}

{# Alignment #}
{% set horizontal_align = hero.alignment | default('center') %}
{% set vertical_align = hero.alignment_vertical | default('center') %}
{% set horizontal_align_class = horizontal_align == 'start' ? 'left' : (horizontal_align == 'end' ? 'right' : 'center') %}

{% if vertical_align == 'center' and horizontal_align_class == 'center' %}
  {% set content_position_class = 'media-content-center' %}
{% else %}
  {% set content_position_class = 'media-content-' ~ vertical_align ~ '-' ~ horizontal_align_class %}
{% endif %}

{# Text color #}
{% set text_color = hero.text_color %}

{# Overlay #}
{% set show_overlay = hero.show_overlay %}
{% set overlay_color = hero.overlay_color | default('#000000') %}
{% set overlay_opacity = show_overlay ? ((hero.overlay_opacity | default(30)) / 100) : 0 %}

{# Spacing #}
{% set gap = hero.gap | default(16) %}
{% set vertical_padding = hero.vertical_padding | default(0) %}
{% set horizontal_padding = hero.horizontal_padding | default(0) %}
{% set content_animation = hero.content_animation | default('none') %}

<div class="hero-divided section-full-width {% if parallax %}hero-parallax{% endif %}" style="min-height: {{ height }}vh; {% if show_overlay %}--media-overlay-color: {{ overlay_color }}; --media-overlay-opacity: {{ overlay_opacity }};{% endif %} {% if text_color %}color: {{ text_color }};{% endif %}">
  <div class="{% if parallax %}js-hero-parallax{% endif %} hero-divided-visual">

    {# Image 1 #}
    <div class="hero-divided-image">
      {% if hero.image %}
        {% set desktop_lazy_1 = has_responsive_images_1 or not is_priority_section %}
        {% include 'snippets/image.tpl' with {
          image_src: hero.image,
          image_alt: image_alt_1,
          image_classes: (has_responsive_images_1 ? 'd-none d-md-block ') ~ (desktop_lazy_1 ? 'fade-in'),
          image_priority_high: not has_responsive_images_1 and is_priority_section,
          image_lazy_js: desktop_lazy_1,
          image_width: hero.image_width,
          image_height: hero.image_height,
          image_aspect_ratio: hero.image_width and hero.image_height,
        } %}
        {% if desktop_lazy_1 %}
          <div class="placeholder placeholder-fade {{ has_responsive_images_1 ? 'd-none d-md-block' }}"></div>
        {% endif %}
      {% else %}
        {% set desktop_lazy = not is_priority_section %}
        {% include 'snippets/image.tpl' with {
          image_src: ('images/placeholders/hero/hero-1.webp') | static_url,
          image_alt: 'accessibility.hero' | t,
          image_classes: desktop_lazy ? 'fade-in',
          image_priority_high: is_priority_section,
          image_lazy_js: desktop_lazy,
          image_thumbs: false,
          image_width: 1280,
          image_height: 700,
          image_aspect_ratio: true,
        } %}
        {% if desktop_lazy %}
          <div class="placeholder placeholder-fade"></div>
        {% endif %}
      {% endif %}
      {% if has_mobile_image_1 %}
        {% include 'snippets/image.tpl' with {
          image_src: hero.image_mobile,
          image_alt: image_mobile_alt_1,
          image_classes: (has_responsive_images_1 ? 'd-md-none ') ~ (not is_priority_section ? 'fade-in'),
          image_priority_high: is_priority_section and not has_responsive_images_1,
          image_lazy_js: has_responsive_images_1 or not is_priority_section,
          image_width: hero.image_mobile_width,
          image_height: hero.image_mobile_height,
          image_aspect_ratio: hero.image_mobile_width and hero.image_mobile_height,
        } %}
        {% if not is_priority_section %}
          <div class="placeholder placeholder-fade {{ has_responsive_images_1 ? 'd-md-none' }}"></div>
        {% endif %}
      {% endif %}
      {% if show_overlay %}
        <div class="media-overlay"></div>
      {% endif %}
    </div>

    {# Image 2 #}
    <div class="hero-divided-image">
      {% if hero.image_2 %}
        {% include 'snippets/image.tpl' with {
          image_src: hero.image_2,
          image_alt: image_alt_2,
          image_classes: (has_responsive_images_2 ? 'd-none d-md-block ') ~ 'fade-in',
          image_priority_high: false,
          image_lazy_js: true,
          image_width: hero.image_2_width,
          image_height: hero.image_2_height,
          image_aspect_ratio: hero.image_2_width and hero.image_2_height,
        } %}
        <div class="placeholder placeholder-fade {{ has_responsive_images_2 ? 'd-none d-md-block' }}"></div>
      {% else %}
        {% include 'snippets/image.tpl' with {
          image_src: ('images/placeholders/hero/hero-2.webp') | static_url,
          image_alt: 'accessibility.hero' | t,
          image_classes: 'fade-in',
          image_lazy_js: true,
          image_thumbs: false,
          image_width: 1280,
          image_height: 700,
          image_aspect_ratio: true,
        } %}
        <div class="placeholder placeholder-fade"></div>
      {% endif %}
      {% if has_mobile_image_2 %}
        {% include 'snippets/image.tpl' with {
          image_src: hero.image_mobile_2,
          image_alt: image_mobile_alt_2,
          image_classes: (has_responsive_images_2 ? 'd-md-none ') ~ 'fade-in',
          image_lazy_js: true,
          image_width: hero.image_mobile_2_width,
          image_height: hero.image_mobile_2_height,
          image_aspect_ratio: hero.image_mobile_2_width and hero.image_mobile_2_height,
        } %}
        {% if has_responsive_images_2 %}
          <div class="placeholder placeholder-fade d-md-none"></div>
        {% endif %}
      {% endif %}
      {% if show_overlay %}
        <div class="media-overlay"></div>
      {% endif %}
    </div>
  </div>

  {# Content #}
  <div class="media-content media-content-floating {{ content_position_class }} {% if hero.link %}media-content-linked{% endif %} {% if content_animation != 'none' %}media-content-animate media-content-animate-{{ content_animation }}{% endif %}" style="gap: {{ gap }}px; padding: {{ vertical_padding }}px {{ horizontal_padding }}px;">
    {% for block in section.blocks %}
      {% include 'blocks/' ~ block.type ~ '.tpl' with { block: block } %}
    {% endfor %}
  </div>

  {# Full section link #}
  {% if hero.link %}
    <a href="{{ hero.link }}" class="media-link" aria-label="{{ 't:names.hero_divided' | t }}"></a>
  {% endif %}
</div>


{% schema %}
{
  "name": "t:names.hero_divided",
  "add_section_order": 1,
  "class": "section section-hero",
  "blocks": [
    { "tags": ["general"] }
  ],
  "settings": [
    {
      "type": "setting",
      "setting_type": "image_picker",
      "id": "image",
      "label": "t:settings.image_1"
    },
    {
      "type": "setting",
      "setting_type": "toggle",
      "id": "use_mobile_image",
      "label": "t:settings.use_mobile_image",
      "default": false
    },
    {
      "type": "setting",
      "setting_type": "image_picker",
      "id": "image_mobile",
      "label": "t:settings.image_mobile",
      "visible_if": "{{ section.settings.use_mobile_image }}"
    },
    {
      "type": "setting",
      "setting_type": "image_picker",
      "id": "image_2",
      "label": "t:settings.image_2"
    },
    {
      "type": "setting",
      "setting_type": "toggle",
      "id": "use_mobile_image_2",
      "label": "t:settings.use_mobile_image",
      "default": false
    },
    {
      "type": "setting",
      "setting_type": "image_picker",
      "id": "image_mobile_2",
      "label": "t:settings.image_mobile",
      "visible_if": "{{ section.settings.use_mobile_image_2 }}"
    },
    {
      "type": "setting",
      "setting_type": "url",
      "id": "link",
      "label": "t:settings.link"
    },
    {
      "type": "header",
      "content": "t:names.disposition"
    },
    {
      "type": "setting",
      "setting_type": "alignment",
      "id": "alignment",
      "label": "t:settings.alignment",
      "options": [
        { "value": "start", "label": "t:options.left" },
        { "value": "center", "label": "t:options.center" },
        { "value": "end", "label": "t:options.right" }
      ],
      "default": "center",
      "vertical_options": [
        { "value": "top", "label": "t:options.top" },
        { "value": "center", "label": "t:options.center" },
        { "value": "bottom", "label": "t:options.bottom" }
      ],
      "vertical_default": "center"
    },
    {
      "type": "header",
      "content": "t:names.design"
    },
    {
      "type": "setting",
      "setting_type": "range",
      "id": "height",
      "label": "t:settings.height",
      "min": 0,
      "max": 100,
      "step": 5,
      "unit": "%",
      "default": 80,
      "icon": "height"
    },
    {
      "type": "setting",
      "setting_type": "range",
      "id": "gap",
      "label": "t:settings.gap",
      "min": 0,
      "max": 50,
      "step": 4,
      "unit": "px",
      "default": 16,
      "icon": "vertical_spacing"
    },
    {
      "type": "setting",
      "setting_type": "range",
      "id": "vertical_padding",
      "label": "t:settings.vertical_padding",
      "min": 0,
      "max": 120,
      "step": 4,
      "unit": "px",
      "default": 0,
      "icon": "vertical_padding"
    },
    {
      "type": "setting",
      "setting_type": "range",
      "id": "horizontal_padding",
      "label": "t:settings.horizontal_padding",
      "min": 0,
      "max": 120,
      "step": 4,
      "unit": "px",
      "default": 0,
      "icon": "horizontal_padding"
    },
    {
      "type": "header",
      "content": "t:names.colors"
    },
    {
      "type": "setting",
      "setting_type": "color",
      "id": "text_color",
      "label": "t:settings.text",
      "default_setting": "text_color"
    },
    {
      "type": "setting",
      "setting_type": "toggle",
      "id": "show_overlay",
      "label": "t:names.transparent_background",
      "default": false,
      "info": "t:settings.add_overlay",
      "header_toggle": true
    },
    {
      "type": "setting",
      "setting_type": "color",
      "id": "overlay_color",
      "label": "t:settings.color",
      "default": "#000000",
      "visible_if": "{{ section.settings.show_overlay }}"
    },
    {
      "type": "setting",
      "setting_type": "range",
      "id": "overlay_opacity",
      "label": "t:settings.overlay_opacity",
      "min": 0,
      "max": 100,
      "step": 5,
      "unit": "%",
      "default": 30,
      "visible_if": "{{ section.settings.show_overlay }}"
    },
    {
      "type": "header",
      "content": "t:names.animation"
    },
    {
      "type": "setting",
      "setting_type": "select",
      "id": "content_animation",
      "label": "t:settings.content_animation",
      "options": [
        { "value": "none", "label": "t:options.none" },
        { "value": "fade", "label": "t:options.fade" },
        { "value": "slide-up", "label": "t:options.slide_up" },
        { "value": "slide-down", "label": "t:options.slide_down" }
      ],
      "default": "none"
    },
    {
      "type": "setting",
      "setting_type": "toggle",
      "id": "parallax",
      "label": "t:settings.parallax",
      "default": false
    }
  ],
  "presets": [
    {
      "name": "t:names.hero_divided",
      "category": "t:categories.media",
      "settings": {
        "gap": 16,
        "vertical_padding": 32,
        "horizontal_padding": 32
      },
      "blocks": [
        { "type": "heading", "settings": { "title": "t:defaults.hero.heading", "size": "h1" } },
        { "type": "text", "settings": { "text": "t:defaults.hero.description" } },
        {
          "type": "group",
          "settings": {
            "direction": "row",
            "alignment": "center",
            "gap": 16,
            "vertical_padding": 0,
            "horizontal_padding": 0
          },
          "blocks": [
            { "type": "button", "settings": { "label": "t:defaults.banner.button", "size": "medium" } },
            { "type": "button", "settings": { "label": "t:defaults.banner.button", "size": "medium" } }
          ]
        }
      ]
    }
  ]
}
{% endschema %}
````

## Contexto íntegro — sections/category-hero.tpl

- Ruta lógica: `sections/category-hero.tpl`
- Clasificación: dependencia de lectura; no es candidata ni escribible
- SHA256 del origen: `ebde50d16b336c18aae56a1ab93817c22fa366c205a169671f453271051e304b`

````
{# Category Hero Section #}
{# Hero banner image for category pages, supports general or per-category images #}

{% set page_width = section.settings.section_width == 'page' %}
{# Top and bottom spacing are separate settings. `vertical_padding` (the old single
   setting) stays as the fallback so templates saved before the split keep their look. #}
{% set padding_top = section.settings.padding_top ?? section.settings.vertical_padding ?? 0 %}
{% set padding_bottom = section.settings.padding_bottom ?? section.settings.vertical_padding ?? 0 %}
{% set horizontal_padding = page_width ? 0 : section.settings.horizontal_padding | default(0) %}

{% set use_category_image = section.settings.show_category_image %}
{% set has_category_images = category.images is not empty %}
{% set has_general_image = section.settings.image %}
{% set has_default_banner = "banner-products.jpg" | has_custom_image %}

{# Resolve image URL #}
{% if use_category_image and has_category_images %}
  {% set banner_image_url = category.images | first %}
{% elseif has_general_image %}
  {% set banner_image_url = section.settings.image %}
{% elseif has_default_banner %}
  {% set banner_image_url = 'banner-products.jpg' | static_url %}
{% endif %}

{% set has_image = banner_image_url is not empty %}
{% set has_mobile_image = section.settings.use_mobile_image and section.settings.image_mobile %}
{% set has_responsive_images = has_image and has_mobile_image %}
{% set image_alt = section.settings.image | media_alt | default(category.name) %}
{% set image_mobile_alt = section.settings.image_mobile | media_alt | default(category.name) %}

{% set is_priority = section.index <= 2 %}

{% if has_image %}


  <div class="category-hero"
    style="padding: {{ padding_top }}px {{ horizontal_padding }}px {{ padding_bottom }}px;">
    {% if page_width %}
      <div class="container">
    {% endif %}

      <div class="category-banner position-relative" data-store="category-banner">
        {% set desktop_lazy = has_responsive_images or not is_priority %}
        {% include 'snippets/image.tpl' with {
          image_src: banner_image_url,
          category_image: use_category_image and has_category_images,
          image_alt: image_alt,
          image_classes: 'img-fluid w-100' ~ (has_responsive_images ? ' d-none d-md-block') ~ (desktop_lazy ? ' fade-in'),
          image_priority_high: not has_responsive_images and is_priority,
          image_lazy_js: desktop_lazy,
          image_thumbs: (use_category_image and has_category_images) or has_general_image ? null : false,
        } %}
        {% if desktop_lazy %}
          <div class="placeholder placeholder-fade {{ has_responsive_images ? 'd-none d-md-block' }}"></div>
        {% endif %}

        {% if has_mobile_image %}
          {% include 'snippets/image.tpl' with {
            image_src: section.settings.image_mobile,
            image_alt: image_mobile_alt,
            image_classes: 'img-fluid w-100 d-md-none' ~ (not is_priority ? ' fade-in'),
            image_priority_high: is_priority,
            image_lazy_js: not is_priority,
          } %}
          {% if not is_priority %}
            <div class="placeholder placeholder-fade d-md-none"></div>
          {% endif %}
        {% endif %}
      </div>

    {% if page_width %}
      </div>
    {% endif %}
  </div>


{% endif %}

{% schema %}
{
  "name": "t:names.category_hero",
  "class": "section section-category-hero m-0",
  "limit": 1,
  "deletable": false,
  "settings": [
    {
      "type": "setting",
      "setting_type": "image_picker",
      "id": "image",
      "label": "t:settings.image"
    },
    {
      "type": "setting",
      "setting_type": "toggle",
      "id": "use_mobile_image",
      "label": "t:settings.use_mobile_image",
      "default": false
    },
    {
      "type": "setting",
      "setting_type": "image_picker",
      "id": "image_mobile",
      "label": "t:settings.image",
      "visible_if": "{{ section.settings.use_mobile_image }}"
    },
    {
      "type": "setting",
      "setting_type": "toggle",
      "id": "show_category_image",
      "label": "t:settings.show_category_image",
      "header_toggle": true,
      "default": true
    },
    {
      "type": "paragraph",
      "content": "t:info.category_image_description",
      "visible_if": "{{ section.settings.show_category_image }}"
    },
    {
      "type": "header",
      "content": "t:names.design"
    },
    {
      "type": "setting",
      "setting_type": "radio",
      "id": "section_width",
      "label": "t:settings.section_width",
      "options": [
        { "value": "page", "label": "t:options.page" },
        { "value": "full", "label": "t:options.full" }
      ],
      "default": "full"
    },
    {
      "type": "setting",
      "setting_type": "range",
      "id": "padding_top",
      "label": "t:settings.padding_top",
      "min": 0,
      "max": 120,
      "step": 4,
      "unit": "px",
      "default": 0,
      "icon": "vertical_padding"
    },
    {
      "type": "setting",
      "setting_type": "range",
      "id": "padding_bottom",
      "label": "t:settings.padding_bottom",
      "min": 0,
      "max": 120,
      "step": 4,
      "unit": "px",
      "default": 0,
      "icon": "vertical_padding"
    },
    {
      "type": "setting",
      "setting_type": "range",
      "id": "horizontal_padding",
      "label": "t:settings.horizontal_padding",
      "min": 0,
      "max": 120,
      "step": 4,
      "unit": "px",
      "default": 0,
      "icon": "horizontal_padding",
      "disabled_if": "{{ section.settings.section_width == 'page' }}"
    }
  ],
  "blocks": [],
  "enabled_on": {
    "page_templates": ["category"]
  },
  "presets": [
    {
      "name": "t:names.category_hero"
    }
  ]
}
{% endschema %}
````

## Contexto íntegro — layouts/layout.tpl

- Ruta lógica: `layouts/layout.tpl`
- Clasificación: dependencia de lectura; no es candidata ni escribible
- SHA256 del origen: `aa0d59caa5947993a057fc13b4517057286a65a28e24029abb22b839cc18ba31`

````
{#
  Lightweight blog endpoints for static/js/blog-tags.js and blog-listing.js. Not linked
  anywhere, noindex, canonical to the real page:
    - /blog/posts/<handle>/?view=tags answers only the tables of the post body (where
      the tags live) instead of the whole page. The platform does not pass post.content
      to the blog listing nor to the product page, but it does on the post page.
    - /blog/?page=N&view=cards answers only the page sections (the listing grid), without
      header, footer and scripts, to index the whole blog for the tag filter.
#}
{% if template == 'blog-post' and params.view == 'tags' %}
<!DOCTYPE html>
<html lang="{{ html_lang }}">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{{ store.url }}/blog/posts/{{ post.handle }}/">
</head>
<body>
<div class="post-content" data-blog-tags-endpoint="true">{% for tags_table in (post.content | default('') | split('<table')) | slice(1) %}<table{{ tags_table | split('</table>') | first | raw }}</table>{% endfor %}</div>
</body>
</html>
{% elseif template == 'blog' and params.view == 'cards' %}
<!DOCTYPE html>
<html lang="{{ html_lang }}">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{{ store.blog_url }}">
</head>
<body>
{{ page_template_content }}
</body>
</html>
{% elseif template == 'product' and params.view == 'card' %}
{#
  Lightweight product endpoint for the product cards of the blog post body
  (static/js/blog-post.js): /productos/<handle>/?view=card answers only the name,
  cover, price, compare price, discount, installments, shipping label and a short
  description, instead of the whole product page. Not linked anywhere, noindex,
  canonical to the product.
#}
{% set card_shipping_discount = cart.free_shipping.min_price_free_shipping %}
{% set card_above_free_shipping = card_shipping_discount and (product.price >= card_shipping_discount.min_price_raw) %}
{% set card_can_show_config_shipping = card_shipping_discount.combines_with_other_discounts or not product.promotional_price_percentage %}
{% set card_show_shipping = not product.is_non_shippable and (product.free_shipping or (card_above_free_shipping and card_can_show_config_shipping)) %}
{% set card_has_compare = product.display_price and product.compare_at_price and product.compare_at_price > product.price %}
<!DOCTYPE html>
<html lang="{{ html_lang }}">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{{ product.canonical_url }}">
</head>
<body>
<div class="js-blog-product-data" data-blog-product-endpoint="true" data-product-id="{{ product.id }}" data-image="{{ product.featured_image | product_image_url('large') }}" data-image-srcset="{{ product.featured_image | product_image_url('medium') }} 320w, {{ product.featured_image | product_image_url('large') }} 480w, {{ product.featured_image | product_image_url('huge') }} 640w, {{ product.featured_image | product_image_url('original') }} 1024w">
<span data-field="name">{{ product.name | escape }}</span>
{% if product.display_price %}<span data-field="price">{{ product.price | money }}</span>{% endif %}
{% if card_has_compare %}<span data-field="compare">{{ product.compare_at_price | money }}</span><span data-field="discount">{{ product.promotional_price_percentage | round }}</span>{% endif %}
{% if settings.product_installments %}<div data-field="installments">{% include 'snippets/payments/installments.tpl' with { location: 'product_item', short_wording: true } %}</div>{% endif %}
{% if card_show_shipping %}<span data-field="shipping">{% if product.free_shipping or card_shipping_discount.is_free %}{{ 'product.free_shipping' | t }}{% elseif card_shipping_discount.discount_type == 'percentage' %}{{ card_shipping_discount.discount_value | round }}% {{ 'shipping.discount' | t }}{% elseif card_shipping_discount.discount_value_money %}{{ card_shipping_discount.discount_value_money }} {{ 'shipping.discount' | t }}{% endif %}</span>{% endif %}
{# Legacy card text = the product's SEO meta description; falls back to the long description #}
{% set card_description = product.seo_description | default('') | striptags | trim %}
{% if not card_description %}{% set card_description = product.description | default('') | striptags | trim %}{% endif %}
<span data-field="description">{{ card_description | slice(0, 240) | escape }}</span>
</div>
</body>
</html>
{% else %}
<!DOCTYPE html>
<html lang="{{ html_lang }}">
  <head>
    {# Meta tags component #}
    {{ component('head-tags') }}

    {# Google Fonts preconnect & DNS prefetch #}
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link rel="dns-prefetch" href="https://fonts.googleapis.com" />
    <link rel="dns-prefetch" href="https://fonts.gstatic.com" />

    {# CDN and external assets prefetch #}
    <link rel="dns-prefetch" href="https://d26lpennugtm8s.cloudfront.net" />
    <link rel="dns-prefetch" href="https://acdn.mitiendanube.com" />
    <link rel="preconnect" href="https://googrev.abejita.co" />
    <link rel="dns-prefetch" href="https://googrev.abejita.co" />
    <link rel="preconnect" href="https://lh3.googleusercontent.com" />
    <link rel="dns-prefetch" href="https://lh3.googleusercontent.com" />
    
    {# Preload critical assets #}
    <link rel="preload" as="style" href="{{ ([settings.font_headings, settings.font_rest] | merge(additional_fonts)) | google_fonts_url('400,500,700,800') }}" />
    <link rel="preload" href="{{ 'js/libraries-standalone.js' | static_url }}" as="script" />
    <link rel="preload" href="{{ 'css/style-critical.css' | static_url }}" as="style" />
    <link rel="preload" href="{{ 'css/style-utilities.css' | static_url }}" as="style" />

    {# Style Tokens (fonts + CSS custom properties) #}
    <style>
      {% include 'layouts/resources/style-tokens.tpl' %}
    </style>

    {# Critical CSS #}
    {{ 'css/style-critical.css' | static_url | static_inline }}

    {# Utilities CSS #}
    {{ 'css/style-utilities.css' | static_url | static_inline }}

    {% if params.preview or is_preview or is_preset_preview or ('rhino-contact' in page_template_content) or ('rhino-account' in page_template_content) %}
      {{ 'css/style-forms.css' | static_url | static_inline }}
    {% endif %}

    {# Async CSS loading #}
    <link rel="stylesheet" href="{{ 'css/style-async.css' | static_url }}" media="print" onload="this.media='all'">

    {# Custom CSS from settings #}
    {% if settings.css_code %}
      <style id="custom-theme-css">
        {{ settings.css_code | raw }}
      </style>
    {% endif %}

    {% set async_js = true %}

    {# Platform head content #}
    {% platform_head_content %}

    {# Structured data #}
    {% include 'snippets/structured-data/structured-data-organization.tpl' %}
    {% include 'snippets/structured-data/structured-data.tpl' %}
    {# Blog post: the include above already emits BlogPosting on this template (the
       platform defines blog_item there); only its breadcrumbs are added here #}
    {% if template == 'blog-post' %}
      <script type="application/ld+json" data-component="structured-data.blog-post-breadcrumbs">
      {
        "@context": "https://schema.org/",
        "@type": "BreadcrumbList",
        "itemListElement": [
          {
            "@type": "ListItem",
            "position": 1,
            "name": {{ 'breadcrumbs.home' | t | json_encode | raw }},
            "item": {{ store.url | json_encode | raw }}
          },
          {
            "@type": "ListItem",
            "position": 2,
            "name": {{ 'breadcrumbs.blog' | t | json_encode | raw }},
            "item": {{ ((store.blog_url starts with 'http://' or store.blog_url starts with 'https://') ? store.blog_url : ((store.url | trim('/')) ~ store.blog_url)) | json_encode | raw }}
          },
          {
            "@type": "ListItem",
            "position": 3,
            "name": {{ post.title | json_encode | raw }},
            "item": {{ (store.url ~ '/blog/posts/' ~ post.handle) | json_encode | raw }}
          }
        ]
      }
      </script>
    {% endif %}

    {# Microsoft Clarity #}
    {% set clarity_id = settings.clarity_project_id ?? 'z9hv5475vm' %}
    {% if clarity_id and not params.preview %}
      {% include 'snippets/analytics/clarity.tpl' with { clarity_id: clarity_id } %}
    {% endif %}

  </head>

  {% set cart_favicon_url = settings.cart_favicon ? (settings.cart_favicon | resolve_media).sourceUrl : '' %}

  <body
    class="{% if customer %}customer-logged-in{% endif %} template-{{ template | replace('.', '-') | replace('/', '-') }} {% if template == 'password' %}body-password{% endif %}"
    {% if settings.ajax_cart %}data-ajax-cart="true"{% endif %}
    {% if settings.inactive_tab_message %}
      data-inactive-tab-msg1="{{ settings.inactive_tab_message_01 | escape }}"
      data-inactive-tab-msg2="{{ settings.inactive_tab_message_02 | escape }}"
    {% endif %}
    {% if cart_favicon_url %}data-cart-favicon="{{ cart_favicon_url | escape }}"{% endif %}
    data-preview="{{ params.preview ? 'true' : 'false' }}"
  >
    {{ component('nubesdk-slot', { type: "before_main_content" }) }}

    {# SVG icons sprite #}
    {% include 'layouts/resources/icons-sprite.tpl' %}

    {# Back to admin bar #}
    {{ back_to_admin }}

    {# Header layout template - not shown on password page #}
    {% if template != 'password' %}
      <header class="js-header header">
        {% layout_template 'header' %}
      </header>
      {{ component('nubesdk-slot', { type: "after_header" }) }}
    {% endif %}

    {# Add to cart notification - Outside header for proper fixed positioning #}
    {% if settings.ajax_cart and template != 'password' %}
      {% include 'snippets/notification.tpl' with {
        type: 'add_to_cart',
      } %}
    {% endif %}

    {# Main content #}
    <main id="MainContent" class="main-content main-container" role="main">
      {{ page_template_content }}
    </main>

    {# Footer layout template - adapts automatically for password page #}
    {% layout_template 'footer' %}

    {% if template != 'password' %}
      {# Quick shop modal #}
      {% if settings.quick_shop %}
        {% include 'snippets/modals/quick-shop-modal.tpl' %}
      {% endif %}

      {# Cart modal - Ajax cart panel #}
      {% include 'snippets/cart/cart-modal.tpl' %}

      {# WhatsApp chat button #}
      {% include 'snippets/social/whatsapp-chat.tpl' %}

      {# Promotional modal #}
      {% if settings.promotional_popup_enabled %}
        {% include 'snippets/promotional-modal.tpl' %}
      {% endif %}

      {# Free shipping progress data #}
      <span class="js-ship-free-min hidden" data-pricemin="{{ cart.free_shipping.min_price_free_shipping.min_price_raw|default(0) }}"></span>
      <span class="js-free-shipping-config hidden" data-config="{{ cart.free_shipping.allFreeConfigurations }}"></span>
      <span class="js-cart-subtotal hidden" data-priceraw="{{ cart.subtotal }}"></span>
      <span class="js-cart-discount hidden" data-priceraw="{{ cart.promotional_discount_amount }}"></span>
    {% endif %}

    {# JavaScript - Standalone libraries (Swiper, Lazysizes) - blocking to guarantee availability #}
    {{ 'js/libraries-standalone.js' | static_url | script_tag }}

    {% set module_preview = params.preview or is_preview or is_preset_preview %}
    {% set page_has_athletes = module_preview or ('js-athletes-embla' in page_template_content) %}
    {% set page_has_products = module_preview or ('js-product-carousel' in page_template_content) %}
    {% set page_has_blog_carousel = module_preview or ('js-blog-carousel' in page_template_content) %}
    {% set page_has_sectionfy = module_preview or ('data-sectionfy-kind=' in page_template_content) %}
    {% set page_has_sectionfy_video = module_preview or ('data-sectionfy-video-slide' in page_template_content) %}
    {% set page_has_video = module_preview or ('js-video-block' in page_template_content) or ('js-pdp-video' in page_template_content) %}
    {# Also owns the header marquee / native Swiper visibility on simple pages. #}
    <script>
      window.rhinoMediaReady = new Promise(function(resolve) { window.rhinoMediaResolve = resolve; });
    </script>
    <script src="{{ 'js/media-visibility.js' | static_url }}" defer onload="window.rhinoMediaResolve()" onerror="window.rhinoMediaResolve()"></script>

    {# JavaScript - Embla carousel engine and the athletes-carousel init that consumes it.
       Deferred and in this order: the library has to define its globals before the init runs.
       Sections cannot emit their own <script>, so the pair is loaded here for every page. #}
    {% if page_has_athletes or page_has_products or page_has_blog_carousel %}
      <script src="{{ 'js/embla-carousel.js' | static_url }}" defer></script>
    {% endif %}
    {% if page_has_athletes %}
      <script src="{{ 'js/athletes-carousel.js' | static_url }}" defer></script>
    {% endif %}
    {# Blog tags: the parser, cache and pill renderer shared by the blog listing, the
       product page blog carousel, the blog post related posts and the home news section
       (static/js/blog-tags.js). Before all of them. #}
    {% if template == 'home' or template == 'product' or template == 'blog' or template == 'blog-post' %}
      <script src="{{ 'js/blog-tags.js' | static_url }}" defer></script>
    {% endif %}
    {# Product page carousels (alternative / complementary products), also on Embla #}
    {% if template == 'product' %}
      {% if page_has_products %}<script src="{{ 'js/product-carousel.js' | static_url }}" defer></script>{% endif %}
      {# Blog posts carousel (sections/blog-carousel.tpl), also on Embla + Autoplay #}
      {% if page_has_blog_carousel %}<script src="{{ 'js/blog-carousel.js' | static_url }}" defer></script>{% endif %}
      {# Product video section (sections/product-video.tpl): the player on click and the
         YouTube poster fallback, both delegated so the editor can add the section later #}
      {% if page_has_video %}<script src="{{ 'js/product-video.js' | static_url }}" defer></script>{% endif %}
    {% endif %}
    {# Home news section (sections/home-news.tpl): its hero and cards carousels run on the
       same blog carousel engine. It does nothing on a home page without that section. #}
    {% if template == 'home' and page_has_blog_carousel %}
      <script src="{{ 'js/blog-carousel.js' | static_url }}" defer></script>
    {% endif %}
    {# Home featured collection (sections/featured-collection.tpl): its mobile carousel
       runs on the product carousel engine (opt-in autoplay / mobile-only options) and its
       tabs on featured-collection.js, after it. Both do nothing on a home page without
       that section. #}
    {% if template == 'home' %}
      {% if page_has_products %}<script src="{{ 'js/product-carousel.js' | static_url }}" defer></script>{% endif %}
      {% if module_preview or ('js-featured-collection' in page_template_content) %}<script src="{{ 'js/featured-collection.js' | static_url }}" defer></script>{% endif %}
    {% endif %}
    {# Blog listing tag filter and filtered pagination (sections/main-blog.tpl) #}
    {% if template == 'blog' %}
      <script src="{{ 'js/blog-listing.js' | static_url }}" defer></script>
    {% endif %}
    {# Blog post page (sections/main-blog-post.tpl and sections/blog-post-related.tpl):
       product cards from the body links, previous / next navigation and the related
       posts fallback. After blog-tags.js, which it uses. #}
    {% if template == 'blog-post' %}
      <script src="{{ 'js/blog-post.js' | static_url }}" defer></script>
    {% endif %}

    {# JavaScript - Sectionfy: the shared content client and the
       section renderers that register against it. Same reason and same order as
       above: the client has to define `window.Sectionfy` before a section script
       registers. The client only touches the network when the page has a Sectionfy
       mount, and it makes one request no matter how many renderers are loaded. #}
    {% if page_has_sectionfy %}<script src="{{ 'js/sectionfy-client.js' | static_url }}" defer></script>{% endif %}
    {% if page_has_sectionfy_video %}
      <link rel="stylesheet" href="{{ 'css/sectionfy-video-slide.css' | static_url }}">
      <script src="{{ 'js/sectionfy-video-slide.js' | static_url }}" defer></script>
    {% endif %}
    {% if module_preview or ('js-sectionfy-faq-' in page_template_content) %}
      <script src="{{ 'js/sectionfy-faq-section.js' | static_url }}" defer></script>
    {% endif %}
    {% if module_preview or ('js-sectionfy-specs' in page_template_content) %}
      <script src="{{ 'js/sectionfy-specs-section.js' | static_url }}" defer></script>
    {% endif %}
    {% if module_preview or ('js-sectionfy-description-card' in page_template_content) %}
      <script src="{{ 'js/sectionfy-description-card-section.js' | static_url }}" defer></script>
    {% endif %}

    {% if template != 'home' and template != 'product' %}
      {% if page_has_products %}<script src="{{ 'js/product-carousel.js' | static_url }}" defer></script>{% endif %}
      {% if page_has_blog_carousel %}<script src="{{ 'js/blog-carousel.js' | static_url }}" defer></script>{% endif %}
    {% endif %}

    {# JavaScript - Non-critical libraries and theme store: loaded after LS.ready #}
    <script>
      Promise.all([LS.ready, window.rhinoMediaReady]).then(function() {

        {% include "static/js/libraries.js.tpl" %}

        var script = document.createElement('script');
        script.src = '{{ "js/store.js" | static_url }}';
        document.body.appendChild(script);
      });
    </script>

    {% platform_body_content %}
  </body>
</html>
{% endif %}
````

## Contexto íntegro — static/js/libraries-standalone.js

- Ruta lógica: `static/js/libraries-standalone.js`
- Clasificación: dependencia de lectura; no es candidata ni escribible
- SHA256 del origen: `da2638c043034114cb004b2fd99cd4d54ee69c7d569bd2c96cca8e586d2e0d34`

````
/*============================================================================
    Libraries that do NOT depend on other libraries
==============================================================================*/

/*! lazysizes - v5.2.2 */
!function(e){var t=function(u,D,f){"use strict";var k,H;if(function(){var e;var t={lazyClass:"lazyload",loadedClass:"lazyloaded",loadingClass:"lazyloading",preloadClass:"lazypreload",errorClass:"lazyerror",autosizesClass:"lazyautosizes",srcAttr:"data-src",srcsetAttr:"data-srcset",sizesAttr:"data-sizes",minSize:40,customMedia:{},init:true,expFactor:1.5,hFac:.8,loadMode:2,loadHidden:true,ricTimeout:0,throttleDelay:125};H=u.lazySizesConfig||u.lazysizesConfig||{};for(e in t){if(!(e in H)){H[e]=t[e]}}}(),!D||!D.getElementsByClassName){return{init:function(){},cfg:H,noSupport:true}}var O=D.documentElement,a=u.HTMLPictureElement,P="addEventListener",$="getAttribute",q=u[P].bind(u),I=u.setTimeout,U=u.requestAnimationFrame||I,l=u.requestIdleCallback,j=/^picture$/i,r=["load","error","lazyincluded","_lazyloaded"],i={},G=Array.prototype.forEach,J=function(e,t){if(!i[t]){i[t]=new RegExp("(\\s|^)"+t+"(\\s|$)")}return i[t].test(e[$]("class")||"")&&i[t]},K=function(e,t){if(!J(e,t)){e.setAttribute("class",(e[$]("class")||"").trim()+" "+t)}},Q=function(e,t){var i;if(i=J(e,t)){e.setAttribute("class",(e[$]("class")||"").replace(i," "))}},V=function(t,i,e){var a=e?P:"removeEventListener";if(e){V(t,i)}r.forEach(function(e){t[a](e,i)})},X=function(e,t,i,a,r){var n=D.createEvent("Event");if(!i){i={}}i.instance=k;n.initEvent(t,!a,!r);n.detail=i;e.dispatchEvent(n);return n},Y=function(e,t){var i;if(!a&&(i=u.picturefill||H.pf)){if(t&&t.src&&!e[$]("srcset")){e.setAttribute("srcset",t.src)}i({reevaluate:true,elements:[e]})}else if(t&&t.src){e.src=t.src}},Z=function(e,t){return(getComputedStyle(e,null)||{})[t]},s=function(e,t,i){i=i||e.offsetWidth;while(i<H.minSize&&t&&!e._lazysizesWidth){i=t.offsetWidth;t=t.parentNode}return i},ee=function(){var i,a;var t=[];var r=[];var n=t;var s=function(){var e=n;n=t.length?r:t;i=true;a=false;while(e.length){e.shift()()}i=false};var e=function(e,t){if(i&&!t){e.apply(this,arguments)}else{n.push(e);if(!a){a=true;(D.hidden?I:U)(s)}}};e._lsFlush=s;return e}(),te=function(i,e){return e?function(){ee(i)}:function(){var e=this;var t=arguments;ee(function(){i.apply(e,t)})}},ie=function(e){var i;var a=0;var r=H.throttleDelay;var n=H.ricTimeout;var t=function(){i=false;a=f.now();e()};var s=l&&n>49?function(){l(t,{timeout:n});if(n!==H.ricTimeout){n=H.ricTimeout}}:te(function(){I(t)},true);return function(e){var t;if(e=e===true){n=33}if(i){return}i=true;t=r-(f.now()-a);if(t<0){t=0}if(e||t<9){s()}else{I(s,t)}}},ae=function(e){var t,i;var a=99;var r=function(){t=null;e()};var n=function(){var e=f.now()-i;if(e<a){I(n,a-e)}else{(l||r)(r)}};return function(){i=f.now();if(!t){t=I(n,a)}}},e=function(){var v,m,c,h,e;var y,z,g,p,C,b,A;var n=/^img$/i;var d=/^iframe$/i;var E="onscroll"in u&&!/(gle|ing)bot/.test(navigator.userAgent);var _=0;var w=0;var N=0;var M=-1;var x=function(e){N--;if(!e||N<0||!e.target){N=0}};var W=function(e){if(A==null){A=Z(D.body,"visibility")=="hidden"}return A||!(Z(e.parentNode,"visibility")=="hidden"&&Z(e,"visibility")=="hidden")};var S=function(e,t){var i;var a=e;var r=W(e);g-=t;b+=t;p-=t;C+=t;while(r&&(a=a.offsetParent)&&a!=D.body&&a!=O){r=(Z(a,"opacity")||1)>0;if(r&&Z(a,"overflow")!="visible"){i=a.getBoundingClientRect();r=C>i.left&&p<i.right&&b>i.top-1&&g<i.bottom+1}}return r};var t=function(){var e,t,i,a,r,n,s,l,o,u,f,c;var d=k.elements;if((h=H.loadMode)&&N<8&&(e=d.length)){t=0;M++;for(;t<e;t++){if(!d[t]||d[t]._lazyRace){continue}if(!E||k.prematureUnveil&&k.prematureUnveil(d[t])){R(d[t]);continue}if(!(l=d[t][$]("data-expand"))||!(n=l*1)){n=w}if(!u){u=!H.expand||H.expand<1?O.clientHeight>500&&O.clientWidth>500?500:370:H.expand;k._defEx=u;f=u*H.expFactor;c=H.hFac;A=null;if(w<f&&N<1&&M>2&&h>2&&!D.hidden){w=f;M=0}else if(h>1&&M>1&&N<6){w=u}else{w=_}}if(o!==n){y=innerWidth+n*c;z=innerHeight+n;s=n*-1;o=n}i=d[t].getBoundingClientRect();if((b=i.bottom)>=s&&(g=i.top)<=z&&(C=i.right)>=s*c&&(p=i.left)<=y&&(b||C||p||g)&&(H.loadHidden||W(d[t]))&&(m&&N<3&&!l&&(h<3||M<4)||S(d[t],n))){R(d[t]);r=true;if(N>9){break}}else if(!r&&m&&!a&&N<4&&M<4&&h>2&&(v[0]||H.preloadAfterLoad)&&(v[0]||!l&&(b||C||p||g||d[t][$](H.sizesAttr)!="auto"))){a=v[0]||d[t]}}if(a&&!r){R(a)}}};var i=ie(t);var B=function(e){var t=e.target;if(t._lazyCache){delete t._lazyCache;return}x(e);K(t,H.loadedClass);Q(t,H.loadingClass);V(t,L);X(t,"lazyloaded")};var a=te(B);var L=function(e){a({target:e.target})};var T=function(t,i){try{t.contentWindow.location.replace(i)}catch(e){t.src=i}};var F=function(e){var t;var i=e[$](H.srcsetAttr);if(t=H.customMedia[e[$]("data-media")||e[$]("media")]){e.setAttribute("media",t)}if(i){e.setAttribute("srcset",i)}};var s=te(function(t,e,i,a,r){var n,s,l,o,u,f;if(!(u=X(t,"lazybeforeunveil",e)).defaultPrevented){if(a){if(i){K(t,H.autosizesClass)}else{t.setAttribute("sizes",a)}}s=t[$](H.srcsetAttr);n=t[$](H.srcAttr);if(r){l=t.parentNode;o=l&&j.test(l.nodeName||"")}f=e.firesLoad||"src"in t&&(s||n||o);u={target:t};K(t,H.loadingClass);if(f){clearTimeout(c);c=I(x,2500);V(t,L,true)}if(o){G.call(l.getElementsByTagName("source"),F)}if(s){t.setAttribute("srcset",s)}else if(n&&!o){if(d.test(t.nodeName)){T(t,n)}else{t.src=n}}if(r&&(s||o)){Y(t,{src:n})}}if(t._lazyRace){delete t._lazyRace}Q(t,H.lazyClass);ee(function(){var e=t.complete&&t.naturalWidth>1;if(!f||e){if(e){K(t,"ls-is-cached")}B(u);t._lazyCache=true;I(function(){if("_lazyCache"in t){delete t._lazyCache}},9)}if(t.loading=="lazy"){N--}},true)});var R=function(e){if(e._lazyRace){return}var t;var i=n.test(e.nodeName);var a=i&&(e[$](H.sizesAttr)||e[$]("sizes"));var r=a=="auto";if((r||!m)&&i&&(e[$]("src")||e.srcset)&&!e.complete&&!J(e,H.errorClass)&&J(e,H.lazyClass)){return}t=X(e,"lazyunveilread").detail;if(r){re.updateElem(e,true,e.offsetWidth)}e._lazyRace=true;N++;s(e,t,r,a,i)};var r=ae(function(){H.loadMode=3;i()});var l=function(){if(H.loadMode==3){H.loadMode=2}r()};var o=function(){if(m){return}if(f.now()-e<999){I(o,999);return}m=true;H.loadMode=3;i();q("scroll",l,true)};return{_:function(){e=f.now();k.elements=D.getElementsByClassName(H.lazyClass);v=D.getElementsByClassName(H.lazyClass+" "+H.preloadClass);q("scroll",i,true);q("resize",i,true);q("pageshow",function(e){if(e.persisted){var t=D.querySelectorAll("."+H.loadingClass);if(t.length&&t.forEach){U(function(){t.forEach(function(e){if(e.complete){R(e)}})})}}});if(u.MutationObserver){new MutationObserver(i).observe(O,{childList:true,subtree:true,attributes:true})}else{O[P]("DOMNodeInserted",i,true);O[P]("DOMAttrModified",i,true);setInterval(i,999)}q("hashchange",i,true);["focus","mouseover","click","load","transitionend","animationend"].forEach(function(e){D[P](e,i,true)});if(/d$|^c/.test(D.readyState)){o()}else{q("load",o);D[P]("DOMContentLoaded",i);I(o,2e4)}if(k.elements.length){t();ee._lsFlush()}else{i()}},checkElems:i,unveil:R,_aLSL:l}}(),re=function(){var i;var n=te(function(e,t,i,a){var r,n,s;e._lazysizesWidth=a;a+="px";e.setAttribute("sizes",a);if(j.test(t.nodeName||"")){r=t.getElementsByTagName("source");for(n=0,s=r.length;n<s;n++){r[n].setAttribute("sizes",a)}}if(!i.detail.dataAttr){Y(e,i.detail)}});var a=function(e,t,i){var a;var r=e.parentNode;if(r){i=s(e,r,i);a=X(e,"lazybeforesizes",{width:i,dataAttr:!!t});if(!a.defaultPrevented){i=a.detail.width;if(i&&i!==e._lazysizesWidth){n(e,r,a,i)}}}};var e=function(){var e;var t=i.length;if(t){e=0;for(;e<t;e++){a(i[e])}}};var t=ae(e);return{_:function(){i=D.getElementsByClassName(H.autosizesClass);q("resize",t)},checkElems:t,updateElem:a}}(),t=function(){if(!t.i&&D.getElementsByClassName){t.i=true;re._();e._()}};return I(function(){H.init&&t()}),k={cfg:H,autoSizer:re,loader:e,init:t,uP:Y,aC:K,rC:Q,hC:J,fire:X,gW:s,rAF:ee}}(e,e.document,Date);e.lazySizes=t,"object"==typeof module&&module.exports&&(module.exports=t)}("undefined"!=typeof window?window:{});

/* Swiper 6.3.2 */
!function(e,t){"object"==typeof exports&&"undefined"!=typeof module?module.exports=t():"function"==typeof define&&define.amd?define(t):(e=e||self).Swiper=t()}(this,(function(){"use strict";function e(e,t){for(var i=0;i<t.length;i++){var s=t[i];s.enumerable=s.enumerable||!1,s.configurable=!0,"value"in s&&(s.writable=!0),Object.defineProperty(e,s.key,s)}}function t(){return(t=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var i=arguments[t];for(var s in i)Object.prototype.hasOwnProperty.call(i,s)&&(e[s]=i[s])}return e}).apply(this,arguments)}function i(e){return null!==e&&"object"==typeof e&&"constructor"in e&&e.constructor===Object}function s(e,t){void 0===e&&(e={}),void 0===t&&(t={}),Object.keys(t).forEach((function(a){void 0===e[a]?e[a]=t[a]:i(t[a])&&i(e[a])&&Object.keys(t[a]).length>0&&s(e[a],t[a])}))}var a={body:{},addEventListener:function(){},removeEventListener:function(){},activeElement:{blur:function(){},nodeName:""},querySelector:function(){return null},querySelectorAll:function(){return[]},getElementById:function(){return null},createEvent:function(){return{initEvent:function(){}}},createElement:function(){return{children:[],childNodes:[],style:{},setAttribute:function(){},getElementsByTagName:function(){return[]}}},createElementNS:function(){return{}},importNode:function(){return null},location:{hash:"",host:"",hostname:"",href:"",origin:"",pathname:"",protocol:"",search:""}};function r(){var e="undefined"!=typeof document?document:{};return s(e,a),e}var n={document:a,navigator:{userAgent:""},location:{hash:"",host:"",hostname:"",href:"",origin:"",pathname:"",protocol:"",search:""},history:{replaceState:function(){},pushState:function(){},go:function(){},back:function(){}},CustomEvent:function(){return this},addEventListener:function(){},removeEventListener:function(){},getComputedStyle:function(){return{getPropertyValue:function(){return""}}},Image:function(){},Date:function(){},screen:{},setTimeout:function(){},clearTimeout:function(){},matchMedia:function(){return{}},requestAnimationFrame:function(e){return"undefined"==typeof setTimeout?(e(),null):setTimeout(e,0)},cancelAnimationFrame:function(e){"undefined"!=typeof setTimeout&&clearTimeout(e)}};function o(){var e="undefined"!=typeof window?window:{};return s(e,n),e}function l(e){return(l=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}function d(e,t){return(d=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function h(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Date.prototype.toString.call(Reflect.construct(Date,[],(function(){}))),!0}catch(e){return!1}}function p(e,t,i){return(p=h()?Reflect.construct:function(e,t,i){var s=[null];s.push.apply(s,t);var a=new(Function.bind.apply(e,s));return i&&d(a,i.prototype),a}).apply(null,arguments)}function u(e){var t="function"==typeof Map?new Map:void 0;return(u=function(e){if(null===e||(i=e,-1===Function.toString.call(i).indexOf("[native code]")))return e;var i;if("function"!=typeof e)throw new TypeError("Super expression must either be null or a function");if(void 0!==t){if(t.has(e))return t.get(e);t.set(e,s)}function s(){return p(e,arguments,l(this).constructor)}return s.prototype=Object.create(e.prototype,{constructor:{value:s,enumerable:!1,writable:!0,configurable:!0}}),d(s,e)})(e)}var c=function(e){var t,i;function s(t){var i,s,a;return i=e.call.apply(e,[this].concat(t))||this,s=function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(i),a=s.__proto__,Object.defineProperty(s,"__proto__",{get:function(){return a},set:function(e){a.__proto__=e}}),i}return i=e,(t=s).prototype=Object.create(i.prototype),t.prototype.constructor=t,t.__proto__=i,s}(u(Array));function v(e){void 0===e&&(e=[]);var t=[];return e.forEach((function(e){Array.isArray(e)?t.push.apply(t,v(e)):t.push(e)})),t}function f(e,t){return Array.prototype.filter.call(e,t)}function m(e,t){var i=o(),s=r(),a=[];if(!t&&e instanceof c)return e;if(!e)return new c(a);if("string"==typeof e){var n=e.trim();if(n.indexOf("<")>=0&&n.indexOf(">")>=0){var l="div";0===n.indexOf("<li")&&(l="ul"),0===n.indexOf("<tr")&&(l="tbody"),0!==n.indexOf("<td")&&0!==n.indexOf("<th")||(l="tr"),0===n.indexOf("<tbody")&&(l="table"),0===n.indexOf("<option")&&(l="select");var d=s.createElement(l);d.innerHTML=n;for(var h=0;h<d.childNodes.length;h+=1)a.push(d.childNodes[h])}else a=function(e,t){if("string"!=typeof e)return[e];for(var i=[],s=t.querySelectorAll(e),a=0;a<s.length;a+=1)i.push(s[a]);return i}(e.trim(),t||s)}else if(e.nodeType||e===i||e===s)a.push(e);else if(Array.isArray(e)){if(e instanceof c)return e;a=e}return new c(function(e){for(var t=[],i=0;i<e.length;i+=1)-1===t.indexOf(e[i])&&t.push(e[i]);return t}(a))}m.fn=c.prototype;var g,y,C,w={addClass:function(){for(var e=arguments.length,t=new Array(e),i=0;i<e;i++)t[i]=arguments[i];var s=v(t.map((function(e){return e.split(" ")})));return this.forEach((function(e){var t;(t=e.classList).add.apply(t,s)})),this},removeClass:function(){for(var e=arguments.length,t=new Array(e),i=0;i<e;i++)t[i]=arguments[i];var s=v(t.map((function(e){return e.split(" ")})));return this.forEach((function(e){var t;(t=e.classList).remove.apply(t,s)})),this},hasClass:function(){for(var e=arguments.length,t=new Array(e),i=0;i<e;i++)t[i]=arguments[i];var s=v(t.map((function(e){return e.split(" ")})));return f(this,(function(e){return s.filter((function(t){return e.classList.contains(t)})).length>0})).length>0},toggleClass:function(){for(var e=arguments.length,t=new Array(e),i=0;i<e;i++)t[i]=arguments[i];var s=v(t.map((function(e){return e.split(" ")})));this.forEach((function(e){s.forEach((function(t){e.classList.toggle(t)}))}))},attr:function(e,t){if(1===arguments.length&&"string"==typeof e)return this[0]?this[0].getAttribute(e):void 0;for(var i=0;i<this.length;i+=1)if(2===arguments.length)this[i].setAttribute(e,t);else for(var s in e)this[i][s]=e[s],this[i].setAttribute(s,e[s]);return this},removeAttr:function(e){for(var t=0;t<this.length;t+=1)this[t].removeAttribute(e);return this},transform:function(e){for(var t=0;t<this.length;t+=1)this[t].style.transform=e;return this},transition:function(e){for(var t=0;t<this.length;t+=1)this[t].style.transition="string"!=typeof e?e+"ms":e;return this},on:function(){for(var e=arguments.length,t=new Array(e),i=0;i<e;i++)t[i]=arguments[i];var s=t[0],a=t[1],r=t[2],n=t[3];function o(e){var t=e.target;if(t){var i=e.target.dom7EventData||[];if(i.indexOf(e)<0&&i.unshift(e),m(t).is(a))r.apply(t,i);else for(var s=m(t).parents(),n=0;n<s.length;n+=1)m(s[n]).is(a)&&r.apply(s[n],i)}}function l(e){var t=e&&e.target&&e.target.dom7EventData||[];t.indexOf(e)<0&&t.unshift(e),r.apply(this,t)}"function"==typeof t[1]&&(s=t[0],r=t[1],n=t[2],a=void 0),n||(n=!1);for(var d,h=s.split(" "),p=0;p<this.length;p+=1){var u=this[p];if(a)for(d=0;d<h.length;d+=1){var c=h[d];u.dom7LiveListeners||(u.dom7LiveListeners={}),u.dom7LiveListeners[c]||(u.dom7LiveListeners[c]=[]),u.dom7LiveListeners[c].push({listener:r,proxyListener:o}),u.addEventListener(c,o,n)}else for(d=0;d<h.length;d+=1){var v=h[d];u.dom7Listeners||(u.dom7Listeners={}),u.dom7Listeners[v]||(u.dom7Listeners[v]=[]),u.dom7Listeners[v].push({listener:r,proxyListener:l}),u.addEventListener(v,l,n)}}return this},off:function(){for(var e=arguments.length,t=new Array(e),i=0;i<e;i++)t[i]=arguments[i];var s=t[0],a=t[1],r=t[2],n=t[3];"function"==typeof t[1]&&(s=t[0],r=t[1],n=t[2],a=void 0),n||(n=!1);for(var o=s.split(" "),l=0;l<o.length;l+=1)for(var d=o[l],h=0;h<this.length;h+=1){var p=this[h],u=void 0;if(!a&&p.dom7Listeners?u=p.dom7Listeners[d]:a&&p.dom7LiveListeners&&(u=p.dom7LiveListeners[d]),u&&u.length)for(var c=u.length-1;c>=0;c-=1){var v=u[c];r&&v.listener===r||r&&v.listener&&v.listener.dom7proxy&&v.listener.dom7proxy===r?(p.removeEventListener(d,v.proxyListener,n),u.splice(c,1)):r||(p.removeEventListener(d,v.proxyListener,n),u.splice(c,1))}}return this},trigger:function(){for(var e=o(),t=arguments.length,i=new Array(t),s=0;s<t;s++)i[s]=arguments[s];for(var a=i[0].split(" "),r=i[1],n=0;n<a.length;n+=1)for(var l=a[n],d=0;d<this.length;d+=1){var h=this[d];if(e.CustomEvent){var p=new e.CustomEvent(l,{detail:r,bubbles:!0,cancelable:!0});h.dom7EventData=i.filter((function(e,t){return t>0})),h.dispatchEvent(p),h.dom7EventData=[],delete h.dom7EventData}}return this},transitionEnd:function(e){var t=this;return e&&t.on("transitionend",(function i(s){s.target===this&&(e.call(this,s),t.off("transitionend",i))})),this},outerWidth:function(e){if(this.length>0){if(e){var t=this.styles();return this[0].offsetWidth+parseFloat(t.getPropertyValue("margin-right"))+parseFloat(t.getPropertyValue("margin-left"))}return this[0].offsetWidth}return null},outerHeight:function(e){if(this.length>0){if(e){var t=this.styles();return this[0].offsetHeight+parseFloat(t.getPropertyValue("margin-top"))+parseFloat(t.getPropertyValue("margin-bottom"))}return this[0].offsetHeight}return null},styles:function(){var e=o();return this[0]?e.getComputedStyle(this[0],null):{}},offset:function(){if(this.length>0){var e=o(),t=r(),i=this[0],s=i.getBoundingClientRect(),a=t.body,n=i.clientTop||a.clientTop||0,l=i.clientLeft||a.clientLeft||0,d=i===e?e.scrollY:i.scrollTop,h=i===e?e.scrollX:i.scrollLeft;return{top:s.top+d-n,left:s.left+h-l}}return null},css:function(e,t){var i,s=o();if(1===arguments.length){if("string"!=typeof e){for(i=0;i<this.length;i+=1)for(var a in e)this[i].style[a]=e[a];return this}if(this[0])return s.getComputedStyle(this[0],null).getPropertyValue(e)}if(2===arguments.length&&"string"==typeof e){for(i=0;i<this.length;i+=1)this[i].style[e]=t;return this}return this},each:function(e){return e?(this.forEach((function(t,i){e.apply(t,[t,i])})),this):this},html:function(e){if(void 0===e)return this[0]?this[0].innerHTML:null;for(var t=0;t<this.length;t+=1)this[t].innerHTML=e;return this},text:function(e){if(void 0===e)return this[0]?this[0].textContent.trim():null;for(var t=0;t<this.length;t+=1)this[t].textContent=e;return this},is:function(e){var t,i,s=o(),a=r(),n=this[0];if(!n||void 0===e)return!1;if("string"==typeof e){if(n.matches)return n.matches(e);if(n.webkitMatchesSelector)return n.webkitMatchesSelector(e);if(n.msMatchesSelector)return n.msMatchesSelector(e);for(t=m(e),i=0;i<t.length;i+=1)if(t[i]===n)return!0;return!1}if(e===a)return n===a;if(e===s)return n===s;if(e.nodeType||e instanceof c){for(t=e.nodeType?[e]:e,i=0;i<t.length;i+=1)if(t[i]===n)return!0;return!1}return!1},index:function(){var e,t=this[0];if(t){for(e=0;null!==(t=t.previousSibling);)1===t.nodeType&&(e+=1);return e}},eq:function(e){if(void 0===e)return this;var t=this.length;if(e>t-1)return m([]);if(e<0){var i=t+e;return m(i<0?[]:[this[i]])}return m([this[e]])},append:function(){for(var e,t=r(),i=0;i<arguments.length;i+=1){e=i<0||arguments.length<=i?void 0:arguments[i];for(var s=0;s<this.length;s+=1)if("string"==typeof e){var a=t.createElement("div");for(a.innerHTML=e;a.firstChild;)this[s].appendChild(a.firstChild)}else if(e instanceof c)for(var n=0;n<e.length;n+=1)this[s].appendChild(e[n]);else this[s].appendChild(e)}return this},prepend:function(e){var t,i,s=r();for(t=0;t<this.length;t+=1)if("string"==typeof e){var a=s.createElement("div");for(a.innerHTML=e,i=a.childNodes.length-1;i>=0;i-=1)this[t].insertBefore(a.childNodes[i],this[t].childNodes[0])}else if(e instanceof c)for(i=0;i<e.length;i+=1)this[t].insertBefore(e[i],this[t].childNodes[0]);else this[t].insertBefore(e,this[t].childNodes[0]);return this},next:function(e){return this.length>0?e?this[0].nextElementSibling&&m(this[0].nextElementSibling).is(e)?m([this[0].nextElementSibling]):m([]):this[0].nextElementSibling?m([this[0].nextElementSibling]):m([]):m([])},nextAll:function(e){var t=[],i=this[0];if(!i)return m([]);for(;i.nextElementSibling;){var s=i.nextElementSibling;e?m(s).is(e)&&t.push(s):t.push(s),i=s}return m(t)},prev:function(e){if(this.length>0){var t=this[0];return e?t.previousElementSibling&&m(t.previousElementSibling).is(e)?m([t.previousElementSibling]):m([]):t.previousElementSibling?m([t.previousElementSibling]):m([])}return m([])},prevAll:function(e){var t=[],i=this[0];if(!i)return m([]);for(;i.previousElementSibling;){var s=i.previousElementSibling;e?m(s).is(e)&&t.push(s):t.push(s),i=s}return m(t)},parent:function(e){for(var t=[],i=0;i<this.length;i+=1)null!==this[i].parentNode&&(e?m(this[i].parentNode).is(e)&&t.push(this[i].parentNode):t.push(this[i].parentNode));return m(t)},parents:function(e){for(var t=[],i=0;i<this.length;i+=1)for(var s=this[i].parentNode;s;)e?m(s).is(e)&&t.push(s):t.push(s),s=s.parentNode;return m(t)},closest:function(e){var t=this;return void 0===e?m([]):(t.is(e)||(t=t.parents(e).eq(0)),t)},find:function(e){for(var t=[],i=0;i<this.length;i+=1)for(var s=this[i].querySelectorAll(e),a=0;a<s.length;a+=1)t.push(s[a]);return m(t)},children:function(e){for(var t=[],i=0;i<this.length;i+=1)for(var s=this[i].children,a=0;a<s.length;a+=1)e&&!m(s[a]).is(e)||t.push(s[a]);return m(t)},filter:function(e){return m(f(this,e))},remove:function(){for(var e=0;e<this.length;e+=1)this[e].parentNode&&this[e].parentNode.removeChild(this[e]);return this}};function b(e,t){return void 0===t&&(t=0),setTimeout(e,t)}function T(){return Date.now()}function S(e){return"object"==typeof e&&null!==e&&e.constructor&&e.constructor===Object}function x(){for(var e=Object(arguments.length<=0?void 0:arguments[0]),t=1;t<arguments.length;t+=1){var i=t<0||arguments.length<=t?void 0:arguments[t];if(null!=i)for(var s=Object.keys(Object(i)),a=0,r=s.length;a<r;a+=1){var n=s[a],o=Object.getOwnPropertyDescriptor(i,n);void 0!==o&&o.enumerable&&(S(e[n])&&S(i[n])?x(e[n],i[n]):!S(e[n])&&S(i[n])?(e[n]={},x(e[n],i[n])):e[n]=i[n])}}return e}function E(e,t){Object.keys(t).forEach((function(i){S(t[i])&&Object.keys(t[i]).forEach((function(s){"function"==typeof t[i][s]&&(t[i][s]=t[i][s].bind(e))})),e[i]=t[i]}))}function M(){return g||(g=function(){var e=o(),t=r();return{touch:!!("ontouchstart"in e||e.DocumentTouch&&t instanceof e.DocumentTouch),pointerEvents:!!e.PointerEvent&&"maxTouchPoints"in e.navigator&&e.navigator.maxTouchPoints>=0,observer:"MutationObserver"in e||"WebkitMutationObserver"in e,passiveListener:function(){var t=!1;try{var i=Object.defineProperty({},"passive",{get:function(){t=!0}});e.addEventListener("testPassiveListener",null,i)}catch(e){}return t}(),gestures:"ongesturestart"in e}}()),g}function P(e){return void 0===e&&(e={}),y||(y=function(e){var t=(void 0===e?{}:e).userAgent,i=M(),s=o(),a=s.navigator.platform,r=t||s.navigator.userAgent,n={ios:!1,android:!1},l=s.screen.width,d=s.screen.height,h=r.match(/(Android);?[\s\/]+([\d.]+)?/),p=r.match(/(iPad).*OS\s([\d_]+)/),u=r.match(/(iPod)(.*OS\s([\d_]+))?/),c=!p&&r.match(/(iPhone\sOS|iOS)\s([\d_]+)/),v="Win32"===a,f="MacIntel"===a;return!p&&f&&i.touch&&["1024x1366","1366x1024","834x1194","1194x834","834x1112","1112x834","768x1024","1024x768"].indexOf(l+"x"+d)>=0&&((p=r.match(/(Version)\/([\d.]+)/))||(p=[0,1,"13_0_0"]),f=!1),h&&!v&&(n.os="android",n.android=!0),(p||c||u)&&(n.os="ios",n.ios=!0),n}(e)),y}function k(){return C||(C=function(){var e,t=o();return{isEdge:!!t.navigator.userAgent.match(/Edge/g),isSafari:(e=t.navigator.userAgent.toLowerCase(),e.indexOf("safari")>=0&&e.indexOf("chrome")<0&&e.indexOf("android")<0),isWebView:/(iPhone|iPod|iPad).*AppleWebKit(?!.*Safari)/i.test(t.navigator.userAgent)}}()),C}Object.keys(w).forEach((function(e){m.fn[e]=w[e]}));var L={name:"resize",create:function(){var e=this;x(e,{resize:{resizeHandler:function(){e&&!e.destroyed&&e.initialized&&(e.emit("beforeResize"),e.emit("resize"))},orientationChangeHandler:function(){e&&!e.destroyed&&e.initialized&&e.emit("orientationchange")}}})},on:{init:function(e){var t=o();t.addEventListener("resize",e.resize.resizeHandler),t.addEventListener("orientationchange",e.resize.orientationChangeHandler)},destroy:function(e){var t=o();t.removeEventListener("resize",e.resize.resizeHandler),t.removeEventListener("orientationchange",e.resize.orientationChangeHandler)}}},z={attach:function(e,t){void 0===t&&(t={});var i=o(),s=this,a=new(i.MutationObserver||i.WebkitMutationObserver)((function(e){if(1!==e.length){var t=function(){s.emit("observerUpdate",e[0])};i.requestAnimationFrame?i.requestAnimationFrame(t):i.setTimeout(t,0)}else s.emit("observerUpdate",e[0])}));a.observe(e,{attributes:void 0===t.attributes||t.attributes,childList:void 0===t.childList||t.childList,characterData:void 0===t.characterData||t.characterData}),s.observer.observers.push(a)},init:function(){if(this.support.observer&&this.params.observer){if(this.params.observeParents)for(var e=this.$el.parents(),t=0;t<e.length;t+=1)this.observer.attach(e[t]);this.observer.attach(this.$el[0],{childList:this.params.observeSlideChildren}),this.observer.attach(this.$wrapperEl[0],{attributes:!1})}},destroy:function(){this.observer.observers.forEach((function(e){e.disconnect()})),this.observer.observers=[]}},O={name:"observer",params:{observer:!1,observeParents:!1,observeSlideChildren:!1},create:function(){E(this,{observer:t(t({},z),{},{observers:[]})})},on:{init:function(e){e.observer.init()},destroy:function(e){e.observer.destroy()}}};function I(e){var t=r(),i=o(),s=this.touchEventsData,a=this.params,n=this.touches;if(!this.animating||!a.preventInteractionOnTransition){var l=e;l.originalEvent&&(l=l.originalEvent);var d=m(l.target);if(("wrapper"!==a.touchEventsTarget||d.closest(this.wrapperEl).length)&&(s.isTouchEvent="touchstart"===l.type,(s.isTouchEvent||!("which"in l)||3!==l.which)&&!(!s.isTouchEvent&&"button"in l&&l.button>0||s.isTouched&&s.isMoved)))if(a.noSwiping&&d.closest(a.noSwipingSelector?a.noSwipingSelector:"."+a.noSwipingClass)[0])this.allowClick=!0;else if(!a.swipeHandler||d.closest(a.swipeHandler)[0]){n.currentX="touchstart"===l.type?l.targetTouches[0].pageX:l.pageX,n.currentY="touchstart"===l.type?l.targetTouches[0].pageY:l.pageY;var h=n.currentX,p=n.currentY,u=a.edgeSwipeDetection||a.iOSEdgeSwipeDetection,c=a.edgeSwipeThreshold||a.iOSEdgeSwipeThreshold;if(!u||!(h<=c||h>=i.screen.width-c)){if(x(s,{isTouched:!0,isMoved:!1,allowTouchCallbacks:!0,isScrolling:void 0,startMoving:void 0}),n.startX=h,n.startY=p,s.touchStartTime=T(),this.allowClick=!0,this.updateSize(),this.swipeDirection=void 0,a.threshold>0&&(s.allowThresholdMove=!1),"touchstart"!==l.type){var v=!0;d.is(s.formElements)&&(v=!1),t.activeElement&&m(t.activeElement).is(s.formElements)&&t.activeElement!==d[0]&&t.activeElement.blur();var f=v&&this.allowTouchMove&&a.touchStartPreventDefault;(a.touchStartForcePreventDefault||f)&&l.preventDefault()}this.emit("touchStart",l)}}}}function A(e){var t=r(),i=this.touchEventsData,s=this.params,a=this.touches,n=this.rtlTranslate,o=e;if(o.originalEvent&&(o=o.originalEvent),i.isTouched){if(!i.isTouchEvent||"touchmove"===o.type){var l="touchmove"===o.type&&o.targetTouches&&(o.targetTouches[0]||o.changedTouches[0]),d="touchmove"===o.type?l.pageX:o.pageX,h="touchmove"===o.type?l.pageY:o.pageY;if(o.preventedByNestedSwiper)return a.startX=d,void(a.startY=h);if(!this.allowTouchMove)return this.allowClick=!1,void(i.isTouched&&(x(a,{startX:d,startY:h,currentX:d,currentY:h}),i.touchStartTime=T()));if(i.isTouchEvent&&s.touchReleaseOnEdges&&!s.loop)if(this.isVertical()){if(h<a.startY&&this.translate<=this.maxTranslate()||h>a.startY&&this.translate>=this.minTranslate())return i.isTouched=!1,void(i.isMoved=!1)}else if(d<a.startX&&this.translate<=this.maxTranslate()||d>a.startX&&this.translate>=this.minTranslate())return;if(i.isTouchEvent&&t.activeElement&&o.target===t.activeElement&&m(o.target).is(i.formElements))return i.isMoved=!0,void(this.allowClick=!1);if(i.allowTouchCallbacks&&this.emit("touchMove",o),!(o.targetTouches&&o.targetTouches.length>1)){a.currentX=d,a.currentY=h;var p=a.currentX-a.startX,u=a.currentY-a.startY;if(!(this.params.threshold&&Math.sqrt(Math.pow(p,2)+Math.pow(u,2))<this.params.threshold)){var c;if(void 0===i.isScrolling)this.isHorizontal()&&a.currentY===a.startY||this.isVertical()&&a.currentX===a.startX?i.isScrolling=!1:p*p+u*u>=25&&(c=180*Math.atan2(Math.abs(u),Math.abs(p))/Math.PI,i.isScrolling=this.isHorizontal()?c>s.touchAngle:90-c>s.touchAngle);if(i.isScrolling&&this.emit("touchMoveOpposite",o),void 0===i.startMoving&&(a.currentX===a.startX&&a.currentY===a.startY||(i.startMoving=!0)),i.isScrolling)i.isTouched=!1;else if(i.startMoving){this.allowClick=!1,!s.cssMode&&o.cancelable&&o.preventDefault(),s.touchMoveStopPropagation&&!s.nested&&o.stopPropagation(),i.isMoved||(s.loop&&this.loopFix(),i.startTranslate=this.getTranslate(),this.setTransition(0),this.animating&&this.$wrapperEl.trigger("webkitTransitionEnd transitionend"),i.allowMomentumBounce=!1,!s.grabCursor||!0!==this.allowSlideNext&&!0!==this.allowSlidePrev||this.setGrabCursor(!0),this.emit("sliderFirstMove",o)),this.emit("sliderMove",o),i.isMoved=!0;var v=this.isHorizontal()?p:u;a.diff=v,v*=s.touchRatio,n&&(v=-v),this.swipeDirection=v>0?"prev":"next",i.currentTranslate=v+i.startTranslate;var f=!0,g=s.resistanceRatio;if(s.touchReleaseOnEdges&&(g=0),v>0&&i.currentTranslate>this.minTranslate()?(f=!1,s.resistance&&(i.currentTranslate=this.minTranslate()-1+Math.pow(-this.minTranslate()+i.startTranslate+v,g))):v<0&&i.currentTranslate<this.maxTranslate()&&(f=!1,s.resistance&&(i.currentTranslate=this.maxTranslate()+1-Math.pow(this.maxTranslate()-i.startTranslate-v,g))),f&&(o.preventedByNestedSwiper=!0),!this.allowSlideNext&&"next"===this.swipeDirection&&i.currentTranslate<i.startTranslate&&(i.currentTranslate=i.startTranslate),!this.allowSlidePrev&&"prev"===this.swipeDirection&&i.currentTranslate>i.startTranslate&&(i.currentTranslate=i.startTranslate),s.threshold>0){if(!(Math.abs(v)>s.threshold||i.allowThresholdMove))return void(i.currentTranslate=i.startTranslate);if(!i.allowThresholdMove)return i.allowThresholdMove=!0,a.startX=a.currentX,a.startY=a.currentY,i.currentTranslate=i.startTranslate,void(a.diff=this.isHorizontal()?a.currentX-a.startX:a.currentY-a.startY)}s.followFinger&&!s.cssMode&&((s.freeMode||s.watchSlidesProgress||s.watchSlidesVisibility)&&(this.updateActiveIndex(),this.updateSlidesClasses()),s.freeMode&&(0===i.velocities.length&&i.velocities.push({position:a[this.isHorizontal()?"startX":"startY"],time:i.touchStartTime}),i.velocities.push({position:a[this.isHorizontal()?"currentX":"currentY"],time:T()})),this.updateProgress(i.currentTranslate),this.setTranslate(i.currentTranslate))}}}}}else i.startMoving&&i.isScrolling&&this.emit("touchMoveOpposite",o)}function B(e){var t=this,i=t.touchEventsData,s=t.params,a=t.touches,r=t.rtlTranslate,n=t.$wrapperEl,o=t.slidesGrid,l=t.snapGrid,d=e;if(d.originalEvent&&(d=d.originalEvent),i.allowTouchCallbacks&&t.emit("touchEnd",d),i.allowTouchCallbacks=!1,!i.isTouched)return i.isMoved&&s.grabCursor&&t.setGrabCursor(!1),i.isMoved=!1,void(i.startMoving=!1);s.grabCursor&&i.isMoved&&i.isTouched&&(!0===t.allowSlideNext||!0===t.allowSlidePrev)&&t.setGrabCursor(!1);var h,p=T(),u=p-i.touchStartTime;if(t.allowClick&&(t.updateClickedSlide(d),t.emit("tap click",d),u<300&&p-i.lastClickTime<300&&t.emit("doubleTap doubleClick",d)),i.lastClickTime=T(),b((function(){t.destroyed||(t.allowClick=!0)})),!i.isTouched||!i.isMoved||!t.swipeDirection||0===a.diff||i.currentTranslate===i.startTranslate)return i.isTouched=!1,i.isMoved=!1,void(i.startMoving=!1);if(i.isTouched=!1,i.isMoved=!1,i.startMoving=!1,h=s.followFinger?r?t.translate:-t.translate:-i.currentTranslate,!s.cssMode)if(s.freeMode){if(h<-t.minTranslate())return void t.slideTo(t.activeIndex);if(h>-t.maxTranslate())return void(t.slides.length<l.length?t.slideTo(l.length-1):t.slideTo(t.slides.length-1));if(s.freeModeMomentum){if(i.velocities.length>1){var c=i.velocities.pop(),v=i.velocities.pop(),f=c.position-v.position,m=c.time-v.time;t.velocity=f/m,t.velocity/=2,Math.abs(t.velocity)<s.freeModeMinimumVelocity&&(t.velocity=0),(m>150||T()-c.time>300)&&(t.velocity=0)}else t.velocity=0;t.velocity*=s.freeModeMomentumVelocityRatio,i.velocities.length=0;var g=1e3*s.freeModeMomentumRatio,y=t.velocity*g,C=t.translate+y;r&&(C=-C);var w,S,x=!1,E=20*Math.abs(t.velocity)*s.freeModeMomentumBounceRatio;if(C<t.maxTranslate())s.freeModeMomentumBounce?(C+t.maxTranslate()<-E&&(C=t.maxTranslate()-E),w=t.maxTranslate(),x=!0,i.allowMomentumBounce=!0):C=t.maxTranslate(),s.loop&&s.centeredSlides&&(S=!0);else if(C>t.minTranslate())s.freeModeMomentumBounce?(C-t.minTranslate()>E&&(C=t.minTranslate()+E),w=t.minTranslate(),x=!0,i.allowMomentumBounce=!0):C=t.minTranslate(),s.loop&&s.centeredSlides&&(S=!0);else if(s.freeModeSticky){for(var M,P=0;P<l.length;P+=1)if(l[P]>-C){M=P;break}C=-(C=Math.abs(l[M]-C)<Math.abs(l[M-1]-C)||"next"===t.swipeDirection?l[M]:l[M-1])}if(S&&t.once("transitionEnd",(function(){t.loopFix()})),0!==t.velocity){if(g=r?Math.abs((-C-t.translate)/t.velocity):Math.abs((C-t.translate)/t.velocity),s.freeModeSticky){var k=Math.abs((r?-C:C)-t.translate),L=t.slidesSizesGrid[t.activeIndex];g=k<L?s.speed:k<2*L?1.5*s.speed:2.5*s.speed}}else if(s.freeModeSticky)return void t.slideToClosest();s.freeModeMomentumBounce&&x?(t.updateProgress(w),t.setTransition(g),t.setTranslate(C),t.transitionStart(!0,t.swipeDirection),t.animating=!0,n.transitionEnd((function(){t&&!t.destroyed&&i.allowMomentumBounce&&(t.emit("momentumBounce"),t.setTransition(s.speed),setTimeout((function(){t.setTranslate(w),n.transitionEnd((function(){t&&!t.destroyed&&t.transitionEnd()}))}),0))}))):t.velocity?(t.updateProgress(C),t.setTransition(g),t.setTranslate(C),t.transitionStart(!0,t.swipeDirection),t.animating||(t.animating=!0,n.transitionEnd((function(){t&&!t.destroyed&&t.transitionEnd()})))):t.updateProgress(C),t.updateActiveIndex(),t.updateSlidesClasses()}else if(s.freeModeSticky)return void t.slideToClosest();(!s.freeModeMomentum||u>=s.longSwipesMs)&&(t.updateProgress(),t.updateActiveIndex(),t.updateSlidesClasses())}else{for(var z=0,O=t.slidesSizesGrid[0],I=0;I<o.length;I+=I<s.slidesPerGroupSkip?1:s.slidesPerGroup){var A=I<s.slidesPerGroupSkip-1?1:s.slidesPerGroup;void 0!==o[I+A]?h>=o[I]&&h<o[I+A]&&(z=I,O=o[I+A]-o[I]):h>=o[I]&&(z=I,O=o[o.length-1]-o[o.length-2])}var B=(h-o[z])/O,D=z<s.slidesPerGroupSkip-1?1:s.slidesPerGroup;if(u>s.longSwipesMs){if(!s.longSwipes)return void t.slideTo(t.activeIndex);"next"===t.swipeDirection&&(B>=s.longSwipesRatio?t.slideTo(z+D):t.slideTo(z)),"prev"===t.swipeDirection&&(B>1-s.longSwipesRatio?t.slideTo(z+D):t.slideTo(z))}else{if(!s.shortSwipes)return void t.slideTo(t.activeIndex);t.navigation&&(d.target===t.navigation.nextEl||d.target===t.navigation.prevEl)?d.target===t.navigation.nextEl?t.slideTo(z+D):t.slideTo(z):("next"===t.swipeDirection&&t.slideTo(z+D),"prev"===t.swipeDirection&&t.slideTo(z))}}}function D(){var e=this.params,t=this.el;if(!t||0!==t.offsetWidth){e.breakpoints&&this.setBreakpoint();var i=this.allowSlideNext,s=this.allowSlidePrev,a=this.snapGrid;this.allowSlideNext=!0,this.allowSlidePrev=!0,this.updateSize(),this.updateSlides(),this.updateSlidesClasses(),("auto"===e.slidesPerView||e.slidesPerView>1)&&this.isEnd&&!this.isBeginning&&!this.params.centeredSlides?this.slideTo(this.slides.length-1,0,!1,!0):this.slideTo(this.activeIndex,0,!1,!0),this.autoplay&&this.autoplay.running&&this.autoplay.paused&&this.autoplay.run(),this.allowSlidePrev=s,this.allowSlideNext=i,this.params.watchOverflow&&a!==this.snapGrid&&this.checkOverflow()}}function G(e){this.allowClick||(this.params.preventClicks&&e.preventDefault(),this.params.preventClicksPropagation&&this.animating&&(e.stopPropagation(),e.stopImmediatePropagation()))}function N(){var e=this.wrapperEl,t=this.rtlTranslate;this.previousTranslate=this.translate,this.isHorizontal()?this.translate=t?e.scrollWidth-e.offsetWidth-e.scrollLeft:-e.scrollLeft:this.translate=-e.scrollTop,-0===this.translate&&(this.translate=0),this.updateActiveIndex(),this.updateSlidesClasses();var i=this.maxTranslate()-this.minTranslate();(0===i?0:(this.translate-this.minTranslate())/i)!==this.progress&&this.updateProgress(t?-this.translate:this.translate),this.emit("setTranslate",this.translate,!1)}var $=!1;function F(){}var V={init:!0,direction:"horizontal",touchEventsTarget:"container",initialSlide:0,speed:300,cssMode:!1,updateOnWindowResize:!0,width:null,height:null,preventInteractionOnTransition:!1,userAgent:null,url:null,edgeSwipeDetection:!1,edgeSwipeThreshold:20,freeMode:!1,freeModeMomentum:!0,freeModeMomentumRatio:1,freeModeMomentumBounce:!0,freeModeMomentumBounceRatio:1,freeModeMomentumVelocityRatio:1,freeModeSticky:!1,freeModeMinimumVelocity:.02,autoHeight:!1,setWrapperSize:!1,virtualTranslate:!1,effect:"slide",breakpoints:void 0,spaceBetween:0,slidesPerView:1,slidesPerColumn:1,slidesPerColumnFill:"column",slidesPerGroup:1,slidesPerGroupSkip:0,centeredSlides:!1,centeredSlidesBounds:!1,slidesOffsetBefore:0,slidesOffsetAfter:0,normalizeSlideIndex:!0,centerInsufficientSlides:!1,watchOverflow:!1,roundLengths:!1,touchRatio:1,touchAngle:45,simulateTouch:!0,shortSwipes:!0,longSwipes:!0,longSwipesRatio:.5,longSwipesMs:300,followFinger:!0,allowTouchMove:!0,threshold:0,touchMoveStopPropagation:!1,touchStartPreventDefault:!0,touchStartForcePreventDefault:!1,touchReleaseOnEdges:!1,uniqueNavElements:!0,resistance:!0,resistanceRatio:.85,watchSlidesProgress:!1,watchSlidesVisibility:!1,grabCursor:!1,preventClicks:!0,preventClicksPropagation:!0,slideToClickedSlide:!1,preloadImages:!0,updateOnImagesReady:!0,loop:!1,loopAdditionalSlides:0,loopedSlides:null,loopFillGroupWithBlank:!1,loopPreventsSlide:!0,allowSlidePrev:!0,allowSlideNext:!0,swipeHandler:null,noSwiping:!0,noSwipingClass:"swiper-no-swiping",noSwipingSelector:null,passiveListeners:!0,containerModifierClass:"swiper-container-",slideClass:"swiper-slide",slideBlankClass:"swiper-slide-invisible-blank",slideActiveClass:"swiper-slide-active",slideDuplicateActiveClass:"swiper-slide-duplicate-active",slideVisibleClass:"swiper-slide-visible",slideDuplicateClass:"swiper-slide-duplicate",slideNextClass:"swiper-slide-next",slideDuplicateNextClass:"swiper-slide-duplicate-next",slidePrevClass:"swiper-slide-prev",slideDuplicatePrevClass:"swiper-slide-duplicate-prev",wrapperClass:"swiper-wrapper",runCallbacksOnInit:!0,_emitClasses:!1},H={modular:{useParams:function(e){var t=this;t.modules&&Object.keys(t.modules).forEach((function(i){var s=t.modules[i];s.params&&x(e,s.params)}))},useModules:function(e){void 0===e&&(e={});var t=this;t.modules&&Object.keys(t.modules).forEach((function(i){var s=t.modules[i],a=e[i]||{};s.on&&t.on&&Object.keys(s.on).forEach((function(e){t.on(e,s.on[e])})),s.create&&s.create.bind(t)(a)}))}},eventsEmitter:{on:function(e,t,i){var s=this;if("function"!=typeof t)return s;var a=i?"unshift":"push";return e.split(" ").forEach((function(e){s.eventsListeners[e]||(s.eventsListeners[e]=[]),s.eventsListeners[e][a](t)})),s},once:function(e,t,i){var s=this;if("function"!=typeof t)return s;function a(){s.off(e,a),a.__emitterProxy&&delete a.__emitterProxy;for(var i=arguments.length,r=new Array(i),n=0;n<i;n++)r[n]=arguments[n];t.apply(s,r)}return a.__emitterProxy=t,s.on(e,a,i)},onAny:function(e,t){if("function"!=typeof e)return this;var i=t?"unshift":"push";return this.eventsAnyListeners.indexOf(e)<0&&this.eventsAnyListeners[i](e),this},offAny:function(e){if(!this.eventsAnyListeners)return this;var t=this.eventsAnyListeners.indexOf(e);return t>=0&&this.eventsAnyListeners.splice(t,1),this},off:function(e,t){var i=this;return i.eventsListeners?(e.split(" ").forEach((function(e){void 0===t?i.eventsListeners[e]=[]:i.eventsListeners[e]&&i.eventsListeners[e].forEach((function(s,a){(s===t||s.__emitterProxy&&s.__emitterProxy===t)&&i.eventsListeners[e].splice(a,1)}))})),i):i},emit:function(){var e,t,i,s=this;if(!s.eventsListeners)return s;for(var a=arguments.length,r=new Array(a),n=0;n<a;n++)r[n]=arguments[n];"string"==typeof r[0]||Array.isArray(r[0])?(e=r[0],t=r.slice(1,r.length),i=s):(e=r[0].events,t=r[0].data,i=r[0].context||s),t.unshift(i);var o=Array.isArray(e)?e:e.split(" ");return o.forEach((function(e){if(s.eventsAnyListeners&&s.eventsAnyListeners.length&&s.eventsAnyListeners.forEach((function(s){s.apply(i,[e].concat(t))})),s.eventsListeners&&s.eventsListeners[e]){var a=[];s.eventsListeners[e].forEach((function(e){a.push(e)})),a.forEach((function(e){e.apply(i,t)}))}})),s}},update:{updateSize:function(){var e,t,i=this.$el;e=void 0!==this.params.width&&null!==this.params.width?this.params.width:i[0].clientWidth,t=void 0!==this.params.height&&null!==this.params.width?this.params.height:i[0].clientHeight,0===e&&this.isHorizontal()||0===t&&this.isVertical()||(e=e-parseInt(i.css("padding-left")||0,10)-parseInt(i.css("padding-right")||0,10),t=t-parseInt(i.css("padding-top")||0,10)-parseInt(i.css("padding-bottom")||0,10),Number.isNaN(e)&&(e=0),Number.isNaN(t)&&(t=0),x(this,{width:e,height:t,size:this.isHorizontal()?e:t}))},updateSlides:function(){var e=o(),t=this.params,i=this.$wrapperEl,s=this.size,a=this.rtlTranslate,r=this.wrongRTL,n=this.virtual&&t.virtual.enabled,l=n?this.virtual.slides.length:this.slides.length,d=i.children("."+this.params.slideClass),h=n?this.virtual.slides.length:d.length,p=[],u=[],c=[];function v(e,i){return!t.cssMode||i!==d.length-1}var f=t.slidesOffsetBefore;"function"==typeof f&&(f=t.slidesOffsetBefore.call(this));var m=t.slidesOffsetAfter;"function"==typeof m&&(m=t.slidesOffsetAfter.call(this));var g=this.snapGrid.length,y=this.snapGrid.length,C=t.spaceBetween,w=-f,b=0,T=0;if(void 0!==s){var S,E;"string"==typeof C&&C.indexOf("%")>=0&&(C=parseFloat(C.replace("%",""))/100*s),this.virtualSize=-C,a?d.css({marginLeft:"",marginTop:""}):d.css({marginRight:"",marginBottom:""}),t.slidesPerColumn>1&&(S=Math.floor(h/t.slidesPerColumn)===h/this.params.slidesPerColumn?h:Math.ceil(h/t.slidesPerColumn)*t.slidesPerColumn,"auto"!==t.slidesPerView&&"row"===t.slidesPerColumnFill&&(S=Math.max(S,t.slidesPerView*t.slidesPerColumn)));for(var M,P=t.slidesPerColumn,k=S/P,L=Math.floor(h/t.slidesPerColumn),z=0;z<h;z+=1){E=0;var O=d.eq(z);if(t.slidesPerColumn>1){var I=void 0,A=void 0,B=void 0;if("row"===t.slidesPerColumnFill&&t.slidesPerGroup>1){var D=Math.floor(z/(t.slidesPerGroup*t.slidesPerColumn)),G=z-t.slidesPerColumn*t.slidesPerGroup*D,N=0===D?t.slidesPerGroup:Math.min(Math.ceil((h-D*P*t.slidesPerGroup)/P),t.slidesPerGroup);I=(A=G-(B=Math.floor(G/N))*N+D*t.slidesPerGroup)+B*S/P,O.css({"-webkit-box-ordinal-group":I,"-moz-box-ordinal-group":I,"-ms-flex-order":I,"-webkit-order":I,order:I})}else"column"===t.slidesPerColumnFill?(B=z-(A=Math.floor(z/P))*P,(A>L||A===L&&B===P-1)&&(B+=1)>=P&&(B=0,A+=1)):A=z-(B=Math.floor(z/k))*k;O.css("margin-"+(this.isHorizontal()?"top":"left"),0!==B&&t.spaceBetween&&t.spaceBetween+"px")}if("none"!==O.css("display")){if("auto"===t.slidesPerView){var $=e.getComputedStyle(O[0],null),F=O[0].style.transform,V=O[0].style.webkitTransform;if(F&&(O[0].style.transform="none"),V&&(O[0].style.webkitTransform="none"),t.roundLengths)E=this.isHorizontal()?O.outerWidth(!0):O.outerHeight(!0);else if(this.isHorizontal()){var H=parseFloat($.getPropertyValue("width")||0),j=parseFloat($.getPropertyValue("padding-left")||0),_=parseFloat($.getPropertyValue("padding-right")||0),W=parseFloat($.getPropertyValue("margin-left")||0),R=parseFloat($.getPropertyValue("margin-right")||0),q=$.getPropertyValue("box-sizing");E=q&&"border-box"===q?H+W+R:H+j+_+W+R}else{var X=parseFloat($.getPropertyValue("height")||0),Y=parseFloat($.getPropertyValue("padding-top")||0),U=parseFloat($.getPropertyValue("padding-bottom")||0),K=parseFloat($.getPropertyValue("margin-top")||0),J=parseFloat($.getPropertyValue("margin-bottom")||0),Q=$.getPropertyValue("box-sizing");E=Q&&"border-box"===Q?X+K+J:X+Y+U+K+J}F&&(O[0].style.transform=F),V&&(O[0].style.webkitTransform=V),t.roundLengths&&(E=Math.floor(E))}else E=(s-(t.slidesPerView-1)*C)/t.slidesPerView,t.roundLengths&&(E=Math.floor(E)),d[z]&&(this.isHorizontal()?d[z].style.width=E+"px":d[z].style.height=E+"px");d[z]&&(d[z].swiperSlideSize=E),c.push(E),t.centeredSlides?(w=w+E/2+b/2+C,0===b&&0!==z&&(w=w-s/2-C),0===z&&(w=w-s/2-C),Math.abs(w)<.001&&(w=0),t.roundLengths&&(w=Math.floor(w)),T%t.slidesPerGroup==0&&p.push(w),u.push(w)):(t.roundLengths&&(w=Math.floor(w)),(T-Math.min(this.params.slidesPerGroupSkip,T))%this.params.slidesPerGroup==0&&p.push(w),u.push(w),w=w+E+C),this.virtualSize+=E+C,b=E,T+=1}}if(this.virtualSize=Math.max(this.virtualSize,s)+m,a&&r&&("slide"===t.effect||"coverflow"===t.effect)&&i.css({width:this.virtualSize+t.spaceBetween+"px"}),t.setWrapperSize&&(this.isHorizontal()?i.css({width:this.virtualSize+t.spaceBetween+"px"}):i.css({height:this.virtualSize+t.spaceBetween+"px"})),t.slidesPerColumn>1&&(this.virtualSize=(E+t.spaceBetween)*S,this.virtualSize=Math.ceil(this.virtualSize/t.slidesPerColumn)-t.spaceBetween,this.isHorizontal()?i.css({width:this.virtualSize+t.spaceBetween+"px"}):i.css({height:this.virtualSize+t.spaceBetween+"px"}),t.centeredSlides)){M=[];for(var Z=0;Z<p.length;Z+=1){var ee=p[Z];t.roundLengths&&(ee=Math.floor(ee)),p[Z]<this.virtualSize+p[0]&&M.push(ee)}p=M}if(!t.centeredSlides){M=[];for(var te=0;te<p.length;te+=1){var ie=p[te];t.roundLengths&&(ie=Math.floor(ie)),p[te]<=this.virtualSize-s&&M.push(ie)}p=M,Math.floor(this.virtualSize-s)-Math.floor(p[p.length-1])>1&&p.push(this.virtualSize-s)}if(0===p.length&&(p=[0]),0!==t.spaceBetween&&(this.isHorizontal()?a?d.filter(v).css({marginLeft:C+"px"}):d.filter(v).css({marginRight:C+"px"}):d.filter(v).css({marginBottom:C+"px"})),t.centeredSlides&&t.centeredSlidesBounds){var se=0;c.forEach((function(e){se+=e+(t.spaceBetween?t.spaceBetween:0)}));var ae=(se-=t.spaceBetween)-s;p=p.map((function(e){return e<0?-f:e>ae?ae+m:e}))}if(t.centerInsufficientSlides){var re=0;if(c.forEach((function(e){re+=e+(t.spaceBetween?t.spaceBetween:0)})),(re-=t.spaceBetween)<s){var ne=(s-re)/2;p.forEach((function(e,t){p[t]=e-ne})),u.forEach((function(e,t){u[t]=e+ne}))}}x(this,{slides:d,snapGrid:p,slidesGrid:u,slidesSizesGrid:c}),h!==l&&this.emit("slidesLengthChange"),p.length!==g&&(this.params.watchOverflow&&this.checkOverflow(),this.emit("snapGridLengthChange")),u.length!==y&&this.emit("slidesGridLengthChange"),(t.watchSlidesProgress||t.watchSlidesVisibility)&&this.updateSlidesOffset()}},updateAutoHeight:function(e){var t,i=[],s=0;if("number"==typeof e?this.setTransition(e):!0===e&&this.setTransition(this.params.speed),"auto"!==this.params.slidesPerView&&this.params.slidesPerView>1)if(this.params.centeredSlides)this.visibleSlides.each((function(e){i.push(e)}));else for(t=0;t<Math.ceil(this.params.slidesPerView);t+=1){var a=this.activeIndex+t;if(a>this.slides.length)break;i.push(this.slides.eq(a)[0])}else i.push(this.slides.eq(this.activeIndex)[0]);for(t=0;t<i.length;t+=1)if(void 0!==i[t]){var r=i[t].offsetHeight;s=r>s?r:s}s&&this.$wrapperEl.css("height",s+"px")},updateSlidesOffset:function(){for(var e=this.slides,t=0;t<e.length;t+=1)e[t].swiperSlideOffset=this.isHorizontal()?e[t].offsetLeft:e[t].offsetTop},updateSlidesProgress:function(e){void 0===e&&(e=this&&this.translate||0);var t=this.params,i=this.slides,s=this.rtlTranslate;if(0!==i.length){void 0===i[0].swiperSlideOffset&&this.updateSlidesOffset();var a=-e;s&&(a=e),i.removeClass(t.slideVisibleClass),this.visibleSlidesIndexes=[],this.visibleSlides=[];for(var r=0;r<i.length;r+=1){var n=i[r],o=(a+(t.centeredSlides?this.minTranslate():0)-n.swiperSlideOffset)/(n.swiperSlideSize+t.spaceBetween);if(t.watchSlidesVisibility||t.centeredSlides&&t.autoHeight){var l=-(a-n.swiperSlideOffset),d=l+this.slidesSizesGrid[r];(l>=0&&l<this.size-1||d>1&&d<=this.size||l<=0&&d>=this.size)&&(this.visibleSlides.push(n),this.visibleSlidesIndexes.push(r),i.eq(r).addClass(t.slideVisibleClass))}n.progress=s?-o:o}this.visibleSlides=m(this.visibleSlides)}},updateProgress:function(e){if(void 0===e){var t=this.rtlTranslate?-1:1;e=this&&this.translate&&this.translate*t||0}var i=this.params,s=this.maxTranslate()-this.minTranslate(),a=this.progress,r=this.isBeginning,n=this.isEnd,o=r,l=n;0===s?(a=0,r=!0,n=!0):(r=(a=(e-this.minTranslate())/s)<=0,n=a>=1),x(this,{progress:a,isBeginning:r,isEnd:n}),(i.watchSlidesProgress||i.watchSlidesVisibility||i.centeredSlides&&i.autoHeight)&&this.updateSlidesProgress(e),r&&!o&&this.emit("reachBeginning toEdge"),n&&!l&&this.emit("reachEnd toEdge"),(o&&!r||l&&!n)&&this.emit("fromEdge"),this.emit("progress",a)},updateSlidesClasses:function(){var e,t=this.slides,i=this.params,s=this.$wrapperEl,a=this.activeIndex,r=this.realIndex,n=this.virtual&&i.virtual.enabled;t.removeClass(i.slideActiveClass+" "+i.slideNextClass+" "+i.slidePrevClass+" "+i.slideDuplicateActiveClass+" "+i.slideDuplicateNextClass+" "+i.slideDuplicatePrevClass),(e=n?this.$wrapperEl.find("."+i.slideClass+'[data-swiper-slide-index="'+a+'"]'):t.eq(a)).addClass(i.slideActiveClass),i.loop&&(e.hasClass(i.slideDuplicateClass)?s.children("."+i.slideClass+":not(."+i.slideDuplicateClass+')[data-swiper-slide-index="'+r+'"]').addClass(i.slideDuplicateActiveClass):s.children("."+i.slideClass+"."+i.slideDuplicateClass+'[data-swiper-slide-index="'+r+'"]').addClass(i.slideDuplicateActiveClass));var o=e.nextAll("."+i.slideClass).eq(0).addClass(i.slideNextClass);i.loop&&0===o.length&&(o=t.eq(0)).addClass(i.slideNextClass);var l=e.prevAll("."+i.slideClass).eq(0).addClass(i.slidePrevClass);i.loop&&0===l.length&&(l=t.eq(-1)).addClass(i.slidePrevClass),i.loop&&(o.hasClass(i.slideDuplicateClass)?s.children("."+i.slideClass+":not(."+i.slideDuplicateClass+')[data-swiper-slide-index="'+o.attr("data-swiper-slide-index")+'"]').addClass(i.slideDuplicateNextClass):s.children("."+i.slideClass+"."+i.slideDuplicateClass+'[data-swiper-slide-index="'+o.attr("data-swiper-slide-index")+'"]').addClass(i.slideDuplicateNextClass),l.hasClass(i.slideDuplicateClass)?s.children("."+i.slideClass+":not(."+i.slideDuplicateClass+')[data-swiper-slide-index="'+l.attr("data-swiper-slide-index")+'"]').addClass(i.slideDuplicatePrevClass):s.children("."+i.slideClass+"."+i.slideDuplicateClass+'[data-swiper-slide-index="'+l.attr("data-swiper-slide-index")+'"]').addClass(i.slideDuplicatePrevClass)),this.emitSlidesClasses()},updateActiveIndex:function(e){var t,i=this.rtlTranslate?this.translate:-this.translate,s=this.slidesGrid,a=this.snapGrid,r=this.params,n=this.activeIndex,o=this.realIndex,l=this.snapIndex,d=e;if(void 0===d){for(var h=0;h<s.length;h+=1)void 0!==s[h+1]?i>=s[h]&&i<s[h+1]-(s[h+1]-s[h])/2?d=h:i>=s[h]&&i<s[h+1]&&(d=h+1):i>=s[h]&&(d=h);r.normalizeSlideIndex&&(d<0||void 0===d)&&(d=0)}if(a.indexOf(i)>=0)t=a.indexOf(i);else{var p=Math.min(r.slidesPerGroupSkip,d);t=p+Math.floor((d-p)/r.slidesPerGroup)}if(t>=a.length&&(t=a.length-1),d!==n){var u=parseInt(this.slides.eq(d).attr("data-swiper-slide-index")||d,10);x(this,{snapIndex:t,realIndex:u,previousIndex:n,activeIndex:d}),this.emit("activeIndexChange"),this.emit("snapIndexChange"),o!==u&&this.emit("realIndexChange"),(this.initialized||this.params.runCallbacksOnInit)&&this.emit("slideChange")}else t!==l&&(this.snapIndex=t,this.emit("snapIndexChange"))},updateClickedSlide:function(e){var t=this.params,i=m(e.target).closest("."+t.slideClass)[0],s=!1;if(i)for(var a=0;a<this.slides.length;a+=1)this.slides[a]===i&&(s=!0);if(!i||!s)return this.clickedSlide=void 0,void(this.clickedIndex=void 0);this.clickedSlide=i,this.virtual&&this.params.virtual.enabled?this.clickedIndex=parseInt(m(i).attr("data-swiper-slide-index"),10):this.clickedIndex=m(i).index(),t.slideToClickedSlide&&void 0!==this.clickedIndex&&this.clickedIndex!==this.activeIndex&&this.slideToClickedSlide()}},translate:{getTranslate:function(e){void 0===e&&(e=this.isHorizontal()?"x":"y");var t=this.params,i=this.rtlTranslate,s=this.translate,a=this.$wrapperEl;if(t.virtualTranslate)return i?-s:s;if(t.cssMode)return s;var r=function(e,t){void 0===t&&(t="x");var i,s,a,r=o(),n=r.getComputedStyle(e,null);return r.WebKitCSSMatrix?((s=n.transform||n.webkitTransform).split(",").length>6&&(s=s.split(", ").map((function(e){return e.replace(",",".")})).join(", ")),a=new r.WebKitCSSMatrix("none"===s?"":s)):i=(a=n.MozTransform||n.OTransform||n.MsTransform||n.msTransform||n.transform||n.getPropertyValue("transform").replace("translate(","matrix(1, 0, 0, 1,")).toString().split(","),"x"===t&&(s=r.WebKitCSSMatrix?a.m41:16===i.length?parseFloat(i[12]):parseFloat(i[4])),"y"===t&&(s=r.WebKitCSSMatrix?a.m42:16===i.length?parseFloat(i[13]):parseFloat(i[5])),s||0}(a[0],e);return i&&(r=-r),r||0},setTranslate:function(e,t){var i=this.rtlTranslate,s=this.params,a=this.$wrapperEl,r=this.wrapperEl,n=this.progress,o=0,l=0;this.isHorizontal()?o=i?-e:e:l=e,s.roundLengths&&(o=Math.floor(o),l=Math.floor(l)),s.cssMode?r[this.isHorizontal()?"scrollLeft":"scrollTop"]=this.isHorizontal()?-o:-l:s.virtualTranslate||a.transform("translate3d("+o+"px, "+l+"px, 0px)"),this.previousTranslate=this.translate,this.translate=this.isHorizontal()?o:l;var d=this.maxTranslate()-this.minTranslate();(0===d?0:(e-this.minTranslate())/d)!==n&&this.updateProgress(e),this.emit("setTranslate",this.translate,t)},minTranslate:function(){return-this.snapGrid[0]},maxTranslate:function(){return-this.snapGrid[this.snapGrid.length-1]},translateTo:function(e,t,i,s,a){void 0===e&&(e=0),void 0===t&&(t=this.params.speed),void 0===i&&(i=!0),void 0===s&&(s=!0);var r=this,n=r.params,o=r.wrapperEl;if(r.animating&&n.preventInteractionOnTransition)return!1;var l,d=r.minTranslate(),h=r.maxTranslate();if(l=s&&e>d?d:s&&e<h?h:e,r.updateProgress(l),n.cssMode){var p,u=r.isHorizontal();if(0===t)o[u?"scrollLeft":"scrollTop"]=-l;else if(o.scrollTo)o.scrollTo(((p={})[u?"left":"top"]=-l,p.behavior="smooth",p));else o[u?"scrollLeft":"scrollTop"]=-l;return!0}return 0===t?(r.setTransition(0),r.setTranslate(l),i&&(r.emit("beforeTransitionStart",t,a),r.emit("transitionEnd"))):(r.setTransition(t),r.setTranslate(l),i&&(r.emit("beforeTransitionStart",t,a),r.emit("transitionStart")),r.animating||(r.animating=!0,r.onTranslateToWrapperTransitionEnd||(r.onTranslateToWrapperTransitionEnd=function(e){r&&!r.destroyed&&e.target===this&&(r.$wrapperEl[0].removeEventListener("transitionend",r.onTranslateToWrapperTransitionEnd),r.$wrapperEl[0].removeEventListener("webkitTransitionEnd",r.onTranslateToWrapperTransitionEnd),r.onTranslateToWrapperTransitionEnd=null,delete r.onTranslateToWrapperTransitionEnd,i&&r.emit("transitionEnd"))}),r.$wrapperEl[0].addEventListener("transitionend",r.onTranslateToWrapperTransitionEnd),r.$wrapperEl[0].addEventListener("webkitTransitionEnd",r.onTranslateToWrapperTransitionEnd))),!0}},transition:{setTransition:function(e,t){this.params.cssMode||this.$wrapperEl.transition(e),this.emit("setTransition",e,t)},transitionStart:function(e,t){void 0===e&&(e=!0);var i=this.activeIndex,s=this.params,a=this.previousIndex;if(!s.cssMode){s.autoHeight&&this.updateAutoHeight();var r=t;if(r||(r=i>a?"next":i<a?"prev":"reset"),this.emit("transitionStart"),e&&i!==a){if("reset"===r)return void this.emit("slideResetTransitionStart");this.emit("slideChangeTransitionStart"),"next"===r?this.emit("slideNextTransitionStart"):this.emit("slidePrevTransitionStart")}}},transitionEnd:function(e,t){void 0===e&&(e=!0);var i=this.activeIndex,s=this.previousIndex,a=this.params;if(this.animating=!1,!a.cssMode){this.setTransition(0);var r=t;if(r||(r=i>s?"next":i<s?"prev":"reset"),this.emit("transitionEnd"),e&&i!==s){if("reset"===r)return void this.emit("slideResetTransitionEnd");this.emit("slideChangeTransitionEnd"),"next"===r?this.emit("slideNextTransitionEnd"):this.emit("slidePrevTransitionEnd")}}}},slide:{slideTo:function(e,t,i,s){void 0===e&&(e=0),void 0===t&&(t=this.params.speed),void 0===i&&(i=!0);var a=this,r=e;r<0&&(r=0);var n=a.params,o=a.snapGrid,l=a.slidesGrid,d=a.previousIndex,h=a.activeIndex,p=a.rtlTranslate,u=a.wrapperEl;if(a.animating&&n.preventInteractionOnTransition)return!1;var c=Math.min(a.params.slidesPerGroupSkip,r),v=c+Math.floor((r-c)/a.params.slidesPerGroup);v>=o.length&&(v=o.length-1),(h||n.initialSlide||0)===(d||0)&&i&&a.emit("beforeSlideChangeStart");var f,m=-o[v];if(a.updateProgress(m),n.normalizeSlideIndex)for(var g=0;g<l.length;g+=1)-Math.floor(100*m)>=Math.floor(100*l[g])&&(r=g);if(a.initialized&&r!==h){if(!a.allowSlideNext&&m<a.translate&&m<a.minTranslate())return!1;if(!a.allowSlidePrev&&m>a.translate&&m>a.maxTranslate()&&(h||0)!==r)return!1}if(f=r>h?"next":r<h?"prev":"reset",p&&-m===a.translate||!p&&m===a.translate)return a.updateActiveIndex(r),n.autoHeight&&a.updateAutoHeight(),a.updateSlidesClasses(),"slide"!==n.effect&&a.setTranslate(m),"reset"!==f&&(a.transitionStart(i,f),a.transitionEnd(i,f)),!1;if(n.cssMode){var y,C=a.isHorizontal(),w=-m;if(p&&(w=u.scrollWidth-u.offsetWidth-w),0===t)u[C?"scrollLeft":"scrollTop"]=w;else if(u.scrollTo)u.scrollTo(((y={})[C?"left":"top"]=w,y.behavior="smooth",y));else u[C?"scrollLeft":"scrollTop"]=w;return!0}return 0===t?(a.setTransition(0),a.setTranslate(m),a.updateActiveIndex(r),a.updateSlidesClasses(),a.emit("beforeTransitionStart",t,s),a.transitionStart(i,f),a.transitionEnd(i,f)):(a.setTransition(t),a.setTranslate(m),a.updateActiveIndex(r),a.updateSlidesClasses(),a.emit("beforeTransitionStart",t,s),a.transitionStart(i,f),a.animating||(a.animating=!0,a.onSlideToWrapperTransitionEnd||(a.onSlideToWrapperTransitionEnd=function(e){a&&!a.destroyed&&e.target===this&&(a.$wrapperEl[0].removeEventListener("transitionend",a.onSlideToWrapperTransitionEnd),a.$wrapperEl[0].removeEventListener("webkitTransitionEnd",a.onSlideToWrapperTransitionEnd),a.onSlideToWrapperTransitionEnd=null,delete a.onSlideToWrapperTransitionEnd,a.transitionEnd(i,f))}),a.$wrapperEl[0].addEventListener("transitionend",a.onSlideToWrapperTransitionEnd),a.$wrapperEl[0].addEventListener("webkitTransitionEnd",a.onSlideToWrapperTransitionEnd))),!0},slideToLoop:function(e,t,i,s){void 0===e&&(e=0),void 0===t&&(t=this.params.speed),void 0===i&&(i=!0);var a=e;return this.params.loop&&(a+=this.loopedSlides),this.slideTo(a,t,i,s)},slideNext:function(e,t,i){void 0===e&&(e=this.params.speed),void 0===t&&(t=!0);var s=this.params,a=this.animating,r=this.activeIndex<s.slidesPerGroupSkip?1:s.slidesPerGroup;if(s.loop){if(a&&s.loopPreventsSlide)return!1;this.loopFix(),this._clientLeft=this.$wrapperEl[0].clientLeft}return this.slideTo(this.activeIndex+r,e,t,i)},slidePrev:function(e,t,i){void 0===e&&(e=this.params.speed),void 0===t&&(t=!0);var s=this.params,a=this.animating,r=this.snapGrid,n=this.slidesGrid,o=this.rtlTranslate;if(s.loop){if(a&&s.loopPreventsSlide)return!1;this.loopFix(),this._clientLeft=this.$wrapperEl[0].clientLeft}function l(e){return e<0?-Math.floor(Math.abs(e)):Math.floor(e)}var d,h=l(o?this.translate:-this.translate),p=r.map((function(e){return l(e)})),u=(r[p.indexOf(h)],r[p.indexOf(h)-1]);return void 0===u&&s.cssMode&&r.forEach((function(e){!u&&h>=e&&(u=e)})),void 0!==u&&(d=n.indexOf(u))<0&&(d=this.activeIndex-1),this.slideTo(d,e,t,i)},slideReset:function(e,t,i){return void 0===e&&(e=this.params.speed),void 0===t&&(t=!0),this.slideTo(this.activeIndex,e,t,i)},slideToClosest:function(e,t,i,s){void 0===e&&(e=this.params.speed),void 0===t&&(t=!0),void 0===s&&(s=.5);var a=this.activeIndex,r=Math.min(this.params.slidesPerGroupSkip,a),n=r+Math.floor((a-r)/this.params.slidesPerGroup),o=this.rtlTranslate?this.translate:-this.translate;if(o>=this.snapGrid[n]){var l=this.snapGrid[n];o-l>(this.snapGrid[n+1]-l)*s&&(a+=this.params.slidesPerGroup)}else{var d=this.snapGrid[n-1];o-d<=(this.snapGrid[n]-d)*s&&(a-=this.params.slidesPerGroup)}return a=Math.max(a,0),a=Math.min(a,this.slidesGrid.length-1),this.slideTo(a,e,t,i)},slideToClickedSlide:function(){var e,t=this,i=t.params,s=t.$wrapperEl,a="auto"===i.slidesPerView?t.slidesPerViewDynamic():i.slidesPerView,r=t.clickedIndex;if(i.loop){if(t.animating)return;e=parseInt(m(t.clickedSlide).attr("data-swiper-slide-index"),10),i.centeredSlides?r<t.loopedSlides-a/2||r>t.slides.length-t.loopedSlides+a/2?(t.loopFix(),r=s.children("."+i.slideClass+'[data-swiper-slide-index="'+e+'"]:not(.'+i.slideDuplicateClass+")").eq(0).index(),b((function(){t.slideTo(r)}))):t.slideTo(r):r>t.slides.length-a?(t.loopFix(),r=s.children("."+i.slideClass+'[data-swiper-slide-index="'+e+'"]:not(.'+i.slideDuplicateClass+")").eq(0).index(),b((function(){t.slideTo(r)}))):t.slideTo(r)}else t.slideTo(r)}},loop:{loopCreate:function(){var e=this,t=r(),i=e.params,s=e.$wrapperEl;s.children("."+i.slideClass+"."+i.slideDuplicateClass).remove();var a=s.children("."+i.slideClass);if(i.loopFillGroupWithBlank){var n=i.slidesPerGroup-a.length%i.slidesPerGroup;if(n!==i.slidesPerGroup){for(var o=0;o<n;o+=1){var l=m(t.createElement("div")).addClass(i.slideClass+" "+i.slideBlankClass);s.append(l)}a=s.children("."+i.slideClass)}}"auto"!==i.slidesPerView||i.loopedSlides||(i.loopedSlides=a.length),e.loopedSlides=Math.ceil(parseFloat(i.loopedSlides||i.slidesPerView,10)),e.loopedSlides+=i.loopAdditionalSlides,e.loopedSlides>a.length&&(e.loopedSlides=a.length);var d=[],h=[];a.each((function(t,i){var s=m(t);i<e.loopedSlides&&h.push(t),i<a.length&&i>=a.length-e.loopedSlides&&d.push(t),s.attr("data-swiper-slide-index",i)}));for(var p=0;p<h.length;p+=1)s.append(m(h[p].cloneNode(!0)).addClass(i.slideDuplicateClass));for(var u=d.length-1;u>=0;u-=1)s.prepend(m(d[u].cloneNode(!0)).addClass(i.slideDuplicateClass))},loopFix:function(){this.emit("beforeLoopFix");var e,t=this.activeIndex,i=this.slides,s=this.loopedSlides,a=this.allowSlidePrev,r=this.allowSlideNext,n=this.snapGrid,o=this.rtlTranslate;this.allowSlidePrev=!0,this.allowSlideNext=!0;var l=-n[t]-this.getTranslate();if(t<s)e=i.length-3*s+t,e+=s,this.slideTo(e,0,!1,!0)&&0!==l&&this.setTranslate((o?-this.translate:this.translate)-l);else if(t>=i.length-s){e=-i.length+t+s,e+=s,this.slideTo(e,0,!1,!0)&&0!==l&&this.setTranslate((o?-this.translate:this.translate)-l)}this.allowSlidePrev=a,this.allowSlideNext=r,this.emit("loopFix")},loopDestroy:function(){var e=this.$wrapperEl,t=this.params,i=this.slides;e.children("."+t.slideClass+"."+t.slideDuplicateClass+",."+t.slideClass+"."+t.slideBlankClass).remove(),i.removeAttr("data-swiper-slide-index")}},grabCursor:{setGrabCursor:function(e){if(!(this.support.touch||!this.params.simulateTouch||this.params.watchOverflow&&this.isLocked||this.params.cssMode)){var t=this.el;t.style.cursor="move",t.style.cursor=e?"-webkit-grabbing":"-webkit-grab",t.style.cursor=e?"-moz-grabbin":"-moz-grab",t.style.cursor=e?"grabbing":"grab"}},unsetGrabCursor:function(){this.support.touch||this.params.watchOverflow&&this.isLocked||this.params.cssMode||(this.el.style.cursor="")}},manipulation:{appendSlide:function(e){var t=this.$wrapperEl,i=this.params;if(i.loop&&this.loopDestroy(),"object"==typeof e&&"length"in e)for(var s=0;s<e.length;s+=1)e[s]&&t.append(e[s]);else t.append(e);i.loop&&this.loopCreate(),i.observer&&this.support.observer||this.update()},prependSlide:function(e){var t=this.params,i=this.$wrapperEl,s=this.activeIndex;t.loop&&this.loopDestroy();var a=s+1;if("object"==typeof e&&"length"in e){for(var r=0;r<e.length;r+=1)e[r]&&i.prepend(e[r]);a=s+e.length}else i.prepend(e);t.loop&&this.loopCreate(),t.observer&&this.support.observer||this.update(),this.slideTo(a,0,!1)},addSlide:function(e,t){var i=this.$wrapperEl,s=this.params,a=this.activeIndex;s.loop&&(a-=this.loopedSlides,this.loopDestroy(),this.slides=i.children("."+s.slideClass));var r=this.slides.length;if(e<=0)this.prependSlide(t);else if(e>=r)this.appendSlide(t);else{for(var n=a>e?a+1:a,o=[],l=r-1;l>=e;l-=1){var d=this.slides.eq(l);d.remove(),o.unshift(d)}if("object"==typeof t&&"length"in t){for(var h=0;h<t.length;h+=1)t[h]&&i.append(t[h]);n=a>e?a+t.length:a}else i.append(t);for(var p=0;p<o.length;p+=1)i.append(o[p]);s.loop&&this.loopCreate(),s.observer&&this.support.observer||this.update(),s.loop?this.slideTo(n+this.loopedSlides,0,!1):this.slideTo(n,0,!1)}},removeSlide:function(e){var t=this.params,i=this.$wrapperEl,s=this.activeIndex;t.loop&&(s-=this.loopedSlides,this.loopDestroy(),this.slides=i.children("."+t.slideClass));var a,r=s;if("object"==typeof e&&"length"in e){for(var n=0;n<e.length;n+=1)a=e[n],this.slides[a]&&this.slides.eq(a).remove(),a<r&&(r-=1);r=Math.max(r,0)}else a=e,this.slides[a]&&this.slides.eq(a).remove(),a<r&&(r-=1),r=Math.max(r,0);t.loop&&this.loopCreate(),t.observer&&this.support.observer||this.update(),t.loop?this.slideTo(r+this.loopedSlides,0,!1):this.slideTo(r,0,!1)},removeAllSlides:function(){for(var e=[],t=0;t<this.slides.length;t+=1)e.push(t);this.removeSlide(e)}},events:{attachEvents:function(){var e=r(),t=this.params,i=this.touchEvents,s=this.el,a=this.wrapperEl,n=this.device,o=this.support;this.onTouchStart=I.bind(this),this.onTouchMove=A.bind(this),this.onTouchEnd=B.bind(this),t.cssMode&&(this.onScroll=N.bind(this)),this.onClick=G.bind(this);var l=!!t.nested;if(!o.touch&&o.pointerEvents)s.addEventListener(i.start,this.onTouchStart,!1),e.addEventListener(i.move,this.onTouchMove,l),e.addEventListener(i.end,this.onTouchEnd,!1);else{if(o.touch){var d=!("touchstart"!==i.start||!o.passiveListener||!t.passiveListeners)&&{passive:!0,capture:!1};s.addEventListener(i.start,this.onTouchStart,d),s.addEventListener(i.move,this.onTouchMove,o.passiveListener?{passive:!1,capture:l}:l),s.addEventListener(i.end,this.onTouchEnd,d),i.cancel&&s.addEventListener(i.cancel,this.onTouchEnd,d),$||(e.addEventListener("touchstart",F),$=!0)}(t.simulateTouch&&!n.ios&&!n.android||t.simulateTouch&&!o.touch&&n.ios)&&(s.addEventListener("mousedown",this.onTouchStart,!1),e.addEventListener("mousemove",this.onTouchMove,l),e.addEventListener("mouseup",this.onTouchEnd,!1))}(t.preventClicks||t.preventClicksPropagation)&&s.addEventListener("click",this.onClick,!0),t.cssMode&&a.addEventListener("scroll",this.onScroll),t.updateOnWindowResize?this.on(n.ios||n.android?"resize orientationchange observerUpdate":"resize observerUpdate",D,!0):this.on("observerUpdate",D,!0)},detachEvents:function(){var e=r(),t=this.params,i=this.touchEvents,s=this.el,a=this.wrapperEl,n=this.device,o=this.support,l=!!t.nested;if(!o.touch&&o.pointerEvents)s.removeEventListener(i.start,this.onTouchStart,!1),e.removeEventListener(i.move,this.onTouchMove,l),e.removeEventListener(i.end,this.onTouchEnd,!1);else{if(o.touch){var d=!("onTouchStart"!==i.start||!o.passiveListener||!t.passiveListeners)&&{passive:!0,capture:!1};s.removeEventListener(i.start,this.onTouchStart,d),s.removeEventListener(i.move,this.onTouchMove,l),s.removeEventListener(i.end,this.onTouchEnd,d),i.cancel&&s.removeEventListener(i.cancel,this.onTouchEnd,d)}(t.simulateTouch&&!n.ios&&!n.android||t.simulateTouch&&!o.touch&&n.ios)&&(s.removeEventListener("mousedown",this.onTouchStart,!1),e.removeEventListener("mousemove",this.onTouchMove,l),e.removeEventListener("mouseup",this.onTouchEnd,!1))}(t.preventClicks||t.preventClicksPropagation)&&s.removeEventListener("click",this.onClick,!0),t.cssMode&&a.removeEventListener("scroll",this.onScroll),this.off(n.ios||n.android?"resize orientationchange observerUpdate":"resize observerUpdate",D)}},breakpoints:{setBreakpoint:function(){var e=this.activeIndex,t=this.initialized,i=this.loopedSlides,s=void 0===i?0:i,a=this.params,r=this.$el,n=a.breakpoints;if(n&&(!n||0!==Object.keys(n).length)){var o=this.getBreakpoint(n);if(o&&this.currentBreakpoint!==o){var l=o in n?n[o]:void 0;l&&["slidesPerView","spaceBetween","slidesPerGroup","slidesPerGroupSkip","slidesPerColumn"].forEach((function(e){var t=l[e];void 0!==t&&(l[e]="slidesPerView"!==e||"AUTO"!==t&&"auto"!==t?"slidesPerView"===e?parseFloat(t):parseInt(t,10):"auto")}));var d=l||this.originalParams,h=a.slidesPerColumn>1,p=d.slidesPerColumn>1;h&&!p?(r.removeClass(a.containerModifierClass+"multirow "+a.containerModifierClass+"multirow-column"),this.emitContainerClasses()):!h&&p&&(r.addClass(a.containerModifierClass+"multirow"),"column"===d.slidesPerColumnFill&&r.addClass(a.containerModifierClass+"multirow-column"),this.emitContainerClasses());var u=d.direction&&d.direction!==a.direction,c=a.loop&&(d.slidesPerView!==a.slidesPerView||u);u&&t&&this.changeDirection(),x(this.params,d),x(this,{allowTouchMove:this.params.allowTouchMove,allowSlideNext:this.params.allowSlideNext,allowSlidePrev:this.params.allowSlidePrev}),this.currentBreakpoint=o,this.emit("_beforeBreakpoint",d),c&&t&&(this.loopDestroy(),this.loopCreate(),this.updateSlides(),this.slideTo(e-s+this.loopedSlides,0,!1)),this.emit("breakpoint",d)}}},getBreakpoint:function(e){var t=o();if(e){var i=!1,s=Object.keys(e).map((function(e){if("string"==typeof e&&0===e.indexOf("@")){var i=parseFloat(e.substr(1));return{value:t.innerHeight*i,point:e}}return{value:e,point:e}}));s.sort((function(e,t){return parseInt(e.value,10)-parseInt(t.value,10)}));for(var a=0;a<s.length;a+=1){var r=s[a],n=r.point;r.value<=t.innerWidth&&(i=n)}return i||"max"}}},checkOverflow:{checkOverflow:function(){var e=this.params,t=this.isLocked,i=this.slides.length>0&&e.slidesOffsetBefore+e.spaceBetween*(this.slides.length-1)+this.slides[0].offsetWidth*this.slides.length;e.slidesOffsetBefore&&e.slidesOffsetAfter&&i?this.isLocked=i<=this.size:this.isLocked=1===this.snapGrid.length,this.allowSlideNext=!this.isLocked,this.allowSlidePrev=!this.isLocked,t!==this.isLocked&&this.emit(this.isLocked?"lock":"unlock"),t&&t!==this.isLocked&&(this.isEnd=!1,this.navigation&&this.navigation.update())}},classes:{addClasses:function(){var e=this.classNames,t=this.params,i=this.rtl,s=this.$el,a=this.device,r=[];r.push("initialized"),r.push(t.direction),t.freeMode&&r.push("free-mode"),t.autoHeight&&r.push("autoheight"),i&&r.push("rtl"),t.slidesPerColumn>1&&(r.push("multirow"),"column"===t.slidesPerColumnFill&&r.push("multirow-column")),a.android&&r.push("android"),a.ios&&r.push("ios"),t.cssMode&&r.push("css-mode"),r.forEach((function(i){e.push(t.containerModifierClass+i)})),s.addClass(e.join(" ")),this.emitContainerClasses()},removeClasses:function(){var e=this.$el,t=this.classNames;e.removeClass(t.join(" ")),this.emitContainerClasses()}},images:{loadImage:function(e,t,i,s,a,r){var n,l=o();function d(){r&&r()}m(e).parent("picture")[0]||e.complete&&a?d():t?((n=new l.Image).onload=d,n.onerror=d,s&&(n.sizes=s),i&&(n.srcset=i),t&&(n.src=t)):d()},preloadImages:function(){var e=this;function t(){null!=e&&e&&!e.destroyed&&(void 0!==e.imagesLoaded&&(e.imagesLoaded+=1),e.imagesLoaded===e.imagesToLoad.length&&(e.params.updateOnImagesReady&&e.update(),e.emit("imagesReady")))}e.imagesToLoad=e.$el.find("img");for(var i=0;i<e.imagesToLoad.length;i+=1){var s=e.imagesToLoad[i];e.loadImage(s,s.currentSrc||s.getAttribute("src"),s.srcset||s.getAttribute("srcset"),s.sizes||s.getAttribute("sizes"),!0,t)}}}},j={},_=function(){function t(){for(var e,i,s=arguments.length,a=new Array(s),r=0;r<s;r++)a[r]=arguments[r];1===a.length&&a[0].constructor&&a[0].constructor===Object?i=a[0]:(e=a[0],i=a[1]),i||(i={}),i=x({},i),e&&!i.el&&(i.el=e);var n=this;n.support=M(),n.device=P({userAgent:i.userAgent}),n.browser=k(),n.eventsListeners={},n.eventsAnyListeners=[],void 0===n.modules&&(n.modules={}),Object.keys(n.modules).forEach((function(e){var t=n.modules[e];if(t.params){var s=Object.keys(t.params)[0],a=t.params[s];if("object"!=typeof a||null===a)return;if(!(s in i)||!("enabled"in a))return;!0===i[s]&&(i[s]={enabled:!0}),"object"!=typeof i[s]||"enabled"in i[s]||(i[s].enabled=!0),i[s]||(i[s]={enabled:!1})}}));var o=x({},V);n.useParams(o),n.params=x({},o,j,i),n.originalParams=x({},n.params),n.passedParams=x({},i),n.params&&n.params.on&&Object.keys(n.params.on).forEach((function(e){n.on(e,n.params.on[e])})),n.params&&n.params.onAny&&n.onAny(n.params.onAny),n.$=m;var l=m(n.params.el);if(e=l[0]){if(l.length>1){var d=[];return l.each((function(e){var s=x({},i,{el:e});d.push(new t(s))})),d}var h,p,u;return e.swiper=n,e&&e.shadowRoot&&e.shadowRoot.querySelector?(h=m(e.shadowRoot.querySelector("."+n.params.wrapperClass))).children=function(e){return l.children(e)}:h=l.children("."+n.params.wrapperClass),x(n,{$el:l,el:e,$wrapperEl:h,wrapperEl:h[0],classNames:[],slides:m(),slidesGrid:[],snapGrid:[],slidesSizesGrid:[],isHorizontal:function(){return"horizontal"===n.params.direction},isVertical:function(){return"vertical"===n.params.direction},rtl:"rtl"===e.dir.toLowerCase()||"rtl"===l.css("direction"),rtlTranslate:"horizontal"===n.params.direction&&("rtl"===e.dir.toLowerCase()||"rtl"===l.css("direction")),wrongRTL:"-webkit-box"===h.css("display"),activeIndex:0,realIndex:0,isBeginning:!0,isEnd:!1,translate:0,previousTranslate:0,progress:0,velocity:0,animating:!1,allowSlideNext:n.params.allowSlideNext,allowSlidePrev:n.params.allowSlidePrev,touchEvents:(p=["touchstart","touchmove","touchend","touchcancel"],u=["mousedown","mousemove","mouseup"],n.support.pointerEvents&&(u=["pointerdown","pointermove","pointerup"]),n.touchEventsTouch={start:p[0],move:p[1],end:p[2],cancel:p[3]},n.touchEventsDesktop={start:u[0],move:u[1],end:u[2]},n.support.touch||!n.params.simulateTouch?n.touchEventsTouch:n.touchEventsDesktop),touchEventsData:{isTouched:void 0,isMoved:void 0,allowTouchCallbacks:void 0,touchStartTime:void 0,isScrolling:void 0,currentTranslate:void 0,startTranslate:void 0,allowThresholdMove:void 0,formElements:"input, select, option, textarea, button, video, label",lastClickTime:T(),clickTimeout:void 0,velocities:[],allowMomentumBounce:void 0,isTouchEvent:void 0,startMoving:void 0},allowClick:!0,allowTouchMove:n.params.allowTouchMove,touches:{startX:0,startY:0,currentX:0,currentY:0,diff:0},imagesToLoad:[],imagesLoaded:0}),n.useModules(),n.emit("_swiper"),n.params.init&&n.init(),n}}var i,s,a,r=t.prototype;return r.emitContainerClasses=function(){var e=this;if(e.params._emitClasses&&e.el){var t=e.el.className.split(" ").filter((function(t){return 0===t.indexOf("swiper-container")||0===t.indexOf(e.params.containerModifierClass)}));e.emit("_containerClasses",t.join(" "))}},r.emitSlidesClasses=function(){var e=this;e.params._emitClasses&&e.el&&e.slides.each((function(t){var i=t.className.split(" ").filter((function(t){return 0===t.indexOf("swiper-slide")||0===t.indexOf(e.params.slideClass)}));e.emit("_slideClass",t,i.join(" "))}))},r.slidesPerViewDynamic=function(){var e=this.params,t=this.slides,i=this.slidesGrid,s=this.size,a=this.activeIndex,r=1;if(e.centeredSlides){for(var n,o=t[a].swiperSlideSize,l=a+1;l<t.length;l+=1)t[l]&&!n&&(r+=1,(o+=t[l].swiperSlideSize)>s&&(n=!0));for(var d=a-1;d>=0;d-=1)t[d]&&!n&&(r+=1,(o+=t[d].swiperSlideSize)>s&&(n=!0))}else for(var h=a+1;h<t.length;h+=1)i[h]-i[a]<s&&(r+=1);return r},r.update=function(){var e=this;if(e&&!e.destroyed){var t=e.snapGrid,i=e.params;i.breakpoints&&e.setBreakpoint(),e.updateSize(),e.updateSlides(),e.updateProgress(),e.updateSlidesClasses(),e.params.freeMode?(s(),e.params.autoHeight&&e.updateAutoHeight()):(("auto"===e.params.slidesPerView||e.params.slidesPerView>1)&&e.isEnd&&!e.params.centeredSlides?e.slideTo(e.slides.length-1,0,!1,!0):e.slideTo(e.activeIndex,0,!1,!0))||s(),i.watchOverflow&&t!==e.snapGrid&&e.checkOverflow(),e.emit("update")}function s(){var t=e.rtlTranslate?-1*e.translate:e.translate,i=Math.min(Math.max(t,e.maxTranslate()),e.minTranslate());e.setTranslate(i),e.updateActiveIndex(),e.updateSlidesClasses()}},r.changeDirection=function(e,t){void 0===t&&(t=!0);var i=this.params.direction;return e||(e="horizontal"===i?"vertical":"horizontal"),e===i||"horizontal"!==e&&"vertical"!==e||(this.$el.removeClass(""+this.params.containerModifierClass+i).addClass(""+this.params.containerModifierClass+e),this.emitContainerClasses(),this.params.direction=e,this.slides.each((function(t){"vertical"===e?t.style.width="":t.style.height=""})),this.emit("changeDirection"),t&&this.update()),this},r.init=function(){this.initialized||(this.emit("beforeInit"),this.params.breakpoints&&this.setBreakpoint(),this.addClasses(),this.params.loop&&this.loopCreate(),this.updateSize(),this.updateSlides(),this.params.watchOverflow&&this.checkOverflow(),this.params.grabCursor&&this.setGrabCursor(),this.params.preloadImages&&this.preloadImages(),this.params.loop?this.slideTo(this.params.initialSlide+this.loopedSlides,0,this.params.runCallbacksOnInit):this.slideTo(this.params.initialSlide,0,this.params.runCallbacksOnInit),this.attachEvents(),this.initialized=!0,this.emit("init"),this.emit("afterInit"))},r.destroy=function(e,t){void 0===e&&(e=!0),void 0===t&&(t=!0);var i,s=this,a=s.params,r=s.$el,n=s.$wrapperEl,o=s.slides;return void 0===s.params||s.destroyed||(s.emit("beforeDestroy"),s.initialized=!1,s.detachEvents(),a.loop&&s.loopDestroy(),t&&(s.removeClasses(),r.removeAttr("style"),n.removeAttr("style"),o&&o.length&&o.removeClass([a.slideVisibleClass,a.slideActiveClass,a.slideNextClass,a.slidePrevClass].join(" ")).removeAttr("style").removeAttr("data-swiper-slide-index")),s.emit("destroy"),Object.keys(s.eventsListeners).forEach((function(e){s.off(e)})),!1!==e&&(s.$el[0].swiper=null,i=s,Object.keys(i).forEach((function(e){try{i[e]=null}catch(e){}try{delete i[e]}catch(e){}}))),s.destroyed=!0),null},t.extendDefaults=function(e){x(j,e)},t.installModule=function(e){t.prototype.modules||(t.prototype.modules={});var i=e.name||Object.keys(t.prototype.modules).length+"_"+T();t.prototype.modules[i]=e},t.use=function(e){return Array.isArray(e)?(e.forEach((function(e){return t.installModule(e)})),t):(t.installModule(e),t)},i=t,a=[{key:"extendedDefaults",get:function(){return j}},{key:"defaults",get:function(){return V}}],(s=null)&&e(i.prototype,s),a&&e(i,a),t}();Object.keys(H).forEach((function(e){Object.keys(H[e]).forEach((function(t){_.prototype[t]=H[e][t]}))})),_.use([L,O]);var W={update:function(){var e=this.params.navigation;if(!this.params.loop){var t=this.navigation,i=t.$nextEl,s=t.$prevEl;s&&s.length>0&&(this.isBeginning?s.addClass(e.disabledClass):s.removeClass(e.disabledClass),s[this.params.watchOverflow&&this.isLocked?"addClass":"removeClass"](e.lockClass)),i&&i.length>0&&(this.isEnd?i.addClass(e.disabledClass):i.removeClass(e.disabledClass),i[this.params.watchOverflow&&this.isLocked?"addClass":"removeClass"](e.lockClass))}},onPrevClick:function(e){e.preventDefault(),this.isBeginning&&!this.params.loop||this.slidePrev()},onNextClick:function(e){e.preventDefault(),this.isEnd&&!this.params.loop||this.slideNext()},init:function(){var e,t,i=this.params.navigation;(i.nextEl||i.prevEl)&&(i.nextEl&&(e=m(i.nextEl),this.params.uniqueNavElements&&"string"==typeof i.nextEl&&e.length>1&&1===this.$el.find(i.nextEl).length&&(e=this.$el.find(i.nextEl))),i.prevEl&&(t=m(i.prevEl),this.params.uniqueNavElements&&"string"==typeof i.prevEl&&t.length>1&&1===this.$el.find(i.prevEl).length&&(t=this.$el.find(i.prevEl))),e&&e.length>0&&e.on("click",this.navigation.onNextClick),t&&t.length>0&&t.on("click",this.navigation.onPrevClick),x(this.navigation,{$nextEl:e,nextEl:e&&e[0],$prevEl:t,prevEl:t&&t[0]}))},destroy:function(){var e=this.navigation,t=e.$nextEl,i=e.$prevEl;t&&t.length&&(t.off("click",this.navigation.onNextClick),t.removeClass(this.params.navigation.disabledClass)),i&&i.length&&(i.off("click",this.navigation.onPrevClick),i.removeClass(this.params.navigation.disabledClass))}},R={update:function(){var e=this.rtl,t=this.params.pagination;if(t.el&&this.pagination.el&&this.pagination.$el&&0!==this.pagination.$el.length){var i,s=this.virtual&&this.params.virtual.enabled?this.virtual.slides.length:this.slides.length,a=this.pagination.$el,r=this.params.loop?Math.ceil((s-2*this.loopedSlides)/this.params.slidesPerGroup):this.snapGrid.length;if(this.params.loop?((i=Math.ceil((this.activeIndex-this.loopedSlides)/this.params.slidesPerGroup))>s-1-2*this.loopedSlides&&(i-=s-2*this.loopedSlides),i>r-1&&(i-=r),i<0&&"bullets"!==this.params.paginationType&&(i=r+i)):i=void 0!==this.snapIndex?this.snapIndex:this.activeIndex||0,"bullets"===t.type&&this.pagination.bullets&&this.pagination.bullets.length>0){var n,o,l,d=this.pagination.bullets;if(t.dynamicBullets&&(this.pagination.bulletSize=d.eq(0)[this.isHorizontal()?"outerWidth":"outerHeight"](!0),a.css(this.isHorizontal()?"width":"height",this.pagination.bulletSize*(t.dynamicMainBullets+4)+"px"),t.dynamicMainBullets>1&&void 0!==this.previousIndex&&(this.pagination.dynamicBulletIndex+=i-this.previousIndex,this.pagination.dynamicBulletIndex>t.dynamicMainBullets-1?this.pagination.dynamicBulletIndex=t.dynamicMainBullets-1:this.pagination.dynamicBulletIndex<0&&(this.pagination.dynamicBulletIndex=0)),n=i-this.pagination.dynamicBulletIndex,l=((o=n+(Math.min(d.length,t.dynamicMainBullets)-1))+n)/2),d.removeClass(t.bulletActiveClass+" "+t.bulletActiveClass+"-next "+t.bulletActiveClass+"-next-next "+t.bulletActiveClass+"-prev "+t.bulletActiveClass+"-prev-prev "+t.bulletActiveClass+"-main"),a.length>1)d.each((function(e){var s=m(e),a=s.index();a===i&&s.addClass(t.bulletActiveClass),t.dynamicBullets&&(a>=n&&a<=o&&s.addClass(t.bulletActiveClass+"-main"),a===n&&s.prev().addClass(t.bulletActiveClass+"-prev").prev().addClass(t.bulletActiveClass+"-prev-prev"),a===o&&s.next().addClass(t.bulletActiveClass+"-next").next().addClass(t.bulletActiveClass+"-next-next"))}));else{var h=d.eq(i),p=h.index();if(h.addClass(t.bulletActiveClass),t.dynamicBullets){for(var u=d.eq(n),c=d.eq(o),v=n;v<=o;v+=1)d.eq(v).addClass(t.bulletActiveClass+"-main");if(this.params.loop)if(p>=d.length-t.dynamicMainBullets){for(var f=t.dynamicMainBullets;f>=0;f-=1)d.eq(d.length-f).addClass(t.bulletActiveClass+"-main");d.eq(d.length-t.dynamicMainBullets-1).addClass(t.bulletActiveClass+"-prev")}else u.prev().addClass(t.bulletActiveClass+"-prev").prev().addClass(t.bulletActiveClass+"-prev-prev"),c.next().addClass(t.bulletActiveClass+"-next").next().addClass(t.bulletActiveClass+"-next-next");else u.prev().addClass(t.bulletActiveClass+"-prev").prev().addClass(t.bulletActiveClass+"-prev-prev"),c.next().addClass(t.bulletActiveClass+"-next").next().addClass(t.bulletActiveClass+"-next-next")}}if(t.dynamicBullets){var g=Math.min(d.length,t.dynamicMainBullets+4),y=(this.pagination.bulletSize*g-this.pagination.bulletSize)/2-l*this.pagination.bulletSize,C=e?"right":"left";d.css(this.isHorizontal()?C:"top",y+"px")}}if("fraction"===t.type&&(a.find("."+t.currentClass).text(t.formatFractionCurrent(i+1)),a.find("."+t.totalClass).text(t.formatFractionTotal(r))),"progressbar"===t.type){var w;w=t.progressbarOpposite?this.isHorizontal()?"vertical":"horizontal":this.isHorizontal()?"horizontal":"vertical";var b=(i+1)/r,T=1,S=1;"horizontal"===w?T=b:S=b,a.find("."+t.progressbarFillClass).transform("translate3d(0,0,0) scaleX("+T+") scaleY("+S+")").transition(this.params.speed)}"custom"===t.type&&t.renderCustom?(a.html(t.renderCustom(this,i+1,r)),this.emit("paginationRender",a[0])):this.emit("paginationUpdate",a[0]),a[this.params.watchOverflow&&this.isLocked?"addClass":"removeClass"](t.lockClass)}},render:function(){var e=this.params.pagination;if(e.el&&this.pagination.el&&this.pagination.$el&&0!==this.pagination.$el.length){var t=this.virtual&&this.params.virtual.enabled?this.virtual.slides.length:this.slides.length,i=this.pagination.$el,s="";if("bullets"===e.type){for(var a=this.params.loop?Math.ceil((t-2*this.loopedSlides)/this.params.slidesPerGroup):this.snapGrid.length,r=0;r<a;r+=1)e.renderBullet?s+=e.renderBullet.call(this,r,e.bulletClass):s+="<"+e.bulletElement+' class="'+e.bulletClass+'"></'+e.bulletElement+">";i.html(s),this.pagination.bullets=i.find("."+e.bulletClass)}"fraction"===e.type&&(s=e.renderFraction?e.renderFraction.call(this,e.currentClass,e.totalClass):'<span class="'+e.currentClass+'"></span> / <span class="'+e.totalClass+'"></span>',i.html(s)),"progressbar"===e.type&&(s=e.renderProgressbar?e.renderProgressbar.call(this,e.progressbarFillClass):'<span class="'+e.progressbarFillClass+'"></span>',i.html(s)),"custom"!==e.type&&this.emit("paginationRender",this.pagination.$el[0])}},init:function(){var e=this,t=e.params.pagination;if(t.el){var i=m(t.el);0!==i.length&&(e.params.uniqueNavElements&&"string"==typeof t.el&&i.length>1&&(i=e.$el.find(t.el)),"bullets"===t.type&&t.clickable&&i.addClass(t.clickableClass),i.addClass(t.modifierClass+t.type),"bullets"===t.type&&t.dynamicBullets&&(i.addClass(""+t.modifierClass+t.type+"-dynamic"),e.pagination.dynamicBulletIndex=0,t.dynamicMainBullets<1&&(t.dynamicMainBullets=1)),"progressbar"===t.type&&t.progressbarOpposite&&i.addClass(t.progressbarOppositeClass),t.clickable&&i.on("click","."+t.bulletClass,(function(t){t.preventDefault();var i=m(this).index()*e.params.slidesPerGroup;e.params.loop&&(i+=e.loopedSlides),e.slideTo(i)})),x(e.pagination,{$el:i,el:i[0]}))}},destroy:function(){var e=this.params.pagination;if(e.el&&this.pagination.el&&this.pagination.$el&&0!==this.pagination.$el.length){var t=this.pagination.$el;t.removeClass(e.hiddenClass),t.removeClass(e.modifierClass+e.type),this.pagination.bullets&&this.pagination.bullets.removeClass(e.bulletActiveClass),e.clickable&&t.off("click","."+e.bulletClass)}}},q={loadInSlide:function(e,t){void 0===t&&(t=!0);var i=this,s=i.params.lazy;if(void 0!==e&&0!==i.slides.length){var a=i.virtual&&i.params.virtual.enabled?i.$wrapperEl.children("."+i.params.slideClass+'[data-swiper-slide-index="'+e+'"]'):i.slides.eq(e),r=a.find("."+s.elementClass+":not(."+s.loadedClass+"):not(."+s.loadingClass+")");!a.hasClass(s.elementClass)||a.hasClass(s.loadedClass)||a.hasClass(s.loadingClass)||r.push(a[0]),0!==r.length&&r.each((function(e){var r=m(e);r.addClass(s.loadingClass);var n=r.attr("data-background"),o=r.attr("data-src"),l=r.attr("data-srcset"),d=r.attr("data-sizes"),h=r.parent("picture");i.loadImage(r[0],o||n,l,d,!1,(function(){if(null!=i&&i&&(!i||i.params)&&!i.destroyed){if(n?(r.css("background-image",'url("'+n+'")'),r.removeAttr("data-background")):(l&&(r.attr("srcset",l),r.removeAttr("data-srcset")),d&&(r.attr("sizes",d),r.removeAttr("data-sizes")),h.length&&h.children("source").each((function(e){var t=m(e);t.attr("data-srcset")&&(t.attr("srcset",t.attr("data-srcset")),t.removeAttr("data-srcset"))})),o&&(r.attr("src",o),r.removeAttr("data-src"))),r.addClass(s.loadedClass).removeClass(s.loadingClass),a.find("."+s.preloaderClass).remove(),i.params.loop&&t){var e=a.attr("data-swiper-slide-index");if(a.hasClass(i.params.slideDuplicateClass)){var p=i.$wrapperEl.children('[data-swiper-slide-index="'+e+'"]:not(.'+i.params.slideDuplicateClass+")");i.lazy.loadInSlide(p.index(),!1)}else{var u=i.$wrapperEl.children("."+i.params.slideDuplicateClass+'[data-swiper-slide-index="'+e+'"]');i.lazy.loadInSlide(u.index(),!1)}}i.emit("lazyImageReady",a[0],r[0]),i.params.autoHeight&&i.updateAutoHeight()}})),i.emit("lazyImageLoad",a[0],r[0])}))}},load:function(){var e=this,t=e.$wrapperEl,i=e.params,s=e.slides,a=e.activeIndex,r=e.virtual&&i.virtual.enabled,n=i.lazy,o=i.slidesPerView;function l(e){if(r){if(t.children("."+i.slideClass+'[data-swiper-slide-index="'+e+'"]').length)return!0}else if(s[e])return!0;return!1}function d(e){return r?m(e).attr("data-swiper-slide-index"):m(e).index()}if("auto"===o&&(o=0),e.lazy.initialImageLoaded||(e.lazy.initialImageLoaded=!0),e.params.watchSlidesVisibility)t.children("."+i.slideVisibleClass).each((function(t){var i=r?m(t).attr("data-swiper-slide-index"):m(t).index();e.lazy.loadInSlide(i)}));else if(o>1)for(var h=a;h<a+o;h+=1)l(h)&&e.lazy.loadInSlide(h);else e.lazy.loadInSlide(a);if(n.loadPrevNext)if(o>1||n.loadPrevNextAmount&&n.loadPrevNextAmount>1){for(var p=n.loadPrevNextAmount,u=o,c=Math.min(a+u+Math.max(p,u),s.length),v=Math.max(a-Math.max(u,p),0),f=a+o;f<c;f+=1)l(f)&&e.lazy.loadInSlide(f);for(var g=v;g<a;g+=1)l(g)&&e.lazy.loadInSlide(g)}else{var y=t.children("."+i.slideNextClass);y.length>0&&e.lazy.loadInSlide(d(y));var C=t.children("."+i.slidePrevClass);C.length>0&&e.lazy.loadInSlide(d(C))}}},X={run:function(){var e=this,t=e.slides.eq(e.activeIndex),i=e.params.autoplay.delay;t.attr("data-swiper-autoplay")&&(i=t.attr("data-swiper-autoplay")||e.params.autoplay.delay),clearTimeout(e.autoplay.timeout),e.autoplay.timeout=b((function(){e.params.autoplay.reverseDirection?e.params.loop?(e.loopFix(),e.slidePrev(e.params.speed,!0,!0),e.emit("autoplay")):e.isBeginning?e.params.autoplay.stopOnLastSlide?e.autoplay.stop():(e.slideTo(e.slides.length-1,e.params.speed,!0,!0),e.emit("autoplay")):(e.slidePrev(e.params.speed,!0,!0),e.emit("autoplay")):e.params.loop?(e.loopFix(),e.slideNext(e.params.speed,!0,!0),e.emit("autoplay")):e.isEnd?e.params.autoplay.stopOnLastSlide?e.autoplay.stop():(e.slideTo(0,e.params.speed,!0,!0),e.emit("autoplay")):(e.slideNext(e.params.speed,!0,!0),e.emit("autoplay")),e.params.cssMode&&e.autoplay.running&&e.autoplay.run()}),i)},start:function(){return void 0===this.autoplay.timeout&&(!this.autoplay.running&&(this.autoplay.running=!0,this.emit("autoplayStart"),this.autoplay.run(),!0))},stop:function(){return!!this.autoplay.running&&(void 0!==this.autoplay.timeout&&(this.autoplay.timeout&&(clearTimeout(this.autoplay.timeout),this.autoplay.timeout=void 0),this.autoplay.running=!1,this.emit("autoplayStop"),!0))},pause:function(e){this.autoplay.running&&(this.autoplay.paused||(this.autoplay.timeout&&clearTimeout(this.autoplay.timeout),this.autoplay.paused=!0,0!==e&&this.params.autoplay.waitForTransition?(this.$wrapperEl[0].addEventListener("transitionend",this.autoplay.onTransitionEnd),this.$wrapperEl[0].addEventListener("webkitTransitionEnd",this.autoplay.onTransitionEnd)):(this.autoplay.paused=!1,this.autoplay.run())))},onVisibilityChange:function(){var e=r();"hidden"===e.visibilityState&&this.autoplay.running&&this.autoplay.pause(),"visible"===e.visibilityState&&this.autoplay.paused&&(this.autoplay.run(),this.autoplay.paused=!1)},onTransitionEnd:function(e){this&&!this.destroyed&&this.$wrapperEl&&e.target===this.$wrapperEl[0]&&(this.$wrapperEl[0].removeEventListener("transitionend",this.autoplay.onTransitionEnd),this.$wrapperEl[0].removeEventListener("webkitTransitionEnd",this.autoplay.onTransitionEnd),this.autoplay.paused=!1,this.autoplay.running?this.autoplay.run():this.autoplay.stop())}},Y={setTranslate:function(){for(var e=this.slides,t=0;t<e.length;t+=1){var i=this.slides.eq(t),s=-i[0].swiperSlideOffset;this.params.virtualTranslate||(s-=this.translate);var a=0;this.isHorizontal()||(a=s,s=0);var r=this.params.fadeEffect.crossFade?Math.max(1-Math.abs(i[0].progress),0):1+Math.min(Math.max(i[0].progress,-1),0);i.css({opacity:r}).transform("translate3d("+s+"px, "+a+"px, 0px)")}},setTransition:function(e){var t=this,i=t.slides,s=t.$wrapperEl;if(i.transition(e),t.params.virtualTranslate&&0!==e){var a=!1;i.transitionEnd((function(){if(!a&&t&&!t.destroyed){a=!0,t.animating=!1;for(var e=["webkitTransitionEnd","transitionend"],i=0;i<e.length;i+=1)s.trigger(e[i])}}))}}},U=[{name:"navigation",params:{navigation:{nextEl:null,prevEl:null,hideOnClick:!1,disabledClass:"swiper-button-disabled",hiddenClass:"swiper-button-hidden",lockClass:"swiper-button-lock"}},create:function(){E(this,{navigation:t({},W)})},on:{init:function(e){e.navigation.init(),e.navigation.update()},toEdge:function(e){e.navigation.update()},fromEdge:function(e){e.navigation.update()},destroy:function(e){e.navigation.destroy()},click:function(e,t){var i,s=e.navigation,a=s.$nextEl,r=s.$prevEl;!e.params.navigation.hideOnClick||m(t.target).is(r)||m(t.target).is(a)||(a?i=a.hasClass(e.params.navigation.hiddenClass):r&&(i=r.hasClass(e.params.navigation.hiddenClass)),!0===i?e.emit("navigationShow"):e.emit("navigationHide"),a&&a.toggleClass(e.params.navigation.hiddenClass),r&&r.toggleClass(e.params.navigation.hiddenClass))}}},{name:"pagination",params:{pagination:{el:null,bulletElement:"span",clickable:!1,hideOnClick:!1,renderBullet:null,renderProgressbar:null,renderFraction:null,renderCustom:null,progressbarOpposite:!1,type:"bullets",dynamicBullets:!1,dynamicMainBullets:1,formatFractionCurrent:function(e){return e},formatFractionTotal:function(e){return e},bulletClass:"swiper-pagination-bullet",bulletActiveClass:"swiper-pagination-bullet-active",modifierClass:"swiper-pagination-",currentClass:"swiper-pagination-current",totalClass:"swiper-pagination-total",hiddenClass:"swiper-pagination-hidden",progressbarFillClass:"swiper-pagination-progressbar-fill",progressbarOppositeClass:"swiper-pagination-progressbar-opposite",clickableClass:"swiper-pagination-clickable",lockClass:"swiper-pagination-lock"}},create:function(){E(this,{pagination:t({dynamicBulletIndex:0},R)})},on:{init:function(e){e.pagination.init(),e.pagination.render(),e.pagination.update()},activeIndexChange:function(e){(e.params.loop||void 0===e.snapIndex)&&e.pagination.update()},snapIndexChange:function(e){e.params.loop||e.pagination.update()},slidesLengthChange:function(e){e.params.loop&&(e.pagination.render(),e.pagination.update())},snapGridLengthChange:function(e){e.params.loop||(e.pagination.render(),e.pagination.update())},destroy:function(e){e.pagination.destroy()},click:function(e,t){e.params.pagination.el&&e.params.pagination.hideOnClick&&e.pagination.$el.length>0&&!m(t.target).hasClass(e.params.pagination.bulletClass)&&(!0===e.pagination.$el.hasClass(e.params.pagination.hiddenClass)?e.emit("paginationShow"):e.emit("paginationHide"),e.pagination.$el.toggleClass(e.params.pagination.hiddenClass))}}},{name:"lazy",params:{lazy:{enabled:!1,loadPrevNext:!1,loadPrevNextAmount:1,loadOnTransitionStart:!1,elementClass:"swiper-lazy",loadingClass:"swiper-lazy-loading",loadedClass:"swiper-lazy-loaded",preloaderClass:"swiper-lazy-preloader"}},create:function(){E(this,{lazy:t({initialImageLoaded:!1},q)})},on:{beforeInit:function(e){e.params.lazy.enabled&&e.params.preloadImages&&(e.params.preloadImages=!1)},init:function(e){e.params.lazy.enabled&&!e.params.loop&&0===e.params.initialSlide&&e.lazy.load()},scroll:function(e){e.params.freeMode&&!e.params.freeModeSticky&&e.lazy.load()},resize:function(e){e.params.lazy.enabled&&e.lazy.load()},scrollbarDragMove:function(e){e.params.lazy.enabled&&e.lazy.load()},transitionStart:function(e){e.params.lazy.enabled&&(e.params.lazy.loadOnTransitionStart||!e.params.lazy.loadOnTransitionStart&&!e.lazy.initialImageLoaded)&&e.lazy.load()},transitionEnd:function(e){e.params.lazy.enabled&&!e.params.lazy.loadOnTransitionStart&&e.lazy.load()},slideChange:function(e){e.params.lazy.enabled&&e.params.cssMode&&e.lazy.load()}}},{name:"autoplay",params:{autoplay:{enabled:!1,delay:3e3,waitForTransition:!0,disableOnInteraction:!0,stopOnLastSlide:!1,reverseDirection:!1}},create:function(){E(this,{autoplay:t(t({},X),{},{running:!1,paused:!1})})},on:{init:function(e){e.params.autoplay.enabled&&(e.autoplay.start(),r().addEventListener("visibilitychange",e.autoplay.onVisibilityChange))},beforeTransitionStart:function(e,t,i){e.autoplay.running&&(i||!e.params.autoplay.disableOnInteraction?e.autoplay.pause(t):e.autoplay.stop())},sliderFirstMove:function(e){e.autoplay.running&&(e.params.autoplay.disableOnInteraction?e.autoplay.stop():e.autoplay.pause())},touchEnd:function(e){e.params.cssMode&&e.autoplay.paused&&!e.params.autoplay.disableOnInteraction&&e.autoplay.run()},destroy:function(e){e.autoplay.running&&e.autoplay.stop(),r().removeEventListener("visibilitychange",e.autoplay.onVisibilityChange)}}},{name:"effect-fade",params:{fadeEffect:{crossFade:!1}},create:function(){E(this,{fadeEffect:t({},Y)})},on:{beforeInit:function(e){if("fade"===e.params.effect){e.classNames.push(e.params.containerModifierClass+"fade");var t={slidesPerView:1,slidesPerColumn:1,slidesPerGroup:1,watchSlidesProgress:!0,spaceBetween:0,virtualTranslate:!0};x(e.params,t),x(e.originalParams,t)}},setTranslate:function(e){"fade"===e.params.effect&&e.fadeEffect.setTranslate()},setTransition:function(e,t){"fade"===e.params.effect&&e.fadeEffect.setTransition(t)}}}];return _.use(U),_}));

function createSwiper(selector, swiperParams, callback = null) {
    /**
     * Use timer to create new task instead of executing in the current one
     * in order to split total blocking time
     */
    // Guard against double-init when createSwiper is invoked again before
    // the setTimeout-scheduled `new Swiper()` has actually run — callers
    // check `selector.swiper`, but that's only set once setTimeout fires.
    // Brand Editor's preview re-runs initSwipers on every morph, so rapid
    // edits can trigger two scheduled inits for the same container in one
    // tick.
    const isDomNode = selector && typeof selector === 'object';
    if (isDomNode && selector._swiperInit) return;
    if (isDomNode) selector._swiperInit = true;
    setTimeout(function() {
        try {
            const swiperInstance = new Swiper(selector, swiperParams);
            if (callback) {
                callback(swiperInstance);
            }
            if (window.RhinoMediaVisibility && swiperInstance.el && swiperInstance.autoplay) {
                let active = false;
                let resume = false;
                const autoplay = swiperInstance.autoplay;
                const dispose = window.RhinoMediaVisibility.observe(swiperInstance.el, function(visible) {
                    active = visible;
                    if (!visible) {
                        if (autoplay.running) resume = true;
                        autoplay.stop();
                    } else if (resume && !swiperInstance.el.contains(document.activeElement)) {
                        resume = false;
                        autoplay.start();
                    }
                }, { respectReducedMotion: true });
                swiperInstance.on('autoplayStart', function() {
                    Promise.resolve().then(function() {
                        if (!active && !swiperInstance.destroyed) { resume = true; autoplay.stop(); }
                    });
                });
                swiperInstance.on('destroy', dispose);
            }
        } finally {
            if (isDomNode) delete selector._swiperInit;
        }
    }, 0);
}
````

## Manifiesto interno v4 íntegro

- Ruta lógica: `manifest.json`
- Clasificación: manifiesto del paquete original
- SHA256 del origen: `1c5fd991f383aecc4fd60515d8906f36bbd2cfd7b1ee1d5c97de4b9d41632cb1`

````
{
  "kind": "rhino-hero-readonly-review-package-v4",
  "based_on_external_manifest_sha256": "33908cf593d8e327319746b13c7f9feed800a75adb0fb7999ebfa2874882b0ab",
  "candidate_files": {
    "sections/hero.tpl": "1e70c54c4c5bc38711272284843d8881c4354ac7725e9de56c0223b599c3e65d",
    "snippets/image.tpl": "e4e622e0c561c4450138e7717a1e5af95cf19d0184aee5cbcb89990f7ada767e"
  },
  "context_files": {
    "blocks/slide.tpl": "ab5e8d97095b36101fe5d4b66b7facbcdfdd87ab03458da5d909b00f9c868a64",
    "blocks/banner.tpl": "61bcb60817456a10177723b8a148b9027f130804b3245f1e5698d087d9de906c",
    "blocks/image.tpl": "ab10579daf74db55eb687b29641947cd67b3145b32a8b65cc7935018789d307f",
    "sections/hero-divided.tpl": "30a85e7b94e062889794463d9f2138dc69d58d620631631e2ab26b3a7f7cb487",
    "sections/category-hero.tpl": "ebde50d16b336c18aae56a1ab93817c22fa366c205a169671f453271051e304b",
    "layouts/layout.tpl": "aa0d59caa5947993a057fc13b4517057286a65a28e24029abb22b839cc18ba31",
    "static/js/libraries-standalone.js": "da2638c043034114cb004b2fd99cd4d54ee69c7d569bd2c96cca8e586d2e0d34"
  },
  "write_files": [],
  "reviewer_task_allowed_files": {
    "claude": [],
    "codex": []
  },
  "file_contract_version": 2,
  "files_sha256": {
    "candidate/sections/hero.tpl": "1e70c54c4c5bc38711272284843d8881c4354ac7725e9de56c0223b599c3e65d",
    "candidate/snippets/image.tpl": "e4e622e0c561c4450138e7717a1e5af95cf19d0184aee5cbcb89990f7ada767e",
    "candidate.patch": "ff73a41106aa153e30f0b84bf018ce89f80d693a68551eb39ab021ce1c09406b",
    "context/blocks/banner.tpl": "61bcb60817456a10177723b8a148b9027f130804b3245f1e5698d087d9de906c",
    "context/blocks/image.tpl": "ab10579daf74db55eb687b29641947cd67b3145b32a8b65cc7935018789d307f",
    "context/blocks/slide.tpl": "ab5e8d97095b36101fe5d4b66b7facbcdfdd87ab03458da5d909b00f9c868a64",
    "context/layouts/layout.tpl": "aa0d59caa5947993a057fc13b4517057286a65a28e24029abb22b839cc18ba31",
    "context/sections/category-hero.tpl": "ebde50d16b336c18aae56a1ab93817c22fa366c205a169671f453271051e304b",
    "context/sections/hero-divided.tpl": "30a85e7b94e062889794463d9f2138dc69d58d620631631e2ab26b3a7f7cb487",
    "context/static/js/libraries-standalone.js": "da2638c043034114cb004b2fd99cd4d54ee69c7d569bd2c96cca8e586d2e0d34",
    "reference/audit_controller_evidence_refs.py": "dc678eded5bbf4ebca4efeb9f3cfdddf713b524d53ff15abef2a83bb4856678f",
    "reference/controller-contract-v2-preflight.json": "23a233fabcf7a93aaac86e7c6fb77354564a56244f55248613222b55522b7a13",
    "reference/historical-reference-audit.json": "1cfbdbea2846c48d91591136e5a8fab9c7a45efa43490447dbd72e1eb5be4610",
    "reference/image-loading-contract.md": "0cdb4b384a3c2162173d46284d864d22e73128a96efe895d6ce2cd7b5e4f23fd",
    "reference/previous-claude-review.json": "b7b4eb9fdfa2c592e2cdd2d62452141e7ecb7f19f24b479164a453ba474a0c9c",
    "reference/previous-codex-receipt.json": "a7f6770a7572a7ea85864947c4e83ab4df887b1bbbfa3d561a117bb1859fcd19",
    "reference/prior-logical-preflight.json": "f27acf86f12a1c073cf1bf69fb752d77e7e115b88271381f78959af2d0a0f677",
    "reference/prior-preflight-findings.md": "7cc89f3a88cdf59df11cef8f94bd3976bb616b3514a3e368fccd1e84312d4510",
    "reference/read-only-review-package-v3-README.md": "85c8acba7c20fa67bc202ffe25b8f9fd069abbd152552be2996023a682134bbd",
    "reference/read-only-review-package-v3-external-manifest.json": "33908cf593d8e327319746b13c7f9feed800a75adb0fb7999ebfa2874882b0ab",
    "reference/read-only-review-package-v3-manifest.json": "acf8a927ed4dcae5ce7cba364ee606d5f6f4304554361f5720ff54f97a145c1e",
    "tests/controller-contract-focused-tests.json": "30f7315627cde6d6125dcf267dd4545fa75161d31fb76186fd69b14a8db999c6",
    "tests/controller-contract-focused-tests.log": "43c45bc8c3721bf3e6fa2c33302cdf9a191fede4b275ae65b0fdc6929ac5f54f",
    "tests/hero-responsive-fallback-results.json": "8779906519c499f55504e6d166f54f1040a3ae31e4f383f7484b2bce319fcc56",
    "tests/reproduction-results.json": "01ae1b2e0cd4a1240db9253e01a35c0db07af859c6447cdecf30a4348d59fe3f"
  },
  "candidate_diff_sha256": "ff73a41106aa153e30f0b84bf018ce89f80d693a68551eb39ab021ce1c09406b",
  "snapshot_read_files": [
    "sections/hero.tpl",
    "snippets/image.tpl",
    "blocks/slide.tpl",
    "blocks/banner.tpl",
    "blocks/image.tpl",
    "sections/hero-divided.tpl",
    "sections/category-hero.tpl",
    "layouts/layout.tpl",
    "static/js/libraries-standalone.js"
  ],
  "reviewer_tasks": [
    {
      "agent": "claude",
      "read_files": [
        "sections/hero.tpl",
        "snippets/image.tpl",
        "blocks/slide.tpl",
        "blocks/banner.tpl",
        "blocks/image.tpl",
        "sections/hero-divided.tpl",
        "sections/category-hero.tpl",
        "layouts/layout.tpl",
        "static/js/libraries-standalone.js"
      ],
      "allowed_files": []
    },
    {
      "agent": "codex",
      "read_files": [
        "sections/hero.tpl",
        "snippets/image.tpl",
        "blocks/slide.tpl",
        "blocks/banner.tpl",
        "blocks/image.tpl",
        "sections/hero-divided.tpl",
        "sections/category-hero.tpl",
        "layouts/layout.tpl",
        "static/js/libraries-standalone.js"
      ],
      "allowed_files": []
    }
  ],
  "source_bytes_total": 194145
}
````

## Manifiesto externo v4 íntegro

- Ruta lógica: `read-only-review-package-v4.manifest.json`
- Clasificación: manifiesto externo del paquete original
- SHA256 del origen: `d1d24d949e1455d9eb3b828d69532d70af0b9d8463531bc186d95954a9127a30`

````
{
  "kind": "rhino-hero-readonly-review-package-v4-external-manifest",
  "package_relative_path": "reports/rhino-performance/performance-html-js-20261117/candidate-d1d2-r1-r4/read-only-review-package-v4",
  "base_external_manifest_sha256": "33908cf593d8e327319746b13c7f9feed800a75adb0fb7999ebfa2874882b0ab",
  "files_sha256": {
    "README.md": "e9074c43f3788fe85d4f2860fd00722cd9c19335be41ad039ab68ea39f4ea353",
    "candidate/sections/hero.tpl": "1e70c54c4c5bc38711272284843d8881c4354ac7725e9de56c0223b599c3e65d",
    "candidate/snippets/image.tpl": "e4e622e0c561c4450138e7717a1e5af95cf19d0184aee5cbcb89990f7ada767e",
    "candidate.patch": "ff73a41106aa153e30f0b84bf018ce89f80d693a68551eb39ab021ce1c09406b",
    "context/blocks/banner.tpl": "61bcb60817456a10177723b8a148b9027f130804b3245f1e5698d087d9de906c",
    "context/blocks/image.tpl": "ab10579daf74db55eb687b29641947cd67b3145b32a8b65cc7935018789d307f",
    "context/blocks/slide.tpl": "ab5e8d97095b36101fe5d4b66b7facbcdfdd87ab03458da5d909b00f9c868a64",
    "context/layouts/layout.tpl": "aa0d59caa5947993a057fc13b4517057286a65a28e24029abb22b839cc18ba31",
    "context/sections/category-hero.tpl": "ebde50d16b336c18aae56a1ab93817c22fa366c205a169671f453271051e304b",
    "context/sections/hero-divided.tpl": "30a85e7b94e062889794463d9f2138dc69d58d620631631e2ab26b3a7f7cb487",
    "context/static/js/libraries-standalone.js": "da2638c043034114cb004b2fd99cd4d54ee69c7d569bd2c96cca8e586d2e0d34",
    "manifest.json": "1c5fd991f383aecc4fd60515d8906f36bbd2cfd7b1ee1d5c97de4b9d41632cb1",
    "reference/audit_controller_evidence_refs.py": "dc678eded5bbf4ebca4efeb9f3cfdddf713b524d53ff15abef2a83bb4856678f",
    "reference/controller-contract-v2-preflight.json": "23a233fabcf7a93aaac86e7c6fb77354564a56244f55248613222b55522b7a13",
    "reference/historical-reference-audit.json": "1cfbdbea2846c48d91591136e5a8fab9c7a45efa43490447dbd72e1eb5be4610",
    "reference/image-loading-contract.md": "0cdb4b384a3c2162173d46284d864d22e73128a96efe895d6ce2cd7b5e4f23fd",
    "reference/previous-claude-review.json": "b7b4eb9fdfa2c592e2cdd2d62452141e7ecb7f19f24b479164a453ba474a0c9c",
    "reference/previous-codex-receipt.json": "a7f6770a7572a7ea85864947c4e83ab4df887b1bbbfa3d561a117bb1859fcd19",
    "reference/prior-logical-preflight.json": "f27acf86f12a1c073cf1bf69fb752d77e7e115b88271381f78959af2d0a0f677",
    "reference/prior-preflight-findings.md": "7cc89f3a88cdf59df11cef8f94bd3976bb616b3514a3e368fccd1e84312d4510",
    "reference/read-only-review-package-v3-README.md": "85c8acba7c20fa67bc202ffe25b8f9fd069abbd152552be2996023a682134bbd",
    "reference/read-only-review-package-v3-external-manifest.json": "33908cf593d8e327319746b13c7f9feed800a75adb0fb7999ebfa2874882b0ab",
    "reference/read-only-review-package-v3-manifest.json": "acf8a927ed4dcae5ce7cba364ee606d5f6f4304554361f5720ff54f97a145c1e",
    "tests/controller-contract-focused-tests.json": "30f7315627cde6d6125dcf267dd4545fa75161d31fb76186fd69b14a8db999c6",
    "tests/controller-contract-focused-tests.log": "43c45bc8c3721bf3e6fa2c33302cdf9a191fede4b275ae65b0fdc6929ac5f54f",
    "tests/hero-responsive-fallback-results.json": "8779906519c499f55504e6d166f54f1040a3ae31e4f383f7484b2bce319fcc56",
    "tests/reproduction-results.json": "01ae1b2e0cd4a1240db9253e01a35c0db07af859c6447cdecf30a4348d59fe3f"
  },
  "provider_calls": false,
  "production_requests": false
}
````

## Índice SHA256 de las fuentes

Este índice permite comprobar la procedencia del contenido incorporado. `embedding_status` distingue contenido íntegro, campos/extractos exactos y archivos cuyo hash solo se conserva. Las evidencias auxiliares no necesarias (recibos del controlador, auditorías previas de contratos) quedan identificadas por hash, pero no se insertan. Los dos candidatos, diff, siete contextos, fixtures y manifiestos están incorporados íntegros; el contrato del helper está completo salvo una ruta local absoluta reemplazada; los recibos de producción y trazas se incluyen como extractos estructurados exactos. El harness suplementario solo se registra por hash porque contiene una ruta local absoluta.

## Índice de fuentes y hashes

- Clasificación: índice de verificación

````
[
  {
    "path_in_frozen_package": "candidate/sections/hero.tpl",
    "sha256": "1e70c54c4c5bc38711272284843d8881c4354ac7725e9de56c0223b599c3e65d",
    "embedding_status": "full"
  },
  {
    "path_in_frozen_package": "candidate/snippets/image.tpl",
    "sha256": "e4e622e0c561c4450138e7717a1e5af95cf19d0184aee5cbcb89990f7ada767e",
    "embedding_status": "full"
  },
  {
    "path_in_frozen_package": "candidate.patch",
    "sha256": "ff73a41106aa153e30f0b84bf018ce89f80d693a68551eb39ab021ce1c09406b",
    "embedding_status": "full"
  },
  {
    "path_in_frozen_package": "context/blocks/banner.tpl",
    "sha256": "61bcb60817456a10177723b8a148b9027f130804b3245f1e5698d087d9de906c",
    "embedding_status": "full"
  },
  {
    "path_in_frozen_package": "context/blocks/image.tpl",
    "sha256": "ab10579daf74db55eb687b29641947cd67b3145b32a8b65cc7935018789d307f",
    "embedding_status": "full"
  },
  {
    "path_in_frozen_package": "context/blocks/slide.tpl",
    "sha256": "ab5e8d97095b36101fe5d4b66b7facbcdfdd87ab03458da5d909b00f9c868a64",
    "embedding_status": "full"
  },
  {
    "path_in_frozen_package": "context/layouts/layout.tpl",
    "sha256": "aa0d59caa5947993a057fc13b4517057286a65a28e24029abb22b839cc18ba31",
    "embedding_status": "full"
  },
  {
    "path_in_frozen_package": "context/sections/category-hero.tpl",
    "sha256": "ebde50d16b336c18aae56a1ab93817c22fa366c205a169671f453271051e304b",
    "embedding_status": "full"
  },
  {
    "path_in_frozen_package": "context/sections/hero-divided.tpl",
    "sha256": "30a85e7b94e062889794463d9f2138dc69d58d620631631e2ab26b3a7f7cb487",
    "embedding_status": "full"
  },
  {
    "path_in_frozen_package": "context/static/js/libraries-standalone.js",
    "sha256": "da2638c043034114cb004b2fd99cd4d54ee69c7d569bd2c96cca8e586d2e0d34",
    "embedding_status": "full"
  },
  {
    "path_in_frozen_package": "reference/audit_controller_evidence_refs.py",
    "sha256": "dc678eded5bbf4ebca4efeb9f3cfdddf713b524d53ff15abef2a83bb4856678f",
    "embedding_status": "hash_only_not_embedded"
  },
  {
    "path_in_frozen_package": "reference/controller-contract-v2-preflight.json",
    "sha256": "23a233fabcf7a93aaac86e7c6fb77354564a56244f55248613222b55522b7a13",
    "embedding_status": "hash_only_not_embedded"
  },
  {
    "path_in_frozen_package": "reference/historical-reference-audit.json",
    "sha256": "1cfbdbea2846c48d91591136e5a8fab9c7a45efa43490447dbd72e1eb5be4610",
    "embedding_status": "hash_only_not_embedded"
  },
  {
    "path_in_frozen_package": "reference/image-loading-contract.md",
    "sha256": "0cdb4b384a3c2162173d46284d864d22e73128a96efe895d6ce2cd7b5e4f23fd",
    "embedding_status": "full"
  },
  {
    "path_in_frozen_package": "reference/previous-claude-review.json",
    "sha256": "b7b4eb9fdfa2c592e2cdd2d62452141e7ecb7f19f24b479164a453ba474a0c9c",
    "embedding_status": "selected_fields_only"
  },
  {
    "path_in_frozen_package": "reference/previous-codex-receipt.json",
    "sha256": "a7f6770a7572a7ea85864947c4e83ab4df887b1bbbfa3d561a117bb1859fcd19",
    "embedding_status": "hash_only_not_embedded"
  },
  {
    "path_in_frozen_package": "reference/prior-logical-preflight.json",
    "sha256": "f27acf86f12a1c073cf1bf69fb752d77e7e115b88271381f78959af2d0a0f677",
    "embedding_status": "hash_only_not_embedded"
  },
  {
    "path_in_frozen_package": "reference/prior-preflight-findings.md",
    "sha256": "7cc89f3a88cdf59df11cef8f94bd3976bb616b3514a3e368fccd1e84312d4510",
    "embedding_status": "hash_only_not_embedded"
  },
  {
    "path_in_frozen_package": "reference/read-only-review-package-v3-README.md",
    "sha256": "85c8acba7c20fa67bc202ffe25b8f9fd069abbd152552be2996023a682134bbd",
    "embedding_status": "hash_only_not_embedded"
  },
  {
    "path_in_frozen_package": "reference/read-only-review-package-v3-external-manifest.json",
    "sha256": "33908cf593d8e327319746b13c7f9feed800a75adb0fb7999ebfa2874882b0ab",
    "embedding_status": "selected_fields_only"
  },
  {
    "path_in_frozen_package": "reference/read-only-review-package-v3-manifest.json",
    "sha256": "acf8a927ed4dcae5ce7cba364ee606d5f6f4304554361f5720ff54f97a145c1e",
    "embedding_status": "hash_only_not_embedded"
  },
  {
    "path_in_frozen_package": "tests/controller-contract-focused-tests.json",
    "sha256": "30f7315627cde6d6125dcf267dd4545fa75161d31fb76186fd69b14a8db999c6",
    "embedding_status": "hash_only_not_embedded"
  },
  {
    "path_in_frozen_package": "tests/controller-contract-focused-tests.log",
    "sha256": "43c45bc8c3721bf3e6fa2c33302cdf9a191fede4b275ae65b0fdc6929ac5f54f",
    "embedding_status": "hash_only_not_embedded"
  },
  {
    "path_in_frozen_package": "tests/hero-responsive-fallback-results.json",
    "sha256": "8779906519c499f55504e6d166f54f1040a3ae31e4f383f7484b2bce319fcc56",
    "embedding_status": "full"
  },
  {
    "path_in_frozen_package": "tests/reproduction-results.json",
    "sha256": "01ae1b2e0cd4a1240db9253e01a35c0db07af859c6447cdecf30a4348d59fe3f",
    "embedding_status": "full"
  },
  {
    "path_in_workspace": "reports/runs/rhino-performance/20261117T-html-capture-authorized-03/desktop-analysis.json",
    "sha256": "2df8c69d91b186048b04f653c2bbf1b6f272fdeb277aabf74e9f14a47850049f",
    "embedding_status": "selected_exact_extract"
  },
  {
    "path_in_workspace": "reports/runs/rhino-performance/20261117T-html-capture-authorized-03/desktop-response-body.html",
    "sha256": "7da336fc86f03ba9d618000d3d4ea56125e2b1cc4957f8495a91b671f1852fc8",
    "embedding_status": "selected_exact_extract"
  },
  {
    "path_in_workspace": "reports/rhino-performance/performance-first-correction-20261113T180949/trace-findings.json",
    "sha256": "3df402f0d0153e45edb1a21d235607d3bf92b11a3d5085854a435e66d24458b1",
    "embedding_status": "selected_exact_extract"
  },
  {
    "path_in_workspace": "reports/rhino-performance/performance-first-correction-20261113T180949/lighthouse-ten-samples.csv",
    "sha256": "65690c16172b323225e71b76743c682682891fb00eb07080293c935dbcf921a7",
    "embedding_status": "full"
  },
  {
    "path_in_workspace": "reports/rhino-performance/performance-html-js-20261117/candidate-d1d2-r1-r4/tests/hero-responsive-fallbacks.browser.mjs",
    "sha256": "aa60ad6ea7807eec6d5e438f766320e6a00b99515f8574282b9ea76ddcea69e0",
    "embedding_status": "hash_only_not_embedded",
    "note": "contains an absolute local installation path; synthetic result JSON is embedded in full"
  }
]
````

## Límites y cuestiones pendientes de plataforma

1. Los resultados sintéticos verifican una tabla de decisión y markup modelado; no son render de Twig de Tiendanube.
2. `resolve_media` real, tipos de objeto, valores de `sourceUrl/srcSets`, y manejo de valores ausentes requieren validación nativa del renderer.
3. Descarga única, `currentSrc`, prioridad, LazySizes posterior, editor Ipanema, proporciones/CLS y accesibilidad real deben comprobarse en una validación autorizada antes de publicar.
4. No hay evidencia posterior al candidato en producción. Los datos de 17-11 son baseline histórico.
5. La fuente de test suplementaria y el resultado JSON se conservan, pero este ensamblado no ejecutó pruebas.
6. El estado sigue siendo `needs_evidence`; Claude y Codex aún deben emitir revisiones independientes del hash actual.
