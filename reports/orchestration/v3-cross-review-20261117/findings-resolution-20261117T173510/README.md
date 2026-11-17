# O1/O2/O3 — defensa y candidato corregido aislado

**Estado: needs_evidence. Sin integración ni activación.** Codex sigue siendo autor. No se ejecutaron Claude, Antigravity, nuevas llamadas a Codex ni operaciones de producción.

## Resultado concreto

- O1: se acepta el registro contradictorio y se consulta exclusivamente agent_policy; identidad/capacidad/autorización quedan separadas. Continúan siendo necesarios dos revisores no autores, que la política dual actual no proporciona.
- O2: se acepta la incompatibilidad y se propone un binding v2 explícito, separado del recibo legado inmutable. No se inventan fingerprints del productor. Un QA histórico sin cobertura sigue insuficiente.
- O3: se acepta la falta de semántica de re-revisión y se añade máquina de estados e historial conservado. El autor no cierra hallazgos; una refutación puede confirmarse sobre el mismo hash mediante revisión nueva. Un diff diferente no limpia el historial adverso.

[Defensa del autor con evidencia, alternativas y riesgos](author-defense.md) · [Diseño, contratos y migración](design-contracts.md) · [ADR pendiente](ADR.json).

Las respuestas anteriores son defensa del autor, **no aprobación independiente**. O1/O2/O3 permanecen pendientes de revisión del nuevo diff por Claude; su changes_requested original sigue conservado.

## Identidad y alcance

Parche anterior intacto: `69c75ac77596439227c4066439711334e8c7bf2724b5a28fbbfabdf2336e0dbb`.

Nuevo parche completo: `c240b16f37ec13a84db4e54f656f15beda7316642c2e078e8d94b906d7ed6085`.

[Diff completo](candidate.patch) · [Delta frente al candidato anterior](incremental-from-69c75ac.patch) · [Manifiesto y respaldos](manifest.json).

Tres archivos del alcance original; frente al repositorio operativo: una modificación, dos altas, ninguna eliminación. Frente al candidato anterior: cambios en esos mismos tres archivos. Solo existen en la copia aislada indicada en el manifiesto.

| Archivo | SHA256 operativo previo | SHA256 nuevo candidato |
|---|---|---|
| `tools/ipanema/orchestration/council.py` | `4ec261a0d84fbdc12d5abf85eab489d21cf85f30af57eac9769c722d17541261` | `f2e7ac875515f9d625338172eec8181aea2d9755ff9813bbf15ee532f605a1b6` |
| `tools/ipanema/orchestration/code_review.py` | `ausente` | `ef2340db1abc358ee569439968df574f2646cfbf31ea7e545e37c64ee8f597f0` |
| `tests/unit/test_code_review_v3.py` | `ausente` | `b45b23e2e19db2408f5bd90282fa205a34b6820389e1f490c4e609e13ab7bd09` |

[Recibo de integridad](controller-integrity-receipt.json): originales del candidato anterior intactos, archivos operativos comprobados sin cambios, nuevas rutas ausentes del repositorio operativo y git apply --check correcto. No se cambiaron models.json, adapters.py, permisos ni el orquestador operativo.

## Pruebas reales de esta intervención

**60/60 pruebas aprobadas: 29 focalizadas nuevas y 31 casos anteriores del gate con fixtures migradas** con fuentes temporales y proveedores/política futura sintéticos, sin red. [Salida íntegra](focused-results.txt) · [Recibo](focused-receipt.json).

No se repitieron las 159 pruebas ni se trasladó su aprobación al diff nuevo. Se conservó un fallo intermedio de indentación del archivo de pruebas, corregido antes de la ejecución final, y las ejecuciones intermedias focalizadas. No hubo fallo operativo ni llamada a proveedores.

Se conservaron los 31 casos anteriores por nombre y se adaptaron sus fixtures a la nueva política simulada y los bindings explícitos; se ejecutaron porque cambió el código que cubren. No se ejecutaron las otras 128 pruebas históricas de council/orquestación. 60 pruebas del gate no equivalen a validación de proveedores reales ni regresión completa.

## Riesgos y condiciones pendientes

1. Revisión independiente del nuevo diff; no se reutiliza una revisión del hash anterior como aprobación.
2. Verificación real de identidad/capacidad y wiring del productor v2 con el controlador. Los hashes no autentican al productor.
3. Migración explícita del registro central para Antigravity, si se autoriza en otra etapa. No hay habilitación lateral desde este gate.
4. Revisión adversa de otro candidato exige conciliación explícita; la automatización de ese traslado queda pendiente y falla en cerrado.
5. [Antigravity sigue bloqueado](antigravity-status.md): autenticación acotada, egreso y restricciones nativas no acreditados.
6. Evaluar y ejecutar el QA afectado de council/consumidores antes de solicitar integración; los 31 casos anteriores del gate ya están conservados y migrados. Sin afirmaciones de compatibilidad universal o rendimiento.

## Siguiente operación mínima y permisos

Preparar/congelar un paquete selectivo del **nuevo hash** y solicitar autorización para una revisión de solo lectura de Claude, sin reabrir el consejo completo. La ejecución de Antigravity exige autorización separada para un piloto sintético una vez demostrables autenticación y aislamiento. No procede solicitar integración ni activar V3 mientras falten estas condiciones.

La preparación aislada actual está cubierta por la solicitud del propietario; no concede permiso para integrar, cambiar políticas, llamar a proveedores o publicar. El candidato puede descartarse retirando únicamente esta copia propia; los respaldos originales se conservan y no se modifica el código operativo.
