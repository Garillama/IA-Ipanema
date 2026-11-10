# RHINO Performance — auditoría integral de rendimiento, accesibilidad y estabilidad

Fecha: 2026-11-10T19:58:35.427455+00:00 (UTC). Proyecto **rhino-performance**. Sitio **https://rhino-performance.com/**. Referencia pública de assets **14828608**. No corresponde a DaMar ni a su instalación = 14748767.

## 1. Resumen ejecutivo

La muestra cubre16 URLs y50 estados/capturas, seis perfiles Lighthouse local con tres muestras cada uno, diez resultados PageSpeed, CrUX URL/origen e histórico de ocho periodos. Se utilizó DevTools MCP real, axe-core, proyecciones SEO y árbol AX. No se modificó el tema, catálogo ni producción. No se realizaron compras ni envíos de formularios.

Los p75 del origen cumplen los objetivos LCP/INP/CLS en el periodo observado, pero no se pueden atribuir a cada URL. La home carece de LCP/INP de URL; PRO AIR móvil devuelve LCP1.655 s y CLS0.02, sin INP. Por ello no se afirma que todas las páginas aprueben los Core Web Vitals.

Prioridades: consistencia real de Offer.price; diagnóstico móvil de producto/blog; estabilidad del embed de video; trabajo de terceros; accesibilidad compartida, packs y estructura; y corrección de salidas SEO observadas. No se declara P0 ni regresión entre versiones sin una comparación válida.

## 2. Alcance, inventario y selección

| Página | URL real | Estados/capturas | Criterio |
|---|---|---|---|
| article_1 | /blog/posts/pedaleaste-100-km-y-luego-qu-dd31584de196 | 2 | Variante de plantilla/estado a 390 y 1440 |
| article_2 | /blog/posts/el-wod-termina-en-15-minutos-tu-recuperacin-no-d379eea67569 | 2 | Variante de plantilla/estado a 390 y 1440 |
| blog | /blog/ | 2 | Variante de plantilla/estado a 390 y 1440 |
| bundle | /arma-tu-pack-de-recuperacion/ | 2 | Variante de plantilla/estado a 390 y 1440 |
| cart | /comprar/ | 2 | Variante de plantilla/estado a 390 y 1440 |
| category | /presoterapia/ | 8 | Seis anchos + sin JS + reduced-motion |
| category_accessories | /accesorios/ | 2 | Variante de plantilla/estado a 390 y 1440 |
| home | / | 8 | Seis anchos + sin JS + reduced-motion |
| login | /account/login/ | 2 | Variante de plantilla/estado a 390 y 1440 |
| not_found | /__ipanema_audit_missing_20261110__/ | 2 | Variante de plantilla/estado a 390 y 1440 |
| policy | /politica-de-devolucion/ | 2 | Variante de plantilla/estado a 390 y 1440 |
| product | /productos/botas-presoterapia-inalambricas-pro-air/ | 8 | Seis anchos + sin JS + reduced-motion |
| product_accessory | /productos/baterias-doble-capacidad-pro-air/ | 2 | Variante de plantilla/estado a 390 y 1440 |
| register | /account/register | 2 | Variante de plantilla/estado a 390 y 1440 |
| search | /search/?q=presoterapia | 2 | Variante de plantilla/estado a 390 y 1440 |
| search_empty | /search/?q=ipanema_audit_no_result_179433 | 2 | Variante de plantilla/estado a 390 y 1440 |

Home, categoría principal y PDP principal:360,390,768,1024,1440,1920 px; sin JS y reduced motion a 360 px. Otras variantes:390/1440 px. Se añadieron carrito vacío, packs, login y registro. No se inventó una ruta de contacto; no fue descubierta. El blog se amplió con una segunda página enlazada de verdad y comprobada sin JS. No es un crawl de todas las URLs del catálogo.

## 3. Condiciones y procedencia

Baseline de navegador: Chrome155.0.8059.84, contextos anónimos, sin cookies personales y sin decisión de consentimiento. QA con DPR1, red/CPU sin throttling explícito y caché CDP desactivada; isMobile/hasTouch se activan por debajo de768 px. No representa todos los dispositivos físicos. POST y acciones comerciales están bloqueados; ello puede cambiar apps, analytics y reproducción respecto a un navegador sin esa protección.

