# Carruseles rastreables y progresivos

Fecha: 2026-11-08. **Google puede descubrir productos y categorías del carrusel si existen URLs reales en enlaces `<a href>` accesibles al rastreador.** La base preferida es incluir esos enlaces y su contenido en el HTML servidor. Las tarjetas locales y muchos banners ya los generan; no sustituirlos por onclick sin href. [Fuente de Google](https://developers.google.com/search/docs/crawling-indexing/links-crawlable).

Descubrir una URL, renderizar su tarjeta, indexar la página destino y atribuir relevancia al contenido son cosas distintas. Un slide oculto mediante transform, display o visibility no queda automáticamente excluido del procesamiento SEO; la presentación visual y la accesibilidad también difieren. El riesgo más claro aparece cuando los nodos/enlaces todavía no existen hasta una interacción, se desmontan por virtualización o el único dato es una URL dentro de un objeto JS.

Lazy loading de imágenes no debe eliminar el anchor/título de producto. Cargar imágenes al entrar en viewport es distinto de requerir que Google arrastre un carrusel. La [documentación sobre contenido lazy](https://developers.google.com/search/docs/crawling-indexing/javascript/lazy-loading) permite razonar sobre lo que aparece en renderizado; no garantiza ejecución de todos los gestos.

El slideshow local itera slides en Twig; products itera tarjetas en Twig. La galería de card puede montar imágenes posteriores desde data-images, pero eso no elimina necesariamente el enlace al producto, que ya está en el contenedor. Loop puede clonar nodos: contar enlaces únicos, IDs duplicados y foco de clones, sin presentar los clones como contenido nuevo.

## Diseño de referencia, solo documentación

Para categorías, una lista con desplazamiento nativo conserva destinos sin JS. Ejemplo con rutas observadas, no un archivo instalado en el tema:

```html
<section aria-labelledby="recovery-categories">
  <h2 id="recovery-categories">Categorías de recuperación</h2>
  <ul class="category-links">
    <li><a href="/presoterapia/">Presoterapia</a></li>
    <li><a href="/pistolas-de-masaje/">Pistolas de masaje</a></li>
  </ul>
</section>
```

La propuesta CSS usaría flex/grid, overflow horizontal y scroll snap proximity con anchura/reserva de medios estable. Flechas opcionales se habilitarían tras detectar el enhancement; los enlaces y el scroll básico seguirían funcionando. Si se necesita loop/autoplay, evaluar el Swiper ya cargado antes de otro motor. No repetir imágenes/texto para conseguir cada breakpoint.

Cada tarjeta debe tener nombre de destino comprensible y alt según función de la imagen. Los botones de avanzar cambian estado; los anchors navegan. Pausa, navegación por teclado, foco y anuncios deben comprobarse, especialmente con autoplay y clones. [WAI carruseles](https://www.w3.org/WAI/tutorials/carousels/). El criterio SEO no certifica accesibilidad ni obliga a usar un carrusel si un grid facilita descubrir el catálogo.

Verificar con JS desactivado, HTML inicial, DOM renderizado, URLs únicas y categorías/páginas siguientes. Si se virtualiza una lista grande, conservar otra vía real al catálogo completo y medir el coste: DOM pequeño no justifica dejar productos huérfanos.

## Validación del motor y modalidades Google

La ampliación separa enlaces de destinos y acciones nativas: selectors de variantes, thumbnails, reproducción y cierre de modal no son URLs rotas por tener href vacío o fragmento. Sí requieren accesibilidad/interacción apropiada. La regla anterior del QA marcó doce fallos candidatos por ese motivo en la muestra viva; se corrigió con contratos encontrados en archivos reales y prueba de regresión. No presentar esos doce como pérdida demostrada de rastreo. [Evidencia](../../reports/seo/audited-pages.md).

ItemList semántico de URLs reales, carrusel visual y carrusel de Google son funciones diferentes. El [carrusel tradicional](https://developers.google.com/search/docs/appearance/structured-data/carousel) admite tipos concretos. La [beta regional](https://developers.google.com/search/docs/appearance/structured-data/carousels-beta), consultada el 2026-11-08, incluye Product/LocalBusiness/Event con requisitos adicionales, al menos tres elementos y páginas de detalle únicas del mismo sitio. Su disponibilidad regional/programa se verifica aparte; no se documenta como habilitada para productos de México. El motor solo comprueba sus requisitos específicos si `facts.google_experience` la solicita; no fuerza a una lista semántica a imitarla.

No emitir otro Product por cada clon del slider ni asumir que retirar marcado válido mejora SEO. Antes de cambiar, inventariar fuente y propósito, comprobar la PDP de destino y evitar contradicciones. `seo audit` compara HTML/DOM/sin JS; el QA de red demuestra solicitudes y bytes bajo un perfil, no decodificación o visibilidad. Lazy loading de imágenes conserva enlaces sin obligar a descargar todas las imágenes inmediatamente.
