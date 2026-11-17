# Procedimiento propuesto del piloto: diseño pendiente, no ejecutable todavía

El motor integrado y sus hashes permanecen válidos. No se repiten 191 unitarias,13 integraciones ni quick. Solo se revisa cómo ejecutar cinco destinos cerrados. No se ha autorizado red, modificado código ni consultado Rhino/Google.

## Destinos y límites

`targets.json` contiene los dos primeros productos y los tres primeros artículos de pending-75.csv, conciliados literalmente con url-matrix.csv. Conserva filas lógicas, hashes de CSV, procedencia sitemap y enlaces observados. Las respuestas individuales siguen pendientes, no se atribuye HTTP200 nuevo.

Origen exacto: https://rhino-performance.com (sin www, según proyecto registrado e inventario). No se siguen redirecciones a www u otro origen. Si producción exige una, el piloto se detiene: no se amplía la autorización automáticamente.

Límites solicitados:12GET totales;concurrencia1;máximo0,5GET/s (al menos2s entre inicios, o más si robots);120s totales;20s por solicitud o tiempo restante menor;2.000.000bytes tanto de respuesta como tras descompresión;máximo3saltos seguros. Se propone que los3saltos sean un presupuesto global compartido entre robots y los cinco destinos, además del máximo por cadena, para ser más estricto que la interpretación por cadena.

## Mecanismo actual verificado

- `crawl(project, *, limits=None, allow_network=False, transport=None, captures=None, clock=None, sleep=None)` no recibe destinos cerrados. Policy exige public_url en la raíz.
- Lee robots.txt; admite200 y reconoce404/410 como ausencia conocida de reglas. Otras respuestas, errores de parsing o agotamiento de redirecciones dejan robots desconocido y no habilitan el rastreo. Conserva decisiones del agente propio y Googlebot por separado.
- Sigue sitemaps declarados o sitemap.xml por defecto, salvo max_sitemaps=0. Desactivar sitemaps no cambia la semilla: sigue siendo home. El sitemap puede redirigir a un CDN fuera del origen exacto: no se amplía el origen para esta prueba.
- Después usa BFS desde home y añade entradas del sitemap si la navegación se agota. `max_urls=5` limita nodos, no elige estos cinco; los saltos también consumen nodos. Enlaces/canonical no son una lista de semillas autorizadas.
- Policy valida cada GET y redirección: HTTPS/origen, parámetros, rutas privadas/acciones, activos y escapes. https_get resuelve IPs públicas, fija la IP y valida TLS/SNI, no usa cookies/auth/proxy heredados. GET únicamente. No hay reintentos.
- `_https_get_once` cuenta bytes, descomprime gzip con límite y rechaza otras codificaciones. Fetcher reduce timeout al tiempo restante y serializa solicitudes. DNS/TLS se incluyen en el timeout real del hijo, aunque no sean solicitudes HTTP aparte.
- Fetcher mantiene parada irreversible por403/429, desafío de acceso y presupuestos. **Un error genérico de transporte se propaga y el loop general lo registra por nodo, pero puede continuar con la cola**. Lo mismo sucede con ciertos destinos de redirección rechazados; no garantiza la parada global más estricta de este piloto.
- `max_seconds` controla inicios/esperas/deadlines HTTP, pero no es un watchdog duro sobre todo el parsing y exportación posterior. No se promete un máximo absoluto de proceso de120s usando solo ese campo.

`offline-procedure-proofs.json` conserva dos comprobaciones nuevas con transporte inyectado y dominio example.invalid, sin DNS/HTTP reales: max_urls5/depth0/sitemaps0 solo consulta robots y home; una excepción de transporte en /a no impide consultar /b. No son resultados de producción ni repetición de las suites aprobadas.

## Invocación concreta y bloqueo

No existe hoy una invocación soportada que garantice simultáneamente la selección de estos cinco destinos, ninguna navegación adicional y todas las paradas globales exigidas. La ayuda real de `seo crawl --help` no ofrece lista de destinos/semillas/resume. No se presenta un comando de red que simule cumplirlo, ni se inventan flags disponibles.

Tampoco se puede cambiar public_url a cada producto: Policy exige raíz. Un runner que reimplemente robots, cola y redirects alrededor de Fetcher sería un segundo crawler y se descarta. Alterar/falsificar sitemap o respuestas para dirigir el recorrido también se descarta.

## Adaptación mínima propuesta, sujeta a autorización y revisión