Lighthouse local13.6.0 conserva viewport, CPU/red simuladas, reinicio de almacenamiento, versiones y muestras individuales en [performance-baseline.json](performance-baseline.json). Mobile412×823/DPR1.75, CPU×4, RTT150 ms/1638.4Kbps; desktop1350×940/DPR1, CPU×1, RTT40 ms/10240Kbps. PSI utiliza Chrome157 y no expone todas sus condiciones en estos resultados. No hay comparación causal entre esas fuentes.

Fuente local candidata: `Rhino-Ipanema`, ref Git `c0bc7b8b423957e6545e2fb6b49d24fe1364ef1e`, manifest local1.2.2. No se verificó equivalencia con despliegue ni se presenta esa versión como versión remota confirmada.381 archivos con baseline de hash verificable no cambiaron; tres hashes de plantillas password fueron redactados por el escritor de evidencias y no permiten comparación. No se interpretaron como cambios de código.

## 4. PageSpeed Insights: muestras reales separadas por dispositivo

| URL | Dispositivo | Perf/Acc/BP/SEO | LCP s | FCP s | TBT ms | CLS | Speed Index s |
|---|---|---|---|---|---|---|---|
| / | mobile | 85 / 94 / 96 / 100 | 3.74 | 1.36 | 190.50 | 0.045 | 3.80 |
| / | desktop | 70 / 94 / 77 / 100 | 0.88 | 0.33 | 828.50 | 0.053 | 1.49 |
| /presoterapia/ | mobile | 72 / 96 / 96 / 100 | 3.30 | 1.06 | 770.50 | 0.045 | 3.74 |
| /presoterapia/ | desktop | 83 / 96 / 96 / 100 | 0.96 | 0.28 | 345.00 | 0.013 | 1.05 |
| /productos/botas-presoterapia-inalambricas-pro-air/ | mobile | 47 / 93 / 96 / 92 | 11.82 | 4.14 | 606.00 | 0.021 | 5.77 |
| /productos/botas-presoterapia-inalambricas-pro-air/ | desktop | 84 / 93 / 96 / 92 | 0.80 | 0.32 | 303.20 | 0.107 | 1.05 |
| /productos/baterias-doble-capacidad-pro-air/ | mobile | 50 / 97 / 96 / 100 | 11.46 | 3.83 | 465.50 | 0.021 | 6.33 |
| /productos/baterias-doble-capacidad-pro-air/ | desktop | 82 / 97 / 96 / 100 | 0.90 | 0.34 | 259.55 | 0.155 | 1.02 |
| /blog/ | mobile | 66 / 93 / 96 / 100 | 11.04 | 1.10 | 248.00 | 0.045 | 4.92 |
| /blog/ | desktop | 52 / 93 / 96 / 100 | 2.41 | 0.49 | 1174.50 | 0.036 | 2.47 |

Una muestra PSI por URL/dispositivo. Todas respondieron con resultado Lighthouse; no hay estimación de variabilidad PSI con n = 1. Los scores no son garantías de WCAG, indexación ni posicionamiento.

## 5. Lighthouse local: medianas y variabilidad

| URL | Dispositivo/n | Perf mediana | LCP s (mín–máx) | FCP s | TBT ms | CLS | Speed Index s |
|---|---|---|---|---|---|---|---|
| / | mobile/3 | 60 | 3.67 (3.48–4.08) | 1.81 | 1396.00 | 0.000 | 3.58 |
| / | desktop/3 | 73 | 1.06 (1.02–1.13) | 0.48 | 176.00 | 0.449 | 1.13 |
| /presoterapia/ | mobile/3 | 66 | 3.13 (2.78–3.23) | 1.24 | 2097.04 | 0.027 | 2.89 |
| /presoterapia/ | desktop/3 | 94 | 1.30 (1.25–1.86) | 0.41 | 135.50 | 0.027 | 1.13 |
| /productos/botas-presoterapia-inalambricas-pro-air/ | mobile/3 | 60 | 3.79 (3.28–3.84) | 1.63 | 1791.59 | 0.000 | 3.69 |
| /productos/botas-presoterapia-inalambricas-pro-air/ | desktop/3 | 91 | 1.48 (0.95–1.55) | 0.66 | 128.00 | 0.079 | 1.44 |

