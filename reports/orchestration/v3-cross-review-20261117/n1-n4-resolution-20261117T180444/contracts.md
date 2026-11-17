# Contratos de la corrección aislada N1–N4

Esta es una propuesta del autor, no un contrato integrado o aprobado por los revisores. No existen nuevos proveedores, almacenes, autenticadores o ejecutores: solo helpers y una interfaz de lectura dentro del gate opcional.

## Contexto /1 y hashes

`CONTEXT_CONTRACT = ipanema-code-review-context/1` define `context_hash(value)`:

- JSON con `sort_keys=True`, `ensure_ascii=True`, `allow_nan=False`, separadores explícitos `(', ', ': ')`.
- Codificación UTF8 y SHA256 hexadecimal minúsculo.
- Orden de claves irrelevante; orden de listas relevante. NaN/Infinity se rechazan.
- Para el dominio JSON válido de la política actual coincide con `council_runtime.binding`, que usa `json.dumps(..., sort_keys=True)`. La prueba llama a la función productora real local; no simula su algoritmo como si fuera evidencia del productor.

`adapt_context` es un productor aislado explícito: recibe contexto legado, política, permisos autorizados y lineage_id; devuelve una copia que declara el contrato y calcula participation_sha256/permissions_sha256. No modifica el productor operativo ni el recibo legado. Un hash obligatorio ausente o desconocido se rechaza. La identidad/alcance del candidato conservan fingerprint con el formato previo `_hash`; no se reinterpretan esos hashes como si fueran context_hash. Los campos con funciones distintas se documentan y no se intercambian.

**Compatibilidad histórica:** source/QA sin fingerprint siguen parseándose. Para recibos sin context_contract se acepta un hash de política/permisos reconocido (canónico del productor o compacto del candidato histórico) solo si equivale al valor actual realmente suministrado; todos los demás campos existentes deben coincidir. Recibos que declaran el contrato /1 deben incluir sus campos obligatorios. No se añaden campos al original. QA exige artefacto y cobertura exactos; no se retargetea otra alternativa. Los bindings v2 anteriores no se aceptan como atestación nativa ni se promueven silenciosamente: requieren revalidación explícita.

## Fuente del controlador: procedencia y completitud

`ControllerEvidenceSource` es una interfaz de lectura Python, no deserializable desde el JSON del modelo. Su implementación predeterminada es unavailable. Solo código confiable del controlador podrá implementarla después de validar evidencia nativa. El gate rechaza un dict que intente reemplazarla.

| Método | Contrato |
|---|---|
| history(lineage_id) | Snapshot con lineage_id, reviews, complete_review_ids y objection_records |
| history_anchor(lineage_id) | Cabecera SHA256 de la colección completa de revisiones, obtenida independientemente del snapshot/modelo |
| attestation(receipt_id) | AdapterEvidence tipada, procedente de validación del recibo nativo; None si falta |
| migration(reference) | MigrationEvidence tipada del controlador para un solo hallazgo y par de candidatos; None si falta |

La cabecera se calcula sobre `{lineage_id, reviews}` mediante context_hash. El índice completo debe coincidir exactamente con los IDs de reviews y no contener duplicados. Se validan schema, candidato y autor histórico de cada revisión. El argumento legacy `review_history` puede contrastarse si se suministra; omitirlo no evita consultar la fuente completa. Un historial truncado no coincide con su cabecera/índice y no permite aprobar.

**Precisión respecto al diseño inicial de la defensa:** la cabecera se obtiene de la interfaz del controlador y no se añade al fingerprint del candidato. Una revisión sobre el mismo candidato puede pasar a ser histórica; incluirla recursivamente en su propia identidad produciría una dependencia circular. El controlador debe entregar snapshot y cabecera de un checkpoint consistente e inmutable. La autenticidad/completitud no surge de un self-hash: depende de esa implementación confiable, aún pendiente en el transporte real. Un proceso malicioso con ejecución dentro del controlador queda fuera de esta garantía; no se disimula esa frontera.

Límites: 64 revisiones, 256 registros de objeción y 128 eventos por registro; fuentes conservan los límites anteriores. Historial excesivo, incompleto o sin origen conocido se rechaza o queda pendiente, nunca se recorta para aprobar. Estas cotas no son un benchmark de rendimiento.

