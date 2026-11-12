# Rhino — operaciones preparadas y validación incremental

**Actualización posterior:** [paquete definitivo de autorización de paginación](publication/README.md). Hashes remotos reconfirmados, respaldo nuevo, cinco muestras locales por dispositivo y revisión final real de Claude aprobada exclusivamente para fuente/preparación de solicitud. Paginación lista para pedir autorización específica, sin push ejecutado. Menú pendiente del respaldo del propietario; blog sin cambios y consulta aún no enviada. El contenido siguiente conserva el checkpoint previo.

12 noviembre2026. **Sin cambios al tema ni a producción.** Se conservaron el ADR, v2, candidatos posteriores y todas las pruebas. No se repitieron Google Inspection, Search Analytics, sitemap ni discovery.

## 1. Menú: vía oficial y procedimiento manual

[Procedimiento exacto](menu-manual.md). Se confirmó que la CLI gestiona temas, no menús. En el índice oficial de AdminAPI consultado no encontré un CRUD de navegación; el webhook `navigation/updated` no es una API de administración. No se localizaron exportaciones de menú conIDs documentadas en la ayuda consultada; no se afirma inexistencia universal de esa función.

La vía documentada es **Tienda en línea > Menús**, sobre el menú existente referenciado como `footer`. Su presentación en Rhino se llama «Más información». Los cuatro enlaces actuales se conservan íntegros y solo se proponen Contacto y Sobre Rhino al final.

El usuario confirmó que no tiene una exportación o integración administrativa identificada. No se buscaron cookies, no se leyó una sesión privada ni se inventaron endpoints. El identificador `footer` del tema está comprobado; no se obtuvieron identificadores administrativos de cada elemento ni se los inventó.

Antes de modificar: respaldar desde el administrador el menú completo (campos, orden, jerarquía, URLs yIDs si están expuestos); cotejar duplicados y cambios ajenos; revisar la limitación si losIDs no están disponibles. No basta la captura pública para llamarlo exportación completa. Ningún botón Agregar/Guardar debe pulsarse durante la preparación: puede publicar inmediatamente.

### Vista temporal, no modificación de menú

Se probó añadir solo los dos enlaces al DOM de la página publicada, con el footer/estilos/JS existentes, en360/390/768/1024/1440/1920. No se guardó el menú, no es HTML inicial posterior a una aplicación y no es una medición de rendimiento. Se bloquearon medios en esa prueba para evitar descargas de video irrelevantes.

- Se conservaron los cuatro destinos y no se encontraron duplicados de los dos nuevos.
- En escritorio no hubo desbordamiento ni recorte. Contacto→Sobre funciona con Tab.
- En móvil el acordeón abre con Enter y los dos enlaces quedan en la secuencia de foco. El control móvil comparando cuatro/seis entradas, sin enfocar previamente un enlace colapsado, no mostró recortes ni overflow.
- La primera prueba señaló un recorte; se conservó. Esa corrida también había forzado foco sobre un enlace colapsado. La comparación posterior descarta afirmar un recorte general causado por añadir las dos entradas, pero no demuestra por sí sola toda la cadena causal del primer resultado.
- **Problema previo registrado:** el footer móvil colapsado permite foco en enlaces ocultos. La implementación responsable es el snippet personalizado `footer-rhino.tpl`, no un defecto atribuido universalmente a Tiendanube. Agregar enlaces no corrige ese problema. Debe revisarse por separado y comprobarse en QA posterior; no se certifica WCAG.

[Resultados y controles](menu-preview-results.json). La fuente SSR actual recorre `menus[menu_2_id]`; por ese contrato se **espera** que las nuevas entradas aparezcan en HTML inicial al guardar el menú correcto. Eso aún no está observado después de una modificación, porque no se ejecutó ninguna.

Claude considera coherente el procedimiento, pero no aprobó aplicarlo sin respaldo y autorización. El procedimiento manual está preparado; la operación permanece sin ejecutar.

