---
name: ipanema-visual-qa
description: Ejecutar QA responsive, accesibilidad e interacciones y comparar capturas/métricas antes y después de un cambio Ipanema.
---

# Ipanema visual-qa

Activa esta especialidad cuando la petición requiera su responsabilidad descrita arriba. El proyecto y permisos provienen de [AGENTS.md](../../../AGENTS.md); la coordinadora está en el directorio hermano ipanema-storefront. No cargues otras especialidades por defecto.

Fuentes principales, con carga selectiva: [testing-matrix](../../../ipanema-discovery/10-quality/testing-matrix.md) · [accessibility](../../../ipanema-discovery/10-quality/accessibility.md) · [regression-risks](../../../ipanema-discovery/10-quality/regression-risks.md). El discovery es evidencia fechada; confirma archivo actual, compatibilidad y límites antes de usar una conclusión.

Procedimiento: Elige página/selector y estados reales; captura baseline antes del cambio con el mismo perfil y contenido. Usa qa page/component/browser/full en el proyecto registrado. Define umbrales y máscaras de contenido dinámico, conservando dimensiones/espacio; no enmascares la sección que intentas comprobar.

Alcance y límites: No adapta estilos para que pase una captura: reporta la causa a responsive/component-builder/commerce. Una diferencia de píxeles no decide si el cambio era esperado. No certifica WCAG AA ni indexación; no envía formularios comerciales.

Herramientas permitidas: lectura con rg, `tools/ia.py doctor/search/plan`, `tools/find_component.py`, `tools/audit_source.py` y QA/compare/attempt dentro de permisos aplicables. No instales, publiques o sincronices por activar esta skill. No copies credenciales ni código de cliente a evidencia compartida.

Validación: Ejecuta compare visual/metrics y pruebas de foco, Escape, enlaces y contraste pertinentes. Registra capturas, configuración, checks fallidos, máscaras y revisión necesaria; detén rate limits y nunca reutilices evidencia de password como storefront.

Entrega y cierre: identifica fuente nativa, decisión/alternativas, archivos y consumidores, diff si fue autorizado, pruebas ejecutadas con evidencia y pendientes. Finaliza al comprobar el alcance; si faltan accesos/datos, registra el límite sin declarar aprobación. Hallazgo, propuesta y solución verificada conservan estados distintos.
