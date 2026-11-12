# Rhino Performance — línea base publicada, peso y prioridades móviles

Verificación: 2026-11-12T03:27:59.636796+00:00. Participante: **Codex únicamente**. Sin nuevas consultas PSI, sin cambios del tema ni operaciones remotas de escritura.

Se reutilizaron 130 respuestas PSI válidas (129 mediciones únicas): seis páginas con diez consultas por dispositivo y Home con cinco por dispositivo, una de escritorio repetida. No se presenta Home como si tuviera diez por dispositivo. Las estadísticas siguientes excluyen esa respuesta repetida; el CSV conserva todas las respuestas y sus correspondencias.

## Resultado principal

**El peso de 2,80 MB móvil es el total contabilizado por PageSpeed, no una demostración de que descargamos 12,6 % más bytes que en el PDF histórico.** La Home móvil tiene una transferencia reportada casi constante, mientras Performance oscila 49–86. El problema de las peores ejecuciones no se explica solo por cambios de peso. En escritorio se observa un MP4 de 7,689 MB dentro de un total reportado de aproximadamente 10,716 MB.

## Performance: peor, media aritmética, mediana y mejor

| Página | Dispositivo | Consultas/únicas | Peor | Media | Mediana | Mejor | Desv. estándar descriptiva |
|---|---|---:|---:|---:|---:|---:|---:|
| Home | mobile | 5/5 | 49 | 69.0 | 71.0 | 86 | 14.9 |
| Home | desktop | 5/4 | 66 | 79.0 | 77.0 | 96 | 10.9 |
| PRO AIR | mobile | 10/10 | 50 | 67.5 | 70.5 | 85 | 10.9 |
| PRO AIR | desktop | 10/10 | 68 | 83.0 | 84.0 | 97 | 7.3 |
| Baterías PRO AIR | mobile | 10/10 | 46 | 66.0 | 69.5 | 81 | 11.4 |
| Baterías PRO AIR | desktop | 10/10 | 55 | 70.3 | 64.0 | 91 | 13.3 |
| Presoterapia | mobile | 10/10 | 47 | 79.6 | 82.5 | 91 | 11.9 |
| Presoterapia | desktop | 10/10 | 78 | 82.9 | 81.0 | 93 | 4.8 |
| Accesorios | mobile | 10/10 | 44 | 74.8 | 76.5 | 87 | 11.2 |
| Accesorios | desktop | 10/10 | 68 | 79.5 | 82.0 | 89 | 6.7 |
| Política de devolución | mobile | 10/10 | 74 | 84.0 | 83.0 | 95 | 7.1 |
| Política de devolución | desktop | 10/10 | 70 | 83.2 | 83.0 | 96 | 8.4 |
| Blog | mobile | 10/10 | 62 | 68.2 | 68.0 | 75 | 4.5 |
| Blog | desktop | 10/10 | 59 | 72.5 | 73.5 | 82 | 6.6 |

La desviación estándar describe estas observaciones, no un intervalo de confianza ni una garantía. En las seis páginas hay diez mediciones únicas por dispositivo. No se mezclan métricas de distintas ejecuciones para fabricar un resultado; cada fila del CSV conserva fecha, score, métricas y fuente.

## Mínimos y máximos observados

| Página | Perfil | LCP s, mín.–máx. | TBT ms, mín.–máx. | CLS, mín.–máx. | Peso reportado MB, mín.–máx. |
|---|---|---:|---:|---:|---:|
| Home | mobile | 3.22–8.79 | 233–1138 | 0.0213–0.0455 | 2.803–2.804 |
| Home | desktop | 0.84–0.94 | 155–2434 | 0.0020–0.0025 | 10.705–10.719 |
| PRO AIR | mobile | 3.45–8.56 | 256–1320 | 0.0247–0.4671 | 2.476–2.501 |
| PRO AIR | desktop | 0.77–0.95 | 107–1262 | 0.0494–0.1578 | 2.691–2.785 |
| Baterías PRO AIR | mobile | 3.16–10.49 | 336–1011 | 0.0197–0.1426 | 2.420–2.443 |
| Baterías PRO AIR | desktop | 0.77–0.99 | 121–1422 | 0.0413–0.3613 | 2.812–2.842 |
| Presoterapia | mobile | 2.89–7.75 | 183–1294 | 0.0034–0.0447 | 2.244–2.403 |
| Presoterapia | desktop | 1.02–1.15 | 176–468 | 0.0129–0.0364 | 2.504–2.535 |
| Accesorios | mobile | 2.71–10.56 | 236–1078 | 0.0197–0.0447 | 2.305–2.361 |
| Accesorios | desktop | 0.88–1.17 | 255–1394 | 0.0143–0.0325 | 2.468–2.496 |
| Política de devolución | mobile | 1.08–3.23 | 114–1010 | 0.0236–0.6600 | 2.287–2.311 |
| Política de devolución | desktop | 0.30–0.87 | 105–627 | 0.0020–0.1311 | 2.305–2.318 |
| Blog | mobile | 5.66–7.30 | 148–506 | 0.0010–0.0448 | 3.477–3.547 |
| Blog | desktop | 2.32–2.84 | 87–665 | 0.0079–0.0454 | 4.647–4.742 |

