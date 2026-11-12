# Rhino Performance: nueva línea base y diagnóstico — 11 noviembre 2026

Estado: **parcial; `needs_evidence`, sin aprobación de implementación**. Proyecto `rhino-performance`, origen medido `https://rhino-performance.com/`, assets de instalación 14828608. No es DaMar Beauty. No se modificó ningún archivo del tema ni se ejecutó push/watch/publish.

## Resultado principal

**Home: mediana 64 móvil y87 escritorio; objetivo90 no alcanzado.** Se ejecutaron32 muestras Lighthouse nuevas: cinco por dispositivo para Home, presoterapia y PRO AIR; una exploratoria por dispositivo para blog. No se garantiza PageSpeed90 a partir de Lighthouse local.

La traza móvil identifica trabajo importante de Google Tag/Analytics, Meta y TikTok. No respalda reescribir Sectionfy/Swiper. El encabezado provoca un desplazamiento de74px en escritorio al cambiar de flujo normal a absoluto; una propuesta CSS evita ese desplazamiento en una prueba temporal de navegador, pero sigue sin aprobación completa para aplicarse.

## Métricas originales resumidas

| Página | Dispositivo / n | Performance mediana (mín–máx) | LCP s | FCP s | TBT ms | CLS | Speed Index s |
|---|---|---|---|---|---|---|---|
| home | mobile / 5 | 64 (58–67) | 3.26 | 1.70 | 1694 | 0.0004 | 3.43 |
| home | desktop / 5 | 87 (65–89) | 0.99 | 0.42 | 164 | 0.0682 | 2.44 |
| category | mobile / 5 | 61 (59–74) | 3.69 | 1.33 | 1721 | 0.0000 | 3.14 |
| category | desktop / 5 | 94 (89–96) | 1.26 | 0.37 | 133 | 0.0305 | 0.95 |
| product | mobile / 5 | 60 (58–64) | 3.54 | 1.64 | 1991 | 0.0000 | 3.73 |
| product | desktop / 5 | 94 (91–95) | 1.08 | 0.50 | 142 | 0.0751 | 1.15 |
| blog | mobile / 1 | 47 (47–47) | 6.56 | 1.71 | 1491 | 0.0000 | 4.77 |
| blog | desktop / 1 | 84 (84–84) | 2.21 | 0.98 | 90 | 0.0416 | 1.88 |

Blog tiene n=1: no permite estimar variabilidad ni demostrar regresión. Medianas, mínimos/máximos de cada métrica, desviación estándar de scores, muestras fechadas y perfiles están en [baseline](performance-baseline-20261111.json). Los scores se calculan desde las muestras: el resumen histórico del servicio conserva el score de su primera muestra y no se interpreta como mediana.

Páginas seleccionadas: Home por hero/Sectionfy/header; `/presoterapia/` por listado comercial principal; `/productos/botas-presoterapia-inalambricas-pro-air/` por galería/variantes/video; `/blog/` por componente editorial. No se inspeccionaron todas las categorías, PDP, artículos, búsquedas y estados comerciales como si esta muestra fuera cobertura total.

## Condiciones y comparabilidad

Lighthouse 13.6.0 y Chrome 155.0.8059.84; fuente `lighthouse_local`, simulación, caché reiniciada y navegador nuevo por muestra. Móvil412×823, DPR1.75, CPU4×, RTT150ms/1638.4kbps. Escritorio1350×940, DPR1, CPU1×, RTT40ms/10240kbps. Los parámetros completos, categorías, locale y entorno observado se conservan en los originales. Ejecuciones secuenciales; trazas y QA fuera de las32 muestras. El entorno anfitrión compartido no garantiza carga ambiental idéntica.

Política `guarded-read-only`: GET/HEAD/OPTIONS, sin enviar formularios, compras, cookies privadas ni cambios de consentimiento; POSTs de tracking/transacciones bloqueados. Esto limita la certificación comercial y puede diferir del navegador de un cliente. La CPU física4× de la traza diagnóstica **no equivale** a la simulación de Lighthouse.

Referencia histórica Home: móvil30/LCP15.73s/TBT1587ms/CLS0.0066 y escritorio71/LCP1.09s/TBT113ms/CLS0.449. El comparador existente devuelve `not_comparable` por distinto número de muestras (3 frente a5). Se conservan ambos perfiles y resultados; no se afirma significancia ni causalidad del último parche. Cambió el contenido del hero y pueden variar terceros/servidor.

La comprobación HEAD de `https://www.rhino-performance.com/` devolvió403; se detuvo sin reintentos. El origen canónico sin www ya estaba autorizado y en medición, responde200. No se interpreta el403 de esta herramienta como prueba de bloqueo a Googlebot.

## PageSpeed, CrUX y MCP

PageSpeed y CrUX: referencias configuradas, claves **ausentes del entorno de esta sesión**; seis lecturas del servicio devolvieron `credentials_unavailable`, con0 intentos HTTP. No hay resultados API nuevos ni se convierte falta de autenticación en `insufficient_field_data`.

