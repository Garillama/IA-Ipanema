# Cómo leer las fichas

Fecha: 2026-11-08. Las 223 fichas son proyecciones de archivos, schemas, consumidores y referencias; no 223 componentes visuales independientes ni 223 pruebas funcionales aprobadas.

Cada ficha conserva los campos requeridos y enlaza las fuentes transversales. El nombre procede de translations/es_MX.schema.json cuando existe; para partials se usa el identificador del archivo, sin inventar un nombre oficial. Los defaults se mantienen en la matriz única; no se deduce false/0 cuando no se declara default.

Los includes dinámicos se registran como tales. Un hijo permitido por schema no está necesariamente instanciado; una instancia guardada puede estar oculta; un nodo de sección presente no demuestra que todas sus funciones estén activas. Las clases se extraen léxicamente y pueden contener palabras de expresiones Twig: usar el DOM antes de adoptar un selector.

Accesibilidad, SEO y métricas se verifican por ruta/estado, no aislando arbitrariamente un archivo. Las fichas enlazan esos resultados. INP de campo y todas las variantes del editor siguen pendientes. «No disponible» se limita al ámbito de la fuente inspeccionada.

Riesgos comunes: alterar un snippet compartido afecta varios consumidores; cambiar js-*, data-store, slots, atributos del editor, nombres de inputs o payload comercial puede romper funciones/apps. Los cambios core requieren estado de fork válido y compatibilidad; reutilizar un patrón no concede licencia de redistribuir el archivo. Los riesgos particulares se derivan de dependencias/restricciones de cada ficha.

El método recomendado es ajustar la configuración existente, la variante o fuente compartida adecuada al alcance. El ejemplo de búsqueda de cada ficha localiza sus consumidores; no instala un componente nuevo. Para una prueba, elegir rutas reales con los estados pertinentes y usar la [matriz QA](../10-quality/testing-matrix.md).
