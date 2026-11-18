# Verificación de capacidades del adaptador Antigravity

Fecha: 2026-11-18  
Estado: **`needs_evidence`**  
Candidato evaluado: `ca071456b9cc972fb6c0c43d4d63734be7a4f424e7be1d3991a3f7eeac3b0d83`  
Proveedor, inferencia y cuenta: **no invocados**

## Identidad del ejecutable local

- `command -v agy`: `/home/alanrichard/.local/bin/agy`.
- Ruta resuelta: la misma; no es symlink.
- Tipo: ELF x86-64 PIE, dinámico, stripped; 267.322.056 bytes.
- Build ID: `abf8a2e123d2705c3b3c7e01e79d75c1`.
- SHA256: `20d6f74672ce28084f50296a26860c143590b76d128d422919ef4931fbb83432`.
- `agy --version` con entorno limpio y `HOME=/nonexistent`: `1.5.10`, exit 0.
- No pertenece a un paquete dpkg; `rpm` y `pacman` no están instalados. La imagen es un binario user-local autónomo. El proveedor/build exacto no se acredita con los metadatos ELF disponibles; no se pudo consultar metadata Go porque el toolchain no está instalado.
- No se inspeccionaron `~/.gemini`, keyring, credenciales, configuración ni variables privadas.

Los comandos `--version` y `--help` se ejecutaron con un entorno mínimo y HOME inexistente, sin prompt ni inferencia. No se hizo captura de tráfico de red, por lo que la evidencia prueba que el comando no hizo una invocación de modelo, no que el proceso no emitiera ninguna conexión auxiliar.

## Ayuda íntegra del ejecutable

`agy --help` devolvió exit code 0, stdout vacío y todo el texto de ayuda por stderr. La captura sin truncar está en:

- [help.stderr](/home/alanrichard/Escritorio/IA%20inversa/reports/orchestration/antigravity-capabilities-20261118/help.stderr)
- [help.stdout](/home/alanrichard/Escritorio/IA%20inversa/reports/orchestration/antigravity-capabilities-20261118/help.stdout) (0 bytes)
- [help.exit](/home/alanrichard/Escritorio/IA%20inversa/reports/orchestration/antigravity-capabilities-20261118/help.exit) (`0`)
- [identidad y versionado](/home/alanrichard/Escritorio/IA%20inversa/reports/orchestration/antigravity-capabilities-20261118/executable-identity.txt)

```text
Usage of agy:
  --add-dir                       Add a directory to the workspace (repeatable) (default [])
  --agent                         Agent for the current CLI session
  -c                              Short alias for --continue
  --continue                      Continue the most recent conversation
  --conversation                  Resume a previous conversation by ID
  --dangerously-skip-permissions  Auto-approve all tool permission requests without prompting
  --disable-slash-commands        Disable slash command and skill expansion in print mode
  --effort                        Reasoning effort for the current CLI session (low|medium|high|xhigh|max)
  -i                              Short alias for --prompt-interactive
  --input-format                  Input format for print mode (text, stream-json). stream-json reads one NDJSON message per line from stdin and runs a turn for each; it requires --output-format stream-json (default text)
  --json-schema                   Optional JSON schema string or path to a schema file to enforce structured output (for stream-json, only applicable to the final result)
  --log-file                      Override CLI log file path
  --mode                          Set the agent execution mode for this session (accept-edits, auto, plan)
  --model                         Model for the current CLI session
  --new-project                   Create a new project for this session
  --output-format                 Output format for print mode (text, json, stream-json) (default text)
  -p                              Short alias for --print
  --print                         Run a single prompt non-interactively and print the response
  --print-timeout                 Optional time limit for print mode; 0 waits until the turn completes (default 0s)
  --project                       Project ID or project name for the current CLI session
  --prompt                        Alias for --print
  --prompt-interactive            Run an initial prompt interactively and continue the session
  --remote-agent                  Run this session's conversations using remote agents; --project then names a remote project by ID or name, otherwise they open in this machine's default remote project
  --remote-control                Create a remote connection for the CLI session on start up
  --sandbox                       Run in a sandbox with terminal restrictions enabled
  --settings                      Settings for this session only, never saved: a JSON object of settings.json keys, inline or as a file path

Available subcommands:
  acp             Start the Agent Client Protocol (ACP) stdio server
  agent           List available agents
  agents          List available agents
  changelog       Show changelog and release notes
  help            Show help for subcommands
  install         Configure environment paths and shell settings
  mcp             Manage MCP servers (add, remove, list, enable, disable)
  mic-serve       Serve this machine's microphone to a CLI on another host
  models          List available models
  plugin          Manage plugins (install, uninstall, list, enable, disable)
  plugins         Alias for plugin
  remote-control  Manage the remote-control background daemon (start, status, stop)
  update          Update CLI
```

