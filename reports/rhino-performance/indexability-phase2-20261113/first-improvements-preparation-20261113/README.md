# Rhino Performance — primeras mejoras SEO preparadas

Continuación incremental del [informe de exportaciones adicionales](../additional-exports-20261113/README.md). Se conserva el baseline: 124 páginas HTML verificadas, 122 rutas HTML observadas; ejemplos oficiales guardados con 109 coincidencias exactas indexadas, cuatro descubiertas sin indexar y once sin estado exacto nuevo. No se atribuyen esos estados a una inspección actual.

No se realizaron consultas a Rhino o Google, rastreos, cambios en producción, menús, canonicals, metadatos, catálogo o crawler. Las únicas llamadas a proveedores son las revisiones de documentos por Claude y Codex expresamente solicitadas.

## 1. Terapia fría y brazo individual: cómo cerrar el estado oficial

[Procedimiento manual exacto](inspection-procedure.md) · [Preparación y campos requeridos](inspection-preparation.json).

El control local `access doctor`, sin probe, encontró la configuración GSC, pero ninguna credencial utilizable. No probó la cuenta/API, no abrió OAuth ni leyó remotamente las URLs. Que la sesión del agente no disponga de credencial no significa que el propietario no tenga acceso en su navegador.

Por tanto, la vía preparada es recibir el resultado almacenado de Inspección de URLs de:

- https://rhino-performance.com/terapia-fria/
- https://rhino-performance.com/productos/brazo-presoterapia-pro-3-individual/

Registrar propiedad, URL exacta, fecha/hora con zona, estado/motivo literal, canonical usuario/Google, último rastreo, rastreo e indexación permitidos y obtención de página. Conservar campos ausentes como desconocidos. No ejecutar prueba en vivo ni solicitar indexación como parte del procedimiento.

**Estado:** procedimiento listo; resultados oficiales fechados todavía pendientes. No existe una causa técnica demostrada para modificar el tema. La lectura de capturas/resultados locales que aporte el propietario no requiere nuevas llamadas externas.

## 2. Presoterapia: carencia comprobada en el contenido conservado

La captura completa más reciente localizada en las familias de QA de categoría del 10 de noviembre, a las 20:54 UTC, contiene HTML inicial y DOM renderizado proyectados. Su main muestra pestañas de categorías y tres tarjetas: Botas PRO AIR, Kit Botas y Brazos PRO 3 y Kit Botas PRO 3. No incluye un texto separado que ayude a distinguir kits con compresor de accesorios sin compresor.

Esto es una **carencia observada en esa versión guardada**, no una certificación de que siga faltando hoy. La proyección elimina scripts, formularios y atributos privados conocidos y no es una copia íntegra de la respuesta. La evidencia del 12 de noviembre confirma las tres rutas de tarjetas sin JavaScript, pero no conserva un cuerpo editorial completo más reciente para esta categoría. Los enlaces globales a accesorios también aparecen en menús; no se usan para afirmar que todos estén dentro de su grid.

[Extracción reproducible, fecha, SHA256 y límites](presoterapia-saved-content.json).

Las consultas recibidas justifican estudiar esa ayuda de compra: «presoterapia brazos» tiene 75 impresiones y posición 9,15; «botas de presoterapia», 54 y 7,61; «botas de presoterapia precio», 45, un clic y 8,49. No prueban que la ausencia de una guía cause esas posiciones. El filtro de página es «+URL», con operador todavía sin confirmar; no hay cruce consulta-país-dispositivo. Los conteos bajos no justifican una proyección de tráfico o ingresos.

### Propuesta editorial breve

Preparé el [texto candidato](editorial-candidate.md): dos grupos que distinguen kits PRO 3 con compresor de botas accesorio y brazos PRO 3 sin compresor. La distinción comercial viene de las metadescripciones de producto guardadas en los lotes autorizados; cada afirmación tiene [fuente y puntero exacto](catalog-claim-provenance.json).

No se inventan beneficios, precios, compatibilidades, disponibilidad ni componentes no documentados. El texto remite a las fichas reales para escoger talla y comprobar contenido/compatibilidad, sin sustituir la información comercial nativa. No cambia el título, H1 o metadescripción.

**Ubicación recomendada:** después del listado y su paginación, antes del footer y dentro del main; usar un campo nativo editable solo si existe y permite esa ubicación. Evitar un bloque repetido tras cada carga dinámica. HTML sencillo, sin librerías, imágenes, scripts o nuevos estilos.

**Efecto esperado:** reducir la confusión entre comprar un equipo y comprar una pieza/accesorio. Es una hipótesis de experiencia comercial; no hay mejora de CTR, ranking, conversiones o PageSpeed medida. La categoría ya consta como indexada en los ejemplos oficiales: esta propuesta no es la corrección de un bloqueo de indexación.

**Estado:** borrador preparado sobre carencia histórica comprobada. `needs_evidence` antes de publicación: vigencia del texto actual, hechos de producto actuales, ubicación nativa y revisión del propietario. Si ya hay una explicación equivalente, conservarla y no duplicar el contenido.

## 3. 404 comerciales: verificación previa, sin redirecciones todavía

[Plan con destinos exactos, fuentes, límites y condiciones de seguridad](commercial-404-plan.json).

