# Nativo, personalizado y dependiente de plataforma

Fecha: 2026-11-08. «Nativo encontrado» describe las unidades de este checkout y su relación con la documentación; no certifica que sus bytes sean un release oficial intacto. No se comparó contra un repositorio oficial versionado de Ipanema. [Inventario](component-inventory.md).

| Familia | Evidencia local | Interpretación |
|---|---|---|
| Announcement/header/sticky/navegación | announcement-bar, header, navigation-bar; funciones initAdbar/initStickyHeader | Configuración existente; reutilizar antes de crear barras adicionales |
| Menú y navegación anidada | header-navigation itera categorías, subcategorías y subniveles, con navigation-banner | Se encontró capacidad de navegación de varias columnas/subniveles; probar teclado y disponibilidad del editor antes de prometer un megamenú específico |
| Búsqueda, cuenta y carrito | search-form; templates account; cart-drawer/main-cart | Mezcla de shell configurable y operaciones LS/plataforma |
| Hero/slideshow/banners/video | Secciones, blocks/slide y blocks/banner | Presentación nativa configurable; no implica vídeo alojado o autoplay permitido en todo dispositivo |
| Editorial, grupos, marcas, iconos | rich-text, group, image-with-text, featured-brands, icon-text | La composición existente cubre muchos diseños nuevos sin otro archivo de sección |
| FAQs, testimonios y newsletter | faq/faq-item, testimonials, newsletter/forms | Son contenido y formularios; testimonios no equivalen a reseñas verificadas de productos |
| Código libre | custom y code con salida raw | Punto de extensión real; no valida automáticamente seguridad, rendimiento o SEO de lo insertado |
| Comercio adicional | snippets subscriptions, kit-products y promociones | Ramas dependientes de datos/features; encontradas en source, no activación comprobada |
| Blog | templates blog y blog-post, snippets/blog | Soporte de tema contrastado con siete posts recorridos; revisar contenido y estados editoriales por separado |
| Checkout | checkout.scss.tpl | Branding específico, no implementación completa de checkout |
| Embla/athletes-carousel/Sectionfy | No existen en static local; sí aparecen en Network de password desde 14517784 | Personalizaciones observadas en otra superficie; no agregarlas al catálogo nativo 1.8.0 |

Los [bloques de uso general documentados por Tiendanube](https://ayuda.tiendanube.com/es_MX/diseno-ipanema/que-bloques-puedo-agregar-en-las-secciones-de-mi-tienda-con-el-diseno-ipanema) incluyen botón, imagen, título, descripción, separador, grupo y código. El schema local también etiqueta `label` como general. Esta diferencia exige identificar versión/contexto; no ocultar una unidad encontrada solo porque la guía comercial no la liste.

No se encontró una sección llamada sticky add to cart en los archivos. Sí hay galería sticky y header sticky. No se presenta por eso un CTA sticky nativo como disponible. Tampoco se encontró un sistema arbitrario de bibliotecas exportables del editor.
