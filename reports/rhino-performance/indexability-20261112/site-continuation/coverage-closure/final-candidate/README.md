# V4 — candidato final para autorización de integración local

12 noviembre 2026. Continuación incremental del mismo consejo. **Los tres problemas técnicos quedaron resueltos para el alcance probado.** Claude y Codex aprobaron el diff exacto; el controlador verificó pruebas, aplicación, hashes y recibos. No se integró el motor ni se ejecutó red sobre Rhino.

## Decisión

[ADR actualizado](ADR.json): **approved_with_conditions**, ready_to_request_integration=true, sin bloqueos técnicos abiertos dentro de este delta. `implementation_allowed=false` hasta recibir autorización específica del propietario para este hash nuevo. Puede cambiar legítimamente tras esa autorización y la comprobación final de preimágenes, no por el mero resultado de los tests. El checkpoint histórico del hash anterior no se sobrescribe ni se usa para ejecutar el nuevo.

Parche anterior conservado: `7a5a7066bb22d2f87c18286100a9fba0ce76e50e53a8cf9b211821d0eba8b4a0`.

**Nuevo parche completo SHA256:** `611a5dac1e2767c0d331e42b06c60834e8a427c8bbc41671b9a81a8c977f3e2c`.

[Diff completo](candidate-v4-final.patch) · [delta exclusivo respecto al candidato anterior](delta-from-7a5a7066.patch) · [11 archivos y hashes antes/después](manifest.json).

Hay **7 modificaciones y 4 altas, ninguna eliminación**. Los nueve archivos del parche previo siguen en el paquete; se añade el test nuevo y se actualiza una fixture de regresión existente. Respecto al candidato anterior solo cambian robots.py, regression.py y esos dos archivos de pruebas. No cambian transporte, DNS, TLS, rutas privadas, redirecciones, presupuestos del crawler o su criterio de cobertura completa.

## 1. Gate corregido

`_nodes` conserva el estado global como observación técnica, sin convertir robots limpio en indexada. `_robots_state` evalúa por separado la estructura de directivas. `compare` utiliza esa señal únicamente en :noindex.

| Evidencia | Resultado del control :noindex |
|---|---|
| Limpia y completa en ambos lados | passed, solo para ese control |
| Ausente, heredada, estructura malformada o análisis incompleto sin restricción válida | unknown |
| Nueva restricción válida desde baseline limpio o desconocido | failed |
| Noindex válido observado y otra fuente incompleta | sigue restrictivo; no se neutraliza |
| Noindex válido ya presente en ambos lados | no es una nueva regresión |
| Incertidumbre por contenido, canonical o índice real | permanece en su ámbito; no se interpreta como robots restrictivo |

La fixture histórica que esperaba passed ahora aporta evidencia tipada limpia, en vez de declarar ese aprobado desde una simple cadena. La prueba de aparición de noindex aporta evidencia tipada restrictiva. No se borraron ni debilitaron sus asserts; se añadieron casos separados que exigen unknown para el legado.

## 2. Evidencia acotada sin perder semántica

Las muestras se acotan durante el parsing, sin construir primero listas enormes. Los flags/noindex, la existencia de errores, los tipos de error gramatical y los contadores se acumulan sobre todos los átomos admitidos. Una restricción al final de 200.000 parámetros conserva noindex=true.

- Procesamiento: 2.000.000 bytes UTF-8 por fuente;4.000.000 bytes sumados;128 fuentes físicas.
- Retención:8 muestras por lista;96 caracteres por campo textual;16 fuentes retenidas;65.536 bytes máximos del objeto JSON.
- `truncated` indica muestras resumidas; no significa que se haya omitido evaluación semántica dentro del presupuesto.
- `processing_complete=false` declara un análisis incompleto y evita un aprobado falso. Una fuente demasiado grande se rechaza entera: no se presenta su prefijo como completo.
- Se conservan hashes de fuentes retenidas, offsets, hash de colección procesada y contadores. Fuentes no visitadas tienen recuento desconocido, no cero inventado. Hace falta la captura original para reproducir contenido real; un hash no lo reconstruye. Las entradas sintéticas sí están conservadas.

Se mantiene la duplicación del objeto entre indexability/template_audit por compatibilidad de informe; ambas copias están acotadas. No se promete una eliminación total de duplicaciones.

| Reproducción sintética, misma entrada de 1.599.999 bytes | Anterior | Candidato final |
|---|---:|---:|
| JSON con las dos ubicaciones | 32,000,962 bytes | 3,266 bytes |
| Pico Python trazado | 80,713,291 bytes | 1,650,392 bytes |
| Parsing con tracemalloc | 8.741 s | 3.491 s |
| Parámetros procesados | 200.000 | 200.000 |

Una muestra por versión, no benchmark estadístico ni métrica de tienda. El descenso de tamaño es una diferencia determinista del informe; los tiempos no garantizan aceleración en cualquier entrada o entorno. [Medición final](evidence-final.json).

