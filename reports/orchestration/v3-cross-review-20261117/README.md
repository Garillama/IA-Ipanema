# IA-Ipanema V3 — candidato de revisión cruzada de código

Fecha: **2026-11-17**. Estado global: **`needs_evidence`**. Código preparado y probado en una copia privada de herramientas; **no integrado, no activado como obligatorio y sin cambios en clientes**.

## Resultado y límites

Se preparó una extensión aditiva del consejo, no otro orquestador. El candidato valida independencia, identidad del diff/contexto, revisión de cinco dimensiones, objeciones localizadas, resolución respaldada y QA. **31 pruebas nuevas y128 existentes aprobadas** sobre el candidato aislado.

No se afirma que tres agentes hayan aprobado este código ni que se haya demostrado detección semántica mediante modelos reales. Los revisores de las unitarias son fixtures sintéticas identificadas. Las pruebas demuestran comportamiento del protocolo/gate; la calidad de detección real sigue pendiente.

[Diff completo](candidate.patch) · [Manifiesto y hashes](candidate-manifest.json) · [Schema de respuesta](review-response.schema.json) · [ADR](ADR.md) · [Recibo del controlador](controller-results.json).

## 1. Investigación y diseño de integración

Se inspeccionaron `council.py`, `council_runtime.py`, `adapters.py`, `engine.py`, la política de `models.json`, el discovery V3 y las suites existentes. La búsqueda acotada de duplicidad encontró detección de documentos/entidades/títulos en el motor SEO, pero no un detector contextual de código aplicable a este flujo. No se reutilizan esos detectores SEO: sus responsabilidades y contratos son distintos.

Sí se reutiliza:

- `adapters.validate_schema`: validación estructural cerrada, sin biblioteca nueva.
- `council._ledger` y `_proven`: recibos separados de las respuestas de modelos y ligados al contexto.
- `planner.safe_path`, `core.beneath` y `digest`: rutas, confinamiento e integridad de fuentes.
- El patrón existente de ADR/fingerprint y QA del controlador; no se sustituye el consejo previo.

**Ubicación elegida:** `tools/ipanema/orchestration/code_review.py` contiene contrato y evaluación sin inferencia ni efectos externos. El punto de entrada aditivo `council.review_code_candidate(...)` enlaza con el consejo existente mediante import diferido. No se coloca en SEO, storefront, una skill o el adaptador del proveedor: las reglas de aprobación pertenecen al controlador, no al texto de un modelo.

La nueva identidad canónica no reutiliza literalmente `alternative_fingerprint`: aquel helper solo firma descripción/archivos/tests de una alternativa; aquí deben quedar ligados autores, diff, objetivo, permisos, fuentes, preflight y QA. Compartir una abstracción nueva solo por unas líneas de hashlib/JSON habría aumentado alcance y consumidores. Los recibos y el validador existentes sí se reutilizan directamente.

Alternativas consideradas: instrucciones en prompts únicamente (insuficientes para impedir autoaprobación), reescritura del motor (rechazada), habilitar Antigravity directamente en `models.json` (rechazada sin validar adaptador), o cambiar los estados/contratos duales existentes (riesgo innecesario). Se eligió un gate explícito opcional y reversible, pendiente de revisión e integración posterior.

## 2. Cambios mínimos preparados

| Archivo candidato | Operación | Responsabilidad |
|---|---|---|
| `tools/ipanema/orchestration/council.py` | Modificación aditiva | Wrapper público opcional; agregado V2 intacto |
| `tools/ipanema/orchestration/code_review.py` | Alta | Paquete independiente, schema, integridad y decisión de revisión |
| `tests/unit/test_code_review_v3.py` | Alta |31 pruebas controladas, incluyendo los diez escenarios solicitados |

No se alteran `models.json`, políticas, permisos, planificación activa, recuperación, auth, adaptadores, MCP ni proyectos externos. Antigravity y sus subagentes no se invocan. El candidato está en la ruta privada del manifiesto; los archivos operativos nuevos **todavía no existen** en el repositorio activo.

Parche SHA256:

`69c75ac77596439227c4066439711334e8c7bf2724b5a28fbbfabdf2336e0dbb`

El manifiesto conserva preimagen/postimagen por archivo y un respaldo privado del `council.py` original. No hay eliminaciones ni dependencias nuevas.

## 3. Protocolo de revisión propuesto y preparado

