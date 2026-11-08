# Registro de correcciones

| Fecha | Observación inicial | Evidencia nueva | Conclusión corregida |
|---|---|---|---|
| 2026-11-08 | `manifest.json` indica fork false y versión 1 | `theme diff --json` y `theme list --json` | Instalación 14837617: fork true, versión 1.8.0, publicada; manifiesto desactualizado. No se modificó |
| 2026-11-08 | URL preview asumida como candidata al tema auditado | Redirección a password y recursos de 14517784/1.2.1 | Los resultados del navegador pertenecen a la pantalla servida, sin atribución al storefront 1.8.0 |
| 2026-11-08 | Extractor encontraba `blocks/` como archivo literal ausente | Expresiones Twig concatenan el tipo de bloque | Se corrigió el extractor a `twig-dynamic-prefix`; no se reportan dependencias rotas por ese motivo |
| 2026-11-08 | Comentario de heading dice que emite p | Markup ejecutable del archivo emite div con richtext raw | La semántica no se deduce del comentario ni de las clases h1-h6 |
| 2026-11-08 | Podría suponerse paginación classic por setting global | `templates/pages/category.json` usa infinite en la sección | El valor efectivo de categoría se controla por instancia; se documentó el riesgo de enlaces en esa rama |
| 2026-11-08 | FAQPage podría tratarse como oportunidad de rich result | Google Search updates registra retirada de FAQ rich results en mayo de 2026 | Se distingue Schema.org de presentación en Google; no se promete ese resultado |
| 2026-11-08 | Storefront limitado por password | El propietario autorizó acceso y se verificaron assets 1.8.0 | Se amplió el discovery a rutas públicas; los resultados de password se conservaron separados |
| 2026-11-08 | Algunos campos de fichas figuraban como no ejecutados por el bloqueo inicial | Crawl y matriz responsive posteriores | Se enlazó evidencia runtime parcial sin certificar todas las variantes de cada unidad |
| 2026-11-08 | Extractor asignaba la primera línea a un ID de setting repetido | Un schema contiene el mismo ID en otra declaración privada | Se corrigió una referencia de línea; conteos y hashes del origen permanecen iguales |
| 2026-11-08 | Lighthouse SEO 92 podría atribuirse a productos no descubribles | Selectores del audit crawlable-anchors | En categoría/PDP señaló anchors de acciones; el riesgo de paginación se sustenta en prueba sin JS separada |
| 2026-11-08 | Botón de carga no interactuable podía interpretarse como autoload ya realizado | Antes/después del intento conserva 12 tarjetas | Se corrigió el rótulo del instrumento; no se acredita carga posterior funcional |
| 2026-11-08 | Fetch sin excepción podía contarse como lectura HTML correcta | La pasada suplementaria devolvió 16 HTTP 429 y un desafío en checkout | Se separaron 30 respuestas correctas de las limitadas y se corrigió el instrumento para detenerse ante 403/429. No se reejecutó contra el sitio |

Cada cambio corrige la conclusión principal; esta bitácora conserva por qué cambió, sin duplicar los informes técnicos.
