# ADR-RHINO-011 — descubrimiento e indexación de producción

Estado: **needs_evidence** para implementación. Autor: Codex, único participante por instrucción del propietario. No es aprobación dual ni revisión independiente. Fecha: 2026-11-12 UTC / 2026-11-11 Ciudad de México.

## Objetivo y permisos

Que las páginas públicas relevantes tengan caminos de descubrimiento HTML e indexabilidad técnica verificable, conservando SEO, accesibilidad, rendimiento y comercio. Esta fase autoriza lectura y preparación de evidencia; no publica ni hereda la autorización del arreglo previo de breadcrumbs. No hay archivos del tema modificados en esta fase.

## Evidencia

[Auditoría y matriz](indexability-20261112/README.md). Doce GET de documentos explícitos, sin crawl: cuatro copias de sitemap con 117 URLs únicas en conjunto, robots, siete páginas. Se reutilizan veinte verificaciones de artículos posteriores al arreglo anterior.

Todos los catorce productos del sitemap y las cinco categorías tienen rutas de enlace HTML observadas desde home. Dos páginas institucionales y 62 artículos no tienen camino demostrado en esta muestra; no se certifica orfandad. Blog página 2: doce artículos diferentes, canonical a portada. Catálogo: doce productos en el contenido principal, control de carga sin href; navegación global proporciona rutas adicionales.

GSC configurado, credencial no disponible. Se abrió OAuth read-only bajo autorización previa; espera agotada sin completar consentimiento, sin consultar Search Console. Total indexado y canonical Google desconocidos.

Crawler V4: [entrega no aplicada ni aprobada](../seo/v4-source-review/delivery.json). La revisión exige recibo QA del controlador para el hash candidato y participación/revisión independiente válida. AGENTS: «Objeciones críticas y condiciones obligatorias pendientes impiden implementar». No se alteran estos controles ni se llama a Claude o CommandCode.

## Alternativas y cuestionamiento técnico

1. Mantener código actual y completar evidencia: admisible ahora, sin mejora de navegación aplicada.
2. Configuración nativa classic: evita depender del control infinite, pero cambia paginate12 a paginate60. ¿Qué coste de DOM, imágenes, filtros y diseño introduce? Falta medir. No seleccionada para despliegue.
3. Mantener infinite con enlaces progresivos nativos: preferida como candidata por preservar experiencia, no aprobada. ¿LS intercepta el enlace sin navegar? ¿Se actualiza el cursor tras append? ¿Se conservan filtros/orden? ¿Se duplican cards? Faltan respuestas con producción y pruebas acotadas. No basta agregar un href estático.
4. Agregar un canonical desde layout al blog: podría duplicar el emitido por head-tags. Falta mecanismo soportado para sustituirlo de manera única. No implementar a ciegas.
5. Agregar enlaces a los 62 artículos no observados: innecesario si la paginación existente cubre la cadena. Primero comprobarla; no expandir DOM basado en ausencia de una muestra.
6. Ejecutar V4 sin cerrar revisión o escribir otro crawler: descartado por condiciones explícitas del propietario y AGENTS.

Estas preguntas son revisión crítica de Codex, no se atribuyen a otro proveedor ni se presentan como consenso.

## Decisión

Conservar producción y el fix previo. Priorizar la progresión HTML del catálogo y la señal canonical de paginaciones del blog. Resolver autenticación de Google y aceptación del crawler antes de ampliar cobertura. [Backlog](indexability-20261112/backlog.json) con causas, fuentes, responsables, alternativas, riesgos, pruebas y reversión.

No hay P0 general de indexabilidad de tienda demostrado. La indisponibilidad del crawler es bloqueo de herramienta, no prueba de bloqueo de Google.

## Impacto y pruebas obligatorias

- SEO: URLs reales, canonical único, robots y separación de auxiliares; comprobar Google con inspecciones y exportaciones, no inferirlo de HTTP200.
- Rendimiento: preservar los baselines; ninguna mejora de LCP/TBT/CLS afirmada. Medir candidatos bajo perfiles equivalentes, sin PageSpeed redundante en esta fase.
- Accesibilidad: navegación real con teclado, foco, nombres, noJS y seis anchos; no esconder enlaces para robots.
- Comercio: conservar LS, variantes, filtros, orden, precio y stock. Sin compra ni envío de formularios.
- Revisión: hashes de archivos remotos/locales, respaldo y diff exacto; cierre de condiciones críticas, revisión independiente aplicable y QA antes de solicitar autorización de despliegue.

