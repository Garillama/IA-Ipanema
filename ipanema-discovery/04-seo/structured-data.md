# Datos estructurados y duplicación

Fecha: 2026-11-08. Fuentes locales: snippets/structured-data/structured-data.tpl, structured-data-organization.tpl y sus includes del layout/card/blog. El parseo del HTML real se conserva por ruta.

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