El servicio conserva el score de la primera muestra en su resumen original; este informe calcula explícitamente la mediana de scores a partir de las muestras, sin reescribir los originales. Todos los rangos y valores individuales están en el baseline. No se equipara TBT a INP.

## 6. CrUX: URL, origen y periodos

| Ámbito/URL | Dispositivo | LCP p75 s | INP p75 ms | CLS p75 | FCP p75 s | Estado |
|---|---|---|---|---|---|---|
| / | mobile | — | — | 0.000 | 1.52 | partial |
| / | desktop | — | — | 0.050 | 1.16 | partial |
| ORIGEN | mobile | 1.91 | 112 | 0.010 | 1.52 | observed |
| ORIGEN | desktop | 1.74 | 65 | 0.060 | 1.14 | observed |
| /presoterapia/ | mobile | — | — | — | — | insufficient_field_data |
| /presoterapia/ | desktop | — | — | — | — | insufficient_field_data |
| /productos/botas-presoterapia-inalambricas-pro-air/ | mobile | 1.66 | — | 0.020 | 1.47 | partial |
| /productos/botas-presoterapia-inalambricas-pro-air/ | desktop | — | — | — | — | insufficient_field_data |
| /productos/baterias-doble-capacidad-pro-air/ | mobile | — | — | — | — | insufficient_field_data |
| /productos/baterias-doble-capacidad-pro-air/ | desktop | — | — | — | — | insufficient_field_data |

Periodo diario consultado:12 octubre–8noviembre2026. `partial` significa métricas devueltas y otras ausentes; `insufficient_field_data` no se convierte en ceros ni en un fallo universal del sitio. En el origen móvil,12.76%de las experiencias caen en el bin CLS>0.25 pese al buen p75: conviene investigar la cola.

History del origen, ocho ventanas semanales de28días solapadas: LCP móvil3749→1934 ms y desktop3024→1749 ms entre los extremos observados. Son periodos agregados y diferentes de la ventana diaria actual; no se atribuye la tendencia a esta auditoría ni se promete cambio inmediato. Histogramas, periodos y nulos se preservan en [integral-evidence.json](integral-evidence.json).

## 7. LCP y carga crítica por plantilla

- Home: el LCP es el poster de video `.js-video-thumbnail > img.image-priority-high`. Ya pasa descubrimiento, alta prioridad y ausencia de lazy. No añadir preload a todo ni cargar el video completo para corregir el poster.
- Categoría: primera imagen de producto `.js-product-item-image-container-private … img.image-priority-high`; los mismos checks pasan. Investigar CSS/JS/red, no asumir falta de prioridad.
- PDP: imagen de galería `.js-product-slide-link > img.image-priority-high`; también pasa esos checks. PSI móvil11.82 s contrasta con 3.79 s local y1.655 s de campo en PRO AIR. No demuestra por sí solo una urgencia de campo ni el mismo cuello en todos los usuarios.
- Blog: `.blog-card-img` es LCP, pero no se descubre directamente en HTML y carece de hint de prioridad. El componente local candidato fuerza lazy JS para todas las tarjetas. Es un objetivo concreto de revisión del primer recurso crítico, conservando lazy en los demás.

Los desgloses de insights pueden corresponder a tiempos observados de traza y las métricas a simulación. No se dividen subpartes por el LCP final cuando sus sumas no coinciden ni se inventan porcentajes causales.

## 8. Árbol de accesibilidad, semántica y teclado

AX home:1838 nodos a 390 px y2015a1440 px; dos landmarks contentinfo en ambos. Más nodos no equivale a mejor accesibilidad. Se inspeccionaron roles y una muestra acotada de controles,25Tab por ancho, menú/búsqueda, carrito vacío, Escape, expansión de reseñas y un probe de flecha de carrusel. El despacho de ArrowRight no certifica que el slide haya cambiado.

Fallos reproducidos: ARIA prohibida en el logo Google, contraste en precios/reseñas, nombre accesible que no conserva texto visible; enlace de video sin nombre en PDP; nested-interactive/select-name en packs. Al abrir menú aparece un botón de cierre sin nombre. Faltan H1 en las dos categorías. Footer presenta landmarks duplicados; desktop home no tiene un H1 de contenido accesible demostrado.

