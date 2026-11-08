# Product card compartida

Fecha: 2026-11-08. Confirmado por lectura de `snippets/product-list/product-item/item.tpl` y sus consumidores en el [grafo](../01-architecture/dependency-map.md), contrastado con home, categorías, búsqueda y PDP desbloqueadas. El recorrido no cubre todas las variantes comerciales.

La entrada común es [item.tpl](/home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/product-list/product-item/item.tpl:1). La consumen `blocks/products.tpl`, `sections/main-products-grid.tpl` y `snippets/product-list/_product-grid.tpl`. Los módulos de home y relacionados que usan el bloque products heredan esa tarjeta; no son implementaciones independientes por contexto.

| Contexto | Variación encontrada | Qué reutilizar |
|---|---|---|
| Categoría y búsqueda | Activa slider de imágenes solo con product_item_slider, otras imágenes, sin filtros, sin reduced_item y sin slide_item | Mantener condiciones y product.url/variante; no crear otra card |
| Grid de home | Bloque products determina columnas/formato e image_priority_high | Mismo include con sus parámetros |
| Carrusel de productos | slide_item agrega clases de Swiper e impide slider interno de card | Conservar esa exclusión: evita carruseles anidados innecesarios |
| Relacionados | Composición de bloques de related-products | Revisar fuente de productos y configuración del bloque |
| Cross-selling/reducida | reduced_item desactiva cuotas, swatches, quick shop y etiquetas según ramas | No reactivar todo sin considerar tamaño y contexto |
| Recomendaciones dinámicas | Lógica LS y bloques específicos encontrados | No se demostró que todo HTML obtenido por LS use exactamente este archivo; inspeccionar respuesta antes de afirmarlo |

La tarjeta centraliza enlaces a imagen y nombre, precio/compare_at, cuotas, descuentos, badges, swatches, suscripciones y quick shop. Usa `product.carries_variants_payload` y `data-vap-carrier-ref` para evitar replicar payloads completos cuando corresponde; duplicar HTML de la card puede anular esa optimización. Los IDs incorporan `dom_id_suffix` cuando existe: preservar para evitar colisiones.

`item-image.tpl` obtiene dimensiones y alt del producto, reserva ratio por padding y acepta recorte global. Se contemplan imagen secundaria o slider. Se generan datos para imágenes adicionales en `data-images`; no significa que todas se descarguen al recibir el HTML. El límite y montaje están en [galerías](carousels-and-galleries.md).

**Riesgo de tamaños:** `common_image_params.image_sizes` declara `(min-width: 768px) 50vw` aunque el grid guardado de categoría usa cuatro columnas. La selección de recurso puede exceder la anchura renderizada. Confirmación del atributo en source; ahorro real pendiente de `currentSrc`, DPR, contenedor y Network. La solución debe parametrizar la anchura por contexto en el helper existente. No reducir resolución de todas las imágenes a ciegas.

Cada tarjeta real puede incluir JSON-LD Product desde el snippet compartido. No agregar otro schema por cada carrusel sin inspección previa; evitar generar información de placeholders como productos reales. Los testimonios editoriales no son AggregateRating de esos productos.

La personalización limpia cambia tokens o markup de esta fuente según alcance. Una variante específica puede recibirse como parámetro/clase acotada, preservando hooks de negocio. Validar nombres largos, sin compare_at, precio oculto, agotado, filtros, kit, suscripción, una/muchas imágenes y tarjetas repetidas en la misma página. [Playbook](../12-playbooks/optimize-product-card.md).
