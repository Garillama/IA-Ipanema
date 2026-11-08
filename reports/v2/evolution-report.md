# Evolución IA-Ipanema V2

**Estado: V2 funcional en local; validación integral parcial.** Se implementaron y probaron configuración portable, coordinación selectiva, recuperación de conocimiento, QA unificado, comparaciones, correcciones locales limitadas y registro de soluciones con evidencia. No se modificó la implementación ni se publicó ninguna tienda.

El alcance pendiente se declara de forma explícita: evaluación independiente de un modelo implementando A–J, otros sistemas operativos reales, ejecución remota de CI y QA nuevo del storefront/estados privados. No se acredita autonomía general ni cobertura completa por tener documentos o tests del coordinador.

## Estado inicial y conservación

Inicio en `b800f13`, main, árbol limpio y origin `Garillama/IA-Ipanema`. La versión anterior ya tenía discovery, extractores y mediciones; sus principales carencias eran rutas personales, configuración de una tienda, destinos fijos, pruebas manuales y ausencia de evaluación/registro verificable. [Auditoría inicial](initial-audit.md), [baseline](evidence/agent-baseline.json).

Se conservaron **los 712 archivos del discovery sin cambios**, todos los archivos originales siguen presentes y los **330 archivos del tema coinciden con su captura original**. Los scripts e instrucciones se evolucionaron localmente; los comandos principales find_component, audit_source y check_workspace permanecen. [Comprobación de conservación](evidence/preservation.json).

## Capacidades y clasificación actual

| Capacidad | Clasificación | Evidencia / límite |
|---|---|---|
| Registro y selección multitienda | IMPLEMENTADO Y PROBADO | CLI/env/local/default, validación y varios proyectos sintéticos |
| Portabilidad de entrada/configuración | IMPLEMENTADO Y PROBADO | Copia en otra ruta con espacios, otro cwd, tema ausente y errores; un solo sistema Linux |
| Ocho especialidades y coordinadora | IMPLEMENTADO SIN PRUEBAS SUFICIENTES | Nueve skills validadas y fuentes enlazadas; comportamiento independiente del modelo pendiente |
| Selección y planes estructurados | IMPLEMENTADO Y PROBADO | Router/plan reales y diez casos; asistencia determinista que el runtime debe contrastar |
| Recuperación selectiva | IMPLEMENTADO Y PROBADO | Componentes, settings, consumidores, documentos, hallazgos, soluciones y fechas/hashes |
| Implementación de cambios por IA | PARCIAL | Método, permisos y herramientas disponibles; este encargo implementó el propio agente, no diez tareas de tema |
| QA offline unificado | IMPLEMENTADO Y PROBADO | 35 unitarias, 7 de integración y diez casos del coordinador aprobados |
| QA Chrome/axe/Lighthouse/funcional | IMPLEMENTADO Y PROBADO | Siete pruebas de navegador y puente Python→Node sobre fixtures locales |
| QA de tienda/editor/checkout | PARCIAL | Evidencia histórica conservada; no nueva ejecución remota ni transacciones en esta migración |
| Comparación visual/métricas | IMPLEMENTADO Y PROBADO | PNG, máscaras, umbrales, contexto de métricas y controles negativos; sin baseline nuevo de una tienda modificada |
| Corrección controlada y reversión | IMPLEMENTADO Y PROBADO | Dos intentos reales en fixture, primero revertido y segundo aceptado; conflictos y hashes comprobados |
| Soluciones verificadas y obsolescencia | IMPLEMENTADO Y PROBADO | Dos soluciones de herramientas registradas; pruebas de invalidación por archivos/evidencia/versión |
| Catálogo multitienda y contratos | IMPLEMENTADO SIN PRUEBAS SUFICIENTES | JSON y referencias inspeccionados; integración entre tiendas/versiones no ejecutada y sin distribución de código del tema |
| Biblioteca de implementación compartida | DOCUMENTADO, NO IMPLEMENTADO | Requiere código propio autorizado, compatibilidad e integración por tienda; no se inventó importación en el editor |
| CI offline | IMPLEMENTADO SIN PRUEBAS SUFICIENTES | Workflow preparado con checkout fijado y permiso de lectura; no ejecutado en GitHub |
| Inferencia externa y pruebas ciegas de modelos | BLOQUEADO POR DEPENDENCIA EXTERNA | Protocolo y receptor de artefactos disponibles; sin runtime independiente ejecutado ni uso/coste medidos |
| Publicación y transacciones automáticas | AUSENTE | El ejecutor V2 no expone estas operaciones; requieren autorización específica fuera de este flujo |

