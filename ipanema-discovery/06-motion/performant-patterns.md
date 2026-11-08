# Matriz de animaciones propuesta

Fecha: 2026-11-08. Costes esperados, no tiempos medidos. L=layout, P=paint, C=composición. «GPU posible» nunca significa gratuito. Cada fila debe validarse en móvil y con movimiento reducido.

| Efecto / objetivo UX | Propiedades / técnica | Coste esperado | JS / mobile | Accesibilidad y recomendación |
|---|---|---|---|---|
| Hero: entrada editorial | opacity/transform, CSS | C posible; gran superficie puede costar memoria | 0 JS; simple en mobile | Mostrar contenido sin motion; no retrasar LCP |
| Fade in: continuidad | opacity | C posible, P inicial | 0 JS si no depende de viewport | No esconder texto por fallo de callback |
| Reveal/slide in | translate y opacity | C posible | IO si se activa por visibilidad | Estado base visible; desactivar desplazamiento con reduce |
| Stagger | Delays acotados de la misma transición | Multiplica tiempo/capas aunque no L | CSS; reducir elementos mobile | No demorar CTA ni lectura; limitar retraso total |
| Hover de tarjeta | transform en imagen o borde | C para transform, P para borde/sombra | CSS, hover:hover | Mismo contenido y acción con teclado/touch |
| Zoom de imagen | scale con overflow acotado | C/memoria; imagen debe tener resolución suficiente | CSS; lightbox nativo si procede | Activación clara, botón de cerrar y retorno de foco |
| Parallax | transform por posición | Lecturas geométricas + C/P posibles | JS rAF o enhancement; omitir mobile si no aporta | Off con reduce; no mover contenido de lectura |
| Sticky header | position sticky, transición de estado | L al cambiar altura; C si solo desplaza | CSS donde baste; JS para lógica existente | No tapar foco; reservar espacio |
| Text reveal | opacity/transform del bloque | C; fragmentar por letra aumenta DOM | Evitar split de caracteres por defecto | Conservar un nombre/texto continuo para AT |
| Carrusel | Motor existente o native scroll | C, imágenes, clones y ejecución | Swiper ya cargado o scroll nativo | Teclado, pausa, nombres y foco de slides |
| Marquee | translateX repetido | C continua, memoria/nodos duplicados | CSS+clones existentes | Alternativa estática; controlar repetición y pausa |
| Dropdown | opacity/transform y visibility | C/P acotado | CSS+estado accesible; no solo hover | Botón de expansión, Escape, recorrido de foco |
| Drawer/modal | translate/opacity del panel | C/P por overlay/superficie | Handler nativo | Gestión de foco, nombre, scroll lock y Escape |
| Accordion | details nativo o altura medida | Height implica L; transform no cambia flujo | Preferir contrato existente | Botón/expanded o details; contenido disponible |
| Cart feedback | Mensaje reservado y transición corta | Puede provocar L si cambia altura sin reserva | LS nativo | Anuncio de estado; no duplicar solicitud de compra |
| Skeleton | Fondo/opacity de placeholder | P o C repetitiva | CSS; reducir área/número | No ocultar estado de carga; versión sin movimiento |
| Microinteracción | opacity/transform de icono/estado | C pequeña posible | CSS/WAAPI si hace falta cancelar | No transmitir resultado solo con color/movimiento |

Para cada candidato: capturar traza, localizar L/P/C, observar memoria de capas y ejecutar la interacción durante el efecto. No concluir coste solo por FPS desktop ni por ausencia de cambio de layout. Scroll-driven requiere soporte comprobado del navegador objetivo y un diseño final estable si no está disponible.
