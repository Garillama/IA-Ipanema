# Control del tema, editor y plataforma

Fecha: 2026-11-08. Estado local/remoto explicado en [resumen](../00-executive-summary.md); no se ejecutaron escrituras remotas.

| Necesidad | Camino comprobado | Límite y coste |
|---|---|---|
| Orden, inclusión, ocultamiento y settings | Editor o `templates/**` JSON | Datos de cada tienda; no sincronizar una copia vieja sobre cambios del comerciante |
| Identidad de marca | `config/settings_data.json` con schema global | No todos los controles son globales; los de sección pueden prevalecer |
| CSS propio sin cambiar core | `css_code` y bloque de código encontrados | Carga global/cascada o HTML embebido; no convertirlo en una capa creciente de parches |
| Nuevo archivo de sección/bloque o editar Twig | Código fuente con fork | Aumenta responsabilidad de mantenimiento y compatibilidad |
| Cambiar JS/CSS core, layout o traducciones | Fork y CLI | Requiere revisar actualización de base y regresiones |
| Metadatos del head | Plataforma a través de `head-tags` | El tema coloca el componente; no controla libremente su implementación |
| Precio, stock, envíos y pago | Datos y runtime de Tiendanube | Reutilizar lógica existente; no calcular reglas de negocio paralelas |
| UI de app | Nube SDK en slots y APIs documentadas | Sin acceso arbitrario a DOM; disponibilidad depende de superficie/tema |
| Checkout | Branding soportado y extensiones SDK permitidas | No es una plantilla de página controlada libremente por el tema |
| Indexación HTTP, robots, redirecciones | Plataforma y configuración del servicio | No se encontraron archivos locales que implementen esos endpoints |

La documentación actual distingue personalización de datos sin fork y modificación de source con fork. Los datos se conservan mediante el modelo de actualizaciones; un fork requiere gestionar cambios de código. Ver [guía del CLI](https://tiendanube.dev/themes/developer-tools/cli/sectionable-theme-development) y [fork/versionado](https://tiendanube.dev/es-AR/themes/sectionable-themes/forking). No se promete que una actualización preserve código modificado ni que pueda revertirse un fork en el lugar.

`theme update`, `unfork`, `fork`, `watch`, `push`, `publish`, `create`, `clone` y `delete` cambian estado; no son comprobaciones. `theme diff` es lectura, pero su alcance sigue exclusiones y reglas de fork. `check` valida los archivos que enviaría un push, no necesariamente todos los archivos iguales. Consultar [CLI](../09-integrations/theme-cli.md).

Las skills previas del proyecto contienen datos históricos que contradicen fuentes actuales: por ejemplo, un límite de dos instalaciones y la posibilidad de enviar `custom/` con CLI no se deben aplicar sin verificar. La lectura actual del servidor informa `max_installations: 21` para esta cuenta; no es un límite universal. La documentación actual indica que el CLI no envía `custom/` todavía. [Evidencia remota](../13-evidence/measurements/source-baseline/remote-themes.json).

No se inspeccionó Admin autenticado, permisos de cuenta, aplicaciones instaladas ni su consentimiento. No se verificó importación/exportación de bibliotecas arbitrarias desde el editor. No se accedió a cuentas de clientes, pedidos o checkout.
