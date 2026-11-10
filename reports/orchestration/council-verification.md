# Verificación vigente — autenticación y deliberación dual recuperadas

**2026-11-10 UTC: Claude y Codex completaron dos deliberaciones reales de solo lectura.** Se verificaron propuestas independientes, contraste recíproco y defensas con preguntas correctamente asignadas. CommandCode permaneció deshabilitado y no se modificaron DaMar Beauty, Ipanema ni producción. [Evidencia estructurada](dual-council-verification.json), sección `authentication_recovery`.

| Caso | ADR | Preguntas / respuestas | Objeciones finales | Decisión |
|---|---|---:|---:|---|
| Auditoría real del orquestador | [ADR-2612277f24bd](../runs/ipanema/20261110T161702-orchestration-da5f9463/council/ADR.md) |5 /5 |11 |`needs_evidence` |
| Fixture sintético, perfiles equilibrados | [ADR-316e5b302ad2](../runs/ipanema/20261110T161944-orchestration-35e5e13b/council/ADR.md) |3 /3 |7 |`needs_evidence` |

Ambos ADR tienen `coverage.deliberation_complete=true` y `defense_complete=true`, además de referencias exactas para todas las respuestas. **Deliberación completa no significa aprobación de cambios**: las restricciones técnicas siguen requiriendo pruebas concretas. El estado `blocked` del engine impide iniciar implementación con estos ADR; no significa que haya vuelto a fallar la autenticación. Los participantes mantienen diferencias de criterio, sin votación ni consenso fabricado.

## Qué ocurrió y qué se corrigió

Claude respondió mediante su CLI nativa dentro del mismo aislamiento, sin login, refresh ni lectura de secretos por el controlador. Se usaron los perfiles existentes equilibrados: `claude-sonnet-5-5` y `gpt-6.1-sol`, esfuerzo `medium`. El caso sintético usa L2 declarado de forma conservadora para estabilizar el protocolo después de los errores semánticos observados con el modelo rápido; no se escaló por autenticación.

En el caso real, Claude retiró sus propuestas de cambiar el clasificador y unificar todos los mapas de proveedores después de las objeciones de Codex. Codex distinguió mapas técnicos de capacidades de la autoridad de participación y recordó que una auditoría de lectura no autoriza añadir tests. Ambos reconocieron que un QA genérico no acredita todos los invariantes específicos. Quedaron propuestas, preguntas, respuestas y objeciones en sus checkpoints originales.

El caso sintético descubrió un fallo adicional: una defensa de Claude respondió sus propias preguntas en lugar de la pregunta de Codex dirigida a Claude. La agregación bloqueó la aprobación, pero los campos de cobertura contaban proveedores sin exigir asignación correcta. Se conservaron la respuesta rechazada y el ADR previo a recuperación; no se presentó como una defensa válida.

Se corrigieron únicamente cuatro archivos locales:

- `tools/ipanema/orchestration/engine.py`: conserva la identidad del participante en el prompt congelado del consejo y limita el schema nativo de defensa a IDs y cantidad de preguntas recibidas.
- `tools/ipanema/orchestration/council.py`: valida el conjunto exacto de pares proveedor/pregunta y excluye una defensa mal asignada de la cobertura completa.
- `tools/ipanema/orchestration/council_runtime.py`: valida asignaciones antes de aceptar o reutilizar defensas; conserva los cinco nodos válidos y recupera solo el inválido.
- `tests/unit/test_council_dual.py`: prueba identidad del prompt, rechazo de cobertura falsa y recuperación de una única defensa conservando propuestas y contrastes.

La recuperación real repitió **solo una defensa de Claude**, en8,536s. Se aplicó un presupuesto explícito y acotado de8 invocaciones totales para ese run, frente al límite inicial6; terminó con7 utilizadas. Los procesos previos estaban recogidos y el snapshot del fixture, objetivo, permisos e instrucciones no cambiaron. La respuesta recuperada contestó la pregunta correcta. No se regeneraron las otras cinco intervenciones ni se sustituyó a Claude por otro proveedor.

## Resultados y límites

Hubo13 invocaciones reales:12 seleccionadas válidas y1 defensa contextual rechazada y reemplazada. No hubo nuevas ausencias, fallos de autenticación ni invocaciones CommandCode. Los esquemas nativos y las comprobaciones semánticas/contextuales se aprobaron para los12 nodos seleccionados. El registro conserva cada modelo, esfuerzo, duración, tamaño de contexto y contadores emitidos.

