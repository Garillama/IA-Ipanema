# Lote 12 SEO V4 — resultado de producción

Ejecución única autorizada el 13 de noviembre de 2026. Estado nativo: `complete_for_selected_scope`. Las cinco URLs son candidatas técnicamente indexables en el HTML observado; esto **no acredita indexación en Google**.

## Ejecución y seguridad

- Manifiesto SHA256: `4dee97f0cf689956cc97846145fc3cbd1d620b3153bbcb2bdf7c01411722b30d`. Se ejecutó el comando aprobado sin modificar parámetros. [Preflight](preflight.json) conserva argv, límites, hashes y pertenencia de las cinco URLs al inventario pendiente.
- **6 GET**: robots.txt y los cinco destinos; todos 200. Cero redirecciones, cero reintentos y ninguna visita adicional. [Registro de solicitudes](request-log.json).
- Tiempo supervisado: **14.224 s**, límite absoluto 120 s. Tiempo del rastreo registrado: 11.085 s. Concurrencia 1, frecuencia máxima 0,5/s, 12 GET máximos, timeout 20 s, cuerpos máximos 2.000.000 bytes, tres redirecciones globales.
- Supervisor `finished`, worker recogido (`worker_reaped=true`), 6 peticiones completadas, ninguna sin resultado confirmado o pendiente. No fue necesaria cancelación por plazo ni se repitió su prueba aislada. [Supervisor](supervision.json), [checkpoint](checkpoint.json).
- El encabezado histórico del checkpoint conserva `state: running` y `project: null`; no se interpreta como proceso vivo. El estado terminal consta en el supervisor y las seis peticiones están completadas. Se conserva el archivo original sin repararlo.
- No hubo cambios al motor, tema, menús, contenido, catálogo o canonicals; tampoco GSC, imágenes, CSS, JS, videos, home o sitemap. Los hashes de los cinco archivos integrados y sus dependencias siguen intactos.

## Resultados por URL

| # | URL / title observado | HTTP | Canonical | Caracteres en main | Errores / advertencias del validador |
|---|---|---:|---|---:|---:|
| 1 | [Comienza el año con energía](https://rhino-performance.com/blog/posts/comienza-el-ano-con-energia-9bb92d785569/) | 200 | Propio | 3135 | 0 / 2 |
| 2 | [Eleva tu experiencia deportiva.](https://rhino-performance.com/blog/posts/eleva-tu-experiencia-deportiva-37e67fbefb52/) | 200 | Propio | 3193 | 0 / 2 |
| 3 | [Cómo tener una gran semana pre-triatlón](https://rhino-performance.com/blog/posts/como-tener-una-gran-semana-pre-triatlon-7451956a975f/) | 200 | Propio | 3744 | 0 / 2 |
| 4 | [Presentamos la nueva RHINO PRO V3.0](https://rhino-performance.com/blog/posts/botas-presoterpia-rhino-pro-v3-032780da6369/) | 200 | Propio | 2804 | 0 / 2 |
| 5 | [Mejora tu práctica de yoga con la recuperación de las botas de presote](https://rhino-performance.com/blog/posts/mejora-tu-practica-de-yoga-con-la-recuperacion-de-las-botas-de-presoterapia-b40f7aab659b/) | 200 | Propio | 3758 | 0 / 2 |

Los cinco destinos permiten el agente de auditoría y Googlebot según robots.txt. No se observaron meta robots/googlebot ni X-Robots-Tag en sus respectivas fuentes. No se observaron flags noindex; el procesamiento de directivas está completo. Cada página contiene un H1 y main; ninguna fue marcada como candidata a soft 404. Title, H1 completos, canonical, headers y hashes del contenido figuran en [resultados por URL](per-url-results.json) y en [CSV](five-url-results.csv).

Robots.txt respondió 200. Conserva la advertencia de parseo de la línea 67 para el token de otro agente (`MJ12bot`), sin errores de parseo. El cuerpo histórico se reutiliza únicamente porque coincide su SHA256 con el cuerpo recibido ahora; no se hizo un segundo GET. [Procedencia de robots](robots-provenance.json).

## Datos estructurados: alertas sin ocultar ni sobrediagnosticar

Este lote contiene exclusivamente artículos. Las advertencias de productos de los lotes anteriores se conservan sin volver a analizarlas ni considerarlas resueltas.

Los cinco artículos presentan B030 y B100: el author extraído es texto sin entidad tipada. Es un hallazgo de marcado; la identidad editorial y el tipo Person/Organization requieren una fuente autorizada antes de corregirlo. No se ha observado un rechazo de Google.

El gate general conserva `insufficient_evidence` en los cinco artículos. No se fuerza su aprobación: la revisión contextual del schema y las capturas de navegación/contenido sin JS siguen pendientes. Esto es distinto del estado técnico `indexable_candidate`, que pasó HTTP, canonical y robots. [Interpretación y gates originales](findings-interpretation.json).

## Matriz incremental

- Inventario conservado: 125 URLs, 124 páginas HTML y un documento XML.
- HTML con comprobación HTTP individual: **104 → 109**.
- Pendientes: **20 → 15**, todas de artículos.
- Se actualizaron exactamente estas cinco filas; las otras 120, el grafo previo, las inspecciones GSC y las impresiones históricas se conservaron.
- Las diez URLs históricamente conocidas como indexadas no equivalen al total indexado del dominio. Este lote no consultó Google ni añade indexaciones conocidas.

[Matriz CSV](../../url-matrix.csv), [matriz JSON](../../url-matrix.json), [recibo de actualización y respaldos](matrix-update.json), [15 pendientes](pending-15.csv), [verificación posterior](verification.json).

## Evidencia y límites

[Informe nativo íntegro](raw-crawl-report.json), [salida CLI](cli-result.json), [checkpoint](checkpoint.json) y respaldos anteriores de ambas matrices están conservados. Fecha inicial de la ejecución: `2026-11-13T07:55:11.607982+00:00`; el intervalo hasta el fin de CLI se registra por URL. La fecha de template_audit corresponde al análisis, no a un timestamp de red individual.

El análisis usa HTML inicial y headers, no navegador renderizado ni prueba manual de teclado. El main se conserva como presencia, longitud y hash, no como certificación editorial. Los tamaños del registro son cuerpos HTTP observados, no peso completo de página, TLS ni medición PageSpeed. No se repitieron suites, piloto anterior ni consultas de Search Console. Se reutilizan las revisiones incrementales Claude/Codex del [paquete aprobado](../remaining-65-preparation/README.md); no se simula una revisión nueva posterior de proveedores.

## Estado final y pendientes

La autorización del lote12 está consumida. No se ejecutó ninguna solicitud después de finalizar el lote. Los lotes13–15 permanecen sin ejecutar y requieren autorizaciones específicas nuevas.

Quedan15 páginas pendientes, todas de artículos; los14 productos conocidos conservan su comprobación HTTP individual. [Lista de15 pendientes](pending-15.csv). Las advertencias de datos estructurados, la revisión contextual pendiente de lotes anteriores y la evidencia faltante de navegador siguen abiertas. No se modificó schema, contenido, tema ni motor. No se verificó indexación en Google.

El registro de planificación actualiza únicamente el12 a ejecutado. [Recibo del registro](registry-update.json). Los trece manifiestos, operaciones y comandos mantienen sus hashes originales; las120 filas no seleccionadas y todos los estados históricos de Google permanecen intactos tanto en CSV como en JSON. Los26 hashes aprobados de motor/transporte se verificaron también después de la ejecución.
