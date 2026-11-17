# Lote 02 SEO V4 — resultado de producción

Ejecución única autorizada el 13 de noviembre de 2026. Estado nativo: `complete_for_selected_scope`. Las cinco URLs son candidatas técnicamente indexables en el HTML observado; esto **no acredita indexación en Google**.

## Ejecución y seguridad

- Manifiesto SHA256: `7117b37560a94eb8477d6e1328e2999cd103d69857c1e01b87910b8d269b8f42`. Se ejecutó el comando aprobado sin modificar parámetros. [Preflight](preflight.json) conserva argv, límites, hashes y pertenencia de las cinco URLs al inventario pendiente.
- **6 GET**: robots.txt y los cinco destinos; todos 200. Cero redirecciones, cero reintentos y ninguna visita adicional. [Registro de solicitudes](request-log.json).
- Tiempo supervisado: **16.028 s**, límite absoluto 120 s. Tiempo del rastreo registrado: 11.082 s. Concurrencia 1, frecuencia máxima 0,5/s, 12 GET máximos, timeout 20 s, cuerpos máximos 2.000.000 bytes, tres redirecciones globales.
- Supervisor `finished`, worker recogido (`worker_reaped=true`), 6 peticiones completadas, ninguna sin resultado confirmado o pendiente. No fue necesaria cancelación por plazo ni se repitió su prueba aislada. [Supervisor](supervision.json), [checkpoint](checkpoint.json).
- El encabezado histórico del checkpoint conserva `state: running` y `project: null`; no se interpreta como proceso vivo. El estado terminal consta en el supervisor y las seis peticiones están completadas. Se conserva el archivo original sin repararlo.
- No hubo cambios al motor, tema, menús, contenido, catálogo o canonicals; tampoco GSC, imágenes, CSS, JS, videos, home o sitemap. Los hashes de los cinco archivos integrados y sus dependencias siguen intactos.

## Resultados por URL

| # | URL / title observado | HTTP | Canonical | Caracteres en main | Errores / advertencias del validador |
|---|---|---:|---|---:|---:|
| 1 | [Compresor PRO 3 para Presoterapia | RHINO Performance](https://rhino-performance.com/productos/compresor-pro-3-presoterapia/) | 200 | Propio | 8611 | 6 / 18 |
| 2 | [Par de Brazos de Presoterapia PRO 3 | Accesorio | RHINO](https://rhino-performance.com/productos/brazos-presoterapia-pro-3/) | 200 | Propio | 7161 | 6 / 18 |
| 3 | [Guía completa para cuidar tus botas de presoterapia](https://rhino-performance.com/blog/posts/guia-completa-para-cuidar-tus-botas-de-presoterapia-57e0c1076e6c/) | 200 | Propio | 3674 | 0 / 2 |
| 4 | [Cinco consejos infalibles para mejorar tu rendimiento deportivo con la](https://rhino-performance.com/blog/posts/cinco-consejos-infalibles-para-mejorar-tu-rendimiento-deportivo-con-la-presoterapia-92e925649706/) | 200 | Propio | 3344 | 0 / 2 |
| 5 | [La presoterapia: Un nuevo escencial en la rutina de los campeones](https://rhino-performance.com/blog/posts/la-presoterapia-un-nuevo-escencial-en-la-rutina-de-los-campeones-997eed183e73/) | 200 | Propio | 3411 | 0 / 2 |

Los cinco destinos permiten el agente de auditoría y Googlebot según robots.txt. No se observaron meta robots/googlebot ni X-Robots-Tag en sus respectivas fuentes. No se observaron flags noindex; el procesamiento de directivas está completo. Cada página contiene un H1 y main; ninguna fue marcada como candidata a soft 404. Title, H1 completos, canonical, headers y hashes del contenido figuran en [resultados por URL](per-url-results.json) y en [CSV](five-url-results.csv).

Robots.txt respondió 200. Conserva la advertencia de parseo de la línea 67 para el token de otro agente (`MJ12bot`), sin errores de parseo. El cuerpo histórico se reutiliza únicamente porque coincide su SHA256 con el cuerpo recibido ahora; no se hizo un segundo GET. [Procedencia de robots](robots-provenance.json).

## Datos estructurados: alertas sin ocultar ni sobrediagnosticar

En cada PDP se conservaron 6 D010 (errores), 6 D011, 6 D050 y 6 D070 (advertencias). Todas estas alertas señalan `Product@structured-data.item`, entidades secundarias; no al Product principal `structured-data.page`. D010 y D050 comparan esas entidades con canonical/H1 del contenedor: son **posibles falsos positivos contextuales**, no prueba de seis defectos del producto principal. D011 también conserva `amp%3B` en parámetros; origen y efecto siguen sin demostrar. D070 necesita revisar candidatos de imagen y red; no demuestra por sí solo una imagen comercial ausente. Se conservan también recomendaciones/opcionales originales, sin inventar políticas, precios ni stock.

Los tres artículos presentan B030 y B100: el author extraído es texto sin entidad tipada. Es un hallazgo de marcado; la identidad editorial y el tipo Person/Organization requieren una fuente autorizada antes de corregirlo. No se ha observado un rechazo de Google.

El gate general conserva `blocked` en los dos PDP por las alertas schema y `insufficient_evidence` en los tres artículos. No se fuerza su aprobación: la revisión contextual del schema y las capturas de navegación/contenido sin JS siguen pendientes. Esto es distinto del estado técnico `indexable_candidate`, que pasó HTTP, canonical y robots. [Interpretación y gates originales](findings-interpretation.json).

## Matriz incremental

- Inventario conservado: 125 URLs, 124 páginas HTML y un documento XML.
- HTML con comprobación HTTP individual: **54 → 59**.
- Pendientes: **70 → 65**, distribuidas en **7 productos y 58 artículos**.
- Se actualizaron exactamente estas cinco filas; las otras 120, el grafo previo, las inspecciones GSC y las impresiones históricas se conservaron.
- Las diez URLs históricamente conocidas como indexadas no equivalen al total indexado del dominio. Este lote no consultó Google ni añade indexaciones conocidas.

[Matriz CSV](../../url-matrix.csv), [matriz JSON](../../url-matrix.json), [recibo de actualización y respaldos](matrix-update.json), [65 pendientes](pending-65.csv), [verificación posterior](verification.json).

## Evidencia y límites

[Informe nativo íntegro](raw-crawl-report.json), [salida CLI](cli-result.json), [checkpoint](checkpoint.json) y respaldos anteriores de ambas matrices están conservados. Fecha inicial de la ejecución: `2026-11-13T06:22:35.421733+00:00`; el intervalo hasta el fin de CLI se registra por URL. La fecha de template_audit corresponde al análisis, no a un timestamp de red individual.

El análisis usa HTML inicial y headers, no navegador renderizado ni prueba manual de teclado. El main se conserva como presencia, longitud y hash, no como certificación editorial. Los tamaños del registro son cuerpos HTTP observados, no peso completo de página, TLS ni medición PageSpeed. No se repitieron suites, piloto anterior ni consultas de Search Console. Se reutilizan las revisiones incrementales Claude/Codex del [paquete aprobado](../batch-02-preparation/README.md); no se simula una revisión nueva posterior de proveedores.

## Siguiente paso recomendado

Continuar con otro manifiesto cerrado de cinco destinos entre los 65 pendientes, manteniendo los mismos límites y solicitando **otra autorización antes de cualquier GET**. Las advertencias schema pueden revisarse offline con la evidencia conservada; este lote no justifica modificar automáticamente las páginas ni el motor. No se ejecutó ninguna solicitud después de finalizar el lote 02.