| URL histórica del ejemplo 404 | Clics / impresiones históricos | Situación actual y sustituto |
|---|---:|---|
| `/producto/kit-tina-y-chiller-pro/` | 22 / 582 | Desconocidos |
| `/productos/kit-tina-de-hielo-tub-air-chiller-ice-pro/` | 16 / 442 | Desconocidos |
| `/producto/faja-lumbar-compresion-fria/` | 19 / 1.008 | Desconocidos |
| `/producto/chiller-ice-pro/` | 14 / 512 | Desconocidos |

No se ha comprobado hoy que sigan respondiendo 404. Los ejemplos oficiales y el rendimiento histórico no prueban una pérdida actual de ventas ni la existencia de un producto sustituto. Las cinco redirecciones históricas prioritarias anteriores permanecen conservadas, como población distinta; no se reutilizan sus autorizaciones o manifiestos para estas cuatro rutas.

Antes de proponer un 301:

1. Comprobar HTTP actual y cada salto permitido, dentro de un alcance de lectura autorizado.
2. Confirmar el estado comercial real y un equivalente mediante catálogo autorizado y contenido, no por semejanza de slug.
3. Verificar que el destino sea útil para quien buscaba el producto antiguo: misma necesidad y una relación comercial real, no cualquier categoría o la home.
4. Verificar respuesta del destino, canonical declarado, ausencia de bucles/cadenas y de enlaces internos hacia rutas retiradas. Canonical declarado no equivale al elegido por Google; este último requiere evidencia GSC específica.
5. Solo si existe un defecto y una solución válida, preparar una propuesta exacta de redirección para revisión y autorización separadas. Si el producto se retiró y no hay reemplazo pertinente, mantener 404 puede ser correcto.

### Compatibilidad del futuro alcance

El selector cerrado integrado exige cinco URLs, mientras esta prioridad comercial contiene cuatro. **Estas cuatro no forman un manifiesto ejecutable válido.** No se cambia el motor ni se agrega una URL de relleno.

Existe un quinto destino con justificación propia, si se decide y autoriza ese alcance mixto: `/por-que-corres-lento-posibles-causas-y-como-solucionarlas/`, ejemplo 404 con 18 clics y 1.460 impresiones históricas. Su equivalencia con un artículo actual se evaluaría separadamente; no sustituye a un producto. No se ha creado o ejecutado un comando nuevo para este grupo.

Mantener como referencia los límites ya revisados: 12 GET totales incluyendo robots y redirecciones, concurrencia uno, 0,5/s o menos según robots, 120 segundos supervisados, timeout de 20 segundos, dos millones de bytes codificados/descomprimidos y tres saltos globales. Esos tres saltos pueden impedir completar todas las cadenas: cualquier autorización futura debe aceptar expresamente un resultado parcial acotado o revisar el presupuesto, sin ampliación implícita. Parada global ante condiciones críticas, sin reintentos ni activos externos.

Los manuales PDF históricos siguen en una operación aparte: falta la fuente oficial y versión correcta. No se propone descargar o reemplazar instrucciones con las de otro producto.

## 4. Datos estructurados y restricciones conservadas

Las advertencias de `author` y Product secundarios permanecen pendientes de contexto, sin cambios masivos ni nuevos JSON-LD. Se conservan checkout/add-to-cart bloqueados, canonicals del blog, menús, contenidos publicados, paginación aprobada y motor V4. No se ejecutan suites ni mediciones ya aprobadas para preparar documentos.

## 5. Operaciones que necesitan autorización o datos del propietario

| Operación | Estado |
|---|---|
| Recibir resultados oficiales locales de las dos inspecciones | Preparado; dentro del encargo, archivos pendientes |
| Leer por API las dos inspecciones | No ejecutado; falta credencial utilizable y autorización específica aplicable |
| Confirmar contenido publicado actual y fichas mediante nuevas lecturas | No autorizado en esta fase; preparar alcance mínimo si no se aportan capturas actuales |
| Comprobar las rutas 404 y destinos relevantes | Plan listo; selección final compatible, manifiesto/comando y autorización exacta pendientes |
| Publicar la guía o cualquier redirección | No autorizado; necesita evidencia actual, mecanismo exacto, diff/respaldo/hashes, QA y revisión independiente |

El siguiente paso más corto es proporcionar las dos inspecciones oficiales y una captura actual del texto completo de Presoterapia o autorizar su lectura acotada. No se pide autorización general para publicar contenido sin resolver esas condiciones.

## 6. Revisión incremental y evidencias

[Revisión independiente y contraste completados](review-status.json): ambos participantes respondieron sus preguntas asignadas y revisaron el borrador reducido. Claude resolvió la objeción documental sobre clasificación/enlaces; permanecen abiertas las condiciones de vigencia e integración de ambos revisores. [ADR incremental](ADR.json), con `implementation_allowed=false`. No se fuerza unanimidad ni se sustituye QA por una opinión.


### Alternativa editorial más sencilla

La revisión propuso reducir los cuatro puntos iniciales a dos grupos: kits con compresor y productos vendidos sin compresor. Se eliminó la comparación de PRO AIR y la repetición de los kits; no se denomina «completo» a ningún equipo. Se conservan [el primer borrador](editorial-candidate-v1.md) y [su diff documental](editorial-revision.diff).

Un enlace contextual a una ficha no equivale a afirmar pertenencia al grid de categoría. No se añaden productos al listado. Sigue siendo obligatorio comprobar vigencia y destino de cada ficha antes de publicar; las capturas actuales disponibles no permiten afirmar que los accesorios estén en el grid. Esta distinción se sometió al contraste incremental, sin imponer una preferencia por proveedor.