Las clasificaciones separan implementación de prueba de comportamiento. El catálogo no demuestra por sí solo integración entre dos tiendas reales, ni el router demuestra calidad creativa del modelo.

## Cambios concretos

- Configuración: ruta del tema retirada del JSON compartido; override local ignorado y variable de entorno. Detección de raíz desde archivos del agente, sin fallback a la ruta histórica. Registro con páginas, entorno, observación remota fechada, presupuestos y evidencias por proyecto.
- Instrucciones: AGENTS conserva permisos, mínima intervención, contratos nativos y prevención de overrides. ipanema-storefront coordina ocho skills con responsabilidades separadas y carga progresiva de las fuentes existentes.
- Herramientas: tools/ia.py reúne doctor, projects, route, search, plan, qa, compare, attempt, evals y solutions. Los módulos comparten configuración, errores, evidencia y lógica; browser_runtime/page_collectors se reutilizan desde scripts anteriores.
- QA: pruebas rápidas, de origen, página, componente, fixtures, auditoría completa y comparaciones. Nuevos destinos por ejecución, bloqueo de escritura y límites de acceso, perfiles y fases de red. No se instala ninguna dependencia al ejecutar el agente.
- Corrección: archivos declarados, backups locales privados, hashes, máximo configurable, QA posterior y comparación con el fallo anterior. No se descartan cambios ajenos ni se llama reset/clean.
- Reutilización: catálogo A–G, contratos de imagen/card/comercio y enlace a tokens nativos existentes. Soluciones con fecha, contexto, código, causa, pruebas, evidencia y vigencia calculada.

## Decisiones y correcciones verificadas

Se eligió búsqueda estructurada porque los inventarios, settings y grafo ya permiten recuperar fuentes precisas; no se añadió una base vectorial. Se reutilizaron Python estándar y paquetes de navegador instalados; package.json registra versiones directas, sin instalar nuevas dependencias ni copiar un runtime de Craft Anything.

Las primeras evaluaciones encontraron defectos de ranking y una referencia equivocada en el propio benchmark; se corrigieron con inspección del inventario y tests. Una captura fullPage generó solicitudes responsive adicionales: se separó navegación de instrumentación para evitar diagnósticos falsos.

Una prueba de seguridad encontró dos POST sintéticos de Lighthouse que escapaban del primer interceptor. Se protegieron todas las pestañas y la repetición registró cero en ambos perfiles. Son fallos y soluciones de estas herramientas, no vulnerabilidades atribuidas al tema. [Evidencia y pruebas](testing.md), [soluciones vigentes](../../reusable/solutions.json).

## Criterios de aceptación

| Criterio | Resultado |
|---|---|
| Utilizable en otra ruta, proyecto activo y sin rutas personales obligatorias | Aprobado en simulación local; otros OS físicos no comprobados |
| Skills claras y conocimiento existente conservado | Aprobado estructuralmente; evaluación del modelo parcial |
| Herramientas anteriores conservadas | Comandos principales, extractor, helpers y collector comprobados; no todos los escenarios históricos reejecutados |
| QA y evaluación reproducibles | Aprobado para herramientas/coordinador; ejecución externa de modelos pendiente |
| Recuperación relevante y prioridad nativa | Probada en casos y referencias reales; el agente aún debe comprobar cada fuente actual |
| Cambios locales revisables y sin publicación automática | Aprobado: cambios en el repositorio, tema intacto, sin ejecutor de producción |
| Contratos y soluciones con evidencia fechada | Aprobado, con compatibilidad y límites explícitos |
| Pruebas no ejecutadas identificadas | Aprobado; ver matriz en testing.md |
| Secretos y datos privados fuera de Git | Overrides/backups/runs ignorados; sin contraseñas/cookies/tokens incorporados en esta migración; no equivale a pentest |
| Manual de preparación/configuración/uso | Disponible en README y projects/README |

Por los pendientes de comportamiento integral, sistemas y entornos externos, **no se marca la V2 como validada al 100%**.

## Uso y siguientes verificaciones

El [manual](../../README.md) permite empezar con doctor, projects list y qa quick; la [arquitectura](architecture.md) incluye el diagrama y límites. [Pruebas](testing.md) y [evaluaciones](evaluation.md) separan resultados reales de pendientes.

Prioridad siguiente: ejecutar A–J con un runtime/modelo identificado en aislamiento y revisión independiente. Después comprobar CI en GitHub y una matriz real Windows/macOS/Python, cerrar el lockfile opcional de dependencias y ensayar QA en una preview preparada. Las integraciones de compra, stock/error y editor requieren su entorno específico; no se presentan como aprobadas por HTML ni fixtures.

No se hizo commit/push de esta evolución ni se sincronizó la tienda. Los cambios quedan locales y revisables.
