# Antigravity VM — preflight local de recursos y permisos

**Estado:** `needs_evidence` · solo lecturas locales · no se creó ni inició VM.

## Identidad conservada

Diseño de referencia: `reports/orchestration/antigravity-vm-design-20261118/README.md` (SHA256 `2a3d34317bc2787e902488324e5c6a48381f65c5018a42fae8983331048e58ed`).

Se conserva V2 (Claude + Codex) y el candidato Antigravity congelado `87fa69da25a220ab604b324ee55a4ae75be97dfa925a8f4e209b24fdc584e5cb`. No se inició `agy`, no se usaron credenciales, no se invocaron modelos, no se elevó privilegio y no se modificaron red, firewall, libvirt ni el controlador.

## Resultados observados

| Control | Lectura actual | Evaluación |
|---|---|---|
| RAM | 8,090,230,784 bytes total (~7.53 GiB); 1,284,833,280 bytes disponibles (~1.20 GiB) | **Insuficiente** para la reserva propuesta |
| Swap | 2,147,479,552 bytes total; 2,147,151,872 usados (~99.98%) | No usar como sustituto de RAM |
| Disco de imágenes `/var/lib/libvirt/images` | `/dev/sda2`, ext4; 200,302,858,240 bytes libres (~186.6 GiB) | Supera el umbral de diseño de 40 GiB |
| Pool libvirt `default` | 438.55 GiB capacidad; 208.89 GiB disponibles | Capacidad suficiente según pool; se conserva el valor de `df` como cifra conservadora para el path comprobado |
| CPU/KVM | x86_64, 8 CPU lógicos, flag `vmx`; `/dev/kvm` `root:kvm` 0660 con ACL; lectura y escritura reportadas, apertura `O_RDWR` exitosa | Acceso KVM efectivo comprobado para el usuario |
| QEMU/libvirt | libvirt 10.0.0, QEMU 8.2.2; conexión `qemu:///system` funcional; socket `libvirtd` activo; QEMU/libvirt instalados | Capacidad instalada y conexión comprobadas; no se creó ni arrancó VM |
| Dominios existentes | `linux2024` y `SERVER2016`, ambos apagados | No se modificaron |
| Permiso libvirt | Usuario pertenece a `libvirt`; socket system `root:libvirt` 0660; regla Polkit local concede `org.libvirt.unix.manage` a ese grupo | **Permiso de gestión libvirt concedido por política**; no se probó una operación de escritura por la restricción read-only |
| Firewall | `nft` e `iptables` instalados; UFW figura activo; `firewalld` y unidad `nftables` inactivos | Herramientas instaladas/servicio declarado activo, pero reglas efectivas no visibles desde este usuario |
| Lectura de reglas | `ufw status` exige root; `nft list ruleset` e `iptables -S` devolvieron `Operation not permitted` | No se puede acreditar allowlist ni deny-by-default actual |
| Redes libvirt | `default` es NAT (`virbr0`, `192.168.122.1/24`) | No sirve como evidencia de filtrado por destino |
| Posible red `Descargas` | Apareció en una lectura de listado, pero su XML no pudo obtenerse; la lectura posterior por UUID mostró solo `default` | Resultado inconsistente; no contar como red existente ni aislada |

### Umbral del diseño

El diseño propone 2 vCPU, 4 GiB RAM y disco dinámico de 32 GiB. Como umbral operativo se había fijado al menos 6 GiB disponibles antes de reservar el guest (4 GiB para VM y ~2 GiB para el host) y 40 GiB libres en almacenamiento. Son márgenes de diseño, no requisitos oficiales del producto.

- CPU disponible: 8 lógicos; 2 vCPU son plausibles, sujeto a carga concurrente.
- Disco: sí supera el margen propuesto.
- RAM: no; faltan aproximadamente 4.8 GiB para el umbral de 6 GiB y el swap está casi lleno.
- Resultado: **no se recomienda ni se autoriza crear ahora la VM**. La falta de RAM basta para detenerse.

