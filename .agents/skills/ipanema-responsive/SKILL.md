---
name: ipanema-responsive
description: Resolver layout, cascada y controles por dispositivo en Ipanema sin duplicar contenido ni romper orden semántico.
---

# Ipanema responsive

Activa esta especialidad cuando la petición requiera su responsabilidad descrita arriba. El proyecto y permisos provienen de [AGENTS.md](../../../AGENTS.md); la coordinadora está en el directorio hermano ipanema-storefront. No cargues otras especialidades por defecto.

Fuentes principales, con carga selectiva: [responsive-controls](../../../ipanema-discovery/03-editor/responsive-controls.md) · [responsive-system](../../../ipanema-discovery/08-design-system/responsive-system.md) · [responsive-results](../../../ipanema-discovery/10-quality/responsive-results.md). El discovery es evidencia fechada; confirma archivo actual, compatibilidad y límites antes de usar una conclusión.

Procedimiento: Lee el setting y su consumo Twig/CSS, no solo el ID mobile/desktop. Revisa breakpoint, orden DOM, herencia, especificidad, flex/grid, contenedor y flechas. Comprueba si un grupo nativo admite dirección distinta antes de duplicar una sección.

Alcance y límites: Conserva un contenido y orden de lectura lógico. Cambia la fuente de la regla; no encubras overflow con overflow hidden global ni acumules overrides !important. La skill visual-qa mide regresiones; aquí se decide la corrección de layout.

Herramientas permitidas: lectura con rg, `tools/ia.py doctor/search/plan`, `tools/find_component.py`, `tools/audit_source.py` y QA/compare/attempt dentro de permisos aplicables. No instales, publiques o sincronices por activar esta skill. No copies credenciales ni código de cliente a evidencia compartida.

Validación: Prueba 360/390/768/1024/1440/1920 y límites del breakpoint, zoom/reflow y teclado según alcance. Geometría de solapamientos/recortes produce candidatos: confirma intención antes de corregir.

Entrega y cierre: identifica fuente nativa, decisión/alternativas, archivos y consumidores, diff si fue autorizado, pruebas ejecutadas con evidencia y pendientes. Finaliza al comprobar el alcance; si faltan accesos/datos, registra el límite sin declarar aprobación. Hallazgo, propuesta y solución verificada conservan estados distintos.