Pruebas efectuadas: diez predicados de integridad de la evidencia aprobados, no equivalentes a QA completo ni indexación. XML válido y coincidencia de copias, caminos a productos, continuidad de dos páginas y reproducción de dos defectos. Fuente/checkpoint sin cambios posteriores por esta tarea.

## Pendientes y autorizaciones

Completar OAuth read-only; obtener exportación oficial de indexación si se requiere total. Cerrar revisión/integración de V4 mediante el flujo existente. Revisar primer crawl acotado antes de pedir ampliación. Cualquier cambio de producción exige nueva autorización específica sobre diff, respaldo, hashes y reversión; hoy no hay candidato aprobado para publicar.

## Seguimiento 2026-11-12T16:25Z — acceso Google y consejo dual

El propietario autorizó usar Claude y Codex; ambos smokes reales aprobaron. GSC respondió13inspecciones:10enviadas/indexadas, Contacto descubierta sin indexar, Sobre y blog página2no reconocidas. SearchAnalytics devuelve170filas deURL en el periodo2026-10-12..2026-11-08, filtradas al origen sin www;104URLs coinciden exactamente con el sitemap. No constituyen el total actual del índice. Sitemap registrado general sin errores/advertencias. [Matriz y reporte nuevos](indexability-20261112/google-followup.md).

Consejo real: ADR-79345cdd49e2, dos propuestas independientes y contraste de ambos; diez objeciones, cuatro preguntas y dos respuestas de Claude. Defensa Codex no iniciada por agotar presupuesto6tras reintento de contrato de Claude. **No hay aprobación dual completa**, ni cambio de estado de implementación. Se preservan resultados sin repetir deliberaciones válidas ni ampliar el presupuesto de recuperación.

Nueva evidencia posterior del controlador: LS.hybridScroll publicado genera y solicita `/productos/page/2/` (200,results_only=true,limit12). Scroll lleva12a14IDsúnicos, conserva orden inicial; GET de la ruta completa devuelve200,canonicalpropio y los dos productos en HTML. Resuelve existencia/continuidad del catálogo actual, no filtros futuros ni render de next_link en un parche. La documentación oficial confirma canonical administrado por head-tags; override de blog aún no demostrado.

Cuatro capturas móviles actuales (catálogo/blog2, JS/noJS) conservan enlaces; QA registra fallos de imágenes sinJS y contraste de puntos de paginación. No hay prueba de seis anchos/teclado completo ni mejora de métricas. La continuidad de 12 a 14 IDs en esta muestra no garantiza el comportamiento de otras variantes o tiendas.

Decisión del controlador: conservar el sistema nativo y priorizar una futura alternativa progresiva con contratos comprobados; canonical del blog requiere vía soportada de plataforma. **needs_evidence**, sin diff aplicado y sin autorización remota nueva. El crawlerV4 mantiene su bloqueo de aceptación independiente. No se confunde este consejo con aprobación de su parche.


## Continuación autorizada de defensa y tres problemas — 12 noviembre

Se recuperó únicamente la defensa pendiente de Codex con una nueva invocación acotada, mismo prompt/hash y permisos, sin repetir propuestas/contrastes. Artefactos originales intactos. Cobertura de defensas completa; estado agregado needs_evidence por condiciones y una retirada de alternativa ajena rechazada por el controlador. No se declara consenso ni aprobación.

[Estado detallado, candidato, revisión y propuestas](indexability-20261112/three-issues/README.md). Candidato inicial de href/interceptación rechazado; v2 usa botón nativo y navegación numerada separada, sin interceptar eventos. Claude solicita cambios/evidencia: permanece sin aplicar. Dos archivos respaldados desde producción, hashes coinciden y CLI398archivos en sincronía.48checks defixture aprobados,no equivalentes a renderTwig/QAreal.

