# Rhino Performance — cierre consolidado de cobertura SEO V4

13 de noviembre de2026. Consolidación offline posterior al lote15, sin solicitudes adicionales, nuevas inspecciones de Google ni cambios a la tienda o al motor.

**Cerrada la cobertura HTTP individual de las124 páginas HTML conocidas:124/124 responden200 en sus evidencias conservadas. Cero pendientes de HTTP.** Esto no certifica que las124 sean indexables en todos los niveles ni que Google las haya indexado. Hay20 artículos con comprobaciones técnicas parciales,7 paginaciones de blog con canonical consolidado y advertencias schema que siguen abiertas.

## Inventario y cobertura por plantilla

El inventario conocido contiene125 URLs:116 HTML y1 XML conservados del sitemap, más8 paginaciones verificadas fuera del sitemap. No es un inventario administrativo completo de Tiendanube ni un censo de URLs históricas, parámetros, variantes, contenido nuevo o índice de Google.

| Tipo | HTML conocidas | HTTP individual | En sitemap | Camino HTML observado | PASS histórico GSC |
|---|---:|---:|---:|---:|---:|
| Home | 1 | 1 | 1 | 1 | 1 |
| Informativas / institucionales | 8 | 8 | 8 | 6 | 1 |
| Catálogo | 1 | 1 | 1 | 1 | 1 |
| Productos | 14 | 14 | 14 | 14 | 2 |
| Categorías públicas | 5 | 5 | 5 | 5 | 2 |
| Índice blog | 1 | 1 | 1 | 1 | 1 |
| Artículos | 86 | 86 | 86 | 86 | 2 |
| Blog páginas2–8 | 7 | 7 | 0 | 7 | 0 |
| Catálogo página2 | 1 | 1 | 0 | 1 | 0 |
| **Total HTML** | **124** | **124** | **116** | **122** | **10** |

[Inventario completo de124 URLs CSV](inventory-124.csv) · [JSON con tipos originales](inventory-124.json) · [snapshot125 incluyendo XML](matrix-all-125-snapshot.csv) · [matriz vigente](../../url-matrix.csv) · [resumen estructurado](summary.json).

Cada fila conserva su URL, tipo, sitemap, HTTP, fecha/fuente, canonical, robots, title/H1, rutas y profundidad observadas, estado Google histórico y faltantes. Las fechas de evidencia van de `2026-11-10T20:55:16.385Z` a `2026-11-13T08:07:57.174430+00:00`: no son124 mediciones simultáneas ni se repitieron las antiguas. El análisis tiene su fecha propia; no se inventan timestamps por solicitud.

## Ejecuciones V4 cerradas y seguridad

El piloto inicial y los lotes02–15 completaron75 destinos únicos,11 productos y64 artículos, que estaban pendientes tras las49 observaciones HTTP iniciales. Son15 invocaciones autorizadas individualmente,90 GET:75 destinos y15 robots.txt. Todas terminaron con cinco destinos200, cero redirecciones, ningún resultado sin confirmar y supervisor `finished` con worker recogido. Este total **no cuenta todas las solicitudes históricas de la auditoría ni assets de pruebas anteriores de navegador**.

Cada invocación mantuvo12 GET máximos, concurrencia1, frecuencia máxima0,5/s o menor según robots, supervisor120 s, timeout20 s, cuerpos codificados/descomprimidos máximos2.000.000 bytes y3 redirecciones globales. Se conservaron los comandos originales, marcadores de un uso y checkpoints. No hubo reintentos ni expansión de alcance. [Ledger de15 ejecuciones](execution-ledger.csv), [JSON](execution-ledger.json).

El lote15 usó6 GET y terminó en14,33 s. [Informe específico](../live-batch15-20261113/README.md). Los26 hashes aprobados del motor/transporte fueron verificados antes y después. Todos los manifiestos y comandos de03–15 mantienen sus hashes. Las cabeceras de checkpoint históricas `running`/`project:null` se conservan sin repararlas: el estado terminal se acredita con `supervision.json` y las peticiones completadas.

## Descubrimiento mediante HTML

