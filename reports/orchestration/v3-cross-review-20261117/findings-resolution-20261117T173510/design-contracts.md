# Diseño incremental y contratos — O1/O2/O3

Estado: propuesta del autor, **needs_evidence**, sin integración. Se modifica únicamente la copia aislada de los tres archivos originales; no se modifican adapters.py, models.json, engine, council_runtime ni permisos operativos.

## O1: identidad, capacidad y autorización

`evaluate` consulta `adapters.agent_policy()` como única autoridad de participantes. Se elimina PARTICIPANTS. La identidad del candidato incluye `context.participation_sha256`, calculada sobre la política completa; una política diferente invalida la suficiencia del contexto.

Tres conceptos distintos:

- Identidad: proveedor principal acreditado por el transporte del controlador, no por texto del modelo. `provider`, `actor_kind=principal`, `parent_actor_id=None`.
- Capacidad: el controlador debe acreditar `capability_verified=code_review_readonly` con evidencia del transporte y aislamiento. El helper valida el contrato, **no realiza autenticación ni demuestra aislamiento**.
- Autorización: membresía actual en la política central, candidato y permisos vinculados. Una capacidad técnica no habilita a un proveedor desautorizado.

Se mantienen **dos revisores no autores**. Con Claude+Codex habilitados y Codex autor solo queda un proveedor distinto; el requisito continúa pendiente. Un envelope Antigravity no autorizado se rechaza. Las pruebas de tres participantes utilizan una política simulada explícita en memoria; no habilitan Antigravity ni cambian el registro central. Incorporarlo realmente requiere, por separado, transporte e identidad demostrados y cambio explícitamente autorizado de política/adaptador.

## O2: adaptación compatible y explícita de recibos

El ledger legado y su parser siguen intactos. `read_legacy_receipts` acepta sus formas actuales, incluida la ausencia de alternative_sha256 en source/qa; aceptar formato no equivale a probar el nuevo candidato.

Nuevo productor **local y opcional**: `bind_receipt(receipt, candidate, root=..., permissions=..., qa_report=..., principal=..., resolution_state=...)`. Emite un objeto separado `contract_version=2`:

| Campo | Procedencia y comprobación |
|---|---|
| receipt_id, legacy_sha256 | ID y hash del objeto legado íntegro, sin mutarlo |
| candidate_sha256 | Fingerprint del candidato actual del controlador |
| context_sha256, permissions_sha256 | Contexto actual y permisos realmente suministrados |
| checked_source_files | Hashes de bytes revalidados por el controlador |
| principal | Metadatos acreditados de transporte; solo obligatorios en revisión/resolución |
| purpose, subject, resolves | Tipo, objetivo y lista explícita del recibo original |
| resolution_state | Confirmación explícita resolved/refuted para resolución |
| method | controller_revalidation_v2; no atribuye datos al productor antiguo |
| binding_sha256 | Hash canónico del binding sin este campo |

Reglas de migración:

1. El contexto legado debe coincidir en proyecto, run_id, objetivo y archivos; cualquier clave adicional existente también debe coincidir. Las claves nuevas no se insertan retroactivamente en el recibo.
2. Fuentes: lectura única acotada; esos mismos bytes se usan para hash y citas. Máximo 64 archivos, 2 MB por archivo, 4 MB total. Si faltan o cambiaron, no hay vinculación válida. Las eliminaciones quedan pendientes de contexto histórico, sin aprobación ficticia.
3. QA: exige el artefacto original cargado por el controlador, hash según el algoritmo del productor legado y cobertura exacta de archivos en `checked_source_files` o `verification_state.workspace`; también deben coincidir executed/passed. Un QA viejo sin cobertura se conserva pero **no se puede promover** a prueba actual. Solo reejecutar el QA afectado o aportar su artefacto original suficiente, previa justificación.
4. Si un recibo ya contiene alternative_sha256 distinto, se rechaza; nunca se reasigna a otro diff.
5. Revisión/resolución: exige principal autorizado, evidencia del transporte y vínculo al candidato. `resolves` debe ser lista.
6. `evaluate(..., bindings=(), review_history=())` conserva la firma anterior con argumentos opcionales; sin bindings el resultado es needs_evidence. Compatibilidad sintáctica y del parser no implica conservar una aprobación insegura.