## 2. Paginación: v2 conservado, problemas corregidos en candidato separado

[Diff final revisable](pagination-final-candidate.patch) · [hashes](pagination-final-manifest.json) · [operación propuesta](pagination-operation-proposal.json).

El v2 original sigue intacto. Se preparó una continuación separada:

1. Botón nativo de carga, deshabilitado en HTML y habilitado después de inicializarLS; navegación por enlaces separada y visible, sin interceptar sus clics.
2. Foco: una prueba con elLSpublicado detectó que el v2 dejaba foco enBODY tras activar con teclado. La continuación mantiene un destino estable durante espera/error y enfoca el primer producto nuevo tras éxito, solamente si el usuario no movió el foco entretanto. Con puntero no fuerza foco.
3. Guarda de numeración: se comprueba página positiva y se usa la protección de variantes/cursor del tema. Cuando no corresponde numerar se muestran Anterior/Siguiente, sin aritmética sobre un valor ausente.
4. Nombre de navegación distinto del botón: «Página: productos», compuesto con traducciones existentes. No se añadieron claves ni archivos de idioma. El cambio visible sigue siendo una fila de destinos a páginas independientes, no una promesa de siguiente carga del acumuladoJS.

### Pruebas nuevas y límites

[Prueba del controlador real](native-component-results.json): se utilizó el `LS.hybridScroll` publicado con SHA256 `9dc0e47a547cf88dc0a2f11f416f7338b594a91a7bd2021b775a36b131ccf4a3` y CSS publicado. Se retuvo elJSgeneral para evitar doble inicialización; se ejecutó el inicializador candidato sobre unDOM de prueba. Las respuestas de páginas posteriores fueronfixtures interceptadas localmente: **ninguna solicitud ficticia de páginas3–7 alcanzó producción**.

- Seis anchos: botón habilitado, tecladoEnter/Espacio activa el handler nativo, spinner aparece/desaparece,IDs únicos y foco estable.
- Caso de error explícito a390: no se añadieron productos y el foco permaneció en el enlace funcional.
- Caso adicional a1024: el usuario movió el foco durante la espera y la respuesta no se lo robó.
- Puntero a1440: no se impuso foco a un producto nuevo; el árbolAX mostró roles/nombres de botón, navegación y enlace.
- El primer harness v2 agotó espera al llegar a768; se archivó sin aceptarlo. El harness posterior controló explícitamente el espacio de scroll. No se atribuye ese fallo aislado al rendimiento de la tienda ni se mezclan sus resultados como muestras comparables.

La tienda real conserva la evidencia12→14IDs y la ruta real `/productos/page/2/` con200/HTML/canonicalpropio. No hay tercera página real demostrada y no se inventó una. Lasfixtures de varias páginas sirven para comprobar estados del controlador, no para acreditar contenido comercial existente.

El flujo con filtros/orden no está expuesto en la captura/configuración actual: no se inventaron parámetros para simular que se probó. Las URLs se toman de plataforma yLS conserva su codificación existente. Si se habilitan filtros, variantes como productos o cambian las cards, hay que revalidar ese contrato. El grid real observado tenía unID por tarjeta; la prueba no certifica futuras estructuras anidadas.

### Validación nativa del servidor, sin subir archivos

Se descubrió y usó **`tiendanube theme check --theme-id 14828608`**, comando oficial de validación sin guardar. El código de laCLI confirma que comprueba sintaxisTwig, schemas y tamaño mediante `/files/validate`.

Para no aplicar el candidato en la carpeta original, una vista de lectura virtual sustituyó solo esos dos archivos dentro del proceso de laCLI. No se copiaron credenciales. El transporte solo permitióGETy unPOSTdevalidación con esos dos hashes; cualquierPATCHuotra escritura quedó bloqueada.

Resultado: **All 2 file(s) are valid**, exit0; servidor `valid:true`, `errors:[]`. La comprobación posterior de lectura confirmó398archivos en sincronía con los originales. Los seis hashes protegidos del tema siguen intactos. [Recibo](native-template-validation.json).

