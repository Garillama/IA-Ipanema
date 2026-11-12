# RHINO — primer lote JS de Home aplicado y aceptado localmente

Actualizado: 2026-11-11 T 17:16:58.134645+00:00. **El cambio está aplicado y aceptado solo en el tema local** `~/Escritorio/Cli/Rhino-Ipanema/sections/google-reviews.tpl`, función `setupMore` (línea 364). No hubo push, watch, publicación ni cambios en cuentas/apps o datos comerciales.

Claude recuperó acceso real para inferencia. El Dual-Agent Council revisó exclusivamente este candidato, contrastó propuestas y condiciones y aprobó conservarlo localmente después del QA. **No se ha demostrado 90+ ni una mejora global de PageSpeed.**

## Cambio y reversibilidad

Se conserva el candidato original: primera pasada de lecturas `scrollHeight/clientHeight`, segunda de escrituras de `has-more` solo cuando cambia su estado. No se reescribió el carrusel ni se añadieron observadores, librerías o peticiones.

**Tipografía, tamaños, CSS, HTML, Twig/schema, API de reseñas, eventos, teclado/ARIA y lógica comercial fuera de la función permanecen iguales.** El diff del tema contiene un único archivo,11 líneas añadidas y 6 retiradas. Base Git`2e8c13aefd7b346943e928aee8e598f69dd47374`.

Transacción local **`69974a0971f74e9a90d168d0c316c575`**, intento 1 de 2, estado`accepted`. Respaldo privado con permisos 0600 e ignorado por Git, hash previo comprobado antes de escribir y hash posterior cotejado con el código revisado. El agente no hizo commit ni push.

- Antes: `10e64ea2fb128479636297cdbd543f45b4fdbfdbae99fd53b0e578785367e67b`.
- Después: `75a487600c5d71001fa2e0970dad1cb943f80d399f1af89db559bffc3253fd30`.

## Consejo y revisión independiente

Se ejecutaron 9 invocaciones reales:2 propuestas independientes,2 contrastes,2 defensas, una revisión independiente de Claude previa a la aplicación y dos revisiones posteriores de Claude/Codex tras corregir y ejecutar el QA. Modelos del registro: `claude-sonnet-5-5` y `gpt-6.1-sol`, esfuerzo medio, sin escalado automático ni CommandCode. El subtotal de coste informado por Claude fue USD 0,9383; Codex no expuso coste, por lo que no se presenta un total completo.

El contraste incluyó 5 preguntas concretas y 7 objeciones. Codex cuestionó la atribución geométrica y el coste de asignación; Claude explicó el clamp/ancho de las tarjetas y aceptó limitar las afirmaciones a lo probado. Ambos exigieron cantidades, repetición y render simulado. Se resolvieron las lagunas obligatorias con recibos del controlador, no con votos. El coste de memoria/GC queda sin medir.

El ADR es **`approved_with_conditions` para implementación local**, con QA posterior aprobado. Las condiciones de navegador, render completo y velocidad global no se convierten en hechos medidos. [ADR-RHINO-007](ADR-RHINO-007.md).

## Resultados posteriores a la aplicación

**617 comprobaciones aprobadas:**61 del componente con markup obtenido de la tienda y 556 offline dirigidas. Se verificaron 6 anchos —360,390,768,1024,1440,1920—, estados de apertura/cierre, texto corto/largo/ausente, resize, foco y relaciones ARIA, cantidades 0/1/3/5/24 y estrés 100, reemplazo de tarjetas y API simulada vacía/válida/sin textos.

Las seis comparaciones de captura fueron idénticas **con máscara explícita únicamente sobre la pintura de los avatares externos**, manteniendo sus dimensiones. Texto, botones, clases, geometría y relaciones ARIA no se enmascararon. El fixture comprueba ancho CSS real y familia Poppins antes de validar; no se alteraron fuentes en el tema.

Medianas del ensayo de funciones fuente,5 ejecuciones por variante/ancho, CPU×4. Solo representan ese componente y sus entradas:

| Ancho | Layouts original→aplicado |
|---|---:|
| 360 px | 4→1 |
| 390 px | 3→1 |
| 768 px | 6→1 |
| 1024 px | 5→1 |
| 1440 px | 3→1 |
| 1920 px | 3→1 |

En llamadas repetidas sin cambio de estado, el original produjo 20 mutaciones de clase por tarjeta en 20 llamadas del fixture; el candidato produjo 0. La aceptación transaccional usa esa evidencia offline real ejecutada antes y después, evitando depender del antiguo fixture visual defectuoso.

Un ensayo más controlado, **8 pares alternados en el mismo DOM** por ancho, registró:

| Ancho | Layouts, mediana original→aplicado | Función+layout, mediana original→aplicado |
|---|---:|---:|
| 390 px | 3→1 | 3.90→3.10 ms |
| 768 px | 7→1 | 7.70→4.60 ms |
| 1440 px | 4→2 | 4.50→3.40 ms |

No se garantiza exactamente 1 layout ni ese ahorro temporal en toda llamada. Se redujo trabajo en los casos registrados, pero no se deduce INP ni mejora global. Una serie agrupada entre páginas había mostrado un outlier a 1440(46.6 msfrente a 3.2 ms); no se reprodujo en la alternancia sobre el mismo DOM. Su causa exacta permanece desconocida. El umbral diagnóstico prospectivo —incremento absoluto>2 ms y relativo>25%, con prueba unilateral de cambios de signo pareados p≤0.05— no señaló regresión en esos tres microensayos; **no es certificación de no inferioridad ni un gate de producción**.