Tiempo del controlador hasta el primer ADR:151,844s en el caso real y85,325s en el sintético; recuperación adicional8,536s. No incluye el tiempo humano de diagnóstico y documentación, y no se suma con los tiempos solapados de proveedores. Claude reportó **USD1,0168454**, incluyendo la defensa rechazada; Codex no emitió coste monetario utilizable. El coste conjunto permanece **no disponible**.

[QA quick posterior](../runs/ipanema/20261110T162510-quick-77dfa9a3/report.json): **238 unitarias y34 integraciones aprobadas**. [QA orchestration posterior](../runs/ipanema/20261110T162533-orchestration-7028d949/report.json):41 unitarias de orquestación,87 del consejo,11 integraciones de orquestación y5 del consejo; son subconjuntos del QA anterior. Las simulaciones de proveedor siguen identificadas como fixtures; estas pruebas no se confunden con las13 invocaciones reales.

Los hashes inicial/final de397 archivos de Ipanema y471 de DaMar coinciden. Ambos patches de los casos de lectura están vacíos. No se consultó ninguna tienda, cuenta Google ni MCP durante la recuperación; no hubo push, watch, publish, instalación ni operaciones comerciales.

La auditoría real corresponde al snapshot anterior al ajuste puntual de contexto en `engine.py`; esa diferencia queda registrada. No se utiliza su propuesta para afirmar que toda la fuente posterior recibió una revisión independiente nueva. El QA posterior y la defensa sintética real prueban la corrección acotada, pero no certifican futuros proyectos ni autorizan implementación de las recomendaciones pendientes. Las pruebas de storefront, SEO/performance e indexación siguen fuera de este alcance.

La autenticación dejó de ser el bloqueo observado. El siguiente paso para una tarea concreta es resolver sus evidencias y condiciones del ADR, dentro de sus permisos. No se reabre aquí la investigación ni se modifica DaMar.

---

# Historial: configuración dual antes de recuperar autenticación

**Estado histórico al configurar el modo dual: aceptación real parcial y bloqueada.** El modo actual solo permite Claude y Codex. CommandCode no se ejecutó en este encargo y conserva su adaptador, modelos e historial. No se modificaron temas ni producción. [Evidencia estructurada actual](dual-council-verification.json) · [manual](council.md).

## Cambios integrados

La participación se valida desde `tools/ipanema/orchestration/models.json:council`, sin un segundo registro. Planner, engine, adaptadores, aislamiento, Supervisor y grants activos MCP rechazan proveedores deshabilitados. Los overrides locales no pueden habilitarlos. Se conserva el motor de worktrees, permisos, hashes, contratos, QA, SEO y recuperación; no se instalaron dependencias ni se conectaron cuentas.

Ambos proveedores tienen autoridad técnica igual. Las propuestas iniciales comparten evidencia factual y snapshot, sin opiniones ajenas. El contraste incluye preguntas identificadas al otro participante y la defensa responde sus IDs con referencias, cambios de postura o solicitud de evidencia. El ADR conserva propuestas, preguntas, respuestas, objeciones y criterios; las restricciones no se compensan con votos. El recorrido por defecto tiene propuestas y hasta dos intercambios de deliberación (contraste y defensa), seis workers antes de reintentos e implementación.

Codex implementa y Claude revisa por defecto; `--implementer claude` invierte los roles. En L2–L4 el controlador exige un revisor de proveedor diferente incluso ante un plan manipulado o failover. L4 dual tiene un revisor independiente y QA objetivo reforzado; no se inventan dos revisores distintos con un único proveedor. Si falta un participante obligatorio, la aprobación se bloquea. CommandCode no puede sustituirlo.

## Ejecuciones reales actuales

| Caso | Claude | Codex | Decisión |
|---|---|---|---|
| Fixture sintético, lectura | Haiku 5.5, low: fallo `authentication`, 5,056s | GPT-6 Luna, low: dos respuestas rechazadas por ID de alternativa inválido, 28,803s y 26,147s | `needs_evidence`, sin contraste ni defensa |
| Auditoría real de política, planner, failover, engine, aislamiento y permisos | Opus 5.5, high: fallo `authentication`, 4,181s | GPT-6.1 Sol, high: propuesta independiente válida, 81,623s | `needs_evidence`, participante original ausente |

[ADR sintético](../runs/ipanema/20261110T155918-orchestration-798cb495/council/ADR.md) · [ADR de auditoría real](../runs/ipanema/20261110T160024-orchestration-8579c16d/council/ADR.md) · [propuesta real de Codex](../runs/ipanema/20261110T160024-orchestration-8579c16d/council/council-proposal-codex.json).

