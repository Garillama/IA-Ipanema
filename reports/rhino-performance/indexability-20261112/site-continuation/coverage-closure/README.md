# Rhino — cierre incremental de condiciones V4 y cobertura

12 noviembre 2026. Continuación del inventario/matriz existente. **Sin cambios al motor integrado, tema o producción; cero solicitudes nuevas al storefront y a Google.** No hubo clones Tiendanube, staging, push, publish, watch, cambios de menús, catálogo o canonicals.

## Actualización posterior — recuperación real del consejo

**[Diagnóstico y cierre del protocolo](codex-recovery/README.md):** Codex entregó contrato válido en70,765s con el perfil equilibrado existente y el mismo prompt que había fallado con esfuerzo alto. Se conservaron la propuesta de Claude y el binding; ambos completaron contraste y defensa. El consejo ya no está incompleto por ausencia de Codex, pero el ADR sigue needs_evidence por condiciones técnicas. Se reprodujeron la pérdida de precisión del gate y el crecimiento de la evidencia. Parche y nueve archivos intactos, sin integración ni solicitudes al sitio/GSC. Los apartados siguientes conservan el checkpoint anterior y deben leerse como estado histórico donde hablan de intervención faltante.

## Estado del checkpoint anterior

| Frente | Estado |
|---|---|
| URLs principales conocidas | 125: 124 HTML y 1 XML |
| Rutas HTML observadas | 122 de 124 HTML; evidencia anterior reutilizada |
| HTTP individual de HTML | 49 comprobadas;75 pendientes (11 productos y 64 artículos) |
| V4 | **needs_evidence, implementation_allowed=false**, sin integrar ni ejecutar |
| QA del controlador del candidato | **Cerrado en aislamiento:** 169 unitarias SEO +13 integración +1 TLS local, sobre 9 hashes exactos |
| Consejo original | Incompleto: falta contrato válido de Codex; contraste/defensa no completados |
| GSC | Configurado, credencial no disponible; 0 consultas nuevas |
| Google conocido | 15 inspecciones previas conservadas,10 PASS; no total indexado |
| Categorías administrativas | Sin acceso autorizado identificado; conciliación manual preparada |

[Matriz actualizada](../url-matrix.csv) · [75 destinos pendientes](pending-75.csv) · [estado estructurado](status.json) · [QA exacto](controller-candidate-qa.json) · [revisión de condiciones](council-condition-review.json).

La matriz añade únicamente campos de seguimiento del cierre. HTTP, fuentes, fechas de inspecciones y canonicals existentes permanecen iguales. Los valores pendientes no se transformaron en 200 ni se borraron observaciones. Las ocho páginas del blog siguen acreditando enlaces hacia 86 artículos; no se confundió ese descubrimiento con75 destinos comprobados o indexación de Google.

## 1. Qué bloquea V4 y qué se cerró

Se comprobó el parche final existente SHA256 `7a5a7066bb22d2f87c18286100a9fba0ce76e50e53a8cf9b211821d0eba8b4a0`: seis preimágenes del repositorio coinciden, tres tests nuevos siguen ausentes y AGENTS conserva el hash de la revisión. El candidato se aplicó con cero fuzz **solo a un directorio temporal de código de herramientas/tests**, sin tema ni credenciales.

El controlador ejecutó 169 unitarias SEO, 13 integración y 1 TLS local; las tres ejecuciones aprobaron. Los nueve hashes antes/después de la ejecución coinciden con el manifiesto. No se repitió el subconjunto de 85 pruebas ya incluido en las 169 ni las 396 generales válidas del autor. Esta repetición acotada era necesaria porque la condición pendiente exigía un recibo del controlador sobre el candidato, no reutilizar el QA de la base o etiquetar una ejecución del autor como independiente.

Claude revisó únicamente el recibo nuevo y aceptó que **cierra QA aislado**, no QA posintegración ni funcionamiento en producción. No identificó un defecto nuevo demostrado que requiera cambiar el hash final. Permanecen condiciones reales:

1. Propuesta válida del proveedor original Codex. La recuperación inició, recibió contexto completo y emitió eventos, pero terminó por inactividad a 90 s; un único intento de recuperación con 180 s y máximo 360 s también terminó por inactividad. Ambos procesos quedaron recogidos, sin contrato válido. No hay evidencia para llamarlo fallo de autenticación, cuota, modelo inexistente o congelación; solo silencio de salida durante esos límites. No se volvió a reintentar, cambiar modelo ni activar CommandCode.
2. Contraste y defensa pendientes tras contar con ambas propuestas. La propuesta anterior de Claude permanece válida y conservada; no se compró otra deliberación completa.
3. Recibos del controlador vinculados a alternativas/restricciones concretas. El agregado mantiene pendientes functional,security,compatibility,native_reuse,seo yperformance; aprobar 169 tests no convierte automáticamente cada restricción en pass.
4. Después, autorización específica para integrar el parche local de nueve archivos y QA posterior al workspace. Nada de eso se ejecutó.

La continuación se hizo con el mismo binding de fuente/objetivo/instrucciones; el consejo original quedó respaldado antes de modificar sus checkpoints. Se contabilizaron los cuatro intentos históricos más los intentos nuevos sin reiniciar su contador ni simular votos. La revisión delta de Claude se conserva separada: **no es sustituto de la intervención de Codex ni del contraste formal faltante**.

## 2. Defectos: distinguir correctamente las versiones

El controlador comprobó sobre la base actual, sin red:

