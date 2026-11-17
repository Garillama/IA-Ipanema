# Defensa documental del autor — O1, O2 y O3

Codex continúa siendo autor. Se recuperó la propuesta original revalidada, sin nueva inferencia. Esta defensa no es revisión independiente ni cierra objeciones. El diff anterior y la respuesta íntegra de Claude permanecen intactos.

## O1 — aceptación con precisión de impacto

**Acepto** que PARTICIPANTS mantiene una autoridad contradictoria respecto del registro central. **Refuto parcialmente** que este helper opcional ya cause un bypass operativo o que consulte la política dual para bloquear: no está integrado y precisamente no consulta ese registro.

Evidencia: code_review.py anterior19,104–107,179 frente a adapters.py agent_policy/NAMES/require_agent. La propuesta original de Codex ya exigía identidad del controlador y mantener el bloqueo si falta un proveedor; el universo local fijo contradijo ese objetivo.

Causa: se confundió la identidad esperada del diseño V3 con participantes realmente habilitados. Alternativas: otra lista V3 (rechazada), reducir a un revisor (rechazada), cambiar models.json ahora (fuera de alcance), o consultar la política central y mantener dos revisores obligatorios.

Recomendación: leer agent_policy del registro único; separar principal/proveedor, capacidad acreditada del transporte y autorización operativa. Un hijo conserva el principal y nunca se acepta como otro proveedor. Con la política dual actual no habrá dos revisores no autores: needs_evidence, sin habilitar Antigravity. La incorporación futura requiere migrar el registro/adaptador central por separado, no cambiarlo desde este helper.

Archivos: code_review.py y pruebas; wrapper council.py solo para parámetros opcionales. Riesgos: política cambiada durante revisión; capabilities declaradas sin respaldo real. Pruebas: registro dual no aprueba, proveedor deshabilitado rechazado, política obsoleta invalida, hijo/identidad sustituidos rechazados y fixture de política futura explícitamente simulada.

## O2 — aceptación; compatibilidad no significa aprobación retroactiva

**Acepto** la incompatibilidad: el helper exigía alternative_sha256 en source/qa, pero los productores actuales no lo emiten. No es válido añadir ese campo y fingir que ya estaba acreditado.

Evidencia: proof/QA del helper148–168 y source_ledger/qa:baseline de council_runtime132–138. Las fixtures originales añadían un fingerprint a todos los tipos y ocultaban la discrepancia.

Causa: se reutilizó el parser del ledger confundiendo validez de formato legado con vinculación del candidato nuevo. Alternativas: mutar recibos antiguos (rechazada), relajar fingerprint y aceptar QA sin alcance (rechazada), reescribir todos los productores operativos (fuera de alcance) o una envoltura explícita versionada.

Recomendación: conservar recibos originales byte/objeto a objeto y crear bindings v2 separados mediante un productor local explícito. El binding registra hash del recibo original, candidato, contexto, permisos y fuentes realmente revalidadas; no afirma que el productor antiguo emitió esos campos. Un source legado puede vincularse releyendo su hash. Un QA legado sin artefacto verificable y hashes de alcance NO se convierte en prueba del candidato: se conserva y queda pendiente. Constraints/resolutions con otra identidad se rechazan, no se retargetean.

Archivos: code_review.py y pruebas; contrato de bindings documentado. Riesgos: llamador del controlador deshonesto o artefacto QA sin cobertura; no se promete resolverlos con un booleano del modelo. Pruebas: formato real de source/qa:baseline, no mutación del legado, permisos/hash/contexto viejos, artefacto incompleto, QA fallido, recibo de otra alternativa y binding adulterado.

## O3 — aceptación del contrato incompleto; refutación del hash forzoso

**Acepto** que cerrar una objeción no elimina el changes_requested global y faltaba explicitar la re-revisión. **Refuto** que una refutación documental exija necesariamente cambiar el candidato: puede existir una revisión nueva del mismo hash.

Evidencia: evaluate195–204 añade motivos globales;223–240 resuelve solo objeciones. La propuesta original ya exigía que el autor no cerrase sus propias objeciones.

Causa: se mezclaron estado del hallazgo y decisión global del revisor. Alternativas: borrar changes_requested al recibir una respuesta (rechazada), exigir un diff artificial (rechazada), o historial append-only con confirmación original y re-revisión explícita.

Recomendación: estados open, author_answered, correction_proposed, new_evidence, refuted, resolved y review_pending. Responder o proponer corrección no cierra. Refutar/resolver exige revisor originario acreditado y binding de resolución. Una corrección real cambia identidad y exige nuevos recibos/revisiones. El changes_requested histórico permanece: solo una nueva revisión acreditada con supersedes explícito puede sustituir su efecto actual; no se borran hallazgos HIGH omitidos en la respuesta nueva.

Archivos: code_review.py, wrapper council.py y pruebas. Riesgos: colisiones de IDs, cierre con pruebas de otra revisión, omisión de un HIGH previo o reasignación del origen. Pruebas: defensa insuficiente, cierre por autor rechazado, corrección→review_pending, resolución/refutación por origen, mismo hash con revisión nueva y supersedes, no borrado del historial ni omisión de HIGH.

Estado de O1/O2/O3: respuestas del autor preparadas; objeciones pendientes de revisión independiente. Ningún proveedor fue invocado ni se activa V3.
