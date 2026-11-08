# Ciclo de renderizado y actualización

Fecha: 2026-11-08. Fuente principal: [layout.tpl](/home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/layouts/layout.tpl:1), [store.js](/home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/static/js/store.js:4004).

1. La plataforma resuelve tienda, ruta, entidades y plantilla; Twig recibe objetos y settings. No se ejecutó ese backend localmente.
2. `component('head-tags')` delega los metadatos. Se solicita el filtro `static_inline` para CSS crítico y utilidades, se insertan tokens y se declara CSS async con `media="print"` y `onload`. La forma final emitida por plataforma debe revisarse en el HTML de cada instalación; el comentario «inline» no es una medición de red.
3. Se componen header, contenido, footer y cart drawer desde JSON. Los snippets producen enlaces, formularios y datos iniciales; slots y `data-store` preservan extensiones de apps.
4. Se carga `libraries-standalone.js` de forma bloqueante al final del body. Incluye lazysizes y Swiper.
5. `LS.ready.then(...)` incluye `libraries.js.tpl` y agrega dinámicamente `store.js`. Este registra inicialización con `DOMContentLoaded.addEventOrExecute(init)`; ese helper depende del runtime, no del evento DOM nativo con el mismo nombre.
6. `init()` inicia carrito, header, navegación, sliders, variantes, formularios y notificaciones. Muchas ramas comprueban selectores y salen si no existen; el coste del archivo se paga igualmente al descargarlo/parsearlo.
7. Las interacciones de comercio delegan en LS. El carrito puede reemplazar su sección y restaurar estado. El editor comunica selección mediante `brand-editor:select-element` y puede reconciliar contenido; las guardas de inicialización evitan duplicados en algunas ramas.

No se observó `import()` ni chunks dinámicos como estrategia general del tema. Agregar un nuevo listener por cada actualización del editor puede duplicar ejecuciones aunque cada slider esté protegido: revisar también listeners a `document`, observers, timers y teardown.

El HTML inicial debe conservar dimensiones y estructura útiles antes del paso 5. Los estilos de sliders sin inicializar ya existen en `style-critical.css` (bloques alrededor de L3330 y L4929); reforzar ese patrón ofrece mayor estabilidad que rediseñar el DOM tras `load`. [Carga estable](../05-performance/loading-stability.md).
