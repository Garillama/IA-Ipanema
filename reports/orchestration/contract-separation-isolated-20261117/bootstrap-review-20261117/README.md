# Bootstrap de revisión del controlador candidato

Estado: **`needs_evidence`; no se invocaron Claude ni Codex y no se integró el parche.** El paquete original permanece intacto.

## Identidad y paquete

Paquete congelado: [`../review-package-16802138/README.md`](../review-package-16802138/README.md). Manifiesto SHA256 `d32d4dd0ef5a9b50996cec5bb4e95da3abdac86c889b51477c708721d9f4e96c`; parche SHA256 `16802138df326ef1f47612784756cdad4ad79c9010d4bd9fb866c18c137126a5`. Conserva diez candidatos (cinco del controlador y cinco de pruebas), diez dependencias de contexto y `write_files=[]`.

## Ejecutables y comprobación local

En la copia aislada, `python3 tools/ia.py --project ipanema orchestrate doctor` informó Claude Code `2.1.326`, Codex `0.169.0` y Bubblewrap operativo. La comprobación es de CLI/sandbox solamente: autenticación y acceso a modelos quedaron `not_checked`. CommandCode sigue deshabilitado. No se ejecutó inferencia.

Dos pruebas locales, sintéticas y sin proveedor confirmaron que Bubblewrap rechazó escribir el fixture y que una cancelación de `run_isolated(provider=qa, network=False)` terminó y recolectó el proceso con el marcador del proceso hijo ausente. Esto valida esos casos concretos, no la cancelación de una sesión real del proveedor ni una auditoría general del kernel.

## Presupuesto real del prompt

El paquete anterior enviaba candidatos+contexto: 298.028 bytes de archivos y 327.945 bytes de prompt serializado; sin embargo, **no incluía el diff en el `read_files` de los workers**, aunque el diff sí estaba dentro del paquete. Para revisar el diff exacto se midió un diseño local read-only con las cinco fuentes de controlador completas, las diez dependencias, el parche como contexto y las cinco fuentes de pruebas omitidas porque el parche incluye sus cambios: 285.466 bytes fuente, 313.687 bytes serializados, más 6.268 bytes de esquema nativo. Son medidas del prompt local con metadata de evidencia vacía, no el tamaño final de una corrida real. Debe comprobarse la serialización final del controlador justo antes de cada proveedor; no existe medición local del número de tokens ni del sobre privado interno del CLI.

El set completo (los diez candidatos más diez dependencias más el parche) suma 352.389 bytes y excede el límite de 300.000. El `source_windows` actual no soluciona ese límite: `prompt_for` suma los bytes de cada archivo completo antes de seleccionar ventanas. En la variante medida se conservan las diez rutas en `candidate_files`, pero las fuentes de los cinco tests no se duplican como contenido completo: sus cambios se revisan en el diff íntegro. Esto reduce duplicación y no amplía permisos.

## Evaluación de seguridad

**No se puede garantizar el bootstrap dual seguro con la ruta actual.** La causa principal es el manejo de credenciales de Codex: el controlador monta su archivo de autenticación explícito bajo `/worker-home`, mientras `codex exec` conserva herramientas de shell en modo read-only. Read-only evita escrituras, pero no oculta archivos legibles del sandbox; por ello, un comando invocado por el modelo podría leer el archivo de autenticación. No se inspeccionó ni copió el contenido del archivo. Claude usa `--tools ''`, configuración MCP vacía y sin fuentes de settings, pero eso no corrige el riesgo de Codex.

Además, el namespace exterior comparte red para alcanzar los proveedores y no filtra por hostname. El modo read-only de Codex normalmente restringe red de sus comandos según documentación del CLI, pero la invocación exacta no hizo una comprobación efectiva de ese permiso; no se afirma que la red esté bloqueada.

La copia candidata no contiene `.git`; el flujo workspace necesita Git para preparar snapshots. Cualquier prueba futura requeriría un nuevo directorio desechable con Git inicializado y configuración sintética, sin modificar el checkout operativo.

## QA obligatorio

El `central_qa` de `scope=workspace` se ejecuta antes de inferencia, sin credenciales ni red, y lanza la suite completa `unittest discover -s tests/unit -v`, con timeout de 180 segundos. Repetiría las 113 pruebas unitarias incluidas en la corrida focalizada y descubriría además las demás pruebas unitarias; no repetiría por sí mismo las 12 pruebas de integración de aquella corrida. No se ejecutó en esta preparación y no se alteró esa política. No se conoce el total actual sin volver a descubrir/ejecutar.

## Autoaprobación y contratos

Codex fue autor del parche; su intervención puede defender o explicar el código, pero no cuenta como revisión independiente ni puede aprobarlo. Claude sería el revisor independiente. El Consejo también necesita aclarar la semántica del `council_gate`: hoy exige `implementation_allowed=true` incluso en un plan read-only. Un resultado de consejo no es autorización humana de integración.

## Comando y autorización

**No hay un comando que hoy pueda autorizarse con seguridad para ejecutar el consejo.** El candidato CLI tiene los flags tipados, pero el riesgo de que Codex lea su archivo de autenticación persiste, la red no tiene filtro de destino probado, la copia no es repositorio Git y el gate read-only debe aclararse. No se ejecutará usando directamente `adapters.py`, no se puenteará el controlador y no se omitirán controles.

La autorización actual suficiente sería para preparar una corrección aislada y revisable del manejo de credenciales/egreso y la semántica read-only; **no** para llamar proveedores. Después se necesitarían preflight OS-level, nuevo diff y autorización específica para una única ejecución. Como alternativa, el propietario puede hacer una revisión manual en sesiones oficiales sin herramientas locales conectadas, adjuntando el paquete de solo lectura; las respuestas serían evidencia externa, no recibos del controlador ni certificación de integración.

## Parada obligatoria

Detener si cambian los hashes, el paquete excede el límite efectivo, el proceso puede leer credenciales o escribir el snapshot, no se acredita el proceso hijo cancelado, el sandbox/red difiere de lo medido, falta cualquiera de los dos proveedores, aparece error de contrato/ledger, se activa reintento/fallback, falla central QA o el gate exige interpretar una revisión como autorización. No intentar corregir esas condiciones durante una ejecución.

Detalle de mediciones, resultados sintéticos y riesgos: [`bootstrap-evidence.json`](bootstrap-evidence.json).
