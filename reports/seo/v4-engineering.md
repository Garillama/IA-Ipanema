# IA-Ipanema V4: implementación local y uso

## Cierre técnico de las observaciones humanas sobre v3

Entrega actual: [parche final único](v4-review-corrections-final.patch), SHA-256 `4369d84d3a84bd99808d92eb12ad13bcf185f300615817bb6eedd517412acc6f`, **sin aplicar**. Corrige el parser para distinguir directivas independientes de valores con `=`/`:` y respeta las comillas al separar X-Robots-Tag. Se acredita la identidad del original v3 frente a su manifiesto y al candidato exacto; el texto exportado con hash diferente no se usa para aplicación.

[Matriz final](v4-final-review/matrix.md) · [validación y hashes](v4-final-review/validation.json) · [ZIP con bytes exactos y SHA256SUMS](v4-final-review.zip). Sobre candidato aislado: 50 pruebas específicas incluidas en 134 unitarias SEO, 13 integración, TLS local y la suite SEO existente aprobados. El diff final se aplica directamente a una base nueva y coincide con el árbol probado, sin apilar versiones. Se solicita aprobación humana explícita conforme al punto 6 de la petición actual; no se afirma aprobación independiente ni consenso dual. Tema, producción y crawler externo permanecen fuera de alcance.

## Revisión posterior del parche — antes de aplicar

**Entrega actual: propuesta v3 sin aplicar.** La revisión real de v2 por Claude detectó una regresión de rutas de acción con sufijos; Codex no completó esa ronda por inactividad y el consejo quedó `needs_evidence`. La [matriz final](v4-patch-review/matrix.md) incluye cada observación, contraejemplo, prueba y condición pendiente. [Parche v3](v4-review-corrections-v3.patch) · [delta respecto de v2](v4-review-v2-to-v3.patch) · [evidencia y hashes](v4-patch-review/v3-validation.json). La v3 corrige esos casos en aislamiento: 34 pruebas específicas incluidas en 122 unitarias SEO, 13 de integración y TLS real en loopback aprobados. Su aplicación y revisión/aprobación correspondientes siguen pendientes. La evidencia no se presenta como aprobación dual ni como código ya corregido en el workspace.

Se conservó el parche original y se repitieron sus cinco defectos en una copia nueva: fallan antes y pasan después. Las pruebas ampliadas revelaron seis casos pendientes con ese parche: ciclos y presupuesto de redirects de sitemap, salidas internas de páginas comprobadas por sitemap sin HTTP, NAT64 con IPv4 privada, rutas comerciales con sufijos y solicitud iniciada después de agotarse la espera. Se preparó una propuesta v2 acotada, sin aplicarla al motor.

La [matriz de objeciones, evidencia y pruebas](v4-patch-review/matrix.md) incluye JSON y CSV. [Propuesta v2](v4-review-corrections-v2.patch) · [verificación aislada por hashes](v4-patch-review/revision-validation.json) · [ADR de decisión](v4-patch-review/ADR-002.md). En copia nueva del candidato: 29 casos específicos, incluidos en 117 unitarias SEO; 13 integración y TLS real en loopback aprobados. No son pruebas contra RHINO ni sustituyen revisión independiente. El QA posterior a aplicación sigue pendiente: no se editó el motor.

La revisión del parche original recibió aportaciones reales de Claude y Codex, ambos con cambios solicitados. La revisión del artefacto v2 es independiente y su estado se conserva en la matriz antes de cualquier aplicación. No se cambia AGENTS.md, el tema ni producción, y el rastreo externo completo continúa sin autorización.

Fecha: 2026-11-11. Estado: candidato local con QA offline; revisión independiente del transporte pendiente. El tema y la tienda no se modificaron. El registro de proyectos, extractor, auditor por plantilla, validadores Schema, adaptadores Google, QA y navegador existentes siguen siendo la base.

**Actualización de la revisión concreta:** Claude pidió cambios y el worker Codex volvió a agotar inactividad. Se reprodujeron cinco defectos con pruebas nuevas: vista previa `none` confundida con noindex, selección de agente robots por subcadena, exclusiones críticas posteriores al truncado del log, sitemap pendiente al alcanzar max_urls y contenido editorial con la palabra comprar excluido como acción. El QA previo no cubría estos casos; su aprobación no elimina estos fallos conocidos. La revisión sigue `needs_evidence` y no permite aprobar el subsistema.

Se preparó [un parche revisable](v4-review-corrections.patch) y se probó en una copia temporal aislada de herramientas/tests, **sin aplicarlo al código del workspace**. Los cinco casos fallan antes y pasan con el candidato; la suite SEO de esa copia pasó (111 ejecuciones, incluye casos heredados repetidos). [Evidencia y hashes](v4-review-corrections-qa.json). Hace falta revisión humana o independiente completa antes de aplicar este parche y validar el transporte real; no se reintentará indefinidamente el worker. El parche no contiene operaciones remotas.

