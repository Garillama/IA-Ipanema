# Operación futura y QA

No ejecutada ni autorizada por el permiso de validación.

1. Reconﬁrmar por GET nativo que14828608 sigue publicada; comprobar file-hashes, hash original y respaldo íntegro. Si difieren, detener sin sobrescribir.
2. Enviar un único PATCH nativo de files con un solo upsert text para sections/google-reviews.tpl y contenido del candidato exacto; ninguna eliminación. Verificar hash posterior. No watch/force/sync global, no otros archivos.
3. QA Home real antes y después de acercarse al carrusel, API, Leer más/menos, flechas, scroll, resize, enlace de reseña, teclado Tab/Enter/Space, foco y ARIA. Probar360/390/768/1024/1440/1920px. Confirmar sin JS que permanece el contenido HTML inicial. Comprobar canonical, encabezados, JSON-LD y ausencia de nuevos errores JS.
4. Revisar navegación y ausencia de interferencia con compra/variantes/carrito bajo un alcance específico de lectura. Con POST bloqueado no se certifican eventos de compra ni transacciones. No enviar formularios.
5. Cinco Lighthouse nuevos por dispositivo, perfiles idénticos al CSV, fresca caché/navegador, sin desactivar scripts, registrar benchmarkIndex. Comparar todos los samples, mediana y dispersión; si deriva el host, marcar inconcluso, no declarar causalidad ni hacer reruns sin permiso. Las medianas actuales52/54 están afectadas por drift; no son referencia estable para prometer un delta.
6. Si hay regresión crítica reproducible atribuible al archivo: detener cambios. Solo bajo permiso de reversión, comprobar que el remoto sigue en e6f79c2fd59376efe955662adff44d13329300360a118249c88480d59dde3cd3; restaurar exclusivamente el respaldo de este archivo; verificar75a487600c5d71001fa2e0970dad1cb943f80d399f1af89db559bffc3253fd30 y repetir QA pertinente. Ante hash distinto, detener sin sobrescribir. Fluctuación aislada del score no prueba regresión.

Pendientes: eficacia real, fuentes Poppins y render Twig/componente en tienda completa. Nueva posición arriba del pliegue o uso en editor/iframe exige revalidación proporcional. No se autoriza retirar marketing para hacer subir una puntuación.
