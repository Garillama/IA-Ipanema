# RHINO — rendimiento después del push

Fecha: 2026-11-10T21:16:22.548023+00:00. Proyecto `rhino-performance`, https://rhino-performance.com/. Instalación pública de assets14828608. El propietario indicó que **rendimiento es la prioridad**; la accesibilidad se mantiene como QA complementario.

## Resultado principal

El mayor LCP de la muestra está en blog: **13.26s móvil**, repetido12.69–13.39s. Home móvil: **3.17s LCP y1584ms TBT**. Desktop de home: LCP rápido0.97s, pero CLS0.449 en las tres muestras. Las prioridades no se reducen a un score ni a comprimir todas las imágenes.

Se ejecutaron **15 mediciones normales** (5perfiles×3) y **3 contrafactuales** de marketing. Son pruebas Lighthouse locales reales, no PageSpeed nuevo ni CrUX posterior al despliegue. No se modificó el tema ni se publicó nada durante esta auditoría.

## Mediciones actuales: medianas

| Página | Perfil | Performance/100 | LCP s | FCP s | TBT ms | CLS | LCP mín–máx s |
|---|---|---|---|---|---|---|---|
| Inicio | mobile | 65 | 3.17 | 1.75 | 1584 | 0.000 | 3.12–3.18 |
| Inicio | desktop | 74 | 0.97 | 0.44 | 165 | 0.449 | 0.95–1.05 |
| Presoterapia | mobile | 67 | 3.07 | 1.27 | 1544 | 0.027 | 2.58–3.23 |
| PRO AIR | mobile | 63 | 3.56 | 1.53 | 2017 | 0.000 | 3.25–3.59 |
| Blog | mobile | 44 | 13.26 | 1.97 | 1493 | 0.000 | 12.69–13.39 |

Chrome155.0.8059.84, Lighthouse13.6.0, cuatro categorías en cada muestra; caché/almacenamiento reiniciados, contexto anónimo sin decisión de consentimiento. Mobile412×823/DPR1.75, CPU×4, RTT150ms/1638.4Kbps simulados. Desktop1350×940/DPR1, CPU×1, RTT40ms/10240Kbps. Política del motor de lectura: POST bloqueado. No son dispositivos físicos ni condiciones idénticas a PSI. TBT no es INP.

Scores calculados como mediana de las muestras: el resumen original del servicio conserva el score de la primera, que no se presenta aquí como mediana. Los valores originales se preservaron.

## Comparación con la línea base local

| Perfil | LCP antes→ahora s | TBT antes→ahora ms | CLS antes→ahora | Compatibilidad |
|---|---|---|---|---|
| Inicio mobile | 3.67 → 3.17 | 1396 → 1584 | 0.000 → 0.000 | compared |
| Inicio desktop | 1.06 → 0.97 | 176 → 165 | 0.449 → 0.449 | compared |
| Presoterapia mobile | 3.13 → 3.07 | 2097 → 1544 | 0.027 → 0.027 | compared |
| PRO AIR mobile | 3.79 → 3.56 | 1792 → 2017 | 0.000 → 0.000 | compared |

El comparador existente confirmó mismos perfiles y observaciones distintas. Eso habilita comparación descriptiva, **no causalidad ni un gate estadístico**: n=3, variabilidad y otros cambios previos de la copia Cli desplegados por el propietario. Los deltas positivos que el comparador llama regressions no se interpretan como regresiones estadísticamente demostradas. Blog no tenía baseline Lighthouse local equivalente; PSI anterior no sirve para afirmar una caída de score ni empeoramiento numérico.

## JavaScript: experimento acotado, no solución publicada

En una navegación CDP de home390px se midieron104solicitudes y **1,117,137bytes JS**,58,327bytes CSS y362,232bytes de imágenes. Esta ventana y viewport no se mezclan con el total de Lighthouse. GTM/gtag, TikTok y Meta figuran entre los scripts más grandes; LS/vanilla-adapter son contratos nativos y no deben retirarse por tamaño o Coverage.

Se bloquearon solo `www.googletagmanager.com`, `analytics.tiktok.com` y `connect.facebook.net` en tres navegaciones de diagnóstico con el mismo perfil móvil. Los patrones constan en Lighthouse y esas entidades no transfieren sus scripts en los resultados. Tienda y configuración remota permanecieron intactas.

| Home móvil | Normal, mediana3 | Contrafactual, mediana3 |
|---|---|---|
| Performance/100 | 65 | 72 |
| LCP s | 3.17 | 3.75 |
| TBT ms | 1584 | 661 |

TBT baja aproximadamente58.3%, pero LCP empeora aproximadamente18.2%. **No se recomienda desactivar esos servicios como parche.** Se demuestra coste bajo estas condiciones y se justifica investigar eventos/inicialización/diferimiento por necesidad. No se comprobó duplicación de conversiones ni se hicieron compras. La mejora del contrafactual no es una mejora implementada ni de CrUX.

El primer resultado real se conservó cuando el guard de directorio de evidencias detuvo el segundo navegador antes de iniciarlo. Los otros dos usaron un destino nuevo; no se contaron muestras inexistentes ni se reescribió el motor.

## LCP, imágenes y cadena crítica

