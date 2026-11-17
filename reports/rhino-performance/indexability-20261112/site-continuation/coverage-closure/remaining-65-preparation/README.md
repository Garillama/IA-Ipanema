# Cobertura restante SEO V4 — preparación de 65 destinos

Estado: **listo para solicitar autorización específica del lote03**. Esta preparación no ejecuta el crawler ni autoriza solicitudes. No se modificó el motor, la matriz vigente o la tienda.

## Cobertura acumulada conservada

| Inventario / evidencia | Total |
|---|---:|
| URLs conocidas | 125 |
| Páginas HTML | 124 |
| Documento sitemap XML | 1 |
| HTML con comprobación HTTP individual | 59 |
| HTML pendiente de comprobación individual | 65 |
| Productos pendientes | 7 |
| Artículos pendientes | 58 |
| Caminos HTML observados históricamente | 122 |
| Inspecciones GSC conservadas | 15 |
| URLs conocidas como indexadas en esas inspecciones | 10 |

Las 170 URLs con impresiones del periodo histórico no son el total indexado. No se consultó GSC. Las 59 páginas verificadas no quedan certificadas como indexadas ni libres de todo defecto. Los estados de Google, advertencias schema y posibles falsos positivos permanecen separados en la matriz.

Fuente del cierre anterior: [lote02](../live-batch02-20261113/README.md). Se conservaron sin modificación la [matriz CSV](../../url-matrix.csv), JSON y sus evidencias. [Snapshot de procedencia](matrix-snapshot.csv), [65 pendientes de origen](pending-65-source.csv), [lista definitiva con lote y tipo](pending-65-list.txt), [asignaciones CSV](url-assignment.csv).

## Partición determinista y hashes

Trece lotes de cinco: se conserva el orden de `pending-65.csv` dentro de cada tipo; se toman hasta dos productos restantes y se completa con artículos. Cuando se agotan productos se toman cinco artículos. No se normalizan, inventan ni sustituyen rutas.

| Lote | Productos | Artículos | SHA256 del manifiesto | Operación |
|---|---:|---:|---|---|
| 03 | 2 | 3 | `27375186058c9e953be9cd5e32a550864e852fa4fe49a38478b0b80db91b60be` | [Archivos](batch-03/operation.json) |
| 04 | 2 | 3 | `2e0222f4abeadad55b5bcc98f63bf0660771c2cf6630c4e66fef9f63f0adc56c` | [Archivos](batch-04/operation.json) |
| 05 | 2 | 3 | `a6e21fdd410e33e0394f168a28e4244ddb535370e876582459b499d8c603105e` | [Archivos](batch-05/operation.json) |
| 06 | 1 | 4 | `d8e56a7144bf6694e25e09a973c8def5564dc483e3c35fb6fc84a19f362adf8c` | [Archivos](batch-06/operation.json) |
| 07 | 0 | 5 | `451b86e22685c0e6657d41bb6cb0dbe22ff0db8dcfe7ec8e4826de9bea797fdc` | [Archivos](batch-07/operation.json) |
| 08 | 0 | 5 | `986a67b016b38be92718b35bc820b8cefc5fa10d310c66e462755e0c5f921f2c` | [Archivos](batch-08/operation.json) |
| 09 | 0 | 5 | `6b800083d76be4152c17f0cc6b937c2226afc59266074e3cda35ae0a85fcd46b` | [Archivos](batch-09/operation.json) |
| 10 | 0 | 5 | `f3b328166e9c817e163c0c78401fd53b1d405e519d4e77b281721dcb47d2fbf5` | [Archivos](batch-10/operation.json) |
| 11 | 0 | 5 | `d4d5717dacd3236005c6a6c73cbcdab058a7d61246338c70134895f83e680242` | [Archivos](batch-11/operation.json) |
| 12 | 0 | 5 | `4dee97f0cf689956cc97846145fc3cbd1d620b3153bbcb2bdf7c01411722b30d` | [Archivos](batch-12/operation.json) |
| 13 | 0 | 5 | `ab28cea5f15c41fdcdca840328e828219b728eb28efae31a2ad212263ba091c5` | [Archivos](batch-13/operation.json) |
| 14 | 0 | 5 | `e5833a05665651080a44b4aacd5c5fed3cd35a8bd8213d81fd2959fe5c34280e` | [Archivos](batch-14/operation.json) |
| 15 | 0 | 5 | `e6835d4f1804d59042172800306e8a38eb11b276572530d642c6f51a788b57eb` | [Archivos](batch-15/operation.json) |

Cero URLs repetidas entre lotes, cero omisiones y cero solapamientos con los diez destinos de las dos ejecuciones anteriores. Las65 coinciden exactamente con las filas `http=not_observed` de la matriz de preparación. Cada manifiesto pasó `_pilot_manifest` del motor integrado, sin ejecutar transporte. Tamaños inferiores a64KiB. [Índice completo](batch-index.json), [recibo del controlador](controller-validation.json).

