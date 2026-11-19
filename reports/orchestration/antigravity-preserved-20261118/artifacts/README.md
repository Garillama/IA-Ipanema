# Adaptador Antigravity: corrección acotada del contrato JSON

## Estado

Implementado únicamente en la copia aislada `/tmp/ia-ipanema-antigravity-jsonfix-20261118`. No integrado ni activado. Estado operativo: `needs_evidence`.

El parche base congelado conserva SHA256 `ca071456b9cc972fb6c0c43d4d63734be7a4f424e7be1d3991a3f7eeac3b0d83`. La copia base sigue intacta. El delta nuevo aplica limpiamente sobre ella (`git apply --check`: PASS).

## Cambios

- `tools/ipanema/orchestration/adapters.py`: Antigravity ahora exige un sobre JSON con `status == "SUCCESS"` y `response` no vacío. Para tareas con schema, exige `structured_output` tipo objeto y lo valida contra el schema recibido. Para tareas sin schema nativo, exige que `response` sea JSON objeto válido. Rechaza status de error/cancelación, salida vacía o malformada, claves JSON duplicadas, ausencia de salida estructurada, contenido incompleto o incompatible y campos de identidad declarada (`agent`, `identity`, `provider`). No completa campos ni concede permisos.
- `tools/ipanema/orchestration/engine.py`: entrega el schema al parser únicamente para Antigravity; conserva la validación existente de Claude y Codex sin cambios y evita validar dos veces la salida estructurada de Antigravity.
- `tests/unit/test_antigravity_integration.py`: adapta las aserciones de parser/CLI afectadas al sobre documentado. No se ejecutó este módulo ni la suite histórica.
- `tests/unit/test_antigravity_json_contract.py`: añade diez pruebas sintéticas focalizadas.

La identidad efectiva sigue procediendo de la tarea/controlador. El envelope no puede reemplazarla. El resultado solo es una respuesta de worker; no autoriza integración ni publicación.

## Flags CLI

La evidencia local conservada para `agy` 1.5.10 documenta `-p`, `--model`, `--output-format`, `--json-schema`, `--mode`, `--effort` y `--settings`. El adaptador usa los primeros seis cuando corresponde; acepta `--effort` solo para `low|medium|high|xhigh|max`. No añade `--settings` porque no hace falta para esta corrección. La compatibilidad de un esfuerzo concreto con un modelo sigue sin verificarse. No usa `--dangerously-skip-permissions` ni trata `--sandbox` o `--mode plan` como prueba de que todas las herramientas estén desactivadas.

## Validación ejecutada

Comando único de prueba focal:

```sh
PYTHONPATH=tools python3 -m unittest tests.unit.test_antigravity_json_contract -v
```

Resultado: 10/10 PASS. `git diff --check`: PASS. No se ejecutaron las 107 pruebas anteriores, proveedores, `agy -p`, llamadas de red ni pruebas de inferencia. La compatibilidad de los parsers Claude/Codex se cubrió con aserciones sintéticas del nuevo módulo; no se alteró su rama de producción.

## Ejemplos del contrato

Aceptado con schema:

```json
{"status":"SUCCESS","response":"validated","duration_seconds":0.01,"usage":{},"structured_output":{"decision":"proposed","changes":[]}}
```

Rechazados: `status` `ERROR`/`CANCELED`/`INTERRUPTED`/`INVALID`/`RUNNING`; falta de `status`, `response` o `structured_output`; `structured_output` que incumple el schema; JSON malformado/truncado/duplicado; o identidad declarada dentro del payload.

## Bloqueos restantes

- **B1:** la frontera de credenciales de autenticación CLI no está demostrada para workers capaces de herramientas.
- **B2:** no está demostrado egreso de red restringido por destino.
- No se verificó salida real de cuenta/modelo ni comportamiento real del CLI; solo se usó documentación y ayuda local previamente guardadas.
- No se ha ejecutado una revisión independiente del nuevo diff.
- No se modificó V2 operativo, no se habilitó el consejo de tres agentes y no se llamó a Claude, Codex o Gemini.

Por tanto, esta corrección mejora el contrato de parseo, pero no desbloquea la ejecución real. Requiere revisión independiente antes de cualquier consideración de integración.

## Artefactos

- `incremental-over-ca071.patch`: delta aplicable al candidato congelado.
- `full-candidate.patch`: parche acumulado desde la base Git de la copia aislada.
- `candidate-ca071.patch`: copia del parche congelado original.
- `manifest.json`: hashes base, finales y artefactos.
- `tests-result.txt`: resultado del test focal.