Los probes Escape no devolvieron foco al disparador en las secuencias actuales. Se esperó450 ms en la segunda captura; aun así no se afirma una trampa ni una infracción por cada aria-controls ausente sin confirmar patrón/cierre. Varios enlaces alcanzados con Tab tienen geometría cero: descendientes absolutos pueden seguir pintando contenido; se requiere comprobación visual de foco. No se ejecutó lector de pantalla humano ni certificación WCAG.

## 9. DOM, layout, medios y memoria

La matriz conserva nodos DOM por página, perfiles, imágenes y bytes reales CDP. Home ronda3677–3782 nodos según ancho y estado; profundidad máxima observada22. Los subárboles más grandes se registran en evidencia. No se recomienda eliminar contenedores semánticos ni duplicar contenido responsive solo para bajar un contador.

Overflow: scrollWidth1507con viewport1440 y1059con = 1024 en varias plantillas. La heurística de candidatos no identificó el causante: podría implicar off-canvas/embeds/ancestros. No aplicar overflow:hidden global para esconderlo.

La recolección de imágenes registra currentSrc, srcset, sizes, dimensiones naturales/renderizadas y transferencias CDP por salto. Presencia en DOM no prueba descarga, ni ésta decodificación. No se demostró una doble descarga general de mobile y desktop. Las imágenes fuera de viewport no son por sí mismas recursos inútiles; se exige correlación por URL y estado. Los ahorros de Lighthouse son estimaciones solapadas.

Sin JS hay enlaces y productos en el HTML inicial (home22 productos, categoría4, PDP5 contando relacionados), pero imágenes visibles sin cargar en las capturas. Esto no prueba que Google ignore el contenido. Autoplay, pausa fuera de viewport/pestaña y lectura de iframe requieren validación adicional: la política POST bloqueada puede interferir con proveedores. Se guardaron snapshots puntuales de heap/DOM; no constituyen una prueba de fugas de memoria.

## 10. Trazas, CSS, JavaScript y terceros

DevTools MCP real ejecutó open/snapshot/network/trace y analizó CLSCulprits, ForcedReflow y LCPBreakdown con perfil aislado/allowlist. El trace bruto fue efímero; se conservaron respuestas e insights en el run, no se afirma una exportación de trace que no existe. MCP tiene CrUX automático deshabilitado: su nota “n/a” no invalida los datos consultados directamente por API.

El mayor clúster del segundo trace afecta un VIDEO de YouTube, score0.3563; el insight no identifica una raíz. El contrafactual mantiene el poster y bloquea únicamente www.youtube.com: CLS mediano0.068en = 3 muestras frente a 0.449en = 3originales. Es una intervención diagnóstica que elimina funcionalidad en el navegador; no una mejora desplegada, prueba de UX conservada ni efecto de campo.

ForcedReflow atribuye trabajo a `featured-collection.js:141`, vanilla-adapter y funciones de reseñas. Los tiempos padre/hijo no se suman para inventar impacto. Googrev aparece dos veces, la segunda con cache=memory: no implica dos transferencias completas. Investigar iniciadores/frames y ejecución antes de consolidar apps. No retirar LS, tracking ni código por Coverage de una navegación.

Hay CSS bloqueante (estimaciones móviles cercanas a 0.9–1.1 s según página). Carga condicional o inicialización diferida requieren consumidores y estados comprobados; evitar FOUC y nuevas dependencias. Las tareas largas del observer de QA incluyen trabajo de proyección DOM/SEO: no se usan como presupuesto limpio de aplicación.

## 11. SEO y contratos comerciales

**Discrepancia principal de precio:** PRO AIR muestra10490MXN y declara13990 en WebPage.mainEntity.offers; baterías muestra1290y declara1490. Ambos coinciden con el compare-price tachado y se repiten en HTML inicial/DOM. No se cambió ningún valor ni se verificó un cargo de checkout. Es distinto de D010 sobre productos relacionados: que esas tarjetas enlacen su propia PDP no demuestra una canonical incorrecta del producto principal.

