# Rhino — revisión contextual del piloto y preparación del lote 02

12 de noviembre de 2026. **Lote 2 preparado para solicitar autorización, todavía no ejecutado.** Solo se procesaron evidencias guardadas y se validó localmente el manifiesto nuevo. No se modificaron tema,motor,matriz,menús,canonicals,catálogo,contenido o apps. No se repitieron piloto 1,209 unitarias,22 integraciones,prueba120 s,GSC o discovery.

## 1. Qué indican realmente las advertencias

Fuente exclusiva: [proyección del informe guardado](saved-evidence-excerpts.json),con hash del informe original y punteros a sus nodos/enlaces. No se reconstruyó HTML ni JSON-LD crudo que no se conservaron.

| Observación | Clasificación y alcance |
|---|---|
| Product principal de cada PDP | No hay defecto demostrado en el subconjunto guardado:structured-data.page,$.mainEntity,@id igual a canonical,sin flags de estos cuatro controles. No certifica todo el schema o catálogo. |
|10 D010 sobre Product secundarios | **Posibles falsos positivos contextuales**:compara su mainEntityOfPage con la canonical contenedora;los10destinos tienen enlaces HTML correspondientes en main/carrusel. |
|10 D050 sobre nombres secundarios | **Posibles falsos positivos contextuales**:otro producto no tiene por qué llamarse igual que el H1 de la PDP principal. |
|10 D011 sobre Offer.url secundarios | Diferencia respecto a canonical contenedora compatible con otra entidad;la codificación amp%3B frente a href normal queda **needs_evidence**. No se conoce su origen ni efecto sin JSON-LD crudo. |
|10 D070 sobre imágenes | **needs_evidence**:hay placeholders GIF y srcset=true como booleano,pero no URLs candidatas,data-src,currentSrc o descargas. No demuestra imagen ausente o rota. |
|author de los3 artículos | **Forma escalar confirmada en la evidencia**,con B030/B100 del validador local. No es prueba de bloqueo de indexación ni de identidad editorial. |

Los autores declarados son **RHINO PERFORMANCE**,**Marketing RHINO** y **Erick**,respectivamente. Se preservan como cadenas declaradas:no se inventa nombre completo,Person,Organization,perfil o atribución editorial. Que un alias parezca una marca o persona no basta para decidir su tipo.

Hay un Product principal y cinco secundarios por PDP. Los secundarios tienen marcador structured-data.item y sus URLs aparecen en enlaces de producto dentro del carrusel. Esa correspondencia respalda el contexto,pero no prueba validez universal del marcado ni qué entidad escogería Google. Tampoco demuestra una regresión del motor respecto a otra versión.

Los40 flags D010/D011/D050/D070 se conservan como resultados originales;no se borran ni se convierten en40defectos reales. La comparación de campos comerciales no se completó:el grafo guarda nombres de propiedades,sin certificar precio,stock,variantes o verdad del catálogo. El contador raíz findings=0 del CLI anterior no se usa para negar los hallazgos anidados.

[Clasificación y recomendaciones estructuradas](classification.json). No se confirmó un bloqueo HTTP/robots/canonical nuevo;no hubo nuevas inspecciones Google.

## 2. Recomendaciones y riesgos de corregir sin contexto

- **Ahora:conservar tema y motor.** No hay base para reescribir el Product principal,canonical,H1 o productos relacionados por estas comparaciones.
- No forzar mainEntityOfPage/Offer.url de todos los productos hacia la PDP contenedora:alteraría la identidad de las entidades secundarias. No convertir productos distintos en variantes/ProductGroup sin catálogo autorizado.
- No retirar parámetros de recomendaciones para silenciar D011:puede afectar atribución,y su representación cruda no se conserva. La divergencia guardada no identifica al responsable del escape.
- No eliminar ni reemplazar imágenes por D070:la proyección resumida omite información necesaria. Se requeriría evidencia adicional autorizada para confirmar un defecto real.
- Para author,una mejora futura debe localizar primero el emisor nativo y confirmar la fuente editorial/CMS. Si corresponde una entidad tipada,usar la identidad real y un mecanismo soportado,sin duplicar BlogPosting ni inventar perfiles. Los marcadores guardados no atribuyen el fallo a un archivo de tema o aplicación concreta.
- No silenciar globalmente estas reglas en el motor:podría ocultar un error real del Product principal. La hipótesis de falso positivo contextual no autoriza modificar el validador ni demuestra una regresión.

La sugerencia de preservar HTML crudo se registra como trabajo futuro,no como capacidad del lote 2. La invocación actual conserva resultados derivados y hashes;no se añadió un flag de captura ni se reconsultaron páginas del primer piloto.

## 3. Cinco URLs nuevas, aún sin HTTP individual

Selección determinista:primeros2 productos y primeros3 artículos de pending-70.csv. Se verificaron pertenencia a la matriz actual,HTTP=not_observed,unicidad y ausencia de solapamiento con las cinco páginas del primer piloto. Es muestra operativa de dos tipos de página,no estadística ni prueba de disponibilidad actual.

1. **Producto:** https://rhino-performance.com/productos/compresor-pro-3-presoterapia/
2. **Producto:** https://rhino-performance.com/productos/brazos-presoterapia-pro-3/
3. **Artículo:** https://rhino-performance.com/blog/posts/guia-completa-para-cuidar-tus-botas-de-presoterapia-57e0c1076e6c/
4. **Artículo:** https://rhino-performance.com/blog/posts/cinco-consejos-infalibles-para-mejorar-tu-rendimiento-deportivo-con-la-presoterapia-92e925649706/
5. **Artículo:** https://rhino-performance.com/blog/posts/la-presoterapia-un-nuevo-escencial-en-la-rutina-de-los-campeones-997eed183e73/

