# Búsqueda, filtros y ordenamiento

Fecha: 2026-11-08. Fuente: header/search-form.tpl, product-list/filters/*, main-products-grid.tpl, pagination.tpl, store.js L1619.

Categoría y búsqueda comparten main-products-grid. El encabezado de resultados depende de query/products_count y solo aparece con productos reales. Los filtros requieren datos, feature has_filters_enabled y categorías/propiedades disponibles; no basta con agregar un bloque visual. Existen filtros de precio, propiedades, categorías, eliminación de filtros, sort-by y presentación en modal para mobile.

`initInfiniteScroll` delega la carga a `LS.hybridScroll` y reinicializa el slider de cards tras cargar. Los enlaces clásicos usan `page_next.url` o `pages.next`; la rama infinite muestra `<a class="btn...">` sin `href`. Esta última es una acción JS sin URL rastreable ni fallback de página siguiente en ese control. El template de categoría sí activa esa rama. [Hallazgo y alternativa](../04-seo/crawlability.md).

Se probaron una búsqueda con un resultado y otra sin resultados, que conserva recomendaciones. Las combinaciones exhaustivas, queries vacías, caracteres especiales, historial y persistencia entre sesiones no están cubiertos. Los estados adicionales de precio/orden/carga se registran en su [evidencia](../13-evidence/measurements/browser/additional-states.json); no se extrapolan a todas las facetas. No añadir una capa propia de filtros antes de aprovechar la nativa.

Para personalizar, mantener formularios, nombres de parámetros, mensajes y contratos LS. Separar el layout de filtros del comportamiento de búsqueda. Validar teclado, foco al abrir/cerrar modal, labels, cambio del conteo y anuncio del estado vacío; no afirmar conformidad con solo ver clases ARIA.
