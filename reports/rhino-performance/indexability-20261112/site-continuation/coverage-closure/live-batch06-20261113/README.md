# Lote 06 SEO V4 — resultado de producción

Ejecución única autorizada el 13 de noviembre de 2026. Estado nativo: `complete_for_selected_scope`. Las cinco URLs son candidatas técnicamente indexables en el HTML observado; esto **no acredita indexación en Google**.

## Ejecución y seguridad

- Manifiesto SHA256: `d8e56a7144bf6694e25e09a973c8def5564dc483e3c35fb6fc84a19f362adf8c`. Se ejecutó el comando aprobado sin modificar parámetros. [Preflight](preflight.json) conserva argv, límites, hashes y pertenencia de las cinco URLs al inventario pendiente.
- **6 GET**: robots.txt y los cinco destinos; todos 200. Cero redirecciones, cero reintentos y ninguna visita adicional. [Registro de solicitudes](request-log.json).
- Tiempo supervisado: **15.152 s**, límite absoluto 120 s. Tiempo del rastreo registrado: 11.178 s. Concurrencia 1, frecuencia máxima 0,5/s, 12 GET máximos, timeout 20 s, cuerpos máximos 2.000.000 bytes, tres redirecciones globales.
- Supervisor `finished`, worker recogido (`worker_reaped=true`), 6 peticiones completadas, ninguna sin resultado confirmado o pendiente. No fue necesaria cancelación por plazo ni se repitió su prueba aislada. [Supervisor](supervision.json), [checkpoint](checkpoint.json).
- El encabezado histórico del checkpoint conserva `state: running` y `project: null`; no se interpreta como proceso vivo. El estado terminal consta en el supervisor y las seis peticiones están completadas. Se conserva el archivo original sin repararlo.
- No hubo cambios al motor, tema, menús, contenido, catálogo o canonicals; tampoco GSC, imágenes, CSS, JS, videos, home o sitemap. Los hashes de los cinco archivos integrados y sus dependencias siguen intactos.

## Resultados por URL

