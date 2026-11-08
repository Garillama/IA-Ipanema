# Carrito, drawer y compra

Fecha: 2026-11-08. Fuente: sections/cart-drawer.tpl, main-cart.tpl, snippets/cart/*, promotions/coupon-input.tpl y store.js L2752, L3486, L3595.

Existe página de carrito y cart drawer. El layout cart_drawer se compone como grupo JSON y la sección incluye el modal/panel. Los fragmentos compartidos renderizan ítems, totals, resumen, fulfillment, mínimos, promociones, cupón y cross-selling según datos. No se verificó la disponibilidad efectiva de cupones ni condiciones de la cuenta.

La ruta moderna de carrito puede servir HTML cacheado sin estado personal y restaurarlo con LS.asyncCart si `asyncCartConfig` está presente. El tema inicia ese proceso y aporta hooks. Conserva el nodo modal existente cuando reemplaza contenido, porque plataforma/analytics lo observan. Esa sustitución de estado de comercio no equivale a hidratación React ni justifica redibujar toda la página.

Las operaciones de cantidad y eliminación usan LS.removeItem, minusQuantity, plusQuantity y changeQuantity. El favicon escucha **`cart.updated`**; no confundir ese evento DOM con **`cart:update`** del SDK. Las recomendaciones y notificaciones pueden acompañar una compra; un nuevo botón debe usar el formulario/contrato existente, no emitir otra solicitud en paralelo.

El cálculo de envío está compartido con PDP e incorpora persistencia de zipcode/opciones. No se llamó manualmente a endpoints internos mencionados en comentarios. No se crea carrito de prueba ni se aplica cupón sin autorización de una prueba con estado.

Pruebas pendientes: vacío/con ítems, mínimo, límites de stock, cupón válido/inválido, envío rechazado, cambios rápidos de cantidad, drawer abierto antes de restaurar estado, error de red y paso a checkout. Medir si badge/totales cambian sin reserva de espacio, y anunciar cambios sin mover foco innecesariamente. El checkout alojado es plataforma; los estilos encontrados no permiten reconstruirlo libremente.
