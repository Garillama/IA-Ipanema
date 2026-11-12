## Actualización: Home automática ya conectada

La ruta real se verificó y la integración automática ya está aplicada localmente: no requiere URL manual en Home. [Estado actual y pruebas](sectionfy-automatic-home.md). La configuración pendiente descrita más abajo corresponde a la etapa anterior; producción sigue bajo control del propietario.

# RHINO — fotos nativas y video Sectionfy: candidato implementado

Fecha: 2026-11-11T19:31:01.071998+00:00. **Estado actual: aplicado y aceptado solo localmente.** Claude y Codex aprobaron el diff corregido; se completaron las pruebas posteriores. La configuración y validación del endpoint real siguen pendientes. El bloqueo anterior por `rate_limit` quedó resuelto en la reanudación solicitada por el propietario. No se hizo push, watch, publish, cambios comerciales ni configuración de la app.

## Alcance que pidió el propietario

Fotos cargadas desde Tiendanube y videos actualizados desde Sectionfy. El carrusel utiliza el Swiper existente; tanto su slide como el banner actual pueden optar por el mismo consumidor HTML5. No se importan textos, títulos ni botones remotos. No se crea otro motor ni se añade una biblioteca.

Los ocho archivos ya están aplicados en `~/Escritorio/Cli/Rhino-Ipanema`. Se conservaron los cambios previos del propietario en `manifest.json` y `templates/pages/home.json`, sin migrar ni configurar la instancia de Home. La transacción `74287aba4f02488d9878fbcc74cbd18b` quedó aceptada, con respaldo privado y hashes antes/después comprobados.

| Archivo candidato | Cambio |
|---|---|
| `blocks/slide.tpl` | Selector Foto / Video Sectionfy; fotos/poster con helper nativo; control accesible fuera de la capa del enlace. |
| `sections/slideshow.tpl` | URL pública de consulta configurada una vez por carrusel. |
| `sections/video.tpl` | Modo nativo, foto o Sectionfy en el banner actual; mismos controles y beneficios. Conserva overlay y prioridad del poster en modos nuevos. |
| `static/js/sectionfy-client.js` | Loader acotado, consulta compartida por URL, selección exacta, compatibilidad con consumidores PDP. |
| `static/js/sectionfy-video-slide.js` | Único consumidor HTML5 para ambos hosts; visibilidad, teclado, foco, intención móvil y coordinación con Swiper. |
| `static/css/sectionfy-video-slide.css` | Estilos condicionales, sin nuevos `!important`. |
| `static/js/store.js` | Cambios limitados a `initSwipers`; resto del archivo y reproductor antiguo sin cambios. |
| `layouts/layout.tpl` | Carga condicional de los nuevos assets. |

## Funcionamiento preparado

- Foto en el HTML inicial; no espera a la API. Los modos nuevos usan el poster nativo si no hay video listo.
- Solo video publicado y visible. Usa `campos.videoUrl` y `videoMimeType`; si hay varias secciones, exige su clave exacta en lugar de elegir una al azar.
- Endpoint HTTPS del host público conocido, sin credenciales en URL ni redirecciones. Admite `{token}` para sustituir el token público existente. No se inventó una consulta Home ni se fijó el ID de producto del ejemplo.
- Timeout abortable de 4 s, sin reintentos ante 403/429 ni otro error. Una petición por endpoint compartida también con consumidores de producto cuando coincide la URL; una respuesta legacy redirigida no se reutiliza para video.
- No descarga el archivo antes del Play móvil. Autoplay de video en escritorio es opcional, respeta movimiento reducido y ahorro de datos; pausa al ocultar pestaña, salir de vista o cambiar de slide.
- Carrusel mixto sin clones de loop. El avance de fotos se conserva y se detiene durante reproducción/espera del video; se restituyen las condiciones de foco/visibilidad antes de reanudar.
- Los controles nuevos de slides inactivos salen del orden de tabulación. Si el foco quedaba en el control saliente, pasa a una flecha visible nativa.

## Pruebas ejecutadas

