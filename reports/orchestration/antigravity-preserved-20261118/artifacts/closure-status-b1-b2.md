# IA-Ipanema V3 — cierre de fase Antigravity H1–H4

Estado operativo: **`needs_evidence`**. Esta nota cierra la fase de trabajo; no declara resueltos B1/B2 ni habilita Antigravity.

## Estado conservado

- V2 conserva el consejo dual Claude + Codex como política activa.
- Antigravity permanece registrado, deshabilitado y con perfiles/modelo sin verificar.
- El adaptador H1–H4 está en el candidato local aislado; no se integró al controlador operativo.
- B1: no se demostró una frontera que conserve la autenticación CLI de Antigravity y haga inaccesible la credencial para herramientas y procesos descendientes.
- B2: no se demostró enforcement de egreso por destino. Se conserva la evidencia histórica de que el host no permite crear/consultar las reglas necesarias y de que el canario montado podía ser leído por un proceso hijo.
- No se repitieron pruebas ni diagnósticos del host. No hubo llamadas a proveedores, uso de credenciales reales ni acceso a Rhino.

## Adaptador: capacidades probadas sintéticamente

El candidato implementa selección del sobre JSON de Antigravity con validación de estado, schema y salida estructurada; rechaza estados no exitosos, JSON inválido/duplicado, identidad declarada y roles sin schema. Mantiene límite explícito de prompt y preflight de disponibilidad para una configuración triádica futura. Las 22 pruebas focalizadas registradas cubren estas rutas y confirman que L3/L4 siguen requiriendo Claude + Codex por defecto.

Esto solo demuestra comportamiento local con fixtures. No demuestra autenticación, acceso a cuenta/modelo, transporte de inferencia, aislamiento real de secretos, control de egreso, ni que las herramientas/subagentes de `agy` estén efectivamente deshabilitados.

## Requisitos mínimos para una habilitación futura

1. Entorno aislado administrado que imponga y registre deny-by-default y una allowlist de destinos de inferencia, comprobada contra destinos permitidos y prohibidos, DNS, IPv4/IPv6 y redirecciones.
2. Mecanismo oficialmente compatible con la identidad CLI donde el proceso que ejecuta herramientas no pueda leer credenciales desde filesystem, entorno, `/proc`, sockets, logs o procesos descendientes. Una API o credencial distinta requiere autorización separada y no se presume equivalente ni sin costo.
3. Restricción verificable de herramientas, hooks, MCP y subagentes del runtime elegido.
4. Verificación de runtime, cuenta/modelo y contrato real del sobre, seguida de una ejecución read-only autorizada, recibos vinculados a hashes exactos y revisión independiente.
5. Cambio explícito de política/autorización humana antes de incorporar Antigravity al consejo. La mera disponibilidad del ejecutable no debe activarlo.

Si alguno de estos puntos depende de permisos globales, cambio de identidad, nueva infraestructura o costo no autorizado, se requiere una decisión explícita antes de implementarlo.

## Recuperar el candidato aislado

Directorio: `/tmp/ia-ipanema-antigravity-h1h4-fix-20261118`.

1. Verificar `artifacts/manifest-h1h4.json` (SHA256 `90c6fc4d9a90f2c7fdfb5924ffc158a7e0815040ba4d8f555235d90136de01e8`).
2. El parche acumulado `artifacts/full-candidate.patch` debe coincidir con SHA256 `87fa69da25a220ab604b324ee55a4ae75be97dfa925a8f4e209b24fdc584e5cb`.
3. El delta H1–H4 sobre el candidato JSON anterior `8a0685f...` está en `artifacts/incremental-over-8a0685f.patch` (SHA256 `3e20abe6d62b5d4d9640382d9846f5322bde04598c89ca2f5fb9b9832c649a07`).
4. Recuperar primero en otra copia aislada y ejecutar `git apply --check` contra la base exacta. No copiar al checkout operativo ni habilitar el participante como parte de la recuperación.
5. Los resultados focalizados previos están en `artifacts/tests-result-h1h4.txt`; no son una prueba nueva del host ni una autorización de ejecución.

## Autorización futura

Cualquier intento posterior debe tener alcance específico para el entorno de aislamiento, las pruebas sintéticas y, si se satisfacen los controles, la primera llamada read-only. La integración del candidato, activación del consejo, uso de credenciales/proveedores, cambios de política y cualquier operación en Rhino requieren autorizaciones independientes.
