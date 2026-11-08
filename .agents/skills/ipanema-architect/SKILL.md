---
name: ipanema-architect
description: Revisar arquitectura, dependencias, consumidores y compatibilidad de cambios globales o de instancia en Ipanema.
---

# Ipanema architect

Activa esta especialidad cuando la petición requiera su responsabilidad descrita arriba. El proyecto y permisos provienen de [AGENTS.md](../../../AGENTS.md); la coordinadora está en el directorio hermano ipanema-storefront. No cargues otras especialidades por defecto.

Fuentes principales, con carga selectiva: [dependency-map](../../../ipanema-discovery/01-architecture/dependency-map.md) · [platform-limitations](../../../ipanema-discovery/01-architecture/platform-limitations.md) · [regression-risks](../../../ipanema-discovery/10-quality/regression-risks.md). El discovery es evidencia fechada; confirma archivo actual, compatibilidad y límites antes de usar una conclusión.

Procedimiento: Recupera el archivo con search y sigue consumidores directos/transitivos. Confirma includes dinámicos, instancia JSON, schema y hooks en el código actual. Distingue contrato compartido de ajuste por tienda y revisa estado local frente a observación remota fechada.

Alcance y límites: Produce un plan con archivos, consumidores, opciones, costes, compatibilidad y reversión. No transforma el grafo estático en prueba funcional ni decide licencias por presencia de archivos.

Herramientas permitidas: lectura con rg, `tools/ia.py doctor/search/plan`, `tools/find_component.py`, `tools/audit_source.py` y QA/compare/attempt dentro de permisos aplicables. No instales, publiques o sincronices por activar esta skill. No copies credenciales ni código de cliente a evidencia compartida.

Validación: Contrasta el grafo con rg en el tema disponible, hashes/versión y QA de cada consumidor relevante; el manifiesto local puede estar obsoleto.

Entrega y cierre: identifica fuente nativa, decisión/alternativas, archivos y consumidores, diff si fue autorizado, pruebas ejecutadas con evidencia y pendientes. Finaliza al comprobar el alcance; si faltan accesos/datos, registra el límite sin declarar aprobación. Hallazgo, propuesta y solución verificada conservan estados distintos.
