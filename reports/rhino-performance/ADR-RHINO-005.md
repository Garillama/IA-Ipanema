# ADR-RHINO-005 — prioridad contextual de portada del blog

Fecha: 2026-11-10T21:38:30.704861+00:00. Proyecto rhino-performance. **approved_with_conditions para candidato local; liberación bloqueada hasta render/QA posterior.**

Se reabre solo RHP-01 de ADR-004 tras la autorización de implementación local del propietario. Las demás propuestas siguen pendientes de evidencia.

Claude y Codex seleccionaron codex-blog-priority en propuesta/contraste/defensa. Se descartó mover fuentes sin beneficio demostrado sobre el preload actual y desactivar marketing porque mejoró TBT pero empeoró LCP. Video/CLS conserva su hipótesis sin cambiar reproducción.

Las condiciones altas de visibilidad de fade-in, primera sección actual, fragmentos y consumidores fueron verificadas por el controlador antes de aplicar:35checks estáticos,138de navegador local. Se encontró el cuarto consumidor home-news y se añadió false explícito; la revisión independiente evaluó ese alcance completo de5archivos. La disponibilidad general de params GET está documentada oficialmente, pero no se confunde con un render Twig ejecutado en este entorno.

Decisión: reutilizar image_priority_high en el helper, parámetro opcional defaultfalse en blog-card, condición normal/primera con imagen y exclusiones de fragments/tag, false explícito en los otros tres consumidores. No alterar imagen original, CSS, JS, fuentes, marketing, comercio ni templates JSON. [Implementación, archivos, pruebas y límites](performance-fixes.md).

Beneficio probado: descubrimiento/prioridad/visibilidad sin JS en fixture fuente-vinculada. Beneficio de LCP de tienda: no medido. Riesgos aceptados para conservar localmente: composición futura, filtros/editor/render del backend y tamaño de la imagen que sigue alto. Esos riesgos bloquean aprobación de publicación, no se resuelven por mayoría ni por el score.

El implementador es Codex; Claude revisó independientemente con decisión approve y el controlador verificó diff/hashes/QA. La autorización local del propietario no autoriza push, watch, publish ni cambios CMS. Reversión mediante transacción propia con backups y conflicto de hash protegido.
