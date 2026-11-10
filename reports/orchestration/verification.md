# Implementación y verificación de orquestación

Fecha: 2026-11-08. Estado: **orquestador local funcional, con QA de storefront deliberadamente parcial**. No se modificó ni publicó una tienda. [Manual e inicio](README.md) · [auditoría de runtimes/modelos](runtime-compatibility.md) · [evidencia de inferencia real](live-verification.json).

## Implementación

Se incorporó `tools/ipanema/orchestration/` al CLI existente, sin otra base de conocimiento ni segunda implementación SEO. `planner.py` usa router/Knowledge para riesgo L1–L4, skills y componentes candidatos; `adapters.py` construye argumentos verificados y valida respuestas; `isolation.py` impone Bubblewrap, HOME efímero, auth separada, snapshot RO, tiempo y salida; `engine.py` controla DAG, worktrees, concurrencia, SHA256, QA, corrección limitada y diff. `cli.py` expone doctor/task/plan/run/status/smoke. El registro de modelos tiene fuentes/fecha y esfuerzo por perfil, sin nombres de CLI inventados.

Se conservan AGENTS, nueve skills y registro multitienda. Se amplió la coordinadora con el flujo nuevo y se documentaron permisos. Los candidatos se recuperan del inventario actual; la ejecución no permite convertir un candidato ambiguo en acceso irrestricto. Los cambios del agente y del tema se tratan como scopes separados. El repo original y su HEAD no se cambian por ejecutar un trabajo: cada run tiene repositorio privado/worktrees y entrega un patch.

## Comprobaciones reales

Las tres CLI instaladas ejecutaron inferencia real sobre un archivo sintético: Claude Code 2.1.319, Codex 0.167.0 y CommandCode 1.88.5. Cada worker recibió solo auth propia RO y no vio HOME/Git originales. Estos smoke tests acreditan esos modelos/cuentas en ese momento; no todos los modelos fuertes/críticos ni permisos futuros.

Después se ejecutó el comando `orchestrate task ... --execute` completo sobre un tema sintético: Claude planificó, Codex cambió únicamente el H1 visible, el controlador ejecutó auditoría fuente/schema antes/después y CommandCode aprobó la revisión limitada. Los tres estados terminaron completed, exit code 0, diff disponible y original_still_matches true. El patch dejó el schema intacto. [Evidencia con modelos, decisiones, tiempos y contadores reales](live-verification.json). No se etiquetó como pruebas visuales/SEO vivo/performance aprobadas.

También se ejecutaron tests con Git y Bubblewrap reales. La concurrencia de dos escritores disjuntos se prueba con workers mock explícitos y una barrera; ese caso no afirma haber ejecutado dos modelos simultáneos. Los smoke de inferencia reales sí fueron iniciados en paralelo. La suite offline no consume cuentas/modelos.

## Fallos encontrados y corregidos

- El snapshot de tema inicialmente incluía solo el archivo a editar: el auditor nativo exigía el layout. Ahora el controlador conserva el tema completo para QA local y entrega al worker una vista reducida de lectura.
- El NDJSON de CommandCode alcanzó el límite de salida en revisiones. Se conservan esos runs fallidos y se usa su modo text documentado para recibir únicamente el objeto final, manteniendo límites de proceso/salida. Cambiar a un modelo equilibrado por sí solo no solucionó ese formato.
- Un revisor comparó before_sha256 con el archivo ya modificado e interpretó la ausencia de pruebas del implementador como ausencia de QA central. Ahora recibe hashes antes/después, diff y atribución explícita de QA. La revisión puede seguir bloqueando hallazgos reales; no se fuerza approve.
- Se corrigieron rutas `.`/`./`, aprobación por review sin decisión explícita, downgrade de riesgo en planes manipulados, escritores en planes read-only y paralelismo inválido.
- Se probó que una edición ajena durante inferencia bloquea la entrega y que el diff se calcula contra baseline inmutable. La reversión de correcciones restaura únicamente archivos propios y detecta conflictos.

## QA y límites

El [resumen final](qa-results.json) registra comandos, resultados y cantidades. Hay tests de clasificador/modelos/contratos, CLI portable, dependencias, writers duplicados, paths/hash/symlinks, autenticación aislada, cuotas de tiempo/salida, concurrencia y correcciones (fallo/fallo/éxito y límite persistente). `qa --suite quick` vuelve a ejecutar la regresión existente y las nuevas pruebas; `qa --suite orchestration` ofrece el subconjunto sin inferencia. Los resultados con mocks están identificados.

