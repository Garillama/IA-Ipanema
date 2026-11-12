# Rhino — seguimiento real de Search Console y consejo dual

12 de noviembre de 2026. **Auditoría ampliada, sin modificaciones al tema ni producción. Decisión de implementación: needs_evidence.** Este seguimiento actualiza el bloqueo de acceso GSC del informe anterior; no cambia retroactivamente sus observaciones.

[Inventario base](README.md) · [Matriz actualizada de 117 URLs](url-matrix-gsc.csv) · [13 inspecciones](gsc-inspections.csv) · [170 filas de rendimiento](gsc-search-pages.csv) · [Resumen/API/modelos](google-summary.json) · [Backlog con propuestas y riesgos](backlog-dual-followup.json) · [Verificación](followup-verification.json).

## Resultados de Google

La propiedad `sc-domain:rhino-performance.com` respondió mediante OAuth `webmasters.readonly`; acceso `siteFullUser` comprobado. Se usó la puerta existente, permisos temporales de Codex para esta tarea, sin compartir tokens con workers y revocando el permiso al terminar el lote. No se enviaron sitemaps ni solicitudes de indexación.

| Resultado de URL Inspection | URLs de la muestra |
|---|---:|
| Enviada e indexada / PASS | 10 |
| Descubierta: actualmente sin indexar | 1 |
| Google no reconoce esta URL | 2 |
| Total inspeccionado | 13 |

Las diez confirmadas son home, Presoterapia, Accesorios, catálogo, PRO AIR, baterías, blog, política de devolución y dos artículos (Ejercicio en la mañana; Pedaleaste 100 km). **No son el total de páginas indexadas del dominio.** Doce URLs inspeccionadas pertenecen al sitemap; la adicional es blog página 2.

Los tres casos pendientes son:

- `/contacto/`: descubierta sin indexar. GET posterior: 200, template-contact, texto principal de 726 caracteres, sin indicio textual de 404 en esa captura. No se inventa una causa de exclusión por cantidad de texto.
- `/sobre-rhino-performance/`: Google no reconoce esa URL exacta. GET posterior: 200, texto principal de 455 caracteres, canonical propio. No significa que Google rechace toda la tienda.
- `/blog/?page=2`: URL exacta no reconocida. No devuelve canonical seleccionado ni un rastreo que permita atribuir el estado al canonical de portada observado en producción. Esa relación sigue siendo hipótesis.

Las dos páginas institucionales no tenían camino observado en la muestra anterior de siete documentos. Sus respuestas 200 y sus estados GSC justifican investigar navegación contextual/menús; todavía no certifican orfandad ni prueban qué enlace falta.

La inspección del artículo de Ejercicio devuelve Rutas de exploración `PASS`, sin incidencias en los elementos devueltos, con último rastreo `2026-11-12T05:59:50Z`, posterior al arreglo anterior. Es evidencia positiva para **ese artículo**, no cierre de todos los casos del informe de mejoras ni garantía de presentación enriquecida.

## Rendimiento en búsqueda y límites

Consulta web final, dimensión page, del **2026-10-12 al 2026-11-08**, fechas inclusivas en zona PT de la API, límite 1000, inicio 0. Filtro explícito del origen `https://rhino-performance.com/`; excluye www, HTTP y otros subdominios de la propiedad. No representa el tráfico agregado completo de la propiedad.

- 170 URLs exactas devueltas con datos del periodo; suma de esas filas: 1.543 clics y 66.373 impresiones.
- 104 URLs coinciden exactamente con el inventario de 117 entradas.
- Al normalizar la barra final, 108 filas se asocian a esas mismas 104 rutas; no se cuentan como otras cuatro páginas del sitemap. La matriz toma las métricas de la URL exacta, sin mezclar sus alias.
- Las restantes filas incluyen otras rutas históricas o variantes: no se propone forzarlas a indexar ni se supone que continúen publicadas sin comprobar HTTP/canonical.

La consulta inicial sin filtro fue rechazada durante la validación local del adaptador (`IpanemaError`, causa detallada no conservada). Se preservó el sitemap obtenido y se hizo una consulta nueva, explícitamente acotada al origen registrado. No se deshabilitó la validación ni se reinterpretó ese fallo como un estado de Google. No hubo evasión de 403/429.

