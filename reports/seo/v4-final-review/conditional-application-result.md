# Resultado de autorización condicionada — parche V4 final

**No aplicado. Condiciones obligatorias incumplidas.** Cero aplicaciones al workspace; no se modifica el parche ni se propone otro hash dentro de esta autorización.

SHA-256 comprobado: `4369d84d3a84bd99808d92eb12ad13bcf185f300615817bb6eedd517412acc6f`.

## Comprobaciones previas

| Condición | Estado | Evidencia |
|---|---|---|
| 1. SHA-256 exacto | passed | 4369d84d3a84bd99808d92eb12ad13bcf185f300615817bb6eedd517412acc6f |
| 2. Cinco hashes base y dos archivos ausentes | passed | manifest.json; final_base_hashes; no source drift |
| 3. Diff completo sin archivos adicionales | passed | seven declared files; strict zero-fuzz dry-run; isolated output matches candidate hashes |
| 4. Objeciones críticas y condiciones obligatorias | failed | cross-source noindex false negatives; review needs_evidence |
| 5. AGENTS sin cambios y seguridad | failed_partial | AGENTS unchanged/not targeted; security acceptance fails on review counterexamples |
| 6. Respaldo íntegro del alcance | passed | .local/backups/seo-v4-final-preflight-20261111T174750Z.tar.gz |
| Política permite esta excepción humana | not_satisfied | AGENTS requires independent review; current authorization explicitly preserves it |
| Aplicación única | not_executed | 0 workspace applications; no rollback needed |
| QA posterior en workspace | not_executed | no integration performed; prior 134 unit/13 integration/specific/TLS results belong to isolated candidate |
| Preservación ajena | passed | 1058 files checked, zero differences |

## Resultado de revisión independiente

[ADR real](../../runs/rhino-performance/20261111T174614-orchestration-f2e607f8/council/adr.json) · [Datos completos](conditional-preflight.json). Claude revisó el parche final y no lo aprobó. Codex no completó su participación por inactividad; el circuito se abrió tras dos fallos y no se repitió el proceso. Consejo: `needs_evidence`, `implementation_allowed: false`. No se afirma consenso dual.

La autorización humana recibida es condicionada y expresamente no sustituye la revisión independiente. AGENTS.md exige: «El QA posterior y la revisión independiente siguen siendo obligatorios» y «Objeciones críticas y condiciones obligatorias pendientes impiden implementar». La política vigente no define una excepción que cierre automáticamente estas condiciones con esta autorización. No se alteró AGENTS.md ni se debilitó el controlador.

## Defecto crítico confirmado en candidato exacto

| Fuente 1 | Fuente 2 | Resultado necesario | Resultado del candidato |
|---|---|---|
| Meta `foo="x` sin cierre | X-Robots-Tag `noindex` | noindex | indexable_candidate |
| X-Robots-Tag `foo="x` sin cierre | Otra cabecera `noindex` | noindex | indexable_candidate |

Ambos fallos fueron reproducidos por el agente principal en la copia cuyos siete hashes coinciden con el manifiesto. La causa es la concatenación de fuentes independientes antes del parser: una comilla abierta consume también las directivas de la fuente siguiente. El control con noindex independiente válido pasa. [Casos y resultados](conditional-review-counterexamples.json). Ningún caso hizo solicitudes de red.

La revisión también señala dos asuntos: tokens de acción a mitad de segmento ahora admitidos (por ejemplo `/producto-add-to-cart`) y que un agente ajeno fuera de la gramática invalide todo robots.txt. El primero reproduce una diferencia de exclusión respecto de la base; no se probó que las rutas sean endpoints comerciales reales. El segundo es el comportamiento conservador documentado, pendiente de aceptación de compatibilidad. No se disfrazan como validaciones de una tienda.

Las suites anteriores aprobadas no cubrían el fallo entre fuentes. Por ello no bastan para aceptar el artefacto. Se necesita corregir la separación de fuentes y cerrar las observaciones con un nuevo resultado revisable; esta autorización del hash exacto no autoriza cambiarlo silenciosamente ni aplicar una variante.

## Respaldo, preservación y pruebas pendientes

Respaldo privado verificado: `.local/backups/seo-v4-final-preflight-20261111T174750Z.tar.gz`. SHA-256 `00d7772e52701aa840534a779e61bfcba2226f6629f3f89d3371a9345b501e5b`. Contiene los cinco archivos completos con permisos, marcadores de ausencia de las dos pruebas nuevas y copia exacta de parche/manifiesto/política. Ignorado por Git, modo 0600. No se extrajo sobre el workspace.

Se compararon 1058 archivos ajenos al parche: ninguna diferencia. Los cinco hashes base, las dos ausencias y AGENTS.md siguen intactos. No se inició attempt apply y no hace falta reversión porque hubo cero aplicaciones.

Las 134 pruebas unitarias SEO, 13 de integración, 50 específicas y TLS/suite SEO de la preparación siguen siendo evidencia del candidato aislado anterior. No se presentan como QA posterior a integración. El QA posterior en el workspace, la revisión independiente aprobada y cualquier validación real de RHINO siguen pendientes. No se ejecutaron rastreos externos, formularios, cambios de catálogo, operaciones de producción ni comandos de sincronización. Tampoco se modificaron temas de RHINO o DaMar.

La integración se detiene conforme a la condición del usuario: si alguna condición no se cumple, no aplicar.