## Identidad del adaptador frente a identidad declarada

Cinco niveles separados:

1. **Declaración:** proveedor/actor/principal en JSON, insuficiente para acreditar identidad.
2. **Acreditación:** AdapterEvidence emitida desde validación nativa por la implementación del controlador.
3. **Capacidad:** code_review_readonly, principal sin padre; un hijo nunca cuenta como proveedor independiente.
4. **Permisos:** hash de permisos autorizados, candidato exacto y política central habilitada.
5. **Integridad:** hash de recibo/binding/contenido; no autentica por sí mismo los niveles anteriores.

AdapterEvidence vincula receipt_id, agent, candidate_sha256, permissions_sha256, binding_sha256, adapter_receipt_sha256, capability, actor_kind, parent_actor_id y supersedes_review_ids. Supersedes corresponde a la atestación de revisión, no al objeto principal. El gate verifica que todos los vínculos coincidan. La verificación concreta de ejecución nativa, recibo y capacidades es responsabilidad de la futura implementación del adaptador del controlador; un nombre de clase o hash hexadecimal no demuestra que se haya realizado.

`trust_basis` puede ser unavailable, adapter_verified o synthetic_fixture; el resultado expone también synthetic_only e identity_verified_by_hash=false. Las pruebas usan exclusivamente synthetic_fixture. Ningún resultado de esas pruebas acredita proveedores reales. Sin bridge real, el resultado es needs_evidence; el cliente actual no se convierte automáticamente en compatible por haber producido antes una revisión JSON válida.

## Cierre único y estados

`new_objection` conserva autor, revisor originario, ID, candidato de origen, hash de definición y una identidad de hallazgo derivada de esos datos. Estado inicial open.

`advance_objection` es el único reductor. El gate utiliza `replay_closure` para reproducir los eventos desde la semilla histórica y compara el registro reconstruido íntegro; no confía en un booleano closed, en terminales declarados ni en respuestas sueltas del autor.

Flujo normal:

`open → author_answered → new_evidence → review_pending → resolved/refuted`

- author_answer: solo autor, candidato actual.
- add_evidence: controlador, después de la respuesta, referencias comprobables del ledger/bindings del candidato actual.
- request_review: solo tras evidencia nueva.
- resolve/refute: revisor originario, distinto del autor; recibo de resolución vigente, identidad exacta del hallazgo, estado esperado y AdapterEvidence de su confirmación.
- Terminales inmutables; no se reabren mediante una respuesta del autor.

Una resolución no elimina el dictamen changes_requested de la revisión actual. Solo una revisión nueva acreditada puede sustituir explícitamente los IDs de dictámenes anteriores, que permanecen en el historial.

## Migración entre candidatos

MigrationEvidence conserva identidad de objeción, candidato de origen de la migración, candidato destino, revisor originario y autor. No contiene un booleano que cierre todos los hallazgos.

`propose_correction` exige esa evidencia del controlador y cambia únicamente el candidato de trabajo/estado correction_proposed. Después son obligatorias nueva respuesta, evidencia y revisión. La semilla histórica y la definición no se reescriben; una redefinición de un mismo ID no se acepta silenciosamente. Los hallazgos se registran antes de revisar envelopes actuales: BLOCKER sigue blocked y HIGH sigue changes_requested aun con revisores ausentes, obsoletos o sin acreditar.

La prueba end-to-end sintética demuestra dos puntos separados: migración sola no cierra; migración más flujo completo y revisión acreditada nueva sí permite superar el gate dentro de la fixture, sin borrar historia ni autorizar integración.

## Integración futura y QA

Se mantienen firmas previas con controller opcional; su omisión deja needs_evidence. El productor operativo no se modifica: necesitará un adaptador de contexto /1, evidencia de permisos autorizados, QA con hashes de alcance, una fuente de historial consistente y atestaciones nativas. Esa integración requerirá diseño revisado y autorización separada; no se simula como ya realizada.

No se modifican política central, modelos, orquestador, clientes ni producción. Antigravity y CommandCode permanecen deshabilitados. No se ejecutan nuevos proveedores. N1–N4 conservan sus identidades históricas y están pendientes de revisión independiente sobre el nuevo hash.
