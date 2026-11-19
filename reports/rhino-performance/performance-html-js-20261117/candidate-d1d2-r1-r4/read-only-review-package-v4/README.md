# Preflight actualizado de revisión read-only — hero D1/D2/R1/R4

Estado: **`needs_evidence`; Claude y Codex no fueron invocados.**

Este paquete conserva el candidato, dependencias y recibos históricos. El paquete v3 original permanece intacto. El nuevo preflight documenta la copia aislada del controlador con contrato tipado v2.

## Identidad del candidato

- `sections/hero.tpl`: `1e70c54c4c5bc38711272284843d8881c4354ac7725e9de56c0223b599c3e65d`
- `snippets/image.tpl`: `e4e622e0c561c4450138e7717a1e5af95cf19d0184aee5cbcb89990f7ada767e`
- Diff incremental: `ff73a41106aa153e30f0b84bf018ce89f80d693a68551eb39ab021ce1c09406b`
- Manifiesto externo v3 recibido/verificado: `33908cf593d8e327319746b13c7f9feed800a75adb0fb7999ebfa2874882b0ab`

## Contrato de revisión

**Candidatos:** `sections/hero.tpl`, `snippets/image.tpl`.

**Contexto de solo lectura:** `blocks/slide.tpl`, `blocks/banner.tpl`, `blocks/image.tpl`, `sections/hero-divided.tpl`, `sections/category-hero.tpl`, `layouts/layout.tpl`, `static/js/libraries-standalone.js`. Las rutas lógicas y sus hashes están en `manifest.json`.

**Escritura:** `write_files=[]`; las dos tareas tienen `task.allowed_files=[]`. Ambas leen los nueve archivos. `analysis.files` y los archivos del ADR se limitan a los dos candidatos. Una dependencia puede citarse como `source:<ruta>` si su recibo corresponde al ledger, run y hash, pero no declararse como archivo afectado ni escribible.

El tamaño conjunto de las nueve fuentes es **194.145 bytes**, dentro del límite de lectura de fuente de 300.000 bytes del controlador. Los contenidos están bajo `candidate/` y `context/`; el contrato usa las rutas lógicas sin prefijo.

La verificación v3 encontró coincidencia del manifiesto externo y de las 22 entradas declaradas; no hay discrepancias. El snapshot v3 no se modificó.

## Preflight local

**125 pruebas focalizadas pasaron; 0 fallos y 0 errores.** Casos: 2 candidatos + 7 contextos; subconjunto de escritura; cita de dependencia como evidencia; rechazo de contexto como diff; refs válidas, inexistentes y de otro run/candidato; read-only; dual council; agregación; recibos históricos. Sin proveedores, red ni producción. Log y resumen en `tests/controller-contract-focused-tests.*`.

Esto prueba la copia aislada; no constituye revisión independiente ni integración del controlador.

## Límite del sello de plan

`file_contract_sha256` detecta modificaciones si no se recalcula, pero es un hash no autenticado. No es una firma ni autorización y no evita que quien puede editar el JSON vuelva a sellarlo. El plan exacto debe revisarse antes de ejecución. No se añadió un sistema paralelo de permisos.

## Comando de planificación preparado (no ejecutado)

Después de revisar e integrar la adaptación, el plan se generaría con:

```bash
python3 tools/ia.py --project rhino-performance orchestrate plan "Revisión independiente read-only de la hero responsive D1/D2/R1/R4" --scope theme --read-only --council full \
  --candidate-file sections/hero.tpl \
  --candidate-file snippets/image.tpl \
  --context-file blocks/slide.tpl \
  --context-file blocks/banner.tpl \
  --context-file blocks/image.tpl \
  --context-file sections/hero-divided.tpl \
  --context-file sections/category-hero.tpl \
  --context-file layouts/layout.tpl \
  --context-file static/js/libraries-standalone.js
```

No se incluye `--write-file`; ambas tareas deben terminar con `allowed_files=[]`. El comando no se ejecutó porque el controlador operativo no se modificó y planificar releería la información local del proyecto. Una llamada posterior al consejo requiere autorización separada.
