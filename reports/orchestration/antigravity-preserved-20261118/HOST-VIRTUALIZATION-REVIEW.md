# Antigravity H1–H4 — copia preservada y evaluación de virtualización

Estado: `needs_evidence`. V2 continúa con Claude + Codex; Antigravity permanece aislado/deshabilitado. Esta copia preserva un candidato revisable y no cambia el controlador operativo.

## Identidad y recuperación

- Parche acumulado: SHA256 `87fa69da25a220ab604b324ee55a4ae75be97dfa925a8f4e209b24fdc584e5cb`.
- Base Git observada en el checkout candidato: `b91a85445cb750d5f6482c936cf631919242b5c1`.
- El conjunto de archivos del candidato está en `candidate-files/`; los parches, manifiestos, recibos de pruebas y documento de cierre están en `artifacts/`.
- Para recuperar: copiar esta carpeta a una nueva copia de trabajo, verificar `artifacts/preservation-manifest.json`, aplicar `artifacts/full-candidate.patch` con `git apply --check` contra el commit base exacto y revisar el diff. No copiar archivos al controlador operativo ni activar Antigravity.

## Virtualización: lecturas del host

- Host Linux x86_64; `systemd-detect-virt` indicó `none` (no parece estar dentro de una VM). CPU Intel i7-1065G7, VT-x y VMX presentes.
- `/dev/kvm`: `root:kvm`, modo `0660`; el usuario pertenece a `kvm`.
- QEMU (`qemu-system-x86_64`), `virt-install`, `virsh` y `virt-manager` están instalados. El usuario pertenece a `libvirt`; la conexión `qemu:///system` respondió a consultas de solo lectura. No se probó crear, arrancar ni modificar VMs.
- Libvirt muestra dos dominios apagados (no se registra aquí su nombre) y una red `default` activa, persistente y autoiniciable. No se observó una red de salida con allowlist por destino.
- CPU lógico: 8. Memoria: ~7.5 GiB total, ~1.18 GiB disponible al medir. Swap: 2 GiB total, ~0.5 MiB libre. El margen actual es insuficiente para recomendar un guest de agente sin liberar recursos y volver a medir en una fase autorizada.

## Evaluación B1/B2

**B2 — red:** KVM/libvirt permitirían diseñar una red dedicada para un guest, pero la red NAT `default` observada no prueba restricción de destinos. Haría falta una política de egreso impuesta fuera del guest (hipervisor/host o red administrada), con allowlist de endpoints, control DNS/IPv4/IPv6 y pruebas permitidos/prohibidos. El firewall solo dentro del guest no basta como frontera frente a un proceso con herramientas que pueda modificarlo. No se configuró ninguna red o regla.

**B1 — credenciales:** la VM separaría el guest de los archivos del host, pero no separa por sí sola la credencial CLI de un `agy` con herramientas: el runtime y los procesos de herramientas podrían compartir usuario/espacio de archivos, y el estado de autenticación reside en el contexto del CLI. Hace falta demostrar un modo oficialmente soportado de `agy` sin herramientas/hooks/MCP/subagentes, o una separación broker/ejecutor compatible con la identidad CLI. Ninguna quedó acreditada. No se inspeccionaron ni usaron credenciales reales.

**Conclusión:** la virtualización está disponible, pero no resuelve automáticamente B1/B2. B2 parece técnicamente abordable mediante configuración administrada de red en el hipervisor; B1 sigue dependiendo de una frontera de autenticación/herramientas aún no probada. No hay base para ejecutar proveedores ni para afirmar habilitación segura.

## Camino mínimo futuro

1. Liberar recursos y, con autorización separada, diseñar un guest dedicado; no usar la red NAT por defecto para una ejecución real.
2. Acreditar primero el modo de herramientas cero de `agy` o un broker oficialmente compatible que mantenga intacta la identidad CLI y deje los workers sin credencial. Si no existe, detenerse; cambiar a API requiere consentimiento separado y evaluación de costo/identidad.
3. Solicitar autorización de administración para una red aislada con egreso denegado por defecto y allowlist impuesta en el host/hipervisor. Probar controles con servidores sintéticos: destino permitido, destino prohibido, DNS, IPv4/IPv6, redirects y cancelación de descendientes.
4. Auditar estáticamente el guest y demostrar que tools, plugins, hooks, MCP y subagentes no acceden a secretos. Solo después podría pedirse autorización específica para una única revisión read-only real.
5. Mantener V2 dual como default. Cualquier cambio de política para triada, prueba real de proveedor, integración del candidato o activación requerirá autorización separada.

No se instalaron paquetes, crearon VMs, cambiaron permisos/firewalls ni ejecutaron agentes. No se repitieron los diagnósticos históricos B1/B2.
