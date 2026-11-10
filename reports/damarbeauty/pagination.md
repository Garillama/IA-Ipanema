# DaMar Beauty — paginación: resultado técnico y cambio local

Verificado el10 de noviembre de2026. **Se cerró el ciclo del control de teclado en alcance local; la paginación SEO completa sigue `needs_evidence`.** No se cambió ni publicó la tienda. [ADR actualizado y19 objeciones históricas](pagination-adr.json) · [Diff local](pagination-local.patch).

## Decisión y alcance

Claude y Codex retomaron ADR-7a95be882add y su evidencia, sin heredar autorización. Revisaron por separado fuentes y nuevas capturas, contrastaron sus conclusiones y limitaron la implementación a una corrección demostrable. Se conserva `LS.hybridScroll`, la configuración `infinite`, el lote de12 productos y el umbral nativo de60 antes del control manual. No se crea otro motor ni se modifican filtros, datos comerciales, CSS, JavaScript o schemas.

**ADR-DMR-PAG-20261110-01: `needs_evidence` para la solución SEO integral.** Se descarta añadir solo `href` al control: el helper no cancela su navegación y el enlace quedaría obsoleto tras los lotes. Tampoco se adoptan enlaces generados solo por JS ni un cambio automático a `classic`. La navegación SSR independiente es un candidato para investigación, no una implementación aprobada: faltan el diseño de convivencia con append, cursores y renderizado real.

La subdecisión **ADR-DMR-PAG-20261110-BUTTON** sí autorizó y aceptó una corrección local independiente:

| Elemento | Antes | Después local |
|---|---|---|
| Control de carga, dentro de `.js-load-more` | `<a class="btn btn-primary">` sin href; Tab no lo alcanza | `<button type="button" class="btn btn-primary">`; Tab y Enter/Espacio activan el handler nativo |
| Fuente | Dos etiquetas de ancla | Dos etiquetas de botón; +24 bytes de fuente sin comprimir |
| Integración | Clic registrado en el contenedor padre | Mismo contenedor, clases, traducción y spinner; sin otro listener |

Archivo: `snippets/product-list/pagination.tpl`. Se mantienen todas las directivas Twig y la rama clásica, utilizada también por blog. La corrección no añade enlaces rastreables: **sin JS sigue pendiente la navegación del listado**. No es una certificación de accesibilidad del catálogo.

Codex produjo el contenido completo con hash previo. El controlador comprobó que coincidiera exactamente con el reemplazo aprobado, aplicó una transacción con backup y ejecutó QA. Claude revisó independientemente el diff real. Ambos evaluaron los resultados posteriores. Codex pidió el baseline/diff que faltaba en su primer paquete de QA; se aportó y se repitió solo esa evaluación, conservando la revisión válida de Claude.

## Qué evidencia se resolvió

La captura actual del helper coincide con la anterior. Su listener sobre `.js-load-more` usa `.one('click')` sin `preventDefault`; actualiza `history` pero no un href del DOM. La precarga nativa existe antes del clic manual. No se modificó esa implementación de plataforma.

| Prueba real, solo lectura | Resultado |
|---|---|
| `/lo-mas-nuevo-lippies/page/2/`, sin JS | HTTP200,11 tarjetas, canonical propio; mismo conjunto que el lote nativo posterior a las12 iniciales, sin intersección |
| `/productos/page/2/`, sin JS | HTTP200,12 tarjetas, canonical propio; coincide con el lote incremental nativo, sin intersección con página1 |
| `/productos/page/3/`, sin JS | HTTP200 y12 tarjetas; URL derivada de una solicitud nativa observada |
| Enlaces de paginación en páginas posteriores | Ausentes en las muestras; la condición `pages.current == 1` explica la falta de continuidad |
| Solo añadir href, experimento DOM | Navega a `/page/2/`; falla la conservación del flujo infinite |
| Guardar el clic, experimento DOM | Mantiene pathname y añade132→144 tarjetas; confirma que la interceptación importa, pero no resuelve href obsoleto, cursores o SSR |
| Filtro nativo de marca y ordenamiento | Parámetros conservados en solicitudes posteriores; ocho comprobaciones de filtros aprobadas, incluidas las de Blush |
| Filtros locales Blush | Aplicación, recarga, Forward y Escape/retorno de foco comprobados; no son prueba de filtrado de servidor |
| Carruseles de cards | Dos instancias con2 y7 slides cambiaron de índice mediante `slideNext`; no certifica todos sus controles o gestos |
| Responsive original | Sin overflow horizontal observado a360,390,768,1024,1440 y1920px; no equivale a QA completo del diseño modificado |

Se detectaron **cuatro IDs repetidos antes del reemplazo DOM en una muestra desktop**. Los mismos cuatro permanecieron tras la activación: el prefijo se conservó y las12 tarjetas nuevas eran únicas y no se solapaban con las anteriores. Una repetición nativa independiente y las dos muestras posteriores no mostraron duplicados. Su causa permanece no determinada; no se atribuye al botón ni se declara que todo el catálogo esté libre de duplicados.

Las URL se obtuvieron de requests nativos; no se inventó `?page=`. Las muestras tienen `data-vap-enabled=false` y `page_next=null`, por lo que no prueban el flujo de variantes como productos. No se activó una configuración comercial para fabricar evidencia.

## QA del cambio local

**17 comprobaciones del alcance local aprobadas.**

