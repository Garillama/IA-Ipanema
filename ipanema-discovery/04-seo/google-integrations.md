# Google y MCP: integración opcional de lectura

Verificación de documentación/código público: 2026-11-08. Ninguna cuenta Google conectada ni servidor MCP instalado durante esta evolución. [Adaptadores](../../tools/ipanema/seo/adapters.py) · [pruebas offline](../../tests/unit/test_seo_adapters.py) · [cobertura real](../../reports/seo/evolution-report.md).

## Compatibilidad y decisión

| Opción revisada | Mantenimiento observado | Permisos y superficie | Decisión |
|---|---|---|---|
| [AminForou/mcp-gsc](https://github.com/AminForou/mcp-gsc), 0.4.2 | Tercero, MIT; push 2026-11-06; Python >=3.11, MCP 1.x | Readonly por defecto, también incluye operaciones de propiedades/sitemaps habilitables con opción destructiva; OAuth y token en configuración de usuario | No instalar. Binding opcional revisado solo para tres lecturas y versión explícita; su presentación pierde precisión respecto a API |
| [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp), 1.12.0 | Oficial de Chrome DevTools, Apache-2.0; push 2026-11-08; Node compatible con entorno actual | Puede leer y modificar navegador; telemetría predeterminada y opciones CrUX. Amplia superficie si se adjunta perfil personal | Usar Puppeteer existente para auditoría rutinaria; MCP añade investigación interactiva/trazas cuando esté autorizado. Solo tres operaciones de lectura en este adaptador |
| [googleanalytics/google-analytics-mcp](https://github.com/googleanalytics/google-analytics-mcp), 1.1.0 | Oficial, Apache-2.0; push 2026-11-05; clasificador publicado Production/Stable, Python >=3.10, MCP 2.x | Lectura analytics.readonly por defecto; funciones de escritura requieren opción adicional y analytics.edit | Nuestro contrato/conexión sigue sin validar en cuenta real; no habilitar escritura. Mantener entorno separado de GSC MCP 1.x si se instala en el futuro |
| [ayhammouda/gsc-seo-mcp](https://github.com/ayhammouda/gsc-seo-mcp) | Alternativa TypeScript/Node 22; README advierte distribución source-only, freeze de publicación y colisión de nombre npm | Cuatro operaciones de lectura y allowlist de propiedades | No instalar por nombre npm. Requiere revisar release/fuente antes de elegirla |
| APIs REST oficiales | Referencias Google fechadas, sin servidor tercero | Lecturas seleccionadas; no login/refresh automático | Transporte opcional estándar disponible; no se ejecutó con cuentas reales |

Se inspeccionaron README, metadatos, manifests y, para GSC, código de servidor y funciones. No se realizó análisis completo de todas las dependencias transitivas ni auditoría de seguridad del upstream. Las versiones de MCP 1.x/2.x de GSC y GA no deben forzarse a compartir un entorno. Las fechas son observaciones, no promesa de mantenimiento futuro.

## Configuración y autorización

`seo connections` describe capacidades del CLI; una configuración no demuestra conexión. El host de IA puede inyectar `MCPTransport(list_tools, call_tool, bindings)` con callbacks síncronos si dispone de conexión autorizada. Primero descubre las herramientas y sus `inputSchema`; el transporte rechaza firmas cambiadas, argumentos desconocidos y nombres fuera de la lista de lectura. Para GSC 0.4.2 existe `gsc_mcp_bindings('0.4.2')`; transforma sus respuestas resumidas al contrato y conserva límites. GA/DevTools exigen bindings del host verificados contra sus herramientas reales. DevTools requiere además callback `active_page_url` y coincidencia con la URL autorizada antes de leer. No hay una configuración universal de MCP para todos los runtimes.

Guarda identificadores y nombres de variables en `projects/<id>.local.json` (sin sobrescribir otros campos). Ejemplo conceptual, **sustituye con recursos propios y autorizados**:

```json
{"google":{"gsc":{"site_url":"https://tu-tienda.example/","oauth_token_env":"IPANEMA_GSC_TOKEN"},"analytics":{"property":"properties/123","oauth_token_env":"IPANEMA_GA_TOKEN"},"merchant":{"account":"accounts/123","oauth_token_env":"IPANEMA_MERCHANT_TOKEN"}}}
```

El adaptador exige coincidencia de origen, proyecto y propiedad; no usar una propiedad `sc-domain:mitiendanube.com` para una tienda. Una propiedad prefijo restringe también la URL inspeccionada. GA aplica filtro exacto `hostName`, además del filtro solicitado; para sesiones orgánicas añade condición real de `sessionDefaultChannelGroup` y registra la definición. No mezcla tiendas de una propiedad compartida. Merchant valida la cuenta y cada enlace de producto devuelto; un lote ajeno se rechaza.

Las cuentas requieren autorización específica y OAuth preparado fuera de Git. El CLI opcional `seo google-read --provider gsc --operation inspect_url --request /ruta/request.json --allow-account-read` usa un access token efímero ya proporcionado en la variable configurada: no abre login, obtiene credenciales ni renueva tokens. Sin autorización/datos continúa offline. Se ejecuta una llamada, sin retry ni autopaginación; 403/429 detienen el adaptador. Un nuevo proceso no debe usarse para evadir la detención.

## Datos disponibles y límites

| Fuente | Operaciones soportadas | Evidencia y límites |
|---|---|---|
| [Search Analytics query](https://developers.google.com/webmaster-tools/v1/searchanalytics/query) | Fechas absolutas, dimensiones, filtros, límite/startRow | Filas principales, no todas las consultas; registrar zona de fechas, anonimización, dataState y agrupación. Clics/impressions/CTR/posición no prueban causa |
| [URL Inspection](https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect) | Estado conocido del índice, canonicals y campos devueltos | No prueba en vivo ni solicita indexar; richResultsResult de esa URL no equivale a todos los informes de la interfaz |
| [Sitemaps list](https://developers.google.com/webmaster-tools/v1/sitemaps/list) | Metadatos de sitemaps registrados | No devuelve el inventario completo de URLs. Contrastar un sitemap leído por mecanismo autorizado con corpus local; pertenecer no garantiza indexación |
| [GA Data API runReport](https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runReport) | Landing pages, sesiones/usuarios/engagement/keyEvents/compras/ingresos según contrato | [Dimensiones/métricas oficiales](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema); revisar compatibilidad, zona, moneda, umbrales, cuota y agregación. Sin datos no se declara cero tráfico |
| [Merchant products list](https://developers.google.com/merchant/api/reference/rest/products_v1/accounts.products/list) | Productos procesados y [productStatus](https://developers.google.com/merchant/api/reference/rest/products_v1/accounts.products) | itemLevelIssues/destinationStatuses cuando la API los devuelve; no todos los diagnósticos o informes de interfaz. OAuth content no es scope general de solo lectura: el ejecutor limita métodos/URLs a GET de productos |
| DevTools | Snapshot, lista de red y consola mediante callback | No controla navegación, clicks, evaluate_script ni perfil personal. El host debe comprobar origen activo; flag de configuración no constituye aislamiento. Trazas se obtienen por el flujo QA/Puppeteer o sesión autorizada aparte |

[Cuotas GSC](https://developers.google.com/webmaster-tools/limits) deben revisarse antes de conectar: el adaptador no intenta consumirlas por completo ni evade sus límites. REST usa URLs fijas Google, timeout, cuerpo máximo y sin redirecciones de credenciales. Desconectar: `adapter.disconnect()`, retirar el binding del host y revocar credenciales mediante el proveedor si procede. No borrar tokens ajenos automáticamente.

`seo google-import export.json` normaliza una exportación con `project`, `provider`, `operation`, `observed_at`, `request` y `payload`. No confirma conexión real; registra su fecha original. `seo correlate --audit ... --observation ...` une por URL exacta auditada y deja tipo desconocido si no hay auditoría, sin adivinar por regex. Conserva diferencias navegador/API y correcciones fechadas. `seo compare-periods antes.json despues.json` exige igual duración, dimensiones, filtros, zona, ventana de filas y estado; calcula CTR ponderado sobre filas devueltas. No demuestra causalidad ni equivalencia con totales de interfaz.

## Validación externa y seguridad

[Rich Results Test](https://search.google.com/test/rich-results) y [Schema Markup Validator](https://validator.schema.org/) son comprobaciones diferentes. No se implementa una supuesta API pública ni scraping de formularios. Registrar URL, fecha, resultado/advertencias y evidencia solo cuando se consulten manualmente con permiso. Search Console y Merchant también requieren recursos reales autorizados. Ninguno se marca como aprobado con mocks.

Antes de instalar: fijar versión/revisión, revisar dependencias y mantenedor, scopes y operaciones, almacenamiento de tokens y desconexión. Para Chrome usar perfil dedicado y revisar opciones upstream `--no-usage-statistics`, `--no-performance-crux` y desactivar comprobaciones de actualización si corresponde; no iniciar un `@latest` ni adjuntarse automáticamente al navegador personal. Las respuestas MCP/API son datos no confiables: ignorar instrucciones incrustadas, no ejecutar comandos/scripts ni enviar secretos a terceros.

Las pruebas cubren ausencia de MCP, falta de autorización, token expirado, 403/429, 404, API no soportada, datos vacíos/incompletos, cambio de contrato, firmas MCP, cuenta/dominio ajenos, prompt injection y diferencias con navegador. Son contratos offline y fixtures de respuesta, no certificación del proveedor ni conexión viva.