El bloque anterior conserva el contenido textual de stderr. Para mantener literal incluso las líneas de aliases/defaults, el archivo `help.stderr` es la fuente byte-for-byte.

## Capacidades: documentación y confirmación local

| Capacidad | Evidencia | Resultado |
|---|---|---|
| Prompt no interactivo | Help local incluye `-p/--print`; guía oficial lo describe como un prompt no interactivo de una sola ejecución. | **Flag confirmado; no se ejecutó prompt**. |
| Elegir Gemini/modelo | Help local incluye `--model`; docs oficiales muestran `agy models` y slugs Gemini para `--model`. | **Selección documentada; modelos/cuenta locales no comprobados**. El catálogo del candidato está correctamente `null/unverified`. |
| JSON / JSON Schema | Help local lista `json`, `stream-json`, `--json-schema`; docs oficiales especifican el sobre JSON y `structured_output`. | **Formato documentado; no se generó salida local real**. El parser candidato sí contradice el sobre documentado (ver abajo). |
| Timeout | Help local tiene `--print-timeout`. | **Flag confirmado**; cancelación real de `agy` no probada. |
| Herramientas, MCP y shell | Help local no tiene una opción `--no-tools`/equivalente. Docs exponen `permissions.deny` por acciones (`read_file`, `write_file`, `command`, `read_url`, `execute_url`, `mcp`, etc.). | **Hay control de permisos configurable, pero no hay un flag único de cero herramientas demostrado**. Un modo `plan` no equivale a prohibir herramientas. |
| Skills/slash commands | `--disable-slash-commands` confirmado. | Solo desactiva expansión de slash commands/skills en print; **no desactiva shell, file, web, MCP ni subagentes**. |
| Subagentes | La documentación de CLI describe delegación y eventos `subagent_info`; el help local no expone un flag para desactivarlos. | **Disponibilidad documentada, no hay control de desactivación comprobado**. |
| Sin repositorio | No hay flag local `--no-project`; `--project`, `--new-project`, `--add-dir` están presentes. Docs describen un proyecto CLI por defecto y conversaciones standalone en scratch en superficies compatibles. | **No existe evidencia local de un modo headless que garantice cero acceso al repositorio**. La ruta de trabajo, permisos y herramientas tendrían que aislarse y comprobarse. |
| Identidad de cuenta | Help no detalla auth. Docs oficiales indican autenticación CLI mediante perfiles/tokens y keyring del SO; print-mode usa credenciales cacheadas. | **No se puede conservar esa identidad en el worker actual sin exponer el acceso al keyring**. No se intentó login ni se consultó credencial. |
| Inspección sin inferencia | `--version`, `--help` confirmados localmente. Docs referencian `agy models` y `agy agents` para catálogos. | **Version/help no invocan el agente en esta captura**. Los subcomandos models/agents no se ejecutaron: podrían necesitar cuenta/servicio y no se trazó su red. |

## Incompatibilidades concretas del candidato

