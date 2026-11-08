# Categorías y colecciones

Fecha: 2026-11-08. Fuente: templates/pages/category.json, sections/category-hero.tpl, page-header.tpl y main-products-grid.tpl.

El template guardado compone category-hero → page-header → main-products-grid. Sus columnas son cuatro desktop y dos mobile; la sección guarda paginación **infinite**, que prevalece sobre la lectura aislada del setting global classic. El grid usa `{% paginate by 12 %}` en infinite y `by 60` en la otra rama. No se midió el coste de 60 tarjetas con datos reales.

La plataforma suministra products, category, breadcrumbs y filtros. El tema configura ancho, imagen de categoría, encabezado y presentación. Si no hay productos activos globalmente, genera placeholders; si existen productos pero el resultado está vacío, muestra mensajes de resultado/filtros. Esos estados son distintos y deben probarse por separado.

El source admite variantes como productos mediante `data-vap-enabled`, cursor `page_next` y payloads referenciados. El ordenamiento, conteo y paginación deben conservar esos contratos; una paginación reconstruida solo con `?page=` podría perder offsets o filtros.

Las subcategorías se descubren a través de datos y enlaces de navegación, no mediante otra plantilla de archivo obligatoria. No se encontró una landing page propia adicional ni una plantilla alternativa de categoría guardada. El patrón de página institucional y plantillas alternativas documentadas podría cubrir esos casos, sin asumir que ya estén asignadas. [SEO de categoría](../04-seo/category-seo.md).
