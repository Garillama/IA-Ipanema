# ADR — compuerta de geometría de Google Reviews

Estado: ready_for_owner_review_not_deployed. Fecha2026-11-13.

Objetivo: evitar lecturas iniciales innecesarias fuera de pantalla, conservando el diseño y comportamiento del carrusel actual. Único componente consumidor: script de la propia sección. No se altera setupMore, el motor LS, store.js ni los scripts comerciales.

Decisión: gate nativo IntersectionObserver600px, con activación de foco y pointerdown y fallback síncrono. Fuente nativa remota confirmada y respaldada; exacto diff `2c88fb0d3e619b5d08c8e217eecb9e104d9d402dbe47997c95b91f0e4b1c8d32`.

Alternativas: conservar fuente (sin riesgo nuevo, trabajo evitable sigue); coalescer por rAF (más sencillo, pero conserva24 lecturas tras el frame fuera de pantalla); rectángulo raíz inicial (retirado, puede forzar layout); esperar API o diferir terceros (rechazado en este alcance por riesgo comercial/evidencia insuficiente).

Revisión: propuestas independientes, contraste, cuatro preguntas cruzadas respondidas y defensa. Claude revisa el diff de Codex. No hay objeciones críticas abiertas; límites de primer frame, fuentes reales, impresión, lifecycle y eficacia de producción permanecen documentados. No se convierten en pruebas superadas.

Recibos del controlador: controller-candidate-receipt.json, controller-final-gates.json, native-validation-receipt.json. 163 checks aislados; validación nativa exacta sin persistencia aprobada. El coalescing ya estaba medido: se corrigió su omisión en el paquete de contraste sin repetir el ensayo.

implementation_allowed:false. Falta autorización específica del propietario para producción; después falta QA real y medición comparable. Una opinión approve significa revisable para el propietario, no publicación autorizada. Las condiciones de eficacia permanecen needs_evidence. El drift del benchmark impide atribución histórica estable.

Integridad: before `75a487600c5d71001fa2e0970dad1cb943f80d399f1af89db559bffc3253fd30`, after `e6f79c2fd59376efe955662adff44d13329300360a118249c88480d59dde3cd3`. No se cambió el candidato durante contraste/defensa/validación. Cualquier cambio de fuente, diff, disposición o hash invalida la revisión para esa versión.

Reversión: exclusivamente el respaldo de este archivo y solo si coincide el hash remoto posterior; autorización futura requerida. No sobrescribir cambios ajenos. No se ejecutó reversión.
