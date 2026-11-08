# Arquitectura de enlazado

Fecha: 2026-11-08. El grafo de rutas del crawl complementa el grafo de archivos: uno muestra destinos navegables y el otro quién renderiza cada parte. No son intercambiables.

Priorizar caminos home → categoría → producto, subcategorías y enlaces contextuales pertinentes. Un enlace necesita destino real y texto que describa lo que se encontrará; una imagen sin nombre accesible y un CTA repetido «ver más» fuera de contexto aportan poca claridad. Las tarjetas existentes enlazan imagen y nombre: mantener esas URLs al rediseñar.

Para auditar profundidad, normalizar URL sin fragmentos/tracking, conservar paginación relevante y contar destinos únicos. Los duplicados del loop no reducen profundidad. Cruzar productos del sitemap con enlaces del HTML inicial y del DOM, registrando qué productos solo aparecieron después de una carga incremental.

No introducir bloques masivos de enlaces irrelevantes en footer como sustituto de una navegación clara. Los enlaces externos de contacto/legal no se consideran categorías del catálogo. Comprobar roturas con GET y status final, distinguiendo redirect, 404, login y password.

Limitaciones del crawler actual: solo mismo origen; descarta acciones/logout y normaliza queries a page/q. Por tanto no representa todas las facetas, variantes ni checkout. La cola restante y exclusiones se conservan para no afirmar cobertura total por una normalización conveniente.
