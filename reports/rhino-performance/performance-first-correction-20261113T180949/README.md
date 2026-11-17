# Rhino Performance — primera corrección de rendimiento preparada

Fecha: 2026-11-13. Estado: **candidato listo para decisión del propietario; no aplicado ni publicado**. Instalación publicada confirmada: **14828608**, tienda **7400935**, tema seccionable «RHINO - FAQ Categorias», versión 1.8.0. Se reutilizaron los informes históricos; no se repitió discovery, SEO V4, GSC ni la paginación.

## Decisión concreta

Proponemos diferir únicamente las mediciones automáticas de geometría de Google Reviews mientras el carrusel permanece lejos del viewport. Archivo único: `sections/google-reviews.tpl`. Se conservan HTML, CSS, schema, contenido inicial, consulta API inmediata y la función `setupMore` existente de dos pasadas. No se alteran etiquetas de marketing, Sectionfy, Swiper, `store.js`, fuentes ni diseño.

La API actualiza las reseñas inmediatamente; la geometría se prepara una vez cuando el componente entra en un margen de 600 px, recibe foco o pointerdown. Después sigue el comportamiento anterior de carga, render y resize. Si IntersectionObserver no existe o falla al registrarse, se conserva la medición síncrona original. No se ejecuta una lectura inicial de getBoundingClientRect.

**Beneficio comprobado:** evita las lecturas geométricas automáticas fuera de pantalla en el ensayo aislado. **Beneficio no comprobado:** mejora de Lighthouse, LCP, INP o tiempos de producción. No se afirma 90+ ni se traduce muestreo CPU en ahorro garantizado.

## Diez mediciones actuales de producción

Home `https://rhino-performance.com/`, cinco muestras por dispositivo, alternadas, navegador/caché nuevos, sin elección de consentimiento. Lighthouse **13.6.0**, Chrome **155.0.8059.84**, configuración simulada. Mobile: 412×823, DPR1.75, CPU4×, RTT150ms, throughput1638.4kbps. Desktop: 1350×940, DPR1, CPU1×, RTT40ms, throughput10240kbps. Perfiles completos, fechas, hashes y referencias a originales en [lighthouse-statistics.json](lighthouse-statistics.json); muestras sin combinar métricas entre ejecuciones en [CSV](lighthouse-ten-samples.csv).

**Limitación importante:** el benchmark del host varió de 1977 a 842 durante el lote; desktop también de 1862.5 a 848.5. Cambió el rendimiento efectivo del equipo. La causa concreta no está demostrada. Las observaciones se conservan completas, pero no constituyen una comparación estable antes/después ni permiten atribuir diferencias históricas a la tienda o al último parche. No se descartaron muestras ni se consumieron navegaciones adicionales para elegir un score favorable.

| Dispositivo | Mediana score (mín.–máx.) | Media score ± DE poblacional | LCP mediana | FCP mediana | TBT mediana | CLS mediana | SI mediana | Peso mediana |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| mobile | 52 (47–61) | 54.2 ± 5.1 | 4.41 s | 1.91 s | 2751 ms | 0.000329 | 4.18 s | 2.315 MB |
| desktop | 54 (46–84) | 60.8 ± 13.4 | 2.51 s | 0.60 s | 771 ms | 0.052716 | 2.38 s | 2.542 MB |

Las medianas de métricas son estadísticas separadas, no una ejecución sintética. MB decimal = 1.000.000 bytes.

| Muestra | Performance | LCP s | FCP s | TBT ms | CLS | SI s | MB transferidos | Benchmark host |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| mobile 1 | 52 | 4.56 | 2.03 | 2295 | 0.000335 | 4.18 | 2.316 | 1977 |
| desktop 1 | 84 | 2.03 | 0.44 | 169 | 0.068028 | 1.41 | 2.544 | 1862.5 |
| mobile 2 | 61 | 3.21 | 1.91 | 2751 | 0.000329 | 3.92 | 1.843 | 1915 |
| desktop 2 | 67 | 3.08 | 0.97 | 248 | 0.061327 | 2.27 | 2.492 | 1870 |
| mobile 3 | 59 | 3.64 | 1.76 | 2522 | 0.000335 | 3.71 | 2.315 | 1792.5 |
| desktop 3 | 54 | 2.51 | 0.60 | 771 | 0.052716 | 2.44 | 2.542 | 1530.5 |
| mobile 4 | 52 | 4.41 | 1.77 | 4108 | 0.000329 | 4.22 | 2.315 | 1009 |
| desktop 4 | 53 | 2.31 | 0.55 | 986 | 0.052716 | 2.44 | 2.070 | 927.5 |
| mobile 5 | 47 | 4.71 | 2.20 | 6011 | 0.000329 | 5.19 | 2.315 | 842 |
| desktop 5 | 46 | 3.35 | 0.93 | 1003 | 0.052716 | 2.38 | 2.542 | 848.5 |