Blog página2 devuelve200 y 12 URLs de artículos adicionales, sin solapamiento con las12de la primera página, sin JS, pero su canonical apunta a/blog/. Google recomienda URL/canonical propias para páginas distintas de una secuencia; se debe verificar el mecanismo soportado de Tiendanube antes de proponer cambios. La flecha Anterior desactivada sin href no demuestra imposibilidad de descubrir páginas posteriores.

404real: title vacío y JSON-LD inválido confirmado; corregir en origen futuro, sin agregar otro script para ocultarlo. Búsqueda, carrito y cuenta están bloqueados para Googlebot en robots observado; ausencia de noindex meta no demuestra que estén indexados. Sitemap devuelve200 y 31 URLs. No se consultó GSC ni Merchant Center, ni se afirma indexación o elegibilidad confirmada.

El constructor de packs, carrito vacío y formularios públicos se inspeccionaron sin envío. No se probaron carrito lleno, cupones, cálculo de envíos, compras, login real, checkout o stock privado. Las optimizaciones futuras deben conservar precio/variantes/stock/slots/eventos/cart nativos.

Fuentes técnicas: [Google Product/Offer](https://developers.google.com/search/docs/appearance/structured-data/merchant-listing), [paginación Google](https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading), [WCAG nombre/rol/valor](https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html), [CLS](https://web.dev/articles/optimize-cls).

## 12. Consejo Claude + Codex

Las propuestas iniciales del consejo integral se generaron independientemente sobre el mismo snapshot factual. Después hubo contraste, seis preguntas y seis respuestas: nueve objeciones. Ambos terminaron prefiriendo una matriz plantilla×componente y rechazaron limitar todo a la home. Ninguna opinión constituye QA ni permiso de implementación.

Claude priorizó inicialmente video/home, blog, terceros/CSS y accesibilidad. Codex cuestionó esa cobertura, exigió incluir productos, packs, categorías y404, y advirtió sobre beneficios no medidos, geometría cero y diferencias entre fuentes. Claude retiró su alternativa limitada a home y corrigió estados pass sin evidencia a unknown. Permanecen objeciones que bloquean implementar: sincronización de fuentes, causa precisa y validación funcional de cambios propuestos.

La nueva evidencia CrUX de PRO AIR se revisó de forma acotada por ambos. Un intento de Claude fue rechazado por un recommendation ID que no refería a una alternativa incluida; JSON válido no significó contrato semántico aprobado. Se conservó el resultado válido de Codex y se realizó una recuperación única de Claude, sin cambiar a CommandCode ni inventar participación. La discrepancia de precios se sometió a un segundo anexo factual breve, sin repetir todo el debate. Resultados completos en [integral-council.json](integral-council.json).

La revisión incremental de precios fue aceptada por ambos tras corregir el alcance de referencia de archivo del contexto; los dos intentos previos rechazados no se contaron como aprobación.

## 13. Backlog y estrategia

| ID | Prioridad | Propuesta | Estado |
|---|---|---|---|
| RHI-001 | P1 | Offer.price principal usa el importe anterior en dos PDP | confirmed_discrepancy_pending_authorization |
| RHI-002 | P1 | LCP móvil en PDP y blog: separar laboratorio de experiencia real | needs_evidence |
| RHI-003 | P1 | Primera imagen visible del blog se descubre tarde | needs_evidence |
| RHI-004 | P1 | CLS desktop y carga del reproductor de YouTube | needs_evidence |
| RHI-005 | P1 | Trabajo JS de terceros y revisiones repetidas | needs_evidence |
| RHI-006 | P2 | ARIA, contraste y nombres accesibles compartidos | confirmed_defects_pending_authorization |
| RHI-007 | P2 | Headings y landmarks: categorías sin H1 y footer redundante | confirmed_defects_pending_authorization |
| RHI-008 | P2 | Overflow global y foco con geometría cero | needs_evidence |
| RHI-009 | P2 | Semántica e interacción del armado de packs | confirmed_defects_pending_authorization |
| RHI-010 | P2 | SEO de paginación y página404 | confirmed_output_issues_pending_authorization |
| RHI-011 | P2 | CSS bloqueante, selección de medios y JavaScript deshabilitado | needs_evidence |
| RHI-012 | P3 | Activar gates y vigilancia continua tras aprobar metodología | proposed_not_enforced |

El [ADR-RHINO-002](ADR-RHINO-002.md) registra la estrategia y las condiciones pendientes. Cada ficha incluye evidencia, URL, componente/archivo candidato, causa/hipótesis, impacto estimado, riesgos, alternativas, dependencias, prueba antes/después y reversión en [integral-backlog.json](integral-backlog.json). No hay parche en el tema. El ADR queda en **needs_evidence para implementación**: el diagnóstico puede revisarse, pero no hay autorización ni validación de un cambio.

## 14. Línea base y Performance Regression Gates

[performance-baseline.json](performance-baseline.json) conserva6 perfiles de laboratorio y44 perfiles de recursos/DOM de navegador con fuentes/hashes. [regression-gates.json](regression-gates.json) define condiciones, estados y presupuestos prospectivos. **Es política propuesta, no un hook de enforcement implementado ni una protección CI activa.** No se presenta documentación como funcionalidad ejecutada.

Los objetivos de campo son LCPp75≤2.5 s, INPp75≤200 ms, CLSp75≤0.1, por ámbito y periodo. Los límites de regresión son distintos: tolerancias por perfil basadas en mediana/MAD y mínimos absolutos; recursos/DOM con márgenes explícitos. Con n = 3el baseline es preliminar para bloqueo estadístico. Se propone≥5 muestras, contraste direccional y corrección múltiple antes de bloquear automáticamente por regresión.

Estados previstos: passed, regression_detected, inconclusive, insufficient_evidence y blocked. Actualmente no existe candidato posterior: **insufficient_evidence para comparación de regresión**. No hubo optimización ni comparación antes/después válida. Una política de red diferente, counterfactual, sin JS o versión/CPU/red/caché desconocidas impide usar una diferencia como regresión. Tres comprobaciones reales offline del comparador existente rechazaron fuentes diferentes, reuso de la misma observación y condiciones Google incompletas. Esto verifica elegibilidad de comparación, no el hook de enforcement ni un test estadístico. Un modelo no puede ignorar un gate crítico activado. Falta implementar/verificar ese hook con QA existente en la fase autorizada.

## 15. Vigilancia continua propuesta

Antes/después de cambios: baseline y QA manuales equivalentes. Tras publicación humana autorizada: medición remota controlada, sin asumir que PSI mide un diff local. Revisión semanal de CrUX/History; auditoría mensual o al agregar apps para recursos, DOM, accesibilidad y terceros. Toda automatización externa, cuenta, cadencia y consumo deben aprobarse antes de activarse. No se creó cron, GitHub Action remoto ni consultas periódicas.

## 16. Pruebas, cobertura y pendientes

Pruebas reales de esta fase:50 capturas/estados de16 URLs, axe y seis breakpoints en las tres páginas principales, sin JS/reduced motion, AX/CDP/Tab,8auditorías SEO offline,10 muestras PSI, CrUX por URL/origen y2históricos,18 muestras Lighthouse local y3 contrafactuales, dos trazas MCP y sus insights. Los fallos permanecen fallos; el carrito/checkout real no se declaró aprobado. Evidencias fechadas y hashes en [integral-evidence.json](integral-evidence.json).

Pendientes materiales: todas las URLs/variantes del catálogo, interacción comercial con datos reales, lector de pantalla humano, origen exacto del overflow, prueba funcional de video fuera de la política POST, sincronización de fuente/despliegue, muestras PSI repetidas, trazas limpias de memoria/tareas largas, GSC/Merchant/Rich Results externos y hook de regresión. No se informa100%de cobertura.

## 17. Entrega y control de cambios

Se añadieron únicamente informes, baselines, política de gates y scripts locales de diagnóstico. Se preservaron la auditoría histórica y el discovery. El tema y producción no recibieron parches ni operaciones push/watch/publish/pull/clone/fork. Las API Keys no se enviaron a los agentes ni se guardaron en estos informes. Los callbacks de medición no contienen credenciales de clientes. Los originales extensos, capturas y respuestas del navegador permanecen bajo reports/runs ignorado por Git.

La siguiente fase requiere revisión del diagnóstico y autorización concreta del alcance de implementación; este informe no la concede.
