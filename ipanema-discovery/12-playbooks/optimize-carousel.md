# Optimizar carrusel o galería

1. Identificar el motor/versión del contexto real. Aquí hay Swiper local; Embla se observó solo en otra instalación. No cargar otro slider para cambiar flechas o separación.
2. Confirmar número de elementos, vistas por breakpoint, grid/slider por dispositivo, loop y autoplay necesarios. Con un elemento, preferir presentación estática y controles coherentes.
3. Mantener enlaces/textos en HTML inicial; diferir imágenes secundarias, no destinos del catálogo. Evaluar scroll nativo si cubre la interacción.
4. Reservar ancho/alto antes de init. Las flechas externas causaron overflow real en 768/1024: corregir geometría del componente, sin esconder el problema con overflow global.
5. Comprobar lazy y recursos ocultos por red. Un source en DOM y una descarga completada son evidencias distintas. Revisar clones, IDs, foco y payload de tarjetas.
6. Verificar teclado, nombres de controles, pausa, reduce, sin JS y resize a través de 768. No suponer compatibilidad de una opción de Swiper por aparecer en el objeto de parámetros.
7. Medir LCP/CLS/ejecución y delta del cambio. La optimización no debe alterar lógica de compra ni registrar listeners cada vez que cambia el editor.

[Motores](../07-commerce/carousels-and-galleries.md), [SEO del carrusel](../04-seo/carousel-seo.md) y [motion](../06-motion/performant-patterns.md).
