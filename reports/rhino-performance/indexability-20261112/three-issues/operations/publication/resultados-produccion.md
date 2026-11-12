# Paginación Rhino — publicación autorizada y QA real

12 noviembre 2026. **Publicado únicamente el parche aprobado**, instalación 14828608, tienda 7400935. Una sola petición PATCH, dos archivos, cero eliminaciones, HTTP 200. No watch, force, publish, clones, staging ni operaciones comerciales. La autorización reiterada por el propietario no produjo otra subida.

## Integridad y alcance

Se verificaron de nuevo ambos originales por GET antes de publicar y otra vez inmediatamente antes del PATCH. Los bytes respaldados siguen disponibles y coinciden con los hashes before. El payload fue restringido por rutas y hashes after. La carpeta local se actualizó únicamente con esos dos archivos tras verificar los bytes publicados. El diff nativo final confirma 398 archivos en sincronía; no se sobrescribieron otros cambios.

| Archivo | SHA256 publicado |
|---|---|
| `snippets/product-list/pagination.tpl` | `0958c668ee40bf0d16c76db4d6493bf6387d17e3ec7ff8f66aaffcce564d463c` |
| `static/js/store.js` | `f97557494e017eba623ba2dd7e568789f8d9035d467f0b03f71bc0b3b8393be9` |

Parche autorizado: `1ef6c047b222962f3138cbaa3aba760b16d9569b5e597ad04cfa053df714eb49`.

**Discrepancia de lectura conservada:** el endpoint nativo de archivo individual devolvió la versión anterior de store.js, mientras que el endpoint oficial por lote devolvió exactamente los dos candidatos. El JavaScript descargado y ejecutado por el navegador desde el CDN público también tiene exactamente SHA256 f9755749…e93be9 y 162703 bytes. No se atribuye la discrepancia a caché como causa demostrada. Se detuvieron las escrituras al detectarla; no se reintentó la subida. La corroboración por lote, CDN y diff final permitió continuar el QA de la versión realmente publicada.

## Pruebas de producción

- `/productos/` y `/productos/page/2/`:200 y canonical propio; H1/title/meta/JSON conservados según las proyecciones. Sin errores de sintaxis JSON detectados: esto no certifica rich results ni indexación.
- HTML inicial del catálogo contiene `<a href="/productos/page/2/">Página 2</a>`; página 2 contiene el enlace de retorno `/productos/` con «Página 1». Son href relativos válidos. Un primer comprobador exigía URL absoluta y produjo false; se conservó ese resultado y se corrigió la interpretación con parser de HTML y navegación real.
- LS.hybridScroll publicado:12→14 productos reales en360/390/768/1024/1440/1920;14 IDs únicos y mismo orden de los12 originales. El botón se habilita con JS. No se inventó página3.
- Sin JS a 390 y 1440: botón deshabilitado y navegación HTML real a página 2 con sus 2 productos. Con JS, Enter sobre «Página2» también navega correctamente en ambos tamaños.
- Foco del enlace y roles/nombres reales en Accessibility Tree; «Página: productos» y «Página2» se resuelven correctamente. Axe sobre la nueva navegación a 390 y 1440:0 violaciones,0 incompletas,7 reglas pasadas. No es certificación WCAG ni examen completo de toda la tienda.
- Capturas de inicio y paginación en los seis anchos, más página 2sin JS. Se revisaron las seis capturas de la nueva navegación; la fila visible corresponde al cambio aceptado, sin recorte del enlace. No existe una comparación visual anterior completa por píxeles para certificar toda la página.
- Home, PDP PRO AIR y blog:200, contenido/LS y canonical presentes,0 pageerrors a 390 y 1440. Smoke de carga, no prueba exhaustiva de variantes, carrito, checkout, tracking ni todos los carruseles. No se enviaron formularios ni compras.

### Límites y hallazgo visual separado

Con 14 productos, el umbral manual nativo de 60 no se alcanza: la carga es automática y el botón acaba oculto. Por tanto el foco al primer producto tras pulsar manualmente, el movimiento del usuario durante espera y la ruta de error conservan sus pruebas nativas con fixtures; **no se declaran repetidas con datos reales**. Filtros/orden no están expuestos; revalidar si se habilitan.

Se observó overflow horizontal antes del append en 1024/1440, sin JSen 1440y en el smoke de home/PDP/blog a 1440; después del append del catálogo no se observó. No hay baseline geométrico previo equivalente para atribuirlo ni demostrar que era preexistente. El check original no_horizontal_overflow se refería solo al catálogo tras append: se acotó explícitamente en controller-QA-final, conservando el original. No se modificó CSS, footer ni otros archivos para ocultarlo.

