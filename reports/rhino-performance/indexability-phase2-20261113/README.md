# Rhino Performance — fase2: indexación conocida y oportunidades orgánicas

13 noviembre2026. Resultado: **Google Search Console está configurado, pero esta sesión no tiene credencial utilizable**. No se intentó la API ni se inició OAuth. La matriz conserva124 HTML conHTTP individual,122 caminos observados,14 productos,5 categorías y86 artículos; no se repitieron lotes ni se modificó la tienda.

El consejo incremental terminó con los cuatro contratos válidos, preguntas y respuestas conservadas; el ADR queda **needs_evidence** y `implementation_allowed=false`. Claude pidió cambios/condiciones en el procedimiento y ambos mantienen abierta la identidad editorial/remota. No se presenta como aprobación completa ni se cambia el estado para terminar.

## 1. Matriz Google: qué conocemos

| Evidencia oficial conservada | URLs del inventario |
|---|---:|
| Indexada en inspección histórica | 10 |
| Descubierta sin indexar, histórica | 1 — Contacto |
| Google no reconocía la URL exacta | 4 — Sobre Rhino y blog2/3/8 |
| Sin inspección oficial conservada | 109 |
| **Total HTML** | **124** |

[CSV de124URLs con estado/fuente/fecha](url-google-matrix-124.csv) · [JSON](url-google-matrix-124.json). Son estados del12 noviembre2026, **no estados actuales inventados**. Los109 sin inspección no se clasifican como no indexados. Tampoco hay evidencia para asignar ahora a nuevas filas «rastreada sin indexar», duplicada, canonical alternativo, noindex, robots o error; esas categorías quedan desconocidas hasta un resultado oficial porURL o ejemplo exportado.

Las170 URLs con impresiones del periodo histórico no son un censo del índice. La indexabilidad técnica y un canonical declarado no sustituyen el canonical elegido porGoogle ni sus decisiones de inclusión.

## 2. Search Console y siguiente entrada necesaria

[Estado comprobado del acceso](access-status.json): configurado=true, credential_available=false, account_access_tested=false, api_available=null. Eso no prueba una caída deGoogle ni un rechazo de autenticación: no se hizo una llamada sin token. No se copiaron credenciales ni se probó un conector alternativo.

