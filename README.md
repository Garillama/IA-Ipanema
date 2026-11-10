# IA-Ipanema V2

El [acceso compartido a DevTools y Google](reports/access/README.md) añade permisos por agente, proyecto y tarea para Claude, Codex y CommandCode. Reutiliza QA/SEO existentes, instala solo DevTools MCP fijado y activa las lecturas Google con OAuth autorizado por proyecto.

La [orquestación multiagente](reports/orchestration/README.md) coordina Claude Code, Codex y CommandCode con riesgo L1–L4, modelos proporcionales, worktrees y validación central. `python3 tools/ia.py orchestrate doctor` comprueba requisitos. `python3 tools/ia.py orchestrate task "Optimiza el carrusel de categorías en mobile y desktop sin afectar SEO ni rendimiento"` prepara el plan; añade `--execute` para inferencia real y cambios aislados. Entrega diff y evidencia, sin publicar ni escribir en el tema original. [Resultados y límites](reports/orchestration/verification.md).

Agente de ingeniería para temas seccionables Ipanema de Tiendanube. Combina instrucciones de trabajo, nueve skills, conocimiento existente y herramientas locales para investigar, preparar cambios, probarlos y registrar evidencia. Necesita el runtime de IA con el que abras esta carpeta; no incluye un modelo ni un servidor de inferencia propio.

La V2 conserva el discovery original. **El tema y las tiendas remotas no se modifican al instalar o ejecutar las pruebas offline.** [Evolución y cobertura V2](reports/v2/evolution-report.md), [arquitectura](reports/v2/architecture.md), [auditoría inicial](reports/v2/initial-audit.md). La extensión **V2.1 SEO** añade auditorías por página, grafo/validación de schemas, propuestas con procedencia y adaptadores Google opcionales: [resultado y límites](reports/seo/evolution-report.md).

## Preparación

