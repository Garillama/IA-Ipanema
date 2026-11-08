# image

**Identificador:** `snippets:image` · **Tipo:** snippets · **Fecha:** 2026-11-08 · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.

**Fuente:** [snippets/image.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/snippets/image.tpl:1>). **Schema:** no disponible; partial sin schema propio.

| Campo | Evidencia / valor |
|---|---|
| Función / nombre | image; unidad image de snippets; seguir consumidores para su papel en la página |
| Consumidores literales | blocks/banner.tpl:L83, blocks/banner.tpl:L100, blocks/banner.tpl:L117, blocks/brand-logo.tpl:L16, blocks/category-item.tpl:L18, blocks/category-item.tpl:L27, blocks/footer-institutional.tpl:L19, blocks/header-logo.tpl:L14, blocks/icon-text-item.tpl:L32, blocks/image-with-text.tpl:L37, blocks/image.tpl:L21, blocks/image.tpl:L35, blocks/image.tpl:L55, blocks/instagram-posts.tpl:L25, blocks/nav-icon-text-item.tpl:L22, blocks/navigation-banner.tpl:L24, blocks/navigation-banner.tpl:L33, blocks/payment-icons.tpl:L17, blocks/slide.tpl:L52, blocks/slide.tpl:L70, blocks/slide.tpl:L89, blocks/testimonial.tpl:L19, blocks/timer.tpl:L35, blocks/video.tpl:L59, sections/category-hero.tpl:L41, sections/category-hero.tpl:L55, sections/hero-divided.tpl:L59, sections/hero-divided.tpl:L74, sections/hero-divided.tpl:L90, sections/hero-divided.tpl:L112, sections/hero-divided.tpl:L124, sections/hero-divided.tpl:L137, sections/hero.tpl:L53, sections/hero.tpl:L67, sections/hero.tpl:L82, sections/main-contact.tpl:L96, sections/newsletter.tpl:L54, sections/newsletter.tpl:L70, sections/newsletter.tpl:L113, sections/video.tpl:L76, sections/video.tpl:L104, snippets/blog/blog-post-content.tpl:L13, snippets/blog/blog-post-item.tpl:L15, snippets/cart/_cart-item.tpl:L19, snippets/cart/_cross-selling.tpl:L28, snippets/footer/footer-legal.tpl:L54, snippets/footer/payment-shipping-logos.tpl:L19, snippets/logo/logo-img.tpl:L10, snippets/modals/quick-shop-modal.tpl:L25, snippets/navigation/country-options.tpl:L8, snippets/notification.tpl:L48, snippets/payments/payments-info-banks.tpl:L22, snippets/payments/payments-info-banks.tpl:L64, snippets/payments/payments-info-banks.tpl:L103, snippets/payments/payments-info-banks.tpl:L132, snippets/payments/payments-info-banks.tpl:L161, snippets/payments/payments-info-methods.tpl:L22, snippets/payments/payments-info-methods.tpl:L119, snippets/payments/payments-info.tpl:L21, snippets/payments/payments-info.tpl:L146, snippets/product/kit-product-variants.tpl:L32, snippets/product/kit-products.tpl:L22, snippets/product/product-image-thumbs.tpl:L7, snippets/product/product-image-thumbs.tpl:L21, snippets/product/product-image.tpl:L58, snippets/product/product-variants.tpl:L63, snippets/product/product-variants.tpl:L74, snippets/product/product-video-item.tpl:L20, snippets/product/product-video-item.tpl:L60, snippets/product/product-video-item.tpl:L71, snippets/product-list/product-item/item-image.tpl:L124, snippets/product-list/product-item/item-image.tpl:L136, snippets/product-list/product-item/item-slider.tpl:L21, snippets/product-list/product-item/item-slider.tpl:L28, snippets/product-list/product-item/item-slider.tpl:L41, snippets/promotional-modal.tpl:L51, snippets/promotional-modal.tpl:L59 |
| Ubicaciones posibles por grafo | templates/layout/cart_drawer.json, templates/layout/footer.json, templates/layout/header.json, templates/pages/404.json, templates/pages/blog-post.json, templates/pages/blog.json, templates/pages/cart.json, templates/pages/category.json, templates/pages/contact.json, templates/pages/home.json, templates/pages/password.json, templates/pages/product.json, templates/pages/search.json |
| Instancias guardadas | no disponible |
| Dependencias | no disponible como literal |
| Restricciones | {} |
| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |
| Configuración/defaults | Sin schema propio; contexto del consumidor |
| Desktop dedicado por ID | no disponible; revisar controles compartidos |
| Mobile dedicado por ID | no disponible |
| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |
| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |
| Variables CSS locales | no disponible en este archivo |
| Hooks JS | no disponible en marcado directo |
| Referencias store.js | no disponible por búsqueda literal; puede residir en LS |
| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |
| Clases candidatas | elseif, endif, if, image-priority-high, image_classes, image_lazy_js, image_priority_high, image_swiper_lazy_class, lazyload, swiper-lazy |
| Atributos data | expand, sizes, src, srcset |
| Semántica directa | picture: 3, img: 4; excluye hijos y plataforma |
| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |
| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |
| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |
| Imágenes | 0 includes literales de image.tpl, más posibles hijos |
| Reutilización | B, C, F, G; [motivos y alcance](../reusable-components.md) |
| Presencia observada en rutas | 0 registros de crawl para este tipo de sección; no atribuible directamente para partial/bloque o no presente |
| Personalización recomendada | Reutilizar include y contexto de datos |
| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |
| Ejemplo de localización | `rg -n --fixed-strings "snippets/image.tpl" templates sections blocks snippets` |
| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |

**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).