Las distribuciones completas (mínimo, media, mediana, máximo, desviación y n) de LCP/FCP/TBT/CLS/Speed Index y bytes están en `analysis.json`. Las tablas de rangos no representan una ejecución ficticia combinada.

## Comparación de peso frente al PDF histórico

| Tipo de página | PDF móvil MB | PSI móvil mediano MB | Diferencia aritmética MB | Variación aritmética | PSI desktop mediano MB |
|---|---:|---:|---:|---:|---:|
| Home | 2.49 | 2.803 | +0.313 | +12.6% | 10.716 |
| PRO AIR | 2.17 | 2.488 | +0.318 | +14.7% | 2.781 |
| Baterías PRO AIR | 2.13 | 2.430 | +0.300 | +14.1% | 2.838 |
| Presoterapia | 2.16 | 2.387 | +0.227 | +10.5% | 2.532 |
| Accesorios | 2.09 | 2.348 | +0.258 | +12.3% | 2.481 |
| Política de devolución | 2.02 | 2.299 | +0.279 | +13.8% | 2.317 |
| Blog | 3.12 | 3.494 | +0.374 | +12.0% | 4.681 |

**Estos deltas son aritméticos, no aumentos causales demostrados.** El PDF aporta totales redondeados y no conserva el inventario de peticiones, URLs exactas por variante ni el perfil completo. Solo contiene referencia móvil. No hay histórico desktop de ese documento para calcular una subida de escritorio. MB nuevos = 1.000.000 bytes; la convención exacta del peso antiguo no está acreditada.

## Desglose del peso por página y dispositivo

Medianas de cada categoría, MB contabilizados por PSI. `third-party` es un subconjunto superpuesto y no se suma al total. Las medianas por categoría tampoco tienen por qué sumar exactamente la mediana total.

| Página | Perfil | JS | CSS | Imágenes | Video/media | Fuentes | HTML/documentos | Otros |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Home | mobile | 1.732 | 0.214 | 0.617 | 0.000 | 0.035 | 0.124 | 0.083 |
| Home | desktop | 1.743 | 0.213 | 0.828 | 7.689 | 0.035 | 0.124 | 0.084 |
| PRO AIR | mobile | 1.750 | 0.212 | 0.290 | 0.000 | 0.035 | 0.134 | 0.068 |
| PRO AIR | desktop | 1.750 | 0.212 | 0.585 | 0.000 | 0.035 | 0.134 | 0.068 |
| Baterías PRO AIR | mobile | 1.733 | 0.212 | 0.251 | 0.000 | 0.035 | 0.133 | 0.067 |
| Baterías PRO AIR | desktop | 1.744 | 0.212 | 0.649 | 0.000 | 0.035 | 0.133 | 0.067 |
| Presoterapia | mobile | 1.692 | 0.212 | 0.320 | 0.000 | 0.026 | 0.073 | 0.063 |
| Presoterapia | desktop | 1.698 | 0.212 | 0.461 | 0.000 | 0.026 | 0.073 | 0.063 |
| Accesorios | mobile | 1.686 | 0.212 | 0.287 | 0.000 | 0.026 | 0.074 | 0.063 |
| Accesorios | desktop | 1.686 | 0.212 | 0.420 | 0.000 | 0.026 | 0.074 | 0.063 |
| Política de devolución | mobile | 1.689 | 0.212 | 0.257 | 0.000 | 0.017 | 0.062 | 0.062 |
| Política de devolución | desktop | 1.689 | 0.212 | 0.275 | 0.000 | 0.017 | 0.062 | 0.062 |
| Blog | mobile | 1.706 | 0.212 | 1.327 | 0.000 | 0.026 | 0.067 | 0.157 |
| Blog | desktop | 1.695 | 0.212 | 2.521 | 0.000 | 0.026 | 0.067 | 0.155 |

## Caché: por qué no equiparamos el total PSI con descarga física

En todas las muestras de Home hay nueve filas marcadas como `cache=memory` con valores `transferSize` no nulos; representan aproximadamente 0,443 MB del total contabilizado. El SDK `googrev-7400935.js` aparece dos veces, una marcada `none` y otra `memory`; también se repiten CSS e imágenes de la app. El navegador publicado confirmó una respuesta de red y otra con `fromCache=true` para el SDK, y un único iframe/SDK en el DOM final. No se afirma que existan dos descargas físicas ni dos widgets simultáneos.

