# RHINO — Home, rendimiento avanzado y estabilidad

Fecha de consolidación: 2026-11-11T00:04:35.828205+00:00. Página medida: https://rhino-performance.com/ (origen registrado sin www). Prioridad operativa: **Home móvil**, protegiendo desktop. Referencia pública de assets14828608. Código local limpio al iniciar: `2e8c13aefd7b346943e928aee8e598f69dd47374`. **Diagnóstico de lectura: ningún cambio del tema, push o publicación.**

## Resultado principal

La Home todavía no alcanza90. Los cuellos de botella difieren por dispositivo: **trabajo del hilo principal en móvil y estabilidad visual en escritorio**. Se conservan las mejoras del blog, accesibilidad y pausa condicional ya existentes. No se hizo otro discovery.

| Home / fuente | Performance | LCP | FCP | TBT | CLS | Speed Index |
|---|---:|---:|---:|---:|---:|---:|
| Lighthouse local móvil, mediana3 actual | 53 | 4.25s | 1.91s | 3105ms | 0.0003 | 3.84s |
| Lighthouse local desktop, mediana3 actual | 64 | 1.22s | 0.61s | 282ms | 0.449 | 1.41s |
| PageSpeed móvil, histórico10nov19:13UTC, n1 |85|3.74s|1.36s|190.5ms|0.045|3.80s|
| PageSpeed desktop, histórico10nov19:14UTC, n1 |70|0.88s|0.33s|828.5ms|0.053|1.49s|

No son cuatro muestras de un mismo entorno. **No hay PageSpeed nuevo**: las referencias a claves están configuradas, pero sus valores no están en este proceso. Los informes Google anteriores existen, provienen de llamadas reales y son los más recientes guardados para la Home; no se presentan como validación del último push.

En la nueva serie móvil, LCP3.24–4.32s y TBT2.71–3.11s; desktop LCP1.16–1.27s, TBT237–382ms y CLS0.449 en3/3. La serie local anterior era65móvil/74desktop, LCP3.17/0.97s y TBT1584/164.5ms. El comparador reconoce perfiles compatibles, pero **no acredita una regresión causada por código**: n3, sin candidato controlado ni aislamiento de cambios de terceros/red. No se revierte nada por esta diferencia.

## Procedencia y reproducibilidad

Chrome 155.0.8059.84, Lighthouse 13.6.0, cuatro categorías, localees. Móvil412×823/DPR1.75, CPU×4, RTT150ms/1638.4Kbps; desktop1350×940/DPR1, CPU×1, RTT40ms/10240Kbps. Simulación Lighthouse, almacenamiento/caché reiniciados por muestra, sesión anónima sin aceptar ni rechazar consentimiento. Solo lectura: POST bloqueado, ningún formulario o carrito enviado. Eso puede alterar aplicaciones/video y debe conservarse al comparar.

Los cinco valores LCP/FCP/CLS/TBT/Speed Index están presentes y son numéricos en las seis muestras. Se recalculan medianas desde `samples`: el resumen histórico del servicio conserva el score de la primera muestra y **no se interpreta como mediana**. Los 40 tests existentes de extracción/contratos pasaron; son offline, no nuevas consultas Google.

Los339hashes verificables de342archivos del inventario siguen iguales. Los3hashes de rutaspassword fueron redactados por el serializador y no pueden cotejarse directamente; Git conserva el mismoHEAD y árbol limpio, sin indicios de modificaciones. Las huellas MD5 en URLs de cinco assets publicados coinciden con los archivos locales en ambas vistas. Es verificación de esos assets, **no una certificación completa del render Twig ni del contenido CMS**.

## CrUX y métricas faltantes

Periodo real guardado12oct–8nov2026. Home por URL devuelve cobertura **parcial**: CLS p75=0.00móvil/0.05desktop y FCP1525/1159ms, pero **faltan LCP e INP** en ambos. Para esas métricas: `insufficient_field_data`, no cero ni error de Lighthouse.

| Origen, no URL | LCP p75 | INP p75 | CLS p75 | FCP p75 |
|---|---:|---:|---:|---:|
| Mobile |1908ms|112ms|0.01|1518ms|
| Desktop |1742ms|65ms|0.06|1138ms|