| Caso | Resultado de la base actual | Resultado necesario |
|---|---|---|
| `max-image-preview:none` | `noindex` | no debe convertirse en noindex |
| `User-agent: bot` con Disallow total frente a Googlebot | bloquea Googlebot por subcadena | no seleccionar ese grupo solo por contener bot |
| Meta con comilla abierta + cabecera independiente noindex | conserva noindex | noindex |
| Cabecera con comilla abierta + otra cabecera noindex | conserva noindex | noindex |

Los dos últimos falsos negativos pertenecían al **candidato anterior rechazado 4369d84d**, no se deben atribuir automáticamente a la base actual. El parche final 7a5a7066 corrige/previene esos casos y los incluye en sus regresiones. Los dos primeros fallos sí se reprodujeron en la base actual. No son prueba de que una URL de Rhino esté excluida porGoogle; son defectos del motor que impiden darlo por seguro.

El siguiente cambio técnico justificado es **el parche final ya existente**, no crear otro crawler. [Diff exacto preparado](candidate-v4.patch) · [hashes y archivos](candidate-manifest.json). No se modificó ni se solicita aplicar mientras las condiciones obligatorias sigan pendientes. La política de AGENTS exige que las condiciones pendientes impidan implementar; no se propone una excepción ni debilitar DNS/TLS/robots/rutas/presupuestos.

## 3. Cómo completar las 75 respuestas cuando se autorice

[Procedimiento seguro](plan-75.md): cerrar el consejo y recibos, solicitar integración local exacta, QA posintegración, revisar piloto de cinco destinos pendientes con presupuesto acotado y parada 403/429; ampliar únicamente después de revisar el piloto.

La CLI actual no tiene --urls/--skip/resume por lista: no se inventó un comando que garantice comprobar solo 75 sin repetir páginas anteriores. Antes del piloto debe revisarse la invocación concreta del mismo transporte aprobado o acordarse las lecturas de paso necesarias del crawler existente. No se construyó ni ejecutó un verificador alternativo para evitar este bloqueo.

## 4. Categorías y GSC

No se encontró conector administrativo Tiendanube disponible ni integración autorizada de catálogo en el proyecto. La CLI de temas no se reutilizó como autorización administrativa. La [conciliación manual](procedimientos-manuales.md) y su [plantilla](admin-category-reconciliation.csv) permiten registrar árbol completo, padres, visibilidad, publicación y IDs si se exponen. Los cinco registros iniciales son referencias públicas, **no datos administrativos ya conciliados**. Categoría oculta, estado de publicación y URL accesible son dimensiones diferentes; no se inventan estados que el panel no muestre.

El doctor de acceso existente informó credential_available=false y account_access_tested=false. No se probó la API sin token ni se inició autenticación alternativa. Siguen preparados únicamente Pistolas de masaje, Terapia fría, Compresión frío/calor y catálogo página 2 para nuevas inspecciones cuando vuelva acceso autorizado. Las 15 anteriores y 170 filas históricas se reutilizan y no se convierten en censo indexado.

El [procedimiento oficial de exportación](procedimientos-manuales.md) explica selección de propiedad, filtros, informe Páginas y descarga por motivo, conservando totales/fecha/límites. Google limita los ejemplos exportados a 1000 filas y puede no mostrar todas las URLs aunque sean menos. No se garantiza cobertura exhaustiva por exportar un CSV. Fuentes oficiales enlazadas dentro del procedimiento.

## 5. Qué requiere intervención y qué permanece intacto

- Recuperar una intervención válida de Codex en el nodo pendiente; no se pide renovar credenciales a ciegas porque no hay prueba de fallo de autenticación. La sesión principal de Codex no se cuenta como aprobación independiente de su propio candidato.
- Restablecer el acceso autorizado GSC mediante el mecanismo existente, o aportar exportaciones oficiales sin credenciales.
- Aportar la lectura/exportación administrativa de categorías para conciliar la taxonomía; no crear ni mostrar elementos.
- Autorizar la integración local exacta **solo después de cerrar las condiciones**, con respaldo y reversión. La autorización anterior de paginación no cubre el motor.

Contacto y Sobre Rhino no se modificaron ni promocionaron; Sobre sigue pendiente editorial. Canonicals del blog y consulta a Tiendanube se conservan, sin envío ni corrección nueva. No se repitieron categorías, paginación publicada, Lighthouse o inspecciones ya válidas.

La cobertura permanece 49/124 HTML con HTTP propio y75 pendientes. No hay nuevas URLs de producción con problemas técnicos demostrados en esta fase porque no se hicieron solicitudes al sitio. La incertidumbre no se presenta como defecto ni se promete indexación.

## Evidencia

Run privado/ignorado: `reports/runs/rhino-performance/20261112T194437-v4-coverage-closure-3d3473a2`. Conserva matriz anterior, artefacto aplicado en aislamiento,183 pruebas del controlador, propuesta previa, intentos Codex y límites/procesos, revisión delta y agregado bloqueado. Los módulos base siguen idénticos y el parche no se aplicó al workspace. No hay permisos de producción ni cuentas transferidos a workers.


## Continuación: tres reservas corregidas en candidato aislado

El estado anterior de needs_evidence se conserva como historial del hash7a5a7066. El [candidato nuevo](final-candidate/README.md) resuelve las tres reservas, cuenta con revisión final de ambos proveedores y está listo para solicitar autorización específica de integración local. No se aplicó al motor ni se ejecutó el piloto.