Restar mecánicamente esas filas deja aproximadamente 2,361 MB en móvil, pero **no es una medición directa completa de bytes de red ni sustituye los 2,803 MB originales**. Los metadatos de caché, el alcance de iframes y la ventana observada deben conservarse. Tampoco demuestra que el sitio haya adelgazado respecto al PDF.

El código instalado de Lighthouse 13.6.0 conserva `cache` y `transferSize` por separado en `core/audits/network-requests.js`; `core/computed/resource-summary.js` agrega los tamaños. Su implementación de Lightrider obtiene transferencia mediante cabeceras internas cuando existen. No se diagnostica un bug de Google ni se altera el adaptador para maquillar las cifras.

## Verificación actual de producción

Tres navegaciones de lectura a la Home canónica: móvil, escritorio y consumidor de reseñas. GET/HEAD/OPTIONS, contextos anónimos, sin formularios, carrito, consentimiento ni compras. Chrome DevTools Protocol mediante Puppeteer existente; no había una herramienta Chrome DevTools MCP conectada en este runtime. Son observaciones de producción, no scores Lighthouse ni datos de usuarios reales.

- La Home canónica respondió 200; no se reintentó el alias www que tuvo un 403 anteriormente.
- Assets públicos observados pertenecen a instalación 14828608. Esa referencia no sustituye verificar la vinculación del CLI antes de un eventual despliegue.
- El video no tenía fuente MP4 activa en móvil sin interacción: pausado y `readyState=0`.
- En escritorio el MP4 se descargó con respuesta 206, aproximadamente 7.689 MB; 1920×1080, 20,42 s y reproducción activa. Al desplazarlo fuera del viewport quedó pausado.
- La portada inicial conserva prioridad alta y formato AVIF en el navegador observado; no se justifica añadir otro preload genérico.
- El CSS publicado contiene el guard `scripting: enabled` y la condición `data-transparent-runtime` del ajuste de header. No se afirma identidad de todo el Twig local con producción.
- La app de reseñas se ejecuta en un iframe público; el SDK no figura como inclusión directa en los archivos del tema inspeccionados. La sección personalizada sí consume su API. No se deduce que su llamada pequeña sea la responsable de todo el peso de la app.

## Imágenes y documentación de Tiendanube

