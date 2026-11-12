# Menú «Más información» — procedimiento preparado, no ejecutado

**Suspendido por la instrucción posterior del propietario:** no modificar menús ni añadir enlaces. «Sobre Rhino Performance» está pendiente de contenido y no debe promocionarse. El procedimiento siguiente se conserva como historial; no es una operación pendiente de ejecución ni una autorización vigente. Véase la [continuación de rastreabilidad](../../site-continuation/README.md).

Tienda Rhino Performance. Instalación publicada de referencia14828608. Identificador del menú en el tema: `footer`. No crear un menú nuevo, no editar Menú principal y no reasignar el bloque del footer.

## Vías oficiales comprobadas

La CLI instalada solo ofrece operaciones de temas y skills. No ofrece lectura/exportación/edición de menús. El catálogo público de [recursos Admin API](https://tiendanube.github.io/api-documentation/resources) consultado no documenta un recurso Menu/Navigation con CRUD. Existe el evento [navigation/updated](https://tiendanube.github.io/api-documentation/resources/webhook), pero una notificación de cambio no proporciona un endpoint para descargar ni modificar el menú. No se instala una app ni se reutilizan credenciales de temas/GSC como credenciales administrativas.

La [referencia Twig](https://tiendanube.dev/es-AR/themes/twig-reference/objects) expone `menus` para renderizar nombres, URLs e hijos, no un exportador administrativo completo. No se construye un endpoint de debug para exponer esos datos desde producción.

La ayuda oficial describe edición desde [Tienda en línea > Menús](https://ayuda.tiendanube.com/es_MX/123259-menues/como-editar-el-menu-principal-de-navegacion) y [menú inferior](https://ayuda.tiendanube.com/es_MX/123259-menues/como-cambiar-el-menu-inferior-de-mi-tienda). No encontré una exportación de menús con IDs documentada en esas fuentes. Eso no demuestra que todas las cuentas carezcan de alguna función adicional: hay que verificarlo dentro del administrador autorizado.

## Antes de pedir autorización de aplicación

1. El propietario abre el administrador de Rhino y entra en **Tienda en línea > Menús**. Solo lectura en esta fase. Abrir el menú ya seleccionado por el footer; comprobar su nombre real, no inferir que su título administrativo coincide con «Más información».
2. Comparar los cuatro elementos de la tabla siguiente, en ese orden, con sus URLs completas. Revisar tipo de enlace, subniveles, destino en misma/nueva pestaña si el editor lo muestra, y cualquier otro campo existente. Si hay diferencias o elementos adicionales, detener: la captura pública anterior no autoriza sobrescribirlos.
3. Guardar un registro local del menú completo antes de editar: fecha/cuenta/menú, etiquetas, URLs exactas, orden, jerarquía, tipo y opciones visibles. Registrar sus identificadores si el panel los muestra. Si existe exportación oficial, preferirla. Complementar con captura/PDF local del panel. No guardar cookies, cabeceras, contraseñas, HAR de sesión ni tokens.
4. Si los IDs no están disponibles, escribir expresamente «no expuestos por el administrador»; no inventarlos ni llamar respaldo completo con IDs a una transcripción parcial. El propietario solicitó preparar la reversión manual con esa limitación: identificar cada entrada por menú concreto, nombre, URL, orden, jerarquía y todos los campos visibles. Esto no significa que el respaldo ya exista ni autoriza editarlo. La autorización manual final debe vincularse al respaldo real revisado.
5. Comprobar que no existen ya las dos URLs normalizadas, incluso con otra etiqueta, barra final o variante absoluta/relativa. Confirmar sus títulos en las lecturas200 conservadas: **Contacto - RHINO Performance** y **SOBRE RHINO PERFORMANCE**; canonical propio. No repetir Google Inspection para preparar esta operación.
6. Conservar el archivo local fuera de Git y calcular su SHA256. Vincularlo a la autorización; un template o una captura del storefront no reemplazan el respaldo administrativo.

| Orden actual que se conserva | Etiqueta | URL |
|---|---|---|
|1|Aviso de privacidad|https://rhino-performance.com/aviso-de-privacidad/|
|2|Cambios y garantía|https://rhino-performance.com/politica-de-reembolso-y-cambios/|
|3|Política de cookies|https://rhino-performance.com/politica-de-cookies/|
|4|Políticas de envíos|https://rhino-performance.com/politica-de-envios/|

## Operación exacta, solamente después de autorización específica

En ese menú existente, añadir al final mediante **Agregar link**:

| Orden nuevo | Nombre | Dirige a | URL |
|---|---|---|---|
|5|Contacto|URL interna, mediante la opción URL del editor|https://rhino-performance.com/contacto/|
|6|Sobre Rhino Performance|URL interna, mediante la opción URL del editor|https://rhino-performance.com/sobre-rhino-performance/|

No modificar nombres, tipos, URLs ni orden de los primeros cuatro. No crear nuevas páginas ni cambiar su contenido. No tocar header, newsletter, diseño, metadatos, políticas, precios ni catálogo. Guardar puede publicar inmediatamente: no pulsar **Agregar/Guardar** durante la preparación previa a la autorización. Si la interfaz difiere, detener y adaptar el procedimiento sobre la operación real observada.

## QA posterior obligatorio

- Home y páginas representativas publicadas: seis enlaces correctos en el HTML inicial, sin duplicados, conservando los cuatro anteriores.
- Ambos destinos200, canonical propio y contenido esperado. Esto no es una nueva confirmación de indexación.
-360,390,768,1024,1440,1920: apertura/cierre del footer cuando corresponda, enlaces visibles sin recorte, foco y secuencia de teclado.
- Sesión sinJavaScript: comprobar disponibilidad de enlaces y documentar limitaciones nativas existentes; no presentar DOM modificado por pruebas como HTML inicial publicado.
- No recursos nuevos deJS/CSS/imágenes por los dos enlaces; comprobar cualquier cambio inesperado de layout o scripts.

## Reversión controlada

Registrar cada nuevo ID si la interfaz lo ofrece. Para revertir, eliminar únicamente las dos entradas nuevas si mantienen exactamente su nombre/URL/posición esperados y no fueron modificadas después por otra persona. Si no hay IDs, confirmar la identidad de cada entrada desde el menú concreto y sus campos completos antes de eliminarla. Ante duplicados, renombrados, cambios ajenos o ambigüedad, detener. No restaurar un menú completo encima de cambios posteriores.

**Estado:** procedimiento manual listo para revisión; respaldo administrativo no obtenido; modificación no autorizada ni ejecutada. No se solicita todavía autorización para aplicar una operación cuyo respaldo obligatorio está pendiente.

## Continuación: respaldo del propietario y riesgo separado del footer

El propietario preparará el respaldo desde el administrador. Registrar fecha, menú seleccionado, campos visibles completos, evidencias locales y hash SHA256; no enviar credenciales. La ausencia de IDs no impide preparar una reversión manual, pero reduce la certeza de identidad: si los nombres/URLs/posiciones ya cambiaron, detener en lugar de borrar por coincidencia parcial.

El foco en enlaces colapsados es un defecto previo del footer móvil: riesgo relevante de accesibilidad, porque Tab puede llevar a contenido visualmente oculto. Añadir dos enlaces podría sumar dos destinos a esa secuencia oculta; no se supone que el problema desaparezca. El preview con el acordeón abierto sí mostró ambos destinos accesibles. No hay evidencia de pérdida de datos comerciales, indexación o deterioro de rendimiento causado por ese defecto. Se registra como P2 de accesibilidad, independiente de paginación; no se modifica footer-rhino.tpl en este paquete. Antes de autorizar el menú, declarar esa limitación; una corrección futura requiere su propio diff, revisión y QA de apertura/cierre/Tab/Enter/Escape según el contrato real, sin ocultar enlaces rastreables ni imponer ARIA redundante.
