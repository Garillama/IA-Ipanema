# Tiendanube: producción como referencia, cambios locales

Procedimiento vigente para DaMar Beauty por instrucción del usuario: **usar 14748767 como referencia publicada; no crear clon ni cambiar de instalación**. El CLI puede trabajar con borradores y preview, pero esa alternativa no está autorizada ni se usa. Se ejecutó después un único push del CSS, autorizado específicamente; no se ejecutaron clone, watch, publish, fork o pull.

## Identidad y sincronización verificadas

Tiendanube CLI **2.5.1**. La lectura nativa confirmó tienda **8408995**, `https://damarbeauty.mx`, Ipanema `Clothing-2`, versión **1.7.0**, instalación **14748767**, publicada y forked. La copia externa está configurada en `projects/damarbeauty.local.json`; su manifest y `theme current` apuntan a 14748767. El `theme_id` del CLI identifica la instalación; `base_theme=ipanema` es el tema base.

Existe un borrador 14708020, versión 1 y no productivo. Se conserva intacto y no es la referencia de esta tarea. La tienda tiene 2 de 21 plazas usadas; no se consumió ninguna adicional.

Lecturas ejecutadas:

```bash
tiendanube theme current
tiendanube theme list --json
tiendanube theme diff --theme-id 14748767 --json
tiendanube theme diff --theme-id 14748767 --json --detailed
```

Resultado del diff real: **468 archivos iguales, uno modificado, cero añadidos, cero borrados, cero fallos de lectura y cero skips**. El único distinto es `static/css/damar.css`, por el ajuste local de objetivos táctiles de esta tarea. Las lecturas no sobrescribieron el árbol local. Ese era el estado anterior al push. Tras la operación autorizada, el diff nativo confirmó 469 iguales y cero diferencias: evidencia `20261109T201038-postpush-native-diff-4a522a34/verification.json`.

Evidencia: `reports/runs/damarbeauty/20261109T193707-production-reference-dc7d2bcf/` y `reports/runs/damarbeauty/20261109T193921-production-exact-diff-577f2b83/`. La referencia está registrada en `projects/damarbeauty.json` con fecha y origen de observación; no se transfirió evidencia histórica de otra instalación.

## Punto de recuperación

Se guardaron HEAD Git y SHA-256 de 469 archivos de fuente, excluyendo credenciales. El intento local `c79e18cd0f5846338e875a76512204c7` conserva contenido previo y hashes de `static/css/damar.css`, en un backup privado ignorado.

Se revirtió el patch nativo **en una carpeta temporal**, sin tocar el tema local, y el SHA-256 reconstruido coincidió con el backup anterior. El patch JSON del CLI carecía de salto final de línea: se añadió únicamente ese salto a una copia para comprobarlo con `git apply --reverse --check`; los hunks no se cambiaron. Evidencia: `reports/runs/damarbeauty/20261109T194114-production-rollback-proof-146b7737/verification.json`.

Diff de tarea y reversión: `reports/runs/damarbeauty/20261109T193827-footer-review-039b20ec/`. El backup de CSS reconstruido está en `.local/access/backups/damarbeauty/14748767/20261109T1940/`, modo 0600. No incluye `.nuvem`, tokens o cookies.

Para revertir **solo el intento local**, si el archivo aún conserva el hash propio:

```bash
python3 tools/ia.py --project damarbeauty attempt revert c79e18cd0f5846338e875a76512204c7
```

No usar reset, clean, stash o pull. El intento quedó aceptado después del QA publicado, limitado al footer. El comando de reversión de arriba documenta el mecanismo para intentos aplicados; no debe ejecutarse sobre este intento ya aceptado. Cualquier reversión futura requiere un nuevo plan por hash y autorización específica de escritura remota.

## Investigar y preparar cambios

1. Elegir explícitamente `--project damarbeauty` y comprobar referencia, hashes y consumidores actuales.
2. Usar el gateway y permisos de tarea para Claude/Codex/CommandCode. No entregarles `.nuvem` o credenciales Google; el broker del controlador media las lecturas. Los resultados no autorizan escrituras remotas.
3. Comparar con 14748767 mediante diff nativo de lectura, con la guardia de no reintentos ante 403/429. No sobrescribir la copia local para igualarla.
4. Declarar archivos y preservar baseline/backup antes de editar. Revisar componentes nativos, consumidores directos/transitivos y cascada; no modificar archivos ajenos a la tarea.
5. Analizar SEO, responsive, accesibilidad y rendimiento. Reutilizar helpers, motores y contratos de la tienda; no replicar lógica comercial.
6. Ejecutar QA local proporcional y conservar fallos reales. Preparar diff exacto y reversión por hash. Separar fuente comprobada, propuesta y comportamiento renderizado.

Caso actual: `blocks/damar-footer-help.tpl` produce los enlaces, `sections/footer.tpl` los compone y `layouts/layout.tpl` carga `static/css/damar.css`. Se modificó la regla existente `.section-footer .damar-footer-support__column a`: `inline-flex`, alineación y altura mínima de 24 px. No cambian URLs, textos, stock, precios, formularios, estructura SEO o JavaScript. Aumenta el área clicable y puede aumentar la altura del footer en sus consumidores, por lo que requiere comprobación renderizada en móvil/escritorio.

