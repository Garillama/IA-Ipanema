# Rhino — cierre acotado de los tres pendientes

**Continuación posterior:** [operaciones preparadas y validación nativa](operations/README.md). El v2 de esta fase se conserva; una continuación separada corrigió foco/cursores y pasó `theme check` del servidor sin guardar archivos. El menú sigue sin modificar y su procedimiento manual está preparado. El texto siguiente conserva el checkpoint anterior.

**Estado: defensa pendiente recuperada; diagnóstico ampliado; candidato sin aplicar y todavía no apto para publicar.** No se volvió a hacer discovery ni se repitieron las13inspecciones o las170filas de rendimiento. No se modificó el tema, no hubo push/watch/publish ni clones/staging de tienda.

## Consejo recuperado

La única intervención nueva del consejo fue la defensa pendiente de Codex. Se conservaron ambas propuestas, ambos contrastes y la defensa de Claude. Se verificó el mismo binding, el mismo SHA del prompt congelado (`b4c619ab5fd521ad1561552e393bbbbbeffeeef3d3ef8dca02de7f7ac6c15b29`), los permisos de solo lectura y la salida de los procesos anteriores. El nodo original de Codex nunca había iniciado proceso.

El recuperador automático rechaza el checkpoint agotado; no se alteró ese comportamiento ni su presupuesto. Bajo la nueva petición explícita se ejecutó **una continuación acotada de una llamada**, sin reintentos/fallback, usando el worker y el validador existentes. Se preservan los seis intentos del run anterior y la séptima invocación queda registrada por separado. No se cambiaron el orquestador, modelos, AGENTS ni políticas.

[Cobertura y motivos del ADR recuperado](council-recovery.json): propuestas, contraste y defensas completos; cuatro preguntas y cuatro respuestas. **No hay aprobación de implementación.** Quedan respuestas `needs_evidence` y el agregador rechaza que Codex retire una alternativa ajena. No se elimina esa condición, no se repara una respuesta para convertirla en aprobación y no se afirma consenso. El ADR anterior queda intacto y la continuación lo referencia.

## 1. Paginación: diagnóstico y candidato

Evidencia válida reutilizada: `/productos/` sirve12productos; el scroll nativo solicita `/productos/page/2/` con resultados parciales y añade dosIDs únicos, conservando los doce iniciales y su orden. La ruta completa responde200, muestra esos dos productos y canonical propio. La tienda actual tiene14productos en sitemap; no se inventa una página3 para una prueba de continuidad que el catálogo actual no ofrece.

El control actual es un `<a>` sin href. No aporta por sí mismo el enlace HTML a página2, aunque los14productos tienen rutas alternativas desde home. `LS.hybridScroll` se suscribe al padre `.js-load-more`; no cancela el default de un enlace. Añadir href sin más puede navegar y cargar por JS simultáneamente.

### Revisión y corrección del candidato

Se descartó el primer candidato que añadía href más `preventDefault`: Claude solicitó cambios por doble acción con modificadores y tratamiento insuficiente de errores de carga. No se aplicó.

El [candidato v2 exacto](pagination-v2-candidate.patch) separa acciones:

- Botón HTML nativo para cargar más, habilitado después de inicializarLS. Enter/Espacio funcionan sin añadir handlers propios.
- Enlaces visibles numerados mediante `prev_link`/`next_link` ya calculados por la plantilla. No se construyen URLs ni se ocultan enlaces para robots.
- La navegación numérica sigue siendo una ruta a una página independiente aunque el scroll haya acumulado sus productos. No promete ser la siguiente carga del acumulado.
- Sin JavaScript queda el botón deshabilitado y la navegación por enlaces. Sin interceptar clics de esos enlaces, Ctrl/Cmd no dispara el control de carga.
- El ajuste `infinite` y el cuerpo deLS se conservan. La rama classic original no se modifica.

**Cambio visual declarado:** se añade una fila de enlaces de página con estilos nativos. No se presenta como diseño idéntico ni como cambio autorizado. Mantiene la composición y no cambia tipografía/configuración de otras secciones.

Archivos: `snippets/product-list/pagination.tpl` y `static/js/store.js`. [Hashes antes/después](candidate-manifest.json). Patch SHA256 `0e52661e81a0ab192e9bf8d345728fd6f5a6d2e679bad0b39571bb1a75f47cd6`.

Los tres respaldos de fuente se obtuvieron **desde producción14828608**, tienda7400935, con transporte nativo limitado a lectura. Coinciden byte a byte con el código local. La CLI informa398archivos en sincronía, sin añadidos/modificados/eliminados. [Verificación de respaldos](backup-verification.json). Copias completas privadas en el run de esta fase, no en el tema.

### QA y condiciones de publicación

- `node --check` v2 aprobado.
-48comprobaciones de DOM/teclado en Chrome real enfixtures, a360/390/768/1024/1440/1920: estado disabled inicial, foco del enlace sinJS, activación Enter/Espacio del botón, navegación con modificadores separada, y enlace disponible ante fallo simulado de inicialización. **LS está mockeado**; no es renderTwig ni QA definitivo de tienda. [Resultados](fixture-v2-results.json).
- Claude revisó el segundo diff y volvió a pedir cambios/evidencia. [Revisión y contraste factual del controlador](independent-review.json). Parte de sus objeciones eran falta de contexto: `prev_link`/`next_link` sí están definidos al inicio del archivo, y `.pagination-nav`/`.pagination-counter` existen en `style-async.css`. Estas comprobaciones corrigen hechos, pero no inventan una nueva aprobación de Claude.
- Siguen pendientes: valor real renderizado de los enlaces, label apropiado del nav, revisión final del diff, apariencia/estado disabled, seis anchos del tema real, teclado y errores de carga conLSreal, filtros/orden/variantes y medición comparable mobile/desktop. No se afirma que lasfixtures cierren esas pruebas.