Necesitas Git y Python 3.10 o superior. Clona o copia este repositorio y abre la carpeta con tu asistente. [AGENTS.md](AGENTS.md) define permisos y método; las [skills de OpenAI](https://learn.chatgpt.com/docs/build-skills) se descubren por sus descripciones y cargan su contenido cuando corresponde.

```bash
python3 tools/ia.py --version
python3 tools/ia.py projects list
python3 tools/ia.py doctor
python3 tools/ia.py qa --suite quick
```

Los comandos también funcionan desde otro directorio usando la ruta completa a `tools/ia.py`. Las pruebas básicas usan la biblioteca estándar de Python, sin pip ni npm. `doctor` muestra dependencias opcionales y disponibilidad local; no se conecta a Tiendanube ni instala paquetes.

Para navegador se necesitan Node >=22.19, Chrome/Chromium y Puppeteer, axe-core y, si vas a medir rendimiento, Lighthouse. El runtime reutiliza paquetes ya instalados, incluidos los del CLI de Tiendanube; también admite node_modules del repositorio o `IPANEMA_NODE_MODULE_ROOT`. `IPANEMA_CHROME_PATH` selecciona otro Chrome. [package.json](package.json) registra las versiones usadas. Si decides instalar dependencias en otro equipo, revisa primero ese archivo y ejecuta `npm install` de manera explícita; no hay instalación automática ni lockfile de dependencias transitivas todavía.

## Configurar y seleccionar una tienda

El [registro](projects/registry.json) contiene proyectos compartidos. La ubicación real del tema va en `projects/ipanema.local.json`, ignorado por Git:

```json
{"theme_root":"/ruta/real/al/tema"}
```

También puedes usar `IPANEMA_THEME_ROOT`. Nunca se usa la ruta personal antigua de las evidencias como requisito ni fallback. Sin tema puedes consultar el conocimiento y probar el agente; los cambios/auditorías de código necesitan una ruta válida.

```bash
python3 tools/ia.py projects register tienda-dos --name "Tienda dos" --theme-root /ruta/real/al/tema --url https://ejemplo.mitiendanube.com
python3 tools/ia.py projects use tienda-dos
python3 tools/ia.py --project ipanema doctor
```

La selección sigue `--project` → `IPANEMA_PROJECT` → selección local → default. Registrar un proyecto no descarga el tema ni verifica su instalación remota. La versión/variante/fork guardada es una observación con fecha. [Configuración, páginas, presupuestos e interacciones](projects/README.md).

## Uso cotidiano

Puedes pedir: «Modifica esta product card sin duplicar la lógica», «Haz otro layout móvil con el mismo contenido» o «Comprueba cómo descubre Google los enlaces de este carrusel».

El asistente selecciona especialidades, recupera fuentes y verifica la implementación real. El router propone capacidades mediante reglas; necesita el juicio del agente. No se invocan subagentes automáticamente.

```bash
python3 tools/ia.py route "Quiero modificar una product card"
python3 tools/ia.py search "tarjeta de producto" --limit 2
python3 tools/ia.py search "padding_top" --limit 2
python3 tools/ia.py plan "Modificar la product card compartida" --action local-change --authorize-local --save
```

`search` devuelve fichas, configuraciones, consumidores directos/transitivos, hallazgos, fuentes y vigencia. Comprueba el archivo actual: un hash igual no acredita sincronización remota. Un proyecto nuevo recibe referencias históricas con compatibilidad sin comprobar. El plan contiene candidatos y pruebas pendientes; no sustituye la inspección del código.

La preferencia es configuración nativa, composición existente, tokens, componente compartido, extensión y solo después código nuevo. Se conservan contratos LS, js-*, data-store, precio/stock/variantes y formularios. No se agregan `!important`, motores de carrusel o copias de componentes por defecto.

## QA reproducible

| Comando | Alcance |
|---|---|
| `python3 tools/ia.py qa --suite quick` | Repositorio, unitarias, integración, diez evaluaciones del coordinador y ocho acciones SEO con fixtures; offline |
| `python3 tools/ia.py qa --suite seo` | Pruebas SEO unitarias/integración y ocho evaluaciones de acciones; no conecta cuentas |
| `python3 tools/ia.py qa --suite repo` | Enlaces, JSON, skills, inventario y estado del tema si está disponible |
| `python3 tools/ia.py qa --suite source` | Captura estática del tema configurado y métricas de assets sin modificarlo |
| `python3 tools/ia.py qa --suite fixtures` | Chrome, axe, responsive, teclado, red y Lighthouse en servidor sintético de loopback |
| `python3 tools/ia.py qa --suite page --page home --allow-network` | Página real configurada; solo con lectura remota autorizada |
| `python3 tools/ia.py qa --suite component --page category --component ".js-product-container" --allow-network` | Selector real del componente en página configurada |
| `python3 tools/ia.py qa --suite full --page home --allow-network --lighthouse` | Offline más navegador, seis anchos, sin JS, reduced motion, Coverage y Lighthouse |

Los comandos de tienda requieren un entorno preparado y autorizado. Durante V2.1 se ejecutó el runner existente en lectura sobre cinco tipos de página/seis anchos y una 404: [resultados reales](reports/seo/audited-pages.md). El QA por selector no equivale a todos sus consumidores: selecciona y verifica las páginas/estados pertinentes. Las interacciones se configuran con selectores inspeccionados, sin enviar compras, registros, contacto o newsletter. El runtime bloquea solicitudes de escritura salvo el acceso de storefront expresamente provisto; se detiene ante límites de acceso. No es un sandbox del resto de herramientas que pudiera usar un runtime externo.

Los runs usan directorios nuevos en `reports/runs/<proyecto>/`, ignorados por Git. Sus JSON registran herramientas, versiones, perfiles, resultados, limitaciones y hashes; las capturas/mediciones se preservan ahí. Copia solo evidencia revisada y sin datos confidenciales a un informe compartido.

```bash
python3 tools/ia.py compare visual /ruta/antes.png /ruta/despues.png --pixel-threshold 12 --max-changed-ratio 0.005
python3 tools/ia.py compare visual /ruta/antes.png /ruta/despues.png --mask 0,0,200,60
python3 tools/ia.py compare metrics /ruta/antes-metrics.json /ruta/despues-metrics.json
```

La protección incluye pestañas iniciales y las creadas por Lighthouse. Bloquear POST puede alterar apps que lo usan para lectura; no atribuyas ese efecto al tema y compara bajo la misma política de red.

## SEO y datos estructurados

```bash
python3 tools/ia.py seo source
python3 tools/ia.py seo audit --capture /ruta/al/run/browser/category-390-rendered.seo.json
python3 tools/ia.py seo connections
python3 tools/ia.py seo evals
```

El [manual SEO](ipanema-discovery/04-seo/seo-engine.md) explica auditoría offline, HTML/DOM/sin JS, corpus de enlaces, fuentes comerciales y generación de propuestas. `seo source` prepara un diff revisable del defecto nativo cuando coincide con el patrón encontrado; no aplica cambios. JSON válido, vocabulario comprobado, requisitos Google, consistencia, prueba externa y aparición en Google son estados distintos. No se inventan datos ni se duplica el marcado nativo para compensar errores.

`seo generate` exige HTML actual y datos referenciados/hash del mismo proyecto; su salida queda fuera del tema. Search Console/GA/Merchant y MCP son [integraciones opcionales](ipanema-discovery/04-seo/google-integrations.md), desconectadas por defecto. No se instalan servidores ni conectan cuentas con estos comandos básicos. Los mocks prueban contratos; no demuestran acceso real a Google ni indexación.

PNG admite RGB/RGBA 8-bit hasta 20 MP. Las dimensiones distintas se reportan; diferencias por encima del umbral requieren revisión de intención. Las máscaras no deben cubrir lo que se está comprobando. Métricas necesitan misma página/perfil. Comparar una muestra de laboratorio no demuestra mejora estadística; TBT no es INP. Las solicitudes se separan por fase para distinguir navegación de efectos de la propia captura/instrumentación.

## Corrección controlada

Para una corrección no trivial conserva primero un QA que reproduzca el fallo. El agente diagnostica y propone el parche; las herramientas limitan cambios y verificación, sin generar parches arbitrarios en bucle.

```bash
python3 tools/ia.py attempt begin --file sections/mi-seccion.tpl --max-attempts 2 --authorize-local
python3 tools/ia.py attempt apply ID --patch /ruta/parche-local.json
python3 tools/ia.py attempt verify ID --suite quick --baseline /ruta/qa-del-fallo/report.json
```

El patch es un objeto JSON `{ "ruta/relativa": "contenido nuevo completo" }` para archivos declarados; guárdalo fuera de Git si contiene código del cliente. `verify` ejecuta QA, acepta solo si hay pruebas aprobadas posteriores con los hashes actuales y corrección del fallo anterior; ante fallo revierte el intento si no hay cambios posteriores ajenos. Para aceptar con otro QA pertinente usa `attempt accept ID --evidence REPORTE --baseline BASELINE`; `attempt revert ID` revierte explícitamente el intento. Los archivos nuevos se eliminan solo si siguen siendo los creados por el intento. Nunca se usa reset/clean.

El máximo predeterminado es dos intentos, configurable hasta cinco. Un conflicto o límite detiene el proceso y requiere un informe. Las transacciones privadas están ignoradas y conservan el estado previo del usuario, no solo HEAD. Una comparación insuficiente no se convierte en aprobación; completar el contexto/pruebas puede requerir intervención del agente.

## Conocimiento reutilizable y evaluación

El [catálogo y contratos](reusable/README.md) distinguen conocimiento, patrones, procedimientos, código autorizado, código de cliente, funcionalidad nativa y recursos propietarios. No contienen copias de implementación del tema ni conceden derechos sobre ellas. Usa `python3 tools/ia.py solutions` para consultar soluciones efectivamente vigentes; [el registro](reusable/solutions.json) exige evidencia QA y se invalida al cambiar código, instrucciones, proyecto o evidencia pertinentes.

```bash
python3 tools/ia.py evals
python3 tools/ia.py evals --responses /ruta/respuestas.jsonl
```

La primera ejecución prueba selección, recuperación de referencias y planificación del coordinador. **No es una evaluación completa de un modelo implementando diez tiendas.** La segunda recibe artefactos de una ejecución externa para calificar decisiones/referencias/pruebas; requiere revisión humana de calidad funcional y visual. [Casos y protocolo](tests/agent-evals/README.md), [resultados y límites](reports/v2/evaluation.md).

## Errores frecuentes y permisos

- Tema ausente: configura una ubicación real en el override local o variable; no se hace pull automático.
- Proyecto incompleto: corrige id/schema_version/registro según doctor; el CLI termina con error claro.
- Paquete o Chrome ausente: usa doctor y configura las dependencias opcionales; los tests offline siguen disponibles.
- Resultado `blocked`: falta acceso/dependencia o hubo 403/429; no es una prueba aprobada. No reintentes ni evadas el control automáticamente.
- Captura de password: no se acredita la página solicitada; usa acceso de lectura autorizado mediante variable de entorno temporal. No pongas contraseñas en argumentos, archivos o logs.
- Baseline cambiado: la validación normal lo informa y la búsqueda marca obsolescencia. `python3 tools/check_workspace.py --strict-source` exige coincidencia con la captura; es control de integridad, no QA de un cambio intencional.

El CLI no publica ni sincroniza tiendas. watch, push, publish, cambios de catálogo/checkout y operaciones comerciales necesitan autorización específica. Los scripts históricos se conservan, con rutas/runtime portables y destinos nuevos; los renderizadores reconstruyen documentos fechados y no deben usarse como actualización automática del discovery.

La [base original](ipanema-discovery/README.md), sus [hallazgos](ipanema-discovery/11-opportunities/critical-findings.md) y su [cobertura](ipanema-discovery/DISCOVERY-COMPLETENESS-REPORT.md) siguen disponibles. Craft Anything se estudió como metodología en el [análisis original](ipanema-discovery/01-architecture/craft-anything-assessment.md); no se instaló como motor de esta V2.