Blog3y8:200,artículospropios,canonicala/blog/,Google no reconoceURLs exactas; no causalidad demostrada ni override soportado. Institucionales:200,sitemap,canonicalpropio,sinrestricciónobservada,pero home no ofrecehref haciaellas; proponer2entradas en menúfooter nativo,preservando4actuales. Sin cambiar footer por código. Pendiente exportación nativa/revisión/autorización. No cambios de tema ni producción.

## Preparación operativa incremental — 12 noviembre, validación nativa

El propietario confirmó que no dispone de exportación/IDs de menú ni integración administrativa identificada y autorizó preparar la vía manual, sin modificarlo. Se investigaron recursos oficiales y CLI: no se encontró CRUD/exportación de navegación documentado en las fuentes consultadas; el webhook navigation/updated no lo sustituye. Procedimiento manual preparado para conservar4entradas y añadirContacto/Sobre; respaldo administrativo eIDs no inventados. No se ejecuta ni bloquea las otras investigaciones.

Paginación: v2 original preservado. Prueba aislada conLSpublicado detectó foco enBODY; continuidad separada corrigió foco tras teclado/error y no lo roba si usuario lo movió. Se comprobó en seis anchos con respuestasfixture locales, nunca solicitudes reales a páginas3+. Se corrigió guarda de numeración/cursor y nombre distinto de la navegación, sin nuevas traducciones ni dependencias. Fullfile review confirmó ausencia de defecto de fuente demostrado, sin aprobar implementación.

**Nuevo control cerrado:** comando oficial themecheck con vista de lectura virtual de dos archivos, sin modificar carpeta original. El servidor validó exactamenteTpl0958c668… yJSf9755749… con valid=true/errors=[]; POSTsolo avalidación, ningúnPATCH. Diffposterior confirmó398archivos publicados en sincronía. Esto acredita sintaxis/schema/tamaño, no renderHTML ni indexación.

Claude revisó incrementalmente el recibo y distinguió precondiciones de propuesta de la aceptación posterior. La versión publicada/render/rendimiento del candidato solo pueden comprobarse después de una operación específicamente autorizada; no se marcan pasados con fixtures. Mantiene blocked para ejecución/aceptación general. El paquete puede presentarse únicamente para revisión del propietario, no para aplicar.

[Paquete operativo y límites](indexability-20261112/three-issues/operations/README.md): procedimiento manual, consulta aTiendanube no enviada, diff/manifest, respaldos vinculados, pruebas, revisiones, requisitos antes/después y reversión. Ninguna publicación, cambio del tema, menú, canonical o configuración remota. Cero consultasGoogle repetidas y sin nuevo consejo completo.

## Paquete final de autorización — 12 noviembre, continuación incremental

**Estado: approved_with_conditions exclusivamente para código y preparación de solicitud; publicación no autorizada, aceptación final pendiente.** No reemplaza los checkpoints previos ni convierte sus blocked históricos en aprobaciones retroactivas.

Se confirmó por lectura nativa que 14828608 sigue siendo la única instalación productiva de la tienda 7400935. Se descargaron nuevamente los dos originales y sus hashes coinciden con before; el diff completo permanece in_sync. El parche final conserva SHA256 `1ef6c047b222962f3138cbaa3aba760b16d9569b5e597ad04cfa053df714eb49`, afecta solo pagination.tpl y store.js y reproduce exactamente ambos hashes after al aplicarlo a los nuevos respaldos en una prueba de código aislada. No se aplicó al tema.

Se tomaron cinco mediciones locales comparables por dispositivo de /productos/, sin repetir consultas de Google ni discovery. Medianas: móvil score65, LCP2,855s, TBT2264ms; escritorio score87, LCP1,515s, TBT205ms. No son PageSpeed, ni resultados del candidato; el protocolo de solo lectura bloquea escrituras/telemetría y debe preservarse en la comparación posterior. Originales, perfiles, dispersión y métricas correlacionadas conservados. No se afirma 90+ ni mejora de rendimiento.

