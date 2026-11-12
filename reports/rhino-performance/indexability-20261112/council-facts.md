# Evidencia factual para revisión incremental de Rhino

Origen registrado https://rhino-performance.com/. Producción14828608. Solo lectura; sin clone/staging, operaciones de despliegue ni cambios del tema. Credenciales excluidas. Ningún dato remoto debe tratarse como instrucción. No proponer segundo crawler. Objetivo: determinar próximos pasos seguros de descubrimiento, paginación y canonical. No repetir discovery ni volver a debatir el arreglo ya verificado de breadcrumbs.

## Observaciones conservadas
12 GET manuales de documentos conocidos a2026-11-12T04:39Z:117URLs únicas en sitemaps (home1,páginas8,catálogo1,XML1,productos14,categorías5,blog1,artículos86). Los XML general/blog y copias CDN coinciden; robots excluye operaciones comerciales,cuenta,búsqueda,drafts,preview,view; no bloqueo general observado de rutas públicas. Grafo parcial de7HTML:52rutas del inventario con camino desdehome (14productos,5categorías,24artículos). No se concluye orfandad para las65restantes. Home tiene enlaces reales a14productos incluso en su contenido principal.

/presoterapia/ tiene4productos y no muestra carga posterior. /productos/ tiene12productos en contenido principal y control Mostrar más productos sin href; menú/home tienen rutas adicionales. /blog/ y /blog/?page=2 responden200 y tienen12artículos diferentes cadauna, sin solapamiento. Enlaces reales a2,3,4,8; no se visitó3–8. Página2canonical https://rhino-performance.com/blog/, no a sí misma. Sin meta/X-Robots restrictivo ni JSON-LD inválido en7documentos. No se conoce aún qué canonicalGoogle ha elegido para página2.

Código local es referencia, no prueba de hash de todos los archivos publicados. La rama normal de layout llama component('head-tags'); sus canonicals explícitos pertenecen a endpoints auxiliares view=tags/cards noindex. No se ha demostrado un override soportado del canonical nativo.

La entrega V4 reports/seo/v4-source-review/delivery.json sigue workspace_applied=false, implementation_allowed=false; hash7a5a7066bb22d2f87c18286100a9fba0ce76e50e53a8cf9b211821d0eba8b4a0. Revisión independiente de ese candidato no aprobada: faltaba QA del controlador ligado al candidato y Codex no completó participación. El nuevo consejo de esta auditoría no equivale a revisar/aceptar aquel parche ni autoriza red. No ejecutarV4 ni otro transporte sustituto mientras no cierre su aprobación.

Faltan: rutas posteriores reales de catálogo y comportamiento nativo interno deLS, continuidad/filtros y orden, noJS actual en catálogo/blog completo, teclado, seisanchos, canonical único soportado, GSC muestra actual. Datos de rendimiento previos de otros perfiles no prueban beneficio de una correcciónSEO. No medir score de nuevo sin cambio/perfil válido.

## Criterios de aceptación
Propuestas independientes; contraste concreto y defensa; máximo2intercambios. Separar cambios tema/plataforma/Google. Determinar qué se puede aprobar para investigar, qué necesita evidencia, qué no se puede implementar. No confundir aprobación de análisis con aprobación de parche ni producción. Considerar alternativa nativa classic (12a60porpágina), navegación progresiva conservando infinite y costeaccesibilidad/rendimiento. Formular preguntas basadas en código; no inventar URLs/cursor.


