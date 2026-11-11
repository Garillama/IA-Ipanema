# RHINO — primer lote JS de Home: pruebas terminadas, aplicación pendiente

Fecha: 2026-11-11T00:34:12.840497+00:00. **El propietario eligió continuar solo con pruebas y dejar la aplicación pendiente. El tema no se modificó.**

El borrador está en `candidate/sections/google-reviews.tpl` dentro de la evidencia de este lote; **no está aplicado** en `~/Escritorio/Cli/Rhino-Ipanema/sections/google-reviews.tpl`. No se hizo push, watch, publicación ni operación comercial.

## Qué se investigó y preparó

Se reutilizó [ADR-RHINO-006](ADR-RHINO-006.md), sin repetir discovery ni reconstruir herramientas. Dos perfiles reales de CPU móvil×4 localizaron `setupMore`, de las reseñas, con unos **156 y45ms**. Son muestras diagnósticas distintas de Lighthouse: no explican por sí solas el TBT global3.1s.

La función original alternaba lecturas `scrollHeight/clientHeight` y escrituras de clase por tarjeta. El candidato separa todas las lecturas de las escrituras y evita modificar clases que ya tienen el estado correcto. Se preservan CSS, HTML, ARIA, enlaces, API, fuente/contenido de reseñas, listeners y comercio. El diff está limitado a esa función, y el schema conserva sus bytes originales. No se creó otro motor ni otro observer.

## Pruebas del componente

**13checks aprobados**, seis anchos:360,390,768,1024,1440,1920. Se ejecutó la función fuente exacta contra markup de reseñas obtenido de la página y CSS real, dentro de un componente aislado. Se verificaron estados iniciales, abiertos/cerrados mediante Enter, textos cortos/largos, texto ausente, load y resize. No es un renderer completo de Tiendanube.

Las seis comparaciones de capturas fueron idénticas. Máscara explícita: se retiró el src de avatares que aún no estaban completos en el fixture, manteniendo sus cajas CSS; no se enmascararon el texto, botones ni geometría que se quería comprobar. Los conteos por caso están en el recibo QA. Los estados ARIA y geometría también se compararon, además de los píxeles.

Medianas de5ejecuciones por variante y ancho, CPU×4 en este microensayo:

| Ancho | Layouts antes→candidato | Función+layout final antes→candidato |
|---|---:|---:|
| 360px | 3→1 | 6.90→4.10ms |
| 390px | 3→1 | 5.80→3.80ms |
| 768px | 4→1 | 5.10→3.40ms |
| 1024px | 3→1 | 5.40→3.80ms |
| 1440px | 3→1 | 7.50→5.70ms |
| 1920px | 3→1 | 7.90→6.40ms |

La reducción de3–4layouts a1 es el resultado específico comprobado. Los tiempos son descriptivos y pueden variar; no son una reducción demostrada del TBT total ni de INP. El candidato solo es una optimización pequeña.

## Página completa: ensayo interno y límites

Se completaron **12muestras Lighthouse**,3por variante y dispositivo, alternando control/candidato. Ambos pasaron por la misma sustitución de respuesta dentro del navegador y conservaron recursos externos. El cambio de función se comprobó contra el código publicado. La Home real no fue modificada.

**No se pueden usar sus scores como resultados de producción:** servir el HTML decodificado desde la intervención cambia cómo Lighthouse modela la transferencia del documento. Estos datos se mantienen separados del baseline real53móvil/64desktop y de PageSpeed. No se presenta este ensayo como comparación con esos scores.

| Perfil experimental | TBT mediano antes→candidato | LCP mediano antes→candidato | CLS antes→candidato |
|---|---:|---:|---:|
| mobile | 3310→3127ms | 9.51→9.56s | 0.0003→0.0005 |
| desktop | 408→332ms | 1.94→1.93s | 0.4492→0.4492 |

El TBT experimental mediano bajó en ambos dispositivos, pero móvil no mejoró FCP/LCP y su score experimental pasó29→28; desktop47→51. Con3muestras y variación de terceros, **no hay una mejora global de rendimiento acreditada**. El CLS desktop0.449 sigue pendiente. Estado de la comparación global: `inconclusive`.

Un prototipo de la intervención conservó bytes comprimidos que Chrome presentó como texto: faltaba title, había57nodos y solo2requests. Los scores91–96de ese prototipo se descartaron por falta de fidelidad al storefront. No son resultados de RHINO ni del parche. Otro recibo conserva una aserción inicial demasiado estricta sobre el número de interceptaciones. Se mantuvieron esos fallos y no se promovieron a pruebas aprobadas.

## Consejo y bloqueo actual

Codex produjo una propuesta independiente válida: probar batching condicionado a equivalencia, métricas y revisión. Claude hizo2invocaciones reales y ambas fallaron con categoría `authentication`, salida1, contexto completo, procesos recogidos y0tokens de análisis. `claude auth status` indicó loggedIn=true, pero eso no demostró acceso válido para inferencia. La causa subyacente exacta no se determinó; no se atribuye a un modelo inexistente, rate limit, timeout o JSON inválido.

No hubo contraste, defensa ni revisión independiente completa de este lote. No se reutiliza el consenso del ADRanterior como permiso automático y no se activó CommandCode. El propietario eligió **pruebas solamente**. [ADR-RHINO-007](ADR-RHINO-007.md) mantiene bloqueada la aplicación.

## Estado y siguiente paso

El borrador tiene una mejora localizada comprobada, pero no está aprobado para aplicarse ni demuestra90+. Para retomarlo: recuperar participación real de Claude, conservar la propuesta válida de Codex y las pruebas, completar el contraste/revisión, resolver las condiciones y solo entonces evaluar la aplicación local si vuelve a estar autorizada. No repetir mediciones o nodos válidos sin una razón nueva.

Antes de una eventual aplicación hay que revalidar hashes; actualmente los9archivos vigilados siguen iguales y Git del tema continúa limpio. No se abrió una transacción de edición sobre el tema ni se registró una solución desplegada como verificada. La tarea global de rendimiento permanece abierta.

## Reproducción y evidencia

El test se añadió al repositorio del agente, no al tema:

```bash
node tests/browser/rhino_review_layout.mjs RUTA_DEL_RUN_FUENTE NUEVO_DIRECTORIO_DE_RESULTADOS
```

Lee el snapshot y candidato grabados; requiere acceso autorizado de lectura a RHINO y dependencias del doctor. El directorio de resultados debe ser nuevo. Tras cambiar fuentes/publicación, revalidar el contexto; no asumir que el mismo recibo sigue vigente.

[Diff propuesto, no aplicado](../runs/rhino-performance/20261111T001413-home-js-first-batch-516bcda9/candidate.diff) · [Candidato](../runs/rhino-performance/20261111T001413-home-js-first-batch-516bcda9/candidate/sections/google-reviews.tpl) · [QA reproducible](../runs/rhino-performance/20261111T001413-home-js-first-batch-516bcda9/reusable-test-verification/component-qa.json) · [CPU](../runs/rhino-performance/20261111T001413-home-js-first-batch-516bcda9/cpu-profile-summary.json) · [Ensayo completo](../runs/rhino-performance/20261111T001413-home-js-first-batch-516bcda9/full-page-ab.json) · [Consejo incompleto](../runs/rhino-performance/20261111T001413-home-js-first-batch-516bcda9/council.json) · [Datos consolidados](home-js-first-batch.json).