- **Home:** LCP en poster del video, WebP de unos31KB, eager/high y descubrible en HTML. No justifica otro preload ni culpar únicamente al peso del hero.
- **Categoría/PDP:** imágenes prioritarias nativas; TBT sigue alto. Conservar galería, variantes, stock y compra. El score no identifica por sí solo qué script puede diferirse.
- **Blog:** primera `.blog-card-img` de unos500KB JPG; no descubrible inicialmente y sin hint de prioridad. La fuente `snippets/blog-card.tpl` fuerza lazy JS en todas las cards. El helper nativo ya desactiva lazy y lazy_js cuando recibe image_priority_high (líneas91–92). Parametrizar ese valor para el primer recurso visible y optimizar la portada real es un candidato concreto. El mecanismo de formato/tamaño del CDN/CMS requiere verificación: no se inventan transformaciones ni se cargan todas eager.
- **CSS/fuentes:** Lighthouse estima~960ms de ahorro bloqueante en home; es una estimación, no un beneficio medido del futuro parche. Se observaron fuente Poppins, CSS critical/utilities y libraries-standalone. La última comprobación HTTP de fuente devolvió403 y se detuvo, sin reintentos; no se afirmó duplicación de preload/inline por esa prueba bloqueada.

Los tiempos de subpartes LCP pueden ser observados de traza mientras el LCP final es simulado; no se reparten porcentajes dividiendo magnitudes incompatibles.

## Estabilidad de escritorio

CLS0.449 se repite en las tres muestras de home. El insight del documento superior muestra un subtotal próximo0.068; no debe confundirse con el total que puede incluir frames. La evidencia previa de DevTools/contrafactual sinYouTube apunta al reproductor, pero no demostró el mecanismo exacto. Debe investigarse sin eliminar funcionalidad ni ocultar el main globalmente, y considerando la política de lectura que bloquea POST. Las fuentes también aparecen en cambios del documento principal.

## Campo y APIs de Google

No hubo consultas Google nuevas: las claves están referenciadas pero no disponibles en el entorno de este proceso. Se conservan los reportes directos anteriores como contexto fechado, sin inventar respuestas.

CrUX del origen, periodo12oct–8nov2026: móvil LCP1908ms/INP112ms/CLS0.01; desktop1742ms/65ms/0.06. Home URL no devolvió LCP/INP; PRO AIR móvil devolvió LCP1655ms y CLS0.02 sin INP. No se atribuye el origen al blog ni se declara CWV completo de todas las URLs. Son datos anteriores agregados, no validación inmediata del push. No se infiere INP a partir del TBT.

## Recomendaciones y orden técnico

1. **RHP-01, P1:** primer recurso del blog, descubrimiento y peso. Cambio pequeño sobre componente/helper existentes; conservar paginación, filtros, carruseles y calidad visual. Beneficio final aún no medido.
2. **RHP-02, P1:** JavaScript compartido/marketing: inventario de etiquetas y ensayo individual. El efecto sobre TBT está respaldado; la forma segura de diferir sin perder eventos no. No eliminar scripts de plataforma por Coverage.
3. **RHP-03, P1:** CLS desktop: traza por frame/reproductor y fuentes con video funcional. No cambiar autoplay ni retirar medios sin verificar UX.
4. **RHP-04, P2:** CSS/fuentes críticos: revisar orden y carga por plantilla, conservando layout inicial sin FOUC. No retirar reglas usadas en otros estados.

Este orden responde a la evidencia técnica; no se consultaron tráfico/ventas y la prioridad comercial debe ajustarse con datos autorizados. Cada propuesta exige baseline/candidato equivalentes, QA comercial/SEO/accesibilidad y revisión independiente. La política de regression-gates previa continúa propuesta, sin hook activo ni programación externa.

## Revisión independiente de Claude

No hay propuesta válida de Claude; no se simula revisión ni consenso.

El intento previo de revisión de accesibilidad agotó120s de primera respuesta y fue cancelado/recolectado. El primer intento de performance terminó, pero su JSON fue rechazado sin reparación ambigua. El contrato nativo siguiente pasó sintaxis pero se rechazaron referencias a archivos no incluidos en el allowlist del helper. Se amplió únicamente esa lista de referencias de lectura a archivos existentes y se hizo una última invocación acotada; ambos intentos nativos quedaron rechazados por alcance de referencias y no se hicieron más intentos. No se repararon respuestas ambiguas, no se concedieron escrituras y la revisión independiente permanece pendiente. No se ejecutó CommandCode, no se alteró el orquestador y no se presenta esto como nueva deliberación completa ni autorización de implementación.

## Evidencias y límites

[Resultados normalizados](postpush-performance.json) · [Mediciones originales](../runs/rhino-performance/20261110T205329-postpush-accessibility-7f9a46ef/performance-summary.json) · [Contrafactual](../runs/rhino-performance/20261110T205329-postpush-accessibility-7f9a46ef/marketing-counterfactual.json) · [Revisión de Claude](../runs/rhino-performance/20261110T205329-postpush-accessibility-7f9a46ef/claude-performance-scope-review.json) · [Accesibilidad complementaria](postpush-accessibility.md).

Los12archivos locales vigilados mantienen sus hashes. No se enviaron formularios, no hubo compras ni publicación. La prueba HTTP final403 quedó bloqueada; no se evadió. No se evaluó ni declaró equivalencia criptográfica de todo el código publicado. El diagnóstico no es un parche aplicado ni garantiza una puntuación futura.
