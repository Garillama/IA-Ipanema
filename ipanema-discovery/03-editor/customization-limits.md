# Límites de personalización

Fecha: 2026-11-08. La fuente principal para permisos es [límites de plataforma](../01-architecture/platform-limitations.md); para controles, [settings](settings.md).

Una composición nueva con hero, group, heading, image y button existentes puede ser un cambio de datos. Un tipo nuevo en `sections/` es un cambio de código. Un rediseño de product card compartida afecta catálogo y módulos que la consumen: no debe insertarse una card alternativa completa como atajo.

`blocks/code.tpl` imprime `block.settings.code | raw`; `layouts/layout.tpl` permite `settings.css_code | raw`. Son puntos reales de código propio, pero el código guardado no pasa por una arquitectura compartida automáticamente. Es posible crear conflictos, scripts duplicados y contenido dependiente de JS desde esos campos. Para trabajo continuo, preferir unidades con responsabilidad y versión; conservar código por tienda únicamente donde varíe su contenido/configuración.

Cambiar el schema requiere fork y mantenimiento de traducciones. No se asume que un control arbitrario de CSS tenga equivalente en el editor. Tampoco se asume API pública del Brand Editor, importación de paquetes de componentes ni persistencia automática de customizaciones de source tras actualizar.

Las capacidades de la cuenta, el editor autenticado, el comportamiento de guardar en publicado y las restricciones server-side no se probaron. No se alteró ningún setting para descubrirlas.
