# ADR SEO V4 001 — Rastreo y evidencia de indexabilidad

Estado: candidato local con QA offline; revisión independiente obligatoria pendiente. Ejecución local autorizada por el propietario. No es aprobación de producción ni de Google.

## Objetivo y fuentes

Evolucionar el motor existente sin sustituir extractor, validación Schema, QA de navegador, registro de proyectos ni adaptadores Google. Fuentes actuales: `tools/ipanema/seo/{cli,reports,page_audit,extractor,adapters}.py`, `tools/qa_browser.mjs`, `tools/page_collectors.mjs`. El tema es externo y no se modifica en estas fases.

## Alternativas y refutación

1. Añadir un framework de scraping: duplica infraestructura y dependencias; descartado mientras stdlib y navegador preparado cubran el alcance.
2. Rastrear con navegador cada URL: reproduce más comportamiento, pero ejecuta terceros, cuesta más y aumenta superficie de operaciones. Se mantiene como captura selectiva mediante el QA existente, no descubrimiento predeterminado.
3. Extender SEO con parsers offline, transporte GET acotado y BFS desde home: elegido para implementación local incremental, sujeto a pruebas y revisión independiente. Los informes reutilizan el auditor existente y conservan evidencia faltante como desconocida.

## Contratos y seguridad

- Biblioteca estándar. Transporte inyectable para fixtures; transporte real sin cookies, autenticación, proxy de entorno ni redirects automáticos. Solo HTTPS y origen registrado, DNS público comprobado, redirects validados antes de seguir, límites de bytes/tiempo/requests/rate/profundidad/URLs. Concurrencia inicial 1 explícita; no prometer paralelismo no implementado.
- Red deshabilitada sin `--allow-network`. Robots respetado por defecto; errores o reglas desconocidas impiden candidatos. 403/429 y señales CAPTCHA detienen el run entero sin retries. No cuenta/carrito/checkout/login, variantes de acciones, parámetros secretos, búsquedas/filtros/ordenamientos salvo contrato de consulta expresamente permitido.
- El sitemap no se reemplaza. XML sin DTD/entidades; límites de documentos/entradas/profundidad, soporte urlset/index, provenance y errores. Las URLs de sitemap no se usan como semillas de navegación: se distingue cobertura de enlaces de chequeos de sitemap.
- Ningún reporte conserva HTML ejecutable completo, cookies, credenciales, scripts arbitrarios ni valores de formularios. Proyecciones estructurales acotadas y hashes; enlaces confidenciales se rechazan antes de persistir. CSV protege fórmulas.
- Las fechas lastmod son datos declarados, no certificación. Soft404 y duplicación son candidatos; evidencia desconocida no es cero ni ausencia demostrada.
- Clasificación por HTTP/robots/directivas/canonical sin afirmar indexación. Google se incorpora únicamente mediante adapters/exports del mismo proyecto y propiedad; no OAuth ni escritura.
- Readiness usa predicados con cobertura, bloqueos críticos y aprobación separada del número. El gate requiere evidencias comparables y no aprueba una regresión por promedio.

## Fases y archivos previstos

A: `seo/sitemaps.py`, fixtures/unitarias de XML. B: `seo/crawl_policy.py`, `seo/crawler.py`, pruebas de transporte y BFS. C–D: `seo/indexability.py`, integración con extractor/auditor actual y evidencia HTML/DOM/noJS. E: reutilizar `seo/adapters.py` e imports con aislamiento de propiedades. F: `seo/regression.py`, CLI y suite SEO existente. G: auditoría RHINO autorizada de lectura, máximo 30 URLs, profundidad 4, 0,5 solicitudes/s, 120s, 6 sitemaps; parar ante restricciones. Exportación JSON/CSV con fecha, límites y errores.

## QA y condiciones

Unitarias XML válido/inválido/DTD/index/duplicados, HTTP y redirects, URLs privadas/secretas/SSRF, loops/parámetros/rate/bytes/tiempo, robots/403/429/CAPTCHA; fixtures de enlaces y paginación, JS/noJS, Product/Article y regresiones. Transporte mock no es prueba de Google. Fixture local HTTP solo mediante inyección de transporte, sin debilitar el cliente real. QA quick/SEO del repositorio y navegador selectivo preparado, sin crawls remotos en CI. Ningún código de ejecución de modelos se convierte en comando del controlador.

## Pendientes de evidencia

