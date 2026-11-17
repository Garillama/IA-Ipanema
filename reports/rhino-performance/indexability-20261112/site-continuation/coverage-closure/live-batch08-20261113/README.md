# Lote 08 SEO V4 — resultado de producción

Ejecución única autorizada el 13 de noviembre de 2026. Estado nativo: `complete_for_selected_scope`. Las cinco URLs son candidatas técnicamente indexables en el HTML observado; esto **no acredita indexación en Google**.

## Ejecución y seguridad

- Manifiesto SHA256: `986a67b016b38be92718b35bc820b8cefc5fa10d310c66e462755e0c5f921f2c`. Se ejecutó el comando aprobado sin modificar parámetros. [Preflight](preflight.json) conserva argv, límites, hashes y pertenencia de las cinco URLs al inventario pendiente.
- **6 GET**: robots.txt y los cinco destinos; todos 200. Cero redirecciones, cero reintentos y ninguna visita adicional. [Registro de solicitudes](request-log.json).
- Tiempo supervisado: **14.021 s**, límite absoluto 120 s. Tiempo del rastreo registrado: 11.032 s. Concurrencia 1, frecuencia máxima 0,5/s, 12 GET máximos, timeout 20 s, cuerpos máximos 2.000.000 bytes, tres redirecciones globales.
- Supervisor `finished`, worker recogido (`worker_reaped=true`), 6 peticiones completadas, ninguna sin resultado confirmado o pendiente. No fue necesaria cancelación por plazo ni se repitió su prueba aislada. [Supervisor](supervision.json), [checkpoint](checkpoint.json).
- El encabezado histórico del checkpoint conserva `state: running` y `project: null`; no se interpreta como proceso vivo. El estado terminal consta en el supervisor y las seis peticiones están completadas. Se conserva el archivo original sin repararlo.
- No hubo cambios al motor, tema, menús, contenido, catálogo o canonicals; tampoco GSC, imágenes, CSS, JS, videos, home o sitemap. Los hashes de los cinco archivos integrados y sus dependencias siguen intactos.

## Resultados por URL

