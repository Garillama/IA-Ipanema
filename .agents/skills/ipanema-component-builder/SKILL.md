---
name: ipanema-component-builder
description: Construir o modificar secciones, bloques y snippets Ipanema mediante composición nativa y contratos parametrizables.
---

# Ipanema component-builder

Activa esta especialidad cuando la petición requiera su responsabilidad descrita arriba. El proyecto y permisos provienen de [AGENTS.md](../../../AGENTS.md); la coordinadora está en el directorio hermano ipanema-storefront. No cargues otras especialidades por defecto.

Fuentes principales, con carga selectiva: [component-inventory](../../../ipanema-discovery/02-native-components/component-inventory.md) · [settings-matrix](../../../ipanema-discovery/02-native-components/settings-matrix.md) · [build-new-section](../../../ipanema-discovery/12-playbooks/build-new-section.md). El discovery es evidencia fechada; confirma archivo actual, compatibilidad y límites antes de usar una conclusión.

Procedimiento: Busca primero la unidad nativa y su ficha. Revisa schema, padres permitidos, defaults, settings efectivos por instancia y consumidores. Prefiere configuración/composición; modifica la fuente compartida solo si el alcance global lo requiere. Reutiliza helper de imagen y motor existentes.

Alcance y límites: Elige y justifica la intervención mínima y conserva atributos de editor/plataforma. Nuevo código necesita contrato y configuración explícitos; no inventes tipos de settings, imports de bibliotecas del editor ni una segunda lógica comercial.

Herramientas permitidas: lectura con rg, `tools/ia.py doctor/search/plan`, `tools/find_component.py`, `tools/audit_source.py` y QA/compare/attempt dentro de permisos aplicables. No instales, publiques o sincronices por activar esta skill. No copies credenciales ni código de cliente a evidencia compartida.

Validación: Valida JSON/schema y composición con audit_source en un destino nuevo; prueba la sección y sus consumidores, contenido vacío/largo, seis anchos pertinentes y fallback esencial.

Entrega y cierre: identifica fuente nativa, decisión/alternativas, archivos y consumidores, diff si fue autorizado, pruebas ejecutadas con evidencia y pendientes. Finaliza al comprobar el alcance; si faltan accesos/datos, registra el límite sin declarar aprobación. Hallazgo, propuesta y solución verificada conservan estados distintos.
