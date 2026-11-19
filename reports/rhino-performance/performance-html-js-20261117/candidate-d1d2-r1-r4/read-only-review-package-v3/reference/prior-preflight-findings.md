# Preflight del consejo (v2)

Los candidatos están vinculados al run por sus hashes y nombres lógicos. El controller valida que las rutas de archivos declaradas estén dentro de `plan.allowed_files`, pero la tarea read-only solo recibe `task.read_files` y cualquier archivo de lectura debe pertenecer a ese allowlist global. Por ello no se pueden proporcionar consumidores externos como archivos de contexto sin añadirlos al allowlist. Las tareas read-only mantienen `task.allowed_files=[]`, de modo que agregar deps al contexto no concede escritura.

También se reprodujo que `validate_objections` acepta un `evidence_ref` inexistente; no verifica cada referencia contra `controller_evidence`. El run sigue ligado a candidate hashes, pero la integridad referencial individual no está implementada.

No se ejecutó ningún proveedor; el consejo permanece detenido antes de invocaciones.
