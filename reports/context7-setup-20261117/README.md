# Context7 en IA-Ipanema — 2026-11-17

Estado: configuración instalada en Claude Code y Codex; pendiente de autenticación del propietario y carga en una sesión nueva. No se declara una integración operativa completa.

Fuente oficial consultada: https://context7.com/get-started.md. Requiere Node>=22.13; instalado24.22.0, npm11.19.1. Claude Code2.1.326; Codex0.169.0; instalador ctx7@latest resuelto0.12.2 en caché npx. No se instaló otro runtime ni un servidor stdio local: ambos clientes usan HTTP OAuth remoto https://mcp.context7.com/mcp/oauth.

## Operaciones realizadas

Se ejecutó una vez por cliente, tras comprobar ausencia de Context7 y respaldar los archivos afectados:

```sh
npx ctx7@latest setup --claude --mcp --oauth --yes
npx ctx7@latest setup --codex --mcp --oauth --yes
```

Ambos terminaron correctamente. No se inició OAuth, no se pidieron claves, ni se guardaron tokens manualmente. Se conservó el alcance global oficial, sin MCP de proyecto adicionales. No hubo cambios en lógica de negocio, modelos, orquestador, clientes externos ni Rhino Performance.

## Archivos afectados

- ~/.claude.json: única entrada context7 HTTP OAuth añadida; otros campos idénticos semánticamente.
- ~/.claude/rules/context7.md: regla oficial y límites de uso proporcional, versiones, evidencia y permisos.
- ~/.claude/skills/context7-mcp/SKILL.md: skill oficial instalada.
- ~/.codex/config.toml: única entrada mcp_servers.context7 añadida; configuración anterior preservada semánticamente.
- ~/.codex/AGENTS.md: regla oficial y límites equivalentes.
- ~/.agents/skills/context7-mcp/SKILL.md: skill oficial para Codex.
- AGENTS.md del repositorio: sección documental añadida; todo el contenido anterior conservado. No cambia requisitos del consejo ni autorización remota.

Los archivos de configuración global no se copian al informe público. Respaldos privados y manifiesto en .local/context7-setup/20261117T162025/, directorio0700, copias0600. verification.json contiene hashes, rutas y comprobaciones sin tokens. Se verificó el contenido anterior de ambos config excluyendo únicamente la entrada Context7; igualdad completa. No se eliminaron otros MCP.

## Verificación y límites

- JSON de Claude y TOML de Codex parsean correctamente.
- claude mcp list: context7 aparece como Needs authentication.
- codex mcp list --json: context7 enabled:true, auth_status:not_logged_in.
- Codex mantiene postman-mcp listado y habilitado; también not_logged_in. Eso no demuestra su conectividad autenticada.
- Configuración del plugin Postman de Claude sin cambios byte a byte. No se certifica su funcionamiento en una sesión autenticada.
- El servidor Context7 no está cargado entre las herramientas de la sesión controladora actual. No se usó un conector de cuenta como sustituto.
- resolve-library-id y query-docs: NO ejecutados todavía; pendientes del login y recarga del cliente correspondiente. No se finge una consulta válida mediante otra API o credencial.

## Acciones del propietario

Claude Code: reiniciar; ejecutar /mcp; seleccionar context7; Authenticate. Completar el inicio de sesión en el navegador.

Codex: ejecutar en la terminal propia:

```sh
codex mcp login context7
```

Completar el inicio de sesión del navegador y abrir una sesión nueva de Codex para cargar herramientas. No compartir tokens ni contraseñas.

En cada cliente autenticado, pedir: «Usa Context7 para resolver next.js con resolve-library-id; después llama query-docs con el identificador obtenido para consultar una API del App Router». Registrar fecha, ID realmente devuelto y respuesta; no usar un identificador supuesto como prueba. Confirmar que ambos tools finalizan sin error. Verificar después los demás MCP en su propio estado autenticado. No instalar ni repetir setup por faltar login.

## Reversión

Antes de revertir comprobar los hashes posteriores de verification.json. Si cambiaron, detener y reconciliar cambios ajenos. Retirar únicamente la entrada context7 y las instrucciones/skills añadidas por esta operación; restaurar un archivo completo desde respaldo solo si permanece exactamente en el estado posterior registrado. Para AGENTS.md eliminar exclusivamente el apartado añadido si no hay cambios posteriores en él. No sustituir otros MCP, permisos o configuraciones del usuario.

Estado oficial por cliente: Claude Code — waiting for sign-in; Codex — waiting for sign-in. Docs check: pending en ambos. El login no forma parte de las acciones automatizadas autorizadas.
