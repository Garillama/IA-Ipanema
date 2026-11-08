# Interfaces oficiales y alcance

Fecha: 2026-11-08. Investigación documental; no se creó una app, webhook ni integración. Las lecturas remotas realizadas fueron operaciones de temas del CLI autorizado.

| Interfaz | Finalidad / requisitos | Permisos y límites | Coste y alternativa |
|---|---|---|---|
| Admin API | Gestión de catálogo, categorías, pedidos y otros recursos; JSON/HTTPS | OAuth y scopes de app o credencial autorizada; backend, nunca token en tema | Red, cuotas y mantenimiento; usar editor/datos nativos para presentación |
| Storefront API | Frontend headless, catálogo público e inicio de compra | Autenticación/documentación propia; no equivale a Admin ni a editar archivos de tema | Añade cliente y lógica; innecesaria para reestilizar una card nativa |
| Theme CLI | Lectura/sincronización de archivos de una instalación | Identidad de tienda y tema; operaciones source sujetas a fork | El diff es verificable; watch/push pueden cambiar remoto |
| Nube SDK | UI de apps y eventos de comercio en superficies soportadas | App registrada, worker y slots, sin DOM arbitrario | Revisar proveedor, carga y contexto; preferir componente nativo cuando cubra el caso |
| Webhooks | Notificar backend de cambios | Registro autorizado, HTTPS y verificación de origen | Sin coste directo de UI; no sustituyen eventos interactivos del navegador |
| Componentes privados/LS | Renderizado y runtime nativo del tema | Contratos de la plataforma, parte del código no editable | Reutilizarlos; no tratarlos como API REST pública externa |

La [Admin API](https://tiendanube.dev/es-AR/api/getting-started) usa una versión de recurso y límites por tienda/app; la documentación consultada indica bucket 40 y reposición 2/s como base, con variaciones según plan. Respetar headers, 429 y alcance de permisos; no aplicar números de Admin a Storefront API. [Autenticación Admin](https://tiendanube.dev/es-AR/api/authentication).

La [Storefront API](https://tiendanube.dev/es-AR/storefront-api/getting-started) está orientada a catálogo público y checkout alojado, sin app OAuth para ese caso. Su [autenticación](https://tiendanube.dev/es-AR/storefront-api/authentication) se revisa por separado; no se llamó durante discovery ni se asume que el acceso por contraseña a la tienda conceda permisos administrativos.

[Product](https://tiendanube.dev/es-AR/api/resources/2025-03/product) y [Category](https://tiendanube.dev/es-AR/api/resources/2025-03/category) documentan campos de contenido/SEO, entre otros. Esa capacidad no justifica sobrescribir catálogo para cambiar una sección. El [changelog de la API](https://tiendanube.dev/es-AR/api/resources/2025-03/CHANGELOG) sirve para verificar cambios concretos antes de una integración; no se certifica aquí cada entrada histórica.

[Webhooks](https://tiendanube.dev/es-AR/api/resources/2025-03/webhook) notifican eventos como product/updated o theme/updated. Pueden repetirse y llegar fuera de orden; una futura integración necesitaría idempotencia y validar HMAC del cuerpo original con el secreto de app. No se registró endpoint de pruebas ni se asumió que el access token de tienda sea la clave de firma.