Se completaron cinco invocaciones iniciales reales, incluido un reintento acotado de contrato. Los dos controladores duraron 64,453s y 88,077s; los tiempos de proveedor se solapan y no deben sumarse como latencia total. No hubo timeout, límite de salida ni contexto incompleto en esos nodos. Todos confirmaron salida del proceso. Claude produjo la categoría de autenticación; no hay evidencia suficiente para distinguir credencial ausente/expirada de permisos de cuenta o modelo. No se inspeccionaron secretos ni se inició login, refresh u OAuth.

Dos comprobaciones reales adicionales de contrato, solo Codex rápido y sin atribuirlas a Claude, duraron 25,542s y 32,862s. La primera fue rechazada por no declarar pruebas; la segunda por recomendar un ID que no figuraba en sus alternativas. Los schemas ahora exigen patrón de ID, textos y pruebas no vacíos. La coherencia entre campos sigue verificándose localmente; no se repara una recomendación inválida. **El último intento rápido siguió fallando semánticamente**: no acredita una deliberación completa ni la fiabilidad de ese perfil. Sus resultados y límites están en el JSON actual. No se hicieron reintentos indefinidos ni escalado automático de modelo.

El coste monetario total es **no disponible**. Claude reportó coste cero y cero tokens para sus fallos; Codex emitió contadores pero no coste utilizable. Se conservan por invocación, sin estimaciones inventadas. Los modelos provienen del registro existente; no se cambiaron identificadores por estos fallos.

## Hallazgo real corregido

Codex detectó que un plan recibido de nivel L2, con sus revisores eliminados, podía omitir las comprobaciones inicial y final de independencia. Se confirmó la condición en el engine y se hizo obligatoria desde L2. La regresión `test_l2_cannot_omit_reviewer_from_received_plan` demuestra rechazo antes de QA o inferencia. Los fixtures de concurrencia se actualizaron para incluir revisión independiente, conservando la prueba de dos worktrees reales y archivos disjuntos. No se debilitó el gate para hacer pasar las pruebas.

La auditoría real corresponde al snapshot anterior a esa corrección. Su propuesta no se presenta como aprobación de la fuente posterior; falta revisión real del otro proveedor.

## QA final y aceptación

[QA quick](../runs/ipanema/20261110T160732-quick-ebd455b4/report.json): **237 unitarias y34 integraciones aprobadas**, además de repositorio y evaluaciones deterministas/SEO. [QA orchestration](../runs/ipanema/20261110T160757-orchestration-78fb71c4/report.json):41 unitarias de orquestación,86 de consejo,11 integraciones de orquestación y5 de consejo aprobadas; son subconjuntos, no pruebas adicionales que deban sumarse al total anterior. Las dos skills ajustadas pasaron `quick_validate`. `git diff --check` pasó.

| Criterio | Evidencia actual |
|---|---|
| Dos propuestas, preguntas y defensas; ADR con resolución | Pipeline offline con fixtures explícitos aprobado; recorrido real incompleto |
| Desacuerdo sin voto por proveedor; objeción crítica | Pruebas de matriz y recibos aprobadas; una opinión no resuelve objeciones |
| Agente ausente, failover sin CommandCode | Fixtures aprobados y ambos casos reales bloqueados por ausencia de Claude |
| Independencia y rechazo de autoaprobación | Pruebas L2–L4, inversión de roles, revisión tras failover y plan sin revisor aprobadas |
| Contratos inválidos y evidencia insuficiente | Pruebas aprobadas y respuestas reales rechazadas sin reparación ambigua |
| Dos originales reales y contraste recíproco | **Pendiente: autenticación de Claude y contratos válidos de ambos** |
| Ningún cambio en DaMar ni Ipanema | Hashes inicial/final coincidentes en471 y397 archivos no ocultos; detalle en JSON |
| Ninguna producción/MCP/Google | Cero operaciones remotas de tienda, nuevas conexiones o invocaciones CommandCode |

Los tests de proveedores son fixtures identificados; Git, worktrees y validaciones del controlador son reales. No se ejecutó render Twig, QA visual de tienda, medición de SEO/velocidad ni Search Console: esta tarea configura el orquestador. No se registra la funcionalidad dual como solución verificada de extremo a extremo.

## Uso y siguiente comprobación

