# Acceso compartido IA-Ipanema

Política vigente: solo Claude y Codex pueden recibir o utilizar permisos activos. CommandCode conserva integración y evidencia histórica, pero está deshabilitado por `tools/ipanema/orchestration/models.json:council`; ni planes antiguos ni grants existentes pueden reactivarlo. Esta configuración no inicia MCP, OAuth ni consultas Google.

Verificación histórica: **Claude, Codex y CommandCode invocaron herramientas reales** para DaMar Beauty. Search Console respondió mediante OAuth de solo lectura. El único push de `static/css/damar.css` a 14748767, autorizado expresamente, terminó y su render publicado pasó seis comprobaciones de footer. El QA completo conserva hallazgos previos de SEO/accesibilidad, sin hallazgos nuevos. [Evidencia y límites](verification.md) · [referencia de producción y procedimiento](tiendanube-preview.md).

## Componentes existentes y acceso por tarea

La puerta sigue siendo `tools/access_mcp.py` y `Gateway`; no hay otro motor SEO, otro MCP GSC ni otro renderer. `TaskBroker` transporta ese mismo protocolo por un socket privado de tarea. El worker solo monta su socket y el puente stdio, no `.local/access`, el proyecto completo, otras tiendas o credenciales Google. Se reutilizan Bubblewrap, runtime_defaults, modelos y Supervisor del orquestador. Puppeteer/Lighthouse/QA continúan ejecutando las pruebas repetibles.

Los permisos se emiten fuera del worker por agente, proyecto y tarea, con capacidades, perfil, TTL y cuota persistente. El gateway comprueba revocación y límites antes de cada llamada. Reiniciar el cliente no recupera llamadas ni elimina una detención 403/429. El mismo usuario del host con escritura en el controlador sigue siendo parte confiable; no se presenta el identificador del permiso como autenticación criptográfica del proveedor.

```bash
python3 tools/ia.py --project damarbeauty access doctor --probe-devtools
python3 tools/ia.py --project damarbeauty access grant --agent codex --task seo-home-001 --capability devtools.read --browser-profile audit --allow-network
python3 tools/ia.py --project damarbeauty access config --grant ID_DEVUELTO
python3 tools/ia.py --project damarbeauty access revoke --grant ID_DEVUELTO
```

`config` genera una configuración revisable sin modificar ajustes personales. Para invocaciones reales de tarea, con consumo de inferencia autorizado:

```bash
python3 tools/ia.py --project damarbeauty access probe-agents --url https://damarbeauty.mx/ --browser-profile audit --execute
python3 tools/ia.py --project damarbeauty access probe-agents --url https://damarbeauty.mx/ --browser-profile audit --agent claude --execute
```

El éxito exige eventos observados en el gateway para descubrimiento, apertura y snapshot; una respuesta textual del modelo no basta. El informe conserva agente asignado, efectivo, causa, sustituto, modelo, métricas disponibles y proceso terminado. Un sustituto no acredita éxito del agente original. Los checkpoints previos no se reproducen para recuperar una CLI: se prueba solamente el agente recuperado.

CommandCode usa `dont-ask` con lista de herramientas permitidas: su modo plan oculta MCP. Claude usa configuración MCP estricta y herramientas locales deshabilitadas. Codex usa configuración de tarea, sandbox de lectura y aprobaciones explícitas solo para las herramientas concedidas; su aislamiento monta también `codex-code-mode-host` y `codex-exec-server` de la misma distribución, sin montar el directorio personal. No se hicieron cambios en configuraciones personales.

## Dos perfiles independientes

| Perfil | Recursos | Uso |
|---|---|---|
| `security` | Solo origen registrado de la tienda/preview | Pruebas aisladas; no representa rendimiento de la tienda con CDN |
| `audit` | Orígenes comprobados en HTML/red y registrados en `browser.devtools_audit_origins` | Auditoría real con CDN, imágenes, fuentes y scripts legítimos |

El perfil queda ligado al permiso de tarea, no a argumentos que un agente pueda ampliar. Cada sesión tiene navegador y perfil efímero propios. DevTools MCP **1.12.0** conserva pin e integridad npm, estadísticas desactivadas, CrUX desactivado, sin evaluación de scripts del cliente ni archivos locales. No se adjunta a un navegador personal. El navegador dedicado lo inicia el runtime Puppeteer existente; DevTools se conecta exclusivamente a ese endpoint privado.

