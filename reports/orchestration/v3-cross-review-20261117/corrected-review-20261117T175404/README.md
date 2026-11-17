# Revisión independiente del candidato corregido

**V3: needs_evidence. Claude: changes_requested. Sin integración ni activación.**

Se ejecutó exactamente una invocación de Claude mediante el transporte existente, sin wrapper duplicador, reintento, fallback ni cambios de límites. Recibió el JSON literal completo; salida estructurada válida, cambios vacíos y los tres archivos declarados. Duración: **163.479 segundos**, exit0; proceso recogido. No se ejecutaron Antigravity, producción ni pruebas adicionales.

## Identidad y recibos

- Parche: `c240b16f37ec13a84db4e54f656f15beda7316642c2e078e8d94b906d7ed6085`.
- Paquete congelado: `1f0de2c1e33d01863c1055266bd67362f714b7069b2583d1f2197b762064a188`; **396414 bytes**.
- Modelo/esfuerzo: `claude-sonnet-5-5` / `medium`.
- Límites conservados: inicio30s, primera salida CLI120s, inactividad90s y absoluto240s. Primera salida CLI no equivale a primer token de revisión.
- Coste reportado por el proveedor: USD 0.8362757; no estimación propia.

[Respuesta íntegra estructurada de Claude](claude-response-complete.json) · [Recibo](claude-receipt.json) · [Paquete literal](review-packet.json) · [Congelación y suficiencia](freeze.json) · [Preflight](execution-preflight.json) · [Postflight](postflight.json).

Se conserva la respuesta final completa, no razonamiento privado ni stderr crudo. El snapshot del proveedor contenía solo packet.json; fuentes candidatas/dependencias aparecen una vez cada una. Los dos diffs se incluyen porque fueron solicitados, sin diffs automáticos de archivos de contexto. El sandbox montó únicamente autenticación nativa acotada del proveedor; no HOME completo, clientes ni credenciales comerciales. La red del transporte existente no tiene firewall de destinos: herramientas/MCP/subagentes están deshabilitados por CLI; esto no certifica egreso API-only.

## Comparación O1/O2/O3

| Hallazgo anterior | Evaluación de Claude en el nuevo diff | Pendiente |
|---|---|---|
| O1 — registro | Mayormente resuelto: registro local eliminado, política central y dos revisores no autores conservados | N4: procedencia de principal/capacidad; integración real pendiente |
| O2 — recibos | Parcialmente resuelto: legado intacto y binding separado | N1: hash de política incompatible; N5: productor QA sin cobertura exigida |
| O3 — cierre | Parcialmente resuelto: estados e historial añadidos | N2: gate no consume la máquina; N3: historial incompleto/migración no definida |

[Comparación completa](comparison.json). No se borró changes_requested anterior ni se fabricaron recibos de cierre. El dictamen actual tampoco autoriza integración.

## Nuevas objeciones

**Cuatro MEDIUM**:

1. **N1:** participation_sha256 se calcula con serializaciones distintas en el productor existente y el gate. La comparación local de hashes confirma la diferencia sin ejecutar QA ni llamar a un proveedor. También falta el contrato de permissions_sha256 en el contexto original.
2. **N2:** evaluate cierra por respuesta+recibo y no consume el estado/eventos de advance_objection; las pruebas de una ruta no acreditan la otra.
3. **N3:** historial opcional, omisión posible y migración entre diffs sin contrato de salida. Los hallazgos anteriores se procesan después de algunos continue. El riesgo de omisión depende de un llamador que incumpla la frontera del controlador; no hay bypass de producción demostrado.
4. **N4:** binding con hash sin clave comprueba consistencia, no procedencia de principal/capacidad. Esta limitación ya se documentaba; falta reflejarla en el resultado/API y separar la sucesión de dictámenes de la identidad.

**Cuatro LOW**: N5, integración del QA/política; N6, lecturas repetidas acotadas; N7, acoplamiento privado existente; N8, complejidad y dos harnesses de pruebas. No son permiso para un refactor amplio.

[Auditoría del controlador](controller-findings-audit.json) conserva las citas originales y añade precisiones/rangos reales. En particular, hay citas de líneas imprecisas y el acoplamiento N7 no demuestra por sí mismo duplicidad semántica. La sugerencia de probar un registro con CommandCode no lo habilita: permanece deshabilitado y no se ejecutó.

## Evidencia y pruebas pendientes

Las60 pruebas conservadas son evidencia anterior suministrada al revisor; Claude declara no haberlas ejecutado. No se repitieron ni esas60 ni las159. Tampoco se cambiaron candidato, modelos, política ni orquestador operativo; hashes posteriores íntegros.

Pendientes, previa autorización de corrección/pruebas aisladas: contexto real frente a hash canónico; productor QA con cobertura explícita; cierre único consumido por evaluate; integridad/completitud y migración del historial; principal acreditado frente a datos del llamador. Las objeciones son revisión estática y contraste local, no nuevas reproducciones ejecutadas.

## Siguiente acción mínima

Preparar la defensa incremental y un alcance de corrección aislada para **N1–N4**, con reproducciones focalizadas y sin tocar el orquestador operativo. No repetir discovery ni llamar otra vez a Claude por esta autorización. Cualquier nueva versión exige identidad nueva y revisión independiente autorizada; Antigravity sigue bloqueado.

[ADR de esta revisión](ADR.json): needs_evidence, integración/activación/producción no autorizadas. Los ADR y recibos anteriores permanecen intactos.
