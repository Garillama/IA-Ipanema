# Verificación real de acceso — 9-11-2026

**Claude, Codex, CommandCode y Search Console están verificados con invocaciones reales. El recorrido del CSS del footer también terminó con render publicado y comparación anterior/posterior.** El usuario autorizó después un único push condicionado de `static/css/damar.css` a producción 14748767; se cumplieron sus condiciones. No se crearon clones ni se realizaron otras mutaciones remotas. La autorización posterior sustituye el criterio inicial de no modificar producción exclusivamente para ese archivo/operación.

Aceptación final: `20261109T201036-published-footer-qa-56b0b215/acceptance.json`. No equivale a aprobar todos los defectos previos de la tienda.

## Actores y aislamiento

| Actor | Herramientas realmente ejecutadas | Evidencia |
|---|---|---|
| Codex / gpt-6.1-sol | Descubrimiento, devtools_open, devtools_snapshot, gsc_sitemaps | `20261109T192546-access-agents-9ea99aa2/agents.json`, agente asignado=efectivo |
| CommandCode / deepseek/deepseek-v4.1-flash | Descubrimiento, devtools_open, devtools_snapshot, gsc_sitemaps | Mismo run, actor propio |
| Claude / claude-sonnet-5-5 | Descubrimiento, devtools_open, devtools_snapshot, gsc_sitemaps | `20261109T192921-access-agents-91c8d542/agents.json`, tras autenticación del usuario |

Todos los runs se encuentran bajo `reports/runs/damarbeauty/`. Los eventos de gateway acreditan las llamadas, independientemente de lo que afirmó el modelo. Se usaron sockets por tarea, Bubblewrap, snapshot RO y autenticación exclusiva del proveedor de inferencia. No se montaron política/almacén Google, HOME del host u otras tiendas. No se modificaron configuraciones personales.

La primera ronda registró autenticación fallida de Claude y failover real; no se contó al sustituto como éxito de Claude. Codex necesitó los ejecutables auxiliares de su distribución dentro del aislamiento; después invocó por sí mismo. Tras `claude auth login`, `claude auth status` confirmó sesión activa y se ejecutó solo su prueba de recuperación. Se conservaron los resultados/checkpoints anteriores; no se repitieron tareas completadas por CommandCode. Las 18 regresiones del mecanismo de recuperación pasaron, con fallos simulados identificados. [Registro de orquestación](../orchestration/verification.md).

Prueba adicional de aislamiento real: un worker sin red accedió únicamente al socket permitido, vio solo herramientas de su permiso y no pudo leer política ni credenciales personales del host. Revocación, cuota persistente, caducidad, dominio/proyecto ajenos y detención 403/429 están cubiertos. La identidad se atribuye al permiso del controlador: no se afirma aislamiento entre procesos host del mismo usuario que puedan escribir la política.

## Google real, separado de mocks

Google OAuth de escritorio: PKCE S256, state y callback loopback, scope exclusivo `webmasters.readonly`. El usuario concedió consentimiento. Sites.get confirmó **siteOwner** en `sc-domain:damarbeauty.mx`.

`reports/runs/damarbeauty/20261109T192720-access-google-live-66b92dce/verification.json` acredita tres respuestas reales de OfficialREST:

- Search Analytics: observed; cero filas en el periodo solicitado, sin concluir ausencia total de tráfico.
- URL Inspection de la home: observed; estado conocido del índice, no inspección en vivo ni petición de indexación.
- Sitemaps registrados: observed; no equivale a inventario de URLs.

El resumen posterior `20261109T194820-gsc-live-summary-c90cc0bb/summary.json` guarda parámetros y resultados normalizados reales: Search Analytics del 10-10 al 6-11 de 2026 devolvió cero filas; la home tiene verdict PASS, Submitted and indexed, rastreo móvil y canonicals coincidentes; la propiedad devolvió una lista vacía de sitemaps registrados. No se deduce que el sitio carezca de sitemap.

Cada actor ejecutó además su propia lectura de sitemaps a través de la puerta. El access token se guarda fuera de Git, ligado a proyecto/propiedad/scope/expiración, en archivo 0600 y directorio 0700. No se guardaron tokens, cookies, códigos OAuth o client secret en informes, mensajes o mounts del worker. No se comparte entre proyectos. No hay refresh automático; la expiración necesita nuevo consentimiento.

Los tests de OAuth/REST usan transportes simulados identificados y no acreditan acceso real; las evidencias anteriores provienen de Google. Analytics y Merchant permanecen opcionales, sin activar.

## Perfiles y auditoría real

