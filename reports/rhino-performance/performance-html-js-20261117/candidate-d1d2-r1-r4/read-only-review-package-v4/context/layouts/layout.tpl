{#
  Lightweight blog endpoints for static/js/blog-tags.js and blog-listing.js. Not linked
  anywhere, noindex, canonical to the real page:
    - /blog/posts/<handle>/?view=tags answers only the tables of the post body (where
      the tags live) instead of the whole page. The platform does not pass post.content
      to the blog listing nor to the product page, but it does on the post page.
    - /blog/?page=N&view=cards answers only the page sections (the listing grid), without
      header, footer and scripts, to index the whole blog for the tag filter.
#}
{% if template == 'blog-post' and params.view == 'tags' %}
<!DOCTYPE html>
<html lang="{{ html_lang }}">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{{ store.url }}/blog/posts/{{ post.handle }}/">
</head>
<body>
<div class="post-content" data-blog-tags-endpoint="true">{% for tags_table in (post.content | default('') | split('<table')) | slice(1) %}<table{{ tags_table | split('</table>') | first | raw }}</table>{% endfor %}</div>
</body>
</html>
{% elseif template == 'blog' and params.view == 'cards' %}
<!DOCTYPE html>
<html lang="{{ html_lang }}">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{{ store.blog_url }}">
</head>
<body>
{{ page_template_content }}
</body>
</html>
{% elseif template == 'product' and params.view == 'card' %}
{#
  Lightweight product endpoint for the product cards of the blog post body
  (static/js/blog-post.js): /productos/<handle>/?view=card answers only the name,
  cover, price, compare price, discount, installments, shipping label and a short
  description, instead of the whole product page. Not linked anywhere, noindex,
  canonical to the product.
#}
{% set card_shipping_discount = cart.free_shipping.min_price_free_shipping %}
{% set card_above_free_shipping = card_shipping_discount and (product.price >= card_shipping_discount.min_price_raw) %}
{% set card_can_show_config_shipping = card_shipping_discount.combines_with_other_discounts or not product.promotional_price_percentage %}
{% set card_show_shipping = not product.is_non_shippable and (product.free_shipping or (card_above_free_shipping and card_can_show_config_shipping)) %}
{% set card_has_compare = product.display_price and product.compare_at_price and product.compare_at_price > product.price %}
<!DOCTYPE html>
<html lang="{{ html_lang }}">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{{ product.canonical_url }}">
</head>
<body>
<div class="js-blog-product-data" data-blog-product-endpoint="true" data-product-id="{{ product.id }}" data-image="{{ product.featured_image | product_image_url('large') }}" data-image-srcset="{{ product.featured_image | product_image_url('medium') }} 320w, {{ product.featured_image | product_image_url('large') }} 480w, {{ product.featured_image | product_image_url('huge') }} 640w, {{ product.featured_image | product_image_url('original') }} 1024w">
<span data-field="name">{{ product.name | escape }}</span>
{% if product.display_price %}<span data-field="price">{{ product.price | money }}</span>{% endif %}
{% if card_has_compare %}<span data-field="compare">{{ product.compare_at_price | money }}</span><span data-field="discount">{{ product.promotional_price_percentage | round }}</span>{% endif %}
{% if settings.product_installments %}<div data-field="installments">{% include 'snippets/payments/installments.tpl' with { location: 'product_item', short_wording: true } %}</div>{% endif %}
{% if card_show_shipping %}<span data-field="shipping">{% if product.free_shipping or card_shipping_discount.is_free %}{{ 'product.free_shipping' | t }}{% elseif card_shipping_discount.discount_type == 'percentage' %}{{ card_shipping_discount.discount_value | round }}% {{ 'shipping.discount' | t }}{% elseif card_shipping_discount.discount_value_money %}{{ card_shipping_discount.discount_value_money }} {{ 'shipping.discount' | t }}{% endif %}</span>{% endif %}
{# Legacy card text = the product's SEO meta description; falls back to the long description #}
{% set card_description = product.seo_description | default('') | striptags | trim %}
{% if not card_description %}{% set card_description = product.description | default('') | striptags | trim %}{% endif %}
<span data-field="description">{{ card_description | slice(0, 240) | escape }}</span>
</div>
</body>
</html>
{% else %}
<!DOCTYPE html>
<html lang="{{ html_lang }}">
  <head>
    {# Meta tags component #}
    {{ component('head-tags') }}

    {# Google Fonts preconnect & DNS prefetch #}
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link rel="dns-prefetch" href="https://fonts.googleapis.com" />
    <link rel="dns-prefetch" href="https://fonts.gstatic.com" />

    {# CDN and external assets prefetch #}
    <link rel="dns-prefetch" href="https://d26lpennugtm8s.cloudfront.net" />
    <link rel="dns-prefetch" href="https://acdn.mitiendanube.com" />
    <link rel="preconnect" href="https://googrev.abejita.co" />
    <link rel="dns-prefetch" href="https://googrev.abejita.co" />
    <link rel="preconnect" href="https://lh3.googleusercontent.com" />
    <link rel="dns-prefetch" href="https://lh3.googleusercontent.com" />
    
    {# Preload critical assets #}
    <link rel="preload" as="style" href="{{ ([settings.font_headings, settings.font_rest] | merge(additional_fonts)) | google_fonts_url('400,500,700,800') }}" />
    <link rel="preload" href="{{ 'js/libraries-standalone.js' | static_url }}" as="script" />
    <link rel="preload" href="{{ 'css/style-critical.css' | static_url }}" as="style" />
    <link rel="preload" href="{{ 'css/style-utilities.css' | static_url }}" as="style" />

    {# Style Tokens (fonts + CSS custom properties) #}
    <style>
      {% include 'layouts/resources/style-tokens.tpl' %}
    </style>

    {# Critical CSS #}
    {{ 'css/style-critical.css' | static_url | static_inline }}

    {# Utilities CSS #}
    {{ 'css/style-utilities.css' | static_url | static_inline }}

    {% if params.preview or is_preview or is_preset_preview or ('rhino-contact' in page_template_content) or ('rhino-account' in page_template_content) %}
      {{ 'css/style-forms.css' | static_url | static_inline }}
    {% endif %}

    {# Async CSS loading #}
    <link rel="stylesheet" href="{{ 'css/style-async.css' | static_url }}" media="print" onload="this.media='all'">

    {# Custom CSS from settings #}
    {% if settings.css_code %}
      <style id="custom-theme-css">
        {{ settings.css_code | raw }}
      </style>
    {% endif %}

    {% set async_js = true %}

    {# Platform head content #}
    {% platform_head_content %}

    {# Structured data #}
    {% include 'snippets/structured-data/structured-data-organization.tpl' %}
    {% include 'snippets/structured-data/structured-data.tpl' %}
    {# Blog post: the include above already emits BlogPosting on this template (the
       platform defines blog_item there); only its breadcrumbs are added here #}
    {% if template == 'blog-post' %}
      <script type="application/ld+json" data-component="structured-data.blog-post-breadcrumbs">
      {
        "@context": "https://schema.org/",
        "@type": "BreadcrumbList",
        "itemListElement": [
          {
            "@type": "ListItem",
            "position": 1,
            "name": {{ 'breadcrumbs.home' | t | json_encode | raw }},
            "item": {{ store.url | json_encode | raw }}
          },
          {
            "@type": "ListItem",
            "position": 2,
            "name": {{ 'breadcrumbs.blog' | t | json_encode | raw }},
            "item": {{ ((store.blog_url starts with 'http://' or store.blog_url starts with 'https://') ? store.blog_url : ((store.url | trim('/')) ~ store.blog_url)) | json_encode | raw }}
          },
          {
            "@type": "ListItem",
            "position": 3,
            "name": {{ post.title | json_encode | raw }},
            "item": {{ (store.url ~ '/blog/posts/' ~ post.handle) | json_encode | raw }}
          }
        ]
      }
      </script>
    {% endif %}

    {# Microsoft Clarity #}
    {% set clarity_id = settings.clarity_project_id ?? 'z9hv5475vm' %}
    {% if clarity_id and not params.preview %}
      {% include 'snippets/analytics/clarity.tpl' with { clarity_id: clarity_id } %}
    {% endif %}

  </head>

  {% set cart_favicon_url = settings.cart_favicon ? (settings.cart_favicon | resolve_media).sourceUrl : '' %}

  <body
    class="{% if customer %}customer-logged-in{% endif %} template-{{ template | replace('.', '-') | replace('/', '-') }} {% if template == 'password' %}body-password{% endif %}"
    {% if settings.ajax_cart %}data-ajax-cart="true"{% endif %}
    {% if settings.inactive_tab_message %}
      data-inactive-tab-msg1="{{ settings.inactive_tab_message_01 | escape }}"
      data-inactive-tab-msg2="{{ settings.inactive_tab_message_02 | escape }}"
    {% endif %}
    {% if cart_favicon_url %}data-cart-favicon="{{ cart_favicon_url | escape }}"{% endif %}
    data-preview="{{ params.preview ? 'true' : 'false' }}"
  >
    {{ component('nubesdk-slot', { type: "before_main_content" }) }}

    {# SVG icons sprite #}
    {% include 'layouts/resources/icons-sprite.tpl' %}

    {# Back to admin bar #}
    {{ back_to_admin }}

    {# Header layout template - not shown on password page #}
    {% if template != 'password' %}
      <header class="js-header header">
        {% layout_template 'header' %}
      </header>
      {{ component('nubesdk-slot', { type: "after_header" }) }}
    {% endif %}

    {# Add to cart notification - Outside header for proper fixed positioning #}
    {% if settings.ajax_cart and template != 'password' %}
      {% include 'snippets/notification.tpl' with {
        type: 'add_to_cart',
      } %}
    {% endif %}

    {# Main content #}
    <main id="MainContent" class="main-content main-container" role="main">
      {{ page_template_content }}
    </main>

    {# Footer layout template - adapts automatically for password page #}
    {% layout_template 'footer' %}

    {% if template != 'password' %}
      {# Quick shop modal #}
      {% if settings.quick_shop %}
        {% include 'snippets/modals/quick-shop-modal.tpl' %}
      {% endif %}

      {# Cart modal - Ajax cart panel #}
      {% include 'snippets/cart/cart-modal.tpl' %}

      {# WhatsApp chat button #}
      {% include 'snippets/social/whatsapp-chat.tpl' %}

      {# Promotional modal #}
      {% if settings.promotional_popup_enabled %}
        {% include 'snippets/promotional-modal.tpl' %}
      {% endif %}

      {# Free shipping progress data #}
      <span class="js-ship-free-min hidden" data-pricemin="{{ cart.free_shipping.min_price_free_shipping.min_price_raw|default(0) }}"></span>
      <span class="js-free-shipping-config hidden" data-config="{{ cart.free_shipping.allFreeConfigurations }}"></span>
      <span class="js-cart-subtotal hidden" data-priceraw="{{ cart.subtotal }}"></span>
      <span class="js-cart-discount hidden" data-priceraw="{{ cart.promotional_discount_amount }}"></span>
    {% endif %}

    {# JavaScript - Standalone libraries (Swiper, Lazysizes) - blocking to guarantee availability #}
    {{ 'js/libraries-standalone.js' | static_url | script_tag }}

    {% set module_preview = params.preview or is_preview or is_preset_preview %}
    {% set page_has_athletes = module_preview or ('js-athletes-embla' in page_template_content) %}
    {% set page_has_products = module_preview or ('js-product-carousel' in page_template_content) %}
    {% set page_has_blog_carousel = module_preview or ('js-blog-carousel' in page_template_content) %}
    {% set page_has_sectionfy = module_preview or ('data-sectionfy-kind=' in page_template_content) %}
    {% set page_has_sectionfy_video = module_preview or ('data-sectionfy-video-slide' in page_template_content) %}
    {% set page_has_video = module_preview or ('js-video-block' in page_template_content) or ('js-pdp-video' in page_template_content) %}
    {# Also owns the header marquee / native Swiper visibility on simple pages. #}
    <script>
      window.rhinoMediaReady = new Promise(function(resolve) { window.rhinoMediaResolve = resolve; });
    </script>
    <script src="{{ 'js/media-visibility.js' | static_url }}" defer onload="window.rhinoMediaResolve()" onerror="window.rhinoMediaResolve()"></script>

    {# JavaScript - Embla carousel engine and the athletes-carousel init that consumes it.
       Deferred and in this order: the library has to define its globals before the init runs.
       Sections cannot emit their own <script>, so the pair is loaded here for every page. #}
    {% if page_has_athletes or page_has_products or page_has_blog_carousel %}
      <script src="{{ 'js/embla-carousel.js' | static_url }}" defer></script>
    {% endif %}
    {% if page_has_athletes %}
      <script src="{{ 'js/athletes-carousel.js' | static_url }}" defer></script>
    {% endif %}
    {# Blog tags: the parser, cache and pill renderer shared by the blog listing, the
       product page blog carousel, the blog post related posts and the home news section
       (static/js/blog-tags.js). Before all of them. #}
    {% if template == 'home' or template == 'product' or template == 'blog' or template == 'blog-post' %}
      <script src="{{ 'js/blog-tags.js' | static_url }}" defer></script>
    {% endif %}
    {# Product page carousels (alternative / complementary products), also on Embla #}
    {% if template == 'product' %}
      {% if page_has_products %}<script src="{{ 'js/product-carousel.js' | static_url }}" defer></script>{% endif %}
      {# Blog posts carousel (sections/blog-carousel.tpl), also on Embla + Autoplay #}
      {% if page_has_blog_carousel %}<script src="{{ 'js/blog-carousel.js' | static_url }}" defer></script>{% endif %}
      {# Product video section (sections/product-video.tpl): the player on click and the
         YouTube poster fallback, both delegated so the editor can add the section later #}
      {% if page_has_video %}<script src="{{ 'js/product-video.js' | static_url }}" defer></script>{% endif %}
    {% endif %}
    {# Home news section (sections/home-news.tpl): its hero and cards carousels run on the
       same blog carousel engine. It does nothing on a home page without that section. #}
    {% if template == 'home' and page_has_blog_carousel %}
      <script src="{{ 'js/blog-carousel.js' | static_url }}" defer></script>
    {% endif %}
    {# Home featured collection (sections/featured-collection.tpl): its mobile carousel
       runs on the product carousel engine (opt-in autoplay / mobile-only options) and its
       tabs on featured-collection.js, after it. Both do nothing on a home page without
       that section. #}
    {% if template == 'home' %}
      {% if page_has_products %}<script src="{{ 'js/product-carousel.js' | static_url }}" defer></script>{% endif %}
      {% if module_preview or ('js-featured-collection' in page_template_content) %}<script src="{{ 'js/featured-collection.js' | static_url }}" defer></script>{% endif %}
    {% endif %}
    {# Blog listing tag filter and filtered pagination (sections/main-blog.tpl) #}
    {% if template == 'blog' %}
      <script src="{{ 'js/blog-listing.js' | static_url }}" defer></script>
    {% endif %}
    {# Blog post page (sections/main-blog-post.tpl and sections/blog-post-related.tpl):
       product cards from the body links, previous / next navigation and the related
       posts fallback. After blog-tags.js, which it uses. #}
    {% if template == 'blog-post' %}
      <script src="{{ 'js/blog-post.js' | static_url }}" defer></script>
    {% endif %}

    {# JavaScript - Sectionfy: the shared content client and the
       section renderers that register against it. Same reason and same order as
       above: the client has to define `window.Sectionfy` before a section script
       registers. The client only touches the network when the page has a Sectionfy
       mount, and it makes one request no matter how many renderers are loaded. #}
    {% if page_has_sectionfy %}<script src="{{ 'js/sectionfy-client.js' | static_url }}" defer></script>{% endif %}
    {% if page_has_sectionfy_video %}
      <link rel="stylesheet" href="{{ 'css/sectionfy-video-slide.css' | static_url }}">
      <script src="{{ 'js/sectionfy-video-slide.js' | static_url }}" defer></script>
    {% endif %}
    {% if module_preview or ('js-sectionfy-faq-' in page_template_content) %}
      <script src="{{ 'js/sectionfy-faq-section.js' | static_url }}" defer></script>
    {% endif %}
    {% if module_preview or ('js-sectionfy-specs' in page_template_content) %}
      <script src="{{ 'js/sectionfy-specs-section.js' | static_url }}" defer></script>
    {% endif %}
    {% if module_preview or ('js-sectionfy-description-card' in page_template_content) %}
      <script src="{{ 'js/sectionfy-description-card-section.js' | static_url }}" defer></script>
    {% endif %}

    {% if template != 'home' and template != 'product' %}
      {% if page_has_products %}<script src="{{ 'js/product-carousel.js' | static_url }}" defer></script>{% endif %}
      {% if page_has_blog_carousel %}<script src="{{ 'js/blog-carousel.js' | static_url }}" defer></script>{% endif %}
    {% endif %}

    {# JavaScript - Non-critical libraries and theme store: loaded after LS.ready #}
    <script>
      Promise.all([LS.ready, window.rhinoMediaReady]).then(function() {

        {% include "static/js/libraries.js.tpl" %}

        var script = document.createElement('script');
        script.src = '{{ "js/store.js" | static_url }}';
        document.body.appendChild(script);
      });
    </script>

    {% platform_body_content %}
  </body>
</html>
{% endif %}
