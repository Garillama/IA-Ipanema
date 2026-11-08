# Resultados Lighthouse del storefront

2026-11-08, Lighthouse 13.6.0, una muestra por ruta/perfil. Las seis ejecuciones del storefront finalizaron en la ruta solicitada y sin advertencias. Laboratorio simulado, no datos de campo; TBT no sustituye INP. Password inicial queda en archivos mobile/desktop sin prefijo y no se mezcla aquí.

| Ruta / perfil | Performance | LCP ms | FCP ms | TBT ms | CLS | Evidencia |
|---|---:|---:|---:|---:|---:|---|
| home-mobile | 76 | 4133 | 1372 | 403 | 0 | [JSON](../13-evidence/measurements/lighthouse/home-mobile.json) · [HTML](../13-evidence/measurements/lighthouse/home-mobile.html) |
| home-desktop | 98 | 1056 | 393 | 51 | 0.0028 | [JSON](../13-evidence/measurements/lighthouse/home-desktop.json) · [HTML](../13-evidence/measurements/lighthouse/home-desktop.html) |
| category-mobile | 78 | 3834 | 1357 | 417 | 0 | [JSON](../13-evidence/measurements/lighthouse/category-mobile.json) · [HTML](../13-evidence/measurements/lighthouse/category-mobile.html) |
| category-desktop | 91 | 1825 | 447 | 38 | 0.0712 | [JSON](../13-evidence/measurements/lighthouse/category-desktop.json) · [HTML](../13-evidence/measurements/lighthouse/category-desktop.html) |
| pdp-mobile | 78 | 3492 | 1384 | 485 | 0 | [JSON](../13-evidence/measurements/lighthouse/pdp-mobile.json) · [HTML](../13-evidence/measurements/lighthouse/pdp-mobile.html) |
| pdp-desktop | 98 | 960 | 471 | 6 | 0.0723 | [JSON](../13-evidence/measurements/lighthouse/pdp-desktop.json) · [HTML](../13-evidence/measurements/lighthouse/pdp-desktop.html) |

Mobile: 412×823, DPR 1.75; red/CPU simuladas de Lighthouse (RTT 150 ms, throughput 1638.4 Kbps y CPU ×4). Desktop: 1350×940, DPR 1, RTT 40 ms, throughput 10240 Kbps y CPU ×1. Los parámetros completos están en cada summary.

El LCP de home se atribuyó al placeholder del hero; las recomendaciones deben distinguir ese medio de una imagen final de marca. Los insights de ahorro son estimaciones de Lighthouse y no ahorros ya obtenidos. El audit crawlable-anchors de categoría/PDP señaló controles de acción (borrar filtro, reproducir vídeo); no demuestra por sí solo que falten enlaces a productos. El riesgo independiente de paginación sin href está confirmado en source y prueba sin JS.
