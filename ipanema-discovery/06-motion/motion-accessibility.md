# Accesibilidad del movimiento

Fecha: 2026-11-08. Se ejecutó una navegación de home con prefers-reduced-motion; eso prueba el modo de emulación y la página actual, no todos los efectos opcionales.

Las reglas nativas de hero/slideshow eliminan animación/transición y restablecen opacity/transform con reduce. La galería, marquee, autoplay de anuncios y helpers fade deben evaluarse por separado. El parallax consulta reduce al actualizar, pero no se verificó una reacción inmediata a cambiar la preferencia con la página ya abierta.

Para movimiento automático, ofrecer una forma utilizable de detenerlo cuando corresponda, conservar foco y no anunciar cada transición decorativa. El estado estático debe comunicar el mismo contenido. Las alternativas no pueden depender solo de hover porque teclado y touch necesitan acceso equivalente. [Tutorial WAI](https://www.w3.org/WAI/tutorials/carousels/).

Probar autoplay durante foco/lectura, cambio de pestaña, reduce activo al cargar, reduce activado después y JS fallido. Los efectos no usados en esta tienda se registran como source inspeccionado, sin resultado ejecutado. No convertir una captura en prueba de confort vestibular ni conformidad WCAG completa.