Extender el mismo crawl con un modo de alcance cerrado, opt-in, sin cambiar el modo general. Todavía no hay diff ni API/flag implementado. Candidatos: crawler.py para semilla/cobertura/paradas;engineering.py para validar una lista local y transmitirla;tests unitarios e integración directamente relacionados. Solo si la revisión demuestra necesidad, se propondrá un cambio adicional al transporte; no se modifica por anticipado.

1. Validar antes de red exactamente cinco URLs únicas del manifiesto, proyecto/origen y hash. Mantener la lista literal aprobada; no completar automáticamente con otras páginas.
2. Leer solo robots y esos cinco destinos. No solicitar home, sitemaps, imágenes, JS, CSS, canonical, enlaces salientes o URLs detectadas en HTML. Enlaces observados se registran sin programar su descarga.
3. Reutilizar la misma lectura/parser de robots, Fetcher, Policy, https_get, clasificación y auditorías. Tras robots conocido, comprobar permisos para cada destino. Si el agente propio no puede acceder, registrar sin descargar; si Googlebot no puede, no afirmar indexabilidad. Propuesta conservadora del piloto: detener el lote para revisar cualquier bloqueo de robots de uno de los cinco.
4. Reutilizar el loop de redirecciones y validar cada salto antes del GET, incluidos robots. Máximo3saltos globales y por cadena;los saltos solo pueden ser destinos seguros del mismo origen de una cadena iniciada en la lista aprobada. Una cadena que confluyen dos URLs puede reutilizar una respuesta del mismo run si se conserva la asociación; no inventar otra petición o duplicar resultados.
5. En modo cerrado, cualquier rechazo de origen/ruta/DNS/IP/TLS,403/429, robots desconocido o presupuesto agotado deja estado terminal y cancela destinos restantes;no continuar la cola ni cambiar transporte. Procesamiento incompleto se registra, nunca se convierte en cobertura completa.
6. El scope de cobertura será los cinco destinos y sus cadenas;no cobertura completa del sitio ni grafo exhaustivo. Guardar solicitado/final, redirects, motivos y destinos no iniciados. No actualizar matriz con respuestas parciales como si se hubieran completado.
7. Para120s absolutos hace falta un límite externo que abarque el proceso y sus hijos, no otro motor. Revisar el uso de una utilidad de timeout ya instalada o un mecanismo existente de cancelación de grupos;validar antes con fixtures que no quedan hijos DNS/TLS activos. Presupuesto del watchdog debe incluir su gracia de terminación dentro de120s. Un checkpoint de progreso es necesario para distinguir peticiones iniciadas de pendientes si se cancela;su ausencia bloquea ejecutar. No se afirma que ese mecanismo esté validado hoy.

## Solicitudes auxiliares y presupuesto propuesto

Sin redirecciones:1robots +5documentos =6GET. Con hasta3saltos globales compartidos:como máximo9GET. El techo12 es un hard cap, no una meta ni autorización para lecturas nuevas;las3plazas restantes no se rellenan. No hay sitemap ni home en el modo propuesto. Si se necesitase cualquier lectura extra, documentar y aprobar antes, sin superar12.

Tiempo/bytes:serial;timeout cada GET=min(20s,restante);cada respuesta≤2.000.000bytes comprimidos y decodificados;máximo teórico de12respuestas≤24.000.000bytes por cada dimensión. Los cuerpos pueden interrumpirse antes;el presupuesto de120s puede impedir completar los cinco y eso no es un resultado saludable ficticio.

## Pruebas requeridas para autorizar ejecución posterior

Solo fixtures nuevas:lista exacta/duplicados/origen;ausencia de home/sitemap/enlaces fuera de lista;robots200/404/410/desconocido/bloqueo;DNS/TLS/IP rechazada aborta toda la cola;403/429 sin solicitud posterior;redirects de robots y destinos con contador compartido;techo12 y frecuencia con reloj virtual;gzip/bytes2MB sin ampliar el transporte;deadline120s con hijos recogidos y checkpoint;contenido faltante/incompleto no marca cobertura completa. Reutilizar pruebas anteriores donde no cambie el código, ampliar QA proporcional al diff que se apruebe.

## Autorizaciones separadas

Ahora solo se puede solicitar preparar un candidato local de esta adaptación y sus pruebas, sin integrarlo ni ejecutar red. Después: revisión dual del diff exacto, recibos, solicitud específica de integración local. Solo con integración y QA cerrados se presentará una invocación real del piloto para otra autorización independiente, con sus cinco URLs, hashes y presupuesto. No se hereda permiso para75URLs, GSC, tema o producción comercial.
