# Indexación y límites de control

Fecha: 2026-11-08. La indexación requiere más que encontrar un enlace. Separar respuesta HTTP, acceso del robot, renderizado, canonical elegida e incorporación al índice. No se consultó Search Console ni se comprobó la indexación real.

| Caso | Validación necesaria | Criterio propuesto |
|---|---|---|
| Robots / noindex | robots.txt sin sesión, meta robots y X-Robots-Tag de cada tipo | Bloquear rastreo no sustituye noindex; un robot necesita poder leer la directiva |
| Canonical | HTML inicial, una sola señal coherente, URL que responde | No usarlo como redirección ni garantía de selección; respetar contenido distinto |
| Filtros y orden | Combinaciones reales, facetas útiles vs variantes redundantes | Evitar espacios ilimitados; decidir páginas indexables según contenido/demanda, no noindex masivo |
| Paginación | URL única y enlaces siguientes | No ocultar todo el catálogo posterior detrás de interacción |
| Sin resultados / categoría vacía | HTTP, mensajes, enlaces alternativos, metadatos | No indexar masivamente páginas sin valor; decisiones desde capacidades de plataforma comprobadas |
| Agotado temporal | Estado real, Offer y alternativas | Mantener información útil; no borrar automáticamente la URL |
| Descontinuado | Sustituto pertinente, enlaces entrantes y gestión de redirecciones | Evitar redirigir productos sin relación a home |
| Cambio de URL | Redirect real y enlaces internos actualizados | No simular 301 con JS o meta refresh |
| 404 | Código 404 y links de recuperación | Distinguir soft 404 de error HTTP |

La plataforma genera canonical mediante head-tags y los campos SEO provienen de contenido de tienda. La [guía de canonical de Google](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls) describe señales de consolidación, no un mecanismo para arreglar la navegación o imponer indexación. Toda política propuesta debe contrastarse con el HTML/headers de Tiendanube, sin reemplazar el componente privado.

La tienda protegida por contraseña no equivale al sitio público listo para indexar. No se quitó esa protección. Antes de lanzamiento, repetir robots, sitemap, 404, canonical, parámetros y renderizado sin cookies del auditor.