| # | URL / title observado | HTTP | Canonical | Caracteres en main | Errores / advertencias del validador |
|---|---|---:|---|---:|---:|
| 1 | [Botas de Presoterapia PRO 3 (Accesorio) | RHINO Performance](https://rhino-performance.com/productos/botas-presoterapia-pro-3/) | 200 | Propio | 7532 | 6 / 18 |
| 2 | [Los Benecios de la Natación para la Salud y el Rendimiento Físico](https://rhino-performance.com/blog/posts/los-benecios-de-la-natacion-para-la-salud-y-el-rendimiento-fisico-ffeb1529210e/) | 200 | Propio | 3873 | 0 / 2 |
| 3 | [¿Por qué es crucial la hidratación en atletas?](https://rhino-performance.com/blog/posts/por-que-es-crucial-la-hidratacion-en-atletas-070675a646a6/) | 200 | Propio | 3557 | 0 / 2 |
| 4 | [Palabras clave para iniciarse en el mundo runner](https://rhino-performance.com/blog/posts/palabras-clave-para-iniciarse-en-el-mundo-runner-120cd6cf0343/) | 200 | Propio | 4815 | 0 / 2 |
| 5 | [Mangas Cold Therapy: recuperación inteligente al alcance de tu cuerpo](https://rhino-performance.com/blog/posts/mangas-cold-therapy-recuperacion-inteligente-al-alcance-de-tu-cuerpo-30c1563de10f/) | 200 | Propio | 5341 | 0 / 2 |

Los cinco destinos permiten el agente de auditoría y Googlebot según robots.txt. No se observaron meta robots/googlebot ni X-Robots-Tag en sus respectivas fuentes. No se observaron flags noindex; el procesamiento de directivas está completo. Cada página contiene un H1 y main; ninguna fue marcada como candidata a soft 404. Title, H1 completos, canonical, headers y hashes del contenido figuran en [resultados por URL](per-url-results.json) y en [CSV](five-url-results.csv).

Robots.txt respondió 200. Conserva la advertencia de parseo de la línea 67 para el token de otro agente (`MJ12bot`), sin errores de parseo. El cuerpo histórico se reutiliza únicamente porque coincide su SHA256 con el cuerpo recibido ahora; no se hizo un segundo GET. [Procedencia de robots](robots-provenance.json).

## Datos estructurados: alertas sin ocultar ni sobrediagnosticar

En Botas PRO 3 se conservaron 6 D010 (errores), 6 D011, 6 D050 y 6 D070 (advertencias). Todas estas alertas señalan `Product@structured-data.item`, entidades secundarias; no al Product principal `structured-data.page`. D010 y D050 comparan esas entidades con canonical/H1 del contenedor: son **posibles falsos positivos contextuales**, no prueba de defectos del producto principal. D011 también conserva `amp%3B` en parámetros; origen y efecto siguen sin demostrar. D070 necesita revisar candidatos de imagen y red; no demuestra por sí solo una imagen comercial ausente. Se conservan también recomendaciones/opcionales originales, sin inventar políticas, precios ni stock.

Los cuatro artículos presentan B030 y B100: el author extraído es texto sin entidad tipada. Es un hallazgo de marcado; la identidad editorial y el tipo Person/Organization requieren una fuente autorizada antes de corregirlo. No se ha observado un rechazo de Google.

El gate general conserva `blocked` en el PDP por las alertas schema y `insufficient_evidence` en los cuatro artículos. No se fuerza su aprobación: la revisión contextual del schema y las capturas de navegación/contenido sin JS siguen pendientes. Esto es distinto del estado técnico `indexable_candidate`, que pasó HTTP, canonical y robots. [Interpretación y gates originales](findings-interpretation.json).

## Matriz incremental

- Inventario conservado: 125 URLs, 124 páginas HTML y un documento XML.
- HTML con comprobación HTTP individual: **74 → 79**.
- Pendientes: **50 → 45**, todas de artículos.
- Se actualizaron exactamente estas cinco filas; las otras 120, el grafo previo, las inspecciones GSC y las impresiones históricas se conservaron.
- Las diez URLs históricamente conocidas como indexadas no equivalen al total indexado del dominio. Este lote no consultó Google ni añade indexaciones conocidas.

[Matriz CSV](../../url-matrix.csv), [matriz JSON](../../url-matrix.json), [recibo de actualización y respaldos](matrix-update.json), [45 pendientes](pending-45.csv), [verificación posterior](verification.json).

## Evidencia y límites

[Informe nativo íntegro](raw-crawl-report.json), [salida CLI](cli-result.json), [checkpoint](checkpoint.json) y respaldos anteriores de ambas matrices están conservados. Fecha inicial de la ejecución: `2026-11-13T07:18:32.446069+00:00`; el intervalo hasta el fin de CLI se registra por URL. La fecha de template_audit corresponde al análisis, no a un timestamp de red individual.

El análisis usa HTML inicial y headers, no navegador renderizado ni prueba manual de teclado. El main se conserva como presencia, longitud y hash, no como certificación editorial. Los tamaños del registro son cuerpos HTTP observados, no peso completo de página, TLS ni medición PageSpeed. No se repitieron suites, piloto anterior ni consultas de Search Console. Se reutilizan las revisiones incrementales Claude/Codex del [paquete aprobado](../remaining-65-preparation/README.md); no se simula una revisión nueva posterior de proveedores.

## Estado final y pendientes

La autorización del lote06 está consumida. No se ejecutó ninguna solicitud después de finalizarlo. Los lotes07–15 siguen pendientes y requieren autorizaciones específicas nuevas.

Quedan45 páginas pendientes, todas de artículos; no quedan productos pendientes de HTTP individual dentro del inventario conocido. Los14 productos conocidos ya tienen respuesta HTTP individual registrada; esto no certifica indexación en Google, inventario administrativo completo ni resolución de todas sus alertas schema. [Lista de45 pendientes](pending-45.csv).

Las advertencias de datos estructurados y la evidencia faltante de navegador siguen abiertas. No se modificó schema, contenido, tema ni motor. El registro de planificación actualiza únicamente el06 a ejecutado. [Recibo del registro](registry-update.json). Los trece manifiestos, operaciones y comandos mantienen sus hashes originales; las120 filas no seleccionadas y los estados históricos de Google permanecen intactos en CSV y JSON. Los26 hashes aprobados del motor/transporte se verificaron también después del lote.