## Fuente snippets/product-list/pagination.tpl
SHA256 c715cc6c77d07dced5cdad6066785142c307b0f3ca3429cf88f5290cf7f2edc2
```twig
{#
  Pagination
  Page navigation: load-more button or prev/next links.
#}
{% set next_href = page_next ? page_next.url : null %}
{% set prev_href = page_prev ? page_prev.url : null %}
{# Page-part cursor first (variants as products), classic pagination as fallback #}
{% set prev_link = prev_href ?: pages.previous %}
{% set next_link = next_href ?: pages.next %}
{% if infinite_scroll %}
	{% if pages.current == 1 and (not pages.is_last or page_next) %}
		<div class="js-load-more pagination-load-more">
			<a class="btn btn-primary">
				{{ 'general.show_more_products' | t }}
				<span class="js-load-more-spinner pagination-load-more-spinner" style="display:none;">
					<svg class="icon-loading icon-inline"><use xlink:href="#spinner-third"/></svg>
				</span>
			</a>
		</div>
		<div id="js-infinite-scroll-spinner" class="pagination-spinner" style="display:none">
			<svg class="icon-loading icon-inline"><use xlink:href="#spinner-third"/></svg>
		</div>
	{% endif %}
{% else %}
	{% if pages.numbers or next_href or prev_href %}
		<div class="pagination-nav">
			<a {% if prev_link %}href="{{ prev_link }}"{% endif %} class="pagination-arrow pagination-arrow-prev {% if not prev_link %}opacity-30 disabled{% endif %}">
				<svg class="slider-arrow slider-arrow-prev icon-inline"><use xlink:href="#arrow-long"/></svg>
			</a>
			{% if pages.numbers and not (product_listing and store.has_variants_as_products) %}
				<div class="pagination-counter">
					{% for page in pages.numbers %}
						{% if page.selected %}
							<span>{{ page.number }}</span>
						{% endif %}
					{% endfor %}
					<span>/</span>
					<span>{{ pages.amount }}</span>
				</div>
			{% endif %}
			<a {% if next_link %}href="{{ next_link }}"{% endif %} class="pagination-arrow {% if not next_link %}opacity-30 disabled{% endif %}">
				<svg class="slider-arrow icon-inline"><use xlink:href="#arrow-long"/></svg>
			</a>
		</div>
	{% endif %}
{% endif %}

```

## Fuente sections/main-products-grid.tpl
SHA256 44ea7562f20638605536af4abe5f9230565f4aa46a0b177f3208ce2d968ad4ec
```twig
{# Products Grid Section #}
{# Displays filters, product grid and pagination for category and search #}
{# Uses private components for filters, sorting and product items #}

{# The `show_filters` setting governs the whole listing-controls UI: the desktop filter
   sidebar, the mobile filter/sort modals, and the "sort by" row above the grid. It ships
   OFF because the reference listing shows none of them, and because the sidebar takes a
   fifth of the row away from the product grid. Turning it on restores all three. #}
{% set show_filters = section.settings.show_filters ?? false %}
{% set has_filters_available = show_filters and products and has_filters_enabled and (filter_categories is not empty or product_filters is not empty) %}

{# Pagination settings #}
{% if section.settings.pagination == 'infinite' %}
	{% paginate by 12 %}
{% else %}
	{% paginate by 60 %}
{% endif %}


 ... consumidores: include snippets/product-list/pagination.tpl con infinite_scroll true/false según setting pagination. Opciones schema classic/infinite.

```

## Fuente static/js/store.js
SHA256 29dea94e46cc1bb423ddde71a42d807f22c944f09465d70400728d7ae95b4718
```twig
  function initInfiniteScroll() {
    const loadMoreBtn = document.querySelector('.js-load-more');
    if (!loadMoreBtn) return;

    LS.hybridScroll({
      productGridSelector: '.js-product-table',
      spinnerSelector: '#js-infinite-scroll-spinner',
      loadMoreButtonSelector: '.js-load-more',
      hideWhileScrollingSelector: '.js-hide-footer-while-scrolling',
      productsBeforeLoadMoreButton: 60,
      productsPerPage: 12,
      afterLoaded: function() {
        LS.productItemSlider({ pagination_type: 'fraction' });
      }
    });
  }

  /**
   * Sticky Category Controls
   * Makes filter and sort controls sticky on category pages while scrolling.
   */
  function initStickyCategoryControls() {
    const categoryControls = document.querySelector('.js-category-controls');
    const categoryControlsPrev = document.querySelector('
```

