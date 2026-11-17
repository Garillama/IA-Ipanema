# Presoterapia — alternativa nativa documentada

**Recomendación:** evaluar una plantilla alternativa de categoría, copiada de la configuración actual y asignada únicamente a Presoterapia. Es la vía preferida antes de plantear un cambio del código compartido. La capacidad general está documentada; su funcionamiento en la instalación personalizada de Rhino sigue `needs_evidence`.

## Fuente y alcance autorizado

Se consultó una sola [guía oficial de Tiendanube](https://ayuda.tiendanube.com/es_MX/diseno-ipanema/como-usar-plantillas-personalizadas-para-productos-categorias-y-paginas-con-el-diseno-ipanema), actualizada el 19 de octubre de 2026. El lector informó una captura de cinco días antes: no fue una prueba HTTP en vivo de Rhino. No se abrieron artículos relacionados, imágenes, Google, la tienda o el administrador.

La guía documenta plantillas para categorías, creadas en el editor y asignadas individualmente desde el administrador. Permite copiar configuraciones existentes y requiere un diseño publicado para asignarlas. La asignación se conserva por nombre; el editor muestra cuántas entidades la usan. [Hechos y procedencia](official-source-facts.json).

## Respuestas a las siete preguntas

| Pregunta | Conclusión y límite |
|---|---|
| ¿Ipanema soporta la funcionalidad? | Sí, según la guía consultada. No demuestra que los controles estén disponibles en nuestra instalación personalizada. |
| ¿Cómo crearla? | En Tienda online > Diseño, abrir Editar diseño; elegir Categoría, Crear plantilla y copiar una configuración existente en Crear desde. Crear confirma una modificación: no se ejecutó. |
| ¿Cómo asignarla solo a una categoría? | Abrir Presoterapia en Categorías del administrador, seleccionar el nombre en Plantilla y guardar. Es otra modificación: no se ejecutó. |
| ¿Permite rich-text después del listado? | La guía no prueba esa ubicación concreta. El esquema local permite rich-text en plantillas de página y su bloque text admite contenido enriquecido. La colocación tras product_list es una inferencia técnica viable, pendiente del editor real. |
| ¿Conserva filtros, paginación, SEO y responsive? | No hay garantía en esa guía. Copiar la configuración vigente evita rediseñarla, pero hay que comprobar esos contratos y comportamientos. |
| ¿Requiere cambiar código compartido? | No se anticipa si el editor permite copiar y asignar la alternativa con los componentes existentes. No se ha preparado ni aplicado código. |
| ¿Qué limita el tema personalizado? | Falta comprobar versión/editor disponible, plantilla realmente asignada, copia fiel de configuración, renderizado y comportamiento nativo. No actualizar, reemplazar ni publicar otro diseño para intentar habilitarlo. |

Los pasos operativos anteriores sintetizan la fuente autorizada. Las conclusiones sobre rich-text, código compartido y QA proceden del análisis local y no se atribuyen como garantías de Tiendanube. [Evidencia local reutilizada y hashes](local-evidence-reused.json).

## Primero: comprobación administrativa sin cambios

Este procedimiento está preparado para el propietario o un acceso administrativo futuro autorizado; no se ha abierto el administrador.

1. Registrar la instalación/diseño publicado que se está examinando. Nuestra referencia histórica es instalación14828608, tienda7400935; aquí no se volvió a comprobar remotamente.
2. Registrar la plantilla actualmente asignada a Presoterapia, Terapia fría y Accesorios, con nombre y fecha, antes de tocar un selector.
3. En el editor de esa instalación, comprobar que se ve la gestión de alternativas de categoría y que la configuración origen es la actualmente usada por Presoterapia. No crear, guardar, publicar o asignar durante esta inspección.
4. Comprobar qué opciones de sección están disponibles y si el texto enriquecido admite un H2 real y enlaces. Si comprobar la inserción exige crear o modificar algo, detenerse y preparar esa operación para autorización; no convertir una inspección en una edición.
5. Conservar capturas limitadas a controles/configuración relevantes, sin credenciales ni información administrativa ajena. La mera existencia del selector no demuestra que una alternativa futura esté asignada solo a Presoterapia.

Si faltan controles por la personalización del tema, conservar la condición pendiente. No asumir que copiar un archivo JSON local equivale a crear una plantilla correctamente registrada en Tiendanube.

## Después: operación nativa futura, todavía no autorizada

El objetivo sería crear una alternativa de categoría con nombre único, por ejemplo `Presoterapia — guía de compra`, copiando **la configuración realmente asignada**, no una base vacía. La plantilla común de categorías debe quedar intacta. Mantener el encabezado desactivado, las tarjetas, filtros, ordenamientos y configuración de paginación existentes.

Añadir únicamente la sección rich-text existente después del listado y su paginación, con un bloque editorial que produzca un H2 y enlaces descriptivos. Evitar el botón y textos de ejemplo del preset, componentes duplicados y scripts nuevos. El contenido será el [candidato conservado](../first-improvements-preparation-20261113/editorial-candidate.md), solo si sigue siendo necesario y comercialmente correcto tras verificar las seis páginas.

Antes de asignar: respaldo/configuración origen verificables y alternativa sin asignaciones. Después de una autorización específica de asignación: verificar que Presoterapia la usa y que ninguna otra categoría cambió. Un contador de una asignación no identifica por sí solo la categoría: confirmar también los nombres y campos de asignación. No reutilizar un nombre ya existente que pueda estar asociado a otras páginas o diseños.

**Crear, guardar contenido y asignar son operaciones administrativas remotas.** La autorización para leer la guía no permite ejecutarlas. El procedimiento futuro debe presentarse con configuración exacta, respaldo, verificaciones y reversión antes de pedir permiso para aplicarlo.

### Reversión que habría que preparar

Guardar primero el nombre de la plantilla original de Presoterapia y la configuración copiada. Una eventual reversión consistiría en restaurar solo su asignación previa si no existen cambios posteriores ajenos. La alternativa puede permanecer sin asignar; eliminarla sería una acción diferente que necesita alcance propio. No restaurar la plantilla compartida ni sobrescribir categorías no afectadas.

## QA requerido para la versión personalizada

- Comprobar encabezado, filtros, ordenamiento y la paginación publicada sin alterar `pagination.tpl` o `store.js`. Los hashes locales de ambos coinciden con las postimágenes aprobadas; no se hicieron lecturas remotas nuevas.
- Verificar un bloque de guía y un H2 real en el HTML inicial y el DOM. Una sección hermana posterior queda fuera del selector configurado `.js-product-table`, pero eso no certifica la ausencia de duplicación con LS.hybridScroll.
- Si Presoterapia sigue sin tener siguiente página real, documentar que allí no se ejercita «Mostrar más». No inventar productos o rutas para afirmar una prueba remota; cualquier prueba aislada complementaria se identifica como tal.
- Definir el comportamiento con filtros/páginas posteriores y comprobar que no se altera el canonical, indexabilidad o identidad de ninguna categoría. La guía autorizada no garantiza estos resultados.
- Verificar 360, 390, 768, 1024, 1440 y 1920px, teclado, foco, orden de lectura y enlaces. Mantener estilos y tipografía vigentes. No depender del tamaño visual de un bloque para afirmar semántica H2.
- Medir antes/después con perfiles equivalentes en móvil y escritorio; conservar tolerancias y ruido existentes. Texto/enlaces añaden bytes y DOM: no prometer coste cero, mejora de PageSpeed o incremento de tráfico.

Ninguna de estas comprobaciones de un cambio implementado se ha ejecutado ahora. La revisión de documentación no equivale a QA de la instalación.

## Lectura de las seis páginas: planificación conservada

No se consultó ninguna. El alcance sigue siendo Presoterapia y las cinco fichas PRO3 del [plan previo](../editorial-validation-preparation-20261113/production-read-scope-NOT-AUTHORIZED.json).

La inspección local del mecanismo existente confirmó dos límites: V4 cerrado exige cinco destinos y su informe conserva metadatos, encabezados y resúmenes/hashes de contenido, no el texto principal completo. Por ello, un lote no bastaría para certificar que no existe una guía equivalente. Tampoco conviene repetir cuatro URLs en dos lotes de cinco por una limitación de formato.

Una división compatible sin alterar el motor sería un alcance nativo de las **cinco fichas** para metadatos actuales y, por separado, evidencia actual del contenido de **Presoterapia aportada por el propietario**. Si las fichas exigen comprobar contenido de caja o contradicciones en el cuerpo que el informe no conserva, también necesitarían esa evidencia. Se trata de una opción de planificación, no de un lote ejecutado o autorizado ni de una verificación comercial completa.

No se preparó un manifiesto o comando de seis destinos, ni otro crawler. Si se requiere automatizar también la captura completa, falta identificar un mecanismo existente aprobado para ese alcance; no se reduce la seguridad para cerrar el expediente. Las seis páginas pueden asimismo documentarse con capturas/texto público actuales aportados por el propietario, conservando URL y fecha y sin datos privados.

## Estado de la revisión y decisión

[Claude y Codex completaron las revisiones independientes y sus respuestas cruzadas](review-status.json), únicamente sobre la nueva guía y su contraste local. La documentación permite avanzar desde «capacidad nativa desconocida» a «capacidad general soportada». **No resuelve todavía la aplicabilidad, asignación exclusiva o QA de Rhino.** El ADR permanece `needs_evidence`; no hay una configuración aplicada ni operación de publicación lista.


[ADR incremental](ADR.json): recomendación `native-alternative-category-template`, `implementation_allowed=false`. Ambos mantienen abiertas sus objeciones de aplicabilidad y preservación; una recomendación de configuración nativa no equivale a autorizar su creación o asignación.
