# Rhino Performance — piloto SEO V4 real, una ejecución autorizada

12 de noviembre de 2026. **Cinco destinos comprobados: HTTP200,canonical propio,rastreo permitido y sin noindex observado.** Se consumieron6GET de los12permitidos:robots.txt+cinco páginas. No hubo redirecciones,bloqueos de transporte,reintentos ni consultas posteriores. Esto acredita candidatura técnica en HTML inicial,**no indexación real en Google ni aprobación SEO completa**.

## Ejecución y presupuestos

- Manifiesto exacto SHA256: `3b14fcb031ae57ab43ef247ff087c6d8df0b0c400ca12ac3694edfc654a38bb6`.
- Código:los cinco hashes y las dependencias del transporte coincidieron con la versión revisada antes y después.
- Invocación:exactamente la orden aprobada,sin shell ni cambios de parámetros;una sola ejecución,con marcador duradero que impide repetirla con esta autorización.
- GET confirmados:**6**. Sin resultado confirmado:**0**. GET adicionales autorizados pero no utilizados:**6**;no se rellenó presupuesto.
- Concurrencia:**1**;frecuencia configurada:**máximo0,5/s**,gestionada por Fetcher. No hay marcas horarias por GET para reconstruir una gráfica independiente de intervalos.
- Tiempo supervisado:**19.091s** de120s. El crawler registró14.547s hasta emitir provenance;el supervisor incluye también preparación y exportación.
- Máximo cuerpo observado decodificado:**735,602bytes**,bajo2.000.000por cuerpo. Suma de cuerpos decodificados:**2,212,604bytes**;no es tráfico TLS ni peso completo de una página en PageSpeed.
- Redirecciones:**0/3**. Sin403/429,fallosTLS/IP,orígenes externos,presupuesto agotado o desafío de acceso.
- Home,sitemap,imágenes,CSS,JavaScript y videos:**0GET**. Las referencias HTML recogidas en el grafo no son recursos descargados.

[Preflight](preflight.json) · [salida exacta de CLI](cli-result.json) · [registro de seis GET](request-log.json) · [verificación](verification.json).

## Resultados por destino

Meta robots y meta googlebot no estaban presentes en el HTML observado de ninguna de las cinco páginas. Tampoco se observó X-Robots-Tag en sus cabeceras conservadas. Esto significa ausencia observada de esas restricciones,no una etiqueta literal index/follow. Robots permitió al agente propio y a Googlebot.