1. El controlador fija autor, contribuyentes efectivos, objetivo, riesgo, permisos, diff y scope de fuentes con hashes. Conserva evidencia de búsqueda de reutilización y justificación de módulo; para riesgo medio/alto exige además plan previo.
2. `independent_packet` comprueba hashes de diff/fuentes/permisos. Entrega objetivo, código/contexto, diff, tests y permisos. Omite explicaciones conclusivas del autor y revisiones ajenas; usa copias de los datos para evitar mutaciones compartidas accidentales.
3. Los otros dos proveedores originales reciben el paquete por separado. Cada respuesta debe evaluar architecture, duplication, performance, regression y maintainability, y citar evidencia. No basta una explicación del implementador.
4. La identidad solicitada/efectiva y el recibo del transporte los aporta el controlador. La respuesta no puede declarar su identidad ni insertar recibos propios. Se comprueba el hash del cuerpo recibido y la fase independiente.
5. El autor responde; cualquier cierre requiere además confirmación del revisor originario y un recibo de resolución del controlador ligado al candidato exacto.
6. Una corrección cambia la identidad: invalida ambas revisiones, QA y preflight anteriores. No se traslada una aprobación al diff nuevo.
7. El gate devuelve uno de los cuatro estados. Nunca ejecuta integración o publicación, ni siquiera cuando devuelve `approved_for_authorization`.

Matriz obligatoria del candidato:

| Autor | Revisores independientes |
|---|---|
| Codex | Claude y Antigravity |
| Claude | Codex y Antigravity |
| Antigravity | Claude y Codex |

Si un segundo proveedor contribuyó código, también cuenta como autor. Con solo tres proveedores no quedan dos revisores no autores: el gate bloquea, sin reinterpretar un coautor como revisor independiente. Hace falta preservar un único autor o replanificar explícitamente; no fabricar firmas.

**Frontera de confianza:** `candidate`, assignments/envelopes y `evidence` son datos del controlador, no del modelo. `_ledger` valida estructura/contexto, no autentica una cuenta ni verifica por sí mismo todos los artefactos externos. La futura conexión al motor debe obtener esos recibos de su almacén validado, comprobar archivos/resultados y no mezclar JSON propuesto por workers. Un llamador malicioso con capacidad de inventar todo el ledger está fuera de esta frontera; no se promete una firma criptográfica de proveedores.

## 4. Esquema de objeciones

La respuesta cerrada está en `review-response.schema.json`. Cada objeción incluye:

- `id`, único dentro del revisor; clave central `proveedor:id` para evitar colisiones.
- `severity`: BLOCKER, HIGH, MEDIUM, LOW o INFO.
- `challenge`: architecture, duplication, performance, regression o maintainability.
- `sites`: archivo, función y rango de líneas, comprobados contra fuentes del contexto.
- `evidence_refs`, `claim`, `impact`, `recommendation`, `resolution_condition`.
- `duplication_kind`: exact, semantic, legitimate o not_applicable.

Una objeción de duplicidad requiere **dos ubicaciones concretas distintas**, no una similitud genérica. El gate verifica ámbito, rangos y presencia del nombre de función en el rango; **no demuestra automáticamente equivalencia semántica ni que la función citada tenga ese comportamiento**. Esa conclusión exige revisión contextual y pruebas apropiadas.

No se aceptan campos de estado `resolved` enviados por el autor para cerrar una objeción. Las respuestas del autor permiten aceptar/corregir, refutar, proponer alternativa o pedir evidencia; no son recibos de cierre.

## 5. Reglas de resolución y decisión

| Situación | Resultado del gate |
|---|---|
| Autor revisando su código, identidad sustituida/duplicada o BLOCKER abierto | `blocked` |
| HIGH abierto, QA ejecutado que falla o revisión que pide cambios | `changes_requested` |
| Revisor/QA/preflight ausente, hashes obsoletos, evidencia insuficiente o MEDIUM sin respuesta | `needs_evidence` |
| Ambos revisores válidos, evidencias esenciales vigentes y sin HIGH/BLOCKER abiertos | `approved_for_authorization` |

LOW/INFO no bloquean por estilo. Un MEDIUM respondido puede permanecer abierto si no incumple un gate fundamental: se conserva como riesgo visible, no se marca resuelto automáticamente. La falta de una prueba esencial siempre mantiene `needs_evidence`.

