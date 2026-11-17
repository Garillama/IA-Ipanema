# Exportaciones siguientes: obtener la evidencia que falta

No repetir los archivos ya recibidos ni las15 inspecciones conservadas. No aportar claves, cookies ni archivos OAuth.

## A. Asociar las exclusiones a URLs reales

En la propiedad Rhino de Search Console, **Indexación → Páginas → Todas las páginas conocidas**:

1. Abre **Rastreada: actualmente sin indexar** y exporta su tabla de ejemplos (el resumen recibido indica33).
2. Abre **Descubierta: actualmente sin indexar** y exporta su tabla de ejemplos (indica5).
3. Abre **No se ha encontrado (404)** y exporta su tabla (indica33).
4. Abre **Ver datos sobre páginas indexadas** y exporta los ejemplos disponibles. El gráfico recibido muestra141 al8noviembre, pero no trae sus URLs.

Conserva el motivo literal, fecha de actualización mostrada, filtros, archivo original y metadatos. Los conteos pueden haber cambiado desde el archivo actual: no fuerces coincidencia. Las tablas de ejemplos pueden ser incompletas; una URL ausente mantiene estado desconocido. No pulses Validar corrección ni Solicitar indexación para exportar.

## B. Relacionar consultas con categorías, sin inventar un join

Prioriza estas dos páginas comerciales, sin cambiar su contenido:

- `https://rhino-performance.com/presoterapia/`
- `https://rhino-performance.com/compresion-frio-y-calor/`

En **Rendimiento → Resultados de búsqueda**:

1. Tipo **Web**, fechas personalizadas **2026-08-11 a2026-11-10** para reproducir el archivo recibido. Si prefieres un periodo más reciente, exporta también su baseline completo y registra las nuevas fechas; no lo llames mejora frente a los90 días anteriores.
2. Añade **Página → URL exacta** para una categoría y exporta **Consultas**, conservando las demás pestañas y filtros. Repite para la segunda. Esto sí permite atribuir las consultas de ese archivo a la categoría filtrada.
3. Para un segmento comercial concreto, conserva la misma página y fechas, filtra **País: México**, **Dispositivo: Móviles**, y exporta Consultas de nuevo. Repite para la segunda. Los datos globales y segmentados deben mantenerse separados, no sumarse como cohortes independientes.
4. El país de venta y el valor de conversión se deben confirmar antes de tratar México como único objetivo comercial; el segmento se propone porque el archivo recibido muestra allí más clics, no porque pruebe ingresos o disponibilidad comercial.

Opcional después: filtra una consulta exacta candidata —por ejemplo, `botas de presoterapia`— y revisa/exporta **Páginas** con fechas y segmentos fijos. Eso permite saber qué URL recibió sus impresiones; no unir las filas de las tablas globales por posición, orden o similitud del nombre.

No hace falta exportar centenares de archivos: primero las listas de A y las dos categorías de B. Al recibirlos, conservaremos fuentes/hashes y conciliación por URL exacta. El informe de rendimiento no da por sí solo conversiones o ingresos; no los inventaremos.
