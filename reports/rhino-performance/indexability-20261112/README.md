# Rhino — indexación y rastreabilidad de producción

**Continuación vigente:** [matriz ampliada y descubrimiento de artículos antiguos](site-continuation/README.md). Las cinco categorías y catorce productos tienen rutas HTML observadas; blog1–8 cubre los86artículos del sitemap. Matriz de125URLs conocidas, con75destinosHTML aún sin comprobación HTTP individual. La paginación del catálogo ya está publicada y no se modifica; los menús quedan fuera de alcance y Sobre Rhino pendiente de contenido. El texto siguiente conserva la auditoría inicial.

**Seguimiento posterior:** el acceso GSC se restableció y hubo consultas y revisión dual reales. Consulta [la actualización](google-followup.md) y [la matriz con estados Google](url-matrix-gsc.csv). El texto siguiente conserva el estado observado en la primera fase, cuando aún no había sesión activa.

Estado: **auditoría parcial con evidencia real; cobertura completa bloqueada**. Solo Codex. Sin invocaciones a Claude/CommandCode, sin cambios al tema ni operaciones de publicación en esta fase.

Observaciones nuevas: 12 de noviembre de 2026 UTC (11 de noviembre por la noche en Ciudad de México). [Resumen legible por máquina](summary.json), [matriz de las 117 URLs del sitemap](url-matrix.csv), [paginaciones observadas](pagination-matrix.csv), [comprobaciones](verification.json), [checkpoint de fuente](source-checkpoint.json).

## Resultado ejecutivo

- **117 URLs únicas** entre sitemap general y sitemap de blog; sus copias CDN no se cuentan de nuevo.
- **14 productos, 5 categorías, 8 páginas, 1 catálogo, 1 home, 1 blog, 86 artículos y 1 documento XML**. El XML no se considera una página comercial candidata a indexación.
- **52 rutas del inventario tienen un camino HTML observado desde home** en la muestra de documentos leídos. Incluyen los 14 productos, las 5 categorías, el catálogo, el blog, 24 artículos, 6 páginas y la home.
- Las otras **65 entradas no quedaron cubiertas por este grafo parcial**: 62 artículos, 2 páginas y el documento XML. No son 65 huérfanas confirmadas.
- **26 URLs del sitemap tienen observación HTTP 200** al reunir seis URLs de los GET nuevos y veinte artículos del postcheck anterior. No todas esas observaciones tienen auditoría SEO completa. La séptima página nueva es `/blog/?page=2`, fuera del sitemap.
- **Indexadas en Google: no determinado**. No significa cero. No hay credencial GSC activa; las capturas históricas de advertencias acreditan lo que informó aquella interfaz, no el estado actual de todo el índice.
- Dos problemas actuales reproducidos: botón del catálogo sin href y canonical de página 2 del blog hacia página 1. No se demuestra que hayan excluido URLs del índice.
- **Ningún bloqueo P0 general de la tienda demostrado** en estas comprobaciones.

## Alcance y método

No se volvió a hacer discovery ni se consumió PageSpeed. Se recuperaron los informes integrales y el postcheck del arreglo de BreadcrumbList ya publicado. La autorización de aquel despliegue no se reutiliza para otro cambio.

El Crawler V4 **no se ejecutó**: [su entrega final](../../seo/v4-source-review/delivery.json) registra `workspace_applied:false`, `implementation_allowed:false`, consejo `needs_evidence`. La [revisión](../../seo/v4-source-review/README.md) exige recibo QA del candidato y revisión válida. No se instaló el candidato, no se cambió el transporte y no se creó otro crawler para sustituirlo.

Se hicieron dos lecturas explícitas de documentos conocidos (robots y sitemap) y una lista cerrada de diez documentos: dos XML CDN declarados por robots, el XML de blog conocido y siete páginas conocidas. Sin cola de descubrimiento, sin recorrer productos/artículos del XML, sin ampliar el lote. GET, pausas de 2 s, timeout 25 s, máximo 3 MB por cuerpo/descompresión, destinos de redirección acotados, parada ante 403/429. Ninguna de estas doce lecturas devolvió 403/429. Los bloqueos de otras rutas de fases anteriores no se reintentaron.

Evidencias originales: [inventario y documentos](../../runs/rhino-performance/20261112T043917-indexability-inventory-223e7de9/). `inventory.json`, `robots.txt`, `sitemap.xml`, `known-documents.json`, XML secundarios, `internal-link-graph.json` y `pagination-observations.json`. Se conserva hash del cuerpo y momento de cada respuesta; no cookies, credenciales ni cuerpos HTML con tokens de apps.

El grafo se calcula **offline** sobre los enlaces extraídos de siete HTML iniciales, sin visitar sus destinos automáticamente. Para asociar rutas se normaliza únicamente la barra final y se conserva query; se guardan los href originales. Esa asociación no certifica las redirecciones de todas las variantes ni el canonical seleccionado por Google. Los enlaces pueden estar en menús o carruseles; presencia HTML no equivale a accesibilidad visual o por teclado validada en todos sus estados.

