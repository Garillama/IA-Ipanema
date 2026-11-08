# Registro de evidencia

Verificación: **2026-11-08**. Las marcas temporales UTC de ejecución están en cada JSON. El registro diferencia evidencia estática, observación remota, laboratorio e hipótesis. No hay pruebas comerciales aprobadas por inferencia.

| ID | Artefacto / fuente | Método | Estado y límite |
|---|---|---|---|
| E01 | [source-summary](measurements/source-baseline/source-summary.json) | Escáner Python, origen en lectura | 330 archivos y conteos; no ejecuta Twig |
| E02 | [hashes y tamaños](measurements/source-baseline/source-inventory.json) | SHA-256/bytes | Identidad de archivos; no transferencia CDN |
| E03 | [componentes y schemas](measurements/source-baseline/components.json) | Extracción .tpl/schema | 223 unidades; clases léxicas y propiedades por verificar en DOM |
| E04 | [settings](measurements/source-baseline/settings.json) | JSON/schema y traducción es-MX | 708 definiciones, incluidas privadas anidadas; no UI ejercitada |
| E05 | [dependencias](measurements/source-baseline/dependency-graph.json) | Includes literales, prefijos dinámicos y JSON | 646 referencias; no call graph completo de plataforma |
| E06 | [hijos de schema](measurements/source-baseline/schema-dependencies.json) | Resolución de types/tags | Hijos posibles, no presencia efectiva |
| E07 | [instancias JSON](measurements/source-baseline/template-instances.json) | Recorrido de sections/blocks | 178 instancias y valores guardados |
| E08 | [diff remoto](measurements/source-baseline/remote-diff.json) | CLI de lectura | 329 iguales; identidad/fork de la operación |
| E09 | [temas relevantes](measurements/source-baseline/remote-themes.json) | CLI list, salida filtrada | Instalaciones relevantes; sin credenciales/revision_token |
| E10 | [sondas sin sesión](measurements/http/route-probes.json) | HTTP GET, redirects | Password para rutas/endpoints en ese momento |
| E11 | [URL del propietario sin sesión](measurements/http/owner-public-url.json) | Chrome aislado | Versión de assets de pantalla de acceso |
| E12 | [home después de acceso](measurements/browser/storefront-discovery.json) | Chrome con sesión autorizada en memoria | 1.8.0 y composición real; no Admin |
| E13 | [crawl](measurements/crawl/summary.json) | Rutas del sitemap/enlaces, GET | 48 intentos; queries normalizadas y acciones excluidas |
| E14 | [responsive](measurements/responsive-matrix/summary.json) | Recargas de 12 tipos ×6 anchos | 72 muestras, más home ×6 en browser/storefront-* |
| E15 | [home 390](measurements/browser/storefront-viewport-390.json), [home 1440](measurements/browser/storefront-viewport-1440.json) | DOM, red, observers y axe | Laboratorio; observers de carga no son INP de campo |
| E16 | [estados de interacción/scroll](measurements/browser/state-audit.json) | Menú, foco, Escape, medios y variante | Sin transacciones; incluye intento no concluido de drawer vacío |
| E17 | [sin JS de comercio](measurements/browser/no-js-commerce.json) | Categoría/PDP 390 sin JS de página | No se enviaron formularios de compra |
| E18 | [estados adicionales](measurements/browser/additional-states.json) | Orden, filtro GET, intento carga, ubicación H1 y sitemap de blog | Una combinación/opción; carga posterior no aprobada |
| E19 | [Lighthouse storefront](../05-performance/storefront-lighthouse-results.md) | Seis ejecuciones independientes, perfiles simulados | Una muestra por ruta/perfil; sin advertencias de redirect |
| E20 | [Lighthouse password mobile](measurements/lighthouse/mobile.json), [desktop](measurements/lighthouse/desktop.json) | Dos ejecuciones antes de acceso | Contexto antiguo separado, con advertencia de redirect |
| E21 | [robots](measurements/crawl/robots.txt), [sitemap](measurements/crawl/sitemap.xml), [blog](measurements/crawl/sitemap-blog.xml) | GET con sesión autorizada | No certifican acceso del robot sin sesión |
| E22 | [CDN de sitemaps](measurements/crawl/cdn-sitemaps.json) | HTTP GET al gzip declarado | 403 en herramienta, no inferir respuesta a Googlebot |
| E23 | [cobertura derivada](measurements/coverage-summary.json) | Conteo de resultados guardados | No reemplaza evidencia primaria |
| E24 | `tools/check_workspace.py` | Links, JSON e integridad del origen | Resultado final guardado en measurements/workspace-validation.json |
| E25 | [semántica suplementaria](measurements/browser/semantic-audit.json) | GET + DOMParser, H1–H6/landmarks/IDs | 30 HTML válidos; 16 respuestas 429, y checkout 429, marcados como acceso limitado. No reemplaza el crawl anterior |

Capturas: [índice por ruta](../10-quality/runtime-page-audit.md), [por tipo/ancho](../10-quality/responsive-results.md) y directorio screenshots. Se conservaron 216 PNG al cierre del inventario de ejecución; el conteo fechado está en coverage-summary. Las capturas inicial/cargada no son un filmstrip de todos los paints.

No se guardaron cookies, contraseña, headers Authorization ni valores de acceso. No se exportaron HAR/trace con sesiones. Las estimaciones de ahorro de Lighthouse permanecen estimaciones; ningún cambio se implementó para acreditarlas como ahorro conseguido.

Las fuentes públicas y su método están en [references](references.md). Las correcciones de conclusiones y del extractor se conservan en [bitácora](corrections-log.md).
