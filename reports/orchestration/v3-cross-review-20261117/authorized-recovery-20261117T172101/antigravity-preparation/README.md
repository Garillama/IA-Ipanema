# Antigravity — preparación incremental

Estado: **bloqueado**, cero invocaciones `agy`. Se conservan contrato y comprobaciones OS anteriores, sin repetirlas.

**Autenticación:** la ruta oficial `modelProvider:gemini` + `GEMINI_API_KEY` es compatible en principio con HOME vacío y una única credencial gestionada por el propietario. No requiere montar todo el keyring. No se leyó ni solicitó una clave; su uso/facturación requieren elección y autorización separadas. La sesión local no tiene todavía un mecanismo aislado acotado demostrado. ADC es otra alternativa oficial, pendiente de proyecto y permisos. [Autenticación](https://antigravity.google/docs/install/).

**Egreso:** el destino API documentado es `generativelanguage.googleapis.com:443`, POST de generación/stream para un modelo fijo aprobado. Es una lista candidata mínima, no la lista exhaustiva comprobada de agy. Falta un relay/firewall revisado que bloquee salida directa, limite host y valide TLS; limitar paths requiere enforcement de aplicación, no solo CONNECT. No abrir `*.googleapis.com`, toda Internet o subidas de archivos. No hubo consultas a esa API. [Endpoints oficiales](https://ai.google.dev/api/generate-content?hl=en).

**Hooks/plugins:** los hooks se descubren en `~/.gemini/config/hooks.json` y `.agents/hooks.json`; un `hooks` dentro de settings.json no los desactiva porque no se carga. Plugins globales/workspace tienen directorios propios. HOME efímero y workspace sintético excluyen configuraciones del propietario; queda por probar comportamiento bundled/nativo. [Settings](https://antigravity.google/docs/settings?tab=cli).

**Herramientas/subagentes:** conservar Deny documentados, MCP vacío y ausencia de navegador. `--disable-slash-commands` no garantiza desactivar subagentes; tampoco basta una definición `subagent:false`. Debe acreditarse la allowlist efectiva sin herramientas antes de ejecutar. [Subagentes](https://antigravity.google/docs/subagents?tab=cli).

**Recibos y cancelación:** contract-delta.json concreta identidad de binario/config/entrada/modelo, política de red/montajes, eventos sanitizados y observación del controlador; límite60s, concurrencia1, cero reintentos,64KiB de salida y parada ante accesos no declarados o cleanup incierto. Reutilizar supervisor y namespace PID; el hijo Python setsid previo no certifica todo el árbol real de agy.

No existe aún una operación de inferencia segura completamente especificada: faltan ruta de credencial elegida, enforcement de egreso y cobertura nativa. No se cambia el comando anterior para introducir red o credenciales silenciosamente. Si esas condiciones no pueden satisfacerse, mantener bloqueado. Una llamada directa Gemini API no cuenta como revisión de Antigravity.