[Manifiesto exacto](targets.json). **SHA256:** `7117b37560a94eb8477d6e1328e2999cd103d69857c1e01b87910b8d269b8f42`.

La procedencia por destino conserva nombre/hash del CSV pendiente y de la matriz,número lógico de registro y fuentes históricas de sitemap/enlaces. No se reinterpretaron las cadenas históricas de incoming_sources que contienen concatenaciones codificadas;son una limitación del registro anterior,no URLs adicionales que vaya a solicitar el lote.

El controlador leyó los CSV y comprobó la pertenencia. Los agentes revisaron los registros seleccionados y el recibo,no recalcularon hashes ni ejecutaron una auditoría por su cuenta.

## 4. Compatibilidad,presupuesto e invocación exacta

La validación local nativa _pilot_manifest aceptó las cinco URLs y el hash. Los cinco hashes del código integrado y las dependencias del transporte siguen coincidiendo con el piloto anterior. Se reutiliza el QA vigente;no se volvieron a ejecutar sus suites ni la cancelación larga.

| Restricción | Lote2 propuesto |
|---|---:|
|GET totales,incluidos auxiliares/saltos|12 máximo|
|Concurrencia|1|
|Frecuencia|0,5/s máximo,o menos por robots|
|Supervisión absoluta|120 s|
|Timeout porGET|20 s o restante menor|
|Cuerpo codificado y descomprimido|2.000.000bytes cada uno|
|Saltos globales|3 compartidos entre robots y documentos|
|Home,sitemap,links,assets,GSC|0 solicitudes|

Auxiliar obligatorio:robots.txt. Sin redirecciones:1robots+5destinos=6GET;con3saltos globales,como máximo9GET previstos. El techo12no autoriza añadir páginas. max-urls=8 es el margen para5destinos+3saltos,no una selección de8 páginas libres.

Se mantienen las paradas por403/429,robots desconocido/bloqueado,IP no pública,TLS inválido,redirección insegura,ciclo,codificación inválida o presupuesto agotado. El supervisor cubre parsing/exportación y conserva checkpoint. La autorización futura no garantiza cinco respuestas200:si debe parar,los destinos no comprobados siguen pendientes y no se reintentan automáticamente.

**Orden prevista,NO autorizada y NO ejecutada:**

```bash
python3 tools/ia.py --project rhino-performance seo crawl --targets-manifest reports/rhino-performance/indexability-20261112/site-continuation/coverage-closure/batch-02-preparation/targets.json --targets-sha256 7117b37560a94eb8477d6e1328e2999cd103d69857c1e01b87910b8d269b8f42 --allow-network --max-urls 8 --max-depth 0 --max-requests 12 --requests-per-second 0.5 --max-seconds 120 --timeout 20 --max-bytes 2000000 --max-sitemaps 0 --max-redirects 3 --concurrency 1
```

[Operación/argv](operation.json) · [orden preparada](command-NOT-AUTHORIZED.txt) · [recibo local de compatibilidad y pertenencia](controller-validation.json).

## 5. Revisión incremental Claude + Codex

Se conservaron dos análisis independientes sobre el mismo paquete factual y un único intercambio posterior de preguntas/respuestas. No se reinició el consejo del motor ni se repitieron preguntas de su integración. Las cuatro intervenciones reales pasaron schema y normalización con los modelos balanced existentes.

- Revisión independiente,**claude**:claude-sonnet-5-5 / medium,26.600s,[recibo](claude-review.json).
- Revisión independiente,**codex**:gpt-6.1-sol / medium,35.316s,[recibo](codex-review.json).
- Contraste,**claude**:claude-sonnet-5-5 / medium,32.071s,[recibo](claude-contrast.json).
- Contraste,**codex**:gpt-6.1-sol / medium,28.760s,[recibo](codex-contrast.json).

Codex pasó de proposed a approve para la solicitud del lote tras el contraste;Claude también aprobó ese alcance. Coinciden en preservar los límites de evidencia y no modificar automáticamente nada. La fila específica de respuesta de Claude sobre D011 trata D010/D050;su resumen,evidencias y notas sí expresan la separación contextual/codificación de D011. Se conserva esa salida tal cual,no se reescribió para aparentar un protocolo perfecto.

Las preguntas sobre lógica interna del validador y valores originales no se cerraron por consenso:el código/JSON-LD crudo no forman parte del paquete guardado. D011 y D070 siguen needs_evidence. Eso limita recomendaciones de corrección,pero no bloquea solicitar otro lote de lectura con el motor ya aprobado.

[Decisión incremental](ADR.json) · [estado](status.json). No se simula aprobación de Google ni de cambios al tema/motor.

## 6. Solicitud exacta pendiente

Se solicita autorización para **una sola ejecución** del comando anterior,únicamente con este manifiesto SHA256 y sus cinco URLs,robots y redirecciones seguras dentro del origen https://rhino-performance.com. Antes deberán comprobarse de nuevo código,hashes,origen y que los destinos sigan pendientes. No utilizar la autorización ya consumida del piloto 1.

No incluye nuevas lecturas de las páginas del piloto 1,70 URLs,GSC,home,sitemap,recursos,formularios,tienda o cambios de motor. Cualquier parada conserva evidencia;no habilita otra ejecución.

**Estado actual sin cambios:54/124 HTML con HTTP individual y70 pendientes (9 productos,61 artículos).** Las cinco seleccionadas siguen pendientes hasta que se autorice y ejecute el lote 2. No se marca una URL como indexada o comprobada por haber preparado su manifiesto.