El origen histórico tiene buenos p75, pero no sustituye a la Home ni demuestra el efecto de un push. No se deduce INP del TBT. Las APIs respondieron anteriormente; su conectividad actual no se reprobó sin claves. [Metodología oficial CrUX](https://developer.chrome.com/docs/crux/methodology).

## LCP, recursos y causas

**LCP de Home:** `img.image-priority-high.video-block-image`, póster `img.youtube.com/vi_webp/we6rl2Q8AxI/maxresdefault.webp`, unos30969B. Ya tiene `src`, descubrimiento inicial, carga inmediata y prioridad alta. No necesita una solución nueva de lazy ni otro preload indiscriminado.

El MCP nuevo hizo7llamadas reales. Su traza desktop independiente, sin el perfil simulado de Lighthouse, observó LCP410ms: TTFB88, retraso de carga51, duración46 y retraso de render225ms. Esos tiempos describen **esa traza**, no explican porcentajes de los4.25s móviles. El inspector Lighthouse móvil estima1011ms de ahorro en recursos bloqueantes; es estimación, no ahorro final garantizado ni sumable con otras oportunidades. [Guía oficial de diagnóstico de LCP](https://web.dev/articles/optimize-lcp).

En la primera muestra Lighthouse móvil:10.7s de trabajo del hilo principal, ~4.97s de evaluación de scripts, ~2.06s de estilo/layout y ~0.63s de parseo/compilaciónJS. El coste por función/integración todavía requiere atribución de tareas: no se asigna todo a marketing o a un único archivo.

Los valores de CPU por host también se conservaron como medianas de las3muestras (no son contribuciones al TBT ni ahorros al retirar un script):

| Host / grupo | Evaluación JS mediana |
|---|---:|
| www.googletagmanager.com | 809ms |
| connect.facebook.net | 845ms |
| analytics.tiktok.com | 476ms |
| scripts.clarity.ms | 409ms |
| nsk-cdn-static.tiendanube.com | 654ms |

No se concluye que el TBT solo se resuelva tocando terceros. El código del documento y las bibliotecas nativas también consumen CPU; se necesita localizar funciones y disparadores antes de elegir el primer parche.

En la ventana CDP móvil390px, antes de axe/scroll: **JS1119557B, CSS58312B, imágenes366940B, fuentes31380B**,3679elementos y profundidad21. Desktop1440px: JS1126374B, CSS58313B,3784elementos, profundidad21 y scrollWidth1507. Estas ventanas, subframes y condiciones difieren de Lighthouse; no se mezclan sus totales ni tareas con TBT simulado.

Los recursos externos móviles más pesados observados incluyen WebP144262/74233/54521B; la imagen144KB **no es el póster LCP**. Investigar consumidores, `sizes`, DPR y `currentSrc` antes de recomprimir o sustituir. No hay prueba suficiente para afirmar que todas las versiones mobile/desktop se descargan dos veces. Preload+stylesheet para critical/utilities es visible en HTML; sus eventos de red se conservan por URL y no se equiparan a dos descargas.

GTM/gtag, Meta, TikTok, Clarity, apps de reseñas, plataforma y código propio requieren separar propietarios, disparadores y tareas. Ver ambos scriptsGTM/gtag no prueba eventos duplicados. El ensayo histórico de bloquear marketing bajaba TBT1584→660.5ms pero empeoraba LCP3171→3747ms: **no es una optimización aprobada**. No se eliminan eventos, LS, vanilla-adapter o bibliotecas por peso/Coverage. El Coverage nuevo es solo de scroll tardío, deliberadamente incompleto, sin permiso para eliminar recursos.

## Video, CLS y reflow

El CLS desktop0.449 se repite en todas las muestras. Lighthouse muestra indicios de `head > link`/imagen sin tamaño y subtotal de documento~0.068; el MCP nuevo vuelve a identificar un cluster0.3563 sobre `VIDEO.video-stream.html5-main-video`, sin causa raíz identificada. No se suman esas fuentes ni se promete resolverlo con dimensiones de cards. Hace falta correlacionar frame, geometría, inserción y aplicación de estilos en una navegación comparable.

La traza atribuye13ms de reflow a `featured-collection.js:141` y~3ms a `media-visibility.js:22`, además de otras pilas anidadas. Es evidencia para revisar orden de lecturas/escrituras, **no una explicación de3.1sTBT**, y no se suman pilas solapadas.

El código actual conserva observación de visibilidad, `document.hidden`, reduced motion, saveData y controles de reproducción. En mobile no se creó iframeYouTube antes de interacción. En desktop se observó el reproductor antes/después de scroll y pestaña oculta, pero su VIDEO permaneció `paused=true,time=0,readyState=0`: **no demuestra transición reproducción→pausa efectiva**. El bloqueo de POST puede influir. No se retira autoplay desktop ni se duplica su controlador para mejorar un score.

## Accesibilidad, UI y SEO

Lighthouse actual: **97/100 de accesibilidad y100/100SEO**, ambos perfiles; no equivalen a certificaciónWCAG o indexación. AX390px:1835nodos/1136expuestos;1440px:2016/1251; sin nombres vacíos entre controles/link expuestos detectados. Axe confirma contraste2.84:1 del precio anterior gris#999 sobre blanco enambas vistas. Conserva además verificaciones incompletas de ARIA/IDs/contraste que requieren revisión; no son pases automáticos.

Prueba de teclado nueva: menú mobile visible, foco permanece en disparador al abrir, Tab llega a Buscar fuera del panel y Escape no lo cierra. Revisar contrato de modalidad antes de adaptar el motor nativo. El overflow desktop1507/1440 también sigue pendiente; no se oculta globalmente. No se envió búsqueda, carrito ni compra.

El HTML inicial conserva canonical, H1 y enlaces; JSON-LD se inspeccionó sintácticamente. Los problemas históricos Product/Offer vs precio visible enPROAIR/baterías siguen separados y **no corregidos**: modificar esquema/precio sin catálogo autorizado no está aprobado. No se inventan resultadosSearchConsole, indexación o conversiones.

## Otras plantillas: reutilización de evidencia

La cobertura integral anterior incluye16URLs/50estados; se enlaza, no se repite el discovery. La revisión posterior cubrió9URLs/30registros. Como referencia fechada: categoría mobile67/LCP3.07s/TBT1.54s; PROAIRmobile63/LCP3.56s/TBT2.02s. Su PageSpeed histórico11.8s enPDP usa otro entorno y no constituye una regresión frente a esos valores locales.

El **blog ya tiene su validación publicada separada**: móvil48/LCP6.19s y desktop88/LCP1.84s, mediana3porperfil. No se sigue usando su baseline previo13.26s como estado actual. [Blog](blog-release-validation.md), [auditoría integral](integral-audit.md), [validación previa](postpush-performance.md). Home recibe prioridad sin asumir que las demás plantillas ya alcanzan90.

## Consejo, ADR y orden de trabajo

Dos propuestas independientes, dos contrastes y dos defensas reales válidas, con modelos equilibrados y esfuerzo medio: ClaudeSonnet5.5 y Codexgpt-6.1-sol. CommandCode deshabilitado. Hubo2intentos iniciales rechazados por referencias fuera de alcance —sin timeout, truncamiento ni fallo de autenticación— y una recuperación del checkpoint del reporte local sin repetir inferencias ya válidas. Total8invocaciones; no se cambió el orquestador ni el tema. Las primeras respuestas normalizadas no se conservaron, por lo que el archivo exacto que originó esos2rechazos no puede determinarse.

El contraste registró9objeciones y6preguntas cruzadas; las defensas añadieron condiciones y6respuestas. Claude retiró la atribución causal a las cards, corrigió la identificación del LCP y retiró aplazar autoplay desktop y los estadospass no comprobados. Codex precisó criterios de salida y mantuvo abiertas las pruebas de causalidad. Estas correcciones no acreditan un parche inexistente. La traza MCP nueva se añade como evidencia del controlador posterior al snapshot del consejo: no se finge que los agentes la analizaron en aquella ronda.

[ADR-RHINO-006](ADR-RHINO-006.md): estrategia seleccionada `codex-native-sequenced`; **`needs_evidence` para implementar candidatos**. Se elige por preservar contratos y exigir atribución verificable, no por mayoría ni jerarquía entre proveedores.

1. **Lote0—Home:** atribuir tareas largas móviles y el CLS por frame; identificar propietarios de scripts y geometría. Salida: un problema/consumidor y un candidato medible, o bloqueo documentado. No repetir discovery.
2. **Lote1—primer candidato mínimo:** corrección de inicialización propia o geometría solo si se demuestra su causa. QA local/sandbox y revisión independiente; mobile y desktop obligatorios.
3. **Lote2—recursos:** dimensiones/sizes reales y dependencias CSS/fuentes según coste residual. Mantener helpers y visual; acceso CMS separado si fuera necesario.
4. **Lote3—terceros:** solo integración aislada con propietario, contrato de eventos y permiso aplicable. Nunca eliminar tracking para alcanzar90.
5. Accesibilidad/overflow en lotes separados; conservar líneas base y controles de comercio/SEO en todos.

El objetivo de aceptación es **PageSpeed≥90 en ambos**, aspiración de mediana95, pero no hay candidato ni plazo/ganancia de puntos demostrados. Como objetivos técnicos propuestos: móvilLCP≤2.5s/TBT≤200ms/FCP≤1.8s/CLS≤0.1; desktop protegerLCPactual y bajarCLS≤0.1/TBT≤150ms. Se revisan por plantilla, no son garantía del score. El score depende de varias métricas y fluctúa; [documentación oficial](https://developer.chrome.com/docs/lighthouse/performance/performance-scoring).

## Prevención de regresiones: estado real y propuesta

La política existente sigue **`proposed_not_enforced`**. El comparador comprueba perfiles y deltas, pero no hay hook de bloqueo de rendimiento validado. Esta entrega de diagnóstico no crea otro motor ni afirma que ya impida despliegues.

Para la fase autorizada: integrar al QA/controlador existente un gate por proyecto/plantilla/URL/fuente/dispositivo/Git/perfil/consentimiento/versiónChrome-LH, con almenos5muestras comparables antes/después. Tolerancias prospectivas y prueba unilateral/permutación + ajuste por múltiples métricas según política; datos insuficientes/noise→`inconclusive` o `insufficient_evidence`, perfiles/permisos/fallo crítico→`blocked`, regresión respaldada fuera de tolerancia→`regression_detected`, sin regresiones y QAobligatorio satisfecho→`passed`. El modelo no puede omitir el resultado.

Antes de activarlo hay que fijar presupuestos medidos deJS/CSS/imágenes/requests/longtasks/DOM y validar fixtures de ruido y regresión, además de un caso real. Los valores de este informe son baseline descriptivo, no límites certificados. No debe declararse robusto un hook por pasar solo mocks. Los objetivos de campo siguenLCPp75≤2500ms/INPp75≤200ms/CLSp75≤0.1, separados del laboratorio.

Cadencia propuesta, **sin programarla**: porlote antes/después, lectura después del push autorizado, revisión semanalCrUX/History y mensual o por nuevaapp del conjunto representativo. Se necesitan claves en el controlador para nuevas consultasPSI/CrUX y un presupuesto acordado. No hay cron, CIexterna ni consumo periódico instalado.

## Evidencia y pendientes

[Datos normalizados](home-performance-strategy.json) · [Backlog](home-performance-backlog.json) · [Lighthouse6muestras](../runs/rhino-performance/20261110T235059-home-priority-diagnosis-2f04055a/performance-summary.json) · [DOM/red/AX/axe/capturas](../runs/rhino-performance/20261110T235059-home-priority-diagnosis-2f04055a/home-browser.json) · [Medios y teclado](../runs/rhino-performance/20261110T235059-home-priority-diagnosis-2f04055a/media-keyboard.json) · [MCP nuevo](../runs/rhino-performance/20261110T235059-home-priority-diagnosis-2f04055a/devtools-mcp-insights.json) · [Consejo real](../runs/rhino-performance/20261110T235059-home-priority-diagnosis-2f04055a/council.json) · [Tests40](../runs/rhino-performance/20261110T235059-home-priority-diagnosis-2f04055a/existing-performance-tests.json). Las capturas390/1440están en `20261110T235059-home-priority-diagnosis-2f04055a/browser/`. El MCP conserva recibos/insights, no exportó un tracebinario completo.

Pendientes explícitos: PageSpeed/CrUX frescos; causa raíz del CLS; atribución causal de tareas largas; prueba de reproducción efectiva y pausa; candidato con medición antes/después equivalente; QA completo6anchos para ese candidato; estadística/gates implementados; contraste manual/lectoresde pantalla; contratos de tracking/comercio con entorno permitido. **No se aprobaron ni realizaron cambios en el tema.**
