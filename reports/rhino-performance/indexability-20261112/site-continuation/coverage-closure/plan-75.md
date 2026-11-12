# Verificación de los 75 destinos — procedimiento pendiente de aprobación

No se ejecutó ninguna de estas solicitudes. La lista cerrada es [pending-75.csv](pending-75.csv): 11 productos y 64 artículos, tomados de la matriz conservada, sin añadir parámetros o rutas.

## Condiciones antes de hacer red

1. Completar únicamente las etapas pendientes del consejo original sobre el parche V4 exacto, conservando propuestas válidas. El fallo de Codex debe estar resuelto con una respuesta válida del proveedor original; la auto-revisión del principal no sustituye esa intervención. Vincular los recibos de restricciones a la alternativa y al hash correctos; el QA general no acredita por sí solo cada restricción.
2. Mantener el hash del parche `7a5a7066bb22d2f87c18286100a9fba0ce76e50e53a8cf9b211821d0eba8b4a0`. Si aparece un defecto que requiera otra versión, preparar otro diff/manifiesto y revisar la nueva versión; no cambiar este hash silenciosamente.
3. Cuando las condiciones de AGENTS estén satisfechas, presentar autorización específica de integración **local del motor**: seis módulos y tres tests, respaldos, hashes antes/después y reversión propia. No incluye el tema ni un despliegue. Aún no está aprobado ni se solicita aplicar un parche bloqueado.
4. Solo tras la autorización, integrar el candidato exacto y ejecutar el QA posterior en el workspace. El QA aislado nuevo no reemplaza ese control.
5. Aprobar el plan concreto de red y verificar que realmente utiliza el transporte revisado: GET, TLS/SNI y DNS/IP pública fijada, mismo origen, control de cada redirección, exclusión de rutas privadas/comerciales, robots de Googlebot y del agente, límites y parada ante 403/429. No sustituir el transporte ni desactivar controles.

## Piloto y ampliación

Comenzar con cinco URLs pendientes de la lista cerrada, con ambos tipos de página representados. Límites propuestos: concurrencia1;0,5solicitudes/s;máximo12solicitudes incluyendo controles/redirecciones;120s totales;timeout20s por solicitud;2MB por respuesta y descompresión;máximo3redirecciones validadas. No son autorizaciones para ejecutar ahora.

Leer robots vigente al iniciar la fase de red es un control de seguridad, no repetir una auditoría de categorías. Si cambia respecto al documento conservado, conservar ambas versiones y reevaluar. No seguir enlaces nuevos ni acciones comerciales. Ante robots desconocido, origen distinto, IP no pública, certificado inválido, presupuesto agotado o 403/429: detener y registrar; no reintentar ni cambiar de transporte.

Revisar el piloto antes de ampliar. Si resulta aprobado, verificar el resto en lotes acotados conservando un checkpoint por URL; no repetir URLs con evidencia válida. Presupuesto y ampliación deben quedar registrados antes de cada lote. Las 75 no se convierten en un rastreo masivo automático.

**Límite de la interfaz existente:** `seo crawl --help` no ofrece selección de semillas, exclusión de URLs ya comprobadas ni resume por lista. No existen flags `--urls` o `--skip` en esa interfaz. No se inventa un comando que garantice apuntar solo a estas 75. Antes del piloto debe revisarse una invocación acotada de las APIs existentes del mismo transporte aprobado, o acordarse qué lecturas de paso son estrictamente necesarias para el crawler actual. No se ha construido un runner alternativo ni añadido funcionalidad al motor para eludir esta condición.

## Evidencia por URL

Conservar URL solicitada y final, cadena completa de redirecciones y HTTP, fecha, versiones/hashes del motor, decisiones robots de ambos agentes, cada meta robots/googlebot y cada cabecera X-Robots-Tag física por separado, canonical único, title, H1, resumen/hash de main y tipo de plantilla. Conservar evidencia de incertidumbre: no sustituir datos ausentes por valores favorables. No guardar cookies, secretos, tokens ni datos de clientes.

Aplicar el clasificador tipado aprobado y distinguir: descubrimiento observado, rastreo permitido/comprobado, candidatura técnica y estado conocido en Google. HTTP200 o canonical propio no prueban indexación. Un redirect no es necesariamente error; un noindex no se elimina automáticamente. La prueba no compra, modifica carrito, envía formularios ni altera catálogo.

## Actualización de la matriz

Añadir resultados reales sin borrar las observaciones previas: fecha/fuente nuevas, tipo de comprobación, redirect, señales y estado técnico. Mantener las quince inspecciones GSC previas con sus fechas, salvo nueva consulta justificada y explícita. Revisar discrepancias antes de cambiar prioridades. No modificar menús, canonicals del blog, contenido o la paginación publicada como consecuencia automática de un hallazgo.
