# RHINO — comprobación pública tras push

Muestra del 10-11-2026: 9 URLs, 30 estados responsive; axe/Chrome y comprobaciones de teclado/AX. Sin escrituras remotas ni modificaciones del tema.

Se confirmaron en producción role=img del logo Google, un único footer/contentinfo, nombre de Cerrar, H1 en ambas categorías, nombres de selectores, retirada del role=button del pack y estados de Leer más.

| Página, referencia a 390 px | Antes: reglas/nodos | Ahora: reglas/nodos |
|---|---|---|
| article_1 | color-contrast:4, list:1 | list:1 |
| article_2 | color-contrast:6 | ninguna detectada |
| blog | aria-prohibited-attr:1, color-contrast:1 | aria-prohibited-attr:1, color-contrast:1 |
| bundle | color-contrast:6, nested-interactive:3, select-name:4 | color-contrast:3 |
| category | color-contrast:3, label-content-name-mismatch:3 | ninguna detectada |
| category_accessories | color-contrast:5, label-content-name-mismatch:5 | ninguna detectada |
| home | aria-prohibited-attr:1, color-contrast:18, label-content-name-mismatch:2 | color-contrast:1 |
| product | color-contrast:3, label-content-name-mismatch:3, link-name:1 | ninguna detectada |
| product_accessory | color-contrast:3, label-content-name-mismatch:3 | ninguna detectada |

Los números son nodos señalados por regla en una captura, no personas ni defectos únicos de toda la tienda. La comparación a seis anchos está en los originales. Nuevos estados/scroll pueden descubrir fallos que no aparecen inicialmente.

La home obtiene 97/100 de accesibilidad en Lighthouse local móvil y escritorio (una muestra por perfil, categoría accesibilidad). No es PageSpeed ni certificación WCAG.

Pendientes: precio tachado de productos principales (#999 sobre blanco, ratio2.84), contraste de descuentos creados por hydrateComparePrice (#FF343B, ratio3.61), textos de niveles/estado vacío del pack, control de foco del menú móvil, puntos de carruseles de7–10px con separación insuficiente, ARIA/contraste en paginación del blog, lista inválida del artículo y overflow a1024/1440. No son todos regresiones atribuidas al parche.

La prueba de menú inicial devolvía focus_returned=true porque el foco nunca había abandonado el disparador. La prueba posterior con Tab demuestra foco en Buscar fuera del panel, Escape sin cierre y cierre por botón con foco en BODY. No se cuenta el primer indicador como aprobación.

El fixture anterior no cubría la rama asíncrona hydrateComparePrice y retiraba una supresión local de outline sin comprobar la regla global .form-control:focus outline0!important. En el sitio el selector conserva foco pero outline=none; otros indicadores (borde/sombra) siguen sin validarse. Eso demuestra por qué la aprobación local se entregó como parcial.

Claude inició una revisión independiente de esta evidencia, pero agotó120s de primera respuesta y su proceso fue cancelado/recolectado. No hay una revisión aprobada de Claude para esta parte ni se activó CommandCode. El análisis observacional es del controlador Codex; no se ocultó el fallo.

El propietario indicó después que **rendimiento es la prioridad**; se amplió el análisis con nuevas series Lighthouse completas, separadas de estas mediciones de accesibilidad.