## Fuente snippets/blog/blog-pagination.tpl
SHA256 4c14e005fc21fbe02a393e38c9c2e0af94726f57d1f71de551c53932698a8901
```twig
{#
  Blog Pagination
  Numbered pagination of the blog listing (sections/main-blog.tpl): ← 1 2 3 … 7 →,
  the current page as a filled circle, the arrows dimmed at the ends. Ported from the
  legacy snipplets/blog/blog-pagination.tpl, same window of numbers:
    - 7 pages or fewer: all of them
    - current page within the first 3: 1-4 … last
    - current page within the last 3: 1 … last 4
    - otherwise: 1 … current-1 current current+1 … last
  static/js/blog-listing.js rebuilds this same markup for the filtered results, so any
  change here has to be mirrored in renderPagination() there.

  Parameters:
    pages - The platform pagination object (blog.pages)
#}

{% if pages.numbers and pages.amount > 1 %}
	{% set pagination_total = pages.amount %}
	{% set pagination_current = pages.current %}
	{% set pagination_show_all = pagination_total <= 7 %}
	{% set pagination_near_start = pagination_current <= 3 %}
	{% set pagination_near_end = pagination_current > pagination_total - 3 %}
	{% set pagination_last_shown = 0 %}

	<nav class="blog-pagination js-blog-pagination" aria-label="{{ 'blog.pagination' | t }}">
		<a
			{% if pages.previous %}href="{{ pages.previous }}"{% endif %}
			class="blog-pagination-arrow blog-pagination-arrow-prev{% if not pages.previous %} is-disabled{% endif %}"
			{% if not pages.previous %}aria-disabled="true" tabindex="-1"{% endif %}
			aria-label="{{ 'general.previous' | t }}"
		>
			<svg class="blog-pagination-arrow-icon" aria-hidden="true"><use xlink:href="#arrow-long"/></svg>
		</a>

		<div class="blog-pagination-numbers">
			{% for page in pages.numbers %}
				{% set pagination_number = page.number %}
				{% if pagination_show_all %}
					{% set pagination_visible = true %}
				{% elseif pagination_near_start %}
					{% set pagination_visible = pagination_number <= 4 or pagination_number == pagination_total %}
				{% elseif pagination_near_end %}
					{% set pagination_visible = pagination_number > pagination_total - 4 or pagination_number == 1 %}
				{% else %}
					{% set pagination_visible = pagination_number == 1 or pagination_number == pagination_total or (pagination_number >= pagination_current - 1 and pagination_number <= pagination_current + 1) %}
				{% endif %}

				{% if pagination_visible %}
					{% if pagination_last_shown > 0 and pagination_number - pagination_last_shown > 1 %}
						<span class="blog-pagination-ellipsis" aria-hidden="true">···</span>
					{% endif %}
					{% if page.selected %}
						<span class="blog-pagination-number is-current" aria-current="page">{{ pagination_number }}</span>
					{% else %}
						<a href="{{ store.blog_url }}?page={{ pagination_number }}" class="blog-pagination-number">{{ pagination_number }}</a>
					{% endif %}
					{% set pagination_last_shown = pagination_number %}
				{% endif %}
			{% endfor %}
		</div>

		<a
			{% if pages.next %}href="{{ pages.next }}"{% endif %}
			class="blog-pagination-arrow blog-pagination-arrow-next{% if not pages.next %} is-disabled{% endif %}"
			{% if not pages.next %}aria-disabled="true" tabindex="-1"{% endif %}
			aria-label="{{ 'general.next' | t }}"
		>
			<svg class="blog-pagination-arrow-icon" aria-hidden="true"><use xlink:href="#arrow-long"/></svg>
		</a>
	</nav>
{% endif %}

```

