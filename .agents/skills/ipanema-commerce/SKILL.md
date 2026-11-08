---
name: ipanema-commerce
description: Modificar presentación de cards, PDP, variantes y carrito Ipanema conservando lógica nativa y límites de checkout.
---

# Ipanema commerce

Activa esta especialidad cuando la petición requiera su responsabilidad descrita arriba. El proyecto y permisos provienen de [AGENTS.md](../../../AGENTS.md); la coordinadora está en el directorio hermano ipanema-storefront. No cargues otras especialidades por defecto.

Fuentes principales, con carga selectiva: [product-cards](../../../ipanema-discovery/07-commerce/product-cards.md) · [product-detail](../../../ipanema-discovery/07-commerce/product-detail.md) · [cart](../../../ipanema-discovery/07-commerce/cart.md) · [events-and-hooks](../../../ipanema-discovery/09-integrations/events-and-hooks.md). El discovery es evidencia fechada; confirma archivo actual, compatibilidad y límites antes de usar una conclusión.

Procedimiento: Localiza item.tpl, helper, galería/formulario y todos sus consumidores. Revisa entradas product/settings/template, slide_item/reduced_item, variantes, URLs y hooks actuales. Separa presentación de lógica LS/plataforma; destaca parámetros nativos en vez de copiar una card o formulario.

Alcance y límites: Conserva precio, disponibilidad, variantes, contratos data-store/js-*, formularios y eventos. No reemplaces endpoints internos por una API inventada ni asumas control del checkout desde el tema. Cualquier transacción o dato real exige autorización específica.

Herramientas permitidas: lectura con rg, `tools/ia.py doctor/search/plan`, `tools/find_component.py`, `tools/audit_source.py` y QA/compare/attempt dentro de permisos aplicables. No instales, publiques o sincronices por activar esta skill. No copies credenciales ni código de cliente a evidencia compartida.

Validación: Prueba consumidores home/categoría/búsqueda/relacionados pertinentes, longitudes, descuentos y estados disponibles; selección de variante y estados sin compra cuando esté autorizado. Registra agotados/error/carrito con productos no probados como pendientes.

Entrega y cierre: identifica fuente nativa, decisión/alternativas, archivos y consumidores, diff si fue autorizado, pruebas ejecutadas con evidencia y pendientes. Finaliza al comprobar el alcance; si faltan accesos/datos, registra el límite sin declarar aprobación. Hallazgo, propuesta y solución verificada conservan estados distintos.
