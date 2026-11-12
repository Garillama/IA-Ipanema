# V4 — recuperación de Codex y continuación del consejo

12 noviembre 2026. Continuación del ADR `ADR-1136231f425a` y del mismo snapshot. Agregado incremental `ADR-0895add40c30`: **needs_evidence, implementation_allowed=false**. El protocolo pendiente sí terminó; la aprobación técnica no. No se aplicó ningún parche ni se consultó producción/GSC.

## Resultado ejecutivo

- Recuperada la intervención original de Codex, sin repetir la propuesta independiente válida de Claude.
- Dos contrastes reales y dos defensas reales, con contratos nativos y validación aprobados. Cinco preguntas y cinco respuestas conservadas. Ninguna intervención de CommandCode ni sustitución del proveedor.
- Los dos agentes mantienen reservas concretas. Claude corrigió su interpretación anterior del QA y retiró su alternativa de aceptación con seguimiento. No se fabricó consenso.
- El parche de nueve archivos conserva SHA256 `7a5a7066bb22d2f87c18286100a9fba0ce76e50e53a8cf9b211821d0eba8b4a0` y permanece sin integrar. No está listo para solicitar autorización de integración.
- Las 169 unitarias, 13 integraciones y 1 TLS aprobadas se reutilizaron. Solo se añadieron comprobaciones dirigidas a nueva evidencia, no otra auditoría general.

## Diagnóstico operativo

| Comprobación | Evidencia y conclusión |
|---|---|
| Inicio y entrada | Los fallos recibieron el contexto completo y emitieron thread.started/turn.started. El último fallo high recibió 172061 bytes en 0,074 s y emitió salida a 1,49 s. No es un bloqueo demostrado de stdin o arranque. |
| Categoría observada | El controlador canceló y recogió los procesos por **inactividad de stdout/stderr**. No equivale a timeout comunicado por OpenAI ni demuestra congelación. |
| Contrato | En los fallos no hubo respuesta final: el validador nunca llegó a ejecutarse. No hay campo JSON rechazado, texto final sobrante ni truncamiento demostrado. |
| Transporte | El intento instrumentado fallido conservó los 483 bytes recibidos, stderr vacío, sin alcanzar límites de salida. No hay evidencia de atasco por volumen de stdout/stderr. |
| Herramientas | En el intento instrumentado no se observaron eventos de herramientas iniciadas/pendientes. Los logs antiguos no conservan el detalle necesario para afirmar eso retroactivamente. |
| Autenticación/cuota | Las pruebas pequeñas y la recuperación real funcionaron con el mismo mecanismo de acceso. No se observaron errores de autenticación o cuota que expliquen estos fallos; no se pidieron credenciales nuevas. |
| Contexto | Original 210587 bytes; optimizado 172061 bytes. Se conservaron el diff íntegro de nueve archivos y seis originales completos. Se omitieron solo informes QA redundantes ya validados, sustituidos por su recibo/hashes. Reducir contexto por sí solo no resolvió el fallo. |
| A/B de esfuerzo | **Prompt idéntico**, SHA256 `7a39f93ef23ba63024868ea901c67ca70d64d316aab7843f015481af80fccd06`: gpt-6.1-sol high terminó por inactividad a 91,606 s; medium completó contrato válido en 70,765 s. Mismo idle de 90 s; máximo total medium 240 s, menor que high 360 s. |
| Hipótesis mejor respaldada | La carga de la tarea con esfuerzo alto no produjo salida observable dentro del presupuesto de inactividad. El perfil equilibrado existente permite completarla. Una sola comparación no demuestra el tiempo interno de inferencia ni excluye variación del servicio. |
| Tokens/coste | Recuperación Codex: 60364 tokens de entrada, 2483 de salida, 718 de razonamiento según proveedor; no se suman categorías de uso potencialmente solapadas. Coste monetario de Codex no disponible. Los intentos sin turn.completed no entregaron consumo completo: no se anotan como cero. |

La versión instalada era Codex CLI 0.167.1. El ejecutable auxiliar `codex-code-mode-host` existe en el host pero no está incluido en los mounts del runtime aislado. Aparece un evento item.completed de tipo error por esa ausencia. **También aparece en las pruebas exitosas y en la recuperación válida**, por lo que no explica por sí solo la inactividad. No se montó el helper, instaló software ni amplió permisos para evitar el aislamiento. Es una discrepancia operativa separada que puede estudiarse con autorización, no una causa raíz demostrada.