## Qué se puede verificar sin sincronizar

El perfil `audit` obtuvo HTML inicial, DOM, recursos descargados y Lighthouse de producción. Axe detectó `target-size` en WhatsApp/email del footer, además de otros fallos independientes. El SEO de la muestra analizada produjo cero errores y 18 hallazgos; no es evidencia de indexación. El inventario/schema local y diff checks pasaron.

La instalación publicada **no renderiza un CSS que solo existe localmente**. Abrir `?theme_installation_id=14748767` seleccionaría esa misma instalación publicada; no crea un sandbox ni aísla cambios futuros. Un servidor estático, una sustitución de CSS o un Twig improvisado no se presentarán como render real de Tiendanube.

Por elección de trabajar sin clon, comprobar el efecto nativo del cambio exige subirlo a 14748767: será visible para clientes. En esta tarea esa operación se autorizó después y se verificó en la instalación publicada; la simulación previa de CSS no se contó como render publicado. Ninguna variación de LCP/TBT entre mediciones anteriores se atribuye a este CSS local.

## Antes de una operación remota autorizada

Este procedimiento no concede autorización permanente de push, publish, fork, pull o watch. La aprobación específica de un único CSS se consumió en esta tarea. Cada solicitud futura debe indicar operación, tienda, instalación, archivos, hashes, diff y riesgos. Antes de un push, volver a leer el estado publicado y el diff; si cambió el ID, el CSS, el backup o aparecen otros archivos, detenerse.

El comando nativo que se sometería a aprobación para este caso es:

```bash
tiendanube theme push --theme-id 14748767
```

Se ejecutaría únicamente después de autorización expresa para producción y con [la guardia por proceso](../../tools/theme_api_guard.mjs), modo `production-push`, destino y publicado `14748767`, archivo permitido `static/css/damar.css` y SHA-256 exacto del contenido aprobado. La guardia de `push` normal rechaza el ID publicado. Ningún modo publica temas, borra archivos o autoriza una operación por sí solo.

El CLI no tiene push de un archivo mediante flag: compara el árbol completo. El permiso de la guardia limita la validación/upsert al único CSS con hash aprobado, sin borrados ni otros archivos. Evitar `--force`, `--published`, FTP y cualquier sincronización automática. `-y` solo se usa para una operación específica ya autorizada, no para obtener permiso.

Se inspeccionó que 2.5.1 reintenta timeout/429/503 hasta seis veces. La guardia impide repetir creaciones/escrituras inciertas y detiene 403/429. Sus restricciones se probaron con transporte simulado identificado y su carga real se comprobó en `theme list` de lectura. Después se usó en la única escritura autorizada de producción: retorno exitoso y diff posterior completamente sincronizado.

**`watch` sube al guardar/crear/borrar. `--no-browser` no desactiva esa subida. Nunca se ejecuta dentro de este procedimiento.** `pull` sobrescribe archivos locales y tampoco se usa para investigar sincronización. `publish` y `fork` son mutaciones diferentes, excluidas de un permiso de push.

## Después de un push, si se autoriza

Comprobar aceptación real del único archivo; exit 0 no sustituye el resultado de updated/skipped ni la lectura posterior. Ante respuesta incierta o denegación, detenerse sin repetir. Verificar el CSS descargado, hash/versión y estilo calculado antes de atribuir resultados al cambio.

Repetir los perfiles de auditoría con iguales viewport, red, CPU, caché, versión, recursos permitidos y máscaras explícitas; contrastar HTML/DOM, responsive, enlaces, axe y SEO. Conservar fallos previos no relacionados y posibles regresiones. El CSS de objetivos táctiles no justifica afirmar mejoras de velocidad o indexación.

Si hay regresión, restaurar el CSS remoto respaldado **solo si también se autorizó específicamente ese rollback**, con su hash y alcance, y comprobarlo después. No borrar instalaciones ni cambiar de tema. Sin autorización de restauración, parar y entregar evidencia.

## Reutilización

En futuras tiendas repetir identificación y comparación nativas; nunca reutilizar IDs, credenciales o supuesta compatibilidad de DaMar. Mantener producción como referencia de lectura y cambios locales revisables. Una instalación de prueba solo se consideraría si el usuario cambia explícitamente esta decisión. El CLI y sus fuentes distribuidas son la referencia primaria de comandos; sus capacidades no equivalen a autorización para ejecutarlas.

## Cierre de la operación autorizada — 9-11-2026

Se comprobaron diff/hash exactos, ausencia de modificación remota del CSS, respaldo íntegro y diferencias responsive esperadas antes de ejecutar una única invocación de `theme push` con la guardia. Solo se permitió `static/css/damar.css`; no hubo borrados u otros archivos. El asset publicado y seis casos de footer confirmaron el cambio: +16 px en home/PDP móvil, +20 px en categoría móvil, sin cambio de altura desktop. No hubo regresión atribuible ni rollback.

Evidencia y pendientes reales: [verification.md](verification.md). La aceptación es específica de este CSS; persisten hallazgos previos de SEO/accesibilidad. Para futuras tareas hay que repetir identificación, hashes, backup, revisión y autorización específica: no reutilizar esta aprobación.
