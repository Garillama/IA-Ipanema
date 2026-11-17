# Defensa del autor N1–N4 — anterior a la corrección

Codex es el autor; esta defensa no es revisión independiente ni cierre. Se preservan íntegros la respuesta de Claude, sus precisiones y el candidato c240b16f. Reproducciones mínimas ya ejecutadas únicamente sobre fixtures del candidato anterior: before-reproductions.json.

## N1 — aceptada

Evidencia: council_runtime.binding usa json.dumps(sort_keys=True) con separadores y ensure_ascii predeterminados; code_review._hash usa JSON compacto. Los hashes difieren con la misma política. El productor operativo no emite permissions_sha256. Causa: reutilizar un nombre de campo con otra serialización y construir ambos lados del test con el helper nuevo.

Contrato: se define code-review-context/1 con JSON estándar determinista (sort_keys=True, ensure_ascii=True, allow_nan=False y separadores explícitos coma-espacio/dos puntos-espacio), UTF8/SHA256. Coincide con el productor actual para su dominio JSON. Permisos se suministran explícitamente al adaptador de contexto aislado; no se atribuyen al productor viejo. Ausencia de contrato/hash obligatorio deja evidencia insuficiente.

Alternativas: cambiar productor operativo (fuera de alcance), conservar otro nombre incompatible (rechazada), adaptar contexto con definición versionada compartida por el nuevo productor aislado y gate (elegida). Recibos originales conservan campos y hash originales; compatibilidad legacy se valida expresamente, sin mutarlos. Riesgo: productores futuros deberán declarar el contrato y acreditar permisos/cobertura. Pruebas: salida real de binding, orden de claves, permisos cambiados y datos ausentes/legacy.

## N2 — aceptada

Reproducción: una respuesta del autor más recibo de resolución permite approved_for_authorization sin ningún registro de máquina de estados. La máquina es una API paralela que evaluate no consume. Contrato elegido: una única función reductora, historial de eventos y replay en evaluate para obtener cierre; respuestas sueltas nunca cierran. Resolución exige respuesta del autor, evidencia nueva comprobable, revisión pendiente y confirmación acreditada del revisor original. Identidad histórica del hallazgo conserva candidato de origen y hash de definición.

Alternativa rechazada: mantener dos rutas de cierre o sustituir estados con booleanos declarados. Riesgos: registros previos sin eventos suficientes quedan pendientes, no migrados ficticiamente. Prueba: recibo solo no cierra, replay válido cierra, autor/origen equivocado/evidencia ausente/revisión obsoleta no cierran y changes_requested permanece hasta otra revisión acreditada.

## N3 — aceptada con precisión de frontera

Reproducciones: omitir history devuelve aprobado; BLOCKER previo con revisiones actuales ausentes degrada a needs_evidence. No hay bypass de producción demostrado porque el gate es inactivo y el controlador se declaraba confiable. Causa: colección opcional sin compromiso de completitud y evaluación de historia después de continue.

Contrato elegido: interfaz del controlador para obtener una instantánea de historial con lineage_id, índice completo de revisiones y cabecera anclada en el contexto. No puede sustituirse por JSON del modelo. Procesar hallazgos históricos antes de envelopes actuales y preservar severidad. Migración explícita por hallazgo conserva identidad/origen y traslada solo el candidato de trabajo a review_pending; no resuelve nada. Revisión nueva debe acreditar qué dictámenes sustituye. Migración faltante o historial incompleto no permite aprobar.

No se construye almacenamiento/orquestador nuevo: interfaz de lectura, validación y fixtures. Riesgos: integrador deberá acreditar la fuente completa del historial; la cabecera no autentica origen. Pruebas: omisión/truncamiento, severidad con revisor ausente, candidato cambiado, migración explícita sin cierre y posterior resolución revisada.

## N4 — aceptada como contrato de confianza, sin afirmar autenticación criptográfica

Reproducción: identidad sintética declarada con self-hash basta para aprobar sin recibos nativos. Esta frontera ya se reconocía documentalmente; el resultado/API no la hacía obligatoria. Alternativas: MAC/almacén nuevos (fuera del mínimo), identidad JSON (insuficiente), interfaz tipada de evidencia emitida/verificada por controlador (elegida).

Contrato: separar principal declarado del binding (solo integridad) de atestación del adaptador suministrada por interfaz de controlador; comprobar origen/principal sin padre, capacidad, candidato, permisos, binding y recibo exactos. Supersedes sale del objeto principal y pertenece a la atestación de la revisión. El resultado expone trust_basis y synthetic_only. El transporte existente no implementa esta interfaz: por defecto needs_evidence. La clase Python no se presenta como autenticación criptográfica ni protege frente a ejecución arbitraria del propio controlador; modelos no pueden suministrar objetos de controlador ni ejecutar herramientas.

Riesgos: la futura implementación real debe validar el recibo nativo y aislamiento/capacidad; ninguna fixture lo acredita. Pruebas: JSON suplantado, falta de atestación/capacidad, hijo, proveedor distinto, recibo/binding/candidato/permisos alterados. Sin activar proveedor, políticas ni integración.

Archivos del alcance original: code_review.py, wrapper council.py y test_code_review_v3.py; solo en nueva copia aislada. Observaciones LOW no generan refactorizaciones generales. Estado final previsto: candidato probado, needs_evidence y revisión independiente pendiente.
