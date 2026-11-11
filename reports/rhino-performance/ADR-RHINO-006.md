# ADR-RHINO-006 — Home primero, atribución antes de optimizar

Estado: **needs_evidence** para implementación. Fecha:2026-11-11T00:04:35.888619+00:00. Proyecto:rhino-performance. Objetivo:90+PSI mobile/desktop sin perder diseño, comercio, SEO o accesibilidad. Esta decisión autoriza continuar diagnóstico de lectura, no editar/publicar un candidato.

## Fuentes y permisos

[Informe principal](home-performance-strategy.md), [resultados](home-performance-strategy.json), [propuestas/contrastes/defensas](../runs/rhino-performance/20261110T235059-home-priority-diagnosis-2f04055a/council.json), [trazaMCPnueva](../runs/rhino-performance/20261110T235059-home-priority-diagnosis-2f04055a/devtools-mcp-insights.json). Código `2e8c13aefd7b346943e928aee8e598f69dd47374`;339hashes verificables sin cambios de342inventariados (3redactados por serialización); Git limpio sin cambio deHEAD; fingerprint de5assets publicado coincidente. Solo GET/HEAD/OPTIONS y herramientas de inspección. No producción, formularios comerciales, ediciónCMS, ni programación externa.

## Propuestas independientes

**Claude:** Estrategia de diagnóstico: lotes pequeños empezando por el CLS desktop (causa observada: imágenes de cards sin tamaño) y el dimensionado de imágenes. Después, bloqueo de render y diferido del embed de video. Los terceros y el TBT mobile dependen de GTM/apps y requieren autorización del propietario. Alcanzar 90+ mobile es una ruta posible, no garantizada. Sin implementación en esta fase.

**Codex:** Priorizar una ruta nativa por lotes: atribuir el CLS desktop, estabilizar geometría sin cambiar el diseño y después reducir trabajo inicial mobile según trazas. Evaluar terceros por separado. El objetivo 90+ sigue sin demostrarse; esta propuesta no autoriza implementación ni publicación.

## Diferencias, preguntas y respuestas

Codex objetó4aspectos: causaCLS no acreditada, diferimiento que alteraría autoplay, conformidadespass sin candidato y recursoLCP mal identificado. Claude registró5objeciones, incluida la falta de criterios de salida del lote0. Se formularon6preguntas concretas. Las respuestas completas y referencias permanecen en el consejo; no se sustituyen por un voto.

**Claude revisó:** miniaturaYouTube es elLCP; imagen144KB es otro recurso; dimensiones de cards quedan condicionadas a atribución; aplazar autoplaydesktop y pass de conformidad no medidos se retiran. **Codex revisó:** lote0 debe correlacionar frame/geometría/estilos de una misma navegación, atribuir tareas por integración, incluir overflow/teclado y no asumir que solo los terceros explicanTBT.

La traza posterior del controlador vuelve a señalarVIDEO/cluster0.3563 sin causa raíz. Respalda mantener abierta la atribución, no prueba una solución. No se marcan objeciones críticas resueltas por una respuesta ni por consenso: las relativas a causalidad, diseño, comercio y calidad de un futuro candidato necesitan recibos nuevos.

## Decisión y alternativas

Seleccionar **codex-native-sequenced como estrategia de investigación**: Home primero, atribución/criterios de salida, candidato mínimo reutilizando motores actuales, pruebas mobile/desktop y revisión independiente. Ninguna alternativa recibe permiso de edición en esta fase.

Descartadas por ahora: solo dimensionar cards como solución garantizada delCLS, eliminar/diferir todo marketing, cambiar autoplay a interacción, reescribir fuentes sin ensayo, otro helper de imágenes, ocultar contenido o usarCoverage como prueba de código prescindible. No se demuestra90+ con ellas.

Beneficios esperados: menor superficie de cambio y mejores pruebas de causalidad; no se cuantifican puntos o milisegundos de un parche no existente. Coste/riesgo: investigación por frame y validación de terceros puede requerir entorno compatible y permisos adicionales. No se aceptan regresiones comerciales ni visuales a cambio del score.

## Criterios obligatorios antes de implementar

- Causa/candidato respaldado con prueba aislada y consumidores reales; fuentes/hashes vigentes.
- Alcance local autorizado después de revisión de este diagnóstico; ADR actualizado si cambia evidencia.
- Plan de archivos exactos, contratosLS/commerce/imagen/carrusel preservados, reversión por transacción propia.
- Perfiles equivalentes y medianas/rangos; para bloqueo estadístico>=5muestras y tolerancias anteriores a la prueba.
- QAantes/después funcional de lectura, visual6anchos, semántica/JSON-LD, AX/teclado y presupuesto de recursos.
- Revisión independiente del implementador. Twig/plataforma inaccesibles→prueba pendiente explícita; PSIproducción no mide un cambio local no publicado.
- No simular campoHome: LCP/INP porURLausentes; origenagregado separado. Sin claves, informeGoogle nuevo pendiente.

ImpactoSEO/UI/UX/accesibilidad/comercial de un futuro candidato: **unknown hasta probarlo**. LCP/TBT/CLSactuales son observaciones, no certificación.

## Ejecución y trazabilidad

8invocaciones reales:2rechazos iniciales de alcance más6válidas (2propuestas,2contrastes,2defensas). Ambos CLI salieron/reaped; no se atribuyen a autenticación, truncamiento otimeout. La recuperación del reporte local reutilizó nodos completados; no repitió inferencias exitosas. Modelosbalanced/medium, CommandCodefuera.

Duración sumada deworkers:324.8s (no tiempo de pared; hubo paralelismo). CosteClaude comunicado, subtotalUSD2.0381; costeCodex no disponible, coste totaldesconocido. El contexto inicial/recovery y recibos están archivados; se puede compactar más antes del siguiente lote, sin crear infraestructura nueva.

**Sin implementación, diffdeltema, push, publicación o tareas externas programadas.** [Backlog](home-performance-backlog.json). No se reinicia el diagnóstico integral ni se revierte la optimización delblog.

## Seguimiento del primer lote

El propietario autorizó iniciar el primer lote y posteriormente eligió solo pruebas ante el fallo de autenticación de Claude. [ADR-RHINO-007](ADR-RHINO-007.md) conserva un candidato de batching de reseñas probado, sin aplicación al tema. No se altera el estado de las restantes decisiones ni se afirma haber alcanzado90+.