DevTools MCP 1.12.0 fijado e integridad comprobada, estadísticas y CrUX desactivados. El perfil security mantiene solo el origen; audit añade orígenes comprobados en HTML/red. Ambos tienen navegador/perfil efímeros propios y bloqueo de operaciones comerciales/escritura por el runtime Puppeteer existente. Chrome loopback verificó CDN bloqueado en security, recurso registrado cargado en audit y POST que no alcanza el servidor.

La auditoría pública con recursos legítimos está en `20261109T193035-access-real-resources-8ae2762b/browser/`: home 390/1440, HTML inicial/DOM proyectados, red/CDP, currentSrc, fuentes, capturas y Lighthouse. En ese run se registraron 12 orígenes explícitos. La comprobación posterior del footer identificó además el CDN nativo de iconos `d26lpennugtm8s.cloudfront.net` y `apps-scripts.tiendanube.com`: el perfil final registra 14. La captura móvil observó 71 solicitudes, 3.947.633 bytes de imágenes, 609.266 de JS, 63.312 de CSS y 37.988 de fuentes, con cero transferencias completadas sin longitud medida. Los fallos de red de los píxeles/escrituras de terceros se interpretan bajo la política de lectura, no como defecto del tema.

Lighthouse, una ejecución por perfil del job: móvil LCP 7.064 ms, TBT 365 ms, CLS 0; escritorio LCP 939 ms, TBT 26 ms, CLS 0,000203. Son líneas base de laboratorio de perfiles distintos, **no una mejora antes/después**, no INP de campo ni sesión de compra completa. El primer perfil audit, con menos recursos permitidos, se conserva como evidencia histórica y no se compara como optimización.

Axe encontró `aria-prohibited-attr`, `label-content-name-mismatch` y `target-size`. El reporte browser se etiqueta **failed por hallazgos reales de accesibilidad**, aunque capturó ambas páginas y Lighthouse sin un bloqueo de transporte. No se presenta como aprobación AA.

La auditoría SEO de HTML/DOM real `20261109T191631-seo-audit-77deace9` obtuvo cero errores y 18 hallazgos. No prueba indexación, elegibilidad de resultados enriquecidos o verdad comercial del catálogo.

## Código local y referencia de producción

El CLI nativo confirmó tienda 8408995 e instalación publicada/forked **14748767**, Ipanema Clothing-2 1.7.0. `theme current` y el manifest local coinciden. La configuración de proyecto registra esa referencia con procedencia fechada.

El diff nativo completo y detallado detectó **468 iguales, uno modificado, cero añadidos, cero borrados, cero skips y cero fallos de lectura**. No sobrescribió archivos. El único cambio es la regla del footer en `static/css/damar.css`: inline-flex, alineación y altura clicable mínima de 24 px. Se identificaron `blocks/damar-footer-help.tpl`, `sections/footer.tpl` y carga global del CSS como consumidores. No se añadieron recursos/JS ni se alteraron enlaces o lógica comercial.

- Baseline de 469 archivos + HEAD: `20261109T193707-production-reference-dc7d2bcf/baseline.json`.
- Diff remoto→local: `20261109T193921-production-exact-diff-577f2b83/remote-to-local-git.patch`.
- Diff de tarea y reversión: `20261109T193827-footer-review-039b20ec/`.
- Reversión nativa en carpeta temporal, SHA-256 igual al backup: `20261109T194114-production-rollback-proof-146b7737/verification.json`.
- QA fuente aprobado: `20261109T192106-source-2c9f97d9/report.json`.
- Intento aceptado con evidencia publicada del footer: `c79e18cd0f5846338e875a76512204c7`.

La guardia por proceso comprobó destino publicado, único archivo y SHA-256 aprobado `aad247fbfa8160beaf4efda3d01c470d46eb4b53f08a37bb1152b018192916d5`. Antes del push se volvió a leer la instalación/diff; coincidía exactamente con el revisado, sin cambios de terceros en ese CSS, y el backup reconstruido coincidía por hash. La simulación previa sustituyó solo la hoja CSS en un navegador aislado conservando su posición en la cascada; se identificó como simulación y no como publicación.

Se ejecutó **una sola invocación** del push nativo; no hubo rollback, publish, watch, clone, fork ni pull. `20261109T200828-authorized-css-push-f580dda1/state.json` conserva las precondiciones/resultados. `20261109T201038-postpush-native-diff-4a522a34/verification.json` comprobó después **469 archivos iguales, cero modificados/añadidos/borrados y cero skips/fallos de lectura**.

El plan histórico no autorizado se conserva en `20261109T194616-production-operation-review-397811d4/request.json`; su `conditional-authorization.json` registra la aprobación posterior. No concede permiso para futuras subidas.

