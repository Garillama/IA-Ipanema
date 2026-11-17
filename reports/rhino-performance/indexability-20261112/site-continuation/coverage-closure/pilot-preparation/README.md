# Piloto SEO V4 — preparación y revisión incremental

12 noviembre2026. **Preparación documental completada; ejecución bloqueada por falta de una invocación soportada para cinco destinos cerrados.** No se modificó el motor integrado ni se hicieron solicitudes nuevas a Rhino o Google. No se repitieron191unitarias,13integraciones o quick.

## Cinco destinos exactos

Selección determinista: primeros dos productos y primeros tres artículos de la lista de75pendientes;pertenencia literal verificada contra la matriz. Es una muestra funcional de ambos tipos, no una muestra estadística ni cinco URLs recién comprobadas.

1. **Producto:** https://rhino-performance.com/productos/pistola-de-masaje-gun-pro/
2. **Producto:** https://rhino-performance.com/productos/tina-de-hielo-tub-air/
3. **Artículo:** https://rhino-performance.com/blog/posts/la-presoterapia-como-transformador-de-tu-salud-mental-relajacion-y-recuperacion-127cdc829590/
4. **Artículo:** https://rhino-performance.com/blog/posts/el-fro-no-es-un-castigo-es-una-herramienta-cbe9a25855f8/
5. **Artículo:** https://rhino-performance.com/blog/posts/faja-de-compresion-lumbar-el-soporte-que-tu-espalda-agradecera-047c381cf3ac/

[Manifiesto de destinos y procedencia](targets.json) · [cinco filas originales de cada CSV](source-excerpts.json). Se conservaron rutas literales, números de registro y hashes de los CSV, fuentes de sitemap y enlaces HTML anteriores. No se abrieron esas URLs;su HTTP individual continúa pendiente.

## Transporte actual e invocación

El transporte aprobado cumple GET, origen exacto, IP pública fijada, TLS/SNI, límites de cuerpo/descompresión y timeout del hijo, sin credenciales/proxies heredados ni reintentos. El crawler general empieza en home, procesa sitemap y navega por enlaces. La CLI no tiene un selector de destinos cerrados;max_urls limita nodos y no selecciona cinco URLs. Policy no permite usar un producto como home.

**No hay actualmente una invocación real compatible con este piloto.** No se ofrece un comando con flags inventados ni se ejecuta un runner alternativo. El bloqueo y la adaptación mínima están en el [procedimiento revisado](procedure.md) y las [aclaraciones posteriores](review-addendum.md).

Dos fixtures nuevas con transporte inyectado, sin DNS/HTTP, confirmaron:desactivar sitemaps y depth no cambia la semilla home;un error genérico en un destino no detiene necesariamente los siguientes en el modo general. [Reproducciones](offline-procedure-proofs.json). Este contrato de continuación del rastreo general no se presenta como regresión del motor aprobado;simplemente no satisface la parada más estricta requerida para este piloto.

## Presupuesto propuesto y auxiliares

| Recurso | Límite |
|---|---:|
| GET totales, incluidos auxiliares y saltos |12|
| Concurrencia |1|
| Frecuencia máxima |0,5/s;intervalo mínimo2s o más según robots|
| Tiempo absoluto |120s;watchdog/hijos/checkpoint aún sin validar|
| Timeout por GET |20s o restante menor|
| Cuerpo codificado y descomprimido aceptado |2.000.000bytes cada uno|
| Saltos |Propuesta conservadora:3globales compartidos;ratificar frente a interpretación por cadena|
| Auxiliar sin redirecciones |1GET robots.txt|
| Documentos seleccionados |5GET|
| Total sin saltos / con3globales |6 / máximo9GET|
| Sitemap,home,recursos y enlaces fuera de lista |0GET|

El techo12 no permite rellenar plazas con páginas adicionales. DNS/TLS consumen tiempo pero no son GET independientes. La cota del cuerpo no incluye tráfico de cabeceras/TLS;el transporte lee un byte centinela adicional para detectar exceso y rechazar la respuesta. No se promete un techo de tráfico bruto de24MB.

Robots debe comprobarse al iniciar la futura ejecución, no reutilizar su respuesta antigua como permiso vigente. Se mantienen códigos404/410 como ausencia conocida según el motor;otros estados/parser incierto no habilitan rastreo. Si una redirección exige www/CDN/origen distinto,detener,sin ampliar permisos.

## Interrupción y condiciones pendientes

El modo cerrado propuesto reutilizaría el mismo Fetcher/presupuesto. Debe parar toda la cola por403/429,robots desconocido,origen/ruta no autorizados,IP no pública,TLS inválido,timeout,codificación/gzip inválidos,ciclos o Location ambiguo/ausente y presupuestos. Cada documento redirigido debe volver a comprobar robots antes de solicitarlo.

El tiempo de Fetcher limita la red,pero no constituye un watchdog absoluto sobre parsing y reporte. /usr/bin/timeout está instalado;su cancelación de grupo/hijos aún no está probada en este flujo. El checkpoint debe distinguir petición pendiente,iniciada sin resultado confirmado y completada. No se afirma que una petición sin respuesta no llegó al servidor. Estos controles bloquean solicitar ejecución mientras no estén implementados y validados con fixtures.

## Revisión Claude + Codex

Se hicieron únicamente dos revisiones incrementales independientes del procedimiento,con runtimes reales y contratos válidos. No se reinició el consejo del motor. Ambos mantuvieron **blocked para ejecutar red**:

- claude: claude-sonnet-5-5 / medium;29.044s;[revisión](claude-pilot-review.json).
- codex: gpt-6.1-sol / medium;40.889s;[revisión](codex-pilot-review.json).

Coinciden en añadir alcance cerrado al mismo crawler y validar parada global,watchdog y checkpoint. Claude cuestiona que tres saltos globales sean necesarios si se usa el límite por cadena más12GET;Codex pide ratificar esa restricción adicional. El controlador conserva3globales como propuesta conservadora del texto del propietario,hasta que se ratifique el presupuesto definitivo. Se descartan resume,caché compartida u otro crawler por innecesarios.

Los CSV completos no se enviaron a los agentes;su selección fue verificada por el controlador y el extracto se añadió después. Las aclaraciones posteriores no se cuentan como objeciones resueltas ni como respuestas emitidas por el otro proveedor. No hay aprobación ficticia ni una decisión de red por mayoría.

## Operación exacta que puede autorizarse ahora

**Preparar y probar en aislamiento un candidato opt-in del crawler existente**, limitado a los módulos crawler.py,engineering.py y,si el checkpoint lo necesita,crawl_policy.py,más dos archivos específicos de pruebas. Conservar el modo general y todos los controles integrados. No integrar todavía ese candidato,no hacer red,no modificar tema,orquestador,modelos o AGENTS.

Aún no existe un diff de esa adaptación. Primero requiere autorización de preparación dentro de ese alcance;luego revisión del diff/hashes y autorización de integración. Solo después de integrar y hacer QA se podrá presentar el comando realmente soportado y solicitar autorización independiente para estos cinco destinos. No pedir permiso de ejecutar ahora un comando inexistente.

Las75URLs y sus estados anteriores permanecen intactos. [Estado estructurado](status.json) · [binding del motor integrado](source-binding.json) · [disponibilidad de timeout,no prueba de cancelación](deadline-capability.json).
