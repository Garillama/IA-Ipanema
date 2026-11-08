# SEO de categorías y subcategorías

Fecha: 2026-11-08. El template local ofrece imagen de categoría, page-header y grid con filtros/paginación. La navegación de header incluye enlaces a categorías/subcategorías. Los títulos y URLs proceden de plataforma; no construir rutas a partir del nombre visible.

Una categoría útil necesita nombre/H1 descriptivo, productos enlazados, breadcrumb coherente y acceso a subcategorías/páginas siguientes. La descripción editorial puede explicar selección, usos y diferencias reales sin repetir el mismo texto en cada faceta. No cargar toda la descripción por JS después de un clic como única fuente de contenido.

Los campos SEO de categoría alimentan metadatos de plataforma; que no aparezca `category.seo_title` como acceso directo en un tpl no demuestra que no se use. El banner debe reservar ratio y no desplazar el grid. No asignarle prioridad alta a toda categoría solo por su tamaño si el candidato LCP observado es otro.

La navegación facetada exige separar categorías con identidad de filtros transitorios. Antes de proponer noindex/canonical, inspeccionar parámetros, enlaces generados y conteo de combinaciones; los endpoints de plataforma no están bajo control libre del tema. El grid actual de categoría usa infinite: [riesgo concreto](crawlability.md).

BreadcrumbList ya forma parte del JSON-LD del tema. ItemList puede expresar una lista semántica si hay un caso real, pero no ofrece por sí solo un resultado enriquecido genérico de carrusel de productos en Google. No generar Product con precios/reseñas inventados para «completar» la categoría.

Validar categoría llena/vacía, subcategoría, filtrada, página posterior, producto agotado y variantes como productos. Registrar producto único descubierto por enlaces y profundidad desde home. [Playbook de categoría](../12-playbooks/optimize-category.md).

## Comprobación actual y aplicación

La ampliación verificó `/productos/` en seis anchos, sin JS y reduced motion; [evidencia y límites](../../reports/seo/audited-pages.md). `snippets/product-list/pagination.tpl:12` contiene `js-load-more` y su anchor sin href cuando infinite_scroll está activo. El modo alternativo toma `page_next.url`/`page_prev.url` o `pages.next`/`pages.previous`; esas son fuentes reales encontradas, no un parámetro `?page=` inventado. Proponer reutilizar esos destinos en un fallback exige comprobar cursor/variantes y página posterior con catálogo real. El crawler local no garantiza descubrir todo el catálogo solo porque vea la primera cuadrícula.

`seo audit --type category` distingue el control de carga de acordeones «Ver más» y cierre del carrito. `seo corpus` computa profundidad y enlaces entrantes del conjunto observado, títulos repetidos y diferencia con URLs de sitemap proporcionadas. Las páginas no alcanzadas son candidatas, no huérfanas demostradas de toda la tienda. No se ha medido demanda/canibalización sin consultas y contenido suficientes.

Si se justifica ItemList, representar el orden real y URLs efectivamente presentes; no inventar productos todavía no cargados. Permitir posiciones globales de paginación en listas semánticas, sin confundirlas con requisitos específicos de un carrusel de Google. En facetas/ordenamiento comparar canonical, contenido y destinos antes de actuar; la API de Tiendanube y la plataforma controlan endpoints que el tema no puede sobrescribir libremente. [Guía de paginación de Google](https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading).

Contenido editorial: comparar título SEO/H1/intención y selección disponible; explicar diferencias reales, criterios de compra y enlaces de subcategorías útiles. No añadir bloques repetidos por longitud ni ocultarlos detrás de interacción como única vía. Una introducción superior breve y contenido inferior útil pueden compartir una única fuente semántica responsive, sin duplicar texto por dispositivo.