Claude revisó realmente los dos archivos completos y hashes exactos, diff, baseline y plan de QA/reversión: contrato válido, contexto completo, decision approve acotada a fuente y preparación de autorización. Respondió a Codex que no quedan objeciones críticas concretas de fuente previas; el menú es una operación distinta y su respaldo no bloquea paginación. Los controles de render/HTML inicial, valores traducidos, teclado/AX, comportamiento real12→14, seis anchos, smoke de consumidores y rendimiento comparable siguen pendientes para después de una publicación específicamente autorizada. No se simula consenso completo nuevo ni revisión de pruebas que el revisor no ejecutó.

El propietario debe aceptar la fila numerada visible, navegación «Página: productos» y botón visible/deshabilitado sin JavaScript. Se conserva carga nativa; los href separados permiten navegación independiente y no se inventa página3. La CLI no ofrece subida por --file: el procedimiento exige payload exacto de dos modificaciones, cero eliminaciones, hashes after y restricción del transporte existente. Nueve casos offline de esa restricción pasaron; no son un despliegue real. Revalidar hashes e identidad inmediatamente antes de cualquier operación autorizada.

La autorización solicitada debe limitarse a esos dos archivos y, si se acepta, a restaurar exclusivamente sus respaldos ante QA fallido mientras los hashes remotos sigan siendo los after aprobados. Ante cambios ajenos se detiene. Menú sigue pendiente del respaldo administrativo; la ausencia de IDs debe constar y se usará identificación manual por campos completos, no IDs inventados. Foco en enlaces colapsados del footer: defecto previo de accesibilidad P2, riesgo separado, sin modificar en este paquete. Blog conserva canonical; consulta preparada, no enviada, sin respuesta oficial recibida.

[Paquete definitivo, revisión, baseline y controles](indexability-20261112/three-issues/operations/publication/README.md). No se ejecutaron push, watch, publish, clon, staging ni cambios comerciales.

## Ejecución específicamente autorizada y QA posterior — 12 noviembre

El propietario autorizó explícitamente instalación14828608/tienda7400935, el SHA256 exacto del parche y los dos hashes after. Se reconfirmaron los originales y respaldos antes de ejecutar y otra vez inmediatamente antes de enviar el único PATCH. Payload: dos modificaciones, ninguna eliminación; HTTP200. La reiteración posterior de autorización no produjo una segunda subida. Se sincronizaron localmente solo esos dos archivos después de comprobar la publicación. El diff nativo final confirma398archivos en sincronía.

La lectura individual de store.js devolvió los bytes originales; se detuvieron escrituras. El listado oficial de archivos por lote devolvió el JS candidato y la plantilla exactos, y el navegador descargó del CDN público el JS con SHA256f9755749…e93be9, idéntico a lo autorizado. Causa de la discrepancia de lecturas: no determinada. No se justificó otra subida ni se afirmó caché como causa probada. Ambas evidencias se conservan.

QA publicado del alcance: HTML inicial con href relativos reales entre página1y2,200y canonical propio; LS real12→14IDs únicos y orden conservado en seis anchos; botón habilitado con JS; navegación a página2sinJS y con Enter a390/1440; AX con nombres traducidos correctos, axe acotado sin violaciones; home/PDP/blog200sin pageerrors en ambos tamaños. Se tomaron capturas reales. Los estados manuales del botón no son ejercitables con14productos por umbral60: se conserva la evidencia de fixtures, sin fingir pruebas reales adicionales. No se probaron compras, tracking completo ni filtros no expuestos.

Rendimiento local equivalente, cinco muestras por dispositivo: score mediano móvil65→65, escritorio87→88. LCP móvil2,855→3,125s(+9,5%) conserva advertencia; TBT2264→1960ms es un cambio observado sin causalidad. Comparador registra delta positivo de LCP; gates predeclarados no se activaron. CLS máximo móvil0→0,0268, mediana0. No se afirma equivalencia estadística,90+ni INP. No se repitieron APIsGoogle.

Claude revisó de forma independiente los recibos posteriores y aprobó únicamente el alcance probado. Señaló que el check no_horizontal_overflow estaba formulado de forma demasiado general: se renombró en un recibo final a catálogo tras append, sin borrar el original. Hay overflow observado antes de append, sinJSy en otras páginas de escritorio; falta baseline geométrico para atribuirlo o llamarlo preexistente. No se modificaron componentes ajenos para resolverlo.