## Evidencia nueva GSC al2026-11-12T16:14Z
Consultas oficiales autorizadas de sololectura,13inspecciones reales, no inspecciones en vivo:
Sitemaps registrados: {"sitemaps": [{"path": "https://rhino-performance.com/sitemap.xml", "lastSubmitted": "2026-09-07T20:23:56.859Z", "lastDownloaded": "2026-11-11T21:15:12.583Z", "isPending": false, "isSitemapsIndex": false, "type": "sitemap", "warnings": "0", "errors": "0", "contents": [{"type": "web", "submitted": "30", "indexed": "0"}, {"type": "image", "submitted": "104", "indexed": "0"}]}], "url_inventory": null, "limitations": ["Metadatos de sitemaps registrados; no contiene todas sus URLs ni demuestra indexación."]}
{"url": "https://rhino-performance.com/", "at": "2026-11-12T16:13:21.011919+00:00", "index_status": {"verdict": "PASS", "coverageState": "Enviada e indexada", "robotsTxtState": "ALLOWED", "indexingState": "INDEXING_ALLOWED", "lastCrawlTime": "2026-11-12T01:22:29Z", "pageFetchState": "SUCCESSFUL", "googleCanonical": "https://rhino-performance.com/", "userCanonical": "https://rhino-performance.com/", "referringUrls": ["https://www.rhino-performance.com/", "https://rhino-performance.com/los-benecios-de-la-natacion-para-la-salud-y-el-rendimiento-fisico/", "https://rhino-performance.com/politicas-de-reembolso-o-cabios/", "http://rhino-performance.com/"], "sitemap": ["https://rhino-performance.com/sitemap.xml", "https://rhino-performance.com/sitemap_index.xml", "https://rhino-performance.com/wp-sitemap.xml"], "crawledAs": "MOBILE"}}
{"url": "https://rhino-performance.com/presoterapia/", "at": "2026-11-12T16:13:34.894824+00:00", "index_status": {"verdict": "PASS", "coverageState": "Enviada e indexada", "robotsTxtState": "ALLOWED", "indexingState": "INDEXING_ALLOWED", "lastCrawlTime": "2026-11-09T08:32:41Z", "pageFetchState": "SUCCESSFUL", "googleCanonical": "https://rhino-performance.com/presoterapia/", "userCanonical": "https://rhino-performance.com/presoterapia/", "referringUrls": ["https://rhino-performance.com/frecuencia-cardiaca-maxima-que-es-como-calcularla-y-por-que-importa-en-tu-entrenamiento/", "https://rhino-performance.com/categoria-producto/botas-de-presoterapia-botas/", "https://www.rhino-performance.com/productos/botas-presoterapia-inalambricas-pro-air/"], "sitemap": ["https://rhino-performance.com/sitemap.xml", "https://rhino-performance.com/sitemap_index.xml", "https://rhino-performance.com/wp-sitemap.xml"], "crawledAs": "MOBILE"}}
{"url": "https://rhino-performance.com/accesorios/", "at": "2026-11-12T16:13:43.562814+00:00", "index_status": {"verdict": "PASS", "coverageState": "Enviada e indexada", "robotsTxtState": "ALLOWED", "indexingState": "INDEXING_ALLOWED", "lastCrawlTime": "2026-11-10T20:31:30Z", "pageFetchState": "SUCCESSFUL", "googleCanonical": "https://rhino-performance.com/accesorios/", "userCanonical": "https://rhino-performance.com/accesorios/", "referringUrls": ["https://www.rhino-performance.com/blog/?page=1", "https://rhino-performance.com/frecuencia-cardiaca-maxima-que-es-como-calcularla-y-por-que-importa-en-tu-entrenamiento/", "https://rhino-performance.com/presoterapia/", "https://rhino-performance.com/page-sitemap.xml"], "sitemap": ["https://rhino-performance.com/sitemap.xml", "https://rhino-performance.com/sitemap_index.xml", "https://rhino-performance.com/wp-sitemap.xml"], "crawledAs": "MOBILE"}}
{"url": "https://rhino-performance.com/productos/", "at": "2026-11-12T16:13:52.029010+00:00", "index_status": {"verdict": "PASS", "coverageState": "Enviada e indexada", "robotsTxtState": "ALLOWED", "indexingState": "INDEXING_ALLOWED", "lastCrawlTime": "2026-11-12T01:48:26Z", "pageFetchState": "SUCCESSFUL", "googleCanonical": "https://rhino-performance.com/productos/", "userCanonical": "https://rhino-performance.com/productos/", "referringUrls": ["https://rhino-performance.com/shop/", "https://rhino-performance.com/guia-para-el-uso-de-tus-botas-de-presoterapia/", "https://rhino-performance.com/productos"], "sitemap": ["https://rhino-performance.com/sitemap.xml"], "crawledAs": "MOBILE"}}
{"url": "https://rhino-performance.com/productos/botas-presoterapia-inalambricas-pro-air/", "at": "2026-11-12T16:14:00.477330+00:00", "index_status": {"verdict": "PASS", "coverageState": "Enviada e indexada", "robotsTxtState": "ALLOWED", "indexingState": "INDEXING_ALLOWED", "lastCrawlTime": "2026-11-06T15:36:53Z", "pageFetchState": "SUCCESSFUL", "googleCanonical": "https://rhino-performance.com/productos/botas-presoterapia-inalambricas-pro-air/", "userCanonical": "https://rhino-performance.com/productos/botas-presoterapia-inalambricas-pro-air/", "referringUrls": ["https://rhino-performance.com/producto/botas-presoterapia-pro-air/", "https://rhino-performance.com/guia-para-el-uso-de-tus-botas-de-presoterapia/", "https://www.rhino-performance.com/productos/botas-presoterapia-inalambricas-pro-air/"], "sitemap": ["https://rhino-performance.com/sitemap.xml"], "crawledAs": "MOBILE"}}
{"url": "https://rhino-performance.com/productos/baterias-doble-capacidad-pro-air/", "at": "2026-11-12T16:14:08.804757+00:00", "index_status": {"verdict": "PASS", "coverageState": "Enviada e indexada", "robotsTxtState": "ALLOWED", "indexingState": "INDEXING_ALLOWED", "lastCrawlTime": "2026-10-31T08:30:01Z", "pageFetchState": "SUCCESSFUL", "googleCanonical": "https://rhino-performance.com/productos/baterias-doble-capacidad-pro-air/", "userCanonical": "https://rhino-performance.com/productos/baterias-doble-capacidad-pro-air/", "referringUrls": ["https://rhino-performance.com/producto/baterias-pro-air-doble-capacidad/", "https://rhino-performance.com/guia-para-el-uso-de-tus-botas-de-presoterapia/", "https://www.rhino-performance.com/productos/baterias-doble-capacidad-pro-air/"], "crawledAs": "MOBILE"}}
{"url": "https://rhino-performance.com/blog/", "at": "2026-11-12T16:14:17.731208+00:00", "index_status": {"verdict": "PASS", "coverageState": "Enviada e indexada", "robotsTxtState": "ALLOWED", "indexingState": "INDEXING_ALLOWED", "lastCrawlTime": "2026-11-12T02:53:10Z", "pageFetchState": "SUCCESSFUL", "googleCanonical": "https://rhino-performance.com/blog/", "userCanonical": "https://rhino-performance.com/blog/", "referringUrls": ["https://www.rhino-performance.com/blog/?page=5", "https://rhino-performance.com/tag/recuperacion-muscular/", "http://rhino-performance.com/", "https://rhino-performance.com/mangas-de-compresion-frio-y-calor-para-el-cuidado-muscular/"], "crawledAs": "MOBILE"}}
{"url": "https://rhino-performance.com/blog/?page=2", "at": "2026-11-12T16:14:27.579732+00:00", "index_status": {"verdict": "NEUTRAL", "coverageState": "Google no reconoce esta URL", "robotsTxtState": "ROBOTS_TXT_STATE_UNSPECIFIED", "indexingState": "INDEXING_STATE_UNSPECIFIED", "pageFetchState": "PAGE_FETCH_STATE_UNSPECIFIED"}}
{"url": "https://rhino-performance.com/contacto/", "at": "2026-11-12T16:14:35.810074+00:00", "index_status": {"verdict": "NEUTRAL", "coverageState": "Descubierta: actualmente sin indexar", "robotsTxtState": "ROBOTS_TXT_STATE_UNSPECIFIED", "indexingState": "INDEXING_STATE_UNSPECIFIED", "pageFetchState": "PAGE_FETCH_STATE_UNSPECIFIED", "sitemap": ["https://rhino-performance.com/sitemap.xml"], "crawledAs": "CRAWLING_USER_AGENT_UNSPECIFIED"}}
{"url": "https://rhino-performance.com/sobre-rhino-performance/", "at": "2026-11-12T16:14:46.336992+00:00", "index_status": {"verdict": "NEUTRAL", "coverageState": "Google no reconoce esta URL", "robotsTxtState": "ROBOTS_TXT_STATE_UNSPECIFIED", "indexingState": "INDEXING_STATE_UNSPECIFIED", "pageFetchState": "PAGE_FETCH_STATE_UNSPECIFIED"}}
{"url": "https://rhino-performance.com/politica-de-devolucion/", "at": "2026-11-12T16:14:54.571616+00:00", "index_status": {"verdict": "PASS", "coverageState": "Enviada e indexada", "robotsTxtState": "ALLOWED", "indexingState": "INDEXING_ALLOWED", "lastCrawlTime": "2026-10-31T00:32:14Z", "pageFetchState": "SUCCESSFUL", "googleCanonical": "https://rhino-performance.com/politica-de-devolucion/", "userCanonical": "https://rhino-performance.com/politica-de-devolucion/", "referringUrls": ["https://rhino-performance.com/", "https://rhino-performance.com/blog/posts/pedaleaste-100-km-y-luego-qu-dd31584de196"], "sitemap": ["https://rhino-performance.com/sitemap.xml"], "crawledAs": "MOBILE"}}
{"url": "https://rhino-performance.com/blog/posts/ejercicio-en-la-manana-antes-o-despues-de-desayunar-6b4da8f2797c/", "at": "2026-11-12T16:15:03.420051+00:00", "index_status": {"verdict": "PASS", "coverageState": "Enviada e indexada", "robotsTxtState": "ALLOWED", "indexingState": "INDEXING_ALLOWED", "lastCrawlTime": "2026-11-12T05:59:50Z", "pageFetchState": "SUCCESSFUL", "googleCanonical": "https://rhino-performance.com/blog/posts/ejercicio-en-la-manana-antes-o-despues-de-desayunar-6b4da8f2797c/", "userCanonical": "https://rhino-performance.com/blog/posts/ejercicio-en-la-manana-antes-o-despues-de-desayunar-6b4da8f2797c/", "referringUrls": ["https://rhino-performance.com/ejercicio-en-la-manana-antes-o-despues-de-desayunar/", "https://www.rhino-performance.com/blog/posts/ejercicio-en-la-manana-antes-o-despues-de-desayunar-6b4da8f2797c"], "crawledAs": "MOBILE"}}
{"url": "https://rhino-performance.com/blog/posts/pedaleaste-100-km-y-luego-qu-dd31584de196/", "at": "2026-11-12T16:15:12.941331+00:00", "index_status": {"verdict": "PASS", "coverageState": "Enviada e indexada", "robotsTxtState": "ALLOWED", "indexingState": "INDEXING_ALLOWED", "lastCrawlTime": "2026-10-31T00:42:43Z", "pageFetchState": "SUCCESSFUL", "googleCanonical": "https://rhino-performance.com/blog/posts/pedaleaste-100-km-y-luego-qu-dd31584de196/", "userCanonical": "https://rhino-performance.com/blog/posts/pedaleaste-100-km-y-luego-qu-dd31584de196/", "referringUrls": ["https://rhino-performance.com/blog/posts/pedaleaste-100-km-y-luego-qu-dd31584de196"], "crawledAs": "MOBILE"}}
SearchAnalytics devuelve170filas deURL (no totalíndice),dimensiónpage,periodo2026-10-12a2026-11-08enPT,web,final,rowLimit1000,startRow0,filtroorigen ^https://rhino-performance\.com/. No contar impresiones como confirmación actual de todas lasURLs indexadas. Primera consulta sin filtro se rechazó durante validaciónlocal; ninguna causa de índice inferida de ese error.
