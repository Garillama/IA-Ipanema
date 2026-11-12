# RHINO Performance — auditorías

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
