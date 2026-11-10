# ADR-RHINO-002 — diagnóstico integral y estrategia de optimización

Fecha: 2026-11-10. Proyecto: rhino-performance. Sitio: https://rhino-performance.com/. Referencia pública de assets14828608.

**Estado: needs_evidence para implementación.** Se entrega diagnóstico y backlog para revisión del propietario. No autoriza modificar tema, catálogo, aplicaciones ni producción.

## Problema y evidencia

La home no representa por sí sola la tienda: PageSpeed muestra LCP móvil alto en productos/blog, pero los perfiles locales y el campo no son equivalentes. PRO AIR móvil tiene LCP de campo1.655s y falta INP; no hay un pase CWV completo ni una emergencia universal demostrada. Se observan defectos reales de accesibilidad compartida, estructura, packs,404 y representación de precios. El Offer principal usa el precio anterior mientras la UI muestra el activo en dos PDP.

Fuentes: [informe](integral-audit.md), [evidencia fechada](integral-evidence.json), [baseline](performance-baseline.json), [backlog](integral-backlog.json).16URLs/50estados, PSI10, Lighthouse18muestras+3contrafactuales, CrUX URL/origen e History, AX/axe/CDP y MCP real. No son pruebas de índice Google ni de compra.

## Propuestas independientes y contraste

Claude propuso diagnóstico por plantilla con video/home, blog, JS/CSS y accesibilidad. Codex propuso matriz plantilla×componente con prioridad a productos, packs, categorías y límites de causalidad. Se realizaron9objeciones,6preguntas y6respuestas. Claude retiró una opción centrada solo en home y corrigió garantías sin pruebas a unknown. Ambos prefirieron la matriz por componentes. Propuestas, preguntas, defensas, modelos, tiempos/tokens/costes disponibles y rechazos conservados en [integral-council.json](integral-council.json).

Se añadieron revisiones incrementales de campo y precios, sin repetir discovery. Ambos distinguen LCP de campo bueno de CWV completo sin INP. Ambos consideran prioridad alta la discrepancia del Offer principal, distinta de las alertas D010 de cards relacionadas. No afirman error observado en Merchant Center ni pérdida comercial atribuible.

## Decisión

1. Priorizar verificación de la fuente nativa de Offer.price y casos de oferta/variantes/suscripciones, sin cambiar datos comerciales ni copiar precios fijos.
2. Diagnosticar por separado LCP móvil de producto y primer recurso del blog; reutilizar snippets/flags nativos y conservar lazy en recursos no críticos.
3. Investigar estabilidad del video y comportamiento real del reproductor. El bloqueo temporal de YouTube redujo CLS bajo la política controlada, pero elimina funcionalidad y no es una corrección entregable.
4. Corregir después de autorización los defectos de accesibilidad/semántica en componentes compartidos, con sus consumidores y responsive comprobados.
5. Conservar baseline por perfil y la política de gates. No afirmar un guard activo: faltan hook, datos suficientes y pruebas del candidato posterior. No programar consultas externas sin permiso.

## Alternativas descartadas

Limitar auditoría a la home; tratar PSI y local como antes/después; inferir INP a partir de TBT; atribuir el origen CrUX a todas las URLs; remover aplicaciones o librerías solo por Coverage; ocultar overflow globalmente; duplicar JSON-LD para ocultar el original; reemplazar lógica de precio/carrito; usar el contrafactual sin video como optimización aprobada; habilitar CommandCode por failover.

## Objeciones y condiciones abiertas

La correspondencia entre fuente local y despliegue no está certificada. Faltan mecanismo exacto de CLS/overflow, validación funcional del video sin interferencia de la política POST, cobertura de variantes/stock y fuentes comerciales autorizadas, usuario con lector de pantalla, carrito poblado/checkout y verificación GSC/Merchant. Estas condiciones impiden aprobar un parche. No se resuelven por mayoría ni por preferencia de proveedor.

## Impactos y riesgos

SEO: consistencia Product/Offer, H1, canonical y JSON-LD sin duplicación; no garantiza indexación ni rich results. Rendimiento: beneficios propuestos aún no medidos tras un cambio; no prometer mejoras de CrUX inmediatas. UI/UX: preservar composición, autoplay/manual elegido por negocio, foco y contenido. Accesibilidad: nombres/roles/contraste/landmarks y estados; no certificación WCAG. Comercio: conservar variantes, stock, suscripciones, descuentos, cart, LS, hooks y slots; ninguna compra o modificación de catálogo.

## Pruebas obligatorias antes de una futura aprobación

Binding de código/despliegue y diff acotado; baseline y candidato con perfiles compatibles; QA responsive/sin JS/reduced-motion y lector de pantalla; Offer vs datos autorizados por variante/estado; navegación/galería/teclado; regresión visual con máscaras explícitas; video funcional y CLS de traza; consumidores por componente. Los errores críticos o la evidencia insuficiente bloquean liberación técnica. Reversión solo del diff propio mediante backup/hashes, sin reset/clean.

## Autorizaciones

Lecturas públicas y diagnóstico: autorizados. Implementación del tema: pendiente de revisión y autorización específica. Aplicaciones, cuentas privadas, catálogo, checkout o publicación: no autorizados. No se creó programación externa ni despliegue.
