# ADR-RHINO-004 — prioridad de rendimiento tras push

Fecha: 2026-11-10T21:16:22.548199+00:00. Proyecto rhino-performance. Estado: **needs_evidence para implementación**.

Se actualiza el diagnóstico de ADR-002 con15muestras Lighthouse normales y3contrafactuales. No sustituye ADR-003 de accesibilidad ni lo amplía como permiso para optimizar producción.

Decisión de investigación: primer recurso del blog, coste de JS compartido y estabilidad del video desktop. Se conserva Ipanema, sus helpers y contratos. Descartados: desactivar marketing como solución automática (TBT mejora pero LCP empeora), otro preload de hero ya prioritario, eliminar CSS/LS por Coverage, equiparar PSI/local/campo y atribuir origenCrUX a URLs sin cobertura.

Codex reunió mediciones/prueba y formuló las propuestas; la evaluación independiente disponible de Claude se conserva en el [informe](postpush-performance.md). No se repitió una deliberación completa ni se declara consenso formal de implementación. El beneficio del contrafactual no autoriza retirar analítica.

Antes de implementar: comprobar mecanismo/scope y fuente propietaria, ensayar cambio mínimo local en entorno renderizable, QA de eventos/SEO/accesibilidad/commerce autorizado y comparar muestras compatibles con tolerancias. Se preservan restricciones de publicación y datos de clientes. No se activó scheduling ni gates automáticos.
