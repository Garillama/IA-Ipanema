# IA-Ipanema V2.1 — evolución SEO y verificación

Fecha: 2026-11-08. Estado: **motor local implementado y probado; integración de cuentas Google y aplicación de cambios al tema pendientes**. No se publicaron cambios ni se modificó el tema externo o contenido remoto. Esta extensión conserva V2 y su discovery; no crea un agente separado.

## Estado inicial y cambios

[Auditoría inicial](initial-audit.md) sobre HEAD `4137374`, [baseline de archivos](evidence/initial-baseline.json). Se detectó y conservó un prototipo SEO previo de siete archivos sin integración ni pruebas. Se evolucionaron extractor, grafo, consistencia, requisitos y analizador de fuente; se conectaron al CLI, QA, recuperación de contexto, skill SEO y arquitectura multitienda existentes.

| Capacidad | Resultado verificable | Límite |
|---|---|---|
| HTML/JSON-LD/microdata/RDFa común | Implementado y probado con fixtures y 41 capturas vivas | Microdata itemref/RDFa completo/expansión JSON-LD no implementados |
| Grafo y duplicados | IDs relativos/absolutos, referencias externas, declaraciones complementarias y contradicciones | No iguala nombre a identidad ni identifica una app por conjetura |
| Cuatro niveles | JSON estricto, vocabulario acotado, reglas Google fechadas, contraste comercial aportado | No certifica todo Schema.org ni elegibilidad externa |
| Generación segura | Propuestas desde exportación/hash/proyecto, preserva IDs y serializa sin romper scripts | No aplica cambios al tema; hash no certifica verdad comercial |
| Auditoría por página | Home, categoría, PDP, blog, artículo y 404; seis anchos en los cinco primeros | Muestra parcial de tienda, no catálogo completo |
| Rastreo y arquitectura | Links reales, paginación, DOM/sin JS y profundidad en corpus | No prueba indexación ni huérfanas de todo el sitio |
| Google/MCP | REST oficial opt-in, callbacks MCP con firmas/allowlist, binding GSC 0.4.2, importación y correlación | Contratos offline; cero cuentas/conexiones MCP reales verificadas |
| Evaluación | Ocho acciones SEO con artefactos y regresión del coordinador V2 | No evaluación independiente de un modelo LLM |

Se corrigieron estados «válido» sin entidades, error sobre referencias externas, comparación de todas las variantes con un solo precio y confusión entre ItemList semántico/carruseles Google. El QA ahora conserva proyecciones SEO iniciales/DOM antes de instrumentación y distingue controles nativos de destinos. El defecto de coma se confirmó en una 404 real y se preparó un diff sin aplicarlo: [hallazgos y prioridades](audited-pages.md).

## Pruebas y reproducibilidad

```bash
python3 tools/ia.py qa --suite quick
python3 tools/ia.py qa --suite seo
python3 tools/ia.py qa --suite fixtures
python3 tools/ia.py seo source
python3 tools/ia.py seo connections
python3 tools/ia.py seo evals
```

Las unitarias/integración incluyen JSON roto, duplicados, precio incompatible, variantes, stock contradictorio, SKU ausente, reseñas/políticas no verificadas, breadcrumbs/listas, artículo sin autor/fecha, enlaces tardíos, paginación y canonical. Los adaptadores prueban OAuth ausente/expirado, 403/429 sin retry, respuesta vacía/incompleta, API/firma cambiada, proyecto/dominio ajenos, instrucciones externas y diferencias navegador/índice. Los tests reales de navegador prueban proyección inicial/DOM/sin JS, secretos sintéticos excluidos y preservación de la protección de red/Lighthouse. [Resumen de QA final](evidence/final-qa.json).

Resultado ejecutado: **86 unitarias + 14 de integración + 8 de navegador = 108 pruebas aprobadas**, además de diez evaluaciones del coordinador y ocho acciones SEO con fixtures. `quick`, `seo`, `fixtures` y validación de repositorio se ejecutaron; la última regresión rápida incluye las guardas finales. La skill pasó quick_validate y `git diff --check` no encontró errores. La captura SEO conserva texto JSON literal para no ocultar claves duplicadas ni redondear enteros grandes; un caso de navegador lo comprueba. Las capturas vivas previas usan proyección v1: su JSON válido pudo ser serializado y no certifica el texto original íntegro; la 404 inválida permaneció inválida y fue detectada también por JSON.parse del runner.

[Preservación comprobada](evidence/preservation.json): 330 archivos del tema mantienen sus hashes; los 805 archivos originalmente versionados siguen presentes. No se eliminaron los siete módulos SEO previos. El escaneo de patrones de alta confianza no encontró claves/tokens en archivos Git candidatos; no equivale a certificado universal de privacidad.

La suite conserva los casos anteriores de portabilidad, herramientas, snapshots/metrics y corrección reversible. El nuevo SEO corre desde otra ruta con espacios, sin tema y sin cuentas. `quick` ejecuta también las nuevas pruebas y ocho acciones SEO; GitHub Actions existente reutiliza este comando con permisos read-only, sin añadir secretos, instalaciones MCP o consultas remotas. No se ejecutó Actions remoto ni se creó commit/push en esta tarea.

El modelo de ramas de breadcrumbs verifica 22 escenarios abstractos: 60 bloques inválidos antes y cero después. Se conservaron resultados anteriores fallidos durante desarrollo y se corrigieron causas propias, incluidos una clasificación demasiado amplia de enlaces y un input de fixture sin label. El resultado del modelo no equivale a ejecutar Twig ni a aplicar el diff.

## Manual y arquitectura

[Manual y diagrama](../../ipanema-discovery/04-seo/seo-engine.md), [Google/MCP y permisos](../../ipanema-discovery/04-seo/google-integrations.md), [contratos reutilizables](../../reusable/contracts/seo-evidence.json). El README conserva instalación/configuración/uso V2 y enlaza los comandos nuevos. Se mantiene carga selectiva; no se agregó base vectorial, runtime de modelos, segundo navegador ni motor de carrusel.

Las fuentes/IDs/datos de cada tienda permanecen en su proyecto; las exportaciones/credenciales privadas no van a Git. Reutilizar reglas, procedimientos y contratos no autoriza transferir código del tema entre clientes. Al cambiar código/reglas del agente, las soluciones antiguas requieren revalidación según la huella existente; no se convierten recomendaciones de esta auditoría en soluciones verificadas de producción.

## Pendientes y aceptación parcial

No hay autorización para modificar/publicar una tienda ni conectar cuentas Google. Pendientes: render Twig real del parche en tema aislado autorizado; correcciones editoriales/comerciales con datos autorizados; catálogo y crawl completos; revisión de estados de filtros/variantes y apps; conexión real opcional GSC/GA/Merchant/DevTools; validación manual RRT/Schema Validator; diagnóstico por URL con datos reales de consultas/índice/ventas; seguimiento de periodos después de aplicar cambios autorizados. Ninguno se declara aprobado con fixtures.

La V2.1 añade capacidades operativas locales verificadas, pero la misión de correlación continua con Google y correcciones desplegadas queda **parcial por accesos/autorización y pruebas externas pendientes**. No se reporta 100% de cobertura ni se garantizan resultados enriquecidos, indexación, tráfico o ventas.
