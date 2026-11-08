# Secciones, bloques y plantillas

Fecha: 2026-11-08. Fuente: schemas/JSON del inventario y [documentación de estructura](https://tiendanube.dev/themes/sectionable-themes/folder-structure).

Hay 51 tipos de sección y 54 archivos de bloque. No todos son insertables en cualquier página. `enabled_on.page_templates` restringe, por ejemplo, `main-product` a producto, `category-hero` a categoría y `main-products-grid` a categoría/búsqueda. Header, footer y cart-drawer se reservan a sus layouts. Los `limit`, `deletable`, `hideable`, `locked_blocks`, bloques static y tags constituyen parte del contrato del editor.

`main-product` declara límite 1, no eliminable, no ocultable y dos bloques estáticos: product-media/product-info. `related-products` tiene límite 2. `announcement-bar` y `navigation-bar` tienen límite 3 dentro del layout header. Son ejemplos comprobados; el detalle por unidad está en cada [ficha](../02-native-components/component-specifications.md), sin extrapolar esos límites al resto.

El bloque group acepta hijos con tag general y puede anidarlos. `product-info` además declara description y purchase-info privados con sus propias configuraciones. Una definición de bloque dentro del schema de un padre puede complementar su archivo global: inspeccionar ambas fuentes. Los 708 controles incluyen esas declaraciones.

Los 25 archivos de templates locales contienen 178 instancias, entre secciones y bloques. Los valores guardados de home incluyen múltiples variantes de banners, contenido editorial y otros módulos: no son 51 secciones necesariamente visibles en home. [Auditoría de páginas y orden](../10-quality/page-audit.md).

La plataforma permite [plantillas alternativas para producto, categoría y página](https://ayuda.tiendanube.com/es_MX/diseno-ipanema/como-usar-plantillas-personalizadas-para-productos-categorias-y-paginas-con-el-diseno-ipanema), creadas en editor y asignadas en Admin. El checkout local no contiene plantillas alternativas por nombre; su asignación real no se inspeccionó. No se crearon ni publicaron plantillas para probarlo.

La guía de ayuda limita un bloque Código dentro de una sección personalizada, mientras el schema local de custom declara aceptación de tag general y el bloque code no muestra ese límite en su archivo. La aplicación efectiva de esa restricción podría estar en el editor/backend; **no comprobada**. No agregar varios bloques para forzar una conclusión sin acceso y autorización de edición.
