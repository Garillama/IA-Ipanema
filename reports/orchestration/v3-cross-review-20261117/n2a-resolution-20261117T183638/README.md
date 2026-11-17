# Corrección focalizada N2a y señal N4a

**Candidato aislado corregido y probado. Estado: needs_evidence; pendiente de revisión independiente.** No se integró, activó ni modificó el orquestador operativo. Cero proveedores, Antigravity, clientes o solicitudes a producción.

## Reproducción y causa

[Antes](before-reproduction.json): con el candidato fb292ff7, source:sample.py era a la vez evidencia original y único paso incremental; no había demostración nueva. Con confirmación sintética del origen, el cierre se aceptaba como approved_for_authorization. Eso confirma N2a y el riesgo de lectura parcial N4a; no demuestra bypass del revisor.

[Después](after-reproductions.json):

| Caso ejecutado | Resultado | Cierre |
|---|---|---|
| Misma referencia, sin demostración; origen disponible | changes_requested | No |
| Refutación: claim de0 definiciones, conteo real1, mismo archivo/referencia/bytes | synthetic_pass | Sí, con revisión del origen |
| Hecho medido no evaluado previamente: conteo real1 | synthetic_pass | Sí, con revisión del origen |

La materialidad se comprueba en esas fixtures mediante observaciones reales y predicados fijos del controlador. No se decide porque cambie un texto, ID o hash. Las fixtures no verifican claims de clientes ni constituyen un verificador semántico universal.

Causa raíz: el paso add_evidence solo pedía referencias probadas, sin demostración material específica; el replay repetía esa insuficiencia. [Defensa/diseño previo](author-defense.md).

## Corrección mínima

- Se extiende la **misma interfaz existente** con incremental_evidence. Debe devolver MaterialEvidence solo tras comprobar materialidad, pertinencia al claim y procedencia del artefacto. Predeterminado: None, falla en cerrado.
- El mismo reductor exige esa verificación; el replay exige además recibo vigente/probado, específico para hallazgo/claim/candidato, fuentes y artefacto. No existe segunda máquina de estados.
- Se conserva la evidencia original. Se permiten nuevas mediciones y refutaciones documentales sobre los mismos hechos/fuentes. Los hashes solo comprueban integridad y reutilización; la materialidad corresponde al verificador confiable.
- La confirmación del revisor originario sigue siendo obligatoria; la demostración del autor no cierra.
- **N4a:** resultado versionado /2 con synthetic_pass y authorization_ready=false en éxitos sintéticos. Ya no parece una aprobación operativa aunque el consumidor mire solo state.

[Contrato y límites](contracts.md) · [ADR pendiente](ADR.json).

## Identidad y alcance

Anterior intacto: `fb292ff7f11c2ccaed5e90a2325c1703f23ece67bdc1b2a6f96ad3c6d49b8e4f`.

Nuevo parche completo: `288ef3739417e0e15e105e4826ea65598f17c0807265ed68cf42d3fc5008aa6f`.

[Diff completo](candidate.patch) · [Delta mínimo respecto al anterior](delta-from-fb292ff7.patch) · [Manifiesto, hashes previos/posteriores y respaldos](manifest.json).

| Archivo | Contra fb292ff7 | SHA256 nuevo |
|---|---|---|
| `tools/ipanema/orchestration/council.py` | Idéntico | `3bbe36122abe1966fa0fc89eb2a23576284797c4afb2a1b4c071e83cb4cfad7a` |
| `tools/ipanema/orchestration/code_review.py` | Modificado | `4b9cd45475a9a8c0926d8b66ce86d02a153981a0273360760841d901374033e0` |
| `tests/unit/test_code_review_v3.py` | Modificado | `d56a68eb1b4e898d7fecb687853c79e22be07c399be68b5aff1f362bd77b9b77` |

Delta de **dos archivos**: code_review.py y su suite. council.py permanece idéntico al candidato anterior, con su wrapper sin modificar. El parche completo sigue representando el candidato original de tres archivos frente al repositorio operativo. No se aplicó; git apply --check pasó.

## Pruebas focalizadas y compatibilidad

**106/106 pruebas del gate aprobadas:** 90 anteriores directamente afectadas por reducer/interfaz/resultado, adaptadas explícitamente;16 nuevas N2a/N4a. [Salida completa](tests-final.txt) · [Recibo](gate-test-receipt.json).

Se comprueban repetición vacía, reetiquetado, falta de contraejemplo, refutación material con mismos bytes, hecho medido, claims ajenos, pruebas/artefactos alterados, ausencia de recibo, scope incorrecto, autor sin autoridad, confirmación del origen ausente y señal sintética. Se conservan los casos N1, N3 y N4 de hashes/permisos, historial, migración y procedencia sin reabrir su diseño.

No se repitieron las159 históricas ni las9 pruebas de recibos de módulos sin cambios. La evidencia anterior se conserva; no se presenta como una ejecución nueva. Los hashes de fuentes operativas, políticas y candidato anterior se verificaron íntegros. [Recibo del controlador](controller-receipt.json).

## Riesgos y condiciones para cerrar esta fase

La interfaz no hace magia semántica: una implementación real debe cargar artefactos verificados, comprobar hechos/contraejemplos y relación con el hallazgo, y distinguir observaciones ya evaluadas. No debe construir MaterialEvidence desde una afirmación JSON del modelo. El host/controlador sigue siendo frontera de confianza, no una autenticación criptográfica por tipo/hash. Sin verificador real se conserva needs_evidence o la objeción abierta.

El cambio de resultado /2 y registro /2 exige consumidores explícitos. Los registros históricos no se reescriben ni sus cierres se migran automáticamente. Las referencias originales y sus dictámenes permanecen intactos; una revisión de fb292ff7 no aprueba el hash nuevo. Las dependencias reales de identidad, historial, QA y Antigravity siguen pendientes.

Para cerrar la fase aislada: revisión independiente del **nuevo hash**, con estas reproducciones y contrato; aceptación o mitigación de los riesgos restantes. **No se llamó ni se llamará automáticamente a Claude/Codex.** Cualquier llamada requiere autorización específica. Cerrar la fase aislada no autoriza integración, políticas ni producción.
