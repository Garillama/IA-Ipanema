# Lote 15 SEO V4 — resultado de producción

Ejecución única autorizada el 13 de noviembre de 2026. Estado nativo: `complete_for_selected_scope`. Las cinco URLs son candidatas técnicamente indexables en el HTML observado; esto **no acredita indexación en Google**.

## Ejecución y seguridad

- Manifiesto SHA256: `e6835d4f1804d59042172800306e8a38eb11b276572530d642c6f51a788b57eb`. Se ejecutó el comando aprobado sin modificar parámetros. [Preflight](preflight.json) conserva argv, límites, hashes y pertenencia de las cinco URLs al inventario pendiente.
- **6 GET**: robots.txt y los cinco destinos; todos 200. Cero redirecciones, cero reintentos y ninguna visita adicional. [Registro de solicitudes](request-log.json).
- Tiempo supervisado: **14.329 s**, límite absoluto 120 s. Tiempo del rastreo registrado: 11.249 s. Concurrencia 1, frecuencia máxima 0,5/s, 12 GET máximos, timeout 20 s, cuerpos máximos 2.000.000 bytes, tres redirecciones globales.
- Supervisor `finished`, worker recogido (`worker_reaped=true`), 6 peticiones completadas, ninguna sin resultado confirmado o pendiente. No fue necesaria cancelación por plazo ni se repitió su prueba aislada. [Supervisor](supervision.json), [checkpoint](checkpoint.json).
- El encabezado histórico del checkpoint conserva `state: running` y `project: null`; no se interpreta como proceso vivo. El estado terminal consta en el supervisor y las seis peticiones están completadas. Se conserva el archivo original sin repararlo.
- No hubo cambios al motor, tema, menús, contenido, catálogo o canonicals; tampoco GSC, imágenes, CSS, JS, videos, home o sitemap. Los hashes de los cinco archivos integrados y sus dependencias siguen intactos.

## Resultados por URL

