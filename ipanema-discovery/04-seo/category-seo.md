# SEO de categorías y subcategorías

Fecha: 2026-11-08. El template local ofrece imagen de categoría, page-header y grid con filtros/paginación. La navegación de header incluye enlaces a categorías/subcategorías. Los títulos y URLs proceden de plataforma; no construir rutas a partir del nombre visible.

Una categoría útil necesita nombre/H1 descriptivo, productos enlazados, breadcrumb coherente y acceso a subcategorías/páginas siguientes. La descripción editorial puede explicar selección, usos y diferencias reales sin repetir el mismo texto en cada faceta. No cargar toda la descripción por JS después de un clic como única fuente de contenido.

Los campos SEO de categoría alimentan metadatos de plataforma; que no aparezca `category.seo_title` como acceso directo en un tpl no demuestra que no se use. El banner debe reservar ratio y no desplazar el grid. No asignarle prioridad alta a toda categoría solo por su tamaño si el candidato LCP observado es otro.

La navegación facetada exige separar categorías con identidad de filtros transitorios. Antes de proponer noindex/canonical, inspeccionar parámetros, enlaces generados y conteo de combinaciones; los endpoints de plataforma no están bajo control libre del tema. El grid actual de categoría usa infinite: [riesgo concreto](crawlability.md).

BreadcrumbList ya forma parte del JSON-LD del tema. ItemList puede expresar una lista semántica si hay un caso real, pero no ofrece por sí solo un resultado enriquecido genérico de carrusel de productos en Google. No generar Product con precios/reseñas inventados para «completar» la categoría.

Validar categoría llena/vacía, subcategoría, filtrada, página posterior, producto agotado y variantes como productos. Registrar producto único descubierto por enlaces y profundidad desde home. [Playbook de categoría](../12-playbooks/optimize-category.md).
