# Rhino Performance — conciliación adicional y propuestas SEO

Importación offline de seis exportaciones oficiales entregadas el 13 de noviembre de 2026. Continuación de [las oportunidades pendientes](../opportunities-20261113/README.md), sin repetir rastreos, inspecciones, discovery o pruebas del motor. Ninguna modificación de producción ni nueva solicitud a Rhino o Google.

## Qué cambia la evidencia

De las 124 páginas HTML conocidas, **109 aparecen por URL exacta en los ejemplos de páginas indexadas**, cuatro aparecen en «Descubierta: actualmente sin indexar» y11 no tienen un estado exacto en estas nuevas tablas. Esto amplía la evidencia disponible; **no demuestra un aumento de10 a109 páginas indexadas durante el periodo**. Las diez inspecciones históricas indexadas están incluidas entre esas 109.

La lista completa aportada contiene 141 ejemplos indexados; 32 URLs no coinciden exactamente con el inventario124. Se conservan como observaciones externas, sin certificarlas como páginas HTML actuales, variantes equivalentes o nuevas páginas administrativas verificadas. No se infiere un inventario administrativo completo.

| Tipo del inventario | Ejemplos indexados exactos | Descubiertas sin indexar | Sin estado exacto nuevo |
|---|---:|---:|---:|
| Categorías |4|1|0|
| Productos |13|1|0|
| Artículos |83|0|3|
| Páginas informativas |6|2|0|
| Home, catálogo, índice blog |3|0|0|
| Paginaciones de catálogo/blog |0|0|8|
| **Total** |**109**|**4**|**11**|

[Matrix124CSV](url-matrix-124.csv) · [JSON con fuentes por observación](url-matrix-124.json) · [Resumen de controles](summary.json).

Son estados de las exportaciones guardadas, no una inspección en vivo ni una garantía de que Google los conserve. El último punto del gráfico es 8 de noviembre; las fechas de último rastreo son observaciones distintas y algunas posteriores. El archivo se llama 13 de noviembre, pero no aporta una fecha individual de inspección para cada URL.

Los cinco ejemplos de «Descubierta sin indexar» traen último rastreo numérico 25568, que con el calendario1900 del libro se decodifica como 1969-12-31. Se conserva el dato original, marcado como fecha no utilizable; no lo interpretamos como un rastreo real o inventamos una fecha alternativa. La causa de ese valor no está demostrada.

## Primera acción: dos destinos comerciales sin indexación conocida

Las cuatro coincidencias exactas de «Descubierta sin indexar» son:

- `/terapia-fria/` — categoría comercial, prioridad de investigación.
- `/productos/brazo-presoterapia-pro-3-individual/` — producto comercial, prioridad de investigación.
- `/contacto/` — conservar sin cambios.
- `/sobre-rhino-performance/` — pendiente de contenido por decisión del propietario; no promocionar ni forzar indexación.

El quinto ejemplo es `/sitemap_blog.xml/`, fuera del inventarioHTML. No es automáticamente una página comercial que deba indexarse.

Los dos primeros ya cuentan con observaciones técnicas guardadas de200/canonical propio y rutas de descubrimiento. Por tanto, **no se ha demostrado un bloqueo del tema que deba corregirse**. El paso mínimo es aportar una inspección oficial por URL de estos dos destinos o autorizarla separadamente, para comprobar canonical seleccionado, permisos, rastreo y motivo. No se solicitan indexaciones masivas ni se reescribe contenido para intentar eliminar un estado de Google.

Presoterapia, Compresión frío/calor, Accesorios y Pistolas de masaje aparecen por URL exacta como indexadas en el nuevo archivo. No corresponde tratarlas como categorías bloqueadas por falta de indexación.

## Propuesta comercial: Presoterapia

La exportación contiene 117 consultas y una sola página observada: `https://rhino-performance.com/presoterapia/`.

| Consulta del archivo filtrado | Clics | Impresiones | CTR exportado | Posición |
|---|---:|---:|---:|---:|
| presoterapia brazos |0|75|0%|9,15|
| botas de presoterapia |0|54|0%|7,61|
| botas de presoterapia precio |1|45|2,22%|8,49|
| botas presoterapia |1|35|2,86%|8,23|
| botas brazos precio |0|25|0%|10,96|
| precio de botas de presoterapia |0|8|0%|8,25|

Estas consultas permiten enfocar una oportunidad de **selección y compra de equipos**, en vez de atribuir el CTR de toda la categoría a un defecto. «Precio» también puede referirse a sesiones: la intención es una interpretación que debe contrastarse, no una etiqueta de Google. Las consultas locales como «presoterapia vigo» o «presoterapia zaragoza» no justifican orientar la tienda a servicios locales de esas ciudades.

