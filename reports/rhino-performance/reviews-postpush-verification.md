# RHINO — verificación publicada de setupMore

El propietario indicó que publicó el cambio. Se verificó el contenido servido por `https://rhino-performance.com/` en seis navegaciones nuevas: el cuerpo exacto del candidato aparece una vez y el anterior no aparece. No se hizo push, watch, publish, envío de formularios ni edición del tema durante esta verificación.

## Comportamiento publicado

Resultado: **passed**, 66 comprobaciones, anchos 360/390/768/1024/1440/1920. Se probaron nombres accesibles, controles ARIA, expansión con Enter, cierre con Espacio, conservación del foco y ausencia de overflow horizontal de página. Las flechas respondieron al teclado en tablet/escritorio; están ocultas por diseño en 360/390 px y no se cuentan como probadas allí. Además, dos gestos táctiles reales vía Chrome DevTools pasaron a 360 y 390 px: el desplazamiento avanzó de 0 a 258/283 px, conservando las 10 tarjetas. Son 66 comprobaciones de navegador más 2 casos táctiles. Se recibieron 10 reseñas reales por navegación. No hubo errores JavaScript de página observados.

Axe sobre el carrusel a 390 y 1440 px: cero infracciones detectadas. Alcance limitado al componente y estados ejecutados; no certifica WCAG de la tienda. Capturas conservadas, sin comparación visual exacta de página completa contra una versión publicada anterior.

## Rendimiento de Home

Tres muestras por dispositivo con el motor Lighthouse existente, sin navegaciones QA simultáneas. Caché limpia, throttling simulado. La tabla usa la mediana de los scores individuales, no el score de la primera muestra. LCP/FCP/TBT/Speed Index son métricas de laboratorio, no INP de campo.

| Dispositivo | Performance anterior | Performance actual (rango) | LCP | FCP | CLS | TBT | Speed Index |
|---|---:|---:|---:|---:|---:|---:|---:|
| mobile | 53 | 30 (29–46) | 15.73 s | 4.96 s | 0.0066 | 1586 ms | 16.57 s |
| desktop | 64 | 71 (70–76) | 1.09 s | 0.55 s | 0.4492 | 113 ms | 1.22 s |

- **mobile**: compatibilidad del perfil `compared`. Mismos parámetros y versiones registrados. Variaciones de servidor, recursos externos y contenido no están controladas; tres muestras no establecen causalidad de este parche.
- **desktop**: compatibilidad del perfil `compared`. Mismos parámetros y versiones registrados. Variaciones de servidor, recursos externos y contenido no están controladas; tres muestras no establecen causalidad de este parche.

Las claves de PageSpeed/CrUX están configuradas pero no heredadas por esta sesión; no se realizaron nuevas consultas de esas APIs ni se mezclaron sus mediciones con Lighthouse local. Tampoco se inventaron métricas INP.

La aprobación local anterior demostraba reducción de layouts en pruebas acotadas. Esta comprobación confirma despliegue y comportamiento observado; no convierte automáticamente un cambio de score global en beneficio atribuible a `setupMore`. El objetivo 90+ requiere mediciones de PageSpeed comparables y no se declara alcanzado aquí.

## Evidencias

[QA publicado](../runs/rhino-performance/20261111T173235-reviews-postpush/published-QA.json) · [Comparación y perfiles](../runs/rhino-performance/20261111T173235-reviews-postpush/summary.json) · [Lighthouse original](../runs/rhino-performance/20261111T173235-reviews-postpush/performance-summary.json) · [Decisión anterior](ADR-RHINO-007.md).

## Interpretación y prioridades

**Pruebas funcionales aprobadas; rendimiento global pendiente de aprobación.** No se declara solucionada la velocidad de Home ni se revierte un parche por correlación temporal sin causa demostrada.

1. **P0 móvil — LCP y variabilidad:** mediana 15,73 s, frente a 4,25 s en la serie anterior. Los tres scores fueron 46/30/29, frente a 61/53/52. La miniatura del video principal fue el LCP en las tres muestras nuevas. Los desgloses observados muestran variación del TTFB y de la descarga del recurso, con retraso de renderizado relativamente pequeño. Tiene prioridad alta, ya es descubrible en HTML, eager y fetchpriority alta; añadir otro preload sin investigar no está justificado. Los desgloses observados no se suman como porcentajes del LCP simulado. Falta aislar red/servidor/CDN y contenido para atribuir la causa del deterioro móvil; no se atribuye a `setupMore`.
2. **P1 escritorio — estabilidad visual:** mediana CLS 0,4492, igual que el baseline anterior, con una muestra de 1,0044. El score subió en esta serie de mediana 64 a 71, pero no demuestra causalidad. La inestabilidad visual sigue sin resolverse.
3. **P1 móvil — JavaScript:** TBT mediano de 1.586,5 ms frente a 3.104,7 ms antes. Sigue siendo alto. La evaluación de scripts y el trabajo de style/layout aparecen en los diagnósticos; deben aislarse motores y terceros con pruebas antes de eliminar o diferir recursos. No se llama INP al TBT ni se atribuye su reducción al pequeño ahorro del carrusel.

Los perfiles registrados coinciden y permiten comparación descriptiva, pero las muestras no controlan condiciones externas ni prueban estadísticamente una regresión causada por el cambio. La caída móvil queda señalada para investigación: no se oculta bajo el pase funcional.

### Observación SEO adicional

Una muestra móvil obtuvo SEO 92 por el audit `robots-txt`; las otras dos obtuvieron 100. Una consulta independiente de solo lectura a `/robots.txt` devolvió HTTP 403. Se detuvieron consultas sin reintentar ni evadir el bloqueo. Esto limita la validación desde este entorno: no demuestra que Googlebot esté bloqueado, ni que el contenido de robots sea inválido. No se modificó robots ni el tema.

La primera tanda interrumpida no conservó muestras y no se contó. La tanda final guarda cada una de las seis muestras y conserva sus rangos. Chrome 155.0.8059.84 y Lighthouse 13.6.0; sin aceptación/envío del banner ni formularios comerciales. Se permitió GET de terceros y se bloquearon escrituras mediante el guard de lectura existente; no se compara este perfil con uno de seguimiento comercial sin esas restricciones.

[Diagnósticos originales conservados](../runs/rhino-performance/20261111T173235-reviews-postpush/diagnostics.json) · [Pruebas táctiles](../runs/rhino-performance/20261111T173235-reviews-postpush/touch-QA.json) · [Observación robots](../runs/rhino-performance/20261111T173235-reviews-postpush/robots-observation.json).