Las122 rutas observadas desde home pertenecen al grafo guardado, no a un rastreo ilimitado actual. Las cinco categorías conocidas enlazan a los14 productos conocidos; sus tarjetas tienen href reales. La paginación publicada del catálogo conserva `/productos/page/2/`, canonical propio y QA histórico de12→14 IDs únicos, sin duplicados. Se reutilizó [QA de publicación](../../../three-issues/operations/publication/resultados-produccion.md), no se modificó ni volvió a publicar.

El blog tiene ocho páginas con86 artículos distintos:12 por página en1–7 y2 en8, coincidentes con los86 del sitemap conservado. [Continuidad guardada](../../blog-continuity.json). Por tanto, los86 tienen rutas HTML observadas; no se afirma que Google haya seguido cada enlace. Los href con parámetros de tarjetas se conservan como variantes de navegación; no se crean productos adicionales ni se certifican todos los alias.

Contacto y Sobre Rhino carecen de camino observado en este corpus; eso no demuestra orfandad global. Ambas están en sitemap, con HTTP200 y canonical propio. Contacto tenía estado histórico descubierta sin indexar; no se conoce una causa técnica demostrada. Sobre Rhino queda pendiente editorial por decisión del propietario: no promocionar, modificar ni aplicar noindex. No se añaden enlaces a menús.

## Bloqueos confirmados y límites técnicos

- **HTTP:**0 respuestas no200 entre124 observaciones conservadas. Esto acredita disponibilidad en esas fechas, no disponibilidad futura.
- **Bloqueo general de rastreo/indexación:** ninguno demostrado con las fuentes revisadas. No equivale a certificar la ausencia universal de restricciones.
- **75 destinos V4:** permiso observado para agente auditor y Googlebot, meta robots/googlebot y X-Robots-Tag sin restricciones observadas, canonical propio, main presente y procesamiento completo de directivas. Estado técnico nativo `indexable_candidate` en75. No hubo bloqueos de transporte.
- **49 observaciones anteriores:** se conservan sus alcances, fechas y parsers originales; los campos históricos que aún dicen V4 no aprobado describen aquella evidencia, no el estado actual del motor. No se reescriben como si hubiesen usado el nuevo transporte.
- **20 artículos:** tienen HTTP individual, pero `partial_checks_remaining_content_or_directives_review`; meta robots y X-Robots-Tag constan `not_checked`, igual que contenido principal. Proceden del postcheck de BreadcrumbList. [Faltantes por URL](evidence-gaps.json) y [forma de su fuente original](historical-20-source-shape.json). No se convierten a aprobación técnica por su200.
- **7 paginaciones de blog:** canonical hacia `/blog/`, pese a contenido distinto; consolidación confirmada, causalidad de exclusión de artículos no demostrada. No son7 erroresHTTP ni7 artículos bloqueados. La matriz mantiene ese estado aparte.
- **Navegador:** no se hizo render/teclado/performance nuevo por cada destino cerrado. En el gate general V4 permanecen11 PDP `blocked` por comparaciones schema y64 artículos `insufficient_evidence` por los controles pendientes; se conserva ese gate, separado del HTTP y de Google.

La matriz conserva97 candidatos técnicos observados,20 comprobaciones parciales y7 canonical consolidado. Esas categorías no equivalen a decisiones de Google ni a certificación completa de calidad. Hay además22 filas sin observación X-Robots-Tag y23 sin comprobación de main en la matriz —20 artículos más3 páginas blog—; están enumeradas, no tratadas como fallos.

### Los20 artículos con cobertura técnica parcial previa

