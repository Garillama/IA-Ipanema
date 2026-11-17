# Presoterapia — validación local de la vía editorial

Continuación de [la preparación anterior](../first-improvements-preparation-20261113/README.md). Esta entrega incorpora solo lectura del código local vigente, hashes y revisión de las opciones nativas. **No hay lecturas nuevas de producción ni confirmación comercial actual.**

Baseline conservado: 124 páginas HTML verificadas y 122 rutas de descubrimiento; 109 coincidencias exactas en ejemplos indexados, cuatro descubiertas sin indexar y once sin estado exacto nuevo. Los estados de Google siguen ligados a sus exportaciones, no a una inspección actual.

## Resultado por condición

| Condición | Resultado |
|---|---|
| ¿Existe ya una explicación equivalente en producción? | Pendiente de lectura autorizada o evidencia actual del propietario. La ausencia solo está comprobada en la captura guardada del 10 de noviembre. |
| ¿Siguen siendo correctas las afirmaciones con/sin compresor? | Respaldadas por fichas históricas; no revalidadas hoy. No se deduce disponibilidad o contenido actual de caja. |
| ¿Hay un campo nativo de categoría consumido por el tema? | Sí: `category.description`, pero el consumidor localizado está en el encabezado, no después del listado. |
| ¿Está habilitado ese encabezado localmente? | No: `heading.disabled=true` en la plantilla compartida de categoría. No se propone activarlo como atajo. |
| ¿Hay un componente nativo reutilizable después del grid? | Existe `rich-text`, habilitado para todas las plantillas de página, con bloque `text` de tipo `richtext`. Es una opción de composición, todavía sin viabilidad administrativa exclusiva de Presoterapia comprobada. |
| ¿Se garantiza que no se repita con «Mostrar más»? | No. Una sección hermana fuera de `.js-product-table` queda fuera del selector configurado de carga; falta una prueba real del contenido propuesto con `LS.hybridScroll`. |
| ¿Se puede publicar ahora? | No. No hay diff ni operación de publicación autorizable todavía. |

[Fuentes locales, líneas, SHA256 y límites](local-native-evidence.json). Los hashes locales de `pagination.tpl` y `store.js` coinciden con las postimágenes aprobadas. No se presenta esto como una nueva comprobación de los hashes remotos.

## 1. Ubicación nativa: opciones y riesgos

### Opción preferida, si el editor permite aislarla

Reutilizar la sección existente `rich-text` y su bloque `text`, después de `product_list` y su paginación, antes de las FAQ/footer y dentro del main. El esquema local permite todas las plantillas de página; el bloque acepta texto enriquecido y lo imprime en `user-content`.

**Condición decisiva:** confirmar mediante el administrador autorizado o capturas del propietario que la sección pueda aplicarse únicamente a Presoterapia. La plantilla local `templates/pages/category.json` es común a categorías; agregar allí un texto estático sin aislamiento podría mostrarlo en Terapia fría, Accesorios y otras categorías. No existe evidencia administrativa actual que permita garantizar una instancia exclusiva por categoría. La disponibilidad declarada en un schema no certifica los permisos o controles reales del editor.

Evitar el preset por defecto completo si añade botón o texto innecesarios. El bloque `heading` envuelve contenido enriquecido en un `div`: su tamaño visual no garantiza un H2. Usar un H2 semántico mediante el mecanismo soportado del editor y verificar el HTML resultante, sin crear otro H1 ni ARIA redundante. Los enlaces contextuales a fichas no implican agregar productos al grid.

### Campo de descripción de categoría

`sections/page-header.tpl` muestra `category.description` dentro de un `p`, junto al título. El encabezado está desactivado en la plantilla local. Ese consumidor no satisface la ubicación solicitada. No pegar una lista/H2 suponiendo que ese `p` admitirá cualquier HTML, ni activar el encabezado si altera el diseño. Tampoco se han confirmado el contrato de sanitización o el estado del campo en el administrador.

### Alternativa mínima, solo si la composición nativa no puede aislarse

