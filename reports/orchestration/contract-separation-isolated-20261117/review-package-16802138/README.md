# Paquete de revisión independiente — separación de contratos

Estado: **preparado; no ejecutado**. El controlador operativo no fue modificado; Claude y Codex no fueron invocados. No integrar ni ejecutar a partir de este paquete sin autorización nueva.

## Identidad

Parche incremental SHA256: `16802138df326ef1f47612784756cdad4ad79c9010d4bd9fb866c18c137126a5`.

El delta se aplica sobre los cinco archivos de controlador indicados en `reference/file-hashes.json`; incluye cinco rutas de pruebas (una nueva). La igualdad de conjunto entre las diez rutas del manifiesto y las cabeceras del parche fue comprobada al congelar el paquete. El código candidato está bajo `candidate/` conservando rutas lógicas. Los respaldos base de las nueve rutas preexistentes están bajo `reference/base/`; la prueba nueva no tiene preimagen. Los hashes operativos observados coincidían con la base al crear la copia.

## Alcance y permisos del paquete

- `candidate_files`: solo las diez rutas exactas enumeradas en el manifiesto. Son los archivos evaluados.
- `context_files`: solo las diez rutas enumeradas en el manifiesto. Son referencias locales de solo lectura.
- `write_files`: `[]`.
- Cada tarea de revisión tiene `read_only=true`, `read_files=candidate_files + context_files`, y `allowed_files=[]`.
- No existe permiso para cambiar los candidatos. La inclusión de `context_files` nunca autoriza integrarlos ni agregarlos al diff.
- El manifiesto identifica contenido, no es una autorización. Su hash no es firma criptográfica ni prueba de identidad del propietario.

## Preguntas para la revisión — no limitarse a ratificar pruebas

1. ¿La separación candidata/contexto/escritura se aplica igual en CLI, planner, tareas, snapshots, council, workers, QA, binding y gate? Cite rutas y funciones.
2. ¿Hay un camino donde un plan legado, alias `--file`, modificación del JSON, tarea derivada o ruta alternativa amplíe escritura o vuelva candidato un archivo contextual? Analice fail-closed y el límite del hash sin clave.
3. ¿El diff de cinco archivos es mínimo y coherente con los contratos? ¿Hay lógica duplicada o dos fuentes de autoridad?
4. ¿Cada fase que consume `evidence_ref` valida existencia en el ledger controlador, run, binding de candidato y hashes antes de consolidar? Busque propuestas, objeciones, preguntas, defensa y agregación; señale cualquier fase omitida.
5. ¿Se puede citar una dependencia contextual sin declararla archivo afectado? ¿Puede una cita falsa, de otro run o de otro candidato sobrevivir?
6. ¿Se conservan planificación, consejo Claude/Codex, QA central, recibos legacy, CLI `--file`, read-only e implementación local autorizada? Distinga compatibilidad comprobada de inferencia.
7. ¿Las pruebas cubren adversarios relevantes? Identifique escenarios ausentes concretos; no repita las suites.
8. Riesgos de integración: el controlador operativo aún es antiguo; el contrato del parche no autentica un plan editado y re-sellado; el central QA de scope workspace descubre toda `tests/unit`.

Cada objeción debe enlazar ruta, función/contrato, evidencia concreta, impacto, severidad y condición de resolución. Diferencie defecto reproducible, riesgo arquitectónico, integración futura y preferencia.

## Pruebas y evidencia ya conservadas

Las 125 pruebas focalizadas terminaron con 125 pasadas, 0 fallos y 0 errores; recibo y log íntegro están en `reference/`. No se repitieron en esta preparación. Son pruebas locales/sintéticas, no revisiones de modelos ni prueba de integración del controlador operativo. El manifiesto conserva hashes de candidatos, bases y dependencias. El paquete también conserva los casos de referencias inventadas, de otro run, binding/hash y fuentes contextuales.

## Preflight local realizado

Solo se comprobó estáticamente la compatibilidad de las rutas con la interfaz CLI y se validó el contrato tipado localmente contra el módulo del controlador **aislado**: caso read-only con diez candidatos, diez contextos, dos tareas de revisión y cero escrituras; mutaciones de write_files, tarea con escritura, lectura fuera del conjunto y plan incompleto fueron rechazadas. No se llamó ningún proveedor. Los casos son chequeos de contrato, no recibos de aprobación.

El controlador operativo actual solo expone `--file`; no soporta `--candidate-file`, `--context-file` y `--write-file`. Por ello, no hay un comando seguro soportado hoy para ejecutar esta revisión: usar el CLI actual mezclaría contexto con candidatos. El CLI del árbol aislado sí reconoce esos flags, pero no está integrado ni autorizado para invocar proveedores. No ejecutar.

Además, el camino `central_qa` para `scope=workspace` ejecuta `python -m unittest discover -s tests/unit`; una ejecución futura del consejo puede repetir las 125 pruebas focalizadas y ampliar QA. No se modificó esta política. Resolver ese alcance requeriría autorización separada; no se propone evadirlo.

## Condiciones de una futura ejecución única

Solo después de integrar el parche mediante autorización específica y obtener autorización distinta para llamar a los dos revisores: revalidar los diez hashes, usar snapshot congelado, mantener `write_files=[]`, tareas read-only, permitir únicamente las dos identidades originales Claude/Codex, una ejecución sin reintentos, conservar recibos completos y detener ante desajuste de hash, alcance, ledger, permisos o QA. Una respuesta favorable no integra ni activa cambios. El QA central obligatorio debe aprobarse expresamente o quedar pendiente; no omitirlo.

## Estado

`needs_evidence`: no hay revisión independiente real; el controlador operativo no entiende todavía este contrato. Antigravity/V3 no forman parte del paquete.