El JSON estadístico incluye mínimo, máximo, media, mediana, rango y desviación estándar de cada métrica. No se equiparan estas mediciones locales con PageSpeed ni CrUX. No hubo nuevas consultas PSI/CrUX; no hay INP de campo nuevo. Los baselines históricos 64/87 y las respuestas PSI de otros días/perfiles no se utilizan para atribuir una regresión.

Todas las muestras registran accesibilidad97, SEO100 y best-practices77. Son scores de auditoría, no certificación AA, ausencia total de defectos o confirmación de indexación. POST bloqueado impide certificar analítica, conversiones o compras.

## Peso y JavaScript

En la primera muestra móvil se transfirieron 2.316 MB: scripts1.439 MB, imágenes0.531 MB, CSS0.141 MB, documento0.117 MB, fuentes0.031 MB, otros0.056 MB y media0. Desktop primera muestra: 2.544 MB, scripts1.439 MB, imágenes0.758 MB, CSS0.141 MB, documento0.117 MB, fuentes0.031 MB, otros0.056 MB. La fila third-party del auditor es una clasificación transversal y no se suma de nuevo.

No hay una comparación metodológicamente equivalente que demuestre aumento o reducción frente a los 2.49 MB del PDF. El banner actual es una imagen AVIF, mientras existen informes históricos de video y contenido diferente. El candidato agrega **1.035 bytes de fuente sin comprimir**; no reduce las descargas de terceros ni elimina recursos. La transferencia real del archivo compilado/comprimido queda pendiente de publicación autorizada.

El coste Lighthouse de inicio JavaScript tiene mediana5097ms móvil y1859ms desktop, afectado también por el host. Coverage de la sesión CDP observó 4.319.224 caracteres de fuente JS y1.431.353 usados en móvil; desktop4.360.448 y1.384.713. Son rangos de código fuente, no bytes transferidos ni permiso para eliminar el resto.

## Dos trazas y cinco prioridades

Se usó CDP mediante el runtime Puppeteer existente; no se utilizó un MCP DevTools conectado. Dos sesiones reales, una por dispositivo, sin nuevas navegaciones adicionales: mobile412×823/DPR1.75/CPU4×/red150ms y1638.4kbps; desktop1440×900/DPR1/CPU1×/40ms y10240kbps. Ventana inicial20s tras DOMContentLoaded, seguida de scroll en la misma sesión. Coverage y CPU profiler añaden instrumentación: estos tiempos no se mezclan con Lighthouse. Fuentes en `reports/runs/rhino-performance/20261113T180949-home-performance-authorized-e593dae0/trace-summary.json` y [trace-findings.json](trace-findings.json).

1. **Marketing: Google Tags, Meta y TikTok.** Muestras de CPU dentro de las colas de tareas largas móviles: gtag775.7ms, fbevents458.2ms, TikTok303.2ms; Clarity200.9ms. Iniciadores y URLs están conservados en Network. Esto acredita actividad durante carga, no duplicación de eventos ni ahorro obtenible. No hay aún una alternativa diferida probada que preserve atribución/consentimiento; no se tocan configuraciones remotas.
2. **Google Reviews fuera de pantalla.** Una instancia, diez tarjetas, raíz a2413px móvil y2892px desktop. `setupMore`, script inline Home línea16863, lee overflow y prepara Leer más en init, respuesta API, load y resize aunque no sea visible. CPU asociado en cola258.1ms móvil/82.3ms desktop. No equivale a ahorro causal. El candidato único aborda este trabajo evitable; la reproducción aislada acredita el mecanismo y la equivalencia tras activarse.
3. **Código nativo de plataforma y colección destacada.** `vanilla-adapter-0.40.0.min.js` y `linkedstore-v2` acumulan310.8ms y256.4ms de muestreo en colas móviles. Desktop `featured-collection…js:check`, línea141,49.6ms. No se ha demostrado una corrección segura ni que Coverage permita retirarlos; quedan separados del parche.
4. **LCP: recurso y descubrimiento según dispositivo.** CDP observó móvil2.100s: AVIF820 del banner BFM,32.242 bytes, eager/fetchpriorityhigh; desktop1.880s: AVIF1920 del banner BF,31.735bytes, inicialmente lazy sin prioridad alta. Es una posible oportunidad desktop a investigar, no justifica añadir preload sin un ensayo. En móvil `setupMore` se muestreó después del LCP observado: no se presenta como causa de ese LCP. No se observó descarga de video en el resource-summary de estas muestras.
5. **Recursos externos adicionales y posible duplicidad.** El SDK `bzrcdn.openai.com/sdk/oaiq.min.js` registra197.8ms de muestreo en colas móviles y una descarga de≈37KB iniciada desde un script inline de Home. No se ha confirmado su emisor o necesidad, y no se atribuye automáticamente al entorno de pruebas ni se propone eliminarlo. El script de Google Reviews aparece en dos solicitudes; caché/iframe/iniciador deben distinguirse antes de llamarlo doble descarga o doble inicialización. No hay permiso ni evidencia para cambiar estos recursos en este lote.

Se observaron26 tareas largas móviles y12 desktop; suma de exceso sobre50ms dentro de esa ventana:4002ms y538ms. **No son TBT de Lighthouse ni INP.**