El [informe integral anterior](integral-audit.md) conserva PSI y CrUX fechados. Periodo CrUX histórico12oct–8nov2026: origen móvil LCP1.91s/INP112ms/CLS0.01; escritorio1.74s/65ms/0.06. Son métricas de **origen**, no datos actuales de cada URL. Home de URL carecía de LCP/INP en esa consulta. No se inventa INP desde TBT ni se promete mejora inmediata de CrUX.

Chrome DevTools MCP no está conectado en este runtime. Se usó Chrome/CDP/Puppeteer explícitamente, no un MCP simulado.

## Causas comprobadas y límites

**RHINO-NOV11-01 — P1 móvil: JavaScript de medición.** En una traza móvil con CPU física4× y red emulada,19 tareas largas produjeron1566ms de exceso sobre50ms durante una ventana de18.69s. El muestreo alineado por reloj asignó aproximadamente404.8ms de colas a gtag,280.9ms a fbevents,94.0ms a configuración de Meta y154.7ms a TikTok:934.4ms de unos1568ms muestreados. Es atribución de esta captura, **no el TBT oficial de Lighthouse**, no un porcentaje universal ni una predicción de puntos. Clarity aportó55.8ms muestreados en colas. Hay trabajo de plataforma, inline y nativo sin atribuir completamente. Sectionfy, store.js y varios carruseles no presentaron muestras en esas colas; no se concluye coste cero en todos los estados.

Acción: revisar propietarios, duplicidad real de eventos y triggers de tags con un contrafactual local repetido, manteniendo funcionalidad/consentimiento. GTM/plataforma/apps no se modificaron: cambiar sus políticas remotas requiere autorización específica y pruebas de medición/comercio. No se eliminan tags por Coverage.

**RHINO-NOV11-02 — P1 escritorio: header cambia de flujo.** En1024/1440/1920, MAIN pasa de y110 a y36 cuando `initTransparentHeader` activa `position:absolute`; altura final del header74px y del hero750px. A/B de12 contextos: el candidato CSS mantiene MAIN en y36 desde su primera geometría observada y conserva header/hero/fuentes finales en seis anchos; móvil no cambia. Fuente candidata: `static/css/style-critical.css`; consumidores: Home con video inicial y header configurado, sin alterar el JS comercial. La prueba no explica el pico CLS1.0045 ni demuestra un score nuevo. El [diff propuesto](header-initial-flow-candidate.patch) está **sin aplicar**. Falta aceptación completa y procedencia de template/CSS compilado para cerrar las objeciones del consejo.

**RHINO-NOV11-03 — P1 blog: LCP móvil6.56s**, una muestra. Requiere cinco muestras si pasa a prioridad, atribución del recurso y comparación con el parche de blog existente. No se revierte la mejora anterior por una observación.

**Imágenes/video/LCP.** El LCP de Home actual es la foto de respaldo del hero; está en HTML inicial, sin lazy y con prioridad alta. No hay evidencia para añadir otro preload. En la observación móvil no se solicitó MP4 antes de Play; en escritorio el MP4 se reproduce, pero su solicitud no había terminado al cerrar aquella ventana:0 bytes completados no significa0 bytes transferidos. El tamaño7.69MB documentado en la integración previa es una observación anterior del archivo, no una nueva medición de transferencia de esta auditoría. Preservar reproducción condicional, visibilidad y reduced motion. No se redujo resolución ni tipografía.

Una muestra Lighthouse de Home móvil registra135 solicitudes,2.34MB totales y1.48MB de scripts; es esa muestra, no un presupuesto universal. Los tiempos de descarga, LCP simulado y desglose de traza conservan metodologías distintas; no se fuerzan a sumar.

### Contrafactual repetido: contribución de Google Tags

Seis capturas móviles adicionales de diagnóstico, alternadas y con una ventana de análisis fija0–20s, CPU física4×, misma red/caché y contexto anónimo. CDP bloqueó exclusivamente `www.googletagmanager.com` en tres casos; no hubo cambios en el servidor ni en el tema.

| Variante | n | Exceso de tareas largas, mediana (mín–máx) ms |
|---|---|---|
| Normal | 3 | 2022 (1914–2027) |
| Google Tags bloqueados solo en el navegador de prueba | 3 | 1356 (1341–1478) |

Diferencia descriptiva666ms en esa ventana, aproximadamente33%. Las capturas bloqueadas no tuvieron muestras de CPU de Google Tags. Se midió una intervención diagnóstica con tracking deliberadamente incompleto: **no es una optimización entregada, un TBT oficial ni un score admisible para producción**. No se usa como comparación de regresión con distinto perfil de recursos. n=3 no demuestra una distribución estable ni garantiza ahorro tras reconfigurar los tags. Tampoco demuestra que haya eventos duplicados. El SDK oaiq aparece dinámicamente, sin referencia encontrada en los archivos revisados; no se le atribuye un propietario sin analizar su iniciador.

El seguimiento comercial y el consentimiento requieren su propio QA: los POST permanecen bloqueados y no se ha certificado entrega de eventos. El backlog anterior que proponía este contrafactual queda parcialmente satisfecho por el diagnóstico de Google; Meta/TikTok/otros y una solución que conserve medición siguen pendientes.

