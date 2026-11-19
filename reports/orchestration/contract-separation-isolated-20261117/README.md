# Adaptación aislada de contratos de revisión

Estado: **`needs_evidence`**. Cambios probados en una copia temporal. El controlador operativo sigue intacto; no se invocaron Claude ni Codex.

## Cambio preparado

Separación explícita de `candidate_files`, `context_files` y `write_files` en plan, tareas, prompts, binding y gate. Para `read_only`, `write_files=[]` y ninguna tarea de implementación. El consejo solo declara candidatos como archivos afectados; las dependencias se citan por referencias `source:<ruta>` verificadas contra ledger, run y hashes. El control cubre propuestas, objeciones, preguntas, defensas y agregación.

Planes guardados antiguos sin contrato tipado se rechazan explícitamente al ejecutar. `--file` se conserva como alias que genera un plan nuevo V2. Los recibos históricos con binding legado siguen legibles bajo su semántica; no se reescribieron.

## Diff y archivos

10 rutas: cinco componentes (`planner.py`, `cli.py`, `engine.py`, `council.py`, `council_runtime.py`) y cinco archivos de pruebas (cuatro modificados y uno nuevo). Hashes base y aislados: [`file-hashes.json`](file-hashes.json).

Parche: [`controller-adaptation.patch`](controller-adaptation.patch), SHA256 `16802138df326ef1f47612784756cdad4ad79c9010d4bd9fb866c18c137126a5`.

## QA focalizado

**125 pruebas pasaron, 0 fallos, 0 errores.** El comando y log están en [`focused-tests.json`](focused-tests.json) y [`focused-tests.log`](focused-tests.log). No se ejecutó la suite general ni hubo acceso a red, Rhino o Google. Las pruebas usaron datos/proveedores sintéticos; no equivalen a revisión real de agentes.

En una corrida previa hubo un error transitorio creando un worktree Git en una prueba mock; el caso pasó aislado y la corrida final de 125 pasó. Se conserva como posible flake, no como fiabilidad demostrada.

## Limitación

`file_contract_sha256` detecta cambios si no se recalcula, pero es un hash sin clave. No autentica el plan ni detiene a quien pueda editarlo y volver a sellarlo. No es una autorización. El plan exacto debe revisarse antes de `--execute`; no añadí autorización paralela.

## Preflight Rhino

Paquete v4: [`read-only-review-package-v4`](../../rhino-performance/performance-html-js-20261117/candidate-d1d2-r1-r4/read-only-review-package-v4/README.md). Manifiesto externo SHA256 `d1d24d949e1455d9eb3b828d69532d70af0b9d8463531bc186d95954a9127a30`. Contiene dos candidatos y siete dependencias; sus 194.145 bytes están bajo el límite local de 300.000 bytes. Cada revisor tiene `read_files` con esos nueve paths y `allowed_files=[]`; `write_files=[]`.

El manifiesto v3 indicado por el propietario (`33908cf593d8e327319746b13c7f9feed800a75adb0fb7999ebfa2874882b0ab`) y sus 22 archivos pasaron verificación. No se alteró. El preflight v4 fue sintético; no ejecutó el comando de orquestación ni proveedores. El diff seco `patch --dry-run -p1` también pasó contra el árbol operativo, sin aplicar cambios.

## Estado, integración y reversión

Los hashes de los cinco archivos operativos coinciden con los capturados al iniciar; no se integró el parche. La compatibilidad dual y de recibos se cubrió en las pruebas indicadas.

Siguiente paso: revisión independiente de este parche y análisis del sello no autenticado. Integrar solo tras autorización específica. Si una futura integración autorizada falla QA, restaurar las nueve rutas preexistentes a sus hashes base y retirar la prueba nueva si sus hashes posteriores coinciden; ante cambios ajenos, detenerse. V3 sigue inactivo y el candidato Rhino no se revisó en esta fase.