El runtime conserva bloqueos de POST/PUT/PATCH/DELETE, rutas comerciales y formularios. La página puede ejecutar sus scripts de lectura; llamadas de apps basadas en POST y telemetría se bloquean. Esto se registra como diferencia frente a una sesión normal de compra. La prueba Chrome loopback verificó que un CDN no registrado se bloquea en security, el CDN registrado se carga en audit y un POST de página no llega al servidor. Nunca se interpretan trazas del perfil restringido como rendimiento real.

En DaMar se comprobaron descargas desde CDN de Tiendanube, Google Fonts y scripts propios/terceros iniciados por la página. No se usa un comodín de Internet ni se confía automáticamente en un origen sugerido por una respuesta externa.

## Google Search Console

Propiedad: `sc-domain:damarbeauty.mx`. Google confirmó `siteOwner` y respondió Search Analytics, URL Inspection y sitemaps. Se reutiliza `OfficialREST`, `prepare`, `ReadOnlyAdapter` y `normalize`. No se habilitaron escrituras, solicitud de indexación ni envío de sitemaps.

El flujo explícito de escritorio usa PKCE S256, state aleatorio y callback loopback. Solo solicita `webmasters.readonly`, sin refresh token ni acceso offline. El JSON cliente está en `.local/google-oauth-client.json`, modo 0600. Después de verificar acceso, el access token de corta vida se guarda en `.local/access/credentials/damarbeauty-gsc.json`, modo 0600 y directorio 0700, ligado a proyecto, propiedad, scope y expiración. No aparece en informes, prompts, argumentos, Git o mounts del worker. No se renueva automáticamente: una credencial vencida requiere nuevo consentimiento. El almacén usa permisos del sistema de archivos; no se afirma cifrado de disco.

```bash
python3 tools/ia.py --project damarbeauty access oauth --client .local/google-oauth-client.json --url https://damarbeauty.mx/ --probe-agents --execute
```

El comando abre el navegador local; el usuario aprueba Google. Antes de las tres lecturas, una consulta oficial `Sites.get` comprueba la propiedad y el permiso. El resultado de URL Inspection es el estado conocido del índice, no inspección en vivo. Search Analytics puede devolver cero filas en el periodo solicitado; eso no prueba ausencia total de tráfico. Los sitemaps son metadatos registrados, no un inventario completo de URLs.

El gateway utiliza la credencial privada solo en el controlador. Cada agente demostró también `gsc_sitemaps` a través de su socket, sin recibir el token. Las respuestas externas son datos no confiables. Mocks de tests se identifican como tales; las evidencias de esta conexión real están separadas. `doctor` comprueba instalación y disponibilidad de credencial; su estado de API no sustituye la prueba real enlazada en verification.

Analytics y Merchant siguen opcionales y desactivados hasta conceder sus capacidades en una tarea concreta. No se instalaron MCP adicionales para ellos.

## Capacidad concedida

| Capacidad | Herramientas |
|---|---|
| `devtools.read` | open, snapshot, lista de red, consola |
| `devtools.performance` | traza de carga e insights, en la misma sesión de página |
| `gsc.read` | Search Analytics, URL Inspection y sitemaps |
| `analytics.read` | run_report opcional |
| `merchant.read` | productos opcionales |

No se exponen clicks, compras, formularios, cookies, cuerpos/cabeceras de red, archivos, JavaScript arbitrario, publicación o comandos de Tiendanube. Abrir y recargar una página son operaciones explícitas de navegación.

## QA, instalación y reversión

La instalación reproducible mantiene los manifests en `integrations/chrome-devtools`; copiar esos dos archivos a `.local/devtools` y usar `npm ci --prefix .local/devtools --ignore-scripts --no-audit --no-fund`, únicamente si se autoriza instalar en otra máquina. No hay instalación automática, `@latest` ni paquete global nuevo. Chrome >=149 es necesario para el control de orígenes del upstream.

```bash
python3 tools/ia.py qa --suite quick
python3 tools/ia.py qa --suite fixtures
python3 -m unittest tests.integration.test_access_broker tests.unit.test_access_oauth tests.unit.test_orchestration_recovery -v
```

Revocar un permiso cierra futuras llamadas. Retirar la configuración de tarea no cambia configuraciones ajenas. Una detención por 403/429 necesita revisión del operador; no se evade con otro proyecto, agente o proceso. Para el cambio local del footer se conserva su transacción, hashes y patch de reversión. No hay publicación automática ni renderer Twig improvisado.
