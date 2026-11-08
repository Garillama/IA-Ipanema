# SEO de producto

Fecha: 2026-11-08. La PDP nativa reúne H1, descripción, medios, variantes, enlaces relacionados y Product/Offer. Usar esa fuente comercial como autoridad para precio, moneda y disponibilidad; el schema no debe construirse desde texto formateado ni valores de ejemplo.

Product/Offer puede ser elegible para experiencias de búsqueda cuando cumple los requisitos aplicables; un JSON válido no garantiza presentación enriquecida. La [guía de producto de Google](https://developers.google.com/search/docs/appearance/structured-data/product) distingue experiencias y requisitos. Las pruebas locales deben comprobar coherencia con la oferta visible y la URL canónica.

Imágenes de producto necesitan alt útil y dimensiones. El primer medio recibe prioridad en source; la selección de una variante mediante URL puede mostrar otro medio. Comprobar que la variante inicial, precio, disponibilidad y URL coincidan sin esperar una corrección tardía de JS. No canonicalizar o indexar todas las variantes por regla universal sin conocer modelo de plataforma y catálogo.

La descripción debe aportar información real, con encabezados semánticos y contenido accesible. Los relacionados contribuyen a navegación; no duplicar toda la PDP en cada tarjeta. Reseñas y AggregateRating requieren datos verificables de esas entidades: un bloque de testimonios no los acredita.

Un producto agotado temporal y uno eliminado necesitan decisiones diferentes. No alterar estado ni crear productos para esta investigación. Ver [matriz de estados](../10-quality/testing-matrix.md) y [datos estructurados](structured-data.md).
