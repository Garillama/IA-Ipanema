# Motion con coste controlado

Fecha: 2026-11-08. Principios propuestos sobre patrones encontrados, no un benchmark de cada efecto. La fuente nativa está en style-critical.css, style-async.css y funciones de store.js.

Una animación debe comunicar estado, relación o respuesta. Transform y opacity suelen permitir trabajo de composición en condiciones adecuadas, pero superficies grandes, capas, memoria, blur, imágenes pesadas y cambios simultáneos pueden mantener el coste alto. La promoción a GPU no está garantizada por escribir translate3d. [Guía de animaciones de web.dev](https://web.dev/articles/animations-guide).

Separar layout, paint y composición al perfilar. Animar height/top puede recalcular layout; box-shadow/filter puede requerir repintado; transform/opacity puede componer superficies ya pintadas, pero hay que medir. No añadir will-change a todas las tarjetas o capas permanentes sin necesidad.

La tienda debe funcionar con contenido visible antes del enhancement. Usar transitions para cambios de estado simples, CSS keyframes para secuencias conocidas, WAAPI si se necesita control temporal/cancelación y IntersectionObserver para activar trabajo al entrar, no por cada scroll. Scroll-driven animations pueden ser una mejora optativa con detección y fallback, no una dependencia de compra. [Referencia MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations).

El proyecto ya trae animaciones de contenido y un parallax. Antes de introducir una biblioteca, comprobar si CSS o el motor existente cubren el pedido. Una biblioteca se justifica cuando orquesta una secuencia necesaria que no puede mantenerse razonablemente con herramientas nativas; añade bytes, integración y responsabilidad de accesibilidad.

No se implementaron efectos. [Matriz de patrones y costes](performant-patterns.md), [movimiento reducido](motion-accessibility.md).
