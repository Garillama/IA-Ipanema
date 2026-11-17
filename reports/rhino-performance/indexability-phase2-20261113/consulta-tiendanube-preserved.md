# Borrador de consulta técnica a Tiendanube — NO ENVIADO

**Asunto:** Canonical de páginas paginadas del blog en Ipanema seccionable

Hola, equipo de Tiendanube:

Estamos revisando el descubrimiento de artículos en la tienda publicada Rhino Performance (https://rhino-performance.com/), tema Ipanema con personalizaciones de código, referencia técnica opcional para soporte: instalación14828608.

Las siguientes URLs reales, enlazadas por la paginación del blog, responden200 y presentan listas de artículos distintas:

| URL | Artículos observados en HTML | Canonical declarado |
|---|---:|---|
|https://rhino-performance.com/blog/?page=2|12|https://rhino-performance.com/blog/|
|https://rhino-performance.com/blog/?page=3|12|https://rhino-performance.com/blog/|
|https://rhino-performance.com/blog/?page=8|2|https://rhino-performance.com/blog/|

Las respuestas son lecturas de producción de12noviembre2026. El contenido y los enlaces de página2 también se conservaron en una prueba sinJavaScript. El layout normal utiliza `component('head-tags')`; los canonicals explícitos del fork corresponden a endpoints auxiliares `view=cards/tags` con noindex, no a estas páginas públicas.

La inspección de las tres URLs exactas en Search Console devuelve «Google no reconoce esta URL», sin canonical elegido porGoogle ni último rastreo. No atribuimos ese estado al canonical ni afirmamos que los artículos no estén indexados: otras inspecciones y Search Analytics sí muestran artículos de la tienda en Google.

Quisiéramos confirmar:

1. ¿Es intencional que las páginas2,3,8 del blog declaren canonical hacia su portada, aun cuando sus listas de artículos son distintas?
2. ¿Existe una configuración o mecanismo **oficialmente soportado** para emitir canonical propio por página paginada, conservando un único tag en HTML inicial?
3. Si no es el comportamiento esperado, ¿pueden revisar su generación desde head-tags e indicar la corrección o incidencia de plataforma?
4. ¿Qué contrato debe seguir `page_info.canonical_url` en este contexto? No queremos alterar identidades JSON-LD basándonos en una suposición.
5. ¿Qué comportamiento recomiendan oficialmente para descubrimiento de artículos antiguos, paginación y canonicals en este tipo de tema?

Referencia de la recomendación general de Google: https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading

Preferimos conservar el componente nativo. No vamos a añadir un segundo canonical, cambiarlo medianteJavaScript ni improvisar una sustitución de head-tags sin confirmar el mecanismo soportado.

Adjunto preparado para revisión del propietario: `blog-support-evidence.json`, una proyección de las lecturas conservadas (HTTP, canonical y destinos de artículos con su fecha), sin cuerpos de scripts, cabeceras ni credenciales. No es una nueva auditoría ni un informe completo del índice. Gracias.

---

Preparado para que el propietario lo revise y envíe por un canal oficial. No se ha contactado a terceros ni modificado la tienda. No se incluyen claves de Search Console, cookies, contraseñas ni enlaces compartidos privados.