**Decisión de cierre:** aceptar la publicación para el alcance funcional/SEO comprobado, con advertencias y límites documentados; no hay regresión crítica atribuible demostrada que active la reversión autorizada. Ninguna escritura adicional. Menú pendiente del respaldo del propietario; canonical del blog sin cambios y consulta sin enviar. [Informe de producción](indexability-20261112/three-issues/operations/publication/resultados-produccion.md) y resultado estructurado conservan evidencias, hashes y métricas originales.

## Continuación de estructura pública — menús expresamente fuera de alcance

La instrucción posterior del propietario suspende la propuesta de añadir Contacto y Sobre Rhino al menú. Sobre Rhino existe pero está pendiente de contenido: no se promociona, no se añade noindex ni se elimina. Se conserva el procedimiento anterior como historial, sin autorización vigente de ejecución. La autorización de publicación de paginación ya consumida no se transfiere a este trabajo.

**Estado global de cobertura: needs_evidence; sin implementación nueva propuesta.** Se reutilizó inventario de117entradas (116HTML y1XML) y se añadieron al inventario principal las8paginaciones reales ya conocidas:125filas,124HTML. Grafo offline de evidencia inicial:122HTML con camino desdehome; Contacto/Sobre sin camino observado, no huérfanas absolutas. Fechas, href/contexto y fuente por campo se conservan.

Las páginas de blog4–7 se leyeron por primera vez; junto con1/2/3/8conservadas contienen86enlaces de artículos distintos, iguales al inventario de sitemap. Eso cierra el antiguo faltante de descubrimiento de62artículos en la muestra, no su indexación. Todos los listados posteriores conservan canonical de portada; sin cambio ni atribución causal de exclusión. Cinco categorías tienen200/canonicalpropio/1H1 y enlaces de tarjetas sinJS en navegador; sus14rutas de producto asociadas no prueban todas las variantes de URL. GUN AIR con/sin entry_path se comprobó200con canonical limpio; los demás alias conservan estado no verificado individualmente.

CoberturaHTTP:49HTML individuales observados másXML; faltan11productos y64artículos. Los estados administrativos de producto/stock/variantes no se certifican por sitemap. No se confirmó subcategoría adicional ni exhaustividad de la taxonomía administrativa. Las15inspeccionesGSC previas (13+2) se conservan,10PASS conocido, sin censo del índice. Las170filas de rendimiento del periodo previo no equivalen al total indexado. Credencial no disponible en esta sesión; cero consultas nuevas y sin iniciarOAuth. Se preparó un futuro lote acotado de4inspecciones justificadas, sin ejecutarlo.

CrawlerV4 permanece sin integrar y con implementation_allowed=false. Se conserva su bloqueo; no se ejecutó ni reemplazó por otro motor o lote masivo manual. Solo14GET de documentos explícitos conocidos y5navegaciones sinJS de categorías, sin cola de red;19documentos principales, no total de assets. No se tocaron tema, menús, contenido, catálogo, aplicaciones ni canonicals. Los hashes protegidos de paginación y sus consumidores se conservan. Se registró un cambio local ajeno en bundle-builder-js.tpl, no modificado por esta tarea.

[Matriz, prioridades y evidencia de esta continuación](indexability-20261112/site-continuation/README.md). La revisión incremental del consejo se registra separadamente; cualquier fallo o recuperación no equivale a aprobación ni autoriza escrituras.

**Cierre del contraste incremental:** Claude produjo análisis de faltantes; una revisión posterior falló con salida genérica y causa interna no conservada (no determinada), por lo que no se registró aprobación. Se recuperó de forma acotada y pidió precisar22HTTP frente a24destinos enlazados, además de mantener el canonical de blog como hallazgo abierto. Codex contrastó fuentes:24enlaces enblog1/2,86trasblog1–8y22HTTP individuales son dimensiones distintas; el blog ya estaba enP2needs_evidence y nunca se llamó correcto su canonical. Se añadió la conciliación al informe. Claude aprobó únicamente esa precisión documental tras el intercambio final, sin afirmar ejecución de pruebas ni lectura completa de125filas. La auditoría integral mantiene needs_evidence, con75destinos sinHTTP propio. No implementación ni permiso remoto nuevo. Recibos en council-incremental.json; no se atribuye al modelo un consenso o cobertura que no produjo.

