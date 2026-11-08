# Límites reales de esta investigación

Fecha: 2026-11-08. La barrera inicial de storefront se resolvió mediante acceso explícito del propietario. No se obtuvo acceso al Admin ni a cuentas de clientes.

- Las 51 secciones y 54 bloques se inventariaron en source; solo 26 tipos de sección aparecieron en rutas del crawl. No se crearon instancias/configuraciones para probar presets ausentes.
- Los 708 controles se analizaron como definiciones; su interfaz real, condiciones efectivas y validación al guardar en Brand Editor no se ejercitaron.
- Se agotó la cola de rutas normalizada, no todas las combinaciones posibles de filtros, variantes, paginación y querystrings. El recorrido no incluye acciones de logout ni endpoints administrativos.
- Cuenta privada, órdenes, direcciones, suscripciones y checkout transaccional no se inspeccionaron con datos autenticados. No se agregaron productos ni se aplicaron cupones.
- La carga posterior del listado no incrementó las 12 tarjetas en el intento automatizado registrado. No se declara funcional ni rota de forma general sin una reproducción controlada adicional.
- Métricas: una muestra Lighthouse por ruta/perfil, seis ejecuciones storefront y dos password. Sin CrUX, RUM, Search Console, PSI o WPT.
- Accesibilidad: axe/teclado y geometría en Chrome. Sin certificación AA, lector de pantalla ni otros motores/dispositivos reales.
- Robots y sitemap con sesión se inspeccionaron; los gzip CDN declarados respondieron 403 al cliente HTTP usado. No se infiere que Googlebot reciba el mismo resultado.
- No se encontraron derechos explícitos de redistribución del tema ni un mecanismo del editor para importar bibliotecas arbitrarias. No se implementó una biblioteca común.
- No se ejecutó una evaluación integral de vulnerabilidades, cobertura de CSS/JS por todos los estados ni heap profiling.
- Una pasada suplementaria de semántica obtuvo 30 HTML y 16 respuestas 429/desafío; estas últimas no se acreditan como páginas revisadas en esa pasada. El GET de checkout también recibió 429. No se eludió el desafío ni se volvió a ejecutar la pasada; los resultados previos del crawl y Lighthouse se mantienen separados.

Estas limitaciones se reflejan en el [informe de cobertura](../DISCOVERY-COMPLETENESS-REPORT.md). El número de documentos y capturas no elimina las áreas pendientes.