La vía disponible ahora es que el propietario aporte las exportaciones originales. El [procedimiento exacto](GSC-export-procedure.md) explica propiedad, ámbito, resumen, ejemplos por motivo, páginas indexadas y campos de inspección. Google advierte que las listas son muestras, hasta1000 ejemplos y potencialmente incompletas incluso por debajo de ese límite. No asignaremos estado a las URLs ausentes de ellas. [Ayuda oficial del informe](https://support.google.com/webmasters/answer/7440203?hl=es).

Para una URL concreta necesitamos el resultado de la versión indexada y su fecha; una prueba en vivo no determina qué canonical elegiráGoogle. [Ayuda oficial de inspección](https://support.google.com/webmasters/answer/9012289?hl=es). Los cuatro destinos nuevos ya seleccionados siguen siendo Pistolas de masaje, Terapia fría, Compresión frío/calor y catálogo página2; no se repiten las15 inspecciones guardadas. [Lista preparada](Google-next-targets.json).

## 3. Categorías: prioridad comercial y visibilidad histórica

Las cinco categorías tienenHTTP200, canonical propio y caminosHTML conservados. No hay causa demostrada para cambiar su indexabilidad desde el tema. Su estado y su visibilidad son dimensiones diferentes:

| Categoría | URLInspection conservada | Impresiones históricas | Clics históricos | CTR histórico |
|---|---|---:|---:|---:|
| [https://rhino-performance.com/presoterapia/](https://rhino-performance.com/presoterapia/) | indexed_historical | 1729 | 16 | 0.93% |
| [https://rhino-performance.com/pistolas-de-masaje/](https://rhino-performance.com/pistolas-de-masaje/) | unknown_no_official_evidence | 21 | 0 | 0.00% |
| [https://rhino-performance.com/terapia-fria/](https://rhino-performance.com/terapia-fria/) | unknown_no_official_evidence | No devuelto | Desconocido | Desconocido |
| [https://rhino-performance.com/compresion-frio-y-calor/](https://rhino-performance.com/compresion-frio-y-calor/) | unknown_no_official_evidence | 419 | 4 | 0.95% |
| [https://rhino-performance.com/accesorios/](https://rhino-performance.com/accesorios/) | indexed_historical | 759 | 16 | 2.11% |

Periodo:12 octubre–8 noviembre2026 PT. [Datos originales y procedencia](category-visibility-historical.json). La ausencia de Terapia fría en las filas devueltas **no equivale a cero tráfico ni a no indexada**. Compresión frío/calor tiene impresiones históricas aunque no tenga URLInspection conservada; no se rellena su estado actual a partir de eso.

**Prioridad de evidencia:** inspeccionar categorías comerciales con estado desconocido antes de volver a comprobarHTTP. **Prioridad de crecimiento:** Presoterapia tiene volumen histórico mayor yCTR bajo; conviene obtener consultas, dispositivo, país y apariencia de búsqueda antes de proponer títulos o cambios de contenido. No conocemos aquí una palabra clave objetivo demostrada ni el valor de conversión por categoría. No se atribuye elCTR a un title concreto ni se promete mejora de posiciones.

Los14 productos siguen conHTTP y rutasHTML; solo dos tienenPASS histórico en la muestra. Eso no implica que los otros12 estén excluidos. Las páginas institucionales conservan sus estados: Contacto no se modifica sin causa; Sobre Rhino sigue pendiente de contenido y no se promociona.

## 4. Los20 artículos: recuperación de fuentes originales

Se examinaron203 archivos de familias originales breadcrumb/SEO-audit/integral/indexability; ocho archivos contenían rutas de los20 objetivos. El postcheck original guardaHTTP, URLfinal, fecha, hashHTML, canonical y breadcrumbs. Su código conserva una proyección y no el cuerpo/cabeceras. **Se confirman los20 canonical propios ya presentes; no se recuperaron meta robots, X-Robots-Tag ni main** dentro de esas fuentes. No se inventa un cuerpo desde suSHA ni se confunde falta de captura con noindex.

[Recuperación porURL, archivos, punteros ySHA](twenty-original-recovery.json). La búsqueda es acotada: no afirma que nunca pueda existir otra copia fuera de esas familias. El baseline original no se sobrescribió.

[Plan de comprobación limitada](twenty-completion-procedure.md): cuatro manifiestos de5 ya validados por el selector nativo, sin modificar motor. Cada operación conserva12 GETmáximos, concurrencia1,0,5 solicitudes/s —intervalo mínimo2 s, mayor si robots lo exige—, supervisor120 s, timeout20 s,2.000.000 bytes y3 saltos. SeisGETnominales:robots más5 destinos. Robots es obligatorio; no se elimina para ahorrar solicitudes.

**Condición aún abierta del consejo:** el preflight de ejecución debe comprobar señales faltantes y hashes/autorización/marcador, no `http=not_observed`. Los drivers de lotes01–15 exigen ese último estado y no pueden reutilizarse sin adaptar el control del propósito. El procedimiento y comandos están preparados; no se afirma que exista ya un nuevo ejecutor validado. **Ninguna de las cuatro operaciones está autorizada ni ejecutada.** Antes de solicitar su ejecución se debe cerrar ese control acotado; no hay autorización conjunta ni para repetir124 páginas.

## 5. Canonical del blog

Se conserva la [consulta técnica original preparada y no enviada](consulta-tiendanube-preserved.md), con evidencia de blog2/3/8:HTTP200, listas diferentes y canonical hacia `/blog/`. Los siete listados paginados no se cambian. No se encontró una respuesta oficial en los artefactos referenciados y no se contactó aTiendanube.

El candidato de fuente local `layouts/layout.tpl:73` delega en `component('head-tags')`. Su publicación actual no se revalidó en esta fase. No se propone duplicar canonical, manipularlo conJS ni alterar head-tags. El canonical de los listados no demuestra queGoogle excluya sus artículos. Estado: **mecanismo soportado pendiente de confirmación**.

## 6. Datos estructurados: evaluación contextual

[Paquete de evidencia conservada](schema-context-packet.json) · [fuentes locales candidatas, hashes y líneas](source-candidates.json). No se realizaron nuevosGET, validadores externos ni modificaciones para silenciar alertas.

| Hallazgo | Qué está respaldado | Qué falta / decisión |
|---|---|---|
| BlogPosting.author | B030/B100 en64 artículos V4; valores escalares extraídos. Candidato local: `snippets/structured-data/structured-data.tpl:88–89` y`:129–130`, desde `post.author_name`. | TipoPerson/Organization, identidad editorial y correspondencia con el emisor publicado actual. No producir un diff que invente identidad. |
| Product principal | En los ejemplos revisados se identifica `structured-data.page`; no recibe los avisos comparativos citados. | No equivale a certificación integral ni validaciónGoogle de todas las propiedades. |
| D010 / D050 secundarios | Señalan `structured-data.item`, Product de tarjetas distintas comparados con canonical/H1 del contenedor. | Posibles falsos positivos contextuales; no cambiar el producto principal ni forzar todos los nombres aH1. |
| D011 | URLssecundarias pueden diferir legítimamente; se conserva codificación`amp%3B`. | Procedencia/efecto desconocidos sin bloque original; no atribuir automáticamente al tema, plataforma o extractor. |
| D070 | Comparación de imágenes con proyección incompleta y placeholders. | Sin candidatos completos/currentSrc/red no se demuestra imagen comercial ausente. |

**Corrección concreta potencial, aún bloqueada:** serializar author como la entidad editorial real en el mismo emisor existente, conservando su nombre y escapadoJSON, sin añadir otro script. No hay base para escoger el tipo todavía. Consumidores locales: `snippets/blog/blog-post-item.tpl`, `layouts/layout.tpl`; atribución visible en `snippets/blog/blog-post-content.tpl`. El cambio compartido afectaría listados y artículos, no solo una instancia. Riesgos: inventar autor, duplicar marcado o alterar identidad. Requiere fuente editorial, hashes publicados, diff exacto, revisión independiente y QA antes de pedir publicación.

Los Product secundarios proceden como candidato de `snippets/product-list/product-item/item.tpl:244` hacia el mismo snippet. No se cambia precio, stock, ofertas, imágenes ni condiciones comerciales. No se modifica el crawler para transformar una alerta en aprobado.

## 7. Prioridades y criterios de decisión

[Prioridades porlas124URLs CSV](url-priorities-124.csv) · [JSON](url-priorities-124.json).

- **P0:** ningún bloqueo general nuevo demostrado. No crear una corrección de producción para un estado desconocido.
- **P1 — evidencia/indexación comercial:** estadoGoogle de las tres categorías pendientes y catálogo2; conciliar exportaciones y luego productos comerciales. Cerrar los20 campos técnicos mediante el procedimiento mínimo, sin repetir coberturaHTTP.
- **P2 — calidad/consistencia:** resolver autor/emisor; estudiar avisos secundarios; obtener respuesta oficial sobre paginación de blog. No presentar estos ajustes como garantía de indexación.
- **P2/P3 — visibilidad:** analizar consultas yCTR de categorías antes de proponer título, descripción o contenido; cualquier propuesta necesita keywords/relevancia comercial respaldadas. Contacto se mantiene sin modificación; Sobre Rhino diferido por el propietario.

**Bloqueo de indexación:** exige evidencia de directiva/obtención/canonical y estadoGoogle pertinente. **CalidadSEO:** estructura y metadatos pueden mejorarse aunque una URL esté indexada. **Posicionamiento por consulta:** requiere datos de consultas y competencia/intención;HTTP200 o un score no prueban la solución. No se prometen tráfico ni rankings.

## 8. Revisión dual real y objeciones

| Agente | Etapa | Modelo / esfuerzo | Duración | Evidencia |
|---|---|---|---:|---|
| claude | review | claude-sonnet-5-5 / medium | 30.15 s | [Recibo](claude-review.json) |
| claude | contrast | claude-sonnet-5-5 / medium | 14.94 s | [Recibo](claude-contrast.json) |
| codex | review | gpt-6.1-sol / medium | 39.12 s | [Recibo](codex-review.json) |
| codex | contrast | gpt-6.1-sol / medium | 33.25 s | [Recibo](codex-contrast.json) |

[Recibos del controlador y condiciones](controller-final-review.json) · [ADR-RHINO-012](ADR.json) · [uso/costes declarados por cada runtime](council-runtime-metrics.json). Solo se registran costes cuando el proveedor los comunica; no se estima un coste a partir del otro.

Claude preguntó por una prueba del emisor remoto actual y del tipo deautor. Codex respondió que no existe en el paquete: el marcador no acredita identidad editorial ni igualdadremota. Codex preguntó por el preflight correcto para destinosHTTP200. Claude respondió con señalesfaltantes, fuentes/hashes, autorización y marcador propio. Ambas respuestas están conservadas y vinculadas a sus preguntas exactas.

El controlador corrigió dos imprecisiones de las propuestas:robots no es opcional y0,5 solicitudes/s no es un intervalo de0,5 s. Las dudas de identidad y de control previo siguen abiertas; no se inventó consenso ni se autoriza implementación por tener contratosJSONválidos. CommandCode permaneció deshabilitado.

## 9. Qué se necesita del propietario

1. **Ahora:** exportaciones originales deSearchConsole y campos de inspección indicados en[GSC-export-procedure.md](GSC-export-procedure.md). No enviar claves. Alternativamente, recuperar acceso por el flujo de autenticación ya existente cuando lo solicite el propietario; no se inició uno nuevo.
2. **Para completar20 señales:** revisar el procedimiento y cerrar el preflight específico. Después, autorizar porseparado una operación de5 con suSHA/comando; no ejecutar lascuatro con una sola aprobación.
3. **Para schema:** confirmar identidad/autores delCMS y permitir comparación de fuente publicada antes de preparar un diff; no se solicita publicación ahora.
4. **Para blog:** el propietario puede enviar el borrador a soporteoficial y aportar larespuesta. No se envió a terceros automáticamente.

En esta fase se modificaron únicamente informes/proyecciones preparados enIA-Ipanema. No se alteraron la matrizbaseline, el tema, menús, productos, artículos, aplicaciones, canonicals ni motor. Se conservaron las124 comprobacionesHTTP,122 rutas y las15 inspeccioneshistóricas. Las únicas consultas externas fueron las dos páginas públicas de documentación oficial enlazadas; **cero llamadas aGSC/API y cero solicitudes alstorefront**.
