# Rhino Performance — corrección candidata de hero/LCP desktop

Fecha: 2026-11-17. Estado: **candidato local preparado; QA focalizado sintético aprobado; revisión independiente y validación Tiendanube pendientes. No publicado.**

## Causa confirmada

El HTML desktop capturado tenía dos imágenes independientes. La hero desktop servía un GIF transparente y `data-srcset`, sin prioridad; la variante móvil tenía `srcset` y prioridad alta aunque `d-md-none` la ocultaba en escritorio. En la captura desktop se descargaron las dos variantes y Lighthouse histórico detectó tarde la desktop en 5/5 muestras. Véase la [captura/análisis de producción](../../../runs/rhino-performance/20261117T-html-capture-authorized-03/offline-comparative-analysis.json) y el [informe de evidencia](README.md#capturas-autorizadas-y-límites) anterior consolidado en el historial.

Causa del template: `sections/hero.tpl` emite dos includes; si hay alternativa móvil, `desktop_lazy` siempre queda true. `snippets/image.tpl` convierte `image_lazy_js` en `data-srcset` y GIF transparente. `lazySizes` está configurado con `loadHidden:true`, así que `display:none` no garantiza que la imagen oculta evite descarga. Evidencia de producción: [HTML desktop](../../runs/rhino-performance/20261117T-html-capture-authorized-03/desktop-response-body.html), [waterfall y análisis](../../runs/rhino-performance/20261117T-html-capture-authorized-03/offline-comparative-analysis.json), [captura Lighthouse previa](../performance-first-correction-20261113T180949/README.md).

## Candidato

Archivos modificados exclusivamente:

- `sections/hero.tpl`
- `snippets/image.tpl` (helper compartido, rama nueva solo opt-in mediante `image_mobile_src`)

La hero con imagen móvil ahora pide una sola composición `<picture>`: fuentes mobile con `media="(max-width: 767.98px)"`, fuentes desktop como fallback, AVIF/WebP desde `resolve_media` y una sola etiqueta `<img>`/`alt`. La imagen móvil solo existe como fuente de ese `<picture>`; no hay segundo `<img>` oculto. La primera sección prioritaria marca `fetchpriority=high`; las posteriores usan `loading=lazy` y el class hook de LazySizes. Si falta la imagen desktop pero existe la móvil, el fallback desktop sigue siendo el placeholder nativo. Las rutas sin imagen móvil conservan el flujo existente. `templates/pages/home.json` permanece intacto y la hero sigue primera.

`snippets/image.tpl` tiene muchos consumidores, por eso el comportamiento nuevo está condicionado al parámetro opcional `image_mobile_src`; las llamadas anteriores no lo pasan. Los `<source>` reciben dimensiones propias y la rama art-direction no fija la proporción desktop en `<img>`. El [HTML Standard](https://html.spec.whatwg.org/multipage/embedded-content.html) y [MDN `<source>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/source) permiten dimensiones `width`/`height` para `<source>` dentro de `<picture>`, que el navegador usa para determinar el ratio seleccionado. El atributo `alt` es único en el `<img>`: las dos imágenes art-directed deben representar el mismo contenido semántico; la captura actual tenía `alt="Hero"` en ambas.

No se modifican `home.json`, JS, CSS, `store.js`, `pagination.tpl`, configuraciones de apps ni código de terceros. No se añadieron dependencias, preloads ni solicitudes en producción.

## Diff, hashes y respaldo

[Diff exacto](candidate.patch), SHA256 `e6d7edd9bb3590b0909cd71a9245bf5a92cbd7034f24fc57bb00389d0ec3f841`.

| Archivo | Base local | Candidato local |
|---|---|---|
| `sections/hero.tpl` | `36b7f21aed77378f5b5b378c74dd7768bd2717159a1f1d80ae70079fa80b5542` | `5362f1b4ddab56feabc95ad23486cc1b439b02d06a0479a2fcb8deb96fa8861c` |
| `snippets/image.tpl` | `9e6b1624ee75d6d0a9899d7af25cd799b1e59bde31962c98e4fea3aca404ed3b` | `f45641d2f4cd4e9fea775cf1aa19f806686130f79cb191e2a2140436919e178b` |
| `templates/pages/home.json` | `960f96de25d81f54fba64f40e796157bb559b478b51a3271cb7c2c06cb2a6bb3` | sin cambios |

Respaldo local íntegro: [`hero.tpl.base`](candidate-backup/hero.tpl.base) (`36b7f21a…`), [`image.tpl.base`](candidate-backup/image.tpl.base) (`9e6b1624…`). `git status` del tema contiene solo los dos archivos previstos.

## QA focalizado ejecutado

[`Prueba browser sintética`](tests/hero-responsive.browser.mjs) · [`resultados`](hero-responsive-browser-results.json): 32 escenarios y 231 aserciones, Chrome/Puppeteer local. Incluye 360, 390, 412, 768, 1024, 1440 y 1920 px; pareja desktop/móvil distinta; desktop-only; mobile-only con placeholder desktop; sin imagen; primera hero prioritaria y hero posterior diferida. Los casos usan solo URLs `fixtures.invalid` respondidas por interceptores locales (sin Internet). La rama diferida utiliza el código LazySizes del bundle local y fuerza su `unveil` en el fixture.

Resultado: todos los anchos seleccionan la variante esperada; cada caso produce exactamente una solicitud de imagen; `currentSrc` coincide con la única solicitud; ratio móvil 0.82 y escritorio 2.133; CLS del fixture 0; `alt` se conserva; la primera hero tiene `fetchpriority=high` sin `loading=lazy`; la posterior no obtiene prioridad alta y conserva `loading=lazy`.

También pasaron `node --check`, parseo JSON de `home.json` y `git diff --check`. **Estas pruebas no renderizan Twig ni validan la salida de Tiendanube.** No se ejecutó el validador nativo, no se hizo navegación posterior al cambio y no se midió Lighthouse. La selección de assets reales, `currentSrc`, estado visual y el efecto de LCP permanecen pendientes de QA en producción autorizada.

## Revisión dual y por qué está pendiente

La revisión cruzada exacta no se pudo completar sin infringir el límite de pruebas acordado. Se localizó la causa del QA general anterior: `orchestration/engine.py:335–355` ejecuta `central_qa` antes de deliberar; en `scope=workspace` lanza incondicionalmente `unittest discover -s tests/unit` (436 en el run anterior), y no hay opción de CLI para seleccionar pruebas focalizadas o desactivar ese gate. En `scope=theme` sustituye la suite por el auditor de fuente/schema de todo el snapshot, que tampoco es focalizado. No cambié la política ni repetí la llamada al consejo. Por ello Claude y Codex **no han revisado este hash**; la revisión sigue `needs_evidence` y no se presenta aprobación sintética.

## Riesgos y siguiente QA

- El helper de imagen es compartido; el guard de opt-in se debe revisar con el diff exacto antes de aceptar.
- Las pruebas fixture prueban el estándar del navegador, no el renderer Liquid/Twig de Tiendanube ni el marcado nativo final.
- El `alt` unificado debe seguir describiendo ambas variantes.
- Las fuentes `width`/`height` y fallback deben confirmarse con el HTML que genere Tiendanube.
- No están verificados en el entorno remoto los hashes actuales de estos dos archivos.

Antes de publicación se requiere revisión independiente del diff y una validación nativa/salida renderizada aprobada. Luego, bajo autorización separada, QA de red fría por viewport (360/390/412/768/1024/1440/1920), verificar una sola descarga y `currentSrc`, dimensiones/CLS, prioridad, filtros/editor, HTML inicial, comportamiento lazy, mobile/desktop y cinco mediciones Lighthouse por dispositivo comparables. No se solicita ni ejecuta publicación con este candidato.

## Preparación de revisión independiente — 2026-11-17

Se congeló el paquete [`review-package-e6d7edd9`](review-package-e6d7edd9/review-brief.md). Su manifiesto SHA256 es `accbbf7fa4b4fea7fcc71dcdef064b9deac2ca50a1536fd28a837c2bd13ac74d`; se comprobaron los 10 artefactos incluidos. El patch conserva SHA256 `e6d7edd9bb3590b0909cd71a9245bf5a92cbd7034f24fc57bb00389d0ec3f841`. Los archivos candidatos conservan los hashes de la tabla anterior.

**Claude: pendiente. Codex: pendiente.** No se llamaron los adaptadores: el único flujo existente que los ejecuta para el consejo es `orchestrate ... --execute`; `engine.execute()` llama a `central_qa()` antes de `run_council()`. La implementación de `central_qa` no tiene selector focalizado: con `scope=workspace` crea un snapshot de QA sin red y corre `python3 -m unittest discover -s tests/unit -v` (timeout 180 s); el run anterior registró 436 pruebas, 11 omitidas y QA exitoso, luego quedó interrumpido durante las intervenciones. Con `scope=theme` ejecuta `tools/audit_source.py` sobre el snapshot completo del tema, no solo los dos archivos. No existe flag para omitir o reducir central QA. Invocar los adaptadores directamente habría saltado el controlador y sus controles, por lo que no se hizo.

No hay objeciones independientes recibidas ni se reejecutaron las 231 aserciones. La revisión técnica sigue `needs_evidence`; el paquete no es una aprobación del gate.

### Alternativas para continuar

**A. Gate central existente.** Autorizar una ejecución del consejo por el flujo `orchestrate` con su QA obligatorio. Para el plan `workspace` focalizado en los archivos del candidato, el controlador ejecutará la suite unitaria completa de 436 pruebas observada previamente; no se puede prometer que el número siga idéntico si el repositorio cambió. Sin embargo, esto no repite las pruebas sintéticas del navegador y la revisión de los agentes puede aún fallar o quedar incompleta.

**B. Revisión técnica independiente sin gate operativo.** No está soportada hoy por los adaptadores sin saltarse el controlador. La alternativa segura es autorizar primero una propuesta de cambio acotado para que el controlador acepte un conjunto explícito de QA focalizado, con límites y recibos propios; conservaría el consejo central y `needs_evidence`, pero requiere revisión y autorización separadas para modificar el orquestador. No se hizo ese cambio.

### Validación nativa preparada (no ejecutada)

Tras completar revisiones válidas y resolver objeciones, la solicitud propuesta sería una única validación sin persistencia por POST nativo de Tiendanube, instalación `14828608` / tienda `7400935`, limitada a:

- `sections/hero.tpl` — SHA256 `5362f1b4ddab56feabc95ad23486cc1b439b02d06a0479a2fcb8deb96fa8861c`.
- `snippets/image.tpl` — SHA256 `f45641d2f4cd4e9fea775cf1aa19f806686130f79cb191e2a2140436919e178b`.

La operación de referencia es `POST /v1/7400935/theme-installations/14828608/files/validate`; debe recibir exclusivamente esos dos archivos y no persistirlos. **No se envió el POST.** Requiere autorización específica, independiente de la revisión. La validación de Tiendanube no publicaría ni sustituiría QA posterior en producción.

## Ejecución autorizada del consejo dual — 2026-11-17

- Paquete y patch volvieron a pasar comprobación de hashes antes de ejecutar. El plan tenía `scope=theme`, `read_only=true`, `council.mode=full`, participantes Claude/Codex, y únicamente `sections/hero.tpl` y `snippets/image.tpl` en `allowed_files`.
- El QA central obligatorio terminó **passed** como `source-schema-only` (`tools/audit_source.py` sobre el snapshot del tema). No se ejecutó Lighthouse ni hubo tráfico al storefront.
- Se fijaron `max_retries=0`, `fallback=false` y `council_contract_retries=0` mediante configuración temporal por ejecución; se retiró al terminar.
- Resultado: run [`20261117T212443-orchestration-6161880c`](../../runs/rhino-performance/20261117T212443-orchestration-6161880c/). El controlador quedó `blocked`, ADR `needs_evidence`, `implementation_allowed=false`; la fuente original coincidió y el diff de salida fue vacío.

### Claude

Claude entregó una propuesta independiente válida: `changes_requested`. El recibo íntegro está en [`council-proposal-claude.json`](../../runs/rhino-performance/20261117T212443-orchestration-6161880c/council/council-proposal-claude.json), SHA256 `b7b4eb9fdfa2c592e2cdd2d62452141e7ecb7f19f24b479164a453ba474a0c9c`.

Hallazgos concretos de Claude:

- **D1 confirmado — hero solo móvil:** en `sections/hero.tpl`, la rama `has_mobile_image` sustituye la imagen desktop ausente por el placeholder y le da prioridad alta. En viewport desktop el `<picture>` cae al placeholder, mientras antes se mostraba la imagen móvil a todos los anchos en este caso. El escenario mobile-only de la fixture no verificó qué debe mostrarse en desktop.
- **D2 confirmado condicionalmente — referencia no resuelta:** `snippets/image.tpl:32–33` considera art direction válido cuando `image_mobile_src` existe y `mobile_media` es nulo. La rama puede emitir `@media-lib:...` literal en el `srcset` de `snippets/image.tpl:174/181`. Falta establecer con la validación nativa si `resolve_media` puede devolver nulo para una referencia móvil no disponible; el guard actual no lo excluye.
- **R1 condicional:** si el medio desktop resuelve a tipo distinto de imagen, el `if not media or media.type == 'image'` exterior puede omitir también la alternativa móvil.
- **R4 fallback responsive:** el `<source>` original de la rama nueva usa `media.sourceUrl`/`image_src` sin el `srcset` por tamaños que sí conserva el `<img>` normal. Si no se elige AVIF/WebP, el fallback puede perder selección responsive.
- **R3 accesibilidad:** con dos imágenes de descripciones distintas se usa un único `alt` desktop; la descripción móvil propia se pierde. Los dos assets deberían conservar el mismo significado textual o revisarse con salida renderizada.
- **R5 layout:** la reserva de ratio depende de dimensiones en `<source>`; CLS, especialmente con `auto_height`, no está medido en el renderer final.
- Claude también pidió validar Twig, `resolve_media`, LazySizes, editor/preview, red y LCP en Tiendanube; esas pruebas no están incluidas en la suite fixture.

La alternativa de Claude fue corregir D1 y la guarda D2 en los mismos dos archivos, definir fallback para medio desktop no-imagen y comprobar consumidores. Propuso además evaluar mantener variantes originales responsive en fallback. No se aplicó ninguna corrección.

### Codex

Codex **no entregó una revisión válida**. Su recibo [`council-proposal-codex.json`](../../runs/rhino-performance/20261117T212443-orchestration-6161880c/council/council-proposal-codex.json), SHA256 `a7f6770a7572a7ea85864947c4e83ab4df887b1bbbfa3d561a117bb1859fcd19`, registra `inactivity`: proceso iniciado, contexto completo (79,161 bytes), eventos de inicio y un elemento completado, pero sin respuesta contractual durante 90.873 s; el watchdog de inactividad lo canceló y recogió. No consta cuota ni error de autenticación. No hubo reintentos ni fallback.

Sin la segunda revisión independiente, no se inició contraste ni defensa entre pares. El gate bloqueó correctamente el ADR por condiciones `needs_evidence`.

### Contraste estático acotado

La búsqueda local en el tema encontró `image_mobile_src`/`image_mobile_media_query` usados explícitamente solo por `sections/hero.tpl` y la definición en `snippets/image.tpl`; no apareció otro caller que los pase. Esto reduce el riesgo de activación explícita accidental, pero no prueba todos los contextos implícitos del renderer Twig.

**Decisión del candidato:** necesita corrección antes de solicitar validación nativa, al menos por D1; D2 también debe cerrarse con un guard que no permita emitir el identificador de media como URL y una prueba de referencia no resuelta. R4 y los riesgos de plataforma necesitan decisión/evidencia. El patch sigue intacto y no se repitieron las 231 aserciones.

**Próximo paso mínimo:** autorización separada para una corrección local acotada de D1/D2 (y decisión explícita sobre R1/R4); luego generar un nuevo hash y solicitar una nueva revisión dual. La validación nativa POST sigue pendiente de autorización específica y no debe ejecutarse sobre este candidato sin resolver D1/D2.
