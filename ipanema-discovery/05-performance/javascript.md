# JavaScript, dependencias y ejecución

Fecha: 2026-11-08. Los tres archivos principales suman **394,872 bytes de source**: libraries-standalone.js 96,479; libraries.js.tpl 142,482; store.js 155,911. No son bytes de red ni tamaño final tras Twig. [Medidas por archivo](static-asset-measurements.md).

La entrada standalone contiene lazysizes 5.2.2, Swiper 6.3.2 y createSwiper; libraries.js.tpl contiene Fancybox y utilidades minificadas. LS, ModalHandler, DOMContentLoaded helper y jQueryNuvem se consumen desde el entorno de plataforma según ramas; su implementación completa no está aquí. No agregar otra copia de jQuery, lightbox ni slider sin demostrar necesidad.

store.js combina comportamiento global y de páginas. Carga después de LS.ready. Hay delegación en document para carrito/variantes, listeners de scroll/resize, MutationObserver, ResizeObserver, IntersectionObserver, setInterval de contadores y requestAnimationFrame. El inventario de símbolos está en [eventos y hooks](../09-integrations/events-and-hooks.md).

Optimizaciones existentes: initSwiper diferido cerca del viewport en ciertos casos, autoplay diferido a interacción mobile, guardas de instancia, separación de tareas por setTimeout y protección de delegados de galería. `setTimeout(0)` divide tareas pero no reduce su trabajo total. Del mismo modo, passive no vuelve barato un callback que mide layout.

Riesgos a perfilar: varios handlers globales de scroll, lecturas de getBoundingClientRect/offsetHeight junto a escrituras de estilo, observers del header y PDP, listeners de message para vídeo y timers al reconciliar editor. No se confirma fuga de memoria sin comparar listeners/heap tras ciclos; son zonas de investigación. No se encontró una estrategia general de import() en estos archivos.

Para reducir coste, primero deshabilitar funciones nativas innecesarias por settings y medir. Después evaluar carga por ruta/feature usando la infraestructura existente, manteniendo orden de dependencias y estado del editor. No partir bundles a ciegas: más solicitudes, parseo duplicado o LS antes de ready pueden empeorar el resultado. El grafo determina qué puede separarse.

La pantalla de password cargó scripts Embla/Sectionfy de otra instalación. Son un hallazgo de esa superficie, no una razón para borrar archivos locales que no existen. Las oportunidades «unused JS» de Lighthouse se refieren al recorrido medido; no prueban que el código no se use al abrir carrito, menús o variantes.