```bash
python3 tools/ia.py orchestrate doctor
python3 tools/ia.py orchestrate task \
  "Auditar participantes, failover y revisión independiente; solo lectura" \
  --scope workspace --read-only --council full \
  --file tools/ipanema/orchestration/models.json \
  --file tools/ipanema/orchestration/recovery.py \
  --file tools/ipanema/orchestration/engine.py
```

El comando prepara el plan sin inferencia. Tras recuperar la autenticación de Claude mediante el mecanismo oficial fuera de los workers aislados, usar `orchestrate run /ruta/al/plan.json --execute` para repetir una auditoría autorizada. El éxito exige propuestas válidas de ambos originales, preguntas y respuestas recíprocas y evidencia del ADR. Un `needs_evidence` por falta de pruebas objetivas puede ser una deliberación completa; una ausencia de proveedor, como en estas ejecuciones, no lo es.

Se conserva a continuación el informe histórico de tres participantes. Sus seis nodos,19 objeciones y ADR previos **no son resultados del modo dual** ni autorización para cambiar DaMar.

---

# Histórico: verificación del consejo de tres participantes — 2026-11-10 UTC

**Estado histórico: deliberación real de tres participantes completada.** Claude, Codex y CommandCode produjeron tres propuestas independientes válidas y tres contrastes válidos sobre paginación de Ipanema. Se registraron19 objeciones y un ADR verificable. La decisión es diferir la implementación hasta comprobar los contratos pendientes; no hay consenso unánime ni aprobación de cambios en el tema. No se modificó DaMar, ningún archivo del tema ni producción.

## Estabilización: evidencia real del recorrido completo

[Resumen estructurado y hashes](council-stabilization.json) · [ADR completo](../runs/ipanema/20261110T010139-orchestration-b62831d6/council/ADR.md) · [Verificaciones de fuente](../runs/ipanema/20261110T010139-orchestration-b62831d6/council/source-verifications.json).

Tarea: «Auditar el componente compartido de paginación de Ipanema y determinar la mejor estrategia SEO, accesible y compatible con el diseño actual». Proyecto `ipanema` (RHINO), riesgo L3, solo lectura. No se repitió el discovery. Se usaron el snapshot, el engine y los adaptadores existentes.

| Fase | Proveedor/modelo | Esfuerzo | Tiempo CLI | Contexto UTF-8 | Contrato |
|---|---|---|---:|---:|---|
| Propuesta independiente |Claude / claude-sonnet-5-5 |medium |39,416s |45.397B |Aprobado nativo y local |
| Propuesta independiente |Codex / gpt-6.1-sol |medium |51,787s |45.393B |Aprobado nativo y local |
| Propuesta independiente recuperada |CommandCode / deepseek/deepseek-v4.1-flash |No configurado |59,242s |45.409B |Aprobado local |
| Contraste |Claude / claude-sonnet-5-5 |medium |22,099s |78.052B |Aprobado nativo y local |
| Contraste |Codex / gpt-6.1-sol |medium |24,911s |78.048B |Aprobado nativo y local |
| Contraste |CommandCode / deepseek/deepseek-v4.1-flash |No configurado |31,811s |78.064B |Aprobado local |

Los tres paquetes iniciales comparten el mismo binding de snapshot, reglas y fuentes; no contienen `peer_proposals`. Los roles difieren. Los paquetes de contraste contienen las tres propuestas completas, solo después de validarlas todas. Las pruebas corresponden a invocaciones reales, no fixtures. Se preservaron las dos primeras propuestas durante la recuperación.

Resultado:6 nodos reales válidos en2 rondas,7 intentos de worker de un máximo8 (uno falló por salida),19 objeciones,4 comprobaciones de fuente y1 objeción corregida con evidencia del controlador. Ningún proveedor sustituyó a otro. Se verificaron397 archivos del tema: el hash del árbol completo anterior y posterior coincide. Se conserva el registro `acceptance.json` del run.

### Causas identificadas y correcciones

