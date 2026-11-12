# Paquete definitivo de paginación — autorización pendiente

**Estado posterior: publicación autorizada ejecutada una sola vez.** [Resultados reales, hashes, QA y métricas](resultados-produccion.md). El manifest y el texto siguientes conservan el paquete previo a la autorización; no son el estado actual de ejecución. Menú y blog siguen separados y sin cambios.

12 noviembre 2026. **No se ejecutó push ni se modificó tema/producción.**

## Tres operaciones separadas

| Operación | Estado | Siguiente paso |
|---|---|---|
| Menú | Pendiente del respaldo administrativo que preparará el propietario | Cotejar campos, cuatro entradas actuales y duplicados; IDs si están expuestos. Si no, registrar limitación y reversión manual inequívoca. Solicitar autorización manual aparte. |
| Paginación | Listo para solicitar autorización específica de push, condicionada a QA posterior | Revisar este paquete y aprobar solo los dos archivos; comprobar de nuevo hashes y vigencia del baseline justo antes. |
| Blog | Pendiente de confirmación oficial de Tiendanube | Consulta preparada, **no enviada**; todavía no se ha iniciado espera de respuesta por nuestro envío. Conservar canonicals. |

## Identidad, diff y respaldo

La API nativa confirmó la instalación **14828608** como productiva de la tienda **7400935**. GET de los dos archivos: hashes before idénticos a los respaldados anteriormente; el diff nativo completo continúa en sincronía. Se guardó un respaldo remoto nuevo, sin copiar credenciales.

[Manifest completo](manifest.json) · [diff exacto](pagination.patch) · [revisión final de Claude](claude-final-review.json) · [QA y reversión](qa-y-reversion.md).

| Archivo | Hash publicado antes | Hash candidato después |
|---|---|---|
| `snippets/product-list/pagination.tpl` | `c715cc6c77d07dced5cdad6066785142c307b0f3ca3429cf88f5290cf7f2edc2` | `0958c668ee40bf0d16c76db4d6493bf6387d17e3ec7ff8f66aaffcce564d463c` |
| `static/js/store.js` | `29dea94e46cc1bb423ddde71a42d807f22c944f09465d70400728d7ae95b4718` | `f97557494e017eba623ba2dd7e568789f8d9035d467f0b03f71bc0b3b8393be9` |

SHA256 del parche: `1ef6c047b222962f3138cbaa3aba760b16d9569b5e597ad04cfa053df714eb49`. El controlador aplicó ese parche a los respaldos recién obtenidos en una prueba aislada de código y reprodujo exactamente ambos hashes after. Los únicos archivos resultantes afectados son esos dos. No se aplicó al tema.

Respaldo: `reports/runs/rhino-performance/20261112T182131-pagination-release-preflight-a1c49c03/remote-before`. No copiar código completo del cliente a documentación pública; los bytes originales y candidatos permanecen en evidencias privadas ignoradas.

## Diferencias que debe aceptar el propietario

- Fila **visible** de enlaces a páginas independientes, numerados cuando los valores nativos lo permiten; navegación «Página: productos». No es una réplica invisible para buscadores. En páginas posteriores aparece navegación también.
- Con JavaScript: se conserva LS.hybridScroll, el botón se habilita tras inicializarlo; teclado conserva foco estable y tras éxito apunta al primer producto nuevo si el usuario no lo movió. No se fuerza foco con puntero.
- Sin JavaScript: botón visible/deshabilitado y enlaces reales disponibles para navegar. La fila permanece tras anexar productos y sigue llevando a páginas independientes, no representa la siguiente tanda acumulada.
- Ningún cambio a filtros, catálogo, precios, carrito, Swiper, Sectionfy o scripts comerciales. La configuración actual no expone filtros/orden; si esto cambia, hay que revalidar. Solo hay página 2 de catálogo demostrada.

## Revisión independiente incremental