El primer fixture mínimo usó una ruta de symlink sin resolver y falló antes de arrancar; se corrigió el fixture para resolverla como ya hace el engine. Ese fallo **no pertenece al adaptador de producción** y no se cuenta como prueba de autenticación ni como voto. El diagnóstico mínimo válido terminó en 7,755 s y el contrato completo con entrada sintética en 25,15 s. Ninguno aprobó V4.

La documentación oficial describe JSONL y salida estructurada nativa: [modo no interactivo](https://learn.chatgpt.com/docs/non-interactive-mode). La ausencia del helper se verificó en el runtime instalado y sus eventos; no se atribuye a esa documentación.

## Recuperación y continuidad

Se utilizó exclusivamente el perfil balanced ya registrado, no un cambio en models.json, adaptadores o políticas. Los límites no se elevaron. No hubo reintentos automáticos ni failover. Los workers fueron de solo lectura, sin herramientas, con schema nativo. Se conservaron el binding de código/objetivo/AGENTS/permisos y el checkpoint original; no se compartió la propuesta de Claude con Codex antes de recuperar su propuesta independiente.

[Propuestas](recovered-proposals.json) · [contraste](recovered-objections.json) · [defensas](recovered-defenses.json) · [ADR agregado](bounded-council-adr.json) · [tiempos/modelos/consumo](execution-summary.json).

| Intervención nueva válida | Modelo/esfuerzo | Tiempo |
|---|---|---:|
| codex / recovered-Codex-balanced-proposal.json | gpt-6.1-sol / medium | 70.765 s |
| claude / council_defense-claude | claude-sonnet-5-5 / medium | 21.532 s |
| codex / council_defense-codex | gpt-6.1-sol / medium | 31.363 s |
| claude / council_objection-claude | claude-sonnet-5-5 / medium | 37.785 s |
| codex / council_objection-codex | gpt-6.1-sol / medium | 36.785 s |

El agregado registra participación, contraste y defensa completos, pero preferencias distintas y restricciones pendientes. La cobertura del protocolo no es aprobación. No se usan las afirmaciones pass de los modelos como recibos técnicos.

## Objeciones y comprobaciones nuevas del controlador

1. **Granularidad del gate, reproducida.** Con robots_evidence limpio, noindex=false y relevant_errors=[], `_nodes` de seo-page-audit sigue asignando insufficient_evidence. Es conservador; no es un falso aprobado, pero impide cerrar ese control como ausencia observada de restricción. Corrección propuesta: separar el estado de las directivas de otras incertidumbres de indexabilidad, manteniendo unknown para evidencia heredada/ausente y failed ante noindex posterior válido. Requiere un nuevo candidato y pruebas específicas antes de revisión; no se editó ahora.
2. **Expansión de evidencia, medida en un experimento sintético.** 200000 átomos `foo:bar`, entrada de 1599999 bytes, produjeron 32000962 bytes al serializar la misma evidencia en indexability y template_audit. Se observaron 8,741 s de parsing y 1,994 s de serialización con tracemalloc habilitado, y 80713291 bytes máximos trazados de Python. Una muestra por tamaño, sin referencia productiva ni comparativa temporal: prueba el crecimiento, no un coste habitual del sitio. Corrección propuesta: limitar lo persistido por fuente y total, con contadores/truncated, procesando todas las restricciones para no perder un noindex posterior. No cortar el análisis y dar un aprobado falso.
3. **Consumidores del helper, búsqueda acotada realizada.** En tools/tests Python actuales aparecen indexability.py, page_audit.py y tests/unit/test_seo_crawler_v4.py, además de la definición/autollamada. Los consumidores de decisión conocidos migran a evidencia tipada en el diff. No aparecieron otros consumidores de has_noindex en ese alcance. Esto acota el riesgo dentro del checkout, pero no demuestra inexistencia de consumidores dinámicos/externos. Debe documentarse el nuevo contrato de visualización de google_directives; no se marcó compatibilidad universal como pass.
4. **Límites menores conservados como observaciones, no defectos de Rhino demostrados:** NAT64 rechazado de forma conservadora; variantes de robots con versión no soportadas; formas plurales de rutas privadas mencionadas por Claude y meta no estándar `googlebot: noindex`. No hay prueba de que esas rutas existan en Rhino. No se hicieron solicitudes ni se relajó la protección.

[Reproducciones, mediciones y búsqueda exacta](new-objection-probes.json). Son evidencia posterior al intercambio: **ningún agente ha revisado todavía estos resultados adicionales**. No se cambian sus respuestas ni el ledger para simular ese cierre. Cualquier revisión siguiente debe ser incremental sobre estos puntos, sin repetir propuestas.

## Decisión y siguiente paso

Conservar el parche 7a5a7066 sin aplicar. El bloqueo operativo de la intervención faltante está resuelto para esta ejecución; persisten condiciones técnicas. functional/security/compatibility/native_reuse/seo/performance necesitan recibos acotados a una alternativa concreta. El QA aislado sigue válido dentro de su alcance. La alternativa de modificar gate/topes aún no existe como diff aprobado; no se autoriza implícitamente por esta recomendación.

No se solicita autorización de integrar un candidato con estas reservas abiertas. Primero: preparar una corrección mínima de los dos comportamientos reproducidos, documentar contrato del helper y revisar únicamente ese delta; conservar el original y generar hashes nuevos. Después de QA/revisión y recibos, presentar los archivos exactos para autorización local. Integrar IA-Ipanema nunca autoriza modificar el tema remoto.

## Piloto pendiente de cinco destinos

El [procedimiento vigente](../plan-75.md) permanece sujeto a integración autorizada y QA posterior. Selección propuesta: los dos primeros productos y los tres primeros artículos de pending-75.csv, ambos tipos representados; no se ejecutó. Máximo12 solicitudes, concurrencia1, 0,5/s o menos si robots exige más,120s,20s por solicitud,2MB por respuesta y descompresión,3 redirecciones seguras. No seguir enlaces fuera de la selección.

El presupuesto debe contar **cada GET de robots, sitemap si la vía existente lo necesita, documento y salto de redirección**, incluidos los controles adicionales y lecturas de paso; DNS/TLS no son páginas HTTP pero también consumen tiempo y tienen que validarse. Robots desconocido, IP privada, TLS inválido, origen no autorizado o403/429 detienen el lote sin evasión. No ampliar automáticamente para compensar esas lecturas.

La interfaz stock no tiene semillas/lista/exclusiones/resume. Antes de autorizar red falta fijar y revisar una invocación del mismo transporte aprobado que garantice estos cinco destinos o enumerar las lecturas puente inevitables. No se inventó un comando ni se construyó otro crawler. La autorización para integrar deberá ser separada de la autorización de ejecutar/ampliar el piloto.

## Cobertura, permisos y conservación

49/124 HTML con evidencia HTTP individual;75 pendientes (11 productos,64 artículos), sin cambios. Se conservaron quince inspecciones GSC y diez PASS conocidos, que no representan todo el índice. Último estado autorizado disponible de GSC: sin credencial; no se buscó ni extrajo ninguna y no hubo llamadas nuevas.

No se modificaron los seis módulos base, tres tests nuevos no se integraron, nueve hashes del candidato aislado siguen iguales. Orquestador, registro de modelos, políticas, tema, paginación publicada, menús, canonicals y producción sin modificaciones. No hubo push/watch/publish ni clones de tienda/staging. Los worktrees privados utilizados son snapshots de herramientas para revisión, no copias de Tiendanube.

[Verificación final](verification.json). Artefactos operativos conservados en el run indicado en diagnosis.json. La integración de nueve archivos, cambios operativos al adaptador/políticas, ejecución del piloto y ampliación de alcance requieren sus autorizaciones correspondientes. No se pide renovar autenticación de Codex porque no hay evidencia que lo justifique.


## Continuación: tres reservas corregidas en candidato aislado

El estado anterior de needs_evidence se conserva como historial del hash7a5a7066. El [candidato nuevo](../final-candidate/README.md) resuelve las tres reservas, cuenta con revisión final de ambos proveedores y está listo para solicitar autorización específica de integración local. No se aplicó al motor ni se ejecutó el piloto.