| Problema | Evidencia y causa comprobable | Corrección |
|---|---|---|
| Contratos históricos inválidos de Codex |Proceso terminó con código0; el validador rechazó la propuesta. No se conservaron los campos rechazados, por lo que no se puede afirmar qué campo falló ni si hubo truncamiento en aquellos intentos. |Schema estructurado nativo, validación local estricta y diagnóstico por ruta/categoría. No se reconstruyen respuestas antiguas. |
| Falta de salida estructurada nativa |Los adaptadores no pasaban `--output-schema`/`--json-schema`, disponibles en las CLI instaladas. |Codex usa archivo de schema en el snapshot RO; Claude usa schema nativo y stream JSON. CommandCode usa su NDJSON soportado y el mismo schema local, sin inventar soporte nativo. |
| Contexto duplicado |En un mismo task sintético histórico, representación anterior42.094B frente a16.159B con el packet compacto actual, sin hacer otra inferencia. |Eliminar repetición de task/context/contrato y discovery no pertinente. Mantener reglas, skills seleccionadas, fuentes, permisos, evidencia y criterios. |
| CommandCode interrumpido por salida, no timeout |En este run emitió2.899 eventos antes de alcanzar2MB. Ya había entregado primera salida a1,595s; proceso recogido después de53,499s. |Consumir NDJSON línea a línea; descartar snapshots de progreso, conservar resultado/errores/señales de herramientas, contadores y límites separados de transporte y respuesta. |
| Normalizador perdía `evidence` |Dos respuestas habían pasado schema nativo/local, pero el objeto persistido eliminaba el campo raíz y el replay lo rechazaba como ausente. |Preservar el campo. Para los dos checkpoints afectados se acepta explícitamente el formato canónico antiguo solo cuando consta la validación anterior; no se inventa el valor omitido. Se conservan `analysis.evidence_refs` y una nota de migración. |
| Timeouts históricos sin fase |Solo permitían saber timeout/inactividad; no demostraban autenticación fallida ni tiempo exacto en inferencia. |Registrar spawn, entrega del contexto, primera salida, tipos de eventos, duración máxima, inactividad posterior y validación del contrato. No atribuir fases internas que el proveedor no expone. |

En la recuperación, CommandCode procesó2.799.092B y retuvo10.949B; en el contraste procesó6.797.565B y retuvo5.976B. El límite útil sigue en2MB y el de transporte en20MB; no se elevó la salida final ni se aceptó JSON truncado. Se conservaron señales de herramientas y errores. No se almacenaron eventos de razonamiento ni salida privada cruda.

[Schema de propuesta usado](../runs/ipanema/20261110T010139-orchestration-b62831d6/council/proposal.schema.json) · [Schema de contraste usado](../runs/ipanema/20261110T010139-orchestration-b62831d6/council/objection.schema.json). Todos los campos del rol son obligatorios, sin propiedades extra. Máximo3 alternativas,8 objeciones y textos de hasta1.000 caracteres por campo; `changes=[]`. No se reparan comas, campos, fences ni valores ambiguos. Se distinguen sintaxis, duplicación de claves, tipo/schema, campo ausente, incompletitud/max-turns, límite de salida, error de proveedor y ausencia de respuesta final.

### Decisión técnica y desacuerdos

**ADR-7a95be882add: `needs_evidence`; implementación no autorizada.** La deliberación está completa y el desacuerdo sobre alternativas está registrado: Claude y CommandCode prefieren la alternativa mínima de Claude; Codex prefiere su alternativa progresiva. No se eligió por dos votos contra uno.

La conclusión de auditoría es conservar por ahora `infinite` y `LS.hybridScroll`, y comprobar una mejora progresiva del componente compartido que reutilice `next_link/prev_link`, tenga nombres traducibles y permita continuar desde páginas intermedias. `openai-progresiva-nativa` queda como candidato para validación, **no como implementación aprobada**: aborda la continuidad que un `href` añadido solo al control de página1 no cubre. Cambiar automáticamente a `classic` altera la experiencia configurada y el lote de12 a60 productos, sin mejora de rendimiento demostrada.

La fuente confirma que categoría y búsqueda están configuradas como `infinite`; el default `classic` del schema no es su configuración efectiva. La condición `pages.current ==1` limita el control infinite. También se resolvió una afirmación demasiado amplia: el ancla sí contiene texto traducible y `translations/es.json` proporciona «Mostrar más productos». Eso no certifica nombre accesible calculado, foco ni activación por teclado.

Siguen abiertas las objeciones sobre interceptación del clic por `LS.hybridScroll`, actualización de href tras cargas sucesivas, render de páginas2+, diseño responsive y pruebas reales de teclado/red. No se presentó una comprobación estática como solución de esos riesgos. La implementación del helper de plataforma no está demostrada por la llamada local, y no se ejecutaron operaciones remotas para obtenerla.

### Tiempo, coste y QA de estabilización

Tiempo activo de los dos tramos del controlador:148,352s. Tiempo transcurrido desde el inicio hasta finalizar la recuperación:472,512s, incluyendo el diagnóstico y la corrección del controlador. No confundir ambos tiempos con latencia pura de inferencia.

