# Recuperación controlada — dos entregables

Estado: **needs_evidence**. Sin llamada a Claude o Antigravity, sin modificación del candidato y sin integración/activación de V3.

1. **[A — paquete selectivo de Claude](claude/README.md):** 243,861bytes,64.0% menos; tres archivos íntegros, diff/hash, contratos, dependencias y QA preservados. Registro de exclusiones y evaluación de suficiencia. Límites120/240 intactos. No se autorizó ni ejecutó una nueva llamada.
2. **[B — contrato sintético Antigravity](antigravity/README.md):** comando propuesto, fixtures, recursos y cancelación; OS preflight y descendiente sintéticos comprobados sin proveedor. Autenticación, egress y cobertura nativa de restricciones siguen pendientes; no es una ejecución lista para autorizar sin resolverlos.

El candidato sigue en SHA256 `69c75ac77596439227c4066439711334e8c7bf2724b5a28fbbfabdf2336e0dbb`. Las159 pruebas se reutilizaron sin repetirlas. Las únicas pruebas nuevas fueron comprobaciones breves de aislamiento y cancelación sobre código sintético para este piloto. Codex sigue siendo autor y no cuenta como aprobador independiente. Los recibos/ADR históricos no se sobrescribieron.
