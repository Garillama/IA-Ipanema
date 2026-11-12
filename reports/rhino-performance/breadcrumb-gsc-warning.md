# Aviso de BreadcrumbList en Search Console — verificación pública

Estado: **needs_evidence para determinar la URL afectada y el estado del índice**. Codex únicamente; sin cambios de tema ni producción.

La captura del propietario informa «La URL del campo id no es válida (en itemListElement.item)», con severidad no crítica. El enlace recibido identifica la propiedad de dominio de Rhino, pero no enumera las URLs afectadas dentro del contenido disponible. No se guarda el enlace con su clave de compartición.

Se revisó HTML inicial publicado con el extractor existente, sin cookies, formularios ni cambios remotos:

| Ruta | HTTP | Breadcrumb JSON-LD |
|---|---:|---|
| /presoterapia/ | 200 | Sin URL inválida reproducida en los elementos inspeccionados |
| /productos/botas-presoterapia-inalambricas-pro-air/ | 200 | Sin URL inválida reproducida en los elementos inspeccionados |
| /accesorios/ | 200 | Sin URL inválida reproducida en los elementos inspeccionados |
| /politica-de-devolucion/ | 200 | Sin URL inválida reproducida en los elementos inspeccionados |
| / | 200 | Sin URL inválida reproducida en los elementos inspeccionados |
| /blog/ | 200 | No se emitió BreadcrumbList |
| /search/?q=presoterapia | 200 | Sin URL inválida reproducida en los elementos inspeccionados |

Esto no acredita que Google haya actualizado sus datos ni reproduce todos los estados DOM. En la categoría presoterapia tampoco se detectó BreadcrumbList adicional en microdata/RDFa durante una comprobación puntual. No se declara que todo el sitio esté libre del aviso.

## Procedimiento concreto

1. Recuperar una URL de la tabla Ejemplos del aviso de Search Console, su elemento afectado y fecha de último rastreo.
2. Comparar su JSON-LD/DOM actual con la versión que Google conoce. Un aviso histórico no justifica cambiar una salida actual válida.
3. Si `item` o `item.@id` está mal formado, corregir únicamente el generador nativo: conservar URL absoluta válida y jerarquía real, sin duplicar dominio, sin inventar destinos ni agregar un campo literal `id` para ocultar el aviso.
4. Probar el marcado y pedir autorización para el diff exacto antes de publicar. Si el marcado ya está correcto, contrastar el rastreo y usar Validar corrección cuando corresponda; no publicar un parche innecesario.

La fuente local inspeccionada es `snippets/structured-data/structured-data.tpl`, incluyendo la construcción de breadcrumb en líneas168–214. La concatenación de base y crumb exige comprobar si el valor ya es absoluto, pero no se confirmó que esta rama emita una URL inválida en las páginas revisadas. No se aplicó un parche especulativo.

[Requisitos oficiales de Google para BreadcrumbList](https://developers.google.com/search/docs/appearance/structured-data/breadcrumb). El último elemento puede omitir item; no debe diagnosticarse esa omisión aislada como una URL inválida.

## Acceso de cuenta

El propietario autorizó OAuth oficial de solo lectura. La configuración local de Rhino fue preparada preservando los otros ajustes y con backup privado; el consentimiento de Google se inició sin agentes adicionales. No se afirma conexión completada ni inspección de URL consultada hasta recibir y verificar la autorización.

Evidencia pública: `reports/runs/rhino-performance/20261112T041144-breadcrumb-public-verification-36ba6f24/public-breadcrumbs.json`. Hash de HTML, fecha, canonical y valores de cada crumb se conservan allí. Ningún token o clave de compartición en este informe.

## URL afectada confirmada — artículo indicado por el propietario

En `https://rhino-performance.com/blog/posts/ejercicio-en-la-manana-antes-o-despues-de-desayunar-6b4da8f2797c/`, la línea1147 publicada contiene `"item": "\/blog\/"` en la posición2, nombre Blog, del componente `structured-data.blog-post-breadcrumbs`. El valor decodificado es `/blog/`, relativo. El generador está en `layouts/layout.tpl:146`, no en el snippet general revisado antes.

La propuesta normaliza ese elemento a `https://rhino-performance.com/blog/`, conserva serialización JSON y deja intactos Inicio/artículo/BlogPosting. Se conserva un diff de un único campo con hashes, respaldo de fuente local y JSON esperado. No se aplicó al tema ni a producción; no se afirma render Twig real ni validación externa ejecutada.

Evidencia y candidato: `reports/runs/rhino-performance/20261112T041447-breadcrumb-affected-article-3ec9127f`. La URL exacta permitió reproducir un caso que no estaba en las siete rutas iniciales. No hace falta agregar un segundo BreadcrumbList ni un campo literal `id`.

## Publicación autorizada posterior

El propietario autorizó después el cambio exacto: se aplicó únicamente layout a producción14828608 y se verificaron20 artículos. [Cierre y dos pendientes](breadcrumb-production-fix.md). Las secciones anteriores conservan el estado previo al despliegue.
