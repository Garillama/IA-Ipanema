# RHINO — Home integrada automáticamente con Sectionfy

Estado: **aplicado y aceptado localmente, sin publicación**. Fecha:2026-11-11T20:19:39.525241+00:00.

Se comprobó la ruta real proporcionada por el propietario, `https://sectionfy.codefy-apps.com/api/public/content/{token}/home-page`: HTTP200 y un banner publicado con MP4 listo. El token público existente se reutiliza; no se escribe su valor en informes ni en Git. No hace falta pegar una URL en el editor de Home.

El banner principal `video_1790516939240` está configurado localmente en modo `sectionfy_video`. La fuente automática de Inicio vive en el cliente compartido. Los slides de Home pueden usar la misma fuente; el campo de URL queda opcional para sobrescribirla o para otras páginas. Se conserva la portada, beneficios, controles, contenidos y el resto de los ajustes de Home. No se modificó manifest.json ni la PDP en este lote. No hubo push, watch, publish ni modificación de la aplicación.

## Verificación

Claude aprobó el delta acotado. Pasaron **199 comprobaciones funcionales posteriores**:155 de navegador con API/media simulados,38 del cliente offline y6 de API/archivo real en un iframe temporal desde el origen público de Home. El recibo añade10 comprobaciones de hashes/archivos protegidos:209checks. La transacción `827e410704fc48b8be9c7753e17c294b` quedó aceptada con backups privados y hashes. El caso nuevo de fuente automática fallaba antes y pasa después; la evidencia anterior se conservó.

Se reprodujo el archivo real a1920×1080 y se verificó Play/Pause por teclado. Esa prueba del archivo no equivale a validar el render Twig completo del Home publicado. No se declara mejora global de PageSpeed ni90+.

## Rendimiento

En la prueba móvil, el componente realizó **0 solicitudes de MP4 antes de Play**, medido en las respuestas de red del iframe auditado. La foto permanece disponible mientras llega la API. No se inicializa YouTube/Vimeo para este banner cuando usa el archivo de Sectionfy. Continúan las pausas por visibilidad y pestaña oculta y el respeto a ahorro de datos/movimiento reducido.

El MP4 actual dura20,42s y su tamaño total informado por Content-Range es **7.688.530bytes (7,69MB)**. Es tamaño del archivo, no total transferido en todas las pruebas. Su optimización queda para un lote posterior; no se cambió ni re-subió el archivo de la app. La API publica cabeceras de caché compartida de60s y stale-while-revalidate60s: una actualización puede no reflejarse inmediatamente.

## Archivos de este lote

- static/js/sectionfy-client.js: ruta Home automática y host documentado explícito; se conservan validaciones, timeout y compatibilidad PDP.
- sections/video.tpl y blocks/slide.tpl: identificación de la página Home para resolver la fuente.
- sections/slideshow.tpl: ayuda del campo avanzado de origen, ahora opcional en Inicio.
- templates/pages/home.json: únicamente ajustes de fuente del banner principal; resto de contenido intacto.

La implementación está en `~/Escritorio/Cli/Rhino-Ipanema`. El propietario mantiene el control de publicación. Revisar el Home desplegado después de actualizar el tema antes de atribuir cambios de velocidad o declarar cierre visual.

[Consulta real](../runs/rhino-performance/20261111T195618-sectionfy-home-page-source-8ab8e843/request-observation.json) · [Revisión](../runs/rhino-performance/20261111T195618-sectionfy-home-page-source-8ab8e843/independent-review.json) · [QA posterior](../runs/rhino-performance/20261111T195618-sectionfy-home-page-source-8ab8e843/accepted-local-QA.json) · [Video real/red](../runs/rhino-performance/20261111T195618-sectionfy-home-page-source-8ab8e843/live-playback-after-apply.json) · [Aceptación](../runs/rhino-performance/20261111T195618-sectionfy-home-page-source-8ab8e843/acceptance.json).
