# Diseño propuesto: VM desechable para Antigravity

**Estado:** `needs_evidence` · diseño únicamente; no se creó ni inició una VM.

## Decisión

KVM/QEMU/libvirt están disponibles según la inspección de solo lectura ya conservada en `../antigravity-preserved-20261118/HOST-VIRTUALIZATION-REVIEW.md`. Una VM puede separar el guest del HOME, credenciales y checkout operativo del host; no resuelve por sí sola el acceso que herramientas dentro del guest puedan tener a la credencial CLI guardada allí. Por ello, el diseño no autoriza una ejecución real de `agy` ni cierra B1/B2.

V2 continúa con Claude + Codex. El candidato Antigravity permanece congelado en SHA256 `87fa69da25a220ab604b324ee55a4ae75be97dfa925a8f4e209b24fdc584e5cb`, aislado y deshabilitado.

## Capacidades y límites existentes

La inspección anterior registró Linux x86_64 bare metal, CPU Intel i7-1065G7 con VT-x/VMX, `/dev/kvm` accesible por el grupo `kvm`, QEMU, `virt-install`, `virsh` y `virt-manager` instalados, usuario en los grupos `kvm` y `libvirt`, y consultas de solo lectura a `qemu:///system` exitosas. No se probó crear o arrancar VMs ni administrar una red. La red libvirt `default` estaba activa, NAT y autoiniciable; no tenía allowlist de destinos demostrada.

En aquella medición había 7.5 GiB de RAM total y 1.18 GiB disponibles; el swap de 2 GiB estaba prácticamente agotado. El margen fue considerado insuficiente. El informe no registra espacio libre de almacenamiento. Estos valores son históricos: no certifican la capacidad actual.

## Arquitectura propuesta

```text
Host Linux — libvirt/QEMU
  ├─ checkout operativo y HOME: nunca montados en el guest
  ├─ snapshot de revisión sin secretos → ISO/disco virtual de solo lectura
  ├─ salida del guest → disco virtual desechable separado, importado tras apagar
  ├─ red dedicada: deny-by-default aplicado fuera del guest
  │    └─ solo proxy/resolver controlados; nunca NAT `default`
  └─ VM efímera
       ├─ imagen base limpia + overlay temporal
       ├─ Antigravity CLI y cuenta autenticada dentro del guest, solo tras autorización
       └─ sin carpetas compartidas, portapapeles, USB passthrough ni credenciales del host
```

### Recursos iniciales propuestos

- 2 vCPU.
- 4 GiB RAM para guest Linux con flujo de autenticación que puede requerir navegador.
- Disco virtual dinámico de 32 GiB; snapshot base limpio y overlay desechable.
- Antes de crearla, requerir una nueva lectura de memoria y espacio: como regla de operación, al menos 6 GiB de memoria disponible antes de reservar el guest (4 GiB guest más ~2 GiB de margen del host) y al menos 40 GiB libres para imagen, overlay, logs y margen. Son umbrales de diseño, no requisitos oficiales de Antigravity ni una medición actual.

Con la memoria histórica registrada (1.18 GiB disponible) el host no cumplía el umbral propuesto. Almacenamiento sigue desconocido. No se debe crear la VM hasta confirmar ambos requisitos y que el controlador libvirt/firewall tiene permisos efectivos.

## Archivos y autenticación

1. Generar un paquete de revisión con solo los archivos candidatos, dependencias permitidas y evidencia ya aprobada. Verificar el manifiesto antes de transferirlo.
2. Adjuntarlo como ISO o disco virtual de solo lectura. No usar bind mounts, virtiofs compartido, carpetas del host ni montar el checkout.
3. Separar la respuesta en un disco virtual de salida vacío. Apagar el guest antes de importar ese disco; tratar todo su contenido como no confiable y verificar hashes.
4. Si se autoriza una prueba real, el propietario inicia sesión en Google dentro del guest mediante el flujo oficial soportado por el CLI. No copiar `~/.gemini`, keyring, cookies, tokens, perfiles del navegador ni `auth.json` del host. No se ha confirmado aquí el comando exacto de autenticación; no se inventa.
5. No conservar snapshots con sesión autenticada. Para terminar, apagar la VM y destruir overlay/disco de salida; revocar la sesión Google del guest si corresponde.

**Riesgo residual B1:** la credencial creada dentro del guest puede ser legible por el usuario/proceso `agy` y por procesos de herramienta del mismo guest. VM protege el host, no a la credencial frente al propio guest. El deny-list de herramientas documentado y `--sandbox` no sustituyen prueba de que no hay shell, lectura de archivos, hooks, plugins, MCP o subagentes ejecutables. Mientras eso no se demuestre para el runtime exacto, no introducir una cuenta autenticada ni ejecutar revisión real.

## Red deny-by-default (B2)