`qa --suite quick` del repositorio también terminó`passed`. No se repitieron discovery, PageSpeed/CrUX ni los anteriores ensayos globales Lighthouse que no podían acreditar este parche.

## Corrección importante de evidencia

Al ejecutar el QA posterior aparecieron fallos que se conservaron y no se ignoraron:

1. Una comparación de estado a 1920 falló; el harness inicial no conservó el campo discrepante. El diagnóstico aislado A/B y un control A/A pasaron, pero no se afirma que eso determine la causa exacta.
2. Otro fallo visual quedó localizado en los avatares externos, cuyas imágenes podían verse vacías o con iconos de error.
3. Se detectó que el contenedor clonado incluía el script original: podía iniciar otra llamada real a la API y reemplazar los nodos enmascarados mientras se probaba el candidato.
4. El fixture omitía el`meta viewport` y no resolvía bien URLs CSS relativas al protocolo en`about:blank`: podía medir un layout 980 px y una fuente de sistema aunque se pidiera un dispositivo 360 px.

**La antigua evidencia UI de 13 checks fue sustituida para la aceptación**, no se presenta como prueba fiel de la tienda. Las nuevas 61 comprobaciones eliminan scripts/estilos clonados antes de parsear, desactivan la API del fixture, ejecutan solo el script bajo prueba, declaran base/viewport, verifican Poppins/ancho, comparan estados tras estabilización acotada y usan máscaras de avatares explícitas. Los 556 checks sintéticos son independientes de ese problema de clonación.

Estas correcciones afectaron solo a los tests. **No se modificó CSS, viewport ni tipografía de RHINO para conseguir pases.** Claude y Codex revisaron otra vez el diff y toda esta evidencia antes de aceptar el cambio local. Se conserva la trazabilidad de los fallos y del ensayo de compresión inválido anterior; sus scores nunca se consideran rendimiento de RHINO.

## Riesgos y siguiente prioridad

- **Defecto previo separado:** reinicializar todo el componente duplica manejadores y puede alternar dos veces el botón. Se reprodujo tanto en original como en candidato. Este parche no lo introduce ni lo corrige; la Home configurada tiene 1 instancia. `setupMore` repetido es un caso distinto y sí conserva su estado.
- Array/objetos temporales O(n); GC/memoria no medidos. Se probaron los límites configurados 3–24 y estrés 100  solo en fixture.
- Pruebas Chrome de componente y API simulada, sin certificación Safari, render Twig completo, WCAG o indexación.
- La comprobación publicada requiere que el propietario publique cuando decida; **el agente no lo hizo**. Consultar producción no mediría este archivo local sin publicar.
- El objetivo 90+ continúa pendiente. Las prioridades siguientes siguen siendo el trabajo JS inicial móvil y la causa raíz del CLS de video desktop según la evidencia ya existente; no se eliminaron analítica ni funciones para elevar un score.

La solución se registró con alcance local y hashes de sus dependencias como`rhino-reviews-setupmore-batching-20261111`. Cambios posteriores de componente, CSS o fuentes requieren revalidarla; no transfiere derechos de código entre tiendas.

## Evidencia y reproducción

[Diff revisado](../runs/rhino-performance/20261111T163507-reviews-candidate-council-resume-2451ba30/source/candidate.diff) · [Aceptación y respaldo](../runs/rhino-performance/20261111T163507-reviews-candidate-council-resume-2451ba30/acceptance.json) · [QA 61](../runs/rhino-performance/20261111T163507-reviews-candidate-council-resume-2451ba30/post-apply-faithful-fixture/component-qa.json) · [QA 556](../runs/rhino-performance/20261111T163507-reviews-candidate-council-resume-2451ba30/post-apply-edge/edge-qa.json) · [Microensayo pareado](../runs/rhino-performance/20261111T163507-reviews-candidate-council-resume-2451ba30/paired-statistics.json) · [Revisiones finales](../runs/rhino-performance/20261111T163507-reviews-candidate-council-resume-2451ba30/post-review.json) · [ADR del controlador](../runs/rhino-performance/20261111T163507-reviews-candidate-council-resume-2451ba30/council/ADR.md) · [Datos consolidados](home-js-first-batch.json).

```bash
node tests/browser/rhino_review_layout.mjs reports/runs/rhino-performance/20261111T163507-reviews-candidate-council-resume-2451ba30/post-apply-source NUEVO_OUTPUT
node tests/browser/rhino_review_edge_cases.mjs reports/runs/rhino-performance/20261111T163507-reviews-candidate-council-resume-2451ba30/post-apply-source OTRO_OUTPUT
```

Usar destinos nuevos. La primera prueba lee la tienda en modo autorizado; la segunda es offline y usa reseñas sintéticas de prueba. Tras cambiar fuentes o publicar, preparar/revalidar el snapshot en vez de asumir que la evidencia histórica sigue vigente.

[Informe previo a esta reanudación, conservado](../runs/rhino-performance/20261111T163507-reviews-candidate-council-resume-2451ba30/report-before-resume.md).


## Comprobación después de publicación

El propietario publicó el cambio y se verificó el parche servido y el carrusel real. [Resultados publicados, pruebas y Lighthouse](reviews-postpush-verification.md). Esta comprobación no altera los recibos de aceptación local ni demuestra por sí sola una mejora global atribuible al parche.