**No es una propuesta lista para autorizar despliegue.** El candidato es revisable y sus respaldos/hashes existen, pero no pasa aún la revisión y los gates. No se solicita publicar un diff rechazado.

Reversión preparada para un eventual cambio autorizado: restaurar exclusivamente los dos archivos respaldados si los hashes remotos coinciden con los hashes posteriores aprobados; ante cualquier cambio ajeno posterior detener. No hacer restore global ni tocar contenido/configuración.

## 2. Canonical del blog: resultado concreto

Se conservaron los resultados de portada y página2. Únicamente se añadieron lecturas puntuales de las URLs **ya observadas en hrefs**:

| URL | HTTP | Artículos enlazados | Canonical declarado | Google, inspección de URL exacta |
|---|---:|---:|---|---|
| `/blog/?page=2` |200|12|`/blog/`|No reconoce esta URL; dato reutilizado|
| `/blog/?page=3` |200|12|`/blog/`|No reconoce esta URL; consulta nueva|
| `/blog/?page=8` |200|2|`/blog/`|No reconoce esta URL; consulta nueva|

Las páginas tienen contenido de artículos distinto y enlaces de secuencia. Las2consultas nuevas se hicieron por el gatewayGSC autorizado, sin repetir las13anteriores. No devuelven canonicalGoogle ni último rastreo para esas URLs. No se interpreta `UNSPECIFIED` como noindex, bloqueo de robots o error HTTP.

Google recomienda canonical propio para cada página de una secuencia: [documentación](https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading). El canonical observado merece revisión, pero **no está demostrada su causalidad en una exclusión** ni que impida descubrir/indexar los artículos. Canonical no equivale a una prohibición de rastreo.

La [documentación de Tiendanube](https://tiendanube.dev/es-AR/themes/sectionable-themes/seo) confirma que `head-tags` genera el canonical. No se comprobó un override soportado. No se añade otro canonical, no se modifica porJS, no se alteran los auxiliares `view=cards/tags` ni se sustituye todo head-tags.

Decisión: **no cambiar el canonical desde el tema por ahora**. Preparar una consulta técnica a Tiendanube con estas tres URLs, ejemplos200/contenido distinto, canonical observado y respuestasGSC. Pedir confirmación de comportamiento intencional y mecanismo soportado para canonical propio. No se envió ningún mensaje a terceros. No se garantiza indexación de paginaciones al corregirlo.

## 3. Contacto y Sobre Rhino: resultado concreto

Se reutilizaron las lecturas200, sitemap y GSC válidas. Ambas URLs están en el sitemap, tienen canonical propio,H1,texto principal y no mostraron meta/X-Robots-Tag restrictivos. Contacto tiene meta description vacía, mejora editorial secundaria; no prueba una causa de exclusión. No se inventa contenido.

- `/contacto/`: Google la conoce como descubierta, aún sin indexar.
- `/sobre-rhino-performance/`: no reconocida en la inspección exacta disponible.

La comprobación puntual actual de home volvió a dar200 y **cero hrefs hacia esas dos páginas en HTML inicial**. El encabezado “Contacto” del footer no es un enlace a/contacto/: sus destinos son email y WhatsApp. No se confunde texto visible con una ruta navegable. Este resultado también significa que esas rutas no están presentes en el HTML que recibe una sesión sinJS; no es prueba de orfandad de toda la web.

Fuente responsable: `snippets/footer/footer-rhino.tpl` renderiza `menus[menu_2_id]`; el segundo bloque de menú de `templates/layout/footer.json` selecciona `footer`, columna “Más información”. Los cuatro enlaces publicados son Privacidad, Cambios y garantía, Cookies y Envíos.

[Operación exacta propuesta](institutional-menu-proposal.json): añadir al menú nativo **Contacto → `/contacto/`** y **Sobre Rhino Performance → `/sobre-rhino-performance/`**, preservando los cuatro elementos actuales. Sin hardcodear enlaces en el tema, duplicar footer ni cargarJS/CSS adicional.

La instantánea pública de los cuatro destinos existe; **no equivale a exportar el menú completo con susIDs**. Antes de ejecutar falta ese respaldo nativo, aprobación independiente de la operación y autorización específica del propietario. El ejecutor de temas no es un editor de menús; no se inventa un endpoint privado para modificarlo. La reversión quitaría solo los dosIDs creados si conservan sus URLs/valores esperados.

Agregar estos caminos es una mejora justificada de descubrimiento, no prueba de que la ausencia de enlaces sea la causa del estadoGSC ni garantía de que Google indexará ambas páginas.

## Decisión y siguiente paso

La defensa pendiente está recuperada, el diff de paginación está preparado y fue objetado independientemente, y las soluciones de plataforma/menú están acotadas. **No se cerraron todas las condiciones para publicar.** Se conservan prioridadesP1para navegación de catálogo e institucionales yP2para canonical del blog. No se ejecutó el crawlerV4 ni se reconstruyó su infraestructura.

URLs concretas pendientes: `/productos/` y su ruta nativa/page/2/ para probar el candidato; `/contacto/` y `/sobre-rhino-performance/` para validar la futura navegación; blog?page2,3,8 para revisión de plataforma; páginas4–7 únicamente cuando haya que cerrar continuidad editorial. No se fuerza la indexación de variantes/URLsauxiliares.

El [control final](verification.json) verifica hashes y separa sintaxis/fixtures de revisión/QA pendiente. No se repitió PageSpeed para una versión no publicada, no se prometen mejoras deLCP/TBT/CLS ni90+, y ninguna simulación se presenta como validación final de producción.