## Lighthouse local — cinco muestras por dispositivo antes y después

Misma URL del catálogo, Lighthouse 13.6.0, Chrome 155.0.8059.84, perfiles simulados y política de red idénticos. Móvil 412×823/DPR1,75/CPU4×/RTT150ms/1638,4kbps; escritorio según perfil completo registrado, CPU1×/RTT40ms/10240kbps. Navegador nuevo, caché limpia, sin interacción de consentimiento. El guard de lectura bloquea POST, incluido marketing; limita la representación de conversiones y se conservó igual antes/después. No se mezcla con PageSpeed o CrUX; no se consultaron sus APIs.

| Dispositivo | Score mediana antes→después | Rango score antes→después | LCP antes→después | FCP antes→después | CLS antes→después | TBT antes→después | Speed Index antes→después |
|---|---:|---|---:|---:|---:|---:|---:|
| mobile | 65→65 | 60–66 → 60–67 | 2.855→3.125s | 1.590→1.386s | 0.000→0.000 | 2264.000→1960.050ms | 3.449→3.165s |
| desktop | 87→88 | 76–91 → 85–94 | 1.515→1.392s | 0.433→0.387s | 0.016→0.016 | 205.000→178.000ms | 1.166→1.001s |

**Advertencia móvil:** mediana LCP+270ms(+9,5%); rango2,612–3,530s antes y2,781–3,918s después. El comparador registra delta positivo de LCP. Los umbrales predeclarados no se activaron: para LCP exigían >10% y >200ms. Eso no elimina la advertencia ni demuestra equivalencia estadística. Con cinco muestras y rangos/MAD solapados no hay causalidad probada. CLS máximo móvil0→0,0268en dos muestras; mediana 0. El insight señala movimiento de main, sin causa aislada demostrada. No se altera otro componente para resolver esa hipótesis.

TBT mediano móvil2264→1960ms y escritorio205→178ms; son diferencias observadas, **no beneficios atribuibles demostrados**. No se llama INP al TBT. Medianas de score65→65 móvil y87→88 escritorio: no alcanzamos90+en ambos ni se presenta un mejor resultado aislado como habitual.

Transferencia total mediana: móvil1.951.692→1.952.982bytes(+1.290); escritorio2.344.487→2.333.504bytes(−10.983). Transferencia JS mediana móvil+986bytes, escritorio−10.919bytes; cambios totales incluyen variabilidad externa, no solo el parche. No hay bibliotecas o endpoints nuevos del cambio. El código fuente JS aumentó 1174 bytes. El JSON conserva tamaños por tipo y por ejecución, sin mezclar métricas para fabricar una corrida.

## Revisión y decisión

Claude revisó realmente los recibos posteriores mediante el orquestador vigente y aprobó **únicamente el alcance probado**, con las advertencias de LCP, overflow y estados no ejercitables. No ejecutó él las pruebas ni certificó toda la tienda. Codex/controlador ejecutó el QA y corrigió el alcance del check de overflow según los datos originales. Se conservaron la revisión previa, esta revisión, preguntas y advertencias, sin reiniciar el consejo.

**Resultado:** publicación exacta realizada; pruebas funcionales/SEO del alcance pasadas; umbrales de laboratorio pasados con advertencia de LCP móvil. No se detectó regresión crítica atribuible que habilite la reversión; **no se revirtió ni se hizo otro despliegue**. La discrepancia del endpoint individual y el overflow quedan registrados para investigación separada. Menú y canonical del blog sin cambios.

## Evidencias reproducibles

[Resultado estructurado, métricas y revisión](production-result.json). Evidencias originales privadas/ignoradas: `reports/runs/rhino-performance/20261112T183218-pagination-authorized-deployment-b354454c`. Incluyen autorización, originales remotos, recibos del únicoPATCH, lecturas posteriores discrepantes, batch correcto, hashesCDN, HTML inicial, browser/AX/axe, capturas, smoke, diez LHR saneados, perfiles completos, estadísticas, gates y revisión final. Baseline anterior: `reports/runs/rhino-performance/20261112T182131-pagination-release-preflight-a1c49c03/baseline-summary.json`.

La autorización continúa limitada al despliegue ya ejecutado; cualquier cambio adicional exige su revisión y permiso propios. No se invocó CommandCode ni se modificaron menús, canonicals, catálogo, apps o configuración remota.
