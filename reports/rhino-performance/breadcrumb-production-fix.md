# Rhino — corrección del breadcrumb de artículos en producción

Estado: **publicado y verificado en 20 artículos; dos URLs pendientes de confirmar**. Solo Codex; autorización explícita del propietario para corregir este campo en la instalación publicada. No se invocaron otros agentes ni se simuló revisión independiente.

## Cambio aplicado

Archivo único: `layouts/layout.tpl`, línea146. La posición2 “Blog” de `structured-data.blog-post-breadcrumbs` emitía `/blog/`; ahora emite `https://rhino-performance.com/blog/`. Se conserva `json_encode | raw`, se aceptan URLs nativas ya absolutas y se evita duplicar la barra final de store.url. No se añadió otro BreadcrumbList ni un campo literal id.

El cambio corresponde a todo artículo que usa este generador compartido, no a una edición manual de cada artículo. No se modificaron las plantillas de producto/categoría, precios, inventario, scripts, diseño o tipografías.

## Destino, respaldo y alcance

- Tienda7400935, instalación14828608, Ipanema Clothing1.8.0, forked y productiva, confirmados por el CLI nativo.
- `.nuvem` fue gestionado únicamente por el CLI; no se leyó ni copió su contenido a evidencias.
- Archivo remoto anterior respaldado y SHA-256 comprobado contra fuente local antes de editar.
- Cambio local mediante transacción `9ab0793c4419483a94a036b732e6300e`, intento1, aceptada tras QA publicado.
- Push único dirigido a14828608; POST de validación y PATCH respondieron200. Sin watch, publish, fork, clone ni pull.
- La diferencia preexistente en `templates/pages/home.json` se excluyó del cuerpo de validación/subida. Sus hashes remotos antes/después y el hash local permanecieron iguales.

El CLI no tiene flag nativo de un solo archivo y su plan incluía Home; se compuso la guardia existente con un filtro de alcance explícito por proceso, probado offline antes de usarlo. Se permitió únicamente el upsert de layout con su hash aprobado, sin borrados; cualquier archivo inesperado se rechaza. El contador informativo del CLI mostró2 actualizaciones planificadas, pero **las dos peticiones reales (validación/subida) solo contenían layout**. La lectura posterior confirmó que la única diferencia que queda es la Home preexistente. No se da por autorizado ni publicado ese cambio de Home.

## QA real posterior

20 de las22 URLs transcritas de las capturas tenían el mismo breadcrumb relativo. Después del push:

- Las20 respondieron200 y emitieron exactamente un BreadcrumbList de artículo, con Blog absoluto.
- Ninguna presentó errores de sintaxis JSON-LD en esas lecturas.
- Los otros dos elementos de la ruta, sus posiciones/nombres y canonical permanecieron iguales a la evidencia previa.
- Cinco controles de plantillas distintas (Home, categoría, PDP, políticas y blog) conservaron canonical y los campos de breadcrumb registrados; JSON-LD sin errores en esos controles.
- Fuente remota descargada después del push: coincide exactamente por SHA-256 con el candidato aprobado.
- 47 comprobaciones acotadas aprobadas. No equivalen a certificación SEO/WCAG ni a métricas de velocidad o verificación de conversiones.

El primer comparador de los controles falló por comparar objetos de distinta proyección: el registro anterior tenía `url_issue` calculado y no incluía `@type`. Se conservó ese fallo del harness y se compararon solo los campos realmente registrados en ambos (name/item/position); se comprobó por separado el tipo ListItem actual. No hubo otra modificación del tema, nuevos requests para rehacer esa comparación ni rollback por ese error de prueba.

## Dos URLs pendientes

- https://rhino-performance.com/blog/posts/que-debes-saber-antes-de-comprar-unas-botas-de-presoterapia-f0d33d668783/
- https://rhino-performance.com/blog/posts/botas-presoterapia-rhino-pro-v3-032780da6369/

En la primera lectura ambas respondieron200 pero no emitieron el componente de breadcrumb de artículo y mostraron un error JSON previo de otra rama. No se afirmó que fueran artículos actualmente disponibles ni se corrigió otra rama fuera del alcance. Una comprobación adicional de una URL devolvió403: se detuvo y no se reintentó. Ambas se excluyeron de la certificación posterior; se necesita confirmar sus URLs/estado actual con el propietario. No se declara que todos los elementos del informe de Search Console estén resueltos.

## Google Search Console

La corrección está verificada en el storefront publicado. No se pulsó Validar corrección, no se solicitó indexación y no se declara que Google haya actualizado su copia. El propietario puede probar la URL publicada y solicitar validación en el informe; Google necesita volver a rastrear/procesar las páginas. Los dos casos pendientes deben revisarse separadamente.

La sesión OAuth iniciada anteriormente no se considera acceso real mientras no se complete el consentimiento y la verificación de propiedad. No se guardan claves de compartición, cookies ni tokens en este informe.

## Evidencia

Directorio local ignorado por Git: `reports/runs/rhino-performance/20261112T042043-breadcrumb-production-fix-287ff54d`.

- `identity.json`: destino publicado confirmado.
- `remote-layout-before.tpl`, `remote-layout-prepush.tpl`, `remote-layout-after.tpl`: respaldo y lecturas reales de fuente, privadas.
- `transport-prepush.json`: scope, hashes, exclusión de Home y respuestas reales200.
- `native-diff-before.json`, `native-diff-prepush.json`, `native-diff-after.json`: comparación nativa antes/después.
- `articles-before.json`, `articles-after.json`, `controls-after.json`: marcado publicado y límites.
- `post-qa-before-harness-correction.json`, `post-qa-corrected.json`, `acceptance.json`: fallos preservados, QA y aceptación.

Hashes SHA-256 de layout: antes `d1214c8137054f5bef67159db317cb146132b7920afbb9a72686f40fc1b8150b`; después `aa0d59caa5947993a057fc13b4517057286a65a28e24029abb22b839cc18ba31`.
