# Diseño correctivo aislado — bootstrap de revisión V3

Estado: **diseño; no implementación**. No se llamó a Claude/Codex, no se usaron credenciales reales, no se cambió el controlador operativo, no se integró el parche y no se alteró V3. Se mantiene `needs_evidence`.

## Evidencia base preservada

- Adaptación bajo análisis: SHA256 `16802138df326ef1f47612784756cdad4ad79c9010d4bd9fb866c18c137126a5`.
- Paquete de revisión anterior: manifiesto SHA256 `d32d4dd0ef5a9b50996cec5bb4e95da3abdac86c889b51477c708721d9f4e96c`.
- Se volvieron a comprobar los hashes base de los nueve archivos preexistentes contra el checkout operativo. No cambió ningún archivo operativo.
- [Pruebas sintéticas reproducibles](synthetic-probes.py) reproducen la lectura de un token ficticio montado en el sandbox y el bloqueo de un sentinel local cuando la red está totalmente deshabilitada. Nunca contactan un servicio externo.

## Hallazgos reproducidos

1. **Secreto legible desde proceso hijo:** el wrapper monta el archivo explícito `auth_files` en `/worker-home/.codex/auth.json`. Una tarea sintética que ejecuta `/bin/cat` puede leer el canario. Read-only impide escribir; no impide leer un archivo que sí está montado. No se leyó ningún token real.
2. **Red del worker deshabilitada:** con `network=False`, un proceso dentro de Bubblewrap no conecta a un servidor sentinel en el loopback del host. Esto prueba la denegación total del namespace para ese proceso. No prueba una allowlist de salida para un broker ni el comportamiento del Codex real.
3. **Red del camino actual de inferencia:** el controlador habilita red para invocar proveedores y no implementa un firewall por destino. No existe prueba de allowlist efectiva en este camino.
4. **Gate read-only:** el `council_gate` actual exige `implementation_allowed=true` aun cuando el plan sea read-only. El significado de esa aprobación debe separarse; no debe usarse para una revisión sin autorización de implementación.
5. **Tamaño:** el paquete completo con diff y todos los archivos fuente superaría 300.000 bytes. El prompt exacto medido de la variante compacta fue 313.687 bytes, antes de metadata real del ledger. El cálculo previo mostró que source_windows se aplica después del contador de bytes fuente; por tanto, no reduce el preflight de 300.000.

## Arquitectura propuesta

### Componentes y confianza

1. **Orquestador/controlador:** arma el snapshot y el prompt desde archivos hasheados; fija `candidate_files`, `context_files`, `write_files=[]`; calcula tamaño final y binding; registra recibos. No conserva tokens del proveedor en el snapshot, prompt, entorno del worker ni log.
2. **Inference broker confiable, fuera del worker:** proceso separado con identidad del sistema distinta y acceso exclusivo al secreto del proveedor. Únicamente acepta un request estructurado ya limitado (proveedor, modelo allowlisted, prompt bytes/hash, schema, run/candidate binding), hace una llamada de inferencia sin herramientas ni ejecución local y retorna respuesta JSON + metadatos no secretos. No monta el repositorio ni tiene endpoint de ejecución de comandos. El secreto no se pasa como env a un proceso que ejecute shell.
3. **Worker/revisor lógico:** recibe únicamente el prompt y schema ya preparados. Sin `auth.json`, HOME real, keyring, variables secretas, browser, MCP, plugins, subagentes, shell de cliente ni acceso al repo operativo. En la opción preferida no hay un proceso de herramientas del modelo para este trabajo de revisión.
4. **Egreso:** solo el broker obtiene egress. Una política de red externa al modelo y fail-closed permite destinos exactos confirmados por documentación oficial de cada proveedor. Bloquea acceso directo del controlador/worker, dominios no allowlisted, redirecciones no permitidas, DNS rebinding y rangos privados/link-local/metadata. La allowlist queda `needs_evidence` hasta confirmar los hosts exactos vigentes; no se inventan dominios.
5. **Canal interno:** Unix socket con permisos de usuario/grupo exclusivos o pipe autenticado entre controlador y broker. El broker valida longitud, schema, run ID, hash del prompt y número de llamadas. No acepta que el modelo elija URL, endpoint, modelo fuera de lista ni comandos.