Claude reportó USD0,3372327 en sus dos nodos válidos. Codex y CommandCode reportaron tokens, pero no coste monetario total utilizable; el coste global es **no disponible**, incluido el intento CommandCode interrumpido. El JSON de evidencia conserva los contadores exactos, incluyendo caché, sin sumarlos con convenciones incompatibles.

QA posterior aprobado:218 pruebas unitarias y34 integraciones;72 pruebas específicas del consejo (67 unitarias+5 integraciones). Incluye salida nativa, schemas, sintaxis, campos ausentes, normalización de evidencia, eliminación de progreso sin ocultar herramientas, watchdog por fases, recuperación sin repetir nodos válidos y rechazo de binding cambiado.

[QA quick](../runs/ipanema/20261110T011540-quick-78c4f3c2/report.json) · [QA orquestación](../runs/ipanema/20261110T011526-orchestration-46ae1ed0/report.json).

La estabilización demuestra el protocolo completo sobre esta tarea y estos modelos. No certifica futuras respuestas, otros modelos/cuentas, indexación de Google, accesibilidad WCAG, render Twig ni rendimiento de la tienda. No hubo aprobación de una implementación ni cambios en temas.

## Historial de la primera implementación

Las siguientes pruebas y limitaciones describen el estado anterior a esta estabilización; no se borran ni se presentan como resultados actuales.

## Evolución e integración

Antes, el planner distribuía arquitectura, implementación y revisión de forma secuencial. Existían adaptadores, Supervisor, aislamiento Bubblewrap, snapshots/worktrees, QA central, transacciones y motores SEO/MCP. No existía una deliberación colectiva previa verificable.

Ahora el mismo engine ejecuta propuestas independientes de Claude/Codex/CommandCode, contraste acotado y un ADR. Conserva los adaptadores y failover existentes; no instala runtimes ni conecta cuentas. El ADR controla alcance, fuentes, instrucciones, restricciones y evidencias. No usa promedio para compensar fallos obligatorios. Objeciones críticas requieren resolución verificable. Una identidad de alternativa ambigua, participante ausente o prueba insuficiente impide implementar.

La implementación local posterior sigue usando el DAG, QA y revisores existentes. Un ADR aprobado no permite eludir QA con un diff vacío, reutilizar pruebas anteriores a un cambio, ampliar archivos o autorizar producción. El estado final revisable conserva explícitamente las pruebas pendientes.

Fuentes principales: [manual y arquitectura](council.md), `tools/ipanema/orchestration/{council,council_runtime,planner,engine,cli}.py`. Se amplió `tools/ipanema/qa.py`; se corrigió la capitalización del modelo fuerte CommandCode en `models.json`. Se actualizaron las entradas de AGENTS/README, sin duplicar discovery ni herramientas SEO.

## Pruebas reproducibles

| Ejecución final | Resultado | Alcance |
|---|---|---|
| `python3 tools/ia.py qa --suite orchestration` | Aprobada: 41 unitarias previas +52 consejo, 11 integraciones previas +5 consejo | Proveedores simulados explícitos; control, Git y validaciones reales |
| `python3 tools/ia.py qa --suite quick` | Aprobada: 203 unitarias y34 integraciones; repositorio, evaluaciones del coordinador y SEO aprobados | No acredita Google, tienda renderizada ni decisiones de modelos reales |
| Suite específica del consejo |57 pruebas aprobadas | Independencia, consenso/desacuerdo, ausencias, objeciones críticas, bindings, permisos, presupuesto, recibos y QA |
| Revisión independiente de código |APPROVE | Revisor local separado, sin representar una ejecución de CommandCode |
| `git diff --check` | Aprobado después de corregir espacio final del README | Formato del diff |

Comando específico:

```bash
python3 -m unittest tests.unit.test_council_policy tests.unit.test_council_engine tests.unit.test_council_receipts tests.integration.test_council_cli -q
```

La prueba sintética del pipeline usa `aggregate` real y recibos ligados a la identidad exacta de la alternativa. Un no-op que no satisface la condición posterior es rechazado; un parche correcto pasa el QA de su alcance y revisión. Los proveedores/QA general son fixtures declarados: no son llamadas reales ni pruebas del rendimiento de una tienda.

Reportes finales locales:

- [Orquestación](../runs/ipanema/20261110T004510-orchestration-8f04eac9/report.json).
- [Quick](../runs/ipanema/20261110T004523-quick-7e84371a/report.json).

## Demostraciones con CLIs reales

