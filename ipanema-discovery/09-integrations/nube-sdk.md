# Nube SDK

Fecha: 2026-11-08. El SDK oficial permite apps en Web Workers que leen estado y se comunican mediante eventos, renderizando UI declarativa en slots. No ofrece acceso arbitrario al DOM ni reemplazo libre de cualquier sección visual. [Visión general oficial](https://tiendanube.dev/apps/nube-sdk/overview).

El código local incluye 65 llamadas literales a `nubesdk-slot`; eso cuenta ubicaciones del source, no 65 slots únicos/activos simultáneamente. Hay puntos alrededor de precio, medios, CTA, cards y carrito. `data-store` es otro contrato de integración; eliminarlo puede romper apps aunque el diseño parezca igual. [Guía de integración del tema](https://tiendanube.dev/themes/sectionable-themes/app-integration).

Los [slots disponibles](https://tiendanube.dev/apps/nube-sdk/api/available-slots) pueden descubrirse mediante getAvailableSlots en contextos soportados, con métodos asíncronos. La documentación consultada excluye esa API en Patagonia y checkout por el momento. Esa limitación de descubrimiento no significa que no haya slots de checkout por otros contratos. No fijar IDs de instancias dinámicas entre páginas/tiendas.

Antes de proponer una app: identificar finalidad, slot real, evento documentado, disponibilidad del estado, permisos/registro, tamaño del bundle y fallback. Un badge o extensión comercial compartida podría justificarla; cambiar padding o tipografía normalmente se resuelve en el tema. No se instaló una app ni se probó su aislamiento o consentimientos en esta tienda.

Ejemplo de decisión: una UI después del precio requiere comprobar ese slot y contexto, no buscar un selector CSS global y manipularlo desde el worker. Mantener precios y stock en datos de plataforma; no replicarlos como settings del tema. [Primeros pasos](https://tiendanube.dev/apps/nube-sdk/getting-started).