Para cerrar una objeción se requiere respuesta del autor y recibo positivo de resolución del controlador, con candidato/hash/contexto, clave del origen y `confirmed_by` del revisor original. Se rechaza `subject:*` y no se permite cerrar la objeción de otro proveedor aunque tenga el mismo ID local.

`implementation_allowed`, `production_authorized` y `activation_allowed` permanecen **false** en esta API. `approved_for_authorization` es preparación para una decisión humana, no permiso de ejecutar. Paquetes estructuralmente inválidos generan `IpanemaError` o su subclase de contrato: la futura integración debe detener/quarantinar la revisión y jamás convertir una excepción en aprobación.

## 6. Duplicidad: control preparado y evaluación pendiente

El gate exige investigación previa y un challenge de duplicidad con fuentes; diferencia exacta, semántica y legítima. No añade una dependencia ni un «detector universal» que confunda coincidencias sintácticas con responsabilidades idénticas.

Las pruebas exacta/semántica alimentan hallazgos de revisor **sintéticos**. El ejemplo semántico verifica equivalencia de inversión de listas en un dominio pequeño, pero la clasificación no la descubrió un modelo en esas unitarias. Esto no satisface todavía el criterio de detección real por los tres agentes.

Antes de activar, realizar una evaluación separada con fuentes controladas y expectativas ocultas a los revisores: clones exactos, algoritmos equivalentes en dominio declarado, responsabilidades mal ubicadas, dependencia innecesaria, doble listener y duplicación legítima. Registrar qué agente detectó qué, citas, falsos positivos, omisiones y decisiones del controlador. Los golden labels deben permanecer fuera del paquete independiente.

No exigir extraer un helper compartido por unas pocas líneas parecidas si introduce acoplamiento. Una duplicación legítima justificada no debe bloquear; una refutación HIGH precisa evidencia y confirmación, no votación.

## 7. Subagentes, permisos y alcance

Este lote no habilita delegación ni cambia herramientas nativas. Los hijos pueden recolectar evidencia solo cuando su instalación/contrato estén validados y con permisos dentro de los del padre. Se registrarán ID nativo y central, padre, objetivo, scope, permisos, evidencias, estado y resultado según el discovery V3.

Un hijo de Codex sigue siendo del mismo proveedor para independencia. No puede aprobar código de su padre ni reemplazar una revisión Claude/Antigravity. Ningún hijo podrá emitir recibos del controlador o ampliar el manifiesto.

La evaluación actual no abre navegador, red, shell de modelo ni clientes. Trabaja con archivos acotados, sin symlinks, y presupuestos de64 fuentes,2MB por fuente y4MB total. Los límites no certifican consumo universal de todo el proceso; acotan los datos de este helper. No se comparten credenciales. Se conserva el diseño de un escritor central y reserva única de navegador cuando este se implemente.

La futura política de activación debe aplicar a los cambios de código contemplados por el propietario. No se debe poner este gate como obligatorio en el flujo dual actual sin disponer del tercer revisor: bloquearía todo desarrollo. Hasta pasar aceptación se mantiene como candidato opcional fuera del runtime activo.

## 8. Pruebas ejecutadas

| Grupo | Resultado | Naturaleza |
|---|---:|---|
| Nuevo protocolo/gate | **31/31** | Fixtures sintéticas; sin proveedores ni red |
| Suites existentes `test_council*.py` | **87/87** | Compatibilidad del candidato con contratos/recibos/política anteriores |
| Orquestación, recuperación y aislamiento | **41/41** | Suites existentes sobre el candidato |
| Total de casos de estas ejecuciones finales | **159** | No equivale a aceptación con tres proveedores reales |

Resultados originales: [nuevas](unit-results.txt), [consejo](council-compatibility.txt), [orquestación](orchestration-compatibility.txt). No se repitieron auditorías de Rhino ni se ejecutaron los lotes SEO.

Los diez casos solicitados están representados:

1. Hallazgo de clon exacto no neutralizado por dos `approve`.
2. Hallazgo de equivalencia semántica no descartado; equivalencia limitada del ejemplo comprobada.
3. Hallazgo de ubicación arquitectónica incorrecta.
4. Hallazgo de dependencia innecesaria.
5. Dos listeners con ubicaciones verificables.
6. Aserción de regresión que **falla realmente** en un proceso Python sobre un ejemplo fijo del controlador; el gate exige corregir. No se ejecutan comandos sugeridos por modelos.
7. Similitud legítima INFO no bloquea.
8. HIGH refutado necesita confirmación original más recibo; la respuesta del autor sola no basta.
9. QA fundamental ausente conserva `needs_evidence`.
10. Cambio limpio con ambas revisiones sintéticas produce `approved_for_authorization`, sin permisos de operación.