## QA publicado y comparación

`20261109T201036-published-footer-qa-56b0b215/` contiene capturas, `published.json`, `before-after.json`, `seo-comparison.json` y evidencias QA normalizadas con hashes y procedencia. Las seis comprobaciones posteriores cargaron el CSS publicado **sin sustitución de estilos en navegador**. El asset servido cambió de `damar-1e1be6ee0b2cfe4fe53d82c29669ee03.min.css` a `damar-68e5e2192782a229b13213a1b9a58147.min.css`.

| Página | Footer a 390 px, antes → publicado | Footer a 1440 px |
|---|---|---|
| Home | 714 → 730 px (+16) | 504 → 504 px |
| Categoría | 734 → 754 px (+20) | 504 → 504 px |
| PDP | 714 → 730 px (+16) | 504 → 504 px |

Enlaces de 16 → 24 px de alto, mismos textos/destinos, sin overflow ni violaciones axe del footer en seis casos. Revisión visual de las capturas publicadas: sin problema de composición atribuible al CSS. Los placeholders de iconos durante la carga diferida de categoría estaban presentes antes y después; se conservaron como limitación, sin atribuirlos al cambio. La espera contempla el ocultamiento temporal nativo del footer durante `LS.hybridScroll`.

QA de página completa anterior: `20261109T200438-prepush-pages-baseline-eb786d49/browser/`; posterior: `20261109T201125-postpush-pages-qa-9f984599/browser/`. `comparison.json` en este último run comprueba jobs idénticos salvo directorio de salida, seis casos, cero checks nuevos fallidos y **cero targets nuevos de axe**; se resolvieron ocho incidencias observadas (WhatsApp/email en home/PDP, ambos tamaños). Persisten fallos previos de aria/etiquetas, objetivos pequeños de marcas en categoría y dos H1 en PDP. El resultado global de página sigue `failed` por esos hallazgos; no acredita AA.

El motor SEO existente auditó las capturas reales anteriores/posteriores: home 0→0 errores, categoría 1→1, PDP 0→0; **cero hallazgos nuevos**. SEO011 de categoría señala el href del control de carga posterior: requiere investigación nativa separada, no se corrigió automáticamente. No hay certificación externa de rich results/indexación.

La comparación conserva también entradas LCP y transferencias CDP con el mismo perfil final de 14 orígenes. Una muestra por caso, variaciones en ambas direcciones y diferencias dinámicas; **no se atribuye mejora de rendimiento al CSS**. No se realizó diff visual por píxel sin máscaras para contenido dinámico. El rollback no fue necesario: no se detectó regresión atribuible en el alcance probado. El backup íntegro y los hashes permanecen disponibles, sin autorizar nuevas operaciones.

## Recorrido de extremo a extremo

| Paso | Estado |
|---|---|
| Inspección, HTML inicial/DOM y recursos | Real, ejecutado |
| Línea base de rendimiento y problema verificable | Real, ejecutado; problemas de accesibilidad registrados |
| Componente, corrección mínima, diff y backup | Comprobados; único CSS autorizado |
| Pruebas locales | Fuente, herramientas, permisos y transporte aprobados |
| Render del CSS modificado en Tiendanube | Real publicado tras un único push específico autorizado |
| Comparación antes/después y SEO/axe posteriores | Real ejecutada; footer aprobado y hallazgos previos conservados |

## QA de infraestructura y trazabilidad

Último quick: **151 unitarias y 29 de integración**, aprobado; evaluaciones existentes aprobadas. Evidencia: `reports/runs/ipanema/20261109T194729-quick-53d22e9a/report.json`. Fixtures: **11 pruebas de navegador** aprobadas en `reports/runs/ipanema/20261109T192227-fixtures-6b98150b/report.json`, con Chrome/MCP reales en loopback. Los cambios posteriores de almacenamiento privado y guardia nativa se probaron mediante sus regresiones y quick; no se presentan esos mocks como escritura real.

Aceptación conjunta de actores y hashes: `20261109T193631-access-acceptance-e865237c/acceptance.json`. Ese artefacto conserva el estado de entonces; la decisión posterior del usuario sustituyó la solicitud de clon por referencia de producción. La conexión es funcional; la aceptación final y sus límites están en el run publicado enlazado al inicio. El intento del CSS fue aceptado con evidencia normalizada de pruebas reales, limitada al footer; sus timestamps originales y fecha de ensamblaje se conservan. La solución inicial `shared-access-mcp-rest-v1` requiere revalidación al cambiar estas fuentes; no se usa como certificación del nuevo alcance.