Se usaron los ejecutores originales con snapshots y Bubblewrap; no se simularon respuestas ni autenticación. Cada CLI recibió únicamente su contexto y acceso nativo de proveedor previsto por el aislamiento. No hubo accesos a cuentas Google ni a tiendas remotas. Los ajustes de timeout/reintentos fueron locales al proceso de comprobación: no se alteró `.local/orchestration.json`.

### Tarea sintética — colaboración total L1

Fixture: `tests/fixtures/council/read-only.txt`. Primera ronda independiente, máximo2 workers concurrentes, timeout60s, inactividad45s, cero reintentos y sin sustituciones para observar identidades originales.

| Participante | Modelo/esfuerzo | Observación real |
|---|---|---|
| Claude |claude-haiku-5-5 / low |Contrato de propuesta válido, 14,631s |
| Codex |gpt-6-luna / low |Proceso terminó en18,992s; respuesta no cumplió contrato de propuesta |
| CommandCode |deepseek/deepseek-v4.1-flash / sin esfuerzo configurado |Cancelado tras45,102s de inactividad; proceso terminado y recogido |

Resultado: `needs_evidence`,3 intentos del presupuesto6, sin contraste ni implementación. El sistema no fabricó consenso a partir de una propuesta. [ADR y cobertura](../runs/ipanema/20261110T004157-orchestration-8b64d865/council/adr.json).

La prueba detectó una ambigüedad del prompt: el contrato base enumeraba cuatro campos mientras el consejo añadía `analysis`. Se hizo explícita la obligación de entregar el contrato completo y se separó `invalid_council_contract` de fallos CLI/autenticación. Nueva prueba automatizada incluida.

**Revalidación individual real de Codex:** gpt-6-luna/low devolvió contrato válido en16,268s después del ajuste; su decisión fue `blocked`, compatible con límites de evidencia. Esto demuestra cumplimiento del contrato individual, no una decisión colectiva aprobada. [Evidencia](../runs/ipanema/20261110T004440-council-contract-check-80ccfe6e/contract.json).

### Tarea real de solo lectura — DaMar Beauty L3

Archivos actuales: `snippets/product-list/pagination.tpl` y `sections/main-products-grid.tpl`. Objetivo: dependencias y enlaces HTML de la paginación compartida, sin modificar archivos ni consultar la tienda remota.

| Participante | Modelo/esfuerzo | Observación real |
|---|---|---|
| Claude |claude-opus-5-5 / high |Inactividad45,666s; proceso recogido |
| Codex |gpt-6.1-sol / high |Inactividad45,946s; proceso recogido |
| CommandCode |moonshotai/Kimi-K3.1-Pro / sin esfuerzo configurado |Inactividad47,189s; proceso recogido |

El contexto completo fue entregado a los tres procesos. Estos límites diagnósticos **no prueban** autenticación fallida, modelo inexistente, congelamiento ni ausencia permanente: no existe evidencia para atribuir la demora a una causa precisa. El default del ejecutor sigue siendo timeout180s e inactividad desactivada, configurable; este ensayo impuso un límite más corto y no representa el máximo de respuesta de cada modelo.

Resultado: `needs_evidence`,3 intentos, sin segunda ronda ni implementación. El QA de línea base de fuente pasó; no equivale a render Twig, SEO, visual o rendimiento. Los dos hashes originales siguen coincidiendo. [Run](../runs/damarbeauty/20261110T004308-orchestration-6c893c1d/run.json), [ADR](../runs/damarbeauty/20261110T004308-orchestration-6c893c1d/council/adr.json).

El CSS `static/css/damar.css` ya mostraba modificaciones externas durante la verificación. No se editó ni se revirtió: se preservaron los cambios ajenos. Esta tarea no rehízo las correcciones anteriores de DaMar.

### Revalidación final sin corte por inactividad

Se repitieron ambos escenarios con máximo3 participantes concurrentes, timeout120s, inactividad desactivada, cero reintentos y sin sustituciones. No se escaló ningún modelo.

