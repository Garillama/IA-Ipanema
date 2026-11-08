# SEO técnico de Ipanema

Fecha: 2026-11-08. La fuente del tema y la [guía oficial de SEO seccionable](https://tiendanube.dev/es-AR/themes/sectionable-themes/seo) separan responsabilidades: plataforma para title/description/canonical/tags sociales, y tema para semántica visible, enlaces, imágenes y JSON-LD. No añadir una segunda versión de metadatos al corregir un componente.

`layouts/layout.tpl` contiene html lang, header, main y composición de footer. El nombre de una clase `.h1` no crea un encabezado. `blocks/heading.tpl` emite un div con richtext raw; su comentario de p está desactualizado. El tamaño visual puede cambiar en mobile sin modificar semántica. En home desbloqueada se observó un H1 con el nombre de tienda y ausencia de H2/H3 en la muestra inicial de títulos visuales; la jerarquía editorial necesita una decisión explícita, no aplicar H1 a cada hero.

PDP usa H1 para producto y H2 para producto destacado en home; page-header resuelve encabezados de otras páginas. Verificar con datos reales que no queden vacíos o duplicados al combinar secciones. Usar nav para navegación, listas para conjuntos y enlaces para destinos; button para acciones. Evitar que un overlay link genérico reemplace un nombre de destino comprensible.

| Tipo | Evidencia a revisar | Límite / siguiente decisión |
|---|---|---|
| Inicio | H1, title/descripción, categorías y productos enlazados | Los textos de ejemplo encontrados deben sustituirse por contenido autorizado en una fase posterior |
| Categoría/subcategoría | Título, breadcrumb, descripción, enlaces y páginas siguientes | Configuración de infinite requiere alternativa rastreable |
| Producto | H1, canonical, imagen/alt, precio y Offer coherentes | Variantes y disponibilidad no se deben inventar |
| Búsqueda/filtros | Query, estado vacío, parámetros y metadatos | Política de indexación debe verificarse en respuesta real |
| Institucional/contacto/blog | Contenido visible, encabezados y enlaces | Blog puede no estar habilitado o estar vacío; no atribuir artículos inexistentes |
| Cuenta/carrito/checkout | Privacidad, indexación y redirecciones | No exponer datos de cliente para «mejorar SEO» |
| 404 | Status HTTP y contenido útil | Una interfaz de error con HTTP 200 no equivale a una 404 correcta |

Los resultados ejecutados se vinculan en [auditoría de páginas](../10-quality/page-audit.md) y evidencia de crawl. Las recomendaciones de los siguientes documentos son verificables, pero ninguna promete posición en buscadores. La contraseña de tienda modifica lo que puede ver un robot sin sesión; el acceso concedido al auditor no vuelve pública la tienda.
