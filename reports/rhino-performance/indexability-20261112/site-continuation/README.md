# Rhino — descubrimiento de la estructura pública existente

**Cierre incremental posterior:** [V4, matriz pendiente y procedimientos](coverage-closure/README.md). Se cerró el QA aislado del controlador del candidato existente, sin integrarlo: 169 unitarias, 13 de integración y TLS local. Codex volvió a agotar inactividad con procesos terminados; el consejo continúa incompleto y V4 bloqueado. Se mantienen 49/124 HTML con HTTP individual y 75 pendientes. Cero solicitudes nuevas al sitio o GSC; conciliación administrativa manual preparada. El texto siguiente conserva la fase de descubrimiento.

12 noviembre 2026. Continuación del ADR-RHINO-011 y auditorías anteriores. **Sin modificaciones al tema, menús, contenido, canonicals, catálogo ni producción por esta continuación.** Se conserva la paginación publicada con sus hashes aprobados. No se creó clon, staging o crawler alternativo.

## Resultado y límites

El inventario principal conocido contiene **125 URLs**: las 117 entradas del sitemap conservado y 8 paginaciones confirmadas fuera de ese inventario. Son 124 páginas HTML y 1 documento XML. El sitemap contiene 116 páginas HTML y ese XML; no se pretende indexar el documento como página comercial. No se redescargó el sitemap válido ni se asegura que este inventario público sustituya un catálogo administrativo completo.

**122 de 124 páginas HTML tienen camino de enlaces iniciales observado desde home.** Se conserva el camino y profundidad por URL. Las dos sin camino en el corpus son Contacto y Sobre Rhino: no se certifica orfandad global. Sobre Rhino está pendiente de contenido por instrucción del propietario y no debe promocionarse. No se agregará ninguna de las dos al menú.

Se dispone de respuesta individual para 49 de 124 HTML, más el XML. En las 49 observaciones HTML utilizadas hay 200; **75 URLs siguen sin comprobación HTTP individual: 11 productos y 64 artículos**. Un enlace no demuestra que su destino responda 200. No se declara una auditoría exhaustiva de todas las rutas actuales ni indexabilidad completa de estas 75 URLs.

[Matriz completa CSV](url-matrix.csv) · [JSON](url-matrix.json) · [Resumen](summary.json) · [Backlog con evidencia/riesgos/autorización](backlog.json) · [Verificación](verification.json). La matriz conserva fechas, fuentes por campo, señales técnicas, estado Google y faltantes. Sus valores unknown/not_checked son información pendiente, no fallos inventados.

## Resumen por tipo

| Tipo | URLs conocidas | Camino HTML observado | HTTP individual observado | GSC PASS conocido |
|---|---:|---:|---:|---:|
| home | 1 | 1 | 1 | 1 |
| page | 8 | 6 | 8 | 1 |
| catalog | 1 | 1 | 1 | 1 |
| sitemap_document | 1 | 0 | 1 | 0 |
| product | 14 | 14 | 3 | 2 |
| category | 5 | 5 | 5 | 2 |
| blog | 1 | 1 | 1 | 1 |
| article | 86 | 86 | 22 | 2 |
| blog_pagination | 7 | 7 | 7 | 0 |
| catalog_pagination | 1 | 1 | 1 | 0 |

GSC PASS es el resultado de la inspección conservada y su fecha, **no un censo del índice actual**. Robots se revisa con las reglas guardadas y un guard adicional estándar para estas lecturas; no se ejecutó ni certificó el parser V4 pendiente. La candidatura técnica exige señales observadas y no equivale a selección de Google.

## Categorías y subcategorías — prioridad principal

| Categoría | HTTP / canonical | H1 | Rutas de producto en tarjetas | Profundidad observada | Google conocido |
|---|---|---:|---:|---:|---|
| /presoterapia/ | 200 / propio | 1 | 3 | 1 | Enviada e indexada |
| /pistolas-de-masaje/ | 200 / propio | 1 | 2 | 1 | not_inspected_current_status_unknown |
| /terapia-fria/ | 200 / propio | 1 | 1 | 1 | not_inspected_current_status_unknown |
| /compresion-frio-y-calor/ | 200 / propio | 1 | 3 | 1 | not_inspected_current_status_unknown |
| /accesorios/ | 200 / propio | 1 | 5 | 1 | Enviada e indexada |

Las cinco tienen title y descripción presentes, enlaces HTML reales desde la estructura existente y contenido/listado en main. No se detectó un P0 de rastreo en ellas. Navegador sin JavaScript a 390 px: 200, H1/canonical y tarjetas con href en las cinco categorías; no se enviaron formularios ni se recorrieron automáticamente sus productos. Esta prueba acredita enlaces/texto sin JS, no calidad visual de todas las imágenes ni todas las interacciones.

