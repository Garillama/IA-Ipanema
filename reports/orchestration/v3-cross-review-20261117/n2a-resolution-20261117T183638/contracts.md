# Contrato focalizado N2a / señal N4a

## Qué se verifica y qué no

El gate no es un evaluador semántico universal de lenguaje natural. Exige un resultado de verificación material desde la interfaz confiable del controlador, asociado a la objeción y candidato exactos, y después valida integridad, alcance, recibo y autoridad de cierre. Sin esa implementación, el comportamiento predeterminado es no admitir el paso incremental.

La implementación real del controlador deberá comprobar una demostración ejecutada, un hecho comprobado o una refutación documental sustentada. No puede copiar la afirmación del modelo ni crear MaterialEvidence porque cambió un ID/hash/texto. Debe comprobar procedencia, relación con el claim y hechos/argumentos ya evaluados. Las pruebas aquí son verificadores sintéticos acotados y no acreditan que ese bridge nativo exista.

## Interfaz de materialidad

`ControllerEvidenceSource.incremental_evidence(record, evidence_refs, candidate_sha256)` devuelve MaterialEvidence o None. Es una consulta de solo lectura/verificación de evidencia ya preparada; no debe lanzar proveedores, ejecutar código del modelo, ampliar permisos o hacer red no autorizada.

MaterialEvidence:

| Campo | Significado |
|---|---|
| objection_identity | Identidad histórica del hallazgo; no otro ID parecido |
| candidate_sha256 | Candidato que se reevalúa |
| evidence_refs | Fuentes utilizadas, incluidas fuentes originales cuando proceda |
| verification_receipt_id | Recibo de comprobación material; puede ser existente si realmente sustenta una reevaluación válida |
| artifact_sha256 | Integridad del artefacto comprobado; no prueba novedad semántica |
| kind | new_fact o documented_refutation |

`new_fact`: observación/hecho material no evaluado previamente. `documented_refutation`: demostración que refuta un supuesto o conclusión, aunque use los mismos hechos, palabras, archivos y referencias. No se exige modificar el código o inventar nuevo contenido.

El recibo de verificación debe estar probado y vinculado mediante el binding vigente del candidato. Campos del **nuevo productor explícito**, no atribuidos a productores legacy:

- kind=constraint, constraint=incremental_demonstration, method=controller_verified_demonstration.
- subject=identidad del hallazgo; claim_sha256 coincide con el claim original.
- basis_refs y material_kind coinciden con la demostración.
- sha256 coincide con el artefacto factual/documental verificado; executed/passed son verdaderos.

Cambiar únicamente una referencia o hash no satisface la interfaz. No se prohíbe artificialmente un ID de verificación ya disponible: una prueba específica comprueba que una refutación válida puede utilizarlo. La protección contra reutilización del mismo resultado en eventos ya evaluados es adicional a la verificación de materialidad, nunca su sustituto.

## Máquina única y procedencia

Se mantiene advance_objection como único reductor y replay_closure como consumidor de su mismo flujo. El reductor exige la demostración; el replay comprueba también recibo, binding, alcance y artefacto. El registro conserva claim y referencias originales bajo `ipanema-objection/2`; el evento retiene referencia/artefacto/tipo de la verificación que lo sustentó.

El resultado del callback y los registros se reciben del controlador confiable. Los eventos del autor/controlador son afirmaciones de esa fuente, no identidades autenticadas mediante un self-hash. La nueva verificación vincula el paso material con su recibo, pero no introduce firma criptográfica ni autentica un host comprometido. Un almacén real deberá preservar un snapshot consistente e impedir que contenido del modelo se promueva a esos objetos de controlador. El revisor originario todavía requiere su atestación independiente para cerrar.

Se preservan historial e identidad de objeción; versiones viejas sin prueba material suficiente quedan pendientes. No se modifican registros/recibos históricos para fabricar un cierre. Una actualización explícita deberá reconstruir el contexto original y solicitar reevaluación legítima.

## Ejemplos medidos en fixtures

- Claim original: sample.py tiene0 definiciones; bytes sin cambios contienen realmente1. El controlador cuenta las definiciones, registra baseline0/observed1 y verifica la comparación. Es refutación material sobre la misma referencia, sin novedad textual exigida.
- Claim coincidente con la observación: tiene1 y se cuenta1. Aunque alguien proponga otra cadena/ID/hash, no hay contraejemplo y se rechaza.
- Conteo todavía no evaluado: medición real1, baseline no medido. Se admite como hecho comprobado, no como afirmación del autor.
- Repetir los mismos hechos/demostración ya evaluados no crea materialidad. La fixture compara el contenido factual y el gate conserva además la protección de integridad/reutilización.

Las fixtures antiguas del gate usan mediciones sintéticas para ejercitar contratos; no demuestran por sí solas que un hallazgo editorial/comercial real sea verdadero. Las16 pruebas nuevas incluyen los casos factuales/negativos, metadatos falsos, claims ajenos, artefacto alterado y ausencia de la confirmación del origen.

## Resultado /2 y N4a

`result_contract=ipanema-code-review-result/2`.

| state | Significado |
|---|---|
| synthetic_pass | Pasaron condiciones dentro de una fixture; authorization_ready=false |
| approved_for_authorization | Resultado del contrato no sintético preparado para solicitar autorización, nunca permiso de publicación |
| changes_requested | Cambios/objeciones pendientes |
| needs_evidence | Falta evidencia obligatoria |
| blocked | Restricción/objeción crítica pendiente |

implementation_allowed, production_authorized y activation_allowed siguen falsos. synthetic_only se conserva; el consumidor ya no necesita leerlo para distinguir el estado principal de una prueba. Los consumidores futuros deben aceptar la versión /2 explícitamente y rechazar estados desconocidos, sin convertir synthetic_pass en aprobación real. El schema de entrada de revisores no cambia.

## Compatibilidad y pendientes

- N1: context/1 y serialización no se modifican; pruebas existentes pasan.
- N3: identidad, historial, severidad y migración se conservan; el registro añade datos originales necesarios para comprobar materialidad. No hay migración automática de cierres.
- N4: se reutiliza la misma interfaz de procedencia; solo se añade una consulta cuyo default es None. No se reduce la exigencia de la atestación del origen.
- council.py permanece idéntico al candidato anterior. No se modifican adaptadores, modelos, políticas o productores operativos.
- Se conserva N1a como dependencia futura: las identidades de alternativa legacy y candidato no se reinterpretan silenciosamente. No se inventan campos emitidos por el productor actual.

Riesgo principal: la corrección depende de que la futura implementación del verificador material del controlador sea real y revisada; una clase/hash no lo garantiza. Las pruebas actuales no se presentan como integración ni aprobación de proveedores. N2a y N4a requieren revisión independiente del nuevo diff; las valoraciones previas de N1/N3/N4 siguen asociadas a fb292ff7.
