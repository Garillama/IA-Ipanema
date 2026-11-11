# RHINO Performance — auditorías

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

- [Primer lote JS de Home: pruebas completas, aplicación pendiente](home-js-first-batch.md) · [ADR-RHINO-007](ADR-RHINO-007.md).
