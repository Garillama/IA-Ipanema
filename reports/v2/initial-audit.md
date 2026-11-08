# Auditoría del agente anterior y migración V2

Fecha: 2026-11-08. Inicio local en `b800f13`, rama main, árbol limpio, remote `Garillama/IA-Ipanema`. [Baseline de 734 archivos y validación](evidence/agent-baseline.json). No se ejecutó fetch/pull ni se modificó la tienda.

| Capacidad inicial | Clasificación | Evidencia / limitación |
|---|---|---|
| Inventario y búsqueda de componentes | IMPLEMENTADO Y PROBADO | audit_source.py, find_component.py y captura de 223 unidades; búsqueda por nombre/hooks, sin consulta completa de consumidores |
| Integridad del tema y enlaces | IMPLEMENTADO Y PROBADO | check_workspace.py: 330 archivos sin cambios, 4324 enlaces; depende de la ruta histórica |
| Auditorías Chrome/axe/Lighthouse | IMPLEMENTADO Y PROBADO | Evidencias del discovery; ejecución acoplada a paquetes del CLI y Chrome del equipo original |
| Cobertura de todos los estados de comercio | PARCIAL | Carrito vacío y variantes parciales; ninguna transacción autorizada |
| Portabilidad y multitienda | PARCIAL | Raíz Python relativa, pero source_root absoluto, runtime JS absoluto, destinos y URLs fijos |
| Arquitectura reutilizable | DOCUMENTADO, NO IMPLEMENTADO | Playbooks y design system; no catálogo ejecutable de contratos ni distribución de código |
| Coordinación de especialidades | PARCIAL | Una skill y selección manual, sin plan estructurado comprobable |
| Suite de pruebas de las herramientas | AUSENTE | No directorio tests ni runner unificado; validación de sintaxis e integridad anterior no sustituye tests |
| Regresión visual antes/después | AUSENTE | Capturas disponibles, sin comparador/umbrales |
| Evaluación de decisiones del agente | AUSENTE | Sin casos ni scoring reproducible |
| Autocorrección limitada y reversión selectiva | DOCUMENTADO, NO IMPLEMENTADO | No transacciones locales ni límite de intentos |
| Soluciones verificadas/versionadas | AUSENTE | Hallazgos y propuestas, sin registro validado por pruebas |
| CI | AUSENTE | Sin workflow |
| Editor, checkout y datos de campo | BLOQUEADO POR DEPENDENCIA EXTERNA | Requieren entorno/accesos específicos; no se infieren de HTML ni Lighthouse |

Los generadores render_inventory/render_runtime/render_findings son herramientas de reconstrucción del discovery, no un pipeline genérico de auditoría. No deben ejecutarse para actualizar automáticamente una observación histórica. La documentación extensa no se duplicará en cada skill.

La base funciona como instrucciones para un runtime de IA existente. No incluye un modelo propio, daemon ni API de inferencia. Las herramientas nuevas deben complementar esa colaboración, sin atribuir a un router determinista la capacidad de ejecutar una tarea de ingeniería completa.

## Migración y aceptación

1. Configuración: resolver raíz desde el script, seleccionar proyecto por CLI/env/local/default, separar paths locales ignorados y observaciones remotas fechadas. Probar reubicación, ausencia del tema, configuración incompleta y varios proyectos.
2. Coordinación: conservar ipanema-storefront como entrada y separar ocho especialidades; búsqueda estructurada con consumidores, settings, hallazgos y vigencia, sin base vectorial.
3. QA: reutilizar extracción, auth y paquetes existentes; añadir runner, fixtures locales, comparación de métricas/capturas y CI sin acceso a tiendas ni secretos.
4. Control: autorizaciones por nivel, operaciones de producción fuera del ejecutor, intentos acotados y reversión solo de archivos propios sin pisar modificaciones posteriores.
5. Evaluaciones y reutilización: diez casos mínimos con resultados observables; separar pruebas del coordinador de evaluación del modelo. Contratos/patrones propios y registro de soluciones con evidencia y compatibilidad.
6. Cierre: repetir pruebas relevantes, verificar conservación de todos los archivos del discovery y hashes del tema; entregar cobertura y pendientes explícitos.

Se aceptará cada capacidad por su implementación, caso de uso y prueba reproducible. La integración CI remota, otros sistemas operativos reales, transacciones de tienda y ejecuciones de otros modelos no se marcarán probados por simulaciones locales.
