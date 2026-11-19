{# Slide Block - Private to slideshow section #}

{% set slide = block.settings %}
{% set sectionfy_video = slide.media_type == 'sectionfy_video' %}
{% set has_link = slide.link %}

{# Images #}
{% set has_mobile_image = slide.use_mobile_image and slide.image_mobile %}
{% set has_responsive_images = slide.image and has_mobile_image %}

{# Alignment #}
{% set horizontal_align = slide.alignment | default('center') %}
{% set vertical_align = slide.alignment_vertical | default('center') %}
{% set horizontal_align_class = horizontal_align == 'start' ? 'left' : (horizontal_align == 'end' ? 'right' : 'center') %}
{% set vertical_align_class = vertical_align %}

{% if vertical_align_class == 'center' and horizontal_align_class == 'center' %}
  {% set content_position_class = 'media-content-center' %}
{% else %}
  {% set content_position_class = 'media-content-' ~ vertical_align_class ~ '-' ~ horizontal_align_class %}
{% endif %}

{# Text color #}
{% set text_color = slide.text_color %}

{# Overlay #}
{% set show_overlay = slide.show_overlay %}
{% set overlay_color = slide.overlay_color | default('#000000') %}
{% set overlay_opacity = show_overlay ? ((slide.overlay_opacity | default(30)) / 100) : 0 %}

{# Spacing #}
{% set slide_gap = slide.gap | default(16) %}
{% set slide_vertical_padding = slide.vertical_padding | default(32) %}
{% set slide_horizontal_padding = slide.horizontal_padding | default(32) %}

{% set has_image = slide.image or has_mobile_image %}
{% set show_placeholder = not has_image %}
{% set content_animation = slide_content_animation | default('none') %}

{% set image_alt = slide.image | media_alt | default('accessibility.slide' | t) %}
{% set image_mobile_alt = slide.image_mobile | media_alt | default('accessibility.slide' | t) %}

<div
  class="swiper-slide media {% if slide_auto_height %}media-auto{% endif %}"
  {{ block | block_attributes }}
  data-store="slide-{{ block.id }}"
  {% if sectionfy_video %}
    data-sectionfy-kind="video_banner" {% if template == 'home' %}data-sectionfy-page="home-page"{% endif %}
    data-sectionfy-video-slide
    data-sectionfy-video-endpoint="{{ section.settings.sectionfy_video_endpoint | default('') | escape }}"
    data-sectionfy-video-key="{{ slide.sectionfy_video_key | default('') | escape }}"
    data-sectionfy-token="{{ settings.sectionfy_token | default('') | escape }}"
    data-sectionfy-video-autoplay="{{ slide.sectionfy_video_autoplay ? 'true' : 'false' }}"
  {% endif %}
  style="{{ slide_height_style | default('') }} {% if show_overlay %}--media-overlay-color: {{ overlay_color }}; --media-overlay-opacity: {{ overlay_opacity }};{% endif %} {% if text_color %}color: {{ text_color }};{% endif %}"
>
  <div class="media-visual">
      {# Desktop image: always lazy when mobile variant exists, otherwise follows priority #}
      {% if slide.image %}
        {% set desktop_lazy = has_responsive_images or not is_priority %}
        {% include 'snippets/image.tpl' with {
          image_src: slide.image,
          image_alt: image_alt,
          image_classes: (has_responsive_images ? 'd-none d-md-block ') ~ (desktop_lazy ? 'fade-in'),
          image_priority_high: not has_responsive_images and is_priority,
          image_lazy_js: desktop_lazy,
          image_swiper_lazy_class: desktop_lazy,
          image_width: slide.image_width,
          image_height: slide.image_height,
          image_aspect_ratio: slide.image_width and slide.image_height,
        } %}
        {% if desktop_lazy %}
          <div class="placeholder placeholder-fade {{ has_responsive_images ? 'd-none d-md-block' }}"></div>
        {% endif %}
      {% elseif show_placeholder %}
        {# Fallback placeholder only when no image is configured at all. Cycles slide-1/2/3.jpg by position. #}
        {% set placeholder_num = ((slide_index | default(0)) % 3) + 1 %}
        {% set desktop_lazy = not is_priority %}
        {% include 'snippets/image.tpl' with {
          image_src: ('images/placeholders/carrousel/slide-' ~ placeholder_num ~ '.webp') | static_url,
          image_alt: 'accessibility.slide' | t,
          image_classes: desktop_lazy ? 'fade-in',
          image_priority_high: is_priority,
          image_lazy_js: desktop_lazy,
          image_swiper_lazy_class: desktop_lazy,
          image_thumbs: false,
          image_width: 1280,
          image_height: 700,
          image_aspect_ratio: true,
        } %}
        {% if desktop_lazy %}
          <div class="placeholder placeholder-fade"></div>
        {% endif %}
      {% endif %}

      {# Mobile image: prioritized for LCP on first slide of first section #}
      {% if has_mobile_image %}
        {% include 'snippets/image.tpl' with {
          image_src: slide.image_mobile,
          image_alt: image_mobile_alt,
          image_classes: (has_responsive_images ? 'd-md-none ') ~ (not is_priority ? 'fade-in'),
          image_priority_high: is_priority,
          image_lazy_js: not is_priority,
          image_swiper_lazy_class: not is_priority,
          image_width: slide.image_mobile_width,
          image_height: slide.image_mobile_height,
          image_aspect_ratio: slide.image_mobile_width and slide.image_mobile_height,
        } %}
        {% if not is_priority %}
          <div class="placeholder placeholder-fade {{ has_responsive_images ? 'd-md-none' }}"></div>
        {% endif %}
      {% endif %}

      {# Overlay #}
      {% if show_overlay %}
        <div class="media-overlay"></div>
      {% endif %}
    </div>

      {# Controls are a slide sibling of the link, outside the visual stacking context. #}
      {% if sectionfy_video %}
        <button type="button" class="sectionfy-video-toggle" data-sectionfy-video-toggle
          data-label-play="Reproducir video" data-label-pause="Pausar video"
          aria-label="Reproducir video" hidden>
          <svg data-sectionfy-video-play width="20" height="20" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M8 5v14l11-7z"/></svg>
          <svg data-sectionfy-video-pause width="20" height="20" viewBox="0 0 24 24" aria-hidden="true" focusable="false" hidden><path fill="currentColor" d="M6 4h4v16H6zm8 0h4v16h-4z"/></svg>
        </button>
      {% endif %}

  {# Slide link #}
  {% if has_link %}
    <a href="{{ slide.link }}" class="media-link" aria-label="{{ 't:names.slide' | t }}"></a>
  {% endif %}

  {# Content #}
  {% if block.blocks | length > 0 %}
    {% set no_image_align = horizontal_align == 'center' ? 'center' : (horizontal_align == 'end' ? 'end' : 'start') %}
    {% set no_image_classes = 'd-flex flex-column align-items-' ~ no_image_align ~ ' text-' ~ horizontal_align_class %}
    <div class="{% if has_image or show_placeholder %}media-content media-content-floating {{ content_position_class }}{% else %}{{ no_image_classes }}{% endif %} {% if has_link %}media-content-linked{% endif %} {% if content_animation != 'none' %}media-content-animate media-content-animate-{{ content_animation }}{% endif %}" style="gap: {{ slide_gap }}px; padding: {{ slide_vertical_padding }}px {{ slide_horizontal_padding }}px;">
      {% for child_block in block.blocks %}
        {% if child_block and child_block.type is defined and child_block.type != 'trust-benefit' %}
          {% include 'blocks/' ~ child_block.type ~ '.tpl' with { block: child_block } %}
        {% endif %}
      {% endfor %}
    </div>
  {% endif %}

  {# Trust Benefits Pill Overlay inside slide (Figma Glassmorphism Style) #}
  {% set slide_trust_blocks = [] %}
  {% if block.blocks | length > 0 %}
    {% for cb in block.blocks %}
      {% if cb.type == 'trust-benefit' %}
        {% set slide_trust_blocks = slide_trust_blocks | merge([cb]) %}
      {% endif %}
    {% endfor %}
  {% endif %}
  {% if slide_trust_blocks | length == 0 and section.blocks is defined %}
    {% for sb in section.blocks %}
      {% if sb.type == 'trust-benefit' %}
        {% set slide_trust_blocks = slide_trust_blocks | merge([sb]) %}
      {% endif %}
    {% endfor %}
  {% endif %}

  {% if (section.settings.show_trust_pill is not defined or section.settings.show_trust_pill) and slide_trust_blocks | length > 0 %}
    {% set use_slide_custom_colors = slide.use_custom_trust_colors %}
    {% set pill_bg = use_slide_custom_colors and slide.trust_pill_bg_color ? slide.trust_pill_bg_color : (section.settings.trust_pill_bg_color | default('#ffffff')) %}
    {% set pill_opacity = (use_slide_custom_colors and slide.trust_pill_bg_opacity is defined ? slide.trust_pill_bg_opacity : (section.settings.trust_pill_bg_opacity | default(15))) / 100 %}
    {% set pill_text = use_slide_custom_colors and slide.trust_pill_text_color ? slide.trust_pill_text_color : (section.settings.trust_pill_text_color | default('#ffffff')) %}
    {% set pill_align = section.settings.trust_pill_alignment | default('center') %}
    {% set pill_valign = section.settings.trust_pill_vertical_alignment | default('bottom') %}

    <div class="slider-trust-pill-wrapper slider-trust-align-{{ pill_align }} slider-trust-valign-{{ pill_valign }}" style="--trust-pill-spacing-top: {{ section.settings.trust_pill_spacing_top | default(25) }}px; --trust-pill-spacing-bottom: {{ section.settings.trust_pill_spacing_bottom | default(25) }}px; --trust-pill-spacing-left: {{ section.settings.trust_pill_spacing_left | default(0) }}px; --trust-pill-spacing-right: {{ section.settings.trust_pill_spacing_right | default(0) }}px; --trust-pill-spacing-left-mobile: {{ section.settings.trust_pill_spacing_left_mobile | default(0) }}px; --trust-pill-spacing-right-mobile: {{ section.settings.trust_pill_spacing_right_mobile | default(0) }}px;">
      <div class="{% if section.settings.trust_pill_width | default('page') == 'full' %}slider-trust-pill-full{% else %}container{% endif %}">
        <div class="slider-trust-pill slider-trust-pill-mobile-rotate" style="--trust-bg-hex: {{ pill_bg }}; --trust-bg-opacity: {{ pill_opacity }}; --trust-text-color: {{ pill_text }}; --trust-pill-scale: {{ (section.settings.trust_pill_scale | default(100)) / 100 }}; --trust-pill-scale-mobile: {{ (section.settings.trust_pill_scale_mobile | default(100)) / 100 }};">
          {% for trust_block in slide_trust_blocks %}
            {% include 'blocks/trust-benefit.tpl' with { block: trust_block, trust_index: loop.index } %}
          {% endfor %}
        </div>
      </div>
    </div>
  {% endif %}
</div>

{% schema %}
{
  "name": "t:names.slide",
  "icon": "pictureIcon",
  "blocks": [
    {
      "tags": [
        "general"
      ]
    },
    {
      "type": "trust-benefit"
    }
  ],
  "settings": [
    {
      "type": "setting",
      "setting_type": "select",
      "id": "media_type",
      "label": "Contenido multimedia",
      "options": [
        {
          "value": "image",
          "label": "Foto de Tiendanube"
        },
        {
          "value": "sectionfy_video",
          "label": "Video de Sectionfy con foto de respaldo"
        }
      ],
      "default": "image"
    },
    {
      "type": "setting",
      "setting_type": "text",
      "id": "sectionfy_video_key",
      "label": "Clave de la sección de video en Sectionfy",
      "info": "Opcional si la consulta devuelve un único banner publicado. Si devuelve varios, indica su clave completa.",
      "visible_if": "{{ block.settings.media_type == 'sectionfy_video' }}"
    },
    {
      "type": "setting",
      "setting_type": "toggle",
      "id": "sectionfy_video_autoplay",
      "label": "Reproducción automática del video en escritorio",
      "default": false,
      "info": "En teléfono requiere pulsar Play. Respeta ahorro de datos y movimiento reducido.",
      "visible_if": "{{ block.settings.media_type == 'sectionfy_video' }}"
    },
    {
      "type": "setting",
      "setting_type": "image_picker",
      "id": "image",
      "label": "t:settings.image"
    },
    {
      "type": "setting",
      "setting_type": "toggle",
      "id": "use_mobile_image",
      "label": "t:settings.use_mobile_image",
      "default": false
    },
    {
      "type": "setting",
      "setting_type": "image_picker",
      "id": "image_mobile",
      "label": "t:settings.image_mobile",
      "visible_if": "{{ block.settings.use_mobile_image }}"
    },
    {
      "type": "setting",
      "setting_type": "url",
      "id": "link",
      "label": "t:settings.link"
    },
    {
      "type": "header",
      "content": "t:names.disposition"
    },
    {
      "type": "setting",
      "setting_type": "alignment",
      "id": "alignment",
      "label": "t:settings.alignment",
      "options": [
        {
          "value": "start",
          "label": "t:options.left"
        },
        {
          "value": "center",
          "label": "t:options.center"
        },
        {
          "value": "end",
          "label": "t:options.right"
        }
      ],
      "default": "center",
      "vertical_options": [
        {
          "value": "top",
          "label": "t:options.top"
        },
        {
          "value": "center",
          "label": "t:options.center"
        },
        {
          "value": "bottom",
          "label": "t:options.bottom"
        }
      ],
      "vertical_default": "center"
    },
    {
      "type": "header",
      "content": "t:names.colors"
    },
    {
      "type": "setting",
      "setting_type": "color",
      "id": "text_color",
      "label": "t:settings.text",
      "default_setting": "text_color"
    },
    {
      "type": "setting",
      "setting_type": "toggle",
      "id": "use_custom_trust_colors",
      "label": "t:settings.use_custom_trust_colors",
      "default": false
    },
    {
      "type": "setting",
      "setting_type": "color",
      "id": "trust_pill_bg_color",
      "label": "t:settings.trust_pill_bg_color",
      "default": "#ffffff",
      "visible_if": "{{ block.settings.use_custom_trust_colors }}"
    },
    {
      "type": "setting",
      "setting_type": "range",
      "id": "trust_pill_bg_opacity",
      "label": "t:settings.trust_pill_bg_opacity",
      "min": 0,
      "max": 100,
      "step": 5,
      "unit": "%",
      "default": 15,
      "visible_if": "{{ block.settings.use_custom_trust_colors }}"
    },
    {
      "type": "setting",
      "setting_type": "color",
      "id": "trust_pill_text_color",
      "label": "t:settings.trust_pill_text_color",
      "default": "#ffffff",
      "visible_if": "{{ block.settings.use_custom_trust_colors }}"
    },
    {
      "type": "header",
      "content": "t:names.design"
    },
    {
      "type": "setting",
      "setting_type": "range",
      "id": "gap",
      "label": "t:settings.gap",
      "min": 0,
      "max": 50,
      "step": 4,
      "unit": "px",
      "default": 16,
      "icon": "vertical_spacing"
    },
    {
      "type": "setting",
      "setting_type": "range",
      "id": "vertical_padding",
      "label": "t:settings.vertical_padding",
      "min": 0,
      "max": 120,
      "step": 4,
      "unit": "px",
      "default": 32,
      "icon": "vertical_padding"
    },
    {
      "type": "setting",
      "setting_type": "range",
      "id": "horizontal_padding",
      "label": "t:settings.horizontal_padding",
      "min": 0,
      "max": 120,
      "step": 4,
      "unit": "px",
      "default": 32,
      "icon": "horizontal_padding"
    },
    {
      "type": "setting",
      "setting_type": "toggle",
      "id": "show_overlay",
      "label": "t:names.transparent_background",
      "default": false,
      "info": "t:settings.add_overlay",
      "header_toggle": true
    },
    {
      "type": "setting",
      "setting_type": "color",
      "id": "overlay_color",
      "label": "t:settings.color",
      "default": "#000000",
      "visible_if": "{{ block.settings.show_overlay }}"
    },
    {
      "type": "setting",
      "setting_type": "range",
      "id": "overlay_opacity",
      "label": "t:settings.overlay_opacity",
      "min": 0,
      "max": 100,
      "step": 5,
      "unit": "%",
      "default": 30,
      "visible_if": "{{ block.settings.show_overlay }}"
    }
  ],
  "presets": [
    {
      "name": "t:names.slide",
      "settings": {
        "gap": 16,
        "vertical_padding": 32,
        "horizontal_padding": 32
      },
      "blocks": [
        {
          "type": "heading",
          "settings": {
            "title": "t:defaults.slide.heading",
            "size": "h1"
          }
        },
        {
          "type": "text",
          "settings": {
            "text": "t:defaults.slide.description"
          }
        },
        {
          "type": "button",
          "settings": {
            "label": "t:defaults.slide.button"
          }
        }
      ]
    }
  ]
}
{% endschema %}