## Accesibilidad, SEO y estados

Axe en Home390/1440 detecta contraste2.84:1 del precio anterior (#999 sobre blanco; esperado4.5:1). No se detectaron botones/enlaces/combobox sin nombre en las muestras AX. DOM:3614/3716 nodos en aquellos estados; reducir nodos no equivale a mejorar accesibilidad. El H1 de tienda existe con `display:none`, también sin JS: su presencia no lo hace un encabezado accesible de contenido.

Seis anchos:360/390/768/1024/1440/1920. Se observó overflow en1024/1440; causa todavía no identificada, sin `overflow:hidden` global. Se conservaron capturas y traza de escritorio. Teclado:12Tab por ancho en diagnóstico y80Tab adicionales en cuatro estados del candidato; algunos focos con geometría cero requieren inspección, no se certifican como aprobados. Las12 comprobaciones de elegibilidad CSS (Home/otro template, flag apagado, runtime presente, video no inicial, no video, móvil/escritorio) pasaron; esto no certifica todo el comportamiento del tema.

Sin JS en390/1440 hay foto fallback y15 destinos de producto en HTML; no se promete indexación. Lighthouse SEO:100 Home/categoría/blog,92 PDP. Los dos anchors señalados en PDP son controles `.js-play-native-button`, no páginas de producto perdidas; no se les inventaron URLs. JSON-LD inicial de Home se parseó sin errores en el probe; no hubo auditoría completa de consistencia de catálogo ni nuevos schemas. No se enviaron formularios ni se certificó checkout/carrito real.

## Consejo y decisión

Claude y Codex generaron propuestas independientes; después contraste y defensa reales:6 preguntas,6 respuestas,14 objeciones. Se preservan propuestas, cambios de preferencia y metadatos en [consejo](performance-renewal-council.json). Autenticación de Claude e inferencia confirmadas; CommandCode deshabilitado. Hubo tres rechazos semánticos de referencias del harness, sin JSON malformado: se corrigió la correspondencia de rutas originales ya verificadas, conservando respuestas y fallos originales, sin modificar propuestas ni conceder escritura. No se repitió una propuesta válida ni se contó una revalidación como nueva invocación.

Ambos prefieren atribución de TBT antes de una intervención indiscriminada. La actualización acotada con CPU y A/B rechaza reescribir Sectionfy/Swiper y mantiene el CSS del header como `needs_evidence`. El controlador exige restricciones/recibos, no consenso verbal: `implementation_allowed=false`. La autorización local del propietario existe; el bloqueo es técnico, no una solicitud nueva de permiso.

Ocho invocaciones reales, modelos/esfuerzo y tiempos registrados. Suma de duración por llamada294.1s (incluye llamadas paralelas; no es tiempo de pared). Coste comunicado por Claude:USD1.6317; Codex no devolvió coste monetario, por lo que no hay coste total exacto. Tokens por proveedor se conservan sin equiparar sus contadores de caché.

## Backlog y gates

P0: ninguna regresión comercial crítica comprobada. P1: atribución/contrafactual de tags, aceptación del candidato de header y blog si se prioriza. P2: contraste, encabezado accesible y overflow demostrado. P3: activar un gate estadístico probado con una pareja antes/después real.

La [política de gates](regression-gates.json) continúa **propuesta, sin hook automático activo**. Hay baseline5 para tres plantillas; blog solo1. El comparador bloquea perfiles incompatibles, pero su lista de deltas positivos no es un contraste estadístico ni debe bloquear ruido. No se afirma protección permanente por existir el JSON. El siguiente gate debe usar tolerancia explícita, muestras repetidas y ajuste por múltiples métricas; estados passed/regression_detected/inconclusive/insufficient_evidence/blocked. No se programaron cuotas, cron ni tareas externas.

## Evidencia y reproducción

Pruebas offline del motor de rendimiento: **47 tests pasaron**; no son conectividad API ni QA del tema.

Originales locales ignorados por Git: `reports/runs/rhino-performance/20261111T203215-renewed-performance`. Incluyen32 muestras, perfiles, comparaciones, red/LCP/CLS, dos trazas iniciales más seis del contrafactual, CPU profiles, capturas, A/B, pruebas sin JS y recibos de ejecuciones. El manifiesto de hashes está en `evidence-sha256.json` dentro del run; [JSON resumido](performance-renewal-20261111.json) y [ADR](ADR-RHINO-009.md) enlazan las decisiones. Los seis archivos del checkpoint permanecen iguales por hash y no se sobrescribieron cambios ajenos.

Para una auditoría nueva equivalente con la herramienta existente:

```bash
python3 tools/ia.py --project rhino-performance performance local --url https://rhino-performance.com/ --device mobile --runs 5 --allow-network
python3 tools/ia.py --project rhino-performance performance local --url https://rhino-performance.com/ --device desktop --runs 5 --allow-network
```

El lote de esta ejecución guardó cada muestra por separado; un fallo de sobrescritura del checkpoint fue corregido y se reanudó sin repetir las muestras válidas. No hay antes/después de un cambio aplicado, ni PageSpeed90 confirmado, ni aprobación de producción.
