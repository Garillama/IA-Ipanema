# Motores de carrusel, galerías y grids

Fecha: 2026-11-08. Confirmado en `libraries-standalone.js` y `store.js`, con inspección de los componentes presentes en páginas desbloqueadas; los presets no configurados siguen sin prueba funcional. **El motor local es Swiper 6.3.2**, con lazysizes 5.2.2; Fancybox está en libraries.js.tpl para lightbox. El comentario CSS «Swiper 4.4.2» no identifica la versión del JS. Embla aparece en otra instalación servida por password, no en este árbol.

| Sistema | Configuración encontrada | Casos límite / prueba |
|---|---|---|
| Slideshow | loop si >1 slide; lazy, preloadImages false, watchOverflow; flechas y bullets; autoplay optativo; diferido cerca del viewport si no prioritario | Una imagen no usa loop; comprobar imágenes responsive ocultas, pausa, foco y drag |
| Lista de productos | columnas de data attrs; corte 768; loop si cantidad > columnasDesktop; navegación y dots | Una cantidad que desborda mobile pero no desktop no activa loop; medir si es comportamiento deseado |
| Testimonios | 1 mobile; a 768 min(2, columnas); a 1024 columnas completas; gap configurable | Sin loop explícito en esa configuración; no asumir autoplay |
| Categorías/carrusel genérico | columnsMode fijo/auto; cortes 768 y 1024; centerInsufficientSlides configurable | Pocos elementos, anchuras auto, nombres largos y teclado |
| Banners | grid/slider por dispositivo; columnas; cortes 768/1024; loop según columnasDesktop | Revisar cambio de viewport después de inicializar |
| Iconos/texto | Slider solo <768; 1 visible; dots y overflow | Desktop queda como composición CSS; no duplicar contenido |
| Announcement slider | 1 visible; loop/autoplay solo si >1; flechas si presentes | pauseOnMouseEnter está en opciones, pero su efecto depende de versión; comprobar pausa real y teclado |
| Announcement marquee | Clona ítems para llenar pantalla y luego clona contenido | Riesgo de enlaces/lectura repetidos y acumulación al reinicializar |
| Timer offers | Inicialización específica, columnas por data attrs y countdown | Evitar timers/instancias duplicados al editar; probar final de oferta |
| Galería PDP | Swiper de una vista y miniaturas; grid desktop por CSS; deep link de variante | Vídeos mezclados, inicialSlide, scroll y resize |
| Relacionados y recomendaciones | Inicializadores propios y/o bloque products según fuente | No asumir que todo el HTML remoto usa la card local; inspeccionar respuesta |
| Imágenes de card | LS.productItemSlider y datos adicionales | Reutilizar helper nativo, no crear un segundo slider dentro de slide_item |

`createSwiper` difiere la construcción con setTimeout y usa `_swiperInit` para evitar dos inicializaciones pendientes del mismo nodo. No garantiza que cada listener/observer de la página tenga teardown. La protección de una instancia no es una prueba de ausencia de fugas.

En slideshow se quita `swiper-lazy` de imágenes con `display:none` antes de clonar. Es una protección existente que conviene conservar, pero no impide que un `<img src>` prioritario oculto ya haya sido solicitado por el navegador. El comportamiento tras cambiar de breakpoint merece otra prueba: quitar una clase al inicio no acredita carga correcta tras resize.

El fallback sin JS es parcial: hay HTML de las tarjetas y enlaces, pero overflow/transform y data-src pueden impedir ver todas las imágenes o slides. Que Google descubra un enlace no garantiza que el visitante sin JS pueda recorrer toda la galería. [Patrón progresivo propuesto](../04-seo/carousel-seo.md).

**Decisión reutilizable:** usar el motor ya cargado cuando se necesita su interacción; usar grid o desplazamiento nativo con scroll snap cuando bastan y están autorizados. El motor independiente exige justificar ahorro por página, accesibilidad, fallback, editor y mantenimiento; no se recomienda cargar una biblioteca adicional para cambiar el aspecto de un carrusel existente.