**Compatibilidad de identidad pendiente:** el Codex CLI actual no ofrece en el adaptador un modo sin herramientas y su archivo de autenticación queda visible. Un broker con API de inferencia podría cambiar el tipo de identidad/autenticación respecto de Codex CLI/ChatGPT. No asumir equivalencia. Antes de implementarlo, confirmar con el propietario si una credencial API separada y alcance de producto equivalen a la identidad de revisor deseada. Si no, conservar revisión manual externa en UI oficial, sin herramientas locales; sus respuestas no serían recibos del controlador.

### Credenciales

- Quitar cualquier montaje de `~/.codex/auth.json` y `~/.claude/.credentials.json` dentro del worker de herramientas.
- No pasar tokens en argumentos ni variables heredadas.
- Broker lee el secreto mediante fuente explícita y mínima; el worker no puede leer su filesystem, `/proc`, memoria, sockets de administración ni logs.
- El broker devuelve solo datos verificables no secretos: proveedor declarado por el adaptador, modelo, request ID si está disponible, timestamps, prompt hash/bytes, schema hash, response hash y política de egress. Nunca token, headers `Authorization`, `auth.json`, ni fingerprint reversible.
- El registro del controlador se vincula a `run_id`, candidato y ledger local. La identidad acreditada proviene del adaptador/broker, no del JSON del modelo. La respuesta no es autorización humana.

### Egreso

El aislamiento de proceso debe aplicar deny-by-default fuera del broker. El broker usa un proxy/firewall en otro namespace o servicio con reglas de host/puerto/IP y TLS. No basta con `--unshare-net` para el worker, porque el broker necesita llamar al proveedor. El enforcement debe probarse con sentinel permitido y no permitido; DNS y redirecciones se controlan en el punto que abre la conexión. Si no puede distinguir destinos ni bloquear todos los demás, abortar.

## Gate read-only

No reutilizar `implementation_allowed` como resultado de revisión. Añadir contrato separado de resultado:

- `purpose: read_only_review`
- `review_outcome: completed | changes_requested | needs_evidence | blocked`
- `implementation_allowed: false`
- `integration_allowed: false`
- binding exacto candidato + dependencias + prompt + schema + dos participantes

`review_gate` solo registra que la revisión se completó bajo permisos read-only; nunca habilita tareas de implementación. `council_gate` de implementación conserva sus checks actuales y exige un plan nuevo y permiso humano separado. El gate rechaza `implementation_allowed=true`, `write_files` no vacío, revisión obsoleta, falta de uno de los revisores requeridos, autor como aprobador independiente o referencias de ledger fuera de run/candidato.

## Preflight del prompt

1. Construir el cuerpo final una sola vez: instrucciones, archivos/extractos, diff, historial/QA realmente incluidos, source binding, ledger IDs permitidos y JSON Schema nativo.
2. Medir bytes UTF-8 después de serialización canónica y el tamaño total de cada campo/schema/argumento que efectivamente se envíe. No estimar por bytes fuente ni repetir serializaciones con representaciones distintas.
3. Si el proveedor ofrece token count local/documentado compatible, medir los tokens del request completo y reservar output budget; si el envelope de CLI/proveedor es opaco o el conteo no es verificable, mantener `needs_evidence` y usar un margen conservador aprobado. El tamaño en bytes no equivale a tokens ni certifica capacidad.
4. Validar primero hash del diff, candidate/context/write, schema hash, versiones de modelo y binding.
5. Solo tras pasar límites, crear un immutable request ID y permitir al broker una llamada. Sobre tamaño, esquema, binding o egress: cero llamadas, cero receipt de proveedor.
6. Registrar bytes fuente, bytes finales, schema bytes, token count solo si realmente fue medido, límites y hash del request. No incluir contenido sensible de salida del proveedor en logs generales.

## Paquete reproducible

`synthetic-probes.py` se ejecuta con la copia candidata local ya existente:

```bash
IPANEMA_CANDIDATE_ROOT=/tmp/ia-ipanema-contract-separation-20261117/repo \
PYTHONPATH=/tmp/ia-ipanema-contract-separation-20261117/repo/tools \
python3 reports/orchestration/contract-separation-isolated-20261117/bootstrap-correction-design-20261117/synthetic-probes.py
```

Salida esperada: `fake_secret_visible_to_child=true` para demostrar el bloqueo actual; sentinel local bloqueado con `network=False`. Esa primera condición **es una falla de seguridad actual**, no un test de aceptación. No se requiere ni permite autenticación de modelo. Todo el canario se crea y destruye en un directorio temporal.