La documentación [WebP y Thumbnails](https://docs.tiendanube.com/help/webp-y-thumbnails) confirma variantes optimizadas para imágenes del editor y el uso de `settings_image_url`/srcset. Se priorizará el helper existente. El tema ya contiene `snippets/image.tpl`, `resolve_media`, fuentes AVIF/WebP y filtros de imágenes de producto/categoría.

Eso no acredita un endpoint de transformación para R2/Sectionfy, avatares externos o portadas JPG del backend del blog. No se inventan sufijos ni parámetros de redimensionado para esos orígenes. En el blog, las imágenes suman aproximadamente 1,327 MB móvil; se observaron tres JPG de unos 501/315/299 KB. En Home se señaló una imagen de Sectionfy de 54 KB con ahorro estimado cercano a 49 KB: es una oportunidad estimada, no un ahorro implementado. La imagen ya es WebP y lazy, por lo que convertir el nombre de formato o añadir lazy no resuelve por sí solo el tamaño.

Imágenes cargadas cerca del viewport pueden ser precarga legítima del navegador; no se califican de innecesarias únicamente por estar debajo del fold. `naturalWidth` puede estar corregido por densidad/srcset: no se toma como prueba única del tamaño físico del archivo.

## Priorización y alternativas

| ID | Prioridad | Hallazgo y evidencia | Acción recomendada | Riesgo / prueba necesaria | Estado |
|---|---|---|---|---|---|
| RHP-0101 | P1 móvil | JS ≈1,732 MB reportados en Home, ~62%; score 49–86 con peso casi fijo | Aislar CPU por app/tag y su momento de inicialización; revisar lifecycle de la app de reseñas | Preservar eventos, reseñas visibles, consentimiento y compra; no borrar SDK desde el tema | Confirmado el coste/carga; solución needs_evidence |
| RHP-0102 | P1 móvil | La app solicita SDK y recursos repetidos; segunda respuesta del SDK viene de memoria | Revisar con configuración/proveedor qué provoca la segunda carga del iframe; contrastar reducción de ejecución | Un único SDK en DOM final no prueba doble init simultáneo. No usar deduplicación global a ciegas | needs_evidence para cambio |
| RHP-0103 | P1 móvil | Google/Meta/TikTok son relevantes en trazas previas; datos comerciales no verificados por bloquear POST | Auditar etiquetas/eventos reales y ventanas de consentimiento antes de diferir | Perder page_view, atribución o early-bounce; requiere pruebas comerciales autorizadas y control de GTM/apps | No modificar todavía |
| RHP-0104 | P1 desktop | MP4 7,689 MB, ~72% del peso reportado de Home desktop | Preparar una versión optimizada del mismo archivo y comparar calidad/transferencia conservando autoplay/controles | Sustituir contenido de Sectionfy requiere autorización específica; no beneficia el móvil inicial porque ya no descarga ese MP4 | Causa de peso confirmada; candidato por preparar |
| RHP-0105 | P1 blog | Tres portadas JPG explican buena parte del peso editorial | Optimizar originales en CMS/origen o usar variantes oficialmente soportadas cuando se verifiquen | Mantener calidad, alt, enlaces y prioridad de la primera portada; no aplicar filtros de productos a URLs arbitrarias | needs_evidence de transformación/originales |
| RHP-0106 | P2 imágenes | WebP R2 renderizado en card con resolución superior a la necesaria | Verificar variantes del origen; reutilizar picture/helper si hay URLs reales | No inventar srcset; ahorro Lighthouse solo estimado; medir currentSrc/red por dispositivo | Propuesto |
| RHP-0107 | P2 estabilidad | CLS desktop de Home bajo en este lote y guard del header presente | Conservar el cambio y vigilar peores casos por página | No reescribir header/video sin nueva regresión demostrada | Conservado |
| RHP-0108 | P3 metodología | Falta inventario de red del PDF; benchmarkIndex varía entre muestras Google | Mantener baseline por versión/perfil y diferenciar bytes reportados/red/caché | No atribuir variación a parches; benchmark no demuestra una causa única | Limitación registrada |

La primera intervención debe dirigirse a JS/apps y no a la eliminación indiscriminada de imágenes o marketing. La compresión del video es una oportunidad clara para peso desktop, pero es un frente separado y no una solución del TBT móvil.

## Permisos y condición para implementar

Se respetó la instrucción de usar únicamente Codex: no se invocó Claude ni CommandCode, no hay consenso ni revisión independiente simulada. Los cambios de alto riesgo mantienen pendiente la revisión adicional o aprobación humana correspondiente; no se desactivó ningún gate.

No hay diff desplegado ni parche aprobado en este informe. Antes de cualquier modificación remota: confirmar instalación enlazada y estado publicado, preparar diff exacto/asset candidato, hashes antes/después, respaldo recuperable y reversión acotada; ejecutar QA proporcional y solicitar autorización humana específica. El consentimiento general para analizar no autoriza publicar. Después de un despliegue autorizado se medirán varias muestras compatibles sobre producción, incluyendo funcionalidad comercial, SEO, accesibilidad y regresiones.

## Evidencia y archivos

- Originales y diagnóstico de producción: `reports/runs/rhino-performance/20261112T032758-production-weight-analysis-8a197fd8`.
- `analysis.json`: estadísticas completas y muestras con correspondencia de score/métricas, hashes y perfiles.
- `measurements.csv`: todas las observaciones válidas; marca repetidas sin eliminarlas del registro.
- `resource-breakdown.csv`: medianas por tipo de recurso y por página/dispositivo.
- `production-observation.json`: proyección acotada de verificación publicada; los artefactos completos quedan privados.
- Informes conservados: `adr009-followup.md`, `blog-release-validation.md`, `performance-renewal-20261111.md`.

## Candidatos de video preparados, sin desplegar

El original público se descargó una vez con límite de tamaño y sin seguir redirecciones. Original preservado: 7.688.530 bytes; H.264, 1920×1080, 24 fps, 20,416667 s, sin audio. Se prepararon dos alternativas H.264 con faststart, sin cambiar la resolución ni duración.

| Archivo | Bytes | Ahorro del archivo | SSIM global frente al original |
|---|---:|---:|---:|
| candidate-crf26.mp4 | 5,868,674 | 23.67% | 0.992423 |
| candidate-crf30.mp4 | 3,865,883 | 49.72% | 0.989410 |

SSIM cuantifica similitud de píxeles, no aprobación humana ni una mejora de PageSpeed. Los originales, candidatos, comandos y hashes están en el directorio privado `video-candidate/` de esta ejecución. No se eligió ni publicó ninguno. La sustitución del asset remoto requiere revisar calidad en movimiento, confirmar todos sus consumidores, respaldo del asset/configuración y autorización específica del propietario. No cambia el peso inicial móvil porque ese video no se descarga automáticamente allí.