**Propuesta concreta condicional:** evaluar una guía breve dentro de la categoría que ayude a distinguir botas, brazos, equipo completo y accesorio, y elegir entre los productos realmente ofrecidos. Reutilizar sus enlaces y precios nativos; no escribir precios o disponibilidad manualmente. Si se demuestra que falta ese contenido y posteriormente se autoriza, conservar el primer viewport y el listado existentes, evitando componentes, imágenes o scripts adicionales. No crear páginas nuevas ni tocar el menú.

El título guardado ya es «Botas y Brazos de Presoterapia | RHINO Performance»; no hay evidencia suficiente para sustituirlo. La descripción guardada también habla de botas/compresores. Su vigencia comercial y el snippet que Google muestra no se han verificado en esta fase. La guía sigue `needs_evidence` hasta revisar texto actual, distinciones reales de producto e intención por landing. El snippet servido se exige para una hipótesis de CTR/título, no como requisito universal de una guía editorial. P1 indica prioridad de investigación; los volúmenes de 0–1 clics por consulta no prueban un impacto grande. No se promete aumento de clics o ventas.

## Compresión frío/calor: conservar antes de reescribir

El destino del archivo es **`/compresion-frio-y-calor/`**, no el abreviado `/compresion-frio-calor/` que acompañaba al mensaje. No se inventa ni visita esa ruta alternativa.

Hay ocho consultas visibles. «rhino performance» aporta 843 de 876 impresiones de esa tabla, cuatro clics y posición 1,00. Las consultas visibles están dominadas por marca; «cold therapy compression sleeve» tiene una impresión y posición12. No es evidencia suficiente para convertir la categoría en una landing de esa frase ni para eliminar términos de su contenido.

**Decisión concreta:** conservar título y descripción mientras se estudia relevancia por consulta y snippet servido. El título guardado «Compresas de Frío y Calor | RHINO Performance» ya describe el producto. No hay canibalización demostrada por el hecho de que ambas categorías reciban «rhino presoterapia»: hace falta comparar la misma consulta y segmentos entre landings y probar un conflicto de intención o resultado.

## Límites de las métricas que afectan a las decisiones

| Exportación | Gráfico/Páginas | Consultas visibles | Países/Dispositivos |
|---|---|---|---|
| Presoterapia |30clics /2.810impresiones|10 /1.912|10 /1.912|
| Compresión |6 /1.079|4 /876|4 /876|

Las diferencias están conservadas; su causa no queda demostrada por los archivos. No se rellenan consultas desconocidas ni se atribuye todo el desfase a privacidad. No se cruzan por orden de fila las tablas independientes de consultas, países o dispositivos. Así,843/876 describe la tabla de consultas visible de Compresión, no843/1.079 de todas las impresiones de categoría ni una cuota de ventas.

Filtros declara «Últimos 3 meses», y92 filas diarias de Gráfico cubren11 de agosto–10 de noviembre de 2026. Es un intervalo observado, no metadatos de fecha absoluta seleccionada. Cada filtro Página se exporta como «+URL»; el operador exacta/contiene no está explícito. Una sola landing exacta observada permite relacionar estas consultas con el alcance filtrado aportado, pero no probar que el operador fuera «URL exacta» o que no existan filas omitidas. Se ha pedido confirmación al propietario; hasta entonces se conserva esta condición.

[Datos de ambas categorías y fuentes](category-query-evidence.json) · [125 consultas clasificadas provisionalmente](classified-queries.csv). No hay datos de conversiones ni ingresos para cuantificar impacto comercial. No usar un CTR esperado universal por posición como diagnóstico.

## Correcciones técnicas candidatas: 404 históricos con exposición

Las33 URLs del desglose404 y las 33 de «Rastreada sin indexar» no coinciden exactamente con ninguna de las 124 páginas actuales conocidas. Esto no garantiza ausencia de problemas: hay URLs externas al inventario y tablas de ejemplos limitadas. No se transfiere el estado entre www/no-www, barra final, slug relacionado o canonical supuesto.

Entre los404 sí hay rutas con exposición histórica que merecen una investigación acotada:

| Ruta del ejemplo404 | Clics históricos | Impresiones | Posible acción, todavía no aprobada |
|---|---:|---:|---|
| `/producto/kit-tina-y-chiller-pro/` |22|582|Comprobar respuesta actual y equivalente real, si existe.|
| `/productos/kit-tina-de-hielo-tub-air-chiller-ice-pro/` |16|442|Distinguir producto retirado de ruta rota; no asumir que sigue en catálogo.|
| `/producto/faja-lumbar-compresion-fria/` |19|1.008|Verificar equivalencia comercial antes de proponer un 301.|
| `/producto/chiller-ice-pro/` |14|512|Misma comprobación, sin inventar producto sustituto.|
| `/por-que-corres-lento-posibles-causas-y-como-solucionarlas/` |18|1.460|Comparar temática con el artículo actual antes de proponer redirección.|

La prioridad de estas rutas es preservar o recuperar accesos útiles, no interpretar sus clics históricos como ventas perdidas. No dirigir todos los404 a la home. Si no existe reemplazo válido, conservar un 404 puede ser la decisión correcta.

