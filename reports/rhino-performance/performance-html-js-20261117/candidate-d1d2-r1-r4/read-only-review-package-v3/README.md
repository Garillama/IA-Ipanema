# Preflight del paquete read-only de revisión hero v3

Estado: **`needs_evidence`; Claude y Codex no fueron invocados**.

## Candidato congelado

- `sections/hero.tpl`: `1e70c54c4c5bc38711272284843d8881c4354ac7725e9de56c0223b599c3e65d`
- `snippets/image.tpl`: `e4e622e0c561c4450138e7717a1e5af95cf19d0184aee5cbcb89990f7ada767e`
- Diff incremental SHA256: `ff73a41106aa153e30f0b84bf018ce89f80d693a68551eb39ab021ce1c09406b`

## Contexto de solo lectura

| Ruta lógica | SHA256 | Necesidad |
|---|---|---|
| `blocks/slide.tpl` | `ab5e8d97095b36101fe5d4b66b7facbcdfdd87ab03458da5d909b00f9c868a64` | Image helper consumer; responsive desktop/mobile art direction and first/subsequent slide lazy behavior. |
| `blocks/banner.tpl` | `61bcb60817456a10177723b8a148b9027f130804b3245f1e5698d087d9de906c` | Image helper consumer; responsive banner variants and priority/lazy paths. |
| `blocks/image.tpl` | `ab10579daf74db55eb687b29641947cd67b3145b32a8b65cc7935018789d307f` | Image helper consumer; editor-configured desktop/mobile image settings. |
| `sections/hero-divided.tpl` | `30a85e7b94e062889794463d9f2138dc69d58d620631631e2ab26b3a7f7cb487` | Shared helper consumer with multiple desktop/mobile images, placeholders, and lazy loading. |
| `sections/category-hero.tpl` | `ebde50d16b336c18aae56a1ab93817c22fa366c205a169671f453271051e304b` | Shared helper consumer for category image and configured mobile alternative. |
| `layouts/layout.tpl` | `aa0d59caa5947993a057fc13b4517057286a65a28e24029abb22b839cc18ba31` | Shows how the standalone library bundle is included and its position in document loading. |
| `static/js/libraries-standalone.js` | `da2638c043034114cb004b2fd99cd4d54ee69c7d569bd2c96cca8e586d2e0d34` | Contains local LazySizes runtime/configuration used by lazyload/data-srcset markup. |

Se incluyen además el contrato local de carga de imágenes, los resultados de las pruebas previas y recibos históricos; sus hashes constan en `manifest.json`. No hay credenciales ni configuraciones privadas.

## Separación y permisos

El paquete identifica por separado `candidate_files`, `context_files` y `write_files=[]`. El diseño esperado mantiene `task.allowed_files=[]` para todos los revisores. Sin embargo, el motor exige que cada `read_file` esté en el allowlist global, y el validador de propuestas permite citar cualquier archivo de ese allowlist. El campo `candidate_files` no se aplica como límite independiente por el gate. Así, aunque el plan read-only impide escrituras, el controlador no garantiza extremo a extremo que un archivo de contexto no sea descrito como parte del candidato.

Por la condición indicada, **se detiene el consejo** hasta que la separación tipada esté aplicada y verificable.

## Referencias de evidencia

`reference/audit_controller_evidence_refs.py` contrasta las referencias persistidas con IDs del `evidence.json` del mismo run y comprueba que el ledger tenga el mismo `source_binding`. En el recibo histórico que corresponde a la revisión conservada se verificaron 88 apariciones de referencias (3 IDs únicos): 0 desconocidos, 0 IDs duplicados y 0 discrepancias de binding. Esto solo verifica ese run histórico; no aprueba este candidato.

La ruta efectiva sigue sin garantizar todos los refs: `validate_objections` exige que `evidence_refs` sean cadenas, pero no los contrasta con el ledger; la consolidación valida refs de preguntas y defensas, no todas las refs de objeciones. El verificador externo detectaría errores después, pero no bloquea la decisión del consejo.

No existen respuestas de Claude/Codex nuevas cuyos refs puedan verificarse. No se inventaron recibos.

## Adaptación mínima necesaria (no implementada)

1. Añadir conjuntos tipados y disjuntos `candidate_files`, `context_files` y `write_files`; en read-only exigir `write_files=[]` y prohibir deltas.
2. Permitir que el contexto de lectura sea candidatos más dependencias, pero limitar `analysis.files` y cualquier diff a `candidate_files`; citar las fuentes de contexto por IDs `source:` ligados al run.
3. Entregar el ledger a los validadores de propuesta, objeción, preguntas y defensa; rechazar refs inexistentes antes de persistir y consolidar, y comprobar binding contra el mismo run/candidato.
4. Mantener integración/publicación como autorización posterior e independiente.

## Comando del consejo

No hay un comando `orchestrate ... --execute` que cumpla hoy las dos condiciones verificables. No invocar proveedores hasta implementar y revisar la adaptación. Tras esa autorización, el plan read-only deberá tener los nueve paths listados en `global_read_allowlist_required`, `task.allowed_files=[]`, candidatos limitados a dos, y validación referencial activa. Esta preparación no ejecutó QA general, proveedor, red ni storefront.
