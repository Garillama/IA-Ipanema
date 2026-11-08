# Analytics, píxeles y consentimiento

Fecha: 2026-11-08. No se editó GA4, Meta Pixel, data layer ni configuración de apps. Los recursos de red permiten ver scripts observados, pero no un inventario completo de integraciones del Admin.

La [API de Analytics de Nube SDK](https://tiendanube.dev/es-AR/apps/nube-sdk/api/analytics) envía eventos al proveedor del host sin manipular DOM; la documentación consultada indica GA4 como proveedor compatible en ese lanzamiento. Su diseño agnóstico no acredita soporte actual de Meta ni datos históricos de sesiones. Resolver la Promise confirma despacho del host, no recepción final en el sistema externo.

Para un rediseño, preservar los nodos y eventos que la plataforma observa. El carrito asíncrono conserva el modal por esa razón. Agregar un handler que también emita add_to_cart cuando la plataforma ya lo hace puede duplicar conversiones. No inferir que un cambio de precio en la UI sea una nueva compra.

Propuesta de validación: inventariar proveedor/propiedad/evento/owner, revisar eventos por una sola acción autorizada y comprobar duplicados y payloads sin datos personales. El consentimiento se revisa con configuración y comportamiento reales; un banner visible no prueba que todos los scripts esperen aceptación ni que cumpla requisitos jurídicos de cada mercado.

Las pruebas de compra y envío de eventos comerciales no se ejecutaron porque implican estado o integraciones. Los scripts del auditor no agregan un proveedor ni instrumentación al tema: únicamente observan el navegador local y guardan resultados. Antes de instalar una app de medición adicional, comprobar las capacidades nativas y su coste de red/hilo principal.