Los hashes detectan cambios; **no son firmas ni acreditan por sí mismos quién produjo un recibo**. El almacén del controlador y la verificación nativa de identidad siguen siendo una frontera de confianza. No se conectó este productor al orquestador operativo ni se acreditó una identidad real con fixtures.

## O3: estados explícitos e historial

`advance_objection` devuelve una copia con eventos acumulados; no borra el registro previo.

| Evento | Actor permitido | Estado resultante | Condición |
|---|---|---|---|
| author_answer | Autor | author_answered | Mismo candidato; no cierra |
| propose_correction | Autor | correction_proposed | Nuevo hash; exige revisión nueva |
| add_evidence | Controlador | new_evidence | Referencias de evidencia; no cierra |
| request_review | Controlador | review_pending | Revisión todavía pendiente |
| refute | Revisor originario, distinto del autor | refuted | Respuesta previa del autor y binding v2 de resolución válido para esa objeción/candidato |
| resolve | Revisor originario, distinto del autor | resolved | Las mismas exigencias de independencia y evidencia |

Estado inicial open. No se reabre un terminal mediante una respuesta del autor; se necesita un nuevo registro vinculado. Una confirmación de otra objeción o candidato no sirve.

Separación respecto al dictamen global:

- Cerrar una objeción no borra changes_requested ni un challenge fail de la revisión actual.
- Una revisión nueva acreditada del **mismo candidato** puede sustituir el efecto del dictamen previo mediante `supersedes_review_ids` suministrado por el controlador y vinculado al transporte. El historial permanece.
- Los HIGH/BLOCKER anteriores no desaparecen porque el revisor omita su ID; se conservan hasta resolución acreditada. No se permite redefinir el contenido de un ID existente ni duplicarlo dentro de una revisión.
- Si el historial adverso pertenece a **otro candidato**, se conserva y se emite `prior_candidate_review_requires_migration`. La migración verificable de objeciones entre diffs no se automatiza en este candidato. Será necesaria una conciliación explícita del controlador y revisión nueva antes de aprobar; modificar el hash no limpia el historial.

El reducer y el gate son contratos de controlador: no se deben aceptar record/history/principal/binding como campos arbitrarios enviados por modelos. Esta corrección no implementa un almacén autenticado nuevo ni altera el orquestador.

## Pruebas y límites

29 pruebas focalizadas: autoridad central y cambio de política, principal/hijo/capacidad, recibos legados sin campos nuevos, permisos, fuentes obsoletas, QA incompleto y fallido, bindings alterados, resolves tipado, estados, confirmación del origen, terminales, historial, supersedes y conservación de HIGH entre revisiones/diffs.

Se conservan los 31 casos anteriores del gate y se migran sus fixtures a los contratos nuevos; todos se ejecutaron junto con los 29 casos focalizados: 60/60 aprobados. La repetición de ese subconjunto está justificada por el cambio real del gate. El original y sus respaldos permanecen intactos. No se repitieron las 159 pruebas completas ni se atribuye al candidato corregido aquel resultado histórico. Las suites de council y consumidores deben evaluarse según el alcance final antes de integrar. El resultado actual no es aprobación de compatibilidad universal, rendimiento ni proveedores reales.

O4/O6 quedan como riesgos documentados, sin refactorización adicional. La comprobación del nombre de función en citas sigue siendo una búsqueda textual, no un analizador semántico. No se promete detección automática de duplicidad semántica: las fixtures prueban el gate ante hallazgos suministrados.
