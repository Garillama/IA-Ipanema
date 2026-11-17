# Revisión independiente N1–N4 — resultado

**Claude: changes_requested. V3: needs_evidence.** Candidato intacto; ninguna integración/activación ni modificación del orquestador.

## Ejecución única

Se comprobó primero que la interrupción no había iniciado una revisión nueva. Se ejecutó una sola invocación con el JSON literal congelado y sin wrapper duplicador, retries, fallback o ampliación de límites. La autorización está consumida.

- Parche: `fb292ff7f11c2ccaed5e90a2325c1703f23ece67bdc1b2a6f96ad3c6d49b8e4f`.
- Paquete: `198dfc02fbf49c85ac3f08eb8ad02bef51f50ee8830ce7e44071c7ea393bf192`, **422293 bytes**.
- Modelo/esfuerzo: `claude-sonnet-5-5` / `medium`.
- Duración: **98.684 segundos**; exit0, contrato válido, proceso recogido y cambios vacíos.
- Límites originales: inicio30s, primera salida CLI120s, inactividad90s, absoluto240s. Primera salida CLI no demuestra primer token del modelo.
- Coste informado por proveedor: USD 0.807312; sin estimación propia.

[Respuesta estructurada íntegra](claude-response-complete.json) · [Recibo](claude-receipt.json) · [Paquete literal](review-packet.json) · [Congelación/suficiencia](freeze.json) · [Preflight](execution-preflight.json) · [Postflight](postflight.json).

El reporte estructurado añade clasificación y estados individuales para esta revisión; no modifica el schema del gate candidato ni se convierte automáticamente en un recibo de cierre. Se preserva el resultado final completo, no razonamiento privado ni stderr crudo.

## N1–N4 y comparación

| Hallazgo | Dictamen de Claude | Alcance y pendiente |
|---|---|---|
| N1 | Resuelto en el contrato aislado | Canonización compatible y contexto adaptado explícitamente. |
| N2 | Parcialmente resuelto | Replay único aplicado; novedad de evidencia pendiente (N2a). |
| N3 | Resuelto en el contrato aislado | Historial, severidad y migración explícita; store real pendiente. |
| N4 | Resuelto en el contrato aislado | Identidad/procedencia separadas; bridge real pendiente y LOW N4a. |

[Comparación](comparison.json). Estos estados son la evaluación independiente de Claude sobre este hash; no sustituyen los registros anteriores ni autorizan integración. No se crearon bindings/resoluciones ficticias para cerrar automáticamente el gate.

## Hallazgos nuevos por naturaleza

- **N2a — MEDIUM, riesgo arquitectónico:** evidencia marcada como nueva puede ser únicamente la referencia original del hallazgo. Se comprueban orden de eventos, recibo vigente y confirmación del origen, pero no novedad/pertinencia incremental. Los eventos no revisores son afirmaciones del controlador y no forman parte de la cabecera de reviews. Es revisión estática apoyada en el test conservado; Claude no ejecutó un contraejemplo.
- **N4a — LOW, riesgo arquitectónico:** el estado principal puede decir approved_for_authorization en fixtures aunque synthetic_only=true. Un consumidor debe conservar esa distinción. No hay consumidor operativo ni bypass de autorización demostrado; no se presenta como bloqueo crítico autónomo.
- **N1a — INFO, dependencia de integración:** alternative_sha256 nativo identifica una alternativa y el binder aislado espera identidad de candidato. El bridge futuro deberá conservar esa distinción sin reescribir recibos históricos. No es una función ya implementada ni un defecto nuevo de producción.

No se reportaron preferencias de estilo bloqueantes ni un nuevo defecto clasificado como reproducible_defect. Duplicidad y mantenimiento pasan; arquitectura falla por N2a; regresión permanece needs_evidence por integración real no validada. Se evita confundir trazabilidad estática con reproducción ejecutada.

[Auditoría de referencias y precisiones](controller-findings-audit.json) conserva el texto de Claude y registra rangos reales. Algunas líneas están desplazadas. La crítica a la novedad está sustentada; no implica que sea obligatorio cambiar archivos o URLs para refutar: una explicación nueva puede usar la misma fuente si hay un artefacto incremental verificable.

## Integración futura, separada de defectos aislados

Siguen pendientes: fuente real de historial/cabecera de checkpoint consistente; atestación de recibos nativos y capacidades; QA con cobertura de hashes; adaptación explícita de alternativa/candidato; política/adapter de Antigravity e independencia real. Las interfaces actuales documentan esas dependencias, no las implementan. No se accedió a clientes, producción ni credenciales comerciales.

Se preservaron las99 pruebas (90 gate+9 recibos); no se repitieron ni esas ni las159 históricas. Claude declara no haberlas ejecutado. El snapshot del proveedor solo contenía el paquete; fuentes completas únicas y diff completo único. La red del transporte existente sigue sin firewall de destinos; herramientas, MCP y subagentes permanecen deshabilitados por CLI. No se afirma egreso API-only.

## Condiciones para cerrar la fase aislada y siguiente paso mínimo

1. Definir evidencia incremental de una objeción: reutilizar únicamente la referencia original no debe satisfacer la novedad; permitir nueva explicación/artefacto verificado sobre fuentes existentes.
2. Aclarar la confianza/integridad de los eventos no revisores; justificar frontera de controlador o vincular su snapshot, evitando infraestructura general innecesaria.
3. Preparar una corrección aislada mínima de N2a con prueba negativa de repetición y positiva de refutación documental. **Requiere nueva autorización; no se implementó.**
4. Resolver la objeción mediante revisión independiente del hash resultante, también autorizada por separado. No hay bucle automático.

N4a puede tratarse con contrato/guard del consumidor antes de integrar; N1a pertenece al bridge futuro. Una respuesta favorable sobre la fase aislada tampoco autorizará V3 operativo.

[ADR](ADR.json): needs_evidence, candidato sin cambios y autorización de esta revisión consumida. Siguiente operación recomendada: autorizar únicamente la definición/corrección aislada y pruebas de N2a, sin nuevos proveedores ni integración.
