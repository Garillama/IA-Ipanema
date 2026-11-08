# PDP y producto destacado

Fecha: 2026-11-08. Evidencia: main-product.tpl, blocks/product-media.tpl, blocks/product-info.tpl, snippets/product/* y store.js. No se enviaron compras ni formularios.

`main-product` es una sección única con `id="single-product"`, payload `data-variants`, slots y dos bloques estáticos. Product-media incluye `snippets/product/product-image.tpl`; product-info incluye el formulario común y bloques adicionales. La sección featured-product también reutiliza imagen y formulario con `home_main_product: true`; esto cambia título a H2 y limita galería/vídeo/lightbox. No copiar la PDP entera para hacer un destacado.

La galería admite slider y grid desktop; comparte nodos y oculta los controles que no aplican. `product.media` incluye imágenes y vídeos nativos, más vídeo externo si hay product.video_url. La primera imagen de PDP recibe prioridad. El deep link de variante inicializa `data-initial-slide`; en grid desktop el JS puede desplazar a la imagen seleccionada, evitando hacerlo en recarga/back-forward según Navigation Timing.

El formulario contiene nombre, precio dinámico, precio previo, ahorro, impuestos, cuotas y promos según datos/settings, campos de variantes, cantidad, suscripciones/kits y envíos. Sus acciones son POST a `store.cart_url` con producto real; el JS utiliza LS para variaciones, compra y shipping. Preservar `id`, `name`, data attributes y contexto del producto.

| Interacción | Fuente / contrato | Riesgo al rediseñar |
|---|---|---|
| Variante y disponibilidad | initProductVariants/changeVariant, LS.changeVariant | Actualizar solo texto del precio deja stock, cuotas, promociones e imagen desincronizados |
| Cantidad | product-quantity e initQuantitySelectors | Mantener input, restricciones y lectores de pantalla |
| Agregar al carrito | initAddToCart, LS.addToCartEnhanced; rama subscriptionSubmit | Un segundo handler puede duplicar acciones y analytics |
| Cambiar imagen | initProductGallery y hooks de variante | Mantener relación media/posición/variante y foco |
| Envíos | shipping-calculator/branches, calculateShippingAjax | No crear un cotizador paralelo basado solo en precio visible |
| Información extendida | description y product-description | Evitar repetir la descripción completa en dos sitios sin necesidad |
| Relacionados/complementarios | related-products y product-recommendations | Fuente de datos distinta; no asumir equivalencia ni copiar catálogo |

No se encontró un módulo autónomo llamado sticky add to cart. `initStickyProductGallery` sí existe. Cambiar esa función no agrega un CTA sticky nativo. La actualización exacta de URL tras cambiar variante depende de LS; el source local no basta para certificar historial y canonical. Probar deep links, volver/adelante y combinaciones inexistentes.

Estados por ejecutar: disponible, agotado, sin precio, combinación inválida, precio promocional, kit, suscripción, error de envío, validación y error de carrito. Checkout e integraciones no fueron probados. La existencia de ramas no prueba la habilitación de features de la tienda. [Playbook PDP](../12-playbooks/optimize-pdp.md).
