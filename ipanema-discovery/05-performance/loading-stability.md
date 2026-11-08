# Evitar un diseño inicial y otro al terminar de cargar

Fecha: 2026-11-08. Este es el criterio principal para futuros cambios. Se distinguen FOUC por estilos tardíos, cambio de métricas tipográficas, CLS por geometría y actualización legítima de estado comercial. No todo cambio visual es CLS y no todo CLS proviene de JS.

El layout solicita CSS base antes del contenido y CSS async por media print/onload; no declara un noscript alternativo para ese link. En la fuente, imágenes con fade-in y data-src dependen del loader. El header transparente emite estilos iniciales antes de JS, y los sliders tienen reglas para estado sin inicializar. Esas protecciones se deben conservar. [Ciclo de carga](../01-architecture/rendering-lifecycle.md).

Propuesta para cada sección:

1. Renderizar contenido y layout definitivos desde Twig/CSS. Usar la misma estructura antes/después del enhancement.
2. Reservar ratio y dimensiones para medios, espacio para badges/counters y contenedores de elementos dinámicos cuando sea viable.
3. Evitar medir todo con JS para luego mover nodos entre columnas; usar grid/flex para composición responsive.
4. Cargar el CSS necesario para la geometría inicial antes del primer paint; diferir solo lo que no cambia ese layout.
5. Animar un estado ya estable. No poner opacity 0 sobre el contenido esencial esperando un callback que podría fallar.
6. Probar carga fría, JS lento/bloqueado, fuentes tardías y cambios de breakpoint; comparar filmstrip y atribución de shifts.

No se propone ocultar body con un preloader. Eso puede esconder el síntoma, empeorar LCP y dejar una tienda vacía si JS falla. Tampoco añadir !important a todo para «fijar» el primer diseño.

La pantalla de contraseña mostró CLS desktop 0.296 y desplazamientos del footer; Lighthouse también señaló fuentes para algunos de ellos. La causa principal de cada shift requiere traza de la página exacta. Se guardaron capturas inicial/cargada, pero no se presenta esa pareja como filmstrip exhaustivo. No se trasladó ese valor a otras páginas.
