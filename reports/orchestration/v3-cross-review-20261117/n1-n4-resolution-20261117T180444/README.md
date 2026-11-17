# Corrección incremental N1–N4

**Candidato corregido y probado; pendiente de revisión independiente. V3: needs_evidence. Sin integración ni activación.**

Se conservaron el candidato c240b16f, la respuesta íntegra de Claude, sus recibos, precisiones y ADR. Codex sigue siendo autor: no se cierran formalmente N1–N4 ni se presenta esta defensa como aprobación independiente.

## Evidencia y cambios

[Defensa previa a la edición](author-defense.md) · [Reproducciones anteriores](before-reproductions.json) · [Contratos y compatibilidad](contracts.md).

- **N1:** definición versionada `ipanema-code-review-context/1`; misma serialización del productor nativo para su dominio JSON, probada llamando a binding local sin red. Permisos pasan por un adaptador de contexto explícito; no se atribuyen al productor operativo ni se insertan en recibos históricos. Ausencia de contrato/campos obligatorios se rechaza o queda pendiente.
- **N2:** evaluate deriva el cierre exclusivamente de replay de la misma máquina de estados. Respuesta suelta o terminal declarado no cierran. Se requiere evidencia nueva verificable, revisión pendiente y confirmación del origen acreditada por la interfaz de controlador.
- **N3:** historial obtenido de interfaz de lectura obligatoria, índice completo y cabecera independiente. Los hallazgos históricos se evalúan antes de envelopes ausentes/obsoletos; BLOCKER conserva blocked y HIGH conserva changes_requested. Migración tipada por objeción preserva origen/definición, pasa por nueva evidencia/revisión y no cierra automáticamente. Una revisión nueva acreditada puede sustituir el efecto del dictamen previo sin borrar su historial.
- **N4:** principal declarado se conserva como dato; atestación de adaptador se obtiene de una interfaz Python de controlador. Se comprueban principal/sin padre, capacidad, recibo, binding, candidato y permisos. El hash no autentica identidad. El resultado informa trust_basis, synthetic_only e identity_verified_by_hash=false. El transporte actual no tiene bridge: sin evidencia acreditada permanece needs_evidence.

## Identidad del paquete

Anterior: `c240b16f37ec13a84db4e54f656f15beda7316642c2e078e8d94b906d7ed6085`.

Nuevo parche completo: `fb292ff7f11c2ccaed5e90a2325c1703f23ece67bdc1b2a6f96ad3c6d49b8e4f`.

[Diff completo](candidate.patch) · [Delta contra c240b16f](delta-from-c240b16f.patch) · [Manifiesto y respaldos](manifest.json).

| Archivo | SHA256 candidato anterior | SHA256 nuevo candidato |
|---|---|---|
| `tools/ipanema/orchestration/council.py` | `f2e7ac875515f9d625338172eec8181aea2d9755ff9813bbf15ee532f605a1b6` | `3bbe36122abe1966fa0fc89eb2a23576284797c4afb2a1b4c071e83cb4cfad7a` |
| `tools/ipanema/orchestration/code_review.py` | `ef2340db1abc358ee569439968df574f2646cfbf31ea7e545e37c64ee8f597f0` | `e8ac3a263a2b94922f1c0d5844517913e714b5234c5d1f30a7c11a22224e2cba` |
| `tests/unit/test_code_review_v3.py` | `b45b23e2e19db2408f5bd90282fa205a34b6820389e1f490c4e609e13ab7bd09` | `39763d930ac76248c9800456793a26b16f9053cf1071b1eec845a1650cd97b9d` |

Solo los tres archivos del alcance original, dentro de la copia aislada. Frente al repositorio operativo: una modificación y dos altas; ninguna eliminación. No se cambiaron productores operativos, políticas, adaptadores, modelos ni orquestador. `git apply --check` correcto; no se aplicó el parche. [Recibo de integridad](controller-receipt.json).

## Pruebas ejecutadas

**90/90 casos del gate:** 60 anteriores con fixtures migradas +30 casos nuevos N1–N4. [Salida](tests-attempt-3.txt) · [Recibo](gate-tests-receipt.json).

**9/9 pruebas existentes de recibos**, ejecutadas contra los módulos aislados. [Salida](legacy-receipts-results.txt) · [Recibo](legacy-receipts-receipt.json).

Total: **99 pruebas aprobadas**. Solo fixtures/proveedores sintéticos; no inferencia, red ni clientes. No se ejecutó la suite histórica completa de159 ni pruebas de navegación. Las ejecuciones intermedias se conservan: ajustes de fixtures ante transición más estricta, conservación de severidad y duplicación accidental de un recibo; ningún cambio operativo.

La migración de fixtures no presenta las atestaciones sintéticas como reales. Las salidas approved_for_authorization de casos sintéticos llevan synthetic_only=true y todas las banderas operativas falsas.

## Compatibilidad y riesgos

El parser de recibos legacy y los módulos de V2 permanecen sin cambios. La firma del wrapper mantiene argumentos previos y añade controller opcional; sin ese objeto no aprueba. Los bindings v2 originales se conservan pero deben revalidarse explícitamente bajo el contrato nuevo; no se les añade procedencia retroactiva. Answers y review_history de llamador no sustituyen estado/historial del controlador.

La interfaz del controlador es una frontera de confianza, **no un sandbox ni una firma criptográfica**. Código Python malicioso con ejecución dentro del controlador puede mentir; este gate no pretende proteger un host comprometido. La integración futura deberá implementar y demostrar validación nativa, autorización, completitud del historial y lecturas consistentes de cabecera/snapshot. El código aislado no implementa almacenamiento, OAuth ni nuevos proveedores.

Se conserva la política central dual y dos revisores no autores. Las pruebas con Antigravity solo usan mocks explícitos; no es miembro habilitado. No se implementaron refactorizaciones LOW. La regla MEDIUM se endurece únicamente en cuanto a evidencia de cierre: una respuesta suelta ya no cuenta como cierre/condición suficiente; debe constar en el flujo verificado.

## Siguiente revisión y autorización

Preparar un paquete selectivo del nuevo hash para revisión independiente de Claude sobre N1–N4 y sus pruebas. **No se ejecutó ni se ejecutará automáticamente** con esta autorización. Antes de cualquier integración deberán resolverse esa revisión, las dependencias reales de controlador/QA y las condiciones de Antigravity. No procede activar V3.

[ADR de esta corrección](ADR.json): needs_evidence, objeciones históricas conservadas, sin autorización de integración/producción. Reversión local: descartar únicamente esta copia propia; los respaldos anteriores permanecen íntegros y no hay cambios operativos que revertir.
