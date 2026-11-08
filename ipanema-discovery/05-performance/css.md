# CSS y especificidad

Fecha: 2026-11-08. Los CSS suman **252,517 bytes sin compresión**: critical 122,291; utilities 32,236; async 97,990. Contienen respectivamente 15, 496 y 23 ocurrencias de `!important`. Esto es una medida textual, no un índice de calidad ni tiempo de renderizado. [Inventario](static-asset-measurements.md).

Los tokens centralizan identidad y geometría. Los componentes usan clases, variables y estilos inline generados por settings. Las utilidades buscan prevalecer de forma intencional. Añadir al final un bloque global cada vez que cambia una sección acumula contratos de cascada; es preferible cambiar el control/fuente adecuada o una variante acotada. No hace falta prohibir toda utilidad importante nativa para cumplir el objetivo del usuario.

El critical incluye estilos de múltiples páginas y de Swiper; «critical» es el nombre del archivo, no una demostración de que cada regla sea necesaria para el primer viewport. La separación óptima requiere Coverage y pruebas por ruta/estado. La pantalla de password mostró mucho CSS sin uso en Lighthouse; eliminarlo basándose solo en esa pantalla rompería catálogo y PDP.

No se identificó `@layer` como arquitectura existente ni container queries como base del sistema. Una incorporación futura debe considerar la prioridad de CSS sin layer y de !important: meter solo nuevos estilos en una capa no garantiza que ganen. Containment o content-visibility pueden servir a bloques fuera del viewport si se conserva tamaño intrínseco y accesibilidad; no aplicarlos a sticky, dropdowns o contenido LCP sin probar efectos.

Duplicación se debe evaluar por reglas y responsabilidad, no solo por nombres repetidos. Repetir un selector dentro de un breakpoint puede ser correcto. Para un cambio pequeño, revisar la regla existente, estilos computados y nodo afectado suele ser más útil que instalar un linter o reconstruir el CSS del tema entero. [Responsive](../03-editor/responsive-controls.md) y [carga estable](loading-stability.md).