Las tarjetas usan `?entry_path=category`. Se conservan los href originales en [variantes de enlace](product-link-variants.csv). La asociación por path corresponde a 14 rutas distintas del inventario; **no se convierte en una prueba HTTP/canonical de cada alias**. Dos GET puntuales de GUN AIR, con el parámetro y sin él, devuelven 200 y canonical a la misma URL limpia. No se recomienda quitar parámetros nativos ni crear productos duplicados.

No se confirmó una subcategoría adicional. Eso **no prueba que no existan categorías administrativas no enlazadas u ocultas**. Falta contraste con inventario administrativo autorizado; no se inventan subcategorías por encabezados o slugs. Los estados privados/ocultos no se convierten automáticamente en candidatas SEO.

## Productos y paginación preservada

Los 14 productos del sitemap tienen caminos HTML observados. Las cinco categorías contienen enlaces de tarjeta a esas 14 rutas (asociación explícita de entry_path), y el catálogo/página 2 ya tienen QA publicado de 12→14 IDs únicos, orden conservado, HTML alternativo y canonical propio. Se reutiliza el [resultado de publicación](../three-issues/operations/publication/resultados-produccion.md), sin repetirlo ni cambiar archivos.

Solo 3 PDP tienen una respuesta individual reunida en esta matriz. Las otras 11 no se declaran 200 por estar enlazadas. La presencia pública en sitemap/tarjetas no certifica un flag administrativo activo, inventario actual o disponibilidad de todas las variantes. No se alteran ni inventan stock, precio, SKU o estados comerciales. Las variantes y rutas históricas de Search Analytics no se agregan como productos nuevos.

## Blog y artículos antiguos

[Continuidad página por página](blog-continuity.json): páginas 1–7 contienen 12 artículos cada una, página 8 contiene 2. **86 enlaces distintos en main, sin solapamiento entre las listas; coinciden con los 86 artículos del sitemap.** Las cuatro lecturas nuevas fueron páginas 4–7, ya enlazadas en HTML guardado; 1/2/3/8 se reutilizaron.

Por tanto los 62 artículos antes no cubiertos por la muestra parcial **ya tienen ruta HTML observada**. Las profundidades observadas de los artículos van de 1 a 4 en este grafo, con accesos desde home y secuencias de blog. Es el camino más corto del corpus observado, no un mínimo exhaustivo del sitio ni una medida de frecuencia de rastreo Google. No se visitaron automáticamente los 86 artículos.

Los 22 artículos con HTTP individual se reutilizan de pruebas previas; faltan 64. Las ocho páginas del blog responden 200 en la evidencia y las siete posteriores consolidan canonical hacia /blog/. La continuidad HTML está demostrada, pero no que Google indexe esas páginas o que ese canonical cause exclusión de artículos. Se conserva el comportamiento y la [consulta preparada a Tiendanube](../three-issues/operations/consulta-tiendanube.md), sin enviarla ni modificar head-tags.

**Conciliación de conteos:** antes se habían descubierto 24 destinos de artículos mediante enlaces de blog1/2; ahora son 86 mediante blog1–8. Los 22 son respuestas HTTP de artículos individuales, una dimensión diferente: veinte del postcheck de BreadcrumbList y dos de las capturas anteriores. No se suman 24+22 ni se interpreta que los 86 destinos se visitaron individualmente. El canonical de blog2–8 continúa como hallazgo **P2 / needs_evidence**, no como solución verificada. La paginación del catálogo publicada pertenece a otro componente.

## Páginas informativas

Se reunieron lecturas individuales de las ocho páginas: Contacto, Sobre Rhino, Arma tu pack, privacidad, cambios/garantía, cookies, envíos y política de devolución. Se conservaron cuerpos/proyecciones semánticas de seis con camino HTML y dos sin camino en este corpus.

- **Contacto:** 200, sitemap y canonical propio; Google la tenía descubierta sin indexar. Sin ruta en el corpus, no huérfana confirmada. Description vacía observada: mejora editorial potencial, no causa demostrada de exclusión. No se agrega al menú ni se modifica contenido.
- **Sobre Rhino:** 200, sitemap y canonical propio, pero el propietario confirma contenido sin desarrollar. Estado: pendiente editorial/no promoción. No se propone noindex, eliminación, redirección ni solicitud de indexación.
- **Resto:** contenido inicial presente y destinos identificados; esto no certifica calidad editorial, validez legal, vigencia comercial ni ausencia de duplicados en toda la tienda. No se demostraron duplicados exactos de main entre las muestras revisadas, pero falta el rastreo integral.

## Google: qué sabemos y qué falta

Se reutilizaron las 13 inspecciones iniciales **más las 2 posteriores del blog 3/8**: 15 en total, 10 PASS, 1 descubierta sin indexar y 4 URLs exactas desconocidas. Las 170 filas con impresiones son del 2026-10-12 al 2026-11-08 PT, filtradas al origen sin www; no equivalen al total indexado ni describen el estado actual de las 170 URLs.

