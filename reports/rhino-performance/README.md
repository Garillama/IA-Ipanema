# RHINO Performance — auditorías

## Cierre de condiciones V4 — sin rastreo nuevo

[Actualización incremental](indexability-20261112/site-continuation/coverage-closure/README.md): QA del controlador del parche final aprobado en aislamiento, 183 pruebas. Motor sin integrar y consejo aún incompleto por inactividad de Codex; no se convierten condiciones pendientes en aprobación. Las 75 URLs conservan su estado pendiente, con procedimiento seguro y diff exacto preparados. GSC sin credencial disponible y catálogo administrativo pendiente de conciliación manual. Ninguna modificación del tema o producción.

## Rastreabilidad de la estructura existente — continuación

[Informe y matriz URL por URL](indexability-20261112/site-continuation/README.md): 125 URLs principales conocidas; caminos HTML observados hacia 122 de 124 páginas HTML. Cinco categorías 200/canonical propio/H1 y enlaces sin JS; ocho páginas del blog cubren los 86 artículos del sitemap. HTTP individual pendiente para 11 productos y 64 artículos; crawler V4 bloqueado, GSC histórico reutilizado sin inventar cobertura total. Sin modificaciones de tema o producción. Menús suspendidos y Sobre Rhino pendiente de contenido, sin promoción.

## Paginación publicada — validación real

[Publicación autorizada y resultados](indexability-20261112/three-issues/operations/publication/resultados-produccion.md): una sola subida, dos archivos exactos, cero eliminaciones; hashes corroborados por lote nativo y JavaScript del CDN. Carga real 12→14 sin duplicados, enlaces HTML, sin JavaScript, teclado, seis anchos y smoke de consumidores. Cinco Lighthouse por dispositivo: mediana 65→65 móvil y 87→88 escritorio, con advertencia de LCP móvil. Claude aprobó el alcance probado; no se detectó regresión crítica atribuible ni se ejecutó reversión. Overflow y discrepancia de lectura individual registrados, sin atribuir causa. Menú/blog intactos.

## Paginación — paquete definitivo, sin publicar

[Autorización específica preparada](indexability-20261112/three-issues/operations/publication/README.md): instalación publicada y hashes originales reconfirmados, nuevo respaldo remoto de dos archivos, diff reproducido contra ese respaldo, cinco muestras locales por dispositivo y revisión final independiente de Claude. Código listo para solicitar autorización; QA publicado y aceptación final pendientes. Menú pendiente del respaldo administrativo; consulta de blog aún sin enviar.

## Operaciones preparadas — menú manual y validación nativa

[Procedimientos, candidato y controles](indexability-20261112/three-issues/operations/README.md). Menú: vía manual oficial, respaldo administrativo aún pendiente, sin endpoints privados. Paginación: v2 preservado, foco y guarda de cursores corregidos en candidato separado; pruebas con LS publicado en seis anchos y validación nativa `theme check` aprobada para dos archivos exactos, sin guardarlos. Consulta a Tiendanube preparada, no enviada. Propuesta revisable; ejecución/aceptación pendientes de autorización y QA real. Producción y tema sin modificar.

## Tres pendientes concretos — defensa recuperada y candidatos

[Cierre acotado](indexability-20261112/three-issues/README.md) · [Diff v2 sin aplicar](indexability-20261112/three-issues/pagination-v2-candidate.patch). Recuperada solo la defensa Codex, mismo contexto y originales preservados; deliberación completa, ADR aún needs_evidence. Paginación: candidato con botón nativo/enlaces separados, 48 checks aislados, revisión Claude solicita cambios/evidencia. Blog3/8 comprobados sin repetir página2; Contacto/Sobre sin href desde home, propuesta de añadirlos al menúfooter. Respaldos remotos y398archivos en sincronía; cero modificaciones de producción o tema en esta fase.

## Search Console y revisión dual — 12 noviembre, seguimiento

[Resultados reales y límites del consejo](indexability-20261112/google-followup.md) · [Matriz actualizada](indexability-20261112/url-matrix-gsc.csv). 13 inspecciones: 10 enviadas e indexadas, Contacto descubierta sin indexar y dos URLs desconocidas. 170 filas de rendimiento, sin interpretarlas como total indexado. Ruta nativa `/productos/page/2/` verificada: 12→14 productos sin duplicados en scroll y HTML completo 200. Consejo incompleto por presupuesto agotado antes de defensa Codex; sin aprobación de implementación ni cambios al tema/producción.

## Indexación y rastreabilidad — 12 noviembre UTC

[Informe y límites](indexability-20261112/README.md) · [Matriz de 117 URLs](indexability-20261112/url-matrix.csv) · [ADR-011](ADR-RHINO-011.md). Solo Codex, sin cambios al tema: 14 productos, 5 categorías y 86 artículos en los sitemaps. Grafo parcial de HTML: 52 rutas con camino observado; no certifica orfandad del resto. Catálogo sin href de carga posterior y canonical de blog página 2 hacia portada reproducidos. Crawler V4 no aprobado/integrado; GSC sin sesión activa, consentimiento expiró sin consulta. Auditoría completa pendiente, no se afirma indexación.