La API devuelve filas principales, no garantiza todas las filas; ausencia en el periodo no prueba cero impresiones históricas ni falta de indexación. [Contrato oficial de Search Analytics](https://developers.google.com/webmaster-tools/v1/searchanalytics/query).

## Sitemap registrado

Search Console lista un sitemap registrado: `/sitemap.xml`, descargado `2026-11-11T21:15:12.583Z`, sin procesamiento pendiente, **0 errores y 0 advertencias**. El resultado contiene 30 URLs web enviadas y 104 imágenes. El campo `contents.indexed` devuelve 0, pero no se utiliza como total de indexación: las inspecciones individuales confirman diez URLs indexadas.

El sitemap de blog de 87 entradas sigue declarado en robots y fue leído correctamente en la fase anterior. No aparece como registro separado en esta respuesta GSC. Esto no prueba que Google no lo descubra; registrarlo sería una operación separada que exige autorización específica y no se ejecutó.

El inventario sigue siendo 117 URLs únicas: 14 productos, 5 categorías, 8 páginas, 86 artículos, home, catálogo, blog y un XML. No se descargaron otra vez todos los sitemaps ni se hizo un rastreo masivo.

## Contrato real de LS.hybridScroll

Se inspeccionó la función publicada en navegador, hash SHA256 `9dc0e47a547cf88dc0a2f11f416f7338b594a91a7bd2021b775a36b131ccf4a3`, 4.381 caracteres. Es una lectura de la función real, no una reimplementación.

La función genera rutas `/page/N/`, combina parámetros con `LS.urlParams`, solicita resultados parciales y actualiza el historial con `mpage`. También maneja cursores de variantes cuando se activa esa opción; no se verificaron todas sus ramas ni filtros por observar únicamente el caso sin filtros.

**Experimento de scroll de lectura en el catálogo publicado:**

1. Grid inicial: 12 IDs únicos.
2. Scroll hasta el grid: petición nativa real a `/productos/page/2/`, `results_only=true`, `limit=12`, respuesta 200.
3. Grid posterior: 14 IDs únicos; los primeros doce conservan su orden, se añaden dos, sin duplicados en esta muestra.
4. GET separado de la ruta completa **observada**, sin inventar `?page=2`: HTTP 200, canonical propio `/productos/page/2/`, enlaces de los dos productos en HTML inicial (baterías y compresor).

Esto resuelve la existencia de una ruta pública posterior del catálogo actual. No demuestra todavía continuidad de un catálogo de más páginas, conservación efectiva de filtros/ordenamientos ni un parche progresivo de Twig. **No hace falta sustituir LS para resolver un problema que LS no ha demostrado causar.**

El control `.js-load-more a` carece de href, role y tabindex; `focus()` no lo enfoca en el estado observado. La propia función oculta el control durante el autoscroll y lo muestra tras un umbral; el catálogo actual de catorce productos no recorre todos esos estados. No se etiqueta la prueba de focus como validación completa del recorrido de teclado ni se atribuye exclusivamente al href el resultado en un control oculto.

Alternativa preferida por el análisis del controlador: conservar el sistema nativo y preparar navegación progresiva visible que use enlaces de plataforma comprobados. Falta comprobar el valor real de `next_link`, actualización de estado tras append, filtros y revisión del diff. El modo classic nativo cambia la tanda de 12 a 60: no se adopta sin medir DOM/recursos y revisar UX.

## Navegador, no-JS y accesibilidad

Se reutilizó `tools/qa_browser.mjs` y sus protecciones de lectura. Cuatro capturas nuevas, Chrome automatizado, 390 px: catálogo y blog página 2, con JavaScript y sin JavaScript. POST y operaciones comerciales bloqueados; esa política puede cambiar el comportamiento de apps y se conserva como limitación.

- Ambos documentos responden 200; blog página 2 conserva doce enlaces de artículos en ambos modos.
- Se reproduce canonical de blog página 2 hacia portada también sin JS.
- El runner **no aprueba** el conjunto: detecta imágenes esenciales sin cargar sin JavaScript en ambas páginas y contraste insuficiente en `.blog-pagination-ellipsis` con JS. Son tres comprobaciones fallidas conservadas, no ocultadas.
- Hay una comprobación ARIA incompleta de axe; requiere inspección específica, no se presenta como infracción confirmada.
- Catálogo no tuvo violaciones axe reportadas en esta captura móvil; eso no certifica WCAG ni sustituye teclado o seis anchos.

No hay cambio de recursos o baseline que justifique repetir PageSpeed/Lighthouse. No se afirma mejora de LCP/TBT/CLS ni cumplimiento de90+. Antes de cualquier parche se exigen perfiles equivalentes, responsive, noJS, foco, canonical único y conservación de comercio.

## Consejo real: propuestas, objeciones y límite

Ambos smokes reales aprobaron autenticación/disponibilidad: Claude y Codex. CommandCode no se invocó.

El consejo leyó el mismo documento factual, con fragmentos de código y las respuestas GSC, sin propuestas de pares en la primera ronda. [ADR del controlador ADR-79345cdd49e2](../../runs/rhino-performance/20261112T161634-orchestration-d54ada0f/council/adr.json).

- **Claude:** investigar antes de cambiar; comprobar la navegación del catálogo y el mecanismo nativo del canonical. Sugirió estudiar classic, pero inicialmente lo describió erróneamente como 12 por página; corrigió esa lectura a60 en el contraste. Su alternativa de canonical quedó retirada hasta demostrar una vía soportada.
- **Codex:** limitar la aprobación a investigación acotada; distinguir canonical observado del elegido por Google, completar navegación y estado de institucionales, sin tocar el transporte V4 ni autorizar un cambio de tema.
- Hubo dos propuestas válidas, contraste de ambos, diez objeciones y cuatro preguntas concretas. Se conservan dos respuestas de Claude. **La defensa de Codex no se ejecutó**; no hay deliberación completa ni decisión conjunta aprobada.

Causa: primera propuesta de Claude excedía el alcance de archivos y el contrato la rechazó. El reintento autorizado de ese proveedor fue válido. Consumió una de las seis llamadas totales permitidas; al llegar a la última defensa, el presupuesto estaba agotado. No fue fallo de autenticación ni silencio del agente. Se conservaron propuestas, contraste y defensa válida; no se repitieron para simular éxito ni se amplió el presupuesto de recuperación.

El router clasificó esta revisión de un documento como L1 y `--council full` forzó participación dual con dos intercambios. Modelos registrados realmente usados: `claude-haiku-5-5`, esfuerzo low; `gpt-6-luna`, low. Esa clasificación automática de lectura no convierte un futuro cambio compartido en L1: su riesgo y revisión deberán evaluarse antes de implementar.

Seis invocaciones reales de consejo, 159,665 s sumando duraciones individuales (hay concurrencia; no es tiempo total de reloj). Coste reportado de Claude: USD0,03649437; Codex no informó coste, por lo que no se inventa un coste total. Tokens, duración y contratos por invocación están en `google-summary.json`. Los smokes quedan separados.

Los experimentos de scroll y la documentación oficial se obtuvieron después del snapshot del consejo. Son **nueva evidencia del controlador**, no opiniones que se atribuyan retroactivamente a los participantes ni aprobación de un parche.

## Decisión, prioridades y límites

**needs_evidence**, sin diff de tema, sin publicación y sin aprobación dual completa.

1. **P1:** conservar infinite y comprobar navegación progresiva nativa del catálogo con ruta posterior ya demostrada. Filtros, sincronización y revisión exacta siguen pendientes.
2. **P1:** verificar caminos internos a Contacto y Sobre Rhino antes de sugerir enlaces visibles contextuales. Sus estados GSC ya están documentados; causa no determinada.
3. **P1:** completar cobertura del enlazado a artículos antiguos cuando el crawler esté aprobado. No llamar huérfanos a los62artículos no cubiertos por la muestra anterior.
4. **P2:** resolver con Tiendanube el canonical de paginaciones del blog. La [documentación oficial](https://tiendanube.dev/es-AR/themes/sectionable-themes/seo) confirma que el canonical lo genera `head-tags` y advierte contra duplicarlo. No se ha demostrado un override soportado; no se agrega un segundo canonical.
5. **P2:** revisar los hallazgos de imágenes noJS y contraste con evidencia visual y consumidores antes de modificar componentes.

El Crawler V4 continúa sin integración/aprobación de su candidato exacto. Esta auditoría no reabre ni certifica aquel parche. Deben cerrarse su recibo QA/revisión obligatorios antes de ejecutar un primer rastreo acotado; tampoco se escribió un crawler alternativo. La ampliación posterior requiere revisión del primer lote y autorización de alcance.

Para totales completos de indexación se necesita exportación oficial del informe de Páginas, fechada y con sus límites. La API de inspección por URL y las170filas de rendimiento no sustituyen ese inventario.

Se preservaron seis hashes del tema y los cambios ajenos. Doce predicados de integridad de evidencias aprobaron; **no son doce pruebas de conformidad SEO o de la tienda**. Los fallos del navegador, el consejo incompleto y el crawler bloqueado siguen registrados. El backlog incluye propuestas atribuidas, objeciones, fuentes, alternativas, riesgos, pruebas y reversión para preparar una futura operación específica revisable.