Documentar una extensión acotada del renderizado del listado que muestre contenido editable de esa categoría después de la paginación y fuera de `.js-product-table`, con identidad de categoría verificada y contrato de contenido seguro confirmado. No agregar una guía global para toda categoría con descripción no vacía.

Antes de preparar ese parche habría que resolver fuente editable, alcance de la categoría, sanitización/HTML admitido y política de páginas posteriores. No se inventa un ID ni un setting de Tiendanube inexistente. Se preservan los dos archivos de paginación publicados: esta alternativa no justifica cambiarlos. **No se ha modificado código ni preparado un diff de tema.**

## 2. Texto propuesto y comprobación comercial necesaria

[Texto editorial propuesto](editorial-proposed.md), conservado sin cambios respecto al candidato revisado:

- Kits PRO 3 con compresor: Kit de Botas y Kit de Botas y Brazos.
- Productos PRO 3 sin compresor: botas accesorio, par de brazos y brazo individual.
- Recordatorio de consultar contenido, talla y compatibilidad en cada ficha.

No se incorporan precios, ofertas, stock, beneficios terapéuticos ni compatibilidades concretas. No se clasifica PRO AIR ni se denominan «completos» a los kits. Las fuentes históricas y sus punteros se conservan en la [trazabilidad anterior](../first-improvements-preparation-20261113/catalog-claim-provenance.json).

El texto está cerrado como **candidato editorial**, no como afirmación comercial actual aprobada. Si la categoría ya contiene una explicación equivalente, no añadirlo. Si una ficha contradice la afirmación histórica, corregir únicamente esa frase antes de solicitar publicación. Si una ficha no demuestra una afirmación, dejarla fuera o pedir confirmación autorizada del contenido de caja; no inferirlo de su nombre.

## 3. Lecturas de producción pendientes de autorización

[Alcance exacto de seis documentos](production-read-scope-NOT-AUTHORIZED.json):

1. https://rhino-performance.com/presoterapia/
2. https://rhino-performance.com/productos/kit-botas-de-presoterapia-pro-3/
3. https://rhino-performance.com/productos/kit-botas-y-brazos-de-presoterapia-pro-3/
4. https://rhino-performance.com/productos/botas-presoterapia-pro-3/
5. https://rhino-performance.com/productos/brazos-presoterapia-pro-3/
6. https://rhino-performance.com/productos/brazo-presoterapia-pro-3-individual/

Propósito exclusivo: existencia de una explicación equivalente y veracidad de las cinco afirmaciones con/sin compresor, guardando fecha, fuente y condiciones. No consultar Google, administrador, 404, catálogo privado o recursos multimedia como parte de ese alcance. No formularios, compras ni modificaciones.

**No es un manifiesto ejecutable de V4:** el modo cerrado integrado exige cinco URLs. No se inventa un comando de seis destinos, no se cambia el motor y no se añaden rellenos ni solicitudes duplicadas para adaptarlo. Antes de ejecutar una autorización de lectura hay que fijar un mecanismo soportado que conserve los controles aplicables; si no existe, mantener el bloqueo y recurrir a documentación actual aportada por el propietario. Esta entrega solicita el alcance, no afirma un transporte de seis destinos ya validado.

La alternativa sin llamadas externas del agente es recibir el texto/HTML actual completo de la categoría y capturas o fichas actuales de contenido de caja de esos cinco productos. La identidad y fecha deben quedar explícitas.

## 4. «Mostrar más», responsive, accesibilidad y rendimiento

El código local configura `productGridSelector: '.js-product-table'`; `main-products-grid.tpl` termina las tarjetas dentro de ese elemento y renderiza la paginación después. Una guía como sección hermana posterior no pertenece al contenedor configurado para anexar productos. Es una evidencia de arquitectura, no una prueba posterior de no duplicación.

Antes de aceptar cualquier implementación:

