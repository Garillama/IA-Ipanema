---
name: ipanema-seo-expert
description: Diagnosticar SEO técnico de Ipanema mediante HTML inicial, DOM, enlaces, metadatos, categorías, productos y JSON-LD.
---

# Ipanema seo-expert

Activa esta especialidad cuando la petición requiera su responsabilidad descrita arriba. El proyecto y permisos provienen de [AGENTS.md](../../../AGENTS.md); la coordinadora está en el directorio hermano ipanema-storefront. No cargues otras especialidades por defecto.

Fuentes principales, con carga selectiva: [technical-seo](../../../ipanema-discovery/04-seo/technical-seo.md) · [carousel-seo](../../../ipanema-discovery/04-seo/carousel-seo.md) · [structured-data](../../../ipanema-discovery/04-seo/structured-data.md) · [category-seo](../../../ipanema-discovery/04-seo/category-seo.md). El discovery es evidencia fechada; confirma archivo actual, compatibilidad y límites antes de usar una conclusión.

Procedimiento: Inspecciona HTML inicial y renderizado; identifica H1/ancestros, href reales, paginación, canonical, robots y datos estructurados existentes. Si un H1 está duplicado, determina si viene de user-content o plantilla. En carruseles comprueba enlaces de categoría/producto antes y después de JS y sin JS.

Alcance y límites: Separa descubrimiento, rastreo, renderizado e indexación. No deduzcas indexación a partir de HTML ni agregues otro JSON-LD/heading para compensar contenido editable. Respeta los límites entre tema, plataforma y Search Console.

Herramientas permitidas: lectura con rg, `tools/ia.py doctor/search/plan`, `tools/find_component.py`, `tools/audit_source.py` y QA/compare/attempt dentro de permisos aplicables. No instales, publiques o sincronices por activar esta skill. No copies credenciales ni código de cliente a evidencia compartida.

Validación: Ejecuta QA SEO por página, JSON.parse y navegación sin JS; documenta HTTP y ausencia de acceso a GSC/índice. No presentes validación de JSON como garantía de rich results.

Entrega y cierre: identifica fuente nativa, decisión/alternativas, archivos y consumidores, diff si fue autorizado, pruebas ejecutadas con evidencia y pendientes. Finaliza al comprobar el alcance; si faltan accesos/datos, registra el límite sin declarar aprobación. Hallazgo, propuesta y solución verificada conservan estados distintos.
