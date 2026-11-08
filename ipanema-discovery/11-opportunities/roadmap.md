# Orden recomendado para la siguiente fase

Fecha: 2026-11-08. Implementación todavía no autorizada por este discovery; cada lote se convierte primero en diff local revisable. [Matriz](priority-matrix.md).

La evolución local del agente SEO sí fue autorizada y está implementada en V2.1: [resultados](../../reports/seo/evolution-report.md). La restricción anterior sigue aplicando al tema/tienda. Para el lote SEO hay un diff no aplicado y [prioridades con evidencia actual](../../reports/seo/audited-pages.md); conectar cuentas o publicar requiere autorización específica.

1. **Estabilizar contexto y contrato.** Mantener perfil por tienda, estado remoto y source efectivo. Resolver qué código es propio y estrategia de actualización del fork. IPN-001/002/022/023.
2. **Corregir barreras de interacción y responsive.** Menú/foco/cierre, nombres de controles y overflow intermedio, mediante fuentes compartidas y pruebas de consumidores. IPN-004/005/006/015.
3. **Asegurar catálogo descubrible y semántica.** Paginación con fallback, JSON-LD 404, title de error y jerarquía de contenido importado. No tomar un score SEO como diagnóstico suficiente. IPN-007/008/009/017/018.
4. **Optimizar la carga real.** Hero final/LCP, tamaños de imágenes y tareas móviles; medir cada cambio con el mismo perfil, evitando una reescritura de todo el JS. IPN-010/011/012/013/014.
5. **Formalizar variantes reutilizables.** Configuraciones por tienda, ciclo de vida de motores y motion accesible. Distribuir solo código con derechos y compatibilidad documentados. IPN-003/016/019/021/024.
6. **Cerrar validación de lanzamiento.** Admin/editor en lectura autorizada, escenarios comerciales controlados y endpoints sin sesión cuando el negocio decida abrir la tienda. No publicar solo para completar una prueba. IPN-020.

Para cada lote: beneficio esperado, coste, riesgos, rutas afectadas, pruebas y criterio de aceptación. El estado cambia a implementado solo después del diff y pruebas reales, no al aceptar esta lista.
