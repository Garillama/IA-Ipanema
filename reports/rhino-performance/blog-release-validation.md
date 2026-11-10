# RHINO — prueba del parche del blog publicado por el propietario

Fecha: 2026-11-10T21:54:52.780540+00:00. URL: https://rhino-performance.com/blog/. Referencias públicas de assets observadas: 14828608.

**El parche está presente y su comportamiento se verificó en la tienda. El rendimiento móvil mejora en LCP, pero sigue siendo insuficiente.** El agente solo hizo lecturas y mediciones; el push lo ejecutó el propietario.

## Resultado de rendimiento

Tres ejecuciones por perfil, Lighthouse13.6.0 y Chrome155.0.8059.84, mismas condiciones locales que la línea base móvil.

| Métrica del blog | Móvil antes, mediana3 | Móvil ahora, mediana3 | Escritorio ahora, mediana3 |
|---|---|---|---|
| Performance/100 | 44 | 48 | 88 |
| LCP | 13.26s | 6.19s | 1.84s |
| FCP | 1.97s | 1.80s | 0.91s |
| TBT | 1493ms | 1239ms | 43ms |
| CLS | 0.000 | 0.000 | 0.042 |

La reducción observada del LCP móvil mediano es **53.3%**. Antes:12.69–13.39s; ahora:6.07–8.91s. No se oculta el rango ni se promete ese porcentaje a todos los usuarios. El score móvil solo subió4puntos y continúa bajo. Speed Index mediano prácticamente igual:5.16→5.12s.

No hay baseline Lighthouse local comparable de blog desktop: **88/100 y1.84s son resultados actuales**, no una comparación con PageSpeed anterior. Los datos son del blog, no del inicio ni de toda la tienda.

## Perfil y variabilidad

Mobile412×823/DPR1.75, CPU×4, RTT150ms/1638.4Kbps simulados; desktop1350×940/DPR1, CPU×1, RTT40ms/10240Kbps. Cuatro categorías, almacenamiento/caché reiniciados, contextos anónimos sin decisión de consentimiento. El motor bloquea POST y no se enviaron formularios ni se añadieron productos al carrito.

El comparador existente devolvió `compared` para móvil: misma fuente, URL, versiones, viewport, CPU/red, categorías, política y3muestras distintas. Es comparación descriptiva; n=3 no activa un gate estadístico. Sus deltas positivos no se interpretan automáticamente como regresiones demostradas.

En una muestra posterior hubo espera observada al primer byte de4.38s y descarga del recurso de3.52s; las otras dos tuvieron TTFB0.80/0.57s. La mediana observada de TTFB~0.80s es similar a la anterior. No se deduce un fallo permanente de hosting ni se divide ese desglose observado entre el LCP simulado para inventar porcentajes causales.

No hubo consultas nuevas de PSI/CrUX ni se infiere INP del TBT. El campo agregado no verifica inmediatamente un push.

## Comportamiento publicado comprobado

- HTML inicial móvil390px y desktop1440px: primera portada con `src`/`srcset` y `fetchpriority=high`; exactamente una card prioritaria.
- Network CDP: la solicitud de esa portada tiene prioridad **High**. Se verificaron descarga y currentSrc, no solo atributos del DOM.
- Sin JavaScript: imagen descargada, completa, dimensión positiva y opacidad1; otros high=0. Se conserva su URL original JPG.
- Página2: primera portada prioritaria y12enlaces a artículos distintos de los12de la página1, sin solapamiento.
- Fragmento `?page=2&view=cards`:0portadas prioritarias; mantiene lazy.
- Filtro real obtenido de los enlaces de la tienda:0portadas prioritarias, sin inventar destinos.
- Tarjetas del blog en home y producto:0prioridades altas heredadas.
- Todas las lecturas de estas vistas devolvieron200. Los5archivos locales vigilados mantuvieron sus hashes. No se realizó otro push ni se cambió código durante la prueba.

Son 23 checks acotados aprobados sobre el comportamiento publicado y procedencia de mediciones. No equivalen a QA completo de todas las páginas/estados, conformidad AA ni validación de conversiones.

## Qué sigue

1. **Optimizar la portada original (~500KB):** el parche corrigió su descubrimiento y prioridad, no el archivo. Lighthouse sigue señalando ahorro estimado en formato/compresión; ese ahorro no está implementado ni garantizado.
2. **Reducir trabajo JS móvil:** TBT mediano1.24s sigue alto. La prueba anterior de bloquear marketing mejoraba TBT pero empeoraba LCP; se necesita una estrategia que preserve eventos y comercio.
3. **Investigar variabilidad de respuesta/recursos** con más muestras si persiste. No cambiar hosting basándose en una observación.
4. CLS de video de home sigue en el diagnóstico anterior; esta prueba no lo vuelve a medir ni lo declara corregido.

[Resultados y muestras](blog-release-validation.json) · [Verificación HTML/DOM/red](../runs/rhino-performance/20261110T214551-blog-release-validation-f5d536bf/release-check.json) · [Sin JS](../runs/rhino-performance/20261110T214551-blog-release-validation-f5d536bf/no-js.json) · [Lighthouse](../runs/rhino-performance/20261110T214551-blog-release-validation-f5d536bf/performance-summary.json) · [Recibo QA](../runs/rhino-performance/20261110T214551-blog-release-validation-f5d536bf/qa-proof.json).

La revisión independiente del código fue realizada por Claude en la fase anterior. Esta comprobación posterior la ejecutó el controlador Codex con herramientas; no se fingió una nueva deliberación ni otra intervención de Claude. La solución se considera verificada únicamente para el alcance, composición, archivos y fecha indicados; cambios posteriores requieren revalidación.