## Cierre de condiciones del motor V4 — continuación sin integración

Se verificó el mismo parche final SHA256 `7a5a7066bb22d2f87c18286100a9fba0ce76e50e53a8cf9b211821d0eba8b4a0`, seis preimágenes del workspace, tres nuevas pruebas aún ausentes y AGENTS sin cambios. El controlador aplicó el artefacto exclusivamente a una copia temporal de herramientas/tests y ejecutó 169 unitarias SEO, 13 integración y TLS local: pasaron sobre los nueve hashes candidatos. Este recibo cierra el QA aislado pendiente, no la integración ni el funcionamiento de Rhino.

Se recuperó el consejo original ADR-1136231f425a con igual binding y preservando la propuesta de Claude y los artefactos anteriores. Codex inició con contexto completo y eventos válidos pero agotó inactividad a90s; una única recuperación acotada con180s/máximo360s, mismo modelo/proveedor y sin elevar permisos, también agotó inactividad. Ambos procesos fueron recogidos; no hubo contrato válido. La causa interna del silencio no se conoce y no se presenta como autenticación/cuota. No más intentos ni sustitución por CommandCode. El agregado sigue needs_evidence/implementation_allowed=false; faltan propuesta válida de Codex, contraste, defensa y recibos de restricciones por alternativa. La auto-revisión del principal no sustituye el nodo requerido.

Claude revisó el delta de QA y confirmó ese alcance, sin identificar un defecto nuevo demostrado en el hash final y sin aprobar integración. Se distinguieron versiones mediante pruebas locales: la base actual falla en max-image-preview:none y selección del token bot por subcadena; los dos casos de fuentes físicas malformadas que fallaban en el antiguo candidato4369d84d pasan en la base actual y no se le atribuyen falsamente. Todo permanece como evidencia del motor, no prueba de un bloqueo de producción.

Resultado: cero nuevas lecturas de Rhino y Google; matriz125 preservada con columnas explícitas de bloqueo,49/124HTML con HTTP propio y75pendientes. GSC configurado pero sin credencial disponible, sin OAuth nuevo ni repetir las15inspecciones. No hay integración administrativa autorizada identificada; se preparó conciliación manual de categorías y procedimiento oficial de exportación de GSC. La paginación, menús, contenido, catálogo, apps y canonicals no se tocaron.

[Informe de cierre, diff exacto y procedimiento de75URLs](indexability-20261112/site-continuation/coverage-closure/README.md). No se solicita aplicar un parche mientras las condiciones obligatorias estén abiertas. Una autorización futura será específica de los nueve archivos del motor, sin transferencia de la autorización ya consumida de paginación.


## Continuación del 12 noviembre — Codex recuperado, V4 aún pendiente

Se recuperó únicamente la propuesta faltante de Codex y se completaron contraste y defensas con Claude. El ADR conserva needs_evidence y implementation_allowed=false; no se integra el parche 7a5a7066. El controlador reprodujo reservas sobre precisión del gate y expansión de evidencia. [Diagnóstico, respuestas y condiciones](indexability-20261112/site-continuation/coverage-closure/codex-recovery/README.md). No hubo cambios al motor, tema ni producción.


## Candidato incremental final — 12 noviembre

Los tres problemas técnicos de gate/evidencia/contrato están corregidos en aislamiento. Claude y Codex aprobaron el nuevo hash `611a5dac1e2767c0d331e42b06c60834e8a427c8bbc41671b9a81a8c977f3e2c`,11 archivos;191 unitarias SEO y13 integraciones aprobadas. El parche anterior se conserva intacto. Listo para solicitar autorización específica de integración LOCAL; no integrado ni autorizado para red. [Diff, recibos, riesgos y ADR](indexability-20261112/site-continuation/coverage-closure/final-candidate/README.md).