**222 comprobaciones finales aprobadas**, con alcances separados:

| Prueba | Cantidad | Alcance real |
|---|---:|---|
| Navegador | 153 | Swiper y servicio de visibilidad reales; API y reproducción simuladas; seis anchos 360/390/768/1024/1440/1920, dos hosts, teclado/foco, axe, capas de enlace/overlay, fallos y buffering. |
| Cliente offline | 37 | Contratos, instancia, caché en ambos órdenes con PDP, HTTPS, redirecciones, timeout, 403/429/500 sin retry, reinicialización. |
| Reproducción real local | 8 | Archivo MP4 generado para la prueba y servido por TLS local: decodifica, Play/Pause por teclado, pausa fuera de vista y reanudación tras intención previa. API simulada. |
| Fuente/esquemas | 24 | Esquemas originales preservados, sintaxis JS, overlay/prioridad/fallback, hashes originales/protegidos intactos y patch aplicable sin escribir. |

También pasó `qa --suite quick`: [recibo](../runs/rhino-performance/20261111T192303-quick-a8861062/report.json). Esa suite valida herramientas, no renderiza la tienda. La ausencia inicial de la nueva API del cliente se comprobó contra el código original; es baseline de capacidad faltante, no una declaración de que la tienda anterior estuviera averiada.

No hay render Twig nativo completo, editor Tiendanube, comparación visual de marca publicada, certificación WCAG, PageSpeed nuevo ni prueba de archivo real del cliente. Las capturas son fixtures de componente y no se presentan como fidelidad visual del sitio. No se atribuye ahorro de LCP/INP/TBT ni score90+ a este desarrollo.

## Hallazgos corregidos y trazabilidad

1. Una prueba de buffering falló: Swiper emite `autoplayStart` antes de asignar su temporizador; detenerlo dentro del evento era insuficiente. El aviso de slides con video se difiere a una microtarea. La prueba final pasa. No se alteró el autoplay de carruseles solo de fotos.
2. La revisión de Codex encontró overlay ausente en el host nuevo del banner. Se añadió únicamente a la rama de medios nueva; la inspección estática y las pruebas de opacidad, capas y on/off pasan. La reanudación obtuvo aprobación explícita de Claude y Codex sobre el diff corregido.
3. Se evitó que las reglas antiguas `display:…!important` anularan `hidden`: los controles del banner usan un wrapper sin esa regla. No se añadieron overrides `!important`.
4. El poster prioritario de los modos nuevos es eager/alta prioridad y no queda tapado por un placeholder dependiente de lazy loading. La fuente anterior conserva sus condiciones.

Los primeros contratos que propusieron rutas fuera de la allowlist se rechazaron y conservaron; no se convirtieron en aprobaciones. Se corrigió el alcance explícito y se recuperó solo el participante pendiente. Las propuestas válidas iniciales, contraste y defensas se conservaron por separado.

## Bloqueo anterior y revisión resuelta

Hubo dos propuestas independientes válidas, contraste de ambos y defensa de ambos con cinco preguntas técnicas. La revisión final de Claude falló por **`rate_limit`**, con proceso iniciado/recolectado, contexto entregado y cero tokens de salida. No fue timeout ni se declaró fallo de autenticación. No hubo retry, elevación de modelo, sustitución ni CommandCode.

Codex solicitó corregir el overlay. Tras esa corrección y la reanudación autorizada, **Claude y Codex aprobaron expresamente el código opt-in local**, con hashes coincidentes. La autenticación/inferencia de Claude funcionó en esta revisión; no se sustituyó su participación ni se contó una sesión de Codex como revisión de Claude. La aprobación no comprende activación, publicación ni el archivo real de Sectionfy.

## Configuración del código aplicado

En **Carrusel → Diapositiva**, seleccionar Foto de Tiendanube o Video de Sectionfy; la imagen sigue siendo el poster/respaldo. La URL de consulta se configura en el carrusel y la clave de instancia solo es necesaria si hay varios banners publicados.