[URLs históricas adicionales/alias](google-extra-urls.csv) conserva las filas fuera del inventario exacto como diagnóstico, sin declararlas actuales ni promocionarlas. No se ejecutaron nuevas consultas GSC: access doctor indica credencial no disponible; no se inició otro OAuth ni se compartieron tokens con Claude.

Primer lote nuevo justificado cuando vuelva el acceso autorizado: Pistolas de masaje, Terapia fría, Compresión frío/calor y catálogo página 2. No repetir las 15 consultas vigentes. Para cobertura total de indexación y motivos hacen falta exportaciones oficiales del informe Páginas, con fecha y límites de exportación; Search Analytics/Inspection no proporcionan un censo completo mediante estas muestras.

## Bloqueo del crawler y alcance de red

El [último candidato V4](../../../seo/v4-source-review/README.md) mantiene workspace_applied=false, implementation_allowed=false y consejo needs_evidence. No se aplicó ni ejecutó, ni se redujeron sus protecciones. Tampoco se construyó un crawler sustituto.

Se hicieron 14 GET de documentos fijos conocidos: 4 categorías, 4 páginas de blog, 4 informativas y 2 URLs GUN AIR para contrastar el parámetro; además 5 navegaciones sin JS de categorías. Son 19 documentos principales, no el total de solicitudes de assets del navegador. Las lecturas directas tenían origen exacto, sin seguimiento de redirecciones, límites de cuerpo/tiempo, pausa y parada 403/429. El navegador reutilizó sus guardas de lectura. No hubo 403/429 ni redirecciones en estos documentos nuevos. No hubo cola ni BFS de red; el grafo se calculó offline con evidencia inicial conservada.

**Cobertura pendiente no significa sitio roto:** antes de ampliar al control individual de 75 destinos debe resolverse la revisión/recibo QA e integración del transporte V4; no se sustituye por un lote masivo manual. No se emitieron permisos MCP nuevos, conexiones administrativas, solicitudes de indexación ni registros de sitemap.

## Prioridades y decisiones

- **P0:** ningún bloqueo general confirmado en el alcance observado; las URLs no medidas impiden una certificación universal.
- **P1:** cerrar la cobertura de 75 destinos y el inventario administrativo de categorías mediante mecanismos aprobados. Investigar Contacto sin afirmar orfandad ni modificar menús.
- **P2:** conservar el canonical del blog hasta respuesta oficial; completar las cuatro inspecciones nuevas justificadas y documentar la description de Contacto.
- **P3:** Sobre Rhino queda pendiente de contenido sin promocionarla. Ninguna recomendación editorial se aplica automáticamente.

No hace falta añadir nuevas funcionalidades para demostrar descubrimiento de las cinco categorías, catorce productos y 86 artículos: ya hay rutas HTML. Quedan controles técnicos e información de Google por completar. No se ejecutaron Lighthouse/PageSpeed nuevos: no hay cambio de código que comparar y sus baselines publicados se conservan.

## Evidencias y consejo incremental

Codex preparó el grafo/matriz y ejecutó las comprobaciones; Claude hizo un análisis independiente acotado de faltantes, sin rehacer propuestas/contrastes anteriores. La revisión de los nuevos resultados y las preguntas cruzadas se conservan en el registro de esta continuación. Ningún acuerdo sustituye la evidencia.

Run: `reports/runs/rhino-performance/20261112T191008-site-discoverability-continuation-54a878c3`. Contiene documentos nuevos, referencias de observaciones anteriores, grafo con href/contexto/fecha, caminos y hashes de fuente. Las fuentes originales y ADR anteriores se conservan. La paginación publicada mantiene TPL 0958c668…d463c y JS f9755749…e93be9. Menús y páginas no se modificaron.

Durante el cierre se observó un cambio local ajeno en `snippets/bundle/bundle-builder-js.tpl`. No se editó, publicó ni revirtió. Los cinco archivos protegidos de esta auditoría, incluida la paginación publicada, mantienen sus hashes del inicio.

### Cierre de la revisión incremental

[Preguntas, objeciones, respuestas y decisión](council-incremental.json). Claude analizó primero los faltantes; Codex aportó las nuevas pruebas y cuestionó la confusión entre destinos enlazados y HTTP individuales. Claude pidió aclarar 24/22 y mantener abierto el canonical del blog. Los recibos demostraron que eran dimensiones distintas y que el canonical ya se registraba como P2; se añadió una conciliación explícita. Claude aprobó **solo la precisión de esa aclaración documental**. No afirmó leer los 125 registros completos ni ejecutar las pruebas. La cobertura integral continúa **needs_evidence** y no hay aprobación de implementación.

El primer intento de contraste no se completó; el supervisor devolvió un error genérico y el wrapper no conservó el diagnóstico interno. Su causa específica queda no determinada, sin inventar autenticación/cuota/timeout. Se conservó el paquete y se recuperó una sola revisión acotada con metadatos registrados; luego se cerraron las dos precisiones mediante un intercambio final breve. No se repitieron las comprobaciones del storefront ni el consejo completo.