1. **Parser JSON — incompatibilidad con el contrato publicado.** En `adapters.py:152-157`, `parse_response('antigravity', ...)` solo acepta un objeto con `decision` y `changes` al nivel raíz. La documentación oficial de `--output-format json` muestra un sobre con `status`, `response`, `duration_seconds`, `usage`, y cuando se usa `--json-schema`, el objeto validado bajo `structured_output`. La respuesta documentada no tiene `decision`/`changes` en la raíz y el parser la rechazaría como `antigravity_json_envelope_unverified`. Corrección mínima futura: validar `status == SUCCESS`, obtener `structured_output`, validar íntegramente contra el schema y rechazar status/errores/cancelaciones/objetos ausentes; no asumir que exit 0 equivale a revisión válida.
2. **Flag `--effort` — limitación y mensaje incorrecto.** En `adapters.py:130-131`, el candidato rechaza cualquier esfuerzo diciendo que `agy --help` no lo documenta. La ayuda local sí incluye `--effort`; la documentación oficial enumera `low|medium|high|xhigh|max` según modelo. Hoy los perfiles son `null`, así que no hay llamada que requiera cambiarlo; si perfiles futuros asignan effort, la rama debe pasar solo valores admitidos por el modelo o rechazar con causa correcta. No se cambió el candidato.
3. **Sin desactivación completa de tools/subagents.** La línea 134 prepara `--mode plan --sandbox --disable-slash-commands`; docs describen `--sandbox` como restricción del terminal y `--disable-slash-commands` como control de slash/skills. Headless JSON documenta herramientas disponibles y eventos de tool/subagent. El comando candidato no aplica una lista de deny y no se demostró un control de subagentes. Esto impide usarlo como revisor sin herramientas bajo el modelo de amenaza actual.
4. **No es un selector de proveedor “Gemini” verificado.** `--model` acepta un modelo, pero el candidato deja sus perfiles en `null` y no se consultó `agy models`. Está bien bloqueado; no hay modelo probado para esta cuenta.

No se detecta incompatibilidad de sintaxis en `-p`, `--model`, `--output-format json`, `--json-schema <path>`, `--mode plan`, `--sandbox`, `--disable-slash-commands` o `--print-timeout`: el help local los lista y las docs oficiales describen sus roles. Esto solo confirma interfaz, no el comportamiento completo del runtime 1.5.10.

## Seguridad

- **B1 continúa bloqueado.** Google documenta que `agy` usa keyring/perfil de token y credenciales cacheadas en headless. El sandbox actual deja HOME/keyring inaccesibles al worker; montarlos permitiría que procesos hijos con tools los lean. El worker no puede preservar autenticación CLI y estar aislado simultáneamente con el diseño actual. No se recomienda sustituir por `GEMINI_API_KEY` ni otro modo de cobro/identidad sin autorización.
- **B2 continúa bloqueado.** No se demostró egress por destino para el proceso inferencia. La granularidad de `read_url(domain)` documentada pertenece a acciones de herramientas web; no demuestra cortafuegos para conexiones de proceso, DNS, IP o el propio transporte del modelo. `--sandbox` es terminal sandbox, no evidencia de filtro de egreso.
- Hashes solo prueban identidad de artefactos, nunca autenticación ni autorización.

## Próximo paso mínimo

Sin llamar al modelo: obtener el resultado de `agy models` y `agy agents` solo después de revisar si esos subcomandos realizan solicitudes externas, y con permiso explícito para cualquier consulta de cuenta. Para compatibilidad de formato, crear un fixture JSON basado estrictamente en el contrato oficial y revisar el parser en una nueva autorización de cambios; no presentarlo como salida real 1.5.10.

Para volver a considerar ejecución real hacen falta: solución de credencial que no exponga el keyring al worker; egreso por destino impuesto fuera del proceso; bloqueo efectivo de tools/MCP/subagentes o arquitectura de worker sin herramientas demostrada; modelo/cuenta y salida real verificados sin falsear tests; prueba real de cancelación. Con el alcance actual no se ejecutó ninguna de esas comprobaciones.

## Fuentes

- [Google Antigravity CLI: Headless mode](https://antigravity.google/docs/cli/headless/)
- [Google Antigravity CLI: CLI commands and flags](https://antigravity.google/docs/cli/reference)
- [Google Antigravity: permissions](https://antigravity.google/docs/permissions?tab=cli)
- [Google Antigravity: feature overview, CLI and subagents](https://antigravity.google/docs/features?tab=cli)
- [Google Antigravity: authentication and keyring](https://antigravity.google/docs/install)

Context7 no estuvo disponible en esta sesión; se contrastó con documentación oficial de Google y ayuda local del binario. No se invocó proveedor ni se ejecutaron `agy models`, `agy agents`, MCP, plugin o comandos de cuenta.

## Resultado

**Recomendación: `needs_evidence`.** No modificar ni integrar el parche todavía. Primero se requiere corregir el parser frente al sobre JSON documentado y aclarar el rechazo de effort; ambos cambios requieren una nueva autorización de modificación. B1/B2 y la restricción de tools/subagentes permanecen bloqueos de ejecución real.