En el **banner actual**, el selector preparado es Origen del contenido multimedia → Video automático desde Sectionfy; conserva la portada y controles actuales. Se debe indicar la URL pública real de consulta de la sección de la app, no pegar el MP4. Al cambiar el video en Sectionfy, se consultará al cargar la página; no hay sondeo continuo.

Estas opciones ya existen en el código local y aparecerán en el editor cuando el propietario actualice el tema. **La instancia actual de Home conserva su fuente anterior**: para usar Sectionfy debe seleccionar el modo nuevo e indicar la URL pública real de consulta. No se configuró esa URL ni se completó el acceso externo; el sondeo autorizado devolvió403 y no se repitió. No se afirma conexión en vivo ni reproducción del archivo comercial.

## Evidencias y punto de reanudación

[Patch revisable](../runs/rhino-performance/20261111T184050-sectionfy-hero-media-70f3f556/ready-local.patch) · [Estado/hashes](../runs/rhino-performance/20261111T184050-sectionfy-hero-media-70f3f556/implementation-state.json) · [QA navegador](../runs/rhino-performance/20261111T184050-sectionfy-hero-media-70f3f556/qa-final-candidate/qa.json) · [Cliente](../runs/rhino-performance/20261111T184050-sectionfy-hero-media-70f3f556/client-QA-v2.json) · [Video real local](../runs/rhino-performance/20261111T184050-sectionfy-hero-media-70f3f556/qa-final-real-decode/qa.json) · [Fuente](../runs/rhino-performance/20261111T184050-sectionfy-hero-media-70f3f556/final-source-QA.json) · [Revisiones](../runs/rhino-performance/20261111T184050-sectionfy-hero-media-70f3f556/source-review.json) · [Consejo](../runs/rhino-performance/20261111T184050-sectionfy-hero-media-70f3f556/implementation-council.json).

El patch usa contexto cero en los hunks del cliente para excluir su token público existente; la aplicación posterior requiere control de hashes y el modo correspondiente. Se ejecutó solo `git apply --check --unidiff-zero`, nunca su aplicación. Ese patch fue comprobado sin ejecutarlo. La aplicación se realizó posteriormente por la transacción de archivos con hashes y revisión aprobada; no mediante git apply. Retomar desde el checkpoint de aplicación aceptada: configurar y validar el endpoint real cuando exista acceso, sin repetir discovery ni estas pruebas si no cambian las fuentes.

## Verificación posterior a la aplicación local

Pasaron **198 comprobaciones funcionales posteriores**:153 de navegador,37 del cliente y8 de decodificación real del MP4 generado, ejecutadas leyendo la carpeta real del tema. El recibo de aceptación añade11 controles de hashes/archivos protegidos:209checks en total. Los198 funcionales son reejecuciones después de aplicar, no se suman a los222 previos para inflar cobertura. Los schemas y fuentes anteriores quedaron conservados según la comprobación estática previa.

[Revisiones de reanudación](../runs/rhino-performance/20261111T184050-sectionfy-hero-media-70f3f556/source-review-resume.json) · [Aceptación](../runs/rhino-performance/20261111T184050-sectionfy-hero-media-70f3f556/local-acceptance.json) · [QA posterior](../runs/rhino-performance/20261111T184050-sectionfy-hero-media-70f3f556/accepted-local-QA.json) · [Estado aplicado](../runs/rhino-performance/20261111T184050-sectionfy-hero-media-70f3f556/applied-checkpoint.json) · [Informe anterior conservado](../runs/rhino-performance/20261111T184050-sectionfy-hero-media-70f3f556/report-before-local-application.md).

Se registró `rhino-sectionfy-local-media-capability-v1` como capacidad verificada **solo en el alcance local probado**, con hashes de los archivos y dependencias. No representa una conexión real verificada con Sectionfy ni transfiere derechos del código a otras tiendas. No hubo cambios nuevos de tipografía, instalación de dependencias, push, watch, publish ni operaciones comerciales. No se midió ni se afirma90+ de PageSpeed.
