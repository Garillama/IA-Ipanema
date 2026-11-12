# Rhino Performance — cierre del lote del header y diagnóstico de marketing

Fecha: 11 de noviembre de 2026. Continuación de ADR-RHINO-009. Producción sin modificar.

El candidato v2 del header se aplicó exclusivamente al tema local después de revisión real de Claude y Codex, QA del controlador, respaldo y comprobación de hashes. Transacción `81a54d213d92470783a55a5eb2f55689`: accepted, intento 1. La prioridad móvil de marketing permanece pendiente; no se ha demostrado 90+.

## Cambio y alcance

Único archivo del tema modificado: `/home/alanrichard/Escritorio/Cli/Rhino-Ipanema/static/css/style-critical.css`. [Diff exacto](header-initial-flow-v2.patch).

El CSS anticipa la posición absoluta que el header nativo adopta al inicializarse, exclusivamente en Home con video inicial, transparencia habilitada, escritorio desde 1024 px, scripting habilitado y antes del atributo de runtime. Evita el desplazamiento inicial observado de 74 px. El guard de scripting conserva el diseño sin JavaScript; reemplaza al candidato v1, que alteraba esa variante. No se modificaron tipografías, Twig, Sectionfy, Swiper, tracking ni contratos comerciales.

## Mediciones y límites

La última línea base nativa válida de Home sigue siendo mediana 64 móvil / 87 escritorio, cinco muestras por dispositivo. No representa una medición del cambio local publicado.

Experimento controlado: cinco controles y cinco candidatos por dispositivo, Lighthouse 13.6.0 / Chrome 155.0.8059.84, caché reiniciada y perfiles equivalentes dentro de cada dispositivo. La hoja crítica capturada se entregó sin compresión en ambos brazos para verificar exactamente los bytes. Política `guarded-read-only+identity-css-override-v3`. Sus valores absolutos no se deben mezclar con las mediciones nativas de CDN.

| Mediana | Móvil control → candidato | Escritorio control → candidato |
|---|---:|---:|
| Performance | 57 → 60 | 81 → 85 |
| LCP | 4167 → 3699 ms | 1161 → 1075 ms |
| FCP | 1706 → 1754 ms | 448 → 450 ms |
| TBT | 1740 → 1723 ms | 245 → 136 ms |
| CLS | 0,00045 → 0,00045 | 0,06815 → 0,00143 |
| Speed Index | 3506 → 3432 ms | 2878 → 2993 ms |

La evidencia causal sólida es la estabilidad geométrica del header en escritorio. El CSS no se activa en móvil: las diferencias móviles no se atribuyen a este parche. Tampoco se atribuye toda la variación de CPU en escritorio al CSS. Los gates con tolerancias explícitas no detectaron una regresión confirmada; cinco muestras no garantizan resultados futuros.

## QA y revisión independiente

- 60 reglas relevantes del header contrastadas con el CSS compilado publicado.
- Seis anchos: 360, 390, 768, 1024, 1440 y 1920 px; variantes, scroll, foco, enlaces y semántica revisados.
- Test reproducible nuevo: `node tests/browser/rhino_header_initial_flow.mjs CSS_FILE DIRECTORIO_NUEVO`. Antes fallaba en los tres tamaños de escritorio elegibles; sobre el archivo aplicado pasan 72 comprobaciones.
- Comparación visual sin máscaras: sin diferencias en las capturas finales comparables. La comparación inicial de 1440 px se descartó por distinto fotograma/estado de transición; se repitió con pausa nativa, mismo fotograma y cursor fuera del header: cero píxeles diferentes.
- Sin JavaScript: variantes 390/1440 conservadas. No se certifica WCAG completa.
- Se conservan defectos anteriores del menú móvil: Escape no cierra, no atrapa foco y el cierre no devuelve foco al disparador. No los introdujo este cambio y requieren otro lote.
- Claude y Codex: seis invocaciones reales, propuestas independientes, contraste y defensa. Modelos registrados: Claude Sonnet 5.5 y gpt-6.1-sol, esfuerzo medio. Ambos revisaron el mismo diff exacto. Sin CommandCode.
- Estado del controlador: approved_with_conditions; condiciones de implementación local satisfechas, limitaciones de entorno conservadas. No se declara consenso completo ni aprobación de producción. Los nombres distintos que dieron al mismo candidato se normalizaron únicamente por identidad del hash; respuestas originales intactas.

