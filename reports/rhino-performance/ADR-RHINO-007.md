# ADR-RHINO-007 — setupMore aceptado localmente

Estado actual: **approved_with_conditions**, aplicado y aceptado **solo localmente**. Fecha:2026-11-11 T 17:16:58.158291+00:00. Seguimiento de[ADR-RHINO-006](ADR-RHINO-006.md). El propietario autorizó reanudar el consejo y aplicar el candidato únicamente tras revisión/QA; la antigua restricción de“solo pruebas” quedó sustituida por esta instrucción actual. No autoriza producción.

## Decisión

Conservar exactamente el candidato original de Codex en `sections/google-reviews.tpl:setupMore`: calcular los estados antes de cambiar clases y evitar escrituras redundantes. Único archivo del tema modificado. No se cambió CSS, tipografía, HTML, API, ARIA, LS ni comercio ni se añadió infraestructura del orquestador.

Original:10 e 64 ea 2 fb 128479636297 cdbd 543 f 45 b 4 fdbfdbae 99 fd 53 b 0 e 578785367 e 67 b. Aplicado:75 a 487600 c 5 d 71001 fa 2 e 0970 dad 1 cb 943 f 80 d 399 f 1 af 89 db 559 bffc 3253 fd 30. Base Git:2 e 8 c 13 aefd 7 b 346943 e 928 aee 8 e 598 f 69 dd 47374. Transacción privada:69974 a 0971 f 74 e 9 a 90 d 168 d 0 c 316 c 575, intento 1,aceptada con respaldo y hashes comprobados. No hubo commit/push del agente.

## Propuestas, contraste y objeciones

Claude revisó independientemente el diff y exigió cubrir cantidades, repetición y render. Codex cuestionó que el flex-basis demostrase toda equivalencia y que el coste O(n)fuera despreciable sin medirlo. Ambos conservaron el candidato y limitaron sus afirmaciones;5 preguntas recibieron 5 respuestas. La objeción de cobertura fue resuelta por QA fuente/controlador; GC y compatibilidad fuera del entorno probado permanecen límites, no pases inventados.

Se consideró mantener el original. Crear observadores, retrasar la API o introducir otro motor ampliaría el alcance sin necesidad. El candidato reutiliza función, selectores, estilos, controles y llamadas existentes. La elección del ID`claude-candidate-narrow-local`representa esa implementación compartida, no autoridad superior de un proveedor.

## Evidencia final y corrección de pruebas

61 checks del componente en 6 anchos, capturas iguales con máscara de avatares, fuentePoppins/ancho CSS comprobados;556 checks offline de cantidades, repetición, API simulada y teclado/foco/ARIA;48 observaciones en un microensayo de pares alternados. Reducción de layouts observada, sin prometer tiempos globales,INP o 90+.

El QA inicial tenía defectos de clonación de scripts/API, viewport y resoluciónCSS. La evidencia UIantigua fue sustituida por la corregida; fallos y outlier temporal se conservaron. El primer campo discrepante 1920 no puede reconstruirse; no se inventa su causa. El outlier 1440 no se reprodujo en alternancia del mismo DOM. Ambas incidencias se entregaron a los revisores, que aprobaron conservar el código exacto después del QA corregido.

## Aplicación y revisión

9 invocaciones reales entre propuestas, contraste, defensa y revisiones previas/posteriores. Claude y Codex aprobaron la conservación local tras revisar la evidencia final. El controlador revalidó restricciones, hashes y diff mediante el agregador existente. No se contaron respuestas como pruebas y no se activó CommandCode.

Transacción aceptada con evidencia offline previa válida de escrituras redundantes y QA posterior vinculado al hash aplicado. Esa proyección conserva el timestamp de medición original y distingue su fecha de ensamblado; no inventa una prueba ejecutada antes. El antiguo baseline/recibos permanecen archivados.

## Condiciones y pendientes

- Revalidar tras cambios de CSS, fuente, markup, versión o contexto.
- GC/asignaciones y matriz completa de navegadores no medidos.
- No hay render Twig completo ni prueba de publicación; ninguna conformidadWCAG/indexación/score 90+certificada.
- El defecto de doble inicialización es previo y se mantiene en backlog separado.
- Los grandes problemas deJS móvil yCLS desktop requieren sus propios lotes, sin sacrificar diseño, SEO o comercio.

[Informe actual](home-js-first-batch.md) · [ADR bruto y recibos](../runs/rhino-performance/20261111T163507-reviews-candidate-council-resume-2451ba30/council/ADR.md) · [Revisiones posteriores](../runs/rhino-performance/20261111T163507-reviews-candidate-council-resume-2451ba30/post-review.json) · [Estado anterior conservado](../runs/rhino-performance/20261111T163507-reviews-candidate-council-resume-2451ba30/ADR-RHINO-007-before-resume.md).