- [not_checked](https://rhino-performance.com/blog/posts/brazo-de-presoterapia-transforma-tu-experiencia-deportiva-66afbbe13c5b/)
- [not_checked](https://rhino-performance.com/blog/posts/presoterapia-el-secreto-mejor-guardado-de-los-atletas-de-elite-191a8f66c1d6/)
- [not_checked](https://rhino-performance.com/blog/posts/manga-de-compresion-frio-y-calor-el-aliado-perfecto-para-tu-entrenamiento-4f2d85d7c839/)
- [not_checked](https://rhino-performance.com/blog/posts/lo-que-tienes-que-saber-del-drenaje-linfatico-para-atletas-y-deportistas-d8be8c1a69a3/)
- [not_checked](https://rhino-performance.com/blog/posts/beneficios-de-la-siesta-despues-de-entrenar-clave-para-mejorar-el-rendimiento-fisico-y-mental-ef9f9c1ce142/)
- [not_checked](https://rhino-performance.com/blog/posts/mejora-tu-rendimiento-con-las-botas-de-presoterapia-2fc8df74a4e1/)
- [not_checked](https://rhino-performance.com/blog/posts/cuando-y-cuantas-veces-deberias-usar-la-presoterapia-78ce2c4b4e15/)
- [not_checked](https://rhino-performance.com/blog/posts/la-presoterapia-como-complemento-en-la-recuperacion-postoperatoria-5bab92e6be21/)
- [not_checked](https://rhino-performance.com/blog/posts/7-tipos-de-entrenamiento-que-debes-hacer-antes-de-correr-un-maraton-o-cualquier-carrera-244573e551fa/)
- [not_checked](https://rhino-performance.com/blog/posts/hormonas-que-hacen-que-ames-correr-d6b29d573534/)
- [not_checked](https://rhino-performance.com/blog/posts/recuperacion-muscular-en-el-futbol-americano-la-clave-para-un-mejor-rendimiento-b450f269375a/)
- [not_checked](https://rhino-performance.com/blog/posts/retencion-de-liquidos-en-atletas-por-que-ocurre-y-como-tratarla-70e0723bf879/)
- [not_checked](https://rhino-performance.com/blog/posts/en-que-situaciones-no-se-recomienda-el-uso-de-presoterapia-61b45d53ea7b/)
- [not_checked](https://rhino-performance.com/blog/posts/mangas-de-compresion-frio-y-calor-para-el-cuidado-muscular-a30fa0abf6a7/)
- [not_checked](https://rhino-performance.com/blog/posts/motivacion-deportiva-como-conseguirla-a299c19dcb3c/)
- [not_checked](https://rhino-performance.com/blog/posts/los-mejores-estiramientos-despues-de-un-entrenamiento-intenso-e60dcadb9471/)
- [not_checked](https://rhino-performance.com/blog/posts/recuperacion-deportiva-las-tecnicas-con-mayor-respaldo-cientifico-8d45b8378042/)
- [not_checked](https://rhino-performance.com/blog/posts/ejercicio-en-la-manana-antes-o-despues-de-desayunar-6b4da8f2797c/)
- [not_checked](https://rhino-performance.com/blog/posts/guia-para-el-uso-de-tus-botas-de-presoterapia-aad204c7149a/)
- [not_checked](https://rhino-performance.com/blog/posts/sacale-el-maximo-partido-a-tus-botas-de-presoterapia-6d64eb420000/)

Primero corresponde recuperar evidencia ya guardada si contiene esos campos. Si falta, habrá que presentar un alcance concreto nuevo; no se realizaron nuevos GET para rellenarlos automáticamente.

## Advertencias de datos estructurados

[Hallazgos originales de75destinos V4](V4-raw-warning-error-findings.json) y [gates por URL](V4-75-technical-observations.json). Este agregado no incluye validadores no ejecutados de las49 observaciones previas y no cuenta alertas como URLs distintas.

- **64 artículos:** cada uno conserva B030 y B100 sobre `author` como texto sin entidad tipada,128 advertencias de regla para64 URLs. La representación es un hallazgo; identidad editorial y tipo Person/Organization no están confirmados. No se inventan autores/perfiles ni se implementa automáticamente el fix sugerido.
- **11 PDP:**61 D010 con severidad error y61 de cada D011/D050/D070 con severidad warning. Corresponden a Product secundarios `structured-data.item`, comparados con canonical/H1 del PDP contenedor. D010/D050 son posibles falsos positivos contextuales; D011 conserva discrepancias de URL/codificación `amp%3B` cuyo origen/efecto faltan; D070 no acredita imagen ausente sin resolver srcset/data-src/currentSrc/red. No se deben borrar schemas ni corregir datos comerciales basándose solo en esos avisos.
- Recomendaciones de políticas, envío y otros campos opcionales se preservan en el reporte nativo sin inventar valores. El agregado CLI `findings:0` es de raíz y no anula las alertas de cada template.
- No se ha ejecutado una validación externa nueva ni observado un rechazo de Google por estas reglas. Las alertas de BreadcrumbList anteriores y sus correcciones publicadas se conservan con su propio histórico; no se certifica desaparición de Search Console sin nueva evidencia oficial.

## Google: evidencia histórica, no censo del índice

Se conservan15 inspecciones del12 noviembre2026:10`PASS`/enviada e indexada,1 descubierta sin indexar (Contacto) y4 URLexactas desconocidas (Sobre Rhino y blog2/3/8). Las109 HTML restantes carecen de inspección individual conservada; no se clasifican como no indexadas. [Quince inspecciones con fechas y canonicals](google-historical-15.csv).

Las170 filas históricas de Search Analytics con impresiones corresponden al12 octubre–8 noviembre2026 PT, origen sinwww; son URLs con impresiones en aquel informe, no170 páginas actualmente indexadas ni la totalidad del dominio.

Las10 URLs conocidas como indexadas en las inspecciones guardadas son:

- [https://rhino-performance.com/](https://rhino-performance.com/) — inspección `2026-11-12T16:13:21.011919+00:00`, último rastreo `2026-11-12T01:22:29Z`.
- [https://rhino-performance.com/productos/](https://rhino-performance.com/productos/) — inspección `2026-11-12T16:13:52.029010+00:00`, último rastreo `2026-11-12T01:48:26Z`.
- [https://rhino-performance.com/politica-de-devolucion/](https://rhino-performance.com/politica-de-devolucion/) — inspección `2026-11-12T16:14:54.571616+00:00`, último rastreo `2026-10-31T00:32:14Z`.
- [https://rhino-performance.com/productos/baterias-doble-capacidad-pro-air/](https://rhino-performance.com/productos/baterias-doble-capacidad-pro-air/) — inspección `2026-11-12T16:14:08.804757+00:00`, último rastreo `2026-10-31T08:30:01Z`.
- [https://rhino-performance.com/productos/botas-presoterapia-inalambricas-pro-air/](https://rhino-performance.com/productos/botas-presoterapia-inalambricas-pro-air/) — inspección `2026-11-12T16:14:00.477330+00:00`, último rastreo `2026-11-06T15:36:53Z`.
- [https://rhino-performance.com/presoterapia/](https://rhino-performance.com/presoterapia/) — inspección `2026-11-12T16:13:34.894824+00:00`, último rastreo `2026-11-09T08:32:41Z`.
- [https://rhino-performance.com/accesorios/](https://rhino-performance.com/accesorios/) — inspección `2026-11-12T16:13:43.562814+00:00`, último rastreo `2026-11-10T20:31:30Z`.
- [https://rhino-performance.com/blog/](https://rhino-performance.com/blog/) — inspección `2026-11-12T16:14:17.731208+00:00`, último rastreo `2026-11-12T02:53:10Z`.
- [https://rhino-performance.com/blog/posts/ejercicio-en-la-manana-antes-o-despues-de-desayunar-6b4da8f2797c/](https://rhino-performance.com/blog/posts/ejercicio-en-la-manana-antes-o-despues-de-desayunar-6b4da8f2797c/) — inspección `2026-11-12T16:15:03.420051+00:00`, último rastreo `2026-11-12T05:59:50Z`.
- [https://rhino-performance.com/blog/posts/pedaleaste-100-km-y-luego-qu-dd31584de196/](https://rhino-performance.com/blog/posts/pedaleaste-100-km-y-luego-qu-dd31584de196/) — inspección `2026-11-12T16:15:12.941331+00:00`, último rastreo `2026-10-31T00:42:43Z`.

No se consultó Google ni se comprobó de nuevo la credencial. El último diagnóstico documentado indicaba falta de credencial disponible; no se presupone acceso actual. La API usada y una muestra de URLInspection no sustituyen el informe completo de indexación de páginas. Para cobertura global, el propietario puede abrir la propiedad autorizada en Search Console → Indexación → Páginas → exportar el resumen y los ejemplos de cada motivo disponible, conservando fecha, filtros y limitación de ejemplos; no presentar esas muestras como todos los destinos. No se debe iniciar otro OAuth ni extraer cookies/tokens para este cierre.

## Dependencias de Tiendanube e inventario administrativo

La [consulta técnica preparada](../../../three-issues/operations/consulta-tiendanube.md) documenta blog2/3/8 con200, contenido distinto y canonical hacia `/blog/`. No se ha recibido aquí confirmación oficial de un mecanismo soportado para canonicals propios. Se conserva el comportamiento nativo; no se implementan head-tags duplicados o modificaciones medianteJS.

Sitemap, emisor nativo de marcado y estado de publicación del catálogo deben contrastarse con contratos/plataforma y datos administrativos autorizados antes de alterarlos. Solo se conocen cinco categorías públicas; no se acreditó que el administrador carezca de otras subcategorías ocultas/no publicadas. [Conciliación manual preparada](../admin-category-reconciliation.csv) y [procedimiento](../procedimientos-manuales.md). Los14 productos públicos no certifican stock/visibilidad de todas las variantes ni estados administrativos activos. No se modificaron datos comerciales.

La selección de canonical e indexación final corresponde a Google; la tienda puede mejorar descubrimiento y señales técnicas, no garantizar inclusión ni posicionamiento.

## Acciones priorizadas — propuestas sin ejecución

No se ha demostrado un P0 general que justifique modificar producción de inmediato. La prioridad ahora es cerrar evidencia concreta, no añadir infraestructura ni forzar indexación.

| Prioridad | ID | Acción | Estado |
|---|---|---|---|
| P1 | SEO-CLOSE-01 | Recuperar primero los campos ausentes de las capturas guardadas de20 artículos y, si no existen, preparar una comprobación acotada con autorización nueva. No repetir sus HTTP solo por rutina. | needs_evidence |
| P1 | SEO-CLOSE-02 | Contrastar cobertura con Google al recuperar acceso autorizado: priorizar /pistolas-de-masaje/, /terapia-fria/, /compresion-frio-y-calor/ y /productos/page/2/. Exportar informe oficial de indexación si se necesita cobertura global. | requires_authorized_access_and_scope |
| P1 | SEO-CLOSE-03 | Conciliar categorías públicas/subcategorías con inventario administrativo autorizado o plantilla manual; no crear categorías ni cambiar menús. | needs_administrative_evidence |
| P1 | SEO-CLOSE-07 | Revisar vías de descubrimiento de Contacto con evidencia existente; documentar alternativas sin cambiar menús ni añadir enlaces automáticamente. | needs_evidence_no_menu_changes |
| P2 | SEO-CLOSE-04 | Resolver consulta preparada a Tiendanube sobre canonical nativo de blog2..8 antes de proponer cambios. | pending_official_supported_mechanism |
| P2 | SEO-CLOSE-05 | Revisar el emisor real de author con procedencia editorial; elegir Person/Organization solo con datos verificados y revisar un diff independiente antes de implementar. | needs_contextual_review |
| P2 | SEO-CLOSE-06 | Revisar D010/D050 en su contexto secundario y D011/D070 con datos guardados; no corregir todos los PDP por un comparador global. | needs_evidence |
| P3 | SEO-CLOSE-08 | Mantener Sobre Rhino pendiente de contenido, sin promoción ni solicitud de indexación; no editar hasta autorización editorial. | deferred_by_owner |

[Backlog estructurado con causas/riesgos](prioritized-actions.json). Cualquier nuevo GET, conexión de cuenta o cambio visible exige el permiso correspondiente. Las futuras correcciones deben preservar paginación publicada, SEO, accesibilidad y rendimiento; usar baseline comparable y diff mínimo, sin prometer90+ por este controlHTML.

## Integridad, autoría y alcance del cierre

Este informe fue preparado por Codex/controlador con cálculo offline. Se reutilizaron las revisiones Claude/Codex ya válidas del motor y del [plan de lotes](../remaining-65-preparation/README.md); no se simula una revisión dual nueva del consolidado. No se repitieron suites, discovery o consultasGSC.

Los archivos y hashes originales de las15 ejecuciones se conservaron y comprobaron contra sus sellos. El lote15 actualizó solo cinco filas; el resto de120 filas y los campos Google/históricos se conservaron. La matriz125 se copia y el inventario124 se deriva excluyendo únicamente el XML; ninguna fila sin medir fue convertida a200 por estar enlazada.

[Fuentes y hashes](source-hashes.json) · [verificación del cierre](verification.json) · [sellos de los artefactos](artifact-hashes.json). Queda cerrado **el control HTTP del inventario público conocido**, con las limitaciones técnicas y de Google expresamente abiertas.