## Sitemap y robots

| Documento | HTTP | Entradas | XML / duplicados internos |
|---|---:|---:|---|
| `/sitemap.xml` | 200 | 30 | Válido; ninguno |
| CDN general declarado por robots | 200 | 30 | Mismo conjunto que el general |
| `/sitemap_blog.xml/` | 200 | 87 | Válido; ninguno |
| CDN blog declarado por robots | 200 | 87 | Mismo conjunto que el blog |

Los dos documentos son `urlset`; no hay necesidad de convertirlos a `sitemapindex`. Robots declara dos sitemaps reales en `acdn-us.mitiendanube.com/stores/007/400/935/themes/common/`. No se inventaron sitemaps hijos.

El general contiene 26 `lastmod` válidos como fechas declaradas y 4 ausentes; el blog no declara `lastmod`. Ausencia no equivale a error ni autoriza inventar fechas. La veracidad de actualización editorial no se comprobó.

Robots restringe admin, cuenta, checkout/carrito, búsqueda interna, drafts, preview y endpoints `view`. Son exclusiones esperables; no se recomienda abrirlas. No se observó una regla wildcard que bloquee las rutas públicas del inventario. Esto es revisión de las reglas observadas, no certificación del parser V4 pendiente. El origen registrado y leído es **sin www**; no se repitió el 403 histórico de www ni se afirma que ambos hosts tengan estado idéntico.

## Matriz y resumen por plantilla

| Tipo | Sitemap | Con camino HTML observado en muestra | HTTP observado nuevo o reutilizado |
|---|---:|---:|---|
| Home | 1 | 1 | Home actual 200 |
| Catálogo | 1 | 1 | `/productos/` actual 200 |
| Categorías | 5 | 5 | `/presoterapia/` actual 200; demás no solicitadas en este lote |
| Productos | 14 | 14 | PRO AIR actual 200; demás no solicitados en este lote |
| Páginas | 8 | 6 | Política de devolución actual 200 |
| Blog | 1 | 1 | Portada actual 200 |
| Artículos | 86 | 24 | 20 postchecks anteriores reutilizados con su fecha |
| Documento sitemap | 1 | 0 | XML leído; no es contenido comercial |

La matriz no rellena con “aprobado” lo no medido: `not_requested`/`not_checked`, observación y origen separados, estado Google desconocido. La candidatura técnica completa no se certifica ni siquiera por obtener HTTP 200.

Las dos páginas sin enlace observado en esta muestra son `/contacto/` y `/sobre-rhino-performance/`. Antes de añadir enlaces hay que comprobar menús, footer, páginas actuales y pertinencia comercial. No se certifican como huérfanas sin revisar las fuentes restantes.

## Categorías, productos y LS.hybridScroll

`/presoterapia/` responde 200, canonical propio, H1 PRESOTERAPIA, sin meta/X-Robots restrictivo observado y sin errores de JSON-LD en esta captura. No ofrece carga posterior en su HTML actual; el número total de enlaces del header no se confunde con productos de su grid.

`/productos/` muestra doce destinos de producto en el contenido principal y “Mostrar más productos” como `<a class="btn btn-primary">` **sin href**. Hay rutas adicionales hacia productos en la navegación. Los catorce productos del sitemap también tienen enlaces HTML desde home; por eso no se afirma que los dos que no están en este grid inicial sean invisibles para Google.

Fuentes locales inspeccionadas:

- `sections/main-products-grid.tpl`: `paginate by 12` en infinite; `paginate by 60` en classic; conserva render nativo de cards.
- `snippets/product-list/pagination.tpl`: calcula `page_next.url`/`pages.next`; la rama infinite omite href; la rama classic utiliza los enlaces de plataforma.
- `static/js/store.js:initInfiniteScroll`: `LS.hybridScroll` usa `.js-product-table`, `.js-load-more`, umbral 60, 12 por página y reinicialización del slider de cards.
- `templates/pages/category.json`: configuración local infinite.

El HTML publicado coincide con el defecto de esa rama; los hashes locales no certifican por sí solos que todos esos archivos sean byte a byte los remotos. No se extrajo todavía la implementación interna publicada de LS ni se comprobó su interceptación de eventos o sincronización de filtros/cursor. No se inventó `/productos/?page=2` ni se la consultó por conjetura.

Alternativas: (A) configuración classic nativa; cambia 12 a 60 y puede aumentar DOM/transferencias, por lo que no se propone aplicar sin pruebas. (B) mantener infinite y ofrecer navegación progresiva usando URLs reales suministradas por plataforma; exige comprobar cursor, filtros, paginación posterior, teclado y no duplicación de productos. **B es candidata, no implementación aprobada**. Un href estático al primer destino puede quedar obsoleto después de cargar más: no basta agregarlo sin estudiar LS.