| # | URL / title observado | HTTP | Canonical | Caracteres en main | Errores / advertencias del validador |
|---|---|---:|---|---:|---:|
| 1 | [La inmovilidad es el verdadero deterioro](https://rhino-performance.com/blog/posts/la-inmovilidad-es-el-verdadero-deterioro-674a0d517ef4/) | 200 | Propio | 3777 | 0 / 2 |
| 2 | [RHINO GUN AIR: recuperación profunda, estés donde estés](https://rhino-performance.com/blog/posts/rhino-gun-air-recuperacion-profunda-estes-donde-estes-234790e68abf/) | 200 | Propio | 4216 | 0 / 2 |
| 3 | [NUEVOS PRODUCTOS RHINO AIR: recuperación profesional, donde sea y cuan](https://rhino-performance.com/blog/posts/nuevos-productos-rhino-air-recuperacion-profesional-donde-sea-y-cuando-sea-168c475f7bfa/) | 200 | Propio | 4452 | 0 / 2 |
| 4 | [Estás respirando mal (y está afectando tu rendimiento)](https://rhino-performance.com/blog/posts/estas-respirando-mal-y-esta-afectando-tu-rendimiento-75b8c1cc4493/) | 200 | Propio | 3532 | 0 / 2 |
| 5 | [Escalada y Recuperación: ¿Por Qué la Presoterapia es tu Mejor Aliada?](https://rhino-performance.com/blog/posts/escalada-y-recuperacion-por-que-la-presoterapia-es-tu-mejor-aliada-f9d767f0feda/) | 200 | Propio | 3786 | 0 / 2 |

Los cinco destinos permiten el agente de auditoría y Googlebot según robots.txt. No se observaron meta robots/googlebot ni X-Robots-Tag en sus respectivas fuentes. No se observaron flags noindex; el procesamiento de directivas está completo. Cada página contiene un H1 y main; ninguna fue marcada como candidata a soft 404. Title, H1 completos, canonical, headers y hashes del contenido figuran en [resultados por URL](per-url-results.json) y en [CSV](five-url-results.csv).

Robots.txt respondió 200. Conserva la advertencia de parseo de la línea 67 para el token de otro agente (`MJ12bot`), sin errores de parseo. El cuerpo histórico se reutiliza únicamente porque coincide su SHA256 con el cuerpo recibido ahora; no se hizo un segundo GET. [Procedencia de robots](robots-provenance.json).

## Datos estructurados: alertas sin ocultar ni sobrediagnosticar

Este lote contiene exclusivamente artículos. Las advertencias de productos de los lotes anteriores se conservan sin volver a analizarlas ni considerarlas resueltas.

Los cinco artículos presentan B030 y B100: el author extraído es texto sin entidad tipada. Es un hallazgo de marcado; la identidad editorial y el tipo Person/Organization requieren una fuente autorizada antes de corregirlo. No se ha observado un rechazo de Google.

El gate general conserva `insufficient_evidence` en los cinco artículos. No se fuerza su aprobación: la revisión contextual del schema y las capturas de navegación/contenido sin JS siguen pendientes. Esto es distinto del estado técnico `indexable_candidate`, que pasó HTTP, canonical y robots. [Interpretación y gates originales](findings-interpretation.json).

## Matriz incremental

- Inventario conservado: 125 URLs, 124 páginas HTML y un documento XML.
- HTML con comprobación HTTP individual: **84 → 89**.
- Pendientes: **40 → 35**, todas de artículos.
- Se actualizaron exactamente estas cinco filas; las otras 120, el grafo previo, las inspecciones GSC y las impresiones históricas se conservaron.
- Las diez URLs históricamente conocidas como indexadas no equivalen al total indexado del dominio. Este lote no consultó Google ni añade indexaciones conocidas.

[Matriz CSV](../../url-matrix.csv), [matriz JSON](../../url-matrix.json), [recibo de actualización y respaldos](matrix-update.json), [35 pendientes](pending-35.csv), [verificación posterior](verification.json).

## Evidencia y límites

[Informe nativo íntegro](raw-crawl-report.json), [salida CLI](cli-result.json), [checkpoint](checkpoint.json) y respaldos anteriores de ambas matrices están conservados. Fecha inicial de la ejecución: `2026-11-13T07:31:30.373655+00:00`; el intervalo hasta el fin de CLI se registra por URL. La fecha de template_audit corresponde al análisis, no a un timestamp de red individual.

El análisis usa HTML inicial y headers, no navegador renderizado ni prueba manual de teclado. El main se conserva como presencia, longitud y hash, no como certificación editorial. Los tamaños del registro son cuerpos HTTP observados, no peso completo de página, TLS ni medición PageSpeed. No se repitieron suites, piloto anterior ni consultas de Search Console. Se reutilizan las revisiones incrementales Claude/Codex del [paquete aprobado](../remaining-65-preparation/README.md); no se simula una revisión nueva posterior de proveedores.

## Estado final y pendientes

La autorización del lote08 está consumida. No se ejecutó ninguna solicitud después de finalizar el lote. Los lotes09–15 permanecen sin ejecutar y requieren autorizaciones específicas nuevas.

Quedan35 páginas pendientes, todas de artículos; los14 productos conocidos conservan su comprobación HTTP individual. [Lista de35 pendientes](pending-35.csv). Las advertencias de datos estructurados, la revisión contextual pendiente de lotes anteriores y la evidencia faltante de navegador siguen abiertas. No se modificó schema, contenido, tema ni motor. No se verificó indexación en Google.

El registro de planificación actualiza únicamente el08 a ejecutado. [Recibo del registro](registry-update.json). Los trece manifiestos, operaciones y comandos mantienen sus hashes originales; las120 filas no seleccionadas y todos los estados históricos de Google permanecen intactos tanto en CSV como en JSON. Los26 hashes aprobados de motor/transporte se verificaron también después de la ejecución.