Además se prueban autoaprobación con los tres autores, coautoría, duplicación/sustitución de proveedor, segundo revisor ausente, hash de diff/fuentes/permisos cambiado, cita fuera de scope, líneas/función inválidas, recibos aportados por el modelo, challenges ausentes, cierre comodín, colisión de IDs entre revisores, symlink y paquete independiente sin conclusiones del autor.

No existe configuración Python de lint/tipos encontrada en el alcance (`pyproject.toml`, ruff, mypy o setup.cfg). No se instalaron herramientas. Las pruebas importan/ejecutan los módulos candidatos; no se presenta esto como lint o type-check inexistente. Responsive, SEO y rendimiento de tienda no son consumidores de este helper y no se certifican con estas unitarias.

## 9. Revisión real intentada: recibos y bloqueo

Se usó el engine actual con dos propuestas independientes, perfil balanced, sin reintentos ni fallback. No se creó un orquestador alternativo.

- **Claude:** proceso real iniciado y recolectado, exit1,8.401s, sin timeout/cancelación. El adaptador clasificó `error_category:rate_limit`; el proveedor informó0tokens y0coste. No se atribuye a credenciales ni a una causa más específica no conservada. No hubo repetición ni evasión mediante otro proveedor.
- **Codex:** proceso real terminó exit0 y el contrato JSON nativo pasó. La primera validación semántica rechazó `analysis.files` porque el helper del controlador confundió rutas de lectura con los tres destinos futuros. Fue un error del paquete. Se conservó el fallo y **se revalidó la misma respuesta**, sin otra inferencia, contra los tres destinos ya declarados en el design-packet original. La propuesta quedó válida como `proposed`, nunca como revisión/aprobación del diff final.
- **Antigravity:** no se invocó ni habilitó; mantiene las condiciones del discovery sobre adaptador, aislamiento, autenticación y navegador.

No se ejecutaron contraste/defensa/firma final del candidato: faltan participantes válidos para completar esa fase. No se simuló un consejo completo. Recibos privados referenciados en `controller-results.json`, sin tokens ni razonamiento privado.

## 10. Riesgos y plan incremental

1. Restaurar disponibilidad del proveedor por el mecanismo del propietario, sin evadir rate limits. Corregir permanentemente el paquete local de revisión para distinguir lectura y manifiesto de propuesta; no cambiar políticas para aceptar cualquier ruta.
2. Revisar este diff exacto con Claude y Antigravity como los dos revisores del autor Codex, usando un mecanismo Antigravity validado previamente. Si este no está disponible, conservar el bloqueo; no sustituirlo por una segunda sesión de otro proveedor.
3. Demostrar la calidad de detección contextual con los diez casos y golden labels ocultos; incorporar pruebas adversariales adicionales de identidad, recibos y revisión tras correcciones.
4. Si quedan condiciones resueltas, preparar la integración exacta de los tres archivos, revalidar hashes y respaldo y actualizar el ADR con recibos. No integrar este candidato por el mero resultado de las unitarias.
5. En un lote posterior, conectar el gate al punto final del engine y al routing aprobado de V3. Eso requiere otro diff acotado, políticas aprobadas y pruebas reales del tercer adaptador; no ampliar automáticamente este parche.
6. Activar como obligatorio solo después de aceptación real. Conservar V2 sin cambios hasta entonces y mantener autorización independiente para cualquier producción.

Riesgos: falsa sensación de evidencia por un recibo inventado, limitaciones de detección semántica, bloqueo de todo V2 si se activa antes de contar con el tercer proveedor, código corregido con revisiones viejas y presión por cerrar HIGH mediante mayoría. El candidato reduce varios riesgos con contratos/hashes, pero no puede certificar honestidad de modelos o autenticidad externa sin el transporte/almacén del controlador.

Reversión de esta preparación: no hay código activo que revertir; conservar o retirar únicamente los artefactos propios identificados. Una integración futura exige pre/posthashes y detenerse ante cambios ajenos. No se tocan los cambios SEO previos, configuraciones Context7, menús, catálogo, canonicals ni la tienda publicada.
