# Responsive y cascada

Fecha: 2026-11-08. Evidencia: schemas, blocks/group.tpl L19-L47, sections/header.tpl L22-L52 y archivos CSS del [inventario](../05-performance/static-asset-measurements.md).

De las definiciones, 74 IDs contienen mobile, 6 desktop y ninguna tablet; los 628 restantes se clasifican compartidos **por nombre**, no por alcance visual garantizado. `columns` suele representar desktop aunque no lo nombre; los IDs no sustituyen leer Twig/CSS.

| Corte encontrado | Origen | Uso / precaución |
|---|---|---|
| 576 px | style-critical.css | Reglas particulares; no es el cambio global a desktop |
| 768 px | Tres CSS y numerosos matchMedia/innerWidth en JS | Corte dominante para md, mobile/desktop, grid/slider y galerías |
| 992 px | style-critical.css | Ajustes intermedios |
| 1024 px | style-async.css | Reglas de componentes concretos |
| 1200 px | style-critical.css y rango 768–1200 | Ajustes de layout |
| 1400 px | style-critical.css | Pantallas amplias |
| hover:hover | style-async.css | Efectos según capacidad de interacción, no ancho |

No se debe introducir un breakpoint nuevo solo por preferencia visual. Primero identificar el contrato del componente; crear una condición CSS local si es necesaria y verificar límites a ambos lados. Además de los seis anchos pedidos, una modificación sensible a md necesita comprobar 767/768/769 px.

`group` genera una sola estructura y cambia entre `flex-column flex-md-row` y otras combinaciones. Es la alternativa comprobada para una editorial en columnas desktop y apilada mobile. `products` comparte tarjetas y puede usar slider solo en un dispositivo mediante data attributes de formatos; no necesita dos listados de productos. El orden CSS no debe contradecir lectura/teclado.

El padding de hero se inyecta como style compartido. Un media query externo que intente cambiar `padding` del mismo nodo puede perder contra ese inline, llevando a `!important`. Antes de añadirlo, usar control disponible, cambiar la fuente para emitir custom properties por dispositivo si la tarea autoriza código, o aplicar un wrapper con responsabilidad clara. No sumar ambos paddings accidentalmente.

Las utilidades traen 496 ocurrencias de `!important`, por diseño de esa capa. `d-none` y `d-md-*` pueden vencer estilos de componente aunque estos se carguen después. Si una instancia no debe ocultarse, corregir la clase que la oculta suele ser más limpio que otro override. No eliminar todas las utilidades.

Para una variante nueva: base mobile legible, un solo DOM, settings específicos únicamente donde aporten control, selector de componente/instancia y tokens compartidos. Evitar selectores globales de `img`, `.btn` o `h2` para arreglar un módulo aislado. Un ID de sección puede acotar un ajuste local, pero no constituye un contrato portable entre tiendas.

La matriz real incluye home y doce tipos públicos adicionales en los seis anchos. Detectó overflow de home y PDP representativa en 768/1024. En home se localizaron flechas de carrusel fuera del viewport. No equivale a todos los presets, productos o estados. [Resultados responsive](../10-quality/responsive-results.md), [QA](../10-quality/testing-matrix.md).
