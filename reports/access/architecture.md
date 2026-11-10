# Investigación de arquitectura: acceso compartido

Fecha: 2026-11-09. Proyecto: `ipanema`, con selección del registro V2. Se inspeccionó código actual. El plan automático propuso snippets de búsqueda por coincidencia de palabras: se descartaron porque no son consumidores de esta integración.

| Fuente inspeccionada | Cobertura anterior | Decisión |
|---|---|---|
| `tools/ipanema/qa.py`, `tools/qa_browser.mjs`, `tools/browser_runtime.mjs` | Puppeteer, capturas SEO, axe, Lighthouse, permisos de QA remoto | Conservar pruebas repetibles |
| `tools/ipanema/seo/adapters.py` | GSC/GA/Merchant: contratos, REST/callback MCP, normalización, dominio y cuotas | Reutilizar, sin otro MCP para GSC |
| `tools/ipanema/seo/cli.py` | Lecturas con token externo, importación, correlación y comparación | Conservar interfaz compatible |
| `tools/ipanema/orchestration/{adapters,isolation,engine}.py` | Workers aislados, credenciales de inferencia separadas, propuestas JSON y QA central | No añadir secretos Google ni montajes al worker |
| `tools/ipanema/core.py` y registro de proyectos | Selección, configuración local, sanitización, evidencia | Reutilizar `Project`; invalidar permisos si cambia configuración |
| `ipanema-discovery/04-seo/google-integrations.md` | Evaluación histórica de proveedores y límites | Conservar intacta; evidencia nueva separada |

Instalar MCP GSC añadiría otro proceso/contrato aunque REST ya cubre las tres lecturas. Registrar DevTools directamente en cada cliente expondría herramientas fuera de la política del proyecto; se encapsula. Compartir perfiles/cookies o pasar tokens a workers rompería los límites existentes. El upstream recibe HOME temporal y entorno mínimo. No se duplica Lighthouse ni se añade SDK MCP como dependencia Python.

## Flujo y consumidores

Operador → permiso privado por agente/proyecto/tarea/capacidades/TTL/cuota → configuración MCP → `access_mcp.py` → `Gateway` → adaptadores REST existentes o DevTools stdio → observación + auditoría sin payload crudo.

Consumidores nuevos: `tools/ia.py access`, entrada MCP, clientes que carguen su configuración y tests. Cada sesión conserva su upstream/perfil de navegador; se comparte instalación y contrato, no pestañas. Los comandos SEO previos siguen disponibles. No hay servidor público, OAuth automático, publicación o daemon nuevo. Los permisos no provienen de páginas ni instrucciones del modelo.

## Riesgos y alcance

Cambios locales del agente, tests, lock y documentación. No se cambia HTML, CSS, editor, checkout o datos del tema; responsive/SEO/accesibilidad de storefront no se certifican con estas pruebas. El coste DevTools aparece solo en diagnóstico; Puppeteer/Lighthouse conservan las mediciones repetibles. El perfil restringido bloquea CDN/terceros: no se promete una mejora ni equivalencia con carga completa.

La puerta impone permisos en su interfaz. Procesos del mismo usuario con escritura en el controlador no están aislados entre sí. Los workers aislados existentes conservan sus restricciones y no reciben acceso directo nuevo. La etiqueta `agent` identifica el permiso emitido; no autentica un proveedor. Configuración generada y herramientas descubiertas no demuestran que un modelo las haya utilizado.

## QA y reversión

Política: denegación predeterminada, dominio/proyecto ajenos, caducidad, revocación, configuración cambiada, cuotas persistentes y 403/429 entre permisos. Stdio real: initialize, lista filtrada y revocación con sesión abierta para las configuraciones de los tres clientes. Chrome en loopback: apertura, snapshot, consola, red, traza y detención por 403. Google permanece con mocks explícitos hasta disponer de propiedad/token autorizados. Regresión: `qa --suite quick`. Las pruebas locales no demuestran indexación.

La autocorrección usa `attempt`, hashes y backups propios. Retirar únicamente el diff de acceso revierte el código; desregistrar la configuración por tarea y revocar su permiso cierra el acceso. No se descartan cambios previos del usuario, cambia una dependencia global o publica una tienda.

Fuentes: [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp), [metadatos npm de 1.12.0](https://registry.npmjs.org/chrome-devtools-mcp/1.12.0), [scope Search Console](https://developers.google.com/webmaster-tools/v1/how-tos/authorizing), [MCP en Codex](https://learn.chatgpt.com/docs/extend/mcp). También se inspeccionaron los help de las CLI locales, código distribuido del upstream y esquemas por `tools/list`; no se hizo auditoría exhaustiva de dependencias transitivas.
