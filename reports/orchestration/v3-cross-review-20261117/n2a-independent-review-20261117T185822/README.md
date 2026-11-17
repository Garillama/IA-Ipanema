# Revisión independiente incremental N2a/N4a

**Claude: approve para el contrato/candidato aislado. Estado global: `needs_evidence`.** No se modificó el candidato, no se integró V3 y no se accedió a producción.

## Identidad y ejecución

- Candidato: `288ef3739417e0e15e105e4826ea65598f17c0807265ed68cf42d3fc5008aa6f`
- Delta: `715707766927a7e7e0ea6890add15364c048d3607e958261fd29577cc87b2a1b`
- Paquete congelado: `56951ce2905ab945b80eb218436aa78e8ed1e37aa771ab630baa09bc2bfd0d00` (191609 bytes)
- Respuesta íntegra: [`claude-response-complete.json`](claude-response-complete.json), SHA256 `3176d33b95f02ad0d8904b6d0cc852f98e30c44b1180a24ce0c8ef84bf2fece1`
- Recibo: [`claude-receipt.json`](claude-receipt.json); una llamada, 56.32 s, exit 0, proceso recogido, JSON válido. Modelo `claude-sonnet-5-5`, esfuerzo `medium`.
- Pruebas: la revisión recibió evidencia de 106/106 focalizadas; Claude no las ejecutó. No se repitieron las 159 históricas.

## Dictamen

- **N2a — resuelto en la interfaz aislada.** La misma referencia no basta por sí sola; `MaterialEvidence` debe enlazar objeción, candidato y fuentes y el recibo debe probar la demostración. La materialidad real queda a cargo del futuro verificador del controlador. Las fuentes originales pueden reutilizarse cuando una medición o refutación realmente sustentada sea verificada. Un cambio de texto/hash no demuestra materialidad.
- **N4a — resuelto en el contrato aislado.** El resultado sintético usa `synthetic_pass`, `authorization_ready=false`; los flags de implementación/publicación/activación permanecen falsos.
- No se identificaron defectos reproducibles nuevos ni regresiones concretas en N1/N3/N4. Claude no vuelve a aprobar esos hallazgos para este hash.
- **N2a-dep (INFO, dependencia de integración):** falta el verificador material real; la interfaz por defecto falla en cerrado. No es un defecto de la corrección aislada.
- **N2a-fixture-scope (INFO menor):** las fixtures automáticas de `new_fact` ejercitan el contrato, pero no validan pertinencia semántica general. La documentación ya limita esa afirmación; no requiere cambios.

## Alcance y límites

Claude revisó los dos archivos cambiados: `tools/ipanema/orchestration/code_review.py` y `tests/unit/test_code_review_v3.py`. `council.py` es contexto sin cambios (hash conservado), no fue leído íntegramente en el paquete. La revisión fue estática; no ejecutó pruebas.

El candidato está revisado para esta corrección aislada, pero **no está listo para integración operativa**: antes hacen falta el verificador real y revisión de sus bindings con productores/almacén/consumidores; N1/N3/N4 conservan sus dictámenes ligados al hash anterior. No hace falta otra corrección aislada ahora.
