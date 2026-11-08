# Datos estructurados y duplicación

Fecha: 2026-11-08. Fuentes locales: snippets/structured-data/structured-data.tpl, structured-data-organization.tpl y sus includes del layout/card/blog. El parseo del HTML real se conserva por ruta.

Ampliación SEO V2.1: [motor y comandos](seo-engine.md), [auditoría actual](../../reports/seo/audited-pages.md), [Google/MCP](google-integrations.md). El [diff propuesto para breadcrumbs](../../reports/seo/evidence/breadcrumb-proposal.json) se comprobó contra el código actual sin aplicarlo; no se confunde el modelo abstracto con render Twig. Las cinco páginas principales comprobadas en esta ampliación no se deben declarar rotas por ese defecto de otra rama.

| Tipo | Encontrado / aplicabilidad | Condición |
|---|---|---|
| Organization | Sí, snippet global | Nombre, logo, URL y sameAs reales |
| WebPage + BreadcrumbList | Sí, branch por template | Breadcrumbs válidos, sin coma pendiente en listas vacías |
| Product + Offer | Sí, PDP y tarjetas reales según flags | Precio/moneda/stock de producto; ramas de suscripción |
| Blog / BlogPosting | Sí, listados y tarjetas de blog | Posts reales y fechas/autores reales |
| OnlineStore / WebSite | No encontrados como tipos emitidos en estos snippets | Evaluar valor semántico antes de añadir otra entidad global |
| ItemList | No encontrado como tipo global de listados | Puede expresar una lista, sin promesa genérica de rich result |
| AggregateRating / Review | No encontrados como oferta nativa de estos snippets | Exigen reseñas genuinas y asociación correcta |
| FAQPage | No encontrado como emisión de la sección FAQ | Schema.org y resultado de Google son distintos |
| VideoObject / Article | No encontrados en estos snippets con esos nombres | Considerar solo con vídeo/artículo y metadatos suficientes; BlogPosting ya es específico |

La documentación de Google registra retirada del resultado enriquecido FAQ desde mayo de 2026; no ofrecerlo como beneficio de añadir FAQPage hoy. [Registro oficial de cambios](https://developers.google.com/search/updates). La decisión de describir FAQs semánticamente puede ser independiente de su presentación en Google.

El macro json_string del tema usa json_encode con protección de etiquetas y UTF-8. Organization tiene otro escape manual. No concatenar cadenas de clientes en scripts sin serialización segura. El branch WebPage agrega una coma tras home si template no es home y luego itera breadcrumbs: con lista vacía puede generar JSON inválido. Se reprodujo en password inicial y en la 404 del storefront 1.8.0. El resto de rutas HTML del crawl parseó sus objetos observados; eso no certifica todo el vocabulario ni todas las variantes.

Para evitar duplicación, inventariar scripts JSON-LD por entidad/URL, distinguir Organization global de Product de cada tarjeta y comprobar si apps también agregan datos. Varios objetos no son un error por sí solos; valores contradictorios del mismo producto sí crean ambigüedad. No instalar un generador SEO adicional antes de revisar lo existente.

Se ejecutó JSON.parse sobre el HTML inicial y DOM de páginas auditadas. Eso valida sintaxis, no requisitos completos de Schema.org ni elegibilidad de Google. Rich Results Test, Schema Markup Validator y Search Console deben registrarse por separado si se ejecutan; no se les asigna un aprobado aquí.

## Matriz y contratos por página

| Página | Entidades pertinentes según información real | Cuándo abstenerse |
|---|---|---|
| Home | Una identidad Organization/OnlineStore, WebSite, WebPage; ItemList solo con propósito de lista | No generar una identidad comercial adicional si ya existe; SearchAction solo si describe búsqueda real, sin searchbox enriquecido retirado |
| Categoría | CollectionPage/WebPage, BreadcrumbList, ItemList opcional de elementos realmente listados | No convertirla en PDP ni inventar Offer/Review para tarjetas; ItemList no promete carrusel |
| PDP | Product/Offer y BreadcrumbList; ProductGroup si el modelo/URLs de variantes lo sostienen | No inventar GTIN/SKU, stock, fechas de oferta o reseñas; no emitir ProductGroup solo porque exista selector |
| Índice de blog | Blog o CollectionPage/WebPage y lista pertinente | No declarar cada extracto como artículo completo nuevo ni repetir entidades contradictorias |
| Artículo | BlogPosting/Article, WebPage y autor Person/Organization real; ImageObject/VideoObject si existe recurso apropiado | No inventar autor, fecha o vídeo; BlogPosting ya es subtipo de Article |
| Políticas | Organization global y excepciones Offer cuando corresponda | No añadir envío/devolución sin fuente real; no asumir envío gratis si depende del domicilio/monto |

El inventario de cada ejecución está en `structured_data.graph`: tipos, identificadores, propiedades, aristas y referencias pendientes. La identidad global debe ser consistente entre páginas; conservar IDs existentes antes de proponer fragments nuevos. El vínculo página–producto puede ser `WebPage.mainEntity`/`Product.mainEntityOfPage`; no usar el mismo `@id` para tipos incompatibles. URL canónica, URL de selección de variante e identificador de entidad tienen funciones distintas.

Reglas reutilizables, no datos de una tienda: [contrato de procedencia y generación](../../reusable/contracts/seo-evidence.json). El alcance semántico es parcial y se registra con propiedades sin comprobar. No se expande ni se descarga `@context` remoto. El motor distingue validación sintáctica, vocabulario comprobado, requisitos Google por experiencia, consistencia aportada, validación externa y observación en Google.

La [documentación de producto](https://developers.google.com/search/docs/appearance/structured-data/product-snippet), [merchant listings](https://developers.google.com/search/docs/appearance/structured-data/merchant-listing), [variantes](https://developers.google.com/search/docs/appearance/structured-data/product-variants) y [organización](https://developers.google.com/search/docs/appearance/structured-data/organization) fue consultada el 2026-11-08. Su subconjunto ejecutable está versionado en `google_requirements.json`, con fuente por regla. Una recomendación opcional no debe presentarse como error crítico.