## Breadcrumb de artículos — corrección publicada autorizada

[Resultado y pendientes](breadcrumb-production-fix.md). Solo layout.tpl en14828608:20 artículos verificados con enlace Blog absoluto; dos URLs pendientes. Home y cambios ajenos preservados. Google todavía no validado.


## Peso y rendimiento habitual de producción — 12 noviembre UTC

[Informe](production-weight-20261112/README.md) · [PDF](production-weight-20261112/informe.pdf) · [Mediciones por ejecución](production-weight-20261112/measurements.csv) · [ADR-010](ADR-RHINO-010.md). Solo Codex; estadísticas recalculadas de130 respuestas/129 mediciones únicas. Home:2,803MB móvil y10,716MB desktop contabilizados por PSI, con cautela explícita sobre caché e histórico. Candidatos de video preparados sin publicar; tema intacto.


## Comparativa por página — corrección del alcance

[PDF antes/ahora de siete vistas](comparativa-por-pagina-20261111/informe.pdf) · [Datos y procedencia](comparativa-por-pagina-20261111/resultados.json). Reutiliza Home y añade seis consultas PSI móviles actuales. El PDF original no identifica las URLs: se comparan representantes del mismo tipo, sin afirmar identidad ni causalidad. Incluye qué se modificó y qué no, con el estado de las pruebas.


## PageSpeed — lote de diez consultas, 11 noviembre 2026

[PDF de 22 páginas](pagespeed-ten-20261111/informe.pdf) · [Resultados y metodología](pagespeed-ten-20261111/README.md). Máximos móvil/escritorio: 86/96; medianas de mediciones únicas: 71/77. Diez consultas, nueve mediciones únicas: Google repitió una respuesta de escritorio. Sin cambios en la tienda.


## Cierre del lote del header — 11 noviembre 2026

[Resultado y evidencia](adr009-followup.md) · [diff aplicado localmente](header-initial-flow-v2.patch). Header v2 aceptado con revisión Claude/Codex; CLS de escritorio controlado 0,06815 → 0,00143. Marketing sin modificar, objetivo 90+ pendiente. Las secciones siguientes conservan el historial de fases anteriores.


## Última auditoría — 11 noviembre 2026

[32 mediciones nuevas y diagnóstico móvil/escritorio](performance-renewal-20261111.md) · [ADR-009](ADR-RHINO-009.md) · [Baseline5 muestras](performance-baseline-20261111.json). Home:64 móvil/87 escritorio; candidato de header sin aplicar y prioridad en CPU de tags. No se alcanzó90+ ni se modificó el tema en esta fase.


Proyecto `rhino-performance`, https://rhino-performance.com/. Referencia pública de assets14828608; no es DaMar.

- [Informe integral](integral-audit.md): alcance, mediciones, causas/hipótesis y limitaciones.
- [ADR técnico](ADR-RHINO-002.md): needs_evidence para implementación; no autoriza producción.
- [Backlog priorizado](integral-backlog.json).
- [Evidencias y perfiles](integral-evidence.json).
- [Baseline](performance-baseline.json) y [política de gates](regression-gates.json): política propuesta, hook no activo.
- [Consejo real Claude/Codex](integral-council.json): propuestas, objeciones, respuestas y revisiones incrementales.
- [Auditoría de accesibilidad anterior](accessibility-audit.json), conservada como referencia fechada.

No se modificaron archivos del tema ni producción. La implementación queda pendiente de revisión del diagnóstico y autorización del alcance. Capturas y originales extensos se conservan localmente en reports/runs/rhino-performance, ignorado por Git. No se guardaron API Keys en estos informes ni se programaron consultas externas.

## Correcciones locales de accesibilidad

[Implementación y QA parcial](accessibility-fixes.md) · [ADR-003](ADR-RHINO-003.md). Aplicadas localmente tras autorización; sin publicación ni validación completa de Tiendanube.

## Diagnóstico publicado actualizado

[Rendimiento tras push](postpush-performance.md) · [Accesibilidad complementaria](postpush-accessibility.md) · [ADR-004](ADR-RHINO-004.md). Solo lectura; sin nuevos cambios de tema.

## Implementación local de rendimiento

[Primer parche local de rendimiento](performance-fixes.md) · [ADR-005](ADR-RHINO-005.md). Carga inicial del blog corregida con helper nativo; sin publicación ni nuevo LCP de tienda comprobado.

## Validación tras el push del propietario

[Prueba publicada del parche del blog](blog-release-validation.md) — LCP móvil13.26→6.19s en muestras locales comparables; rendimiento móvil aún pendiente de más mejoras.

- [Home: rendimiento y estabilidad, diagnóstico actual](home-performance-strategy.md) · [ADR-RHINO-006](ADR-RHINO-006.md) · [Backlog Home](home-performance-backlog.json).

- [Primer lote JS de Home: aplicado y aceptado localmente](home-js-first-batch.md) · [ADR-RHINO-007](ADR-RHINO-007.md).

- [Sectionfy: carrusel/banner con fotos y video — aplicado localmente, configuración pendiente](sectionfy-hero-media.md).

- [Sectionfy automático en Home: aplicado localmente, API y archivo real verificados](sectionfy-automatic-home.md).