No se repitieron las 125 pruebas. El script es una prueba de aislamiento focalizada; no se aplicó el diseño ni se ejecutó el QA central.

## Matriz de riesgos

| Riesgo | Nivel | Evidencia | Mitigación propuesta | Estado |
|---|---|---|---|---|
| Codex shell lee auth montado | BLOCKER | Canario sintético visible | Secreto fuera del worker; broker sin tool execution; prueba negativa | Reproducido |
| Egreso del proceso de inferencia no filtrado | HIGH | Bubblewrap actual no filtra destinos | Broker con allowlist externa y worker sin red; sentinel permitido/no permitido | Diseño; falta implementar/probar |
| Codex identidad/API incompatibles con broker | HIGH | CLI usa auth file; API auth distinta | Confirmar autorización de identidad con propietario antes de implementar | `needs_evidence` |
| Prompt grande o envelope opaco | HIGH | 313.687 bytes compacto; el ledger real agrega datos | Medir payload final/tokenizer; stop pre-provider | Parcial; sin request real |
| Gate read-only puede significar implementación | HIGH | Contrato exige `implementation_allowed=true` | `review_gate` independiente; implementación false siempre | Diseño |
| Snapshot no aislado o candidato obsoleto | BLOCKER | hash binding actual sí es local; ejecución real no probada | staging desechable, read-only real, hash antes/después, sin proyecto cliente | Pendiente |
| Revisión incompleta aprobada | HIGH | dependencia de dos revisores/ledger | mismo run/candidato, no autor, ledger verificado, status fail-closed | Pendiente |

## Pruebas necesarias para una implementación futura

1. Canario falso: path y variable de entorno del secreto son ilegibles desde worker, comandos, `/proc`, logs, crash report y artefactos. Broker conserva el secreto; ningún output contiene canario.
2. Egreso: con servidor falso permitido la llamada del broker funciona; servidor falso no permitido no observa conexiones; worker no llega a ninguno. Probar IPv4/IPv6, localhost, RFC1918, link-local, metadata, DNS rebinding, TLS inválido y redirect a host no listado.
3. Sin herramientas: respuesta que intenta una herramienta/`mcp_tool_call` es rechazada; no se inicia proceso descendiente.
4. FS: candidatos/contexto no escribibles, fuera de snapshot no visible, `write_files=[]`, plan manipulado queda rechazado.
5. Gate: revisión read-only completa puede ser `review_complete` con implementación/integración falsas; gate de implementación no la consume; un nuevo plan requiere autorización nueva.
6. Prompt: exact-byte body incluye schema/contexto/ledger; pruebas `limit-1`, `limit`, `limit+1`; exceso causa cero `reserve`, cero spawn, cero provider receipt; UTF-8/JSON adversarial y respuesta truncada.
7. Recibos: IDs ficticios válidos solo si el controlador los emitió; rechazo de otros run, otro candidato, hash alterado y firma/ledger inválido.
8. Cancelación: detener broker, socket, worker y descendientes; marcar request indeterminado si no hay acuse final, no reintentar.
9. Doble revisión: Claude y Codex son dos identidades de adaptador; Codex autor no puede contarse como su propio revisor; pruebas de autor/reviewer cruzadas.
10. QA central obligatorio, aprobado por separado, corre offline en fixture sintético; no se modifica la política para evitar su costo.

## Condiciones de interrupción

Parar sin invocar modelos ante cualquier lectura de canario, token en env/argv, fallo de sandbox, shell/herramientas inesperadas, conexión al sentinel prohibido, destino DNS ambiguo, redirect externo, mismatch de hashes, prompt > límite, token budget desconocido, receipt sin binding, interrupción sin reap, council con `implementation_allowed=true`, participante ausente, intento de retry/fallback, o QA obligatorio fallido.

## Autorización futura requerida

La siguiente autorización debe cubrir solo una implementación local aislada de: (a) separación credential broker/worker o una alternativa de no-tools oficialmente soportada para ambos, (b) firewall de egress comprobable, (c) `review_gate` read-only separado, (d) serializador y preflight de tamaño final; más pruebas sintéticas anteriores. No incluiría invocar modelos ni integrar el parche. Tras implementar y revisar el diff, se solicitaría autorización independiente para un único preflight con proveedores reales. **No se solicita autorización de ejecución en este paquete.**