La captura real sin JavaScript de `/presoterapia/` del 10 de noviembre se conserva como antecedente, no se presenta como repetición actual de todo el catálogo. HTML inicial confirma enlaces disponibles antes de ejecutar JS, pero falta QA actual del flujo completo sin JS.

## Blog y artículos

Se reprodujo `/blog/?page=2` desde un href real: HTTP 200; doce artículos distintos de los doce de la portada, **cero solapamiento**. Hay href reales a páginas 1, 2, 3, 4 y 8 según la posición; la página 2 ofrece enlace real a la 3. No se solicitó 3–8 ni se concluye que toda la cadena esté cubierta. De los 86 artículos del sitemap, 24 tienen camino observado en esta muestra; los otros 62 siguen sin comprobar por enlazado.

**Canonical confirmado:** `/blog/?page=2` declara `https://rhino-performance.com/blog/`, pese al contenido distinto. Es una señal de consolidación a revisar; no prueba qué canonical eligió Google. Google recomienda URLs propias y canonical propio en páginas de una secuencia: [guía oficial](https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading).

El layout normal delega metadatos a `component('head-tags')`; los canonicals explícitos de las ramas `view=cards`/`view=tags` pertenecen a endpoints auxiliares noindex, no se confunden con el blog público. Falta comprobar el mecanismo soportado de la plataforma antes de sobrescribir el canonical o duplicarlo en el tema. La paginación se compone en `sections/main-blog.tpl` y `snippets/blog/blog-pagination.tpl`; `static/js/blog-listing.js` reconstruye la versión filtrada y es consumidor obligatorio de cualquier cambio de navegación.

El anterior SEO011 del blog señaló también la flecha anterior deshabilitada. El snippet actual tiene `aria-disabled="true"` y `tabindex="-1"`; no es un destino posterior perdido ni se cuenta como bloqueo de rastreo.

El arreglo previo de BreadcrumbList se conserva: veinte artículos verificados tras su despliegue, sin repetir las veinte solicitudes. No se afirma que Google haya validado la corrección. Dos rutas históricas con artículo no identificado/no BreadcrumbList quedan fuera de la certificación; no se reintenta el 403 observado ni se concluye que restaurarlas sea correcto sin comprobar su estado editorial.

## SEO, accesibilidad y rendimiento

Las siete páginas nuevas respondieron 200 y no mostraron errores de sintaxis JSON-LD. No se interpreta ese resultado como semántica perfecta, elegibilidad Google ni indexación. En los siete HTML se encontraron title, descripción, H1 y canonical; las descripciones de blog son genéricas (“Blog”) y constituyen una mejora editorial posible, no un bloqueo probado.

No se midieron de nuevo LCP/TBT/CLS: no hay cambio a comparar y ya existen baselines. No se publicaron enlaces ocultos, nuevos scripts, schemas, imágenes, CSS ni cambios de tipografía. Toda futura corrección deberá contrastar HTML y DOM, teclado, seis anchos, enlaces, canonical único, datos comerciales y perfiles de rendimiento equivalentes. No se promete 90+ como consecuencia de corregir enlaces.

## Google: información pendiente

GSC tiene la propiedad `sc-domain:rhino-performance.com` configurada, sin credencial activa disponible al inicio. Se abrió una vez el flujo existente OAuth con scope `webmasters.readonly`, bajo la autorización previa; la espera expiró sin consentimiento completado y no se consultó Search Console. Para continuar habrá que completar una sesión nueva desde la cuenta propietaria. No se guardaron secretos en este reporte.

La API ofrece Search Analytics, Sitemaps, Sites e inspección individual, no un inventario completo del informe de indexación: [referencia oficial](https://developers.google.com/webmaster-tools/v1/api_reference_index). La inspección devuelve el estado conocido por Google, **no una prueba en vivo**: [contrato oficial](https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect).

Pendiente: sitemaps registrados/errores, URLs con impresiones en un periodo explícito, inspecciones de muestra con último rastreo y canonical Google. Para recuentos exhaustivos de estados se necesitan exportaciones oficiales del informe de Páginas (incluyendo límites de exportación y fecha); una muestra API no sustituye ese total. Tener sitemap o verificación de dominio no acredita indexación.

## Decisión y siguiente paso

**needs_evidence** para cambios de tema. Priorizar la navegación del catálogo y el canonical del blog; preservar el comportamiento comercial y el arreglo previo. [Backlog con riesgos, pruebas y reversión](backlog.json).

Primero completar GSC y resolver el bloqueo de revisión/integración del crawler. Después preparar el lote inicial revisable (máximo 30 URLs, profundidad 4, 0,5 solicitudes/s, 120 s, protección de rutas y parada 403/429), revisar su resultado antes de solicitar ampliación. Estos límites son una propuesta conservadora heredada del ADR V4, no un rastreo ya ejecutado.

No hay diff de tema ni cambios remotos en esta fase. No se solicita autorización para un despliegue todavía: no existe un candidato que haya cerrado sus pruebas y revisión obligatorias.