- Crear, con autorización de administración separada, una red libvirt exclusiva para esta VM. No conectar el guest a `default`, LAN, bridge físico o sockets/servicios del host.
- En el host/hipervisor, política por interfaz `vnet` con salida e ingreso denegados por defecto; bloquear IPv4 e IPv6, UDP/443 (QUIC), DNS directo, DoT, DoH directo, IPs privadas/reservadas, loopback y link-local. No depender del firewall del guest.
- Permitir solo conexión del guest a un proxy de egreso y resolver controlados. El proxy valida destino exacto, puerto, DNS/resolución pública y redirects; vuelve a validar cada salto y registra únicamente metadatos mínimos. Sin wildcard global de dominios.
- La lista de endpoints oficiales de inicio de sesión e inferencia de Antigravity no está cerrada en esta fase. Debe obtenerse de documentación compatible y capturas de una prueba expresamente autorizada. Hasta entonces, el proxy queda sin destinos externos permitidos y la prueba de proveedor bloqueada.
- Una allowlist de hostname no protege contra exfiltración a través de un endpoint permitido si un proceso con herramientas puede emitir tráfico arbitrario. B1 (herramientas deshabilitadas/procesos segregados) y B2 deben satisfacerse conjuntamente.

No se cambió ninguna regla de red, firewall o configuración del host. La pertenencia a `libvirt` no demuestra permisos de administración de firewall.

## Pruebas sintéticas futuras (sin proveedores)

Ejecutar solo después de autorización para crear/configurar la VM y red de prueba:

1. **Frontera de archivos:** guest no puede enumerar/leer HOME, keyring, `/proc` sensible ni rutas del host; paquete candidato llega solo por medio de solo lectura y sus hashes coinciden.
2. **Canario ficticio:** colocar secreto aleatorio ficticio en ruta de autenticación dentro del guest; ejecutar probes adversariales de procesos de herramienta/subagente/hooks/MCP y verificar denegación y ausencia del canario en stdout, stderr, entorno, archivos de salida y logs. Si el ejecutor de herramientas comparte UID/acceso y puede leerlo, B1 falla y se detiene.
3. **Egreso:** servicios de prueba locales simulando destino permitido y prohibido; probar DNS, IPv4/IPv6, IP directa, redirects, TLS, UDP/443, DNS alternativo y destinos privados. Verificar denegación desde el host y recibos de firewall/proxy. Esto no prueba endpoints de Google.
4. **Proceso/cancelación:** iniciar proceso hijo sintético, cancelar la unidad/VM de prueba y comprobar que no quedan descendientes.
5. **No persistencia:** destruir overlay y comprobar que el snapshot base sigue limpio; ninguna salida se copia al repo operativo.

Estos casos prueban límites de infraestructura y harness sintético. No demuestran que `agy` en la versión instalada no invoque una superficie de herramienta ni que preserve el contrato real de autenticación. Para eso haría falta una prueba separada con CLI/runtime real, credencial de prueba autorizada y proveedor; sigue prohibida en esta fase.

## Secuencia de implementación futura

1. Autorizar y medir capacidad actual (RAM/almacenamiento) y permisos efectivos de libvirt y firewall.
2. Autorizar creación de imagen base limpia, VM efímera y red aislada; no tocar la red `default`.
3. Probar el canal de entrada/salida y el firewall solo con canarios y servicios sintéticos.
4. Revisar el `settings` deny-list y las superficies disponibles para tools/hooks/plugins/MCP/subagentes. Si no se puede imponer un bloqueo efectivo y verificarlo, detenerse sin autenticación.
5. Cerrar lista exacta de dominios de autenticación/inferencia y reglas de proxy. La revisión real permanece bloqueada hasta pasar B2 sin bypass.
6. Con una autorización independiente, propietario autentica una cuenta dentro del guest y se ejecuta una única revisión read-only del snapshot congelado. No integrar V3; conservar recibos y destruir la sesión/overlay al cerrar.

### Permisos requeridos para esa fase

- Operación de libvirt para crear y destruir dominio/red/volúmenes de prueba.
- Privilegio administrativo acotado para instalar reglas de egreso por interfaz y proxy/resolver, o un administrador que lo ejecute con el manifiesto revisado.
- Sin permisos de publicación, checkout operativo, cliente o tienda.
- Autorización separada para iniciar sesión Google en el guest y, más adelante, invocar el proveedor.

## Estado

| Control | Estado |
|---|---|
| KVM/QEMU/libvirt instalados y acceso de lectura | Comprobado históricamente |
| Recursos suficientes ahora | No comprobado; última lectura insuficiente |
| Almacenamiento libre suficiente | Desconocido |
| VM desechable creada | No |
| Snapshot/repo aislados | Diseño; no probado |
| Autenticación Google dentro del guest | Pendiente; ninguna credencial consultada |
| Credencial inaccesible a tools dentro del guest (B1) | No demostrado; bloqueante |
| Egreso externo por destino (B2) | No configurado ni demostrado; bloqueante |
| V2 Claude + Codex | Sin cambios; sigue operativo |
| Antigravity/V3 | Congelado, deshabilitado; `needs_evidence` |

**Resultado:** diseño listo para revisión y autorización de la fase de preflight de recursos/infraestructura, pero no es seguro preparar una VM autenticada todavía. No instalar, crear o iniciar infraestructura con la autorización actual.
