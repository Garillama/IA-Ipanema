# Solicitud específica pendiente — lote 03 SEO V4

Esta solicitud no ejecuta ni autoriza red.

Se propone una única ejecución sobre `https://rhino-performance.com`, exclusivamente para las cinco URLs siguientes:

- https://rhino-performance.com/productos/tobillera-frio-y-calor/
- https://rhino-performance.com/productos/hombrera-frio-y-calor/
- https://rhino-performance.com/blog/posts/errores-comunes-al-usar-los-brazos-de-presoterapia-c80d6e476fb3/
- https://rhino-performance.com/blog/posts/lesiones-por-estres-sintomas-y-como-tratarlas-d080cbc403b8/
- https://rhino-performance.com/blog/posts/claves-para-potenciar-los-resultados-del-ejercicio-a823a76cbadd/

Manifiesto: [targets.json](batch-03/targets.json)

SHA256: `27375186058c9e953be9cd5e32a550864e852fa4fe49a38478b0b80db91b60be`

[Comando exacto propuesto](batch-03/command-NOT-AUTHORIZED.txt) y [argv/presupuesto](batch-03/operation.json). No modificar parámetros.

Máximo 12 GET incluidas consultas a robots.txt y redirecciones; concurrencia 1; frecuencia máxima 0,5/s o menor si robots lo exige; supervisor 120 s; timeout20 s; máximo2.000.000 bytes codificados/descomprimidos; tres redirecciones globales. Solo robots y los cinco destinos; sin home, sitemap, assets, Google o formularios comerciales.

Antes de invocar: comprobar manifiesto, URLs aún pendientes, origen, hashes de motor/transporte, ausencia de cambios ajenos y marcador de consumo único. Fallar de forma segura si no coinciden. Detener ante 403/429, robots desconocido o denegado, TLS/IP/origen/redirección inseguros, timeout, error crítico o presupuesto agotado. Conservar checkpoint, solicitudes inciertas y supervisor. No reintentar ni ejecutar el04 automáticamente. La autorización del03 no autoriza los demás lotes.
