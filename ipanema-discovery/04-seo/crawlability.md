# Rastreo y descubrimiento de URLs

Fecha: 2026-11-08. Antes del acceso autorizado, robots.txt y sitemap.xml devolvieron HTML de password después de una redirección. Eso prueba el comportamiento sin sesión en ese momento, no que el sitemap «no exista». Las comprobaciones con sesión se conservan aparte. [Sondas HTTP](../13-evidence/measurements/http/route-probes.json).

El tema no contiene implementaciones locales de esos endpoints, redirecciones HTTP ni X-Robots-Tag. El HTML servidor puede ofrecer productos/categorías mediante enlaces reales; es preferible que los destinos importantes no requieran clic, drag, scroll o búsqueda para descubrir su URL. [Guía de enlaces de Google](https://developers.google.com/search/docs/crawling-indexing/links-crawlable).

Hallazgo local concreto: category.json usa pagination infinite, y pagination.tpl L13 crea un anchor sin href para cargar más. Aunque LS pueda obtener las tarjetas siguientes, ese control no expone su URL. La rama classic sí usa prev_link/next_link. Alternativas propuestas: mantener paginación nativa clásica si cubre UX, o mejorar progresivamente el control para conservar la URL real suministrada por plataforma junto con la carga incremental. Coste: revisar cursor de variantes, filtros, historial y reintentos; no construir una URL adivinada.

Google puede procesar enlaces insertados con JS y renderizar contenido, pero no se debe depender de que ejecute todas las interacciones del comprador. El HTML inicial y el renderizado son etapas distintas. [Lazy loading de Google](https://developers.google.com/search/docs/crawling-indexing/javascript/lazy-loading).

Para validar un catálogo: extraer href del HTML inicial, recorrer páginas posteriores, comparar productos únicos con sitemap y verificar status/canonical de destinos. Medir profundidad desde home/categoría y detectar productos huérfanos; no confundir número de clones de un carrusel con número de destinos únicos. Los enlaces externos y rutas que cambian sesión se registran sin recorrer acciones de logout.

La política de URL de filtros y la paginación están relacionadas pero no son equivalentes. [Recomendaciones de paginación](https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading): cada página útil necesita un destino accesible; canonicalizar todas a la primera puede ocultar contenido distinto. No se modificó esa política durante discovery.