- **Fixture L1:** Claude y CommandCode entregaron propuestas válidas (12,887s y34,582s). Codex terminó en21,318s, pero incumplió el contrato. El ajuste del prompt mejoró una prueba individual y no garantiza cumplimiento constante. El ADR registra `invalid_council_contract`, no fallo de autenticación. [ADR final sintético](../runs/ipanema/20261110T004740-orchestration-9d0c8b50/council/adr.json).
- **DaMar L3:** Claude y CommandCode alcanzaron timeout120s (120,070s y120,110s); Codex terminó en75,962s, pero su propuesta no cumplió el contrato. Todos los procesos quedaron recogidos. [ADR final real](../runs/damarbeauty/20261110T004825-orchestration-1aea849c/council/adr.json).
- Ambos ADR quedaron `needs_evidence`, con3 intentos cada uno y sin segunda ronda ni implementación. Los hashes de las fuentes originales siguen coincidiendo. La causa de las demoras y los defectos concretos de los contratos rechazados no está determinada por la evidencia conservada; no se guardó salida privada cruda.

Una comprobación individual adicional de **CommandCode** con deepseek/deepseek-v4.1-flash devolvió un contrato válido en30,306s, sin corte por inactividad y timeout90s. [Evidencia](../runs/ipanema/20261110T004556-council-contract-check-69c207b2/contract.json). Los tres proveedores han entregado individualmente propuestas válidas en alguna comprobación; esto no demuestra una deliberación conjunta completa.

La [evidencia resumida versionada](council-verification.json) conserva modelos, resultados observados, tiempos, bindings de fuente y hashes de la implementación, sin credenciales ni salida privada. Los artefactos completos bajo `reports/runs/` permanecen locales e ignorados por Git.

Para reproducir el escenario sintético con los comandos existentes:

```bash
python3 tools/ia.py orchestrate task \
  "Inspecciona únicamente el fixture sintético sin modificar archivos ni inventar pruebas" \
  --scope workspace --read-only --council full \
  --file tests/fixtures/council/read-only.txt --execute
```

Este comando consume inferencia real. Las comprobaciones anteriores ajustaron los límites únicamente en memoria; para otros ensayos se puede usar `.local/orchestration.json`, preservando su contenido existente. No reutilizar un ADR de otro run como autorización.

## Límites y pendientes

1. Falta una deliberación real completa de tres proveedores y un contraste real aprobado. La recuperación conserva identidades y gates, pero no subsana por sí sola una respuesta ausente.
2. Las pruebas de consenso/desacuerdo y rechazo de implementación son reproducibles offline; no acreditan que los modelos siempre tomen buenas decisiones.
3. Un hash, una afirmación del modelo o una prueba de presencia de texto no demuestran corrección funcional, SEO, accesibilidad o velocidad. Sin comprobaciones apropiadas del controlador, el ADR permanece pendiente: el consejo no inventa verificaciones para obtener aprobación automática.
4. Los checks de cada objetivo deben prepararse con fuentes y QA pertinentes. Se aceptan predicados acotados/reportes QA existentes, no shell generado por modelos. La equivalencia entre alternativas con distinta descripción no se presupone.
5. Falta demostrar revisión cruzada y QA de una implementación real bajo un ADR real aprobado. No existe aprobación de despliegue.
6. Las llamadas reales permiten observar algunos contadores de proveedor. Claude reportó USD0,00540959 en el ensayo sintético; no se extrapola coste total ni se inventa el de procesos sin métricas. Los reintentos y sustituciones comparten presupuesto de intentos, no un límite monetario garantizado.
7. El aislamiento existente requiere Linux/Bubblewrap para ejecutar workers. La red de inferencia no dispone de firewall de destinos API; esa limitación preexistente sigue explícita. No se amplían permisos para solventarla.

## Uso cotidiano

```bash
python3 tools/ia.py orchestrate doctor
python3 tools/ia.py --project damarbeauty orchestrate task \
  "Auditar el componente compartido de paginación" --read-only \
  --file snippets/product-list/pagination.tpl --file sections/main-products-grid.tpl
```

El comando anterior guarda un plan sin consumir modelos. Inspecciona el alcance y añade comprobaciones relevantes según [el manual](council.md); `orchestrate run /ruta/al/plan.json --execute` inicia el flujo autorizado. Para L3/L4 el consejo es obligatorio. `--council full` solicita las tres propuestas también en tareas pequeñas. Una salida `needs_evidence` es un bloqueo de implementación, no una aprobación.

Registrar una tienda reutiliza la configuración existente:

```bash
python3 tools/ia.py projects register nueva-tienda --name "Nueva tienda" \
  --theme-root /ruta/real/al/tema --url https://dominio-autorizado.example \
  --environment development
python3 tools/ia.py projects use nueva-tienda
python3 tools/ia.py doctor
```

Sustituye ruta/dominio por los reales. La ruta personal se guarda mediante el mecanismo local existente. Registrar no clona, conecta ni publica una tienda.
