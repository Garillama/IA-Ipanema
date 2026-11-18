# Preflight de recuperación del consejo dual

Estado: **preparación parcial; `needs_evidence`; proveedores no invocados**.

## Snapshot lógico congelado

Ruta: `logical-review-snapshot/`. El directorio contiene únicamente los dos archivos bajo sus nombres lógicos y está marcado como solo lectura.

| Archivo | SHA256 candidato |
|---|---|
| `sections/hero.tpl` | `1e70c54c4c5bc38711272284843d8881c4354ac7725e9de56c0223b599c3e65d` |
| `snippets/image.tpl` | `e4e622e0c561c4450138e7717a1e5af95cf19d0184aee5cbcb89990f7ada767e` |

SHA256 del manifiesto del snapshot: `9b1b41ddc53f12ebe87eb2a9330822622551afd85ba43a2b22e8f6f1972458c8`.
SHA256 del resultado actualizado de preflight: se registra en `logical-contract-preflight-results.json` y en el manifiesto del paquete v2.
Paquete lógico v1 preservado: `logical-review-package/`. El paquete v2 corregido con este hallazgo y su manifiesto se identifican al final de este informe.

## Pruebas locales del contrato existente

Resultado en `logical-contract-preflight-results.json`:

- Los nombres lógicos de ambos candidatos son aceptados por el validador de rutas de archivos del consejo.
- Una referencia a `static/js/store.js`, fuera de alcance, es rechazada.
- El binding del controlador incluye ambos hashes exactos y la identidad del run.
- El binding del run genera IDs `source:` para ambos hashes; una objeción sintética puede incluirlos. Sin embargo, `validate_objections` acepta también `invented-evidence-id`: no verifica que cada referencia exista en el ledger. La vinculación está en el contexto/run, pero la integridad de referencias individuales no queda forzada por el validador.
- La tarea read-only tiene lista de escritura vacía y el validador rechaza cambios propuestos por el revisor.

Estas pruebas son locales y sintéticas; no invocaron Claude/Codex ni modificaron el controlador.

## Bloqueo: dependencias de solo lectura

El controlador actual no separa `allowed_files` globales de archivos de contexto read-only. Además, la validación de referencias de evidencia es sintáctica, no referencial:

- `tools/ipanema/orchestration/planner.py` establece `task.read_files = plan.allowed_files`; en un plan `read_only`, `task.allowed_files` queda vacío.
- `tools/ipanema/orchestration/engine.py` exige que cada `task.read_files` pertenezca a `plan.allowed_files`.
- `tools/ipanema/orchestration/council.py` limita las rutas citadas por la propuesta al mismo conjunto global, pero `validate_objections` no contrasta `evidence_refs` con `controller_evidence`.

Por eso, con `allowed_files` global exactamente limitado a los dos candidatos, los revisores no pueden recibir contenido de consumidores como `blocks/slide.tpl` como contexto de archivos. Sí podrían recibir metadatos del mapa de consumidores en `plan.consumers`, pero no el código de esos consumidores. Incluirlos en el allowlist global no los haría editables en un plan read-only (las tareas conservan `allowed_files: []`), aunque sí excedería la condición literal de allowlist global de dos archivos. No ampliaré esa lista por decisión propia.

El preflight se detiene aquí, como se pidió: bajo la interpretación literal no se pueden entregar dependencias y la integridad de las referencias individuales tampoco está garantizada por el normalizador.

## Recibo de Codex anterior

El run anterior observó `inactivity`, `duration_s=91.992`, `idle_timed_out=True`, `process_reaped=True`, `context_complete=True`, contexto de `168970` bytes y sin uso reportado por el proveedor. Esto no demuestra cuota, autenticación ni que el tamaño del contexto fuera la causa.

SHA256 del recibo: `2b87e9cb6eb8825c91442e456f0dc512093e14c62670f8291549299c2f17c6ea`.

## Comando oficial previsto (no ejecutado)

```bash
IPANEMA_THEME_ROOT='/home/alanrichard/Escritorio/IA inversa/reports/rhino-performance/performance-html-js-20261117/candidate-d1d2-r1-r4/logical-review-snapshot' python3 tools/ia.py orchestrate plan 'Revisión dual read-only del candidato hero D1/D2/R1/R4' --scope theme --read-only --council full --council-rounds 2 --file sections/hero.tpl --file snippets/image.tpl
IPANEMA_THEME_ROOT='/home/alanrichard/Escritorio/IA inversa/reports/rhino-performance/performance-html-js-20261117/candidate-d1d2-r1-r4/logical-review-snapshot' python3 tools/ia.py orchestrate run <plan_generado.json> --execute  # NO EJECUTAR: preflight bloqueado y requiere nueva autorización
```

El comando de planificación produciría un plan read-only con los nombres lógicos correctos y el allowlist exacto de dos archivos, pero no tendría código de consumidores en `read_files`. El comando `run` queda expresamente bloqueado; no existe una ejecución dual autorizable bajo las dos condiciones simultáneas sin que el propietario aclare el alcance de lectura.

## Siguiente paso mínimo

Se requiere una nueva instrucción del propietario sobre una de estas alternativas:

1. Mantener el allowlist global en dos archivos y aceptar que la revisión vea solo el mapa de consumidores, no su código; o
2. Autorizar que el allowlist global de **lectura** incluya dependencias concretas, manteniendo `task.allowed_files=[]` para todos los revisores y sin ampliar ningún permiso de escritura.

No se modificó el candidato, el orquestador, la política, Rhino ni ningún recurso remoto.

Paquete lógico v2: `logical-review-package-v2/`; manifiesto SHA256 `ca3d817761c8d3dc9894e02ae29c709a664ac1a348c7eacb64c16e261e915ba0`. El SHA256 del informe se entrega en el resumen final.