## Marketing: resultados y decisiones

Se observó una inicialización de cada SDK de Google, Meta y TikTok, una configuración GA4 y un init/PageView de Meta. Dos colas de datos contienen `view_item_list`, pero eso no demuestra doble entrega. Las solicitudes POST comerciales se bloquearon durante las pruebas: entrega, atribución y compras no se verificaron.

La configuración pública descargada de GTM contenía cero tags y cero reglas; GA4 seguía configurado separadamente. Esto justifica revisar con el propietario la necesidad actual del contenedor, no retirarlo automáticamente ni inferir el contenido de espacios privados.

Contrafactual móvil, tres capturas por brazo, ventana física de 20 segundos y CPU 4×: mediana de exceso de tareas largas sobre 50 ms de 2270 ms en controles, 1770 ms bloqueando Meta y 1898 ms bloqueando TikTok. Son diagnósticos de CPU, no TBT oficial, INP ni beneficios que conserven eventos. El experimento previo de Google tiene otros controles y fecha; no se suma ni se usa para un ranking preciso entre proveedores.

Antes de pulsar “Entendido”, la cola observada de Google ya declaraba los cuatro estados de consentimiento concedidos; no se observó un update posterior al botón. No se interpreta como dictamen legal ni como una CMP granular. No conviene ligar una demora arbitraria a ese botón.

**Decisión:** no diferir ni retirar tracking desde el tema. Siguiente lote: revisar el contenedor publicado y dependencias con autorización específica, definir matriz de eventos/consentimiento y validar entrega en herramientas de prueba autorizadas antes de cambiar configuración remota. Referencias: [Consent Mode](https://developers.google.com/tag-platform/security/guides/consent) y [depuración de consentimiento](https://developers.google.com/tag-platform/security/guides/consent-debugging).

## Otras plantillas y pendientes

Blog móvil conserva una sola muestra válida: LCP 6562 ms y TBT 1491 ms. La imagen candidata aparece en HTML inicial, carga eager y tiene prioridad alta; no hay evidencia para añadir otro preload. El desglose de LCP del insight no coincide con el valor simulado agregado y no permite porcentajes causales. La misma muestra atribuye unos 765 ms de CPU a blog-tags y 712 ms a Clarity; son candidatos a investigación, no autorización para retirarlos. Categoría y PDP conservan sus baselines previos.

Prioridades pendientes:

1. P1 móvil: validar medición comercial y necesidad del GTM publicado antes de optimizar integraciones.
2. P1 blog: repetir muestras comparables y aislar trabajo de blog-tags antes de proponer un parche.
3. P2 accesibilidad: resolver Escape y retorno de foco del menú en un lote separado.
4. Validar el header en una instalación de pruebas compatible o después de un despliegue autorizado por el propietario; la URL pública no mide archivos exclusivamente locales.
5. PageSpeed/CrUX: esta sesión no dispone de claves; no hay nuevas respuestas API. Datos históricos de origen no se atribuyen a una página ni al cambio local. No se inventa INP.

No se ejecutaron push, watch, publish, compras ni cambios remotos. No se programaron consultas automáticas. El objetivo 90+ permanece abierto.

## Evidencia original

Directorio local ignorado por Git: `reports/runs/rhino-performance/20261111T211930-adr009-followup/`.

- `header-final-controlled-comparison.json`: muestras, perfiles, estadísticos y gates.
- `header-exact-council.json`, `header-controller-ADR.json`, `candidate-identity-aliases.json`: participantes, objeciones, defensa y decisión.
- `header-source-proof.json`, `header-final-QA.json`, `header-neutral-visual-comparison.json`: fuentes, variantes y capturas.
- `header-post-apply-QA.json`, `header-acceptance.json`, `header-candidate-hashes.json`: comprobación del archivo realmente aplicado y aceptación.
- `preflight-marketing-source.json`, `marketing-public-inventory.json`, `marketing-counterfactual-summary.json`: diagnóstico comercial separado de mediciones Lighthouse.

Se preservan los experimentos inválidos y pruebas supersedidas con su condición; no integran los resultados aceptados. La evidencia preaplicación se reutiliza solo al coincidir exactamente el hash del candidato aplicado. No se presenta como prueba posterior de producción.