| Destino | HTTP | Canonical | H1 en HTML | Caracteres de main | Estado técnico |
|---|---:|---|---:|---:|---|
| [GUN PRO](https://rhino-performance.com/productos/pistola-de-masaje-gun-pro/) | 200 | Propio | 1 | 8,280 | indexable_candidate |
| [TUB AIR](https://rhino-performance.com/productos/tina-de-hielo-tub-air/) | 200 | Propio | 1 | 7,522 | indexable_candidate |
| [Presoterapia y salud mental](https://rhino-performance.com/blog/posts/la-presoterapia-como-transformador-de-tu-salud-mental-relajacion-y-recuperacion-127cdc829590/) | 200 | Propio | 1 | 3,247 | indexable_candidate |
| [El frío como herramienta](https://rhino-performance.com/blog/posts/el-fro-no-es-un-castigo-es-una-herramienta-cbe9a25855f8/) | 200 | Propio | 1 | 4,250 | indexable_candidate |
| [Faja de compresión lumbar](https://rhino-performance.com/blog/posts/faja-de-compresion-lumbar-el-soporte-que-tu-espalda-agradecera-047c381cf3ac/) | 200 | Propio | 1 | 3,963 | indexable_candidate |

[Resultados completos por URL](per-url-results.json) · [CSV con URL,canonical,robots,title,H1,contenido,fecha](five-url-results.csv). Ahí se conservan los títulos y H1 exactos,meta description,permisos,hash de HTML y de main,banderas del validador y referencias al informe original.

Las fechas por página son las de generación de su auditoría,posteriores al HTTP. El intervalo de observación de red es el del run;el motor no guarda timestamps individuales de recepción de cada respuesta. main se conserva como presencia,longitud,hash y detector soft404,no como transcripción del cuerpo ni certificación de calidad. Ninguna de las cinco activó soft404 en el detector acotado.

## Problemas y advertencias: interpretación de la evidencia

**No se confirmó un bloqueo en HTTP,robots,canonical o noindex para estos cinco destinos.** No se infiere por ello indexación,visibilidad real bajo CSS ni elegibilidad garantizada para resultados enriquecidos.

- **P2,blog:**los tres BlogPosting declaran author como texto. El validador emite B030/B100 sobre ese mismo aspecto;no son dos bloqueos independientes por artículo. Revisión futura de la entidad de autor con la fuente editorial real,sin inventar autor ni modificar ahora contenido.
- **P2,productos,needs_evidence:**cada PDP contiene un Product principal de structured-data.page y cinco Product de structured-data.item. El validador registra cinco D010 y15warnings por PDP al comparar entidades secundarias contra canonical,H1 e imágenes de la página principal. Se preservan los10errores brutos y30warnings de ambos productos;la atribución a tarjetas/productos relacionados es compatible con el marcado,pero exige revisión contextual antes de declarar defecto del Product principal o corregir el tema. No se presentan como10bloqueos de indexación confirmados.
- **Robots:**200,parsing conocido,sin errores bloqueantes;warning de token en línea67paraMJ12bot,un agente ajeno. La copia histórica de robots tiene exactamente el mismo SHA256 que el cuerpo del GET actual y se reutilizó para identificar la línea,sin segunda solicitud. No se relajó ninguna protección.
- Campos recomendados/opcionales de Offer,identidad del publisher y otras recomendaciones se conservan en los resultados. No se inventaron políticas,fechas,precio,inventario o datos comerciales para completarlos.

El resumen CLI muestra findings=0 porque cuenta hallazgos del nivel raíz,**no agrega template_audit.findings de cada nodo**. No significa ausencia de banderas. Los recuentos por página y el informe original son la evidencia conservada;no se cambió el motor para alterar ese resumen.

La readiness completa permanece **blocked en las dos PDP** por las banderas de structured_data y **insufficient_evidence en los tres artículos**;además faltan capturas de navegador no-JS/DOM renderizado. Es distinto de indexable_candidate en el clasificador HTTP/HTML. Este piloto no autorizaba navegador ni descarga de scripts/recursos para cerrar esas pruebas.

[Interpretación y alcance de hallazgos](findings-interpretation.json) · [informe íntegro,sin modificar las banderas](raw-crawl-report.json) · [robots y procedencia](robots-provenance.json).

## Supervisor y checkpoint

El supervisor terminó en state=finished y confirmó worker_reaped=true. No se agotó el plazo y no fue necesaria cancelación por deadline. Su limpieza del grupo permanece activa al terminar. Las seis operaciones del checkpoint están completed;no quedan peticiones pendientes o sin confirmación en este piloto.

El checkpoint conserva su campo general state=running/project=null,limitación ya documentada;no representa un worker aún activo. La autoridad terminal es supervision.json y los estados por petición. No se editó el checkpoint para ocultar esa limitación.

[Checkpoint original](checkpoint.json) · [supervisión original](supervision.json). Se preservan tal cual. La autorización de una ejecución quedó consumida;no se inició otra consulta para resolver advertencias.

## Matriz SEO actualizada sin sobrescribir historia

Se respaldaron ambas versiones antes de actualizar **solo cinco filas** de url-matrix.csv y url-matrix.json. Las otras120filas y los campos de Google conservan sus valores. Las fuentes/fechas nuevas quedaron vinculadas al informe,y los registros anteriores siguen en el respaldo. No se solicitaron URLs enlazadas nuevas ni se aumentó el inventario de125URLs.

| Cobertura individual HTML | Antes | Después |
|---|---:|---:|
| HTML con HTTP propio comprobado |49|**54**|
| HTML total conocido |124|124|
| Destinos pendientes de HTTP individual |75|**70**|
| Productos pendientes |11|**9**|
| Artículos pendientes |64|**61**|

Se conservan las122rutas HTML observadas previamente,las15inspecciones GSC históricas y10PASS conocidos;no son un censo del índice. No se reconsultó Search Console. Las70filas pendientes no se convierten en200por estar enlazadas o en sitemap.

[Matriz CSV actual](../../url-matrix.csv) · [matriz JSON actual](../../url-matrix.json) · [cambios y hashes antes/después](matrix-update.json) · [70destinos aún pendientes](pending-70.csv). El archivo pending-75.csv original permanece como lista histórica. Los bloqueos de planificación antiguos que permanezcan en filas no actualizadas son del checkpoint anterior:el bloqueo operativo actual de los70es falta de autorización de ampliación,no que V4 siga sin integrar.

## Recomendación y permisos pendientes

1. Revisar los hallazgos de autor y de Product secundarios **sobre los artefactos guardados**,sin nuevas consultas ni cambios de tema. No considerar una advertencia del validador prueba de exclusión de Google.
2. Si se autoriza continuar,preparar otro manifiesto cerrado de cinco de los70pendientes y su hash;solicitar autorización específica para ese lote. El modo actual no admite una lista de70:completarla en este formato requeriría14ejecuciones nuevas,ninguna autorizada por este piloto.
3. Mantener separados descubrimiento,rastreo,candidatura técnica e indexación observada. Para conocer el último punto hará falta acceso GSC autorizado en otra fase,no inferirlo de estos200.

No se modificaron tienda,tema,productos,contenido,menús,canonicals,paginación ni motor. No hubo compras,formularios,credenciales administrativas,despliegues,clones o staging. Solo se ejecutó la invocación aprobada y después se trabajó con sus archivos locales.

Run del permiso y salida: `reports/runs/rhino-performance/20261112T220922-authorized-five-url-pilot`. Informe nativo: `reports/runs/rhino-performance/20261112T220939-seo-v4-crawl-d6f87221/report.json`.