Resultado final: **109 unitarias + 25 de integración = 134 pruebas aprobadas**, incluidas **34 de orquestación**, más diez evaluaciones del coordinador y ocho acciones SEO con fixtures. La revisión final también reprodujo y corrigió contaminación por variables `GIT_*`: el controlador ahora usa un entorno mínimo y hooks desactivados; la regresión verifica que otro repositorio no recibe init/add/commit ni archivos de trace. Un escritor tampoco corre en paralelo con un lector de ese mismo archivo; los lectores dependientes esperan una nueva ola.

Se revalidaron los hashes de los **330 archivos del tema real**, sin cambios. No hubo login de tienda, publicación, instalaciones de dependencias ni conexión a Google durante esta implementación. El discovery anterior permanece como fuente principal; no se rehízo.

Limitaciones vigentes: ejecución de workers requiere Linux/Bubblewrap; inference network no es firewall por dominio; CommandCode no garantiza deshabilitar subagentes internos; auth RO puede impedir refresh; la calidad relativa de todos los modelos no está medida; asignación alternativa puede configurarse en un plan revisado, pero no existe entrenamiento estadístico automático. L4 tiene guardas de independencia probadas offline; no se ejecutó un cambio comercial L4 real. No se afirma haber probado tiendas/clientes/checkout ni todos los estados responsive con código modificado.

El estado `reviewable_partial_qa` significa que existe una propuesta revisable con las comprobaciones descritas, no aprobación de despliegue. La verificación Twig/visual/rendimiento requiere entorno de prueba preparado y autorizado, usando los comandos QA/compare actuales. Una solución reutilizable solo pasa al ledger verificado cuando se pruebe su implementación y contexto; los experimentos de modelos no se convierten en reglas comerciales ni resultados de producción.


## Recuperación real de Claude y acceso compartido — 9-11-2026

Se conservaron los runs/checkpoints anteriores. La ronda de acceso `20261109T191403-access-agents-3519377a` registró fallo real de autenticación de Claude y sustitución supervisada; CommandCode completó apertura y snapshot reales. Codex descubría MCP, pero su ejecutor de code-mode no estaba montado. Se montaron solo `codex-code-mode-host` y `codex-exec-server` de la misma distribución, sin añadir el HOME ni credenciales de tienda. `20261109T192123-access-agents-a73491fc` verificó ambas invocaciones por Codex mismo.

Después de OAuth autorizado, `20261109T192546-access-agents-9ea99aa2` verificó Codex y CommandCode con apertura, snapshot y `gsc_sitemaps`. La sustitución de Claude de ese run no se contó como salud de Claude. Tras el usuario ejecutar `claude auth login`, `claude auth status` devolvió logged_in=true, y se probó **únicamente Claude**: `20261109T192921-access-agents-91c8d542` completó descubrimiento, apertura, snapshot y `gsc_sitemaps` con `claude-sonnet-5-5`. No se repitieron las tareas completadas por CommandCode.

Los tres actores están disponibles con invocaciones reales observadas, no solo `--help`. Se reutilizó el aislamiento y Supervisor existentes. Los circuitos son por run: la recuperación no modifica retrospectivamente los fallos, no reescribe checkpoints ni promete resume automático de trabajos antiguos. Un nuevo run puede usar la sesión reparada; la recuperación específica desactivó sustitución para exigir evidencia del actor original.

Se ejecutaron de nuevo las **18 regresiones de recuperación**, aprobadas, con fallos simulados identificados. La evidencia de failover real anterior se conserva por separado; no se forzó un nuevo fallo de proveedor ni se consumió inferencia para repetir tareas aprobadas. Todas las llamadas de tienda/GSC permanecieron mediadas por el gateway; el worker solo recibió su socket de tarea y autenticación de su propio proveedor.

Aceptación conjunta y hashes: `reports/runs/damarbeauty/20261109T193631-access-acceptance-e865237c/acceptance.json`. Ese era el estado al crear la aceptación de actores. Después, con autorización específica condicionada del usuario, se ejecutó un único push de `static/css/damar.css` a 14748767 y se verificó su render publicado en seis casos. No se crearon clones o instalaciones de QA. El cierre, hashes, comparación y hallazgos previos conservados están en `reports/access/verification.md` y `reports/runs/damarbeauty/20261109T201036-published-footer-qa-56b0b215/acceptance.json`. Se conservaron los checkpoints y no se repitieron trabajos de CommandCode.