## Estado por fase

| Fase | Implementación local | Evidencia y límite |
|---|---|---|
| A — sitemap | `sitemaps.py`: urlset/index, XML acotado, duplicados y lastmod | Fixtures válidos, inválidos, DTD y entradas inseguras. El sitemap nativo no se reemplaza. Inventario real de RHINO pendiente. |
| B — crawler/grafo | `crawl_policy.py`, `robots.py`, `crawler.py`: BFS desde home, grafo, límites y exportaciones | Transporte inyectado probado. Sitemap-only es una comprobación aparte, no una ruta de navegación. Nuevo transporte real sin ejecutar contra RHINO por revisión pendiente. |
| C — indexabilidad/capas | `indexability.py`: estados técnicos, HTML inicial/DOM/no-JS y contenido principal | Chrome real en fixture y Home de RHINO. Sin robots real aportado no se aprueba indexabilidad. Esto no es Googlebot. |
| D — plantillas | Reutiliza `page_audit.py`, `extractor.py` y validadores; añade inventario por tipo | Home, categoría, producto, blog, artículo y página. Los datos declarados no certifican precio/autor/fecha reales; la consistencia comercial requiere facts autorizados. |
| E — Google | `coverage_import.py` y adaptadores existentes: CSV con mapping y exportaciones fechadas | Aislamiento por proyecto/propiedad probado. RHINO no tiene conexión autorizada disponible; ninguna consulta real a GSC ni OAuth. |
| F — gates | `regression.py`, CLI y pruebas integradas en QA existente | Canonical, noindex, robots, enlaces/href, H1, paginación, JSON-LD, errores comerciales y contenido sin JS. Evidencia ausente produce `insufficient_evidence`. |
| G — RHINO real | Navegador existente: Home a 390 px, rendered y no-JS | Validación selectiva, no auditoría de toda la tienda. Sin inventario completo, continuidad de categorías ni Google observado. |

## Ejecución portable

Seleccionar siempre un proyecto registrado. Las rutas locales de tema van en su override privado; no se transfieren permisos entre tiendas.

```bash
python3 tools/ia.py projects list
python3 tools/ia.py --project rhino-performance seo --help
python3 tools/ia.py --project rhino-performance seo sitemap --xml /ruta/sitemap.xml --source-url https://rhino-performance.com/sitemap.xml
python3 tools/ia.py --project rhino-performance seo crawl --responses /ruta/responses.json
python3 tools/ia.py --project rhino-performance seo readiness --capture /ruta/home-rendered.seo.json --no-js /ruta/home-no-js.seo.json --robots /ruta/robots.txt
python3 tools/ia.py --project rhino-performance seo enrich --crawl /ruta/report.json --capture /ruta/home-rendered.seo.json --no-js /ruta/home-no-js.seo.json
python3 tools/ia.py --project rhino-performance seo gate --before /ruta/antes.json --after /ruta/despues.json
```

El manifest offline contiene `project`, `home` y `responses`: un mapa URL → `{status, headers, body}`. Su reloj virtual no representa latencia de red. Capturas y evidencias deben pertenecer a la misma URL/proyecto y a anchos comparables. Las proyecciones iniciales pueden estar redactadas: no certifican sintaxis de scripts originales eliminados por la proyección.

Solo después de revisión obligatoria del subsistema y autorización de lectura del origen se podrá ejecutar `seo crawl --allow-network`. Parámetros predeterminados: 30 URLs comprobadas, profundidad 4, 60 solicitudes totales, 0,5 solicitudes/s, 120 s, timeout 10 s por solicitud, 2 MB por respuesta, 6 sitemaps, 2.000 entradas por sitemap, 2.000 URLs de descubrimiento, 10.000 aristas, 4 variantes por ruta, 5 redirects y concurrencia real 1. No se sigue ningún filtro ni ruta de paginación que no exista como href observado. Las exclusiones y los presupuestos se registran.

El transporte propuesto fija una IP pública validada, verifica TLS con SNI del host y usa un subproceso con deadline para DNS/conexión/cabeceras/cuerpo. Solo GET, mismo origen HTTPS, sin cookies, auth, proxy de entorno ni redirects automáticos. 403/429 y señales de desafío detienen el run. Robots desconocido impide el crawl. No se ejecuta JavaScript en este transporte. La detección conservadora de CAPTCHA puede detener páginas con widgets legítimos; requiere revisión, nunca evasión.

