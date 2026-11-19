# Bootstrap V3 security implementation — bloqueada en preflight

Estado: **`needs_evidence`**. La implementación se detuvo antes de editar archivos por dos bloqueos de seguridad. No se invocaron Claude, Codex ni APIs de inferencia; no se usaron credenciales reales; no se integró el parche ni se modificó el candidato V3.

## Alcance autorizado y resultado

Se autorizó una implementación local aislada de credential broker, egreso deny-by-default, gate read-only y prompt preflight, con pruebas sintéticas. El preflight reveló que no es seguro comenzar la implementación integrada en el entorno disponible. Se preserva la autorización para un siguiente intento cuando se resuelvan los bloqueos; no se interpreta como permiso para cambiar de identidad o habilitar una vía incompleta.

## Bloqueos observados

### B1 — No hay enforcement de egreso por destino disponible para este sandbox

- `unshare -n true` terminó con `Operation not permitted`.
- `nft list ruleset` no pudo leer netfilter: requiere privilegios de root.
- `iptables -S` no pudo consultar reglas: permiso denegado.
- Bubblewrap está instalado, pero solo se verificó el modo de red completamente deshabilitada. Eso no limita un broker conectado a la red a una allowlist de destinos.
- El sentinel anterior probó que un worker sin red no llega al loopback. No prueba que un broker con red no pueda contactar un destino prohibido.

Por tanto, una allowlist implementada solamente en código HTTP no cumpliría el requisito de egreso verificable frente a un fallo o compromiso del proceso. No se implementó ni se certificó como control de seguridad.

### B2 — El transporte actual acopla credencial y proceso con herramientas

- `isolation.py:command` acepta `auth_files` y los monta con `--ro-bind` dentro de `/worker-home`.
- La reproducción sintética anterior leyó el canario ficticio desde ese montaje. Es una falla reproducida del diseño existente; no se leyó ningún secreto real.
- `engine.py:runtime_defaults` prepara esos montajes para las CLIs actuales. Retirarlos impide la autenticación de ese transporte.
- Un broker separado requeriría un protocolo de inferencia/auth que no está implementado ni acreditado como equivalente a la identidad CLI de Claude Code y Codex. Pasar un token en el entorno del worker tampoco satisface la prohibición de secretos heredados.

No se sustituyó CLI por API ni se introdujo una identidad distinta. Hace falta una decisión explícita sobre identidad/protocolo y un transporte compatible cuyo trabajador no tenga herramientas ni acceso al secreto.

## Inventario de código observado (sin modificaciones)

Checkout aislado: `/tmp/ia-ipanema-contract-separation-20261117/repo`

| Archivo | SHA256 observado |
|---|---|
| `tools/ipanema/orchestration/isolation.py` | `0d734fcbf6d10e839d2a7cb46f3416ca60f0751e1491974d73186a8d56408079` |
| `tools/ipanema/orchestration/engine.py` | `927a9292bd997c7f8ce4c04dc1b331b5d29620a3d52d79a0f8f280febadff496` |
| `tools/ipanema/orchestration/adapters.py` | `bae25bee06cf7574ee35f65e9f9055dfa8a495336f80615165ddd5232359d01d` |

No se editaron esos archivos. El árbol operativo no recibió cambios de código por esta tarea.

## Componentes no implementados ni certificados

Debido a B1/B2 se detuvo antes de implementar cualquiera de los cuatro bloques, para no producir controles parciales que aparenten seguridad:

- Credential broker real o integración con un proveedor.
- Restricción de salida a nivel de sistema/broker y pruebas allowed/denied bajo enforcement OS.
- `review_gate` read-only verificable por el controlador operativo.
- Serialización/preflight final integrada antes de reservar o iniciar un proveedor.

No se ejecutaron pruebas de implementación. Las pruebas sintéticas previas del paquete de diseño siguen siendo evidencia del estado anterior, no aprobación de esta implementación.

## Siguiente paso necesario

Resolver ambos bloqueos antes de reanudar:

1. Proporcionar un entorno aislado que permita imponer y probar reglas de egreso a nivel sistema (o un servicio externo administrado con política deny-by-default, logs y pruebas sentinel permitidas/prohibidas), sin dar acceso general al worker.
2. Acordar el mecanismo y la identidad de cada revisor. Si requiere API en vez de CLI, confirmar esa sustitución de identidad explícitamente; de lo contrario, aportar un broker oficialmente compatible con el flujo CLI y una prueba ficticia de que el worker no puede leer credenciales.
3. Después, retomar el alcance autorizado en otra copia limpia, con pruebas unitarias/sintéticas y sin llamadas reales. El estado seguirá `needs_evidence` hasta revisión e integración por separado.

## Evidencia de este preflight

Los comandos y resultados observables están en [evidence.json](evidence.json). El manifiesto cubre ambos archivos del informe y su evidencia. Esta entrega no representa un candidato ni un parche.
