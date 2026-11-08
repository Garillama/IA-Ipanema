# SEO de producto

Fecha: 2026-11-08. La PDP nativa reúne H1, descripción, medios, variantes, enlaces relacionados y Product/Offer. Usar esa fuente comercial como autoridad para precio, moneda y disponibilidad; el schema no debe construirse desde texto formateado ni valores de ejemplo.

Product/Offer puede ser elegible para experiencias de búsqueda cuando cumple los requisitos aplicables; un JSON válido no garantiza presentación enriquecida. La [guía de producto de Google](https://developers.google.com/search/docs/appearance/structured-data/product) distingue experiencias y requisitos. Las pruebas locales deben comprobar coherencia con la oferta visible y la URL canónica.

Imágenes de producto necesitan alt útil y dimensiones. El primer medio recibe prioridad en source; la selección de una variante mediante URL puede mostrar otro medio. Comprobar que la variante inicial, precio, disponibilidad y URL coincidan sin esperar una corrección tardía de JS. No canonicalizar o indexar todas las variantes por regla universal sin conocer modelo de plataforma y catálogo.

La descripción debe aportar información real, con encabezados semánticos y contenido accesible. Los relacionados contribuyen a navegación; no duplicar toda la PDP en cada tarjeta. Reseñas y AggregateRating requieren datos verificables de esas entidades: un bloque de testimonios no los acredita.

Un producto agotado temporal y uno eliminado necesitan decisiones diferentes. No alterar estado ni crear productos para esta investigación. Ver [matriz de estados](../10-quality/testing-matrix.md) y [datos estructurados](structured-data.md).

## Reglas comerciales verificables

La [auditoría vigente](../../reports/seo/audited-pages.md) observó un H1 adicional dentro de `.user-content`: el origen es descripción editable; no justificar otro override del componente global ni editar el contenido remoto. Revisar/autorizar corrección editorial concreta, conservar el H1 del producto y probar consumidores/estados.

El motor distingue [product snippets](https://developers.google.com/search/docs/appearance/structured-data/product-snippet) de [merchant listings](https://developers.google.com/search/docs/appearance/structured-data/merchant-listing). Para estos últimos comprueba nombre/imagen/oferta, precio activo positivo y moneda; `priceSpecification` es una alternativa real, no un error por faltar `Offer.price`. Si existen ambos, el precio directo tiene precedencia según documentación. No usar precio tachado ni precio exclusivo de miembros como precio general activo. Ausencia de SKU/GTIN es recomendación cuando proceda, no permiso para generarlos.

[ProductGroup](https://developers.google.com/search/docs/appearance/structured-data/product-variants) requiere investigar ID del grupo, dimensiones y cada variante identificable/preseleccionable con URL real. Una única canonical del grupo no obliga a que cada URL de selección sea idéntica. El motor compara precio/disponibilidad por variante con sus propios datos; no considera contradicción que dos tallas tengan precios o stock diferentes. Los modelos multipágina pueden referenciar variantes fuera de página mediante URLs; comprobar la página actual y datos comunes sin declarar catálogo completo.

Reviews/AggregateRating deben corresponder a ese producto y ser visibles/procedentes de sistema real. El generador exige fuente declarada, verificación y URL coincidente; el validador informa falta de prueba sin llamar falsas a reseñas que no puede comprobar. Envíos y devoluciones se omiten sin políticas respaldadas. El costo calculado por domicilio no equivale a cero. Las políticas globales de organización y excepciones de oferta tienen contratos distintos; una política con ventana finita necesita días reales. No sustituir el shipping calculator ni copiar su lógica en schema.

Pruebas futuras del tema: precio normal/suscripción/promoción, variante agotada, imagen, canonical/URL seleccionada, JSON inicial/DOM, estados de compra y políticas efectivamente ofrecidas. El generador entrega un artefacto local, no una corrección desplegada ni validación externa Google. Sin exportación comercial independiente el precio de la captura solo es una observación, no una auditoría completa contra inventario.