Dos manuales PDF aparecen en los404 con 55 y 31 clics históricos. Son recursos, no páginasHTML ni oportunidades necesariamente de adquisición. Propuesta separada: localizar con el propietario el manual oficial y versión correcta antes de restaurar archivo o redirigir. No se ha descargado ni publicado ningún documento.

Las cinco redirecciones prioritarias del informe anterior se mantienen sin cambios, como una línea de investigación distinta de estos404. Sus destinos siguen pendientes; no se ha ejecutado el borrador de comprobación ni modificado límites del crawler.

## Estados desconocidos y variantes

Quedan 11 URLs sin coincidencia exacta nueva: tres artículos, siete paginaciones del blog y `/productos/page/2/`. Dos de esos artículos tienen una variantewww sin barra final en los ejemplos indexados; se conserva esa relación como candidata, sin transferir indexación al canonical del inventario. Para «La inmovilidad es el verdadero deterioro» aparece una ruta histórica corta indexada, pero la semejanza de slug no demuestra equivalencia.

Conservar el canonical del blog y la consulta preparada para Tiendanube. No confundir la ausencia de estado de sus paginaciones con falta de indexación de sus 86 artículos: 83 aparecen por URL exacta en los ejemplos.

Se conservan exclusiones de checkout/add-to-cart, advertencias author/Product, diagnóstico de los 20 artículos con campos incompletos, menús y paginación publicada. No se desbloquean acciones comerciales ni se genera marcado para silenciar alertas.

## Backlog y revisión incremental

[Seis propuestas con evidencia, alternativas, riesgos y condiciones](opportunity-backlog.json):

1. **SEO-F2-01 /P1:** aclarar el estado de Terapia fría y brazo individual; investigación de indexación, sin causa técnica inventada.
2. **SEO-F2-02 /P1:** guía de selección comercial en Presoterapia, condicionada a demostrar una carencia real.
3. **SEO-F2-03 /P2:** conservar Compresión y medir intención/snippet antes de redactar.
4. **SEO-F2-04 /P1:** verificación de lectura previa de posibles404 comerciales; recuperación solo si se demuestra estado actual y equivalente real.
5. **SEO-F2-05 /P2:** recuperar manuales solo con fuente y versión autorizadas.
6. **SEO-F2-06 /P2:** evaluar redirección de un artículo antiguo si se confirma equivalencia.

No se identifica un P0 nuevo ni un parche listo para producción. La selección de estas actuaciones no autoriza consultas ni cambios. Las condiciones específicas, no el voto de un modelo, determinan cuándo una propuesta puede convertirse en un diff revisable.

[Claude y Codex completaron la revisión independiente y las respuestas cruzadas](review-status.json). Los contratos y las respuestas asignadas fueron comprobados por el controlador. Las precisiones documentales se incorporaron, pero las objeciones de Claude `claude-obj-1` y `claude-obj-2` permanecen abiertas por falta de evidencia operativa. No se simula aprobación. [ADR incremental](ADR.json). Los modelos no sustituyen QA ni autorizan producción.

## Evidencia y preservación

[Seis originales con SHA256, tamaño, pestañas y filtros](source-manifest.json) · [212 observaciones nuevas](new-official-observations.json) · [Observaciones oficiales anteriores y nuevas](all-official-url-observations.json) · [URLs externas al inventario](external-inventory-observations.json) · [404 y rendimiento histórico exacto](404-historical-visibility.json).

Los 124 registros conservan sus campos originales y reciben observaciones nuevas en columnas separadas. No se reescriben inspecciones históricas con fechas del archivo. Los originales XLSX no se modifican, las fórmulas no se ejecutan y no se instalan dependencias.


### Condiciones de validación antes de cualquier cambio futuro

Separar hipótesis de posicionamiento, carencia editorial y presentación en resultados. Para elegir categoría frente a PDP se requieren Páginas filtradas por la consulta, cohortes comparables y análisis de intención; no basta la tabla de una categoría. Para redactar una guía, comprobar primero una carencia útil en el texto actual y las distinciones reales del catálogo.

Antes de implementar: fijar consultas objetivo, landing, país/dispositivo comercial y ventanas de igual duración; registrar cambios y factores externos. Determinar con esos datos la duración y suficiencia de muestra para un efecto comercialmente útil. Con muestras bajas, filtros incompatibles, incertidumbre importante o factores externos sin control, el resultado será `inconclusive`. No se inventa ahora un umbral de clics, CTR o incremento garantizado.


## Siguiente operación propuesta, sin ejecutar

[Operaciones separadas pendientes de autorización o de exportación oficial del propietario](next-operations-NOT-AUTHORIZED.md). La primera recomendación es aclarar exclusivamente Terapia fría y el brazo individual mediante inspección oficial fechada. La hipótesis editorial de Presoterapia y cualquier ruta404 se conservan como propuestas concretas condicionadas, no como cambios aprobados.
