# Optimizar la tarjeta de producto

1. Partir de item.tpl y determinar todos sus consumidores. Identificar modo grid, slide o reduced, condiciones de quick shop, colores y payload de variantes.
2. Revisar qué se configura globalmente y qué controla la sección. No asumir que products_per_row global modifica el columns guardado en todos los bloques.
3. Medir ancho de imagen por viewport/DPR y comprobar sizes/currentSrc. El 50vw desktop actual merece evaluación frente a cuatro columnas. Parametrizar el helper existente; no crear otra imagen responsive paralela.
4. Reservar ratio, mantener enlace y nombre de producto en HTML inicial y no cargar una imagen secundaria como LCP. Comprobar hover con touch y reducción de motion.
5. Mantener JS/LS y JSON-LD nativos. Si se modifica la distribución, evitar que aria-label o texto visible diverjan; revisar descuentos, cuotas y badges con distintos contenidos.
6. Validar con/sin stock, precio previo, color, múltiples imágenes, kit/suscripción si disponibles, filtros y varias cards del mismo producto. Comprobar IDs y foco después de loop/carga incremental.

Registrar ahorro medido y regresiones de consumidores. [Investigación de cards](../07-commerce/product-cards.md).
