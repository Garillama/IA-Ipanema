# Revisión técnica del principal Codex — candidato de fuentes robots

Esta es la revisión del agente principal que preparó el candidato. No cuenta como revisión independiente, voto adicional ni sustitución del participante Codex del consejo. El consejo nuevo conserva su propia identidad y recibos.

## Comprobaciones observables

- Antes del parser, el transporte y el extractor preservan listas. La concatenación previa del helper era el punto que perdía los límites. No se modifica el transporte ni se inventan fuentes recuperadas de una cadena heredada.
- Cada meta robots/googlebot y cada X-Robots-Tag recibe un análisis independiente. La memoria de comillas y el agente activo se reinician por cabecera física. La agregación posterior une flags/errores, no texto sin interpretar.
- classify consume `google_directive_evidence`. La prioridad es noindex válido → errores relevantes/desconocido → evaluación restante. index/all no eliminan restricciones ni convierten errores en un permiso.
- audit_snapshot conserva evidencia tipada y distingue ausencia de restricción de evidencia insuficiente. El fallback del gate usa esa evidencia; un reporte heredado cuyo texto ya perdió sus límites no recibe una interpretación nueva por subcadena.
- Las fuentes se identifican por tipo, nombre, ordinal y hash UTF-8 del valor extraído. Los offsets de errores son relativos al texto seleccionado de esa fuente, no posiciones de la respuesta HTTP. No se duplica el contenido completo en el registro nuevo.
- Los valores con parámetros no producen flags a partir de sus palabras. Comillas no cerradas producen error relevante en fuentes aplicables y no cruzan a la siguiente fuente. Una restricción válida de otra fuente conserva noindex aunque existan errores adicionales.
- Se mantienen clasificación técnica frente a indexación observada, robots.txt como control independiente, presupuestos y protección de red actuales.

## Evidencia ejecutada

`before-source-boundaries.json` reproduce los dos falsos negativos exactos del bloqueo sobre el candidato anterior, verificado por hashes. `after-source-specific.json`, `after-source-seo-unit.json`, `after-source-seo-integration.json`, `after-source-local-tls.json` y `candidate-qa-report.json` contienen resultados posteriores. Los ejemplos tipados están en `source-evidence-examples.json`.

76 pruebas específicas incluidas en 160 unitarias SEO, 13 integración, TLS local y suite SEO aprobados. La regresión de tokens add-to-cart incrustados también se reproduce/cubre mediante exclusiones, sin conceder acceso a una ruta comercial real ni ejecutar el storefront.

La primera ejecución aislada se conserva en attempt1-bytecode-cache y no fue aceptada. La repetición usa procesos y copia nuevos y no escribe bytecode; no se cambiaron expectativas para hacer pasar el resultado.

## Límites y veredicto acotado

La política de errores de directivas malformadas es conservadora; no se presenta como prueba de recuperación por Google. Googlebot-News no se evalúa como Googlebot de texto. La política anterior de robots.txt ante agentes inválidos puede detener el crawl entero; se conserva como riesgo de compatibilidad sujeto a revisión, no se debilita para obtener aprobación. Se conservan exclusiones conservadoras de IP traducida.

El defecto entre fuentes está corregido en los casos ejecutados y el artefacto único coincide con el árbol probado. Esto no aprueba por sí solo la aplicación: faltan el resultado de revisión independiente del diff completo y sus condiciones obligatorias. No se modifica el workspace, el tema, AGENTS.md ni producción, y no se ejecuta rastreo externo.