## Permisos: capacidad instalada vs. operación demostrada

- **Libvirt:** el usuario está autorizado por la regla Polkit `60-libvirt.rules` para conectar en modo de gestión al socket system. La conexión y consultas funcionan. No se intentó definir/start un dominio ni crear/activar una red; por tanto, no se afirma que cada operación concreta esté probada.
- **Firewall:** hay binarios y UFW aparece activo, pero el usuario no pudo leer la política efectiva. Pertenecer al grupo `sudo` no se trató como elevación ni como prueba de acceso; no se solicitó ni usó sudo. No hay permiso efectivo de administración del firewall demostrado bajo el alcance actual.
- **Red aislada:** no existe una red aislada verificada. No usar `default` NAT ni la mención inconsistente de `Descargas` como sustituto.

## Mecanismo recomendado para deny-by-default

Una red libvirt dedicada para la VM, filtrada fuera del guest mediante reglas de host gestionadas por administrador (preferentemente nftables sobre la interfaz `vnet` correspondiente) y un proxy/resolver controlados. Denegar todo ingreso y egreso por defecto; permitir desde guest únicamente el proxy. El proxy solo habilitaría FQDN oficiales exactos después de documentar los destinos de autenticación/inferencia. Bloquear salida directa IPv4 e IPv6, DNS externo, DoT/DoH directo, QUIC, IP privadas/reservadas y redirects a destinos no aprobados. Las reglas deben persistir y asociarse de forma segura al ciclo de vida de la VM.

Esto es un diseño, no una regla instalada. Los endpoints de autenticación/inferencia no están aprobados ni cerrados; la allowlist no puede configurarse todavía. Además, una allowlist por hostname no evita por sí sola exfiltración hacia un destino permitido si dentro del guest corre un proceso con herramientas.

## Controles requeridos antes de credenciales

1. Liberar recursos y obtener una lectura fresca de RAM, swap y disco justo antes de provisionar; cumplir los umbrales fijados.
2. Autorizar por separado la creación de VM/red y la administración host requerida. El diseño de red debe revisarse antes de cualquier cambio.
3. Probar con servicios/canarios sintéticos la denegación exterior, allowlist controlada, DNS, IPv4/IPv6, IP directa, redirects, TLS, puertos alternos y cancelación de descendientes; revisar evidencia del firewall desde un administrador autorizado.
4. Adjuntar el snapshot como medio realmente de solo lectura; sin HOME, keyring, credenciales, checkout operativo, carpetas compartidas, clipboard, USB passthrough o sockets del host.
5. Probar un canario ficticio contra shell, lector de archivos, hooks, plugins, MCP y subagentes. Si cualquier herramienta/proceso puede leer credenciales que serían usadas por `agy`, B1 sigue bloqueante. La VM no protege credenciales de procesos dentro de ella.
6. Solo con B1/B2 aprobados y una autorización separada, el propietario establece una sesión Google nueva dentro del guest mediante flujo oficial. No copiar el token del host ni guardar snapshots/discos autenticados.

## Condiciones exactas para una futura autorización de creación

- Lectura reciente demuestra ≥6 GiB disponibles, swap no bajo presión y ≥40 GiB libres en el volumen elegido.
- Aprobación explícita para crear un dominio de 2 vCPU/4 GiB/32 GiB dinámicos y sus volúmenes desechables.
- Política explícita que autoriza crear una red dedicada y reglas de host; identificar quién tiene privilegio administrativo y cómo se revisarán las reglas.
- Especificación aprobada de entrada/salida de archivos y destrucción de overlay.
- Ninguna red existente se presume segura por estar activa o por usar NAT.
- La creación de infraestructura no autoriza autenticación, `agy -p`, proveedores, integración V3 ni cambios en Rhino.

**Conclusión:** almacenamiento, CPU, KVM y permiso general de gestión libvirt están disponibles; RAM no cumple y filtrado host no es verificable con permisos actuales. Detenerse sin alternativas automáticas. B1/B2 permanecen `needs_evidence`.