Google ya dispone de `seo connections`, `google-read` y `google-import`: conservar sus validaciones de cuenta/propiedad y acceso de lectura. El nuevo `coverage-import --csv ... --mapping ... --site-url ... --observed-at ...` requiere propiedad GSC configurada en el mismo proyecto. Mapping explícito de columnas `url`, `coverage_state` y, opcionalmente, `last_crawl`, `google_canonical`, `user_canonical`. Después se añade mediante `enrich --coverage-export ...`. No traduce un export parcial en inventario exhaustivo de indexación. No se enviaron sitemaps ni solicitudes de indexación.

## Cómo interpretar los resultados

Cada ejecución guarda JSON, resumen legible y procedencia con hashes. El crawl añade `urls.csv`, `sitemap.csv`, `edges.csv` y `backlog.csv`. Los CSV neutralizan fórmulas y el informe filtra secretos y áreas privadas.

`indexable_candidate` significa que las señales técnicas observadas permiten considerarla candidata. Indexación observada y canonical seleccionado por Google son campos distintos y necesitan datos autorizados de Google. Un HTTP 200 con canonical propio no demuestra indexación.

El número readiness representa cobertura de comprobaciones favorables. Los bloqueos críticos prevalecen; evidencia requerida desconocida impide aprobar. No es una puntuación de posicionamiento. Un sitemap con errores o un crawl que agotó límites queda parcial. Código de salida: 1 para gate bloqueado, 2 para evidencia insuficiente/parcial/detenida, 0 para procesamiento válido dentro del alcance. El crawl puede procesar correctamente errores HTTP observados; su salida 0 no significa que la tienda sea SEO correcta.

Los candidatos sin ruta desde home se distinguen de páginas realmente huérfanas. La duplicación se basa en texto principal extraído; no equivale a la selección de duplicados de Google. Soft 404 es una señal para investigar. `lastmod` es declaración del editor, no prueba de actualización ni factor de ranking certificado.

## RHINO: evidencia real y pendientes

Capturas: `reports/runs/rhino-performance/20261111T163623-seo-v4-home-browser-5567f98d/browser/`. Home, 390 px, con y sin JavaScript; 156 solicitudes bajo un presupuesto de 180 y 90 s. No hubo 403/429 ni errores de página JavaScript. Hubo dos fallos reales del QA: contraste en precio anterior del producto principal y cuatro imágenes esenciales no cargadas/transparentes sin JavaScript. No se aplicaron correcciones al tema en esta tarea.

La muestra de rendimiento no usó un perfil móvil de CPU/red limitado y no se presenta como benchmark comparable de PageSpeed ni INP de campo. No existe comparación antes/después del rendimiento de la tienda porque no se cambió el tema. Axe no equivale a certificación AA; Accessibility Tree explícito y teclado/responsive de categorías siguen pendientes.

El código actual de `snippets/product-list/pagination.tpl` conserva enlaces prev/next en modo clásico y un control sin href en la rama infinite scroll; `static/js/store.js` usa LS.hybridScroll. Esto es evidencia de fuente, no prueba de la configuración activa ni del contrato de filtros/cursor. No se modificó: continuidad, productos únicos, teclado y HTML inicial/no-JS de categorías y blog quedan `needs_evidence`.

El consejo inicial y la revisión de código posterior dejaron `needs_evidence`: Claude aportó propuesta/cambios solicitados, el worker Codex agotó inactividad y faltó deliberación completa. No existe consenso ni aprobación independiente. La autorización local del usuario permite preparar y probar el candidato offline; no elimina la revisión obligatoria del subsistema de red. Ninguna prueba de fixtures se presenta como observación de Google.

## Archivos, QA y reversión

Extensiones: `seo/cli.py`, `extractor.py`, `page_audit.py`, `engineering.py`; módulos nuevos: `sitemaps`, `crawl_policy`, `crawler`, `robots`, `indexability`, `regression`, `coverage_import`. El QA de navegador admite seleccionar modos `rendered`/`no-js` conservando su comportamiento predeterminado. Pruebas: `tests/unit/test_seo_*v4.py`, `tests/integration/test_seo_engineering_v4_cli.py`, `tests/browser/test_seo_engineering_v4.py`. El QA quick existente recoge unitarias/integración; no inicia crawls externos por commit.

No se instalaron dependencias ni se modificó catálogo, contenidos comerciales, cuentas o sitemap. No se ejecutó sincronización, publicación ni operaciones Git destructivas. La reversión debe limitarse al diff propio mediante hashes y respaldos del repositorio; no descartar cambios ajenos ni revertir commits del usuario.

Fuentes de contrato: [robots.txt de Google](https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec), [protocolo sitemap](https://www.sitemaps.org/protocol.html), [URL Inspection API](https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect). La inspección API informa la versión conocida por Google y no equivale a una prueba live.