- Verificar un solo bloque de guía en el HTML inicial y en el DOM, antes y después de cargar productos; excluir el bloque de los fragmentos anexados.
- Confirmar que la primera tanda y la carga posterior mantienen orden, número e identidad de productos, sin modificar el comportamiento o foco de la paginación aprobada.
- Presoterapia tenía tres tarjetas en la evidencia anterior. Si no tiene siguiente página real, no inventar una prueba de «Mostrar más» en producción: documentar la limitación y usar una prueba aislada pertinente, sin presentarla como validación remota de la categoría.
- Decidir explícitamente si la guía aparecerá en páginas posteriores y con filtros. Evitar un texto estático global que invada categorías o resultados de búsqueda. No cambiar canonicals para resolver esa decisión.
- Comprobar 360, 390, 768, 1024, 1440 y 1920 px, teclado y foco nativos, enlaces descriptivos, un H2 real, orden de lectura y ausencia de desbordamientos. Mantener tipografías y estilos actuales.
- Usar HTML sencillo sin librerías, JS, imágenes ni estilos añadidos por el contenido. El texto incorpora DOM/enlaces y bytes: no se afirma coste cero ni mejora de PageSpeed.
- Antes/después de una publicación futura, comparar perfiles equivalentes de móvil y escritorio con mediciones repetidas y tolerancias existentes; revisar recursos y tareas. No atribuir diferencias pequeñas al texto ni prometer ranking o conversiones por añadirlo.

**Estado:** evaluación de riesgos completada; QA de un bloque implementado todavía no ejecutado porque no hay implementación.

## 5. Incorporación de las dos inspecciones oficiales GSC

Reutilizar el [procedimiento manual exacto ya preparado](../first-improvements-preparation-20261113/inspection-procedure.md), sin repetir las quince inspecciones históricas ni los lotes V4. Esperamos resultados oficiales almacenados de:

- https://rhino-performance.com/terapia-fria/
- https://rhino-performance.com/productos/brazo-presoterapia-pro-3-individual/

Al recibirlos: conservar original y SHA256, URL exacta, propiedad, fecha/hora/zona, estado/motivo literal, canonical del usuario/elegido por Google, permisos, obtención de página y último rastreo disponibles. Añadir observaciones a la matriz en columnas/registros nuevos, sin reemplazar fuentes anteriores. Distinguir resultado almacenado de una prueba en vivo y marcar campos ausentes como desconocidos.

El último control local conservado indicó configuración presente sin credencial utilizable. No se ha repetido una prueba de cuenta ni iniciado OAuth. No solicitar indexación o validar correcciones automáticamente. Los resultados oficiales siguen pendientes; no se presenta el procedimiento como una inspección completada.

## 6. 404 y datos estructurados

Conservar [el plan de las cuatro rutas](../first-improvements-preparation-20261113/commercial-404-plan.json). No hubo nuevas lecturas, destino equivalente confirmado o propuesta de redirección. Mantener separadas las antiguas redirecciones útiles y los ejemplos 404. No redirigir todo hacia la home.

Las advertencias de `author` y Product secundarios siguen pendientes de contexto, sin parches para silenciarlas. No se cambian productos, inventario, artículos, apps o crawler.

## 7. Autorizaciones y bloqueos

- **Lectura de producción:** requiere autorización específica para los seis documentos anteriores y un mecanismo real compatible; no está ejecutada ni habilita ediciones.
- **Administrador/editor:** falta evidencia de la ubicación exclusiva de Presoterapia. Capturas del propietario pueden resolverla; acceder remotamente al administrador requeriría autorización y una integración compatible.
- **Publicación:** todavía no hay operación exacta justificada. Primero confirmar carencia/fichas actuales y vía nativa exclusiva; después preparar el diff o configuración exactos, respaldo, hashes, revisión independiente, QA y solicitud de publicación. No solicitar aprobación de un parche inexistente.

[Claude y Codex completaron revisión independiente y respuestas cruzadas](review-status.json). Ambos mantienen bloqueada la implementación: la exclusividad por categoría no está demostrada y faltan vigencia y QA real. Se conservan las objeciones críticas abiertas en el [ADR incremental](ADR.json), sin modificar artificialmente `needs_evidence`. No se propone publicación de una guía global ni se simula aprobación.