- Tab + Enter a1440px y Tab + Espacio a390px añadieron72→84 tarjetas con el motor nativo, manteniendo el pathname y sin duplicados en esas muestras posteriores.
- Geometría y estilos computados del control coinciden. Dos comparaciones visuales antes/después de la simulación DOM: cero píxeles distintos a1440×900 y390×900, umbral12, ratio máximo0,005 y sin máscaras.
- QA `source` aprobado: inventario/schema y estabilidad de fuentes. No es compilación/render de Twig.
- **`tiendanube theme check --theme-id 14748767` aprobado: “All1 file(s) are valid”.** La guardia permitió dos GET y un POST HTTP200 a `files/validate`, con el único archivo y hash declarados. Rechazó métodos de escritura de archivos; no hubo PATCH/PUT/DELETE, guardado remoto ni publicación. Es validación nativa de archivo, no render de sus datos o comportamiento.
- Claude aprobó independientemente el diff; las evaluaciones finales de Claude y Codex aprobaron exclusivamente el alcance local, manteniendo SEO global pendiente.
- Se comprobaron los hashes de todo el árbol no oculto, reconstruyendo el hash agregado previo con el único snippet original: **470 archivos intactos, un archivo cambiado, cero añadidos y cero eliminados**. Se conservan cambios previos ajenos. `git apply --reverse --check` del patch pasó sin ejecutar la reversión.

Transacción `d284e16a7108490ca29b4ac123fabb18`, un intento, estado `accepted` para el ámbito local comprobado. Backup privado conservado. No implica aceptación de producción ni de la solución SEO.

Las pruebas del navegador reproducen el reemplazo exacto de etiquetas sobre la página nativa actual; **no renderizan el Twig local modificado desde Tiendanube**. Esta limitación figura en el QA, ADR y revisión. El chequeo nativo agrega evidencia de aceptabilidad del archivo, sin eliminar esa distinción.

No se añadieron recursos o dependencias. La mutación DOM del experimento previo duró0,4–0,5ms en dos muestras; es tiempo del harness, no ahorro de carga. No se midió mejora de LCP/INP/CLS ni se atribuye al botón la variación del rendimiento de la tienda.

## Pendientes que bloquean la solución SEO completa

1. Renderizar una navegación SSR propuesta en un entorno Tiendanube aislado autorizado, con categoría, búsqueda, páginas intermedias/última, vacío y filtros. La referencia14748767 es la instalación publicada; su URL de preview no aísla escrituras. No se usó otra instalación, clon o borrador sin autorización.
2. Resolver el destino de los enlaces tras los appends sin duplicar controles, ocultar innecesariamente el contenido o reutilizar un href obsoleto; comprobar teclado, foco y clics modificados.
3. Verificar `page_next`/`page_prev` y `page_offset` con un caso real de variantes como productos. Los datos actuales no permiten certificar esa rama.
4. Comparar coste de la propuesta completa con perfiles equivalentes. El experimento de134 bytes del guard de clic no representa una implementación SSR lista.
5. Investigar, dentro de otro alcance acotado, los duplicados ocasionales ya presentes en el flujo nativo. No se deduplicó el catálogo con una lógica paralela.

No se comprobó indexación con Google, todo el catálogo, AA completo ni rendimiento de campo. El botón local resuelve una parte real del problema; **no se declara cerrado el objetivo SEO**.

## Evidencias y agentes

Directorio de esta ejecución: `reports/runs/damarbeauty/20261110T163610-pagination-resolution-925f26ee/`, ignorado por Git. El ADR estable conserva hashes y rutas exactas:

- `browser-baseline/observation.json`: HTML inicial, DOM y helper nativo.
- `browser-behavior/behavior.json`, `browser-advanced/advanced.json`, `browser-native-repeat/behavior.json`: URLs, continuidad y experimentos.
- `filter-checkpoint.json`: ubicación de los ocho checks de filtros.
- `browser-button-probe/` y `browser-button-after-local/`: simulaciones, geometrías y capturas antes/después.
- `agent-deltas-independent/`, `agent-deltas/`: investigaciones y contraste focalizado de Claude/Codex.
- `button-implementation-proposal.json`, `button-independent-review.json`, `button-final-*.json`: implementación y evaluaciones, incluido el bloqueo inicial de Codex por falta de baseline.
- `button-baseline-qa.json`, `button-after-qa.json`, `button-acceptance.json`: comparación y aceptación limitada.
- `native-check.json`, `native-check-network.json`: validación real, métodos y estados sin cabeceras ni secretos. Dos fallos locales previos del lanzador/guardia se conservaron; se corrigieron antes de la solicitud válida, sin reintentar403/429 ni ampliar permisos de escritura.

Nueve invocaciones reales, con los perfiles equilibrados existentes `claude-sonnet-5-5` y `gpt-6.1-sol`, esfuerzo `medium`; cero CommandCode y ningún failover. Claude reportó USD1,4162742; Codex no emitió coste monetario utilizable. El coste conjunto no se inventa. Cada invocación conserva duración, contexto y contadores observados en el ADR JSON.

Referencias consultadas: [paginación de Google](https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading), que distingue carga incremental de descubrimiento por enlaces; [listado de Tiendanube](https://tiendanube.dev/themes/classic-themes/theme-features/product-listing), ejemplo oficial de temas clásicos y no certificación del runtime seccionable. Para esta tienda prevalecen los archivos actuales y la ejecución observada.
