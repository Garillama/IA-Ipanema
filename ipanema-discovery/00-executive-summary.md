# Resumen ejecutivo

Fecha: 2026-11-08. **La base del agente y el discovery del alcance accesible están preparados.** Se inventariaron 330 archivos del tema, con 51 secciones, 54 bloques, 118 snippets, 25 templates JSON, 708 definiciones de controles y 178 instancias de secciones/bloques. Después del acceso autorizado se recorrieron 48 URLs, correspondientes a 46 destinos HTML únicos y 13 tipos públicos, con seis anchos por tipo representativo. El editor autenticado y estados comerciales con escritura siguen pendientes. [Evidencia estática](13-evidence/measurements/source-baseline/source-summary.json), [cobertura ejecutada](13-evidence/measurements/coverage-summary.json).

La arquitectura es Ipanema seccionable: Twig, schemas por unidad, datos JSON y lógica de comercio sobre `LS`. El CLI remoto identifica la instalación **14837617, Ipanema Deco 1.8.0, publicada y con fork**. Su comparación informa 329 archivos iguales, sin altas, cambios, eliminaciones ni fallas de lectura. El manifiesto local dice `theme: null`, versión `1` y `forked: false`; está desactualizado respecto de esa lectura. No se corrigió durante discovery. [Estado remoto](13-evidence/measurements/source-baseline/remote-themes.json), [diff de lectura](13-evidence/measurements/source-baseline/remote-diff.json).

Sin sesión, las URLs pública y preview terminaron en `/password/`, con recursos de **14517784 / Ipanema 1.2.1**, incluidos scripts Embla y Sectionfy ausentes del checkout. Después de que el propietario proporcionó acceso, el storefront cargó **1.8.0**, coincidiendo con el proyecto. La causa de que la pantalla de acceso use otra instalación no está demostrada. Sus métricas quedan separadas del storefront. [Pantalla sin sesión](13-evidence/measurements/http/owner-public-url.json), [home autorizada](13-evidence/measurements/browser/storefront-discovery.json).

## Lo que ya permite trabajar con limpieza

- Las tarjetas de listados y los productos de bloques comparten `snippets/product-list/product-item/item.tpl`; las diferencias se parametrizan. La galería y formulario del producto destacado también reutilizan los de PDP.
- `snippets/image.tpl` centraliza imágenes, fuentes responsive, prioridad y lazy loading. No hace falta crear un segundo helper de imágenes.
- El grupo permite dirección diferente en mobile; productos y categorías pueden variar grid/slider por dispositivo con el mismo contenido. La matriz muestra qué ajustes existen realmente.
- Hay FAQ, acordeón, newsletter, popups, cuenta, suscripciones, kits, blog, banners y navegación anidada. Su presencia no prueba que todas las capacidades estén habilitadas por la cuenta o sus datos.
- Los metadatos del head vienen de plataforma y el JSON-LD del tema. Duplicarlos en nuevas secciones agrega conflictos; no es una mejora SEO automática.

Estas conclusiones se sustentan en las [fichas enlazadas](02-native-components/component-specifications.md), el [mapa de dependencias](01-architecture/dependency-map.md) y los documentos de comercio.

## Atención antes de implementar

El template de categoría guardado usa paginación `infinite`, aunque el setting global `pagination` sea `classic`. El control «mostrar más» de esa rama carece de `href`; hay que verificar descubrimiento de páginas posteriores y fallback. Las imágenes de tarjetas declaran `50vw` en desktop aunque la categoría tiene cuatro columnas; hay riesgo de selección sobredimensionada. Ambos se verificaron en código, sin medir aún su efecto en categoría desbloqueada.

En el storefront se confirmó desborde de home y PDP representativa en 768/1024 px, problemas de foco/cierre del menú móvil, nueve PDP con un H1 adicional en contenido y JSON-LD inválido en la 404. Lighthouse mobile obtuvo LCP **4.133 s en home**, **3.834 s en categoría** y **3.492 s en PDP**, con TBT entre **403 y 485 ms**. Son muestras únicas de laboratorio; no datos de usuarios reales. [Resultados](05-performance/storefront-lighthouse-results.md), [hallazgos](11-opportunities/critical-findings.md).

El agente quedó definido en [AGENTS.md](../AGENTS.md) y en la [skill local](../.agents/skills/ipanema-storefront/SKILL.md). No hay watcher, publicación automática ni motor Craft Anything instalado. La estrategia reutilizable se propone en documentación; no se implementaron nuevas secciones ni una biblioteca de storefront.
