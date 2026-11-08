# Arquitectura reutilizable propuesta

Fecha: 2026-11-08. **Diseño de arquitectura, no implementación.** Parte de las unidades reales del inventario.

| Capa | Unidades existentes | Regla de extensión |
|---|---|---|
| Global | Header, navegación, footer, anuncios, tokens, modals | Cambios globales con prueba de consumidores y todas las rutas representativas |
| Layout | JSON de header/footer/cart y templates de página | Componer tipos existentes, mantener orden y datos del comerciante |
| Contenido | Hero, banners, group, rich-text, media, FAQs | Variantes de configuración antes de archivos duplicados |
| Comercio | Card, product-form, galería, shipping, cart | Centralizar presentación compartida; conservar lógica nativa de negocio |
| Interacción | Swiper/createSwiper, ModalHandler, delegación y LS | Inicialización por instancia, guardas y limpieza donde proceda |
| Utilidad | Image, icon, botones, formularios, mensajes | Una sola entrada por responsabilidad, no forks privados de cada consumidor |

Un componente compartido debe recibir contenido, variante y parámetros visuales de instancia, mientras usa datos comerciales del contexto nativo. Evitar settings que dupliquen precio/stock. Su contrato debe indicar qué requiere del padre, hooks que preserva, valores de configuración y comportamiento sin JS.

Para una tarjeta distinta en una sección: primero comprobar reduced_item/slide_item y parámetros actuales. Si falta una variante, proponer un parámetro semántico acotado que altere solo presentación. Para una editorial mobile diferente, usar group/dirección y CSS con un solo DOM. Para arte distinto por dispositivo, extender el helper de imagen compartido tras medir sus callers.

La propuesta no obliga a transformar cada fragmento en una abstracción. Compartir algo que diverge en lógica de negocio puede crear condiciones inmanejables. La unidad reusable debe tener una razón verificable, consumidores conocidos y forma clara de probar compatibilidad.
