---
name: ipanema-motion
description: Diseñar y revisar animaciones, transiciones y microinteracciones de Ipanema con reduced motion y coste de renderizado medido.
---

# Ipanema motion

Activa esta especialidad cuando la petición requiera su responsabilidad descrita arriba. El proyecto y permisos provienen de [AGENTS.md](../../../AGENTS.md); la coordinadora está en el directorio hermano ipanema-storefront. No cargues otras especialidades por defecto.

Fuentes principales, con carga selectiva: [performant-patterns](../../../ipanema-discovery/06-motion/performant-patterns.md) · [native-animations](../../../ipanema-discovery/06-motion/native-animations.md) · [motion-accessibility](../../../ipanema-discovery/06-motion/motion-accessibility.md) · [carousels](../../../ipanema-discovery/07-commerce/carousels-and-galleries.md). El discovery es evidencia fechada; confirma archivo actual, compatibilidad y límites antes de usar una conclusión.

Procedimiento: Identifica el efecto nativo/motor y objetivo UX. Evalúa layout, paint, composite, memoria y eventos; transform/opacity no son gratuitos. Conserva contenido disponible al fallar JS y layout inicial estable. Prefiere CSS/WAAPI nativos suficientes y observa compatibilidad antes de proponer scroll-driven animation.

Alcance y límites: Define duración/propiedades y alternativa de prefers-reduced-motion; no conviertas efectos en requisito para navegar/comprar. No crear otro carrusel si Swiper existente basta. performance diagnostica la carga; motion decide el efecto.

Herramientas permitidas: lectura con rg, `tools/ia.py doctor/search/plan`, `tools/find_component.py`, `tools/audit_source.py` y QA/compare/attempt dentro de permisos aplicables. No instales, publiques o sincronices por activar esta skill. No copies credenciales ni código de cliente a evidencia compartida.

Validación: Compara modo normal/reduce y teclado, autoplay/pausa si aplica, CLS, tareas y paint. QA en móviles y efecto desactivado; no prometer FPS o coste GPU sin perfilado ejecutado.

Entrega y cierre: identifica fuente nativa, decisión/alternativas, archivos y consumidores, diff si fue autorizado, pruebas ejecutadas con evidencia y pendientes. Finaliza al comprobar el alcance; si faltan accesos/datos, registra el límite sin declarar aprobación. Hallazgo, propuesta y solución verificada conservan estados distintos.
