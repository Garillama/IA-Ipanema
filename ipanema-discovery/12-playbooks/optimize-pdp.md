# Optimizar PDP

1. Seguir main-product → product-media/product-info → imagen/formulario compartidos. Separar variante visual de lógica comercial.
2. Comprobar medio/variante inicial por URL, imagen LCP y espacio reservado. Medir galería grid/slider, thumbnails, vídeos y fallback.
3. Revisar precio/stock/cuotas/promociones y accesibilidad de controles sin reescribir changeVariant ni addToCart. No calcular otra fuente de precio desde DOM formateado.
4. Auditar la descripción del comerciante: H1 adicionales, estilos inline, imágenes y contenido largo pueden originarse allí. No corregirlos con CSS que esconda títulos semánticos.
5. Mantener shipping/kit/suscripción en sus contratos nativos. Un CTA sticky solo se considera si falta y aporta valor; no confundirlo con galería sticky.
6. Ejecutar cambios de variante de lectura y revisar URL/precio/imagen; las pruebas de compra/envío/cupón con estado requieren un escenario autorizado. No reportarlas aprobadas por ver el botón.
7. Comparar seis anchos, tabulación, contenido amplio, errores y métricas de la PDP exacta. Revisar también el producto destacado que comparte snippets.

[PDP investigada](../07-commerce/product-detail.md) y [SEO producto](../04-seo/product-seo.md).