Durante el borrador, un error de comillas tras superar la muestra podía perder su efecto de incertidumbre. Se reprodujo antes de corregirlo ([entrada y resultado anterior](late-header-grammar-before.json)); el agregado de tipos de error lo corrige y una prueba específica evita que reaparezca. Los fallos intermedios de contador/fixtures también se conservaron en el run; nunca se integraron.

## 3. Compatibilidad del helper

`google_directives` recupera el cuerpo histórico exacto, con parámetros, múltiples cabeceras, scopes, wildcard y detalles de comas. El controlador comprobó igualdad de AST excluyendo solo el docstring, además de cinco fixtures exactos y los tests anteriores. Es un **adaptador de texto**, no un parser seguro para decisiones ni un serializador acotado.

Las decisiones de classify, audit_snapshot y compare no importan ni leen ese helper; emplean evidencia tipada. El controlador verificó referencias/importaciones y ejecutó audit_snapshot y compare con el adaptador configurado para lanzar una excepción si se invoca: cero llamadas. Es evidencia para los consumidores conocidos; no certifica todos los consumidores dinámicos o externos. Estos últimos deben migrar decisiones a google_directive_evidence.

[Contrato, alternativas y límites](compatibility.md) · [comprobación AST/consumidores](compatibility-controller.json) · [prueba adicional runtime](runtime-consumers-controller.json).

## 4. Revisión dual incremental

No se repitieron propuestas originales, contrastes originales ni sus cinco respuestas. Se realizaron solo dos revisiones del diseño de estas tres correcciones y dos revisiones finales/defensas sobre el hash nuevo. Ambos proveedores originales usaron balanced: Claude sonnet-5-5 y Codex gpt-6.1-sol, esfuerzo medium. Contratos nativos validados, procesos recogidos, sin fallbacks ni CommandCode.

- Claude: approve;43.628s sobre el diff exacto.
- Codex: approve;38.625s sobre el diff exacto.

[Claude: diseño](claude-delta-design.json) · [Codex: diseño](codex-delta-design.json) · [Claude: revisión final](claude-final-review.json) · [Codex: revisión final](codex-final-review.json).

Las preguntas nuevas se limitaron al gate tipado, presupuestos y adaptador. Los agentes no ejecutaron pruebas ni sus opiniones se transformaron en recibos. El controlador comprobó identidad de todos los inputs revisados después de sus respuestas. Quedaron observaciones bajas sobre cobertura adicional de consumidores y duplicación acotada; la prueba runtime posterior aborda la primera, sin atribuir a los agentes una revisión que no hicieron de ese recibo posterior. La duplicación sigue aceptada como límite de compatibilidad.

## 5. QA y controles obligatorios

- **191 unitarias SEO aprobadas:**169 anteriores más22 específicas nuevas.
- **13 integraciones SEO aprobadas.** Se reejecutaron porque cambió el parser consumido por ellas.
- Aplicación del parche completo en otro worktree privado de herramientas: cero fuzz y los11 hashes finales idénticos al árbol probado.
- TLS local anterior reutilizado por identidad exacta del transporte; no se volvió a ejecutar ni se presenta como prueba nueva.
- Pruebas nuevas de límites exactos, UTF-8, cola restrictiva, errores tardíos, evidencia heredada, fuentes omitidas, hash estable, tamaño total y adaptador.
- Cero solicitudes al storefront/GSC; no es QA de producción ni evidencia de indexación en Google.

[Recibo QA](controller-qa.json) · [resultados](final-test-results.json) · [recibos de restricciones](constraint-receipts.json).

functional/security/compatibility/native_reuse/seo/performance quedan aprobados **en el alcance aislado definido por cada recibo**, con revisión independiente. No certifican seguridad universal, WCAG, rendimiento real ni indexación. No se cambiaron orquestador, modelos o políticas.

## 6. Operación que requiere autorización

Se solicita integrar **únicamente este parche de 11 archivos en IA-Ipanema**, no el tema de Rhino, no producción y no un rastreo. Antes de aplicar: volver a comprobar las7 preimágenes y la ausencia de las4 altas, hash del parche y respaldos. Si hay una discrepancia, detener sin sobrescribir.

Respaldo íntegro ya verificado: `reports/runs/rhino-performance/20261112T-final-v4-three-fixes-1794516722123973026/preintegration-backups`. El manifiesto registra hashes de preimágenes y archivos que deben estar ausentes. Reversión propuesta: restaurar solo esos7 archivos y retirar solo las4 altas propias, exclusivamente si sus hashes siguen siendo los posteriores aprobados y la reversión está autorizada; ante cambios ajenos, detener.

Tras autorizar: aplicar solo el diff; verificar11 hashes; ejecutar QA SEO posterior del workspace. No usar watch, sincronización global ni despliegues.

Después será necesaria una autorización separada del piloto de cinco destinos, con la invocación concreta del transporte revisada y todas las lecturas auxiliares contabilizadas. Las75URLs (11productos,64artículos) continúan pendientes. No se amplía el alcance por aprobar este motor.
