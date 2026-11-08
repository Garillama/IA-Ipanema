# Matriz de pruebas

Fecha: 2026-11-08. La contraseña inicialmente limitó el acceso; después el propietario autorizó el desbloqueo y se continuó. Los resultados antes/después permanecen separados.

| Prueba | Ejecutada | Evidencia / alcance |
|---|---|---|
| Inventario, schemas y JSON | Sí | 330 archivos; 105 schemas de secciones/bloques y schema global; sin errores JSON detectados |
| Comparación remota de archivos | Sí, lectura | 329 comparables iguales; fork true; no garantiza origen oficial intacto |
| Crawl de rutas | Sí | 48 intentos; 46 destinos HTML únicos tras excluir XML y alias de cuenta; cola normalizada vacía |
| HTML inicial vs DOM | Sí | Registros por ruta con links, H1, JSON-LD y metadatos |
| Semántica H1–H6 suplementaria | Parcial | 30 HTML obtenidos; 16 respuestas 429 no se acreditan como páginas de tienda. El crawl principal previo conserva sus 48 intentos y resultados |
| 360/390/768/1024/1440/1920 | Sí | Home y un representante de cada uno de los otros 12 tipos públicos, con recarga; no cada producto en seis anchos |
| Capturas de rutas a 390/1440 | Sí | Todo el crawl; mobile tras resize, distinto de carga fría |
| axe WCAG A/AA | Sí | Home y representantes a 390/1440; menú abierto; no certificación integral |
| Sin JavaScript / reduced-motion / red y CPU | Sí | Home en los tres modos; categoría/PDP también sin JS a 390; red 150 ms, descarga 200,000 B/s y CPU ×4 en home; no datos de campo |
| Scroll completo y medios | Sí | Home, categoría y PDP; respuestas adicionales, imágenes y duplicados DOM |
| Menú, Escape, foco | Sí, automatizado | Estado reproducido y capturas; no lector de pantalla |
| Cambio de variante | Sí, selección sin compra | Una PDP con cuatro opciones; sin assert de todos los precios/stock |
| Carrito vacío | Página sí; drawer no abierto en intento | No se declara drawer aprobado |
| Filtros activos / orden / páginas posteriores | Parcial | Una combinación de precio y orden ascendente ejecutados; intento de carga no aumentó tarjetas; faltan otras combinaciones y reproducción de esa carga |
| Lighthouse | Sí | Password inicial y suite home/categoría/PDP; resultados y perfiles conservados |
| Perfil de interacción / INP de campo | No | No RUM/CrUX/Search Console autorizado ni instalado |
| Coverage de todos los estados / heap leaks | No | Lighthouse unused en recorrido no sustituye ese estudio |
| Pago, cupón aplicado, compra, newsletter/contacto enviados | No | Cambian estado; fuera del discovery sin mutaciones comerciales |
| Cliente autenticado / órdenes / suscripciones privadas | No | No credenciales ni datos de cliente autorizados para esa sesión |
| GET de checkout vacío | Intentado, limitado | HTTP 429/desafío; no se probó checkout con productos o pago, ni se reintentó tras registrar el límite |
| Editor autenticado y guardar configuraciones | No | Schemas y guía pública revisados; no se abrieron controles del Admin |
| Rich Results / Schema Validator / Search Console / PSI / WPT | No | Parseo local de JSON-LD no se presenta como estas herramientas |
| Otros navegadores, lector de pantalla y dispositivos reales | No | Chrome local; no emulación suficiente para declararlos probados |

La lista de 48 URLs contiene una sonda 404 intencional y un endpoint XML del sitemap; no se presenta como 48 páginas comerciales distintas. Las URLs de filtros/variantes se normalizaron para evitar un espacio ilimitado. La cola vacía significa agotamiento de esa estrategia de descubrimiento, no conocimiento de todas las rutas posibles de plataforma.

Los scripts están en `tools/`. Los de browser registran heurísticas, no verdades absolutas: rectángulo en viewport no equivale a visibilidad completa, bytes de Resource Timing pueden ser cero por restricciones cross-origin/caché y screenshot initial no es captura de cada paint. Conservar esas limitaciones al interpretar resultados.

No se creó un mock de plataforma ni se intentó renderizar Twig con un motor ajeno. La plataforma real fue la fuente de renderizado. Las rutas de cuenta privada y checkout se evalúan solo en el alcance permitido, sin usar la contraseña del storefront como credencial administrativa.