## Alternativas y consejo dual

Propuestas independientes reales de Claude y Codex, un contraste cruzado y una defensa final; sin CommandCode, sustituciones ni reinicio del consejo. Modelos registrados balanced: Claude Sonnet5.5 y GPT6.1sol, esfuerzo medium. Contratos y recibos ligados a hashes en [council-final-receipts.json](council-final-receipts.json).

Se comparó con coalescing vía rAF: seis repeticiones alternadas por variante a390 y1440px. En el fixture de24 tarjetas, baseline24 lecturas síncronas; coalescing0 síncronas pero24 tras el frame; candidato0 también tras el frame mientras sigue fuera de pantalla. Medianas init móvil4.60/1.15/1.35ms y desktop5.80/1.05/1.35ms, respectivamente. Esto favorece evitar trabajo innecesario; no demuestra que el gate sea más rápido en todo escenario. Se retiró la lectura inicial del rectángulo propuesta por Codex; Claude aceptó evitar dirty/fonts.ready adicionales porque el primer cálculo usa el DOM vigente y los listeners posteriores se conservan.

Claude revisó independientemente el diff exacto final y no encontró objeciones críticas abiertas. Ambos consideran el candidato presentable al propietario para un despliegue controlado de un archivo. Esa opinión no sustituye QA ni autoriza publicar.

## QA realizado y límites

**163 comprobaciones aisladas aprobadas:**144 principales+19 suplementarias, sin solicitudes externas. Seis anchos360/390/768/1024/1440/1920; captura final idéntica entre variantes en los seis anchos, sin máscaras, en fixture determinista con fuenteArial. API inmediata antes y después de activar, respuesta vacía,0/1/24/100 tarjetas, resize, flechas, Enter/Space, foco, Tab temprano hasta Leer más, pointerdown antes de IO, dos instancias, ausencia/excepción de IO. Axe del componente a390/1440 no halló violaciones; no certifica la tienda completa.

Reinicializar todo el componente conserva un defecto basal de doble toggle; no se declara idempotente ni se reescribe fuera de alcance. Los estados finales arriba del pliegue y después de cambiar fuente se comprobaron, pero no la ausencia de un primer frame transitorio con Poppins. No se simula Twig real ni la página completa en producción.

**Validación nativa autorizada:** GET de instalación, GET de file-hashes y un POST exacto de validación; HTTP200, `valid:true`, `errors:[]`. Se validó exclusivamente el hash final de este archivo. Cero PATCH/PUT/DELETE, cero guardados. [Recibo](native-validation-receipt.json). Prueba sintaxis/schema, no render. La CLI inicialmente ejecutada desde el repositorio no encontró configuración; no hubo GET exitoso hasta corregir el cwd del tema; la operación de lectura autorizada permanece documentada sin reintento de error HTTP.

**Riesgos que permanecen:** IO asíncrono si en el futuro la sección se mueve arriba del pliegue; margen600px sin umbral óptimo medido; posible traslado de trabajo al acercarse con scroll rápido; observer sin desconexión explícita al retirar una raíz aún no activada; impresión sin scroll no prepara has-more; margen IO limitado en iframes de otros orígenes. No se han demostrado regresiones críticas actuales, pero deben vigilarse en QA real. Ninguno acredita mejora de INP.

## Archivo, respaldo y autorización

- Archivo único: `sections/google-reviews.tpl`.
- SHA256 publicado/base: `75a487600c5d71001fa2e0970dad1cb943f80d399f1af89db559bffc3253fd30`.
- SHA256 candidato: `e6f79c2fd59376efe955662adff44d13329300360a118249c88480d59dde3cd3`.
- SHA256 diff: `2c88fb0d3e619b5d08c8e217eecb9e104d9d402dbe47997c95b91f0e4b1c8d32`.
- Tamaño fuente:23.382→24.417bytes.
- Respaldo obtenido mediante GET nativo: `reports/runs/rhino-performance/20261113T180949-home-performance-authorized-e593dae0/remote-before/sections/google-reviews.tpl`; íntegro e igual al tema local.
- [Diff completo](candidate.patch) · [Manifiesto](candidate-manifest.json) · [ADR](ADR.md) · [Solicitud exacta](authorization-request.md).

No se modificó el tema local externo ni producción. Los cambios SEO previos ajenos del repositorio permanecieron intactos. `implementation_allowed` sigue **false** por ausencia de permiso de publicación. `needs_evidence` se conserva para render/QA real y beneficio de rendimiento posterior; no se fuerza un gate global a pass por aprobar las pruebas aisladas.

La publicación futura debe reconfirmar instalación, hashes remotos y respaldo; detenerse si cambió la base, enviar solo un archivo y comprobar el hash final. La reversión también requiere autorización específica y debe detenerse si aparecen cambios posteriores ajenos. QA posterior y nuevas cinco mediciones por dispositivo requieren alcance de lectura nuevo: las diez mediciones actuales ya consumieron su autorización. Véase [QA y reversión](QA-AND-ROLLBACK.md).