Eso cierra la validación de guardado/sintaxis. **No es un render de página ni una confirmación de indexación.** El HTML inicial del candidato todavía no está publicado.

### Rendimiento y consumidores

El controlador verificó que el resto de `store.js` es idéntico byte a byte. La búsqueda de consumidores muestra la selección del padre `.js-load-more`, no una dependencia del hijo `<a>`; el inicializador tiene una invocación en el módulo actual. No se reescribióLS ni se añadieron bibliotecas, imports, timers u observers. No se afirma idempotencia general ante cargas duplicadas externas del módulo.

Cambios de tamaño del código fuente: `store.js` +1.174bytes sin comprimir; estimacióngzip local +287bytes. Plantilla+886bytes no equivale directamente a bytesHTML entregados. No son transferencias reales medidas. [Integridad y tamaños](source-integrity-and-size.json).

La comparación de LCP/TBT/CLS y puntuaciones mobile/desktop requiere perfiles equivalentes en la versión que realmente se publique. No se hicieron consultasPageSpeed redundantes sobre la versión antigua para presentarlas como resultado del candidato, ni se afirmó90+.

## 3. Canonical: consulta lista, sin cambios ni mensajes enviados

[Consulta preparada a Tiendanube](consulta-tiendanube.md) · [proyección de evidencia pública](blog-support-evidence.json).

Se reutilizaron las lecturas de páginas2,3,8:200, listas diferentes de12/12/2artículos, canonicalhacia/blog/. Los estadosGSCde lasURLs exactas no prueban la causa de su no reconocimiento ni el canonical elegido porGoogle.

El borrador pregunta si ese comportamiento es intencional y qué mecanismo oficial permite canonicalpropio por página, preservando un único tag. Se mantienehead-tags sin añadir otrocanonical ni modificarlo conJavaScript. El propietario revisa qué información enviar, incluido elIDtécnico opcional. No se contactó a terceros.

## Revisión y gates

[Revisiones independientes](independent-reviews.json). Claude revisó los archivos completos, el diff y las nuevas pruebas. Ya no encontró un defecto de fuente demostrado en los hashes finales. Aceptó que la validación nativa cierra la condición de sintaxis. Conservó `blocked` para implementación/aceptación general; no se convierte una aprobación parcial en permiso de producción.

Codex cuestionó la exigencia de tener render publicado antes de presentar una propuesta cuando el propietario solo admite producción. Claude distinguió explícitamente:

- **Antes de presentar/ejecutar:** archivos y hashes exactos, respaldo, diff, validación de guardado, baseline apropiado, procedimiento de reversión y autorización específica. Los aspectos visuales «Página: productos» y botón disabled sinJS deben estar declarados para la revisión del propietario.
- **Después de una publicación específicamente autorizada:** hashes publicados, HTMLinicial real con valores/enlaces correctos,AX/teclado/noJS,seisancho y rendimiento equivalente. Estas condiciones no pueden darse por pasadas confixtures.

El paquete puede revisarse como propuesta exacta, **no ejecutarse**. Antes de cualquier aplicación futura se revalidan los hashes remotos y se toma o confirma un baseline realmente comparable; no se gastan mediciones preventivas ahora si todavía no se ha decidido publicar. El menú requiere además su respaldo administrativo o revisión expresa de la limitación manual.

La reversión propuesta restaura únicamente los dos archivos respaldados si los remotos conservan los hashes posteriores aprobados; ante cambios ajenos se detiene. Necesita autorización específica, igual que la aplicación. No se modifica el layout ni se toca el arreglo previo de breadcrumbs.

**Resultado de esta fase:** procedimiento manual y consulta preparados; candidato validado por el servidor y revisado; fuentes, v2 y producción preservados. No hay autorización ni modificación de producción. No se reinició el discovery ni el consejo completo, no se ejecutó el crawler pendiente y no se instalaron integraciones nuevas.