| # | URL / title observado | HTTP | Canonical | Caracteres en main | Errores / advertencias del validador |
|---|---|---:|---|---:|---:|
| 1 | [Tina FríaTUB AIR: el aliado que tu cuerpo necesita después de entrenar](https://rhino-performance.com/blog/posts/tina-fratub-air-el-aliado-que-tu-cuerpo-necesita-despus-de-entrenar-b41c0ed3a1dd/) | 200 | Propio | 3595 | 0 / 2 |
| 2 | [¿Qué debes saber antes de de comprar unas botas de presoterapia?](https://rhino-performance.com/blog/posts/que-debes-saber-antes-de-de-comprar-unas-botas-de-presoterapia-f0d33d668783/) | 200 | Propio | 5936 | 0 / 2 |
| 3 | [Cómo mejorar la salud vascular con la presoterapia](https://rhino-performance.com/blog/posts/como-mejorar-la-salud-vascular-con-la-presoterapia-f919e9e6aae2/) | 200 | Propio | 5163 | 0 / 2 |
| 4 | [Mejora tu circulación y reduce la retención de líquidos con la presote](https://rhino-performance.com/blog/posts/mejora-tu-circulacion-y-reduce-la-retencion-de-liquidos-con-la-presoterapia-4aa13734ec51/) | 200 | Propio | 5057 | 0 / 2 |
| 5 | [Cómo la Presoterapia Puede Revolucionar tu Método Detox](https://rhino-performance.com/blog/posts/como-la-presoterapia-puede-revolucionar-tu-metodo-detox-0b0ae76ebe79/) | 200 | Propio | 4908 | 0 / 2 |

Los cinco destinos permiten el agente de auditoría y Googlebot según robots.txt. No se observaron meta robots/googlebot ni X-Robots-Tag en sus respectivas fuentes. No se observaron flags noindex; el procesamiento de directivas está completo. Cada página contiene un H1 y main; ninguna fue marcada como candidata a soft 404. Title, H1 completos, canonical, headers y hashes del contenido figuran en [resultados por URL](per-url-results.json) y en [CSV](five-url-results.csv).

Robots.txt respondió 200. Conserva la advertencia de parseo de la línea 67 para el token de otro agente (`MJ12bot`), sin errores de parseo. El cuerpo histórico se reutiliza únicamente porque coincide su SHA256 con el cuerpo recibido ahora; no se hizo un segundo GET. [Procedencia de robots](robots-provenance.json).

## Datos estructurados: alertas sin ocultar ni sobrediagnosticar

Este lote contiene exclusivamente artículos. Las advertencias de productos de los lotes anteriores se conservan sin volver a analizarlas ni considerarlas resueltas.

Los cinco artículos presentan B030 y B100: el author extraído es texto sin entidad tipada. Es un hallazgo de marcado; la identidad editorial y el tipo Person/Organization requieren una fuente autorizada antes de corregirlo. No se ha observado un rechazo de Google.

El gate general conserva `insufficient_evidence` en los cinco artículos. No se fuerza su aprobación: la revisión contextual del schema y las capturas de navegación/contenido sin JS siguen pendientes. Esto es distinto del estado técnico `indexable_candidate`, que pasó HTTP, canonical y robots. [Interpretación y gates originales](findings-interpretation.json).

## Matriz incremental

- Inventario conservado: 125 URLs, 124 páginas HTML y un documento XML.
- HTML con comprobación HTTP individual: **119 → 124**.
- Pendientes: **5 → 0**.
- Se actualizaron exactamente estas cinco filas; las otras 120, el grafo previo, las inspecciones GSC y las impresiones históricas se conservaron.
- Las diez URLs históricamente conocidas como indexadas no equivalen al total indexado del dominio. Este lote no consultó Google ni añade indexaciones conocidas.

[Matriz CSV](../../url-matrix.csv), [matriz JSON](../../url-matrix.json), [recibo de actualización y respaldos](matrix-update.json), [Lista de pendientes vacía](pending-0.csv), [verificación posterior](verification.json).

## Evidencia y límites

[Informe nativo íntegro](raw-crawl-report.json), [salida CLI](cli-result.json), [checkpoint](checkpoint.json) y respaldos anteriores de ambas matrices están conservados. Fecha inicial de la ejecución: `2026-11-13T08:07:45.929468+00:00`; el intervalo hasta el fin de CLI se registra por URL. La fecha de template_audit corresponde al análisis, no a un timestamp de red individual.

El análisis usa HTML inicial y headers, no navegador renderizado ni prueba manual de teclado. El main se conserva como presencia, longitud y hash, no como certificación editorial. Los tamaños del registro son cuerpos HTTP observados, no peso completo de página, TLS ni medición PageSpeed. No se repitieron suites, piloto anterior ni consultas de Search Console. Se reutilizan las revisiones incrementales Claude/Codex del [paquete aprobado](../remaining-65-preparation/README.md); no se simula una revisión nueva posterior de proveedores.

## Estado final y cierre de cobertura HTTP

La autorización del lote15 está consumida. No se ejecutó ninguna solicitud después de finalizarlo y no se autoriza ampliar el inventario ni repetir consultas.

Las124 páginas HTML conocidas tienen respuesta HTTP individual registrada. Quedan0 pendientes de ese control; los14 productos y86 artículos conocidos están incluidos. [Lista de pendientes vacía](pending-0.csv). Esto cierra cobertura HTTP, no todas las comprobaciones de renderizado ni la indexación en Google. Las advertencias de schema y las condiciones de evidencia pendientes se mantienen.

El registro actualiza únicamente el15 a ejecutado. [Recibo](registry-update.json). Los trece manifiestos y comandos preparados conservan sus hashes; las120 filas no seleccionadas y los estados históricos de Google permanecen intactos en CSV y JSON. Los26 hashes aprobados de motor/transporte se verificaron también después del lote.

[Informe consolidado de toda la auditoría](../consolidated-20261113/README.md).