Claude recibió los dos archivos completos, diff, hashes exactos, pruebas conservadas y nuevos recibos. Su invocación real terminó con contrato aprobado y contexto completo. **Aprueba revisión de fuente y preparación de solicitud; no concede autorización remota ni aceptación de producción.** No encontró objeciones críticas de fuente pendientes. Codex mantiene explícitas las limitaciones de render posterior, datos fixtures y consumidores de store.js. No se repitieron propuestas iniciales ni inspecciones Google.

Modelo registrado por el adaptador: `claude-sonnet-5-5`, esfuerzo `medium`. Duración observada 31.164 s; coste reportado por el proveedor USD 0.3937549. Un primer paquete local excedió el límite de contexto del controlador **antes de invocar** Claude; se conservó el fallo y se compactaron recibos, sin omitir los dos archivos completos.

## Baseline nuevo del catálogo publicado

URL: `https://rhino-performance.com/productos/`. **Lighthouse local, cinco muestras por dispositivo; no PageSpeed.** Chrome/Lighthouse, viewport, CPU, red simulada, caché y política están registrados por muestra. Navegador nuevo, sin sesión de administrador, sin interacción de consentimiento y con guard de solo lectura: solicitudes de escritura, incluidas de marketing, bloqueadas. Esto limita la representación de eventos comerciales y debe conservarse idéntico en el perfil posterior. No se apagaron JS, medios ni CSS para mejorar puntuaciones.

| Dispositivo | Score mediana (mín–máx) | LCP mediana | FCP mediana | CLS mediana | TBT mediana | Speed Index mediana |
|---|---:|---:|---:|---:|---:|---:|
| mobile | 65 (60–66) | 2.85 s | 1.59 s | 0.0000 | 2264 ms | 3.45 s |
| desktop | 87 (76–91) | 1.51 s | 0.43 s | 0.0157 | 205 ms | 1.17 s |

[Muestras y perfiles resumidos](baseline-summary.json). Originales saneados por muestra: `reports/runs/rhino-performance/20261112T182131-pagination-release-preflight-a1c49c03/baseline`; normalizados con el motor de rendimiento existente. Variabilidad conservada, sin mezclar mejores métricas de muestras distintas. Esta línea base no prueba mejoras del candidato ni sustituye las auditorías históricas de home. El TBT móvil sigue siendo un problema independiente; este parche SEO no promete 90+.

HTML inicial nuevo:200, canonical propio del catálogo,144 enlaces extraídos,718480bytes de respuesta. Se guardó hash y proyección semántica, no cookies. Ninguna nueva consulta GSC/CrUX/PageSpeed. Revalidar vigencia de versión/contenido al autorizar; si cambia de forma relevante no comparar perfiles incompatibles.

## Alcance de la futura autorización

Solicitar autorización para subir **únicamente** los dos archivos del manifest a la instalación ya productiva, incluyendo los cambios visuales descritos. No autoriza menú, blog, theme publish, watch, force, clon, staging ni catálogo. La CLI no ofrece --file: el controlador debe limitar el payload de transporte a exactamente esas dos modificaciones y cero eliminaciones, con hashes after obligatorios. Las nueve pruebas de restricción pasaron con **transporte simulado offline**: no son una subida real. Ante alcance distinto, detener.

Solicitar también reversión exclusiva a los dos respaldos si el QA revela una regresión, siempre que los hashes remotos sigan siendo los after aprobados. Ante cambios posteriores ajenos, detener en vez de sobrescribir. La autorización aún **no se ha recibido**.

Aceptación posterior: hashes publicados, SSR de enlaces/canonicals, LS real12→14IDs, noJS, AX/teclado/foco, seis anchos y capturas, smoke de consumidores y cinco muestras equivalentes mobile/desktop. Todos siguen pendientes. Revisión de fuente, validación nativa y pruebas aisladas no se reinterpretan como QA publicado aprobado.
