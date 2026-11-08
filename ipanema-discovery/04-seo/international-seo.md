# Idiomas, países y monedas

Fecha: 2026-11-08. Se encontraron traducciones de interfaz/schema para en, es, es_AR, es_CL, es_CO, es_MX y pt.default. El layout usa html_lang y existen selectores de idioma/país. Esto no demuestra traducción de catálogo, URLs localizadas ni una estrategia internacional completa.

El head de plataforma puede emitir alternates según configuración; validar los links hreflang y canonical en respuesta de cada mercado. No generar hreflang solo a partir de archivos de traducción. Los destinos necesitan representar versiones equivalentes reales, con idioma/región válidos y referencias consistentes. [Documentación de versiones localizadas](https://developers.google.com/search/docs/specialty/international/localized-versions).

La moneda visible no sustituye idioma ni país de destino; usar la moneda real de Offer y comprobar cómo cambia al seleccionar mercado. No usar el precio convertido por presentación como fuente independiente de datos comerciales. La interfaz que ofrece país no prueba checkout/envío disponible en ese país.

Pendientes específicos: idiomas habilitados de esta tienda, URLs de versiones, contenido traducido, política de canonical entre mercados y efectos del selector. No se alteraron país, moneda ni configuraciones para descubrirlos. Tampoco se presenta una función anunciada como futura como si estuviera activa.