Contratos reales de LS.hybridScroll/cursor/filtros y continuidad de páginas: needs_evidence hasta observar HTML, estados sin JS y eventos en el tema correcto. No inventar page= ni modificar paginación. Search Console de RHINO debe verificarse separada de DaMar. Un crawl parcial no demuestra orfandad ni exhaustividad. Revisión independiente real requerida para aprobar el subsistema de red; si falta Claude, continuar parsers y QA offline y conservar esa aprobación pendiente sin simular consejo.

## Reversión

Cambios solo de workspace y archivos declarados. Preservar diffs ajenos existentes. Nuevos módulos aislados y extensiones CLI compatibles; rollback del intento propio por hashes, nunca reset/clean/stash. Producción, catálogo y configuración de cuentas quedan fuera del alcance.

## Evidencia posterior y objeciones recibidas

Consejo real inicial: `reports/runs/rhino-performance/20261111T155340-orchestration-3e864e6d/council/adr.json`. Claude entregó propuesta; worker Codex agotó inactividad. Estado `needs_evidence`, sin consenso ni autorización independiente del transporte. No se sustituyó un participante por una revisión simulada. El candidato se preparó y probó offline; el nuevo cliente HTTP no se ejecutó contra RHINO.

Objeciones de Claude incorporadas al candidato, aún sujetas a revisión posterior:

- La biblioteca robotparser no basta para reglas wildcard/$/precedencia: parser específico acotado, agentes separados y desconocidos fail-closed, con fixtures.
- Proxies de entorno y redirects automáticos amplían el límite de confianza: cliente GET sin ambos; validación de cada destino.
- DNS público sin fijar la conexión permite rebinding: IP pública validada y fijada a socket; TLS/SNI conserva el hostname.
- URLs confidenciales pueden filtrarse en reportes: filtrado antes de persistir, rutas privadas decodificadas y exportación redactada.
- X-Robots-Tag repetido y directivas por agente no deben aplanarse: lista de cabeceras con alcance conservado; `otherbot: noindex` no bloquea Googlebot.

QA final del candidato: 88 unitarias SEO, 13 integración SEO y una prueba Chrome real local pasadas. QA quick: `reports/runs/rhino-performance/20261111T164613-quick-0c345fd0/report.json`, seis controles aprobados. No se interpreta como revisión independiente ni certificación de la tienda.

Observación real separada mediante navegador existente: Home 390 px rendered/no-JS, 156 solicitudes bajo límite 180 y 90 s, sin 403/429 ni errores JavaScript. QA con dos fallos de storefront: contraste de precio anterior y cuatro imágenes sin carga útil sin JS. Readiness actualizado: `reports/runs/rhino-performance/20261111T164716-seo-v4-readiness-47b2e02b/report.json`, `insufficient_evidence` por robots no aportado. Fuente de paginación inspeccionada, pero continuidad/filtros/cursor reales `needs_evidence`; sin parche del tema.

Implementación, límites por fase y comandos: [v4-engineering.md](v4-engineering.md). Fuentes: [robots Google](https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec), [sitemap](https://www.sitemaps.org/protocol.html), [URL Inspection](https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect).

## Revisión concreta del código: cambios solicitados

`reports/runs/rhino-performance/20261111T164534-orchestration-aa9b603e/council/adr.json`: Claude `changes_requested`, Codex worker `unavailable/inactivity`; sin defensa ni acuerdo completo. `implementation_allowed: false`. No se sigue intentando al worker ni se rebajan controles.

Se reprodujeron cinco defectos en pruebas adicionales: `max-image-preview:none` como falso noindex; matching de grupos robots por subcadena; motivos críticos perdidos al truncar el log; URLs de sitemap sin verificar al alcanzar max_urls; regex de acciones que excluye contenido editorial con comprar. No se acepta el subsistema basándose en los tests anteriores.

Alternativa elegida para revisión humana: mantener arquitectura y proponer corrección acotada de tokenización de directivas, igualdad del product token robots, contadores por motivo independientes del log, completitud con sitemap pendiente y rutas de acción ancladas. Alternativa rechazada: aprobar el transporte porque los tests anteriores pasan, o relajar las exclusiones para conseguir mayor cobertura sin fixtures negativos.

Se entrega `v4-review-corrections.patch`, probado en copia temporal aislada: cinco casos nuevos fallan en la fuente actual y pasan con el parche; suite SEO de la copia aprobada. No se aplicó el parche al workspace ni se ejecutó el nuevo crawler remoto. Evidencia con hashes y salidas: `v4-review-corrections-qa.json`. Revisión humana/independiente pendiente de este resultado concreto; la prohibición de implementar con objeciones críticas pendientes se conserva. Gate sin máscaras dinámicas sigue conservador y requiere allowlist explícita de eliminaciones; no se autoaprueba rotación de productos.
