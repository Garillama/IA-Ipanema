# Animaciones encontradas

Fecha: 2026-11-08. Confirmación por código; cada variante no configurada en la tienda permanece sin prueba visual.

| Patrón real | Fuente / comportamiento | Riesgo a comprobar |
|---|---|---|
| Fade/slide-up/slide-down de contenido | style-critical L254–335, hero/slideshow content_animation | Stagger puede retrasar texto importante; fallback debe permanecer visible |
| Fade de imágenes | fade-in opacity 0 hasta lazyloaded/swiper-lazy-loaded | Si falla loader puede haber URL/espacio pero imagen invisible |
| Placeholder shine/fade | Keyframes de opacity repetitivos | Movimiento continuo y consumo en listas largas |
| Enter/leave utilitario | translateY y opacity, 200/150 ms declarados | El teardown debe retirar el estado al terminar |
| Transition-up | top y opacity, transition all | Puede implicar layout, no solo composición |
| Parallax hero | initHeroParallax L3958; rAF, desktop y reduced-motion | Lee geometría y escribe transform; coste con varias secciones |
| Sticky/slim/transparent header | initStickyHeader/TransparentHeader/SlimHeader | Geometría, scroll, placeholder y foco bajo encabezado fijo |
| Sliders y galería | Swiper, autoplay condicional | Pausa, clones, foco, listeners y selección de recursos |
| Marquee de anuncio | initAdbar clona contenido y CSS translateX | Repetición de enlaces/lectura, pausa y reduced-motion |
| Modal/drawer | Contratos ModalHandler y CSS de modal | Foco, Escape, scroll lock y retorno al disparador |
| Hover de card | CSS y product_hover | No condicionar información indispensable a hover |

Hay dos reglas de reduced-motion en critical: contenido hero/slideshow y utility enter/leave. La función de parallax también consulta la preferencia. No se encontró una protección universal que cubra marquee, todos los loaders o autoplay. No interpretar dos coincidencias como cumplimiento integral.

Los tokens `--transition-fast`, normal y slow contienen `all 0.2s`, `all 0.3s` y `all 1s ease`. Para efectos nuevos conviene declarar propiedades concretas; cambiar esos tokens globales sin revisar consumidores puede afectar toda la tienda.
