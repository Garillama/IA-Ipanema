---
name: ipanema-performance
description: Medir y optimizar carga, imágenes, CSS, JavaScript, fuentes y terceros de Ipanema con evidencia de red y laboratorio.
---

# Ipanema performance

Activa esta especialidad cuando la petición requiera su responsabilidad descrita arriba. El proyecto y permisos provienen de [AGENTS.md](../../../AGENTS.md); la coordinadora está en el directorio hermano ipanema-storefront. No cargues otras especialidades por defecto.

Fuentes principales, con carga selectiva: [image-loading](../../../ipanema-discovery/05-performance/image-loading.md) · [javascript](../../../ipanema-discovery/05-performance/javascript.md) · [performance-budgets](../../../ipanema-discovery/05-performance/performance-budgets.md) · [performance-checklist](../../../ipanema-discovery/12-playbooks/performance-checklist.md). El discovery es evidencia fechada; confirma archivo actual, compatibilidad y límites antes de usar una conclusión.

Procedimiento: Identifica componente/motor/helper y mide antes de proponer. Contrasta currentSrc, solicitudes, respuesta/bytes, carga completada y geometría visible; DOM no prueba descarga ni decodificación. Revisa LCP real de esa página y prioridad de su rama, lazy y sizes frente al ancho efectivo.

Alcance y límites: Reutiliza paquetes/motores existentes; no añadas dependencias para resolver CSS/layout ni marques CSS/JS prescindible solo por Coverage de una navegación. Los presupuestos son objetivos, no mediciones. No confundir TBT de laboratorio con INP de campo.

Herramientas permitidas: lectura con rg, `tools/ia.py doctor/search/plan`, `tools/find_component.py`, `tools/audit_source.py` y QA/compare/attempt dentro de permisos aplicables. No instales, publiques o sincronices por activar esta skill. No copies credenciales ni código de cliente a evidencia compartida.

Validación: QA de navegador/red y Lighthouse autorizado con perfil idéntico antes/después; compara métricas, assets y bytes. Reporta número de muestras, caché, red/CPU, posibles regresiones y limitaciones de atribución.

Entrega y cierre: identifica fuente nativa, decisión/alternativas, archivos y consumidores, diff si fue autorizado, pruebas ejecutadas con evidencia y pendientes. Finaliza al comprobar el alcance; si faltan accesos/datos, registra el límite sin declarar aprobación. Hallazgo, propuesta y solución verificada conservan estados distintos.