## Presupuesto e invocación

Cada carpeta contiene `targets.json`, `operation.json` y `command-NOT-AUTHORIZED.txt`. Los argv conservan el comando ya validado; únicamente cambian la ruta del manifiesto y su SHA. No hay un ejecutor masivo ni un bucle que lance lotes.

Por lote: **12 GET máximos**, concurrencia1, máximo0,5/s (o menor según robots), supervisor absoluto120s, timeout20s/GET,2.000.000bytes por cuerpo codificado y descomprimido, tres redirecciones globales. Profundidad0, sitemaps0, max_urls8 permite cinco destinos y hasta tres nodos de redirección; no autoriza páginas adicionales. Auxiliares: robots.txt y redirecciones seguras permitidas, incluidos en los12GET.

Sin redirecciones se esperan6GET por lote. Los trece representarían78GET y, como techo contractual agregado,156GET y26min de supervisión; **ninguna cifra constituye autorización conjunta**, previsión garantizada de duración ni permiso para consultas sobrantes. El máximo real también queda acotado por tres saltos globales por lote.

## Secuencia y checkpoints

1. Revisar el lote concreto y solicitar autorización específica por manifiesto/hash/comando. Los13 estados iniciales son `pending_authorization`.
2. Justo antes de ejecutar, comprobar que sus cinco destinos siguen sin HTTP individual, y validar hashes exactos de manifiesto, motor y dependencias de transporte. La matriz viva cambiará tras cada lote: su hash inicial es procedencia, no un requisito inmutable que impida continuar.
3. Si un destino ya fue comprobado o existe cualquier discrepancia, bloquear y conciliar; no editar silenciosamente un manifiesto aprobado ni repetir una URL por inercia.
4. Con autorización, consumir un marcador único y ejecutar exclusivamente el comando de ese lote bajo el supervisor existente. Cada invocación genera un checkpoint nativo independiente. No se precrearon checkpoints ficticios ni se agregó un flag inexistente.
5. Conservar ruta del informe, checkpoint, supervisor y resultados inciertos. Actualizar únicamente las filas realmente observadas; mantener pendientes las no verificadas. Un lote parcial consume su autorización y no activa reintentos automáticos.
6. Registrar `executed` cuando corresponda, o `blocked` con su causa y si llegó a invocarse. No disparar el siguiente lote automáticamente. Volver a solicitar autorización individual.

[Registro de estados](batch-status.json) y [procedimiento/controles](execution-policy.json). El registro es documentación del flujo actual; no pretende ser un nuevo orquestador ni un bloqueo técnico adicional al mecanismo existente. El estado terminal se toma del supervisor y de los recibos de peticiones, conservando la limitación conocida de la cabecera histórica del checkpoint.

## Revisión Claude + Codex

Se solicita una sola revisión incremental del conjunto y un contraste compacto, con los mismos proveedores/perfiles equilibrados del proceso existente. No se reabre el consejo del motor ni se repiten sus suites.

- claude / review: contrato válido, decisión `approve`. [Recibo](claude-review.json).
- claude / contrast: contrato válido, decisión `approve`. [Recibo](claude-contrast.json).
- codex / review: contrato válido, decisión `approve`. [Recibo](codex-review.json).
- codex / contrast: contrato válido, decisión `approve`. [Recibo](codex-contrast.json).

[Estado de recibos](review-status.json), [ADR incremental](ADR.json), [cierre del controlador](controller-final-review.json), [semántica de estados](registry-semantics.json) y [comparación de los 13 comandos](all-operations-verified.json). Ambos proveedores emitieron aprobación real del plan, condicionada a autorización y preflight por lote. Estas aprobaciones no autorizan red, publicación ni correcciones de schema. Una fila de respuesta de Claude conserva una discordancia semántica con la pregunta asignada; su resumen/evidencia sí tratan la comparación de argv y el controlador la comprobó. Se preserva la respuesta original y se documenta la limitación, sin declarar perfección del intercambio por haber validado su JSON. Las condiciones del controlador prevalecen sobre afirmaciones de los modelos.

## Riesgos y límites

Los snapshots acreditan procedencia histórica, no respuestas actuales de producción. Un origen o contenido puede cambiar antes de su lote; por eso se exige el preflight vigente y se admite resultado parcial o bloqueado. No se garantiza indexación, cinco respuestas por ejecución ni cobertura administrativa absoluta.

Se preservan D010/D050 secundarios como posibles falsos positivos contextuales; D011/D070 necesitan más evidencia y author escalar no autoriza inventar autores o entidades. Ningún dato estructurado se modificó. No se pidió red a Rhino ni Google, ni pruebas de navegador o suites ya aprobadas.

## Primera autorización pendiente

[Solicitud exacta del lote03](request-batch03-authorization.md), con sus cinco URLs y hash. **No ejecutar hasta recibirla.** Los lotes04–15 seguirán pendientes de sus propias autorizaciones.
