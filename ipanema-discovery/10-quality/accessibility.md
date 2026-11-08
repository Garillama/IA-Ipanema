# Accesibilidad y UX

Fecha: 2026-11-08. WCAG 2.2 AA es la referencia de revisión, no una certificación emitida por axe. [Recomendación W3C](https://www.w3.org/TR/WCAG22/).

Se ejecutó axe con tags WCAG A/AA, 2.1 y 2.2 en home y representantes de los tipos públicos a 390 y 1440, además de menú móvil abierto. Los JSON conservan violations, incomplete, selectores e información del motor. Las reglas que no devolvieron incidencias no sustituyen lector de pantalla, revisión de contenido ni todos los estados.

| Resultado reproducido | Contexto | Acción propuesta |
|---|---|---|
| color-contrast | Home editorial_2 y PDP representativa | Corregir tokens/colores de la instancia, conservando identidad y revisando los demás usos |
| label-content-name-mismatch | Cards, carrito y otros controles según viewport | Revisar nombre accesible vs texto visible; confirmar cada caso antes de modificar aria-label global |
| target-size | PDP representativa | Medir controles señalados y separación, considerando excepciones de WCAG |
| aria-prohibited-attr | Registro/login según resultados, y pantalla de password inicial | Revisar elemento de mostrar contraseña y rol/atributos permitidos |
| document-title | 404 y pantalla de password inicial | Revisar emisión de plataforma para ese tipo, sin añadir un segundo title |
| button-name | Botón de cierre del menú abierto | Proporcionar nombre accesible consistente en el modal compartido |

La prueba de menú a 390 registra foco en el disparador al abrir, seis Tabs fuera del panel y display flex después de Escape, incluso tras esperar las transiciones finitas. No se detectó role/aria-modal/nombre en el contenedor observado. Un menú de navegación no necesita siempre role dialog: decidir el patrón correcto, pero el comportamiento actual requiere revisión de foco/recorrido y cierre. [Evidencia de estados](../13-evidence/measurements/browser/state-audit.json).

El intento automatizado de abrir cart drawer vacío no lo mostró en esa ejecución; no se registra como aprobado ni se atribuye causa sin otra reproducción. La página de carrito vacío sí respondió y fue capturada. La selección de otra variante de PDP se probó sin compra; no prueba validación de stock ni error del servidor.

Pendientes humanos: lector de pantalla, navegación completa sin ratón, zoom 200/400%, contraste de todos los medios configurables, reflow con preferencias de fuente, validación/error de formularios y estados comerciales con datos controlados. Los efectos opcionales no usados requieren prueba específica; [motion](../06-motion/motion-accessibility.md).

Conservar alt apropiado, labels asociados, foco visible y estados anunciables. No agregar ARIA para tapar HTML semántico deficiente ni remover atributos indiscriminadamente para «pasar axe». La calidad de la tienda también depende del contenido cargado por el comerciante.
