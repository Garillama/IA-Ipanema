# B — contrato de piloto sintético Antigravity

**Estado: needs_evidence; proveedor no ejecutado.** El contrato, fixtures y argv propuesto están preparados; la fase de inferencia/autenticación permanece bloqueada.

- [Contrato](pilot-contract.json): recursos, restricciones, interrupciones, recibos y límites.
- [Comando propuesto, no autorizado](command-proposed-NOT-AUTHORIZED.txt): ejecutable con aislamiento OS y supervisor externo; no debe ejecutarse directamente mientras sigan pendientes sus condiciones.
- [Manifiesto sintético](synthetic-fixtures.json).
- [Preflight de filesystem](os-filesystem-preflight.json), [cancelación y descendiente](os-cancellation-preflight.json), [montajes exactos](exact-mount-probe.json).

## Comprobado sin agente

Se reutilizó el aislamiento existente para Python sintético. Se comprobó workspace readonly, marcador sintético del host inaccesible, HOME real ausente, namespace de red distinto y conexión de prueba de loopback denegada. El montaje exacto propuesto se ejercitó sustituyendo únicamente el ejecutable final por el probe Python, nunca por Antigravity.

En una prueba nueva, breve y justificada por este piloto, el supervisor agotó2s y recuperó el proceso; un hijo Python que había hecho setsid también desapareció de /proc. Se identificó por nonce sintético y se confirmó su ausencia. No era un subagente de IA. Esto demuestra esa cancelación local controlada, no todas las futuras variantes del proveedor.

## Operación propuesta

CLI JSON/NDJSON, sin ACP adicional: bwrap con namespace PID/red, entorno vacío y HOME/tmp efímeros; runtime y fixture readonly. GNU timeout impone60s absolutos, sin reintentos. La política nativa propuesta deniega read_file, write_file, command, unsandboxed, read_url, execute_url y mcp mediante sus namespaces documentados; no depende de instrucciones escritas solo en el prompt. [Permisos oficiales](https://antigravity.google/docs/permissions/).

La respuesta estructurada solicitada solo analiza un ejemplo aritmético inline sintético y devuelve un valor/observación. El propio JSON del agente **no puede certificar que se autenticó, respetó permisos o terminó a sus hijos**: eso requiere recibos nativos y observación del controlador. Exit0 tampoco prueba que se ejecutó una herramienta; una denegación puede ser blanda. [Headless oficial](https://antigravity.google/docs/cli/headless/).

## Recursos y prohibiciones

Accesibles: runtime/lib del sistema en solo lectura, binario agy exacto con SHA, directorio de fixtures sintéticas readonly, HOME y tmp desechables. No se montan repo de IA-Ipanema, archivos de Rhino, otros clientes, HOME real, keyring, DBus, cookies, perfiles Chrome ni credenciales. No navegador, MCP configurado, remote-control, subagentes, herramientas de shell o acceso externo.

El comando actualmente mantiene **red descompartida y ninguna credencial**. Por eso no puede presentarse como prueba de inferencia autenticada. El límite de salida64KiB y la comprobación de eventos/descendientes son requisitos del controlador para la futura ejecución; el comando aislado por sí solo no certifica todo ese contrato.

## Condiciones que impiden ejecutar todavía

1. Acordar y autorizar el mecanismo oficial de autenticación acotado; no montar todo el keyring/HOME ni copiar tokens. No hay login ni extracción de credenciales en esta fase.
2. Definir y autorizar los destinos de inferencia estrictamente necesarios y su enforcement. No se propone abrir toda la red o usar credenciales/billing alternativos silenciosamente.
3. Acreditar cómo se deshabilitan/observan todos los subagentes, hooks y plugins nativos en esta versión. No se inventa un flag de desactivación inexistente. Los namespaces Deny documentados y el aislamiento OS son necesarios, pero todavía no prueban esa cobertura nativa.
4. Validar con evidencia nativa las denegaciones efectivas, parseo del resultado y cancelación del árbol real. No dar estas condiciones por pasadas porque funcionó Python sintético.

Interrumpir ante autenticación interactiva, permiso nuevo,403/429/cuota, herramienta/MCP/browser/hijo no declarado, JSON inválido/truncado, presupuesto agotado o cleanup incierto. Conservar checkpoint sin reintentar ni ampliar accesos. Una ejecución futura exige autorización específica después de concretar1–3; este contrato no la concede.
