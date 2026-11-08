# Matriz completa de controles definidos en código

Verificado 2026-11-08. 708 definiciones, incluidos settings de bloques privados declarados dentro de otros schemas. No equivale a 708 controles visibles simultáneamente. La interfaz real del Admin no fue abierta.

Los ámbitos de dispositivo de esta tabla se infieren del identificador: el consumo real se explica en [responsive](../03-editor/responsive-controls.md). Sin default explícito se indica «no disponible»; no significa cero ni false. Valores guardados por instancia: [JSON de instancias](../13-evidence/measurements/source-baseline/template-instances.json). Esquemas íntegros de opciones: [settings.json](../13-evidence/measurements/source-baseline/settings.json).

<a id="blocks-accordion-tpl"></a>
## blocks/accordion.tpl

[blocks/accordion.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/accordion.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `title` — Título (34) | text | shared | "t:defaults.accordion.title" | no disponible | {} |
| `content` — Contenido (41) | richtext | shared | "t:defaults.accordion.content" | no disponible | {} |
| `open_default` — Abierto por defecto (48) | toggle | shared | false | no disponible | {} |
| `icon` — Ícono (55) | select | shared | "" | , shipping, returns, security, info, question | {} |

<a id="blocks-announcement-tpl"></a>
## blocks/announcement.tpl

[blocks/announcement.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/announcement.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `text` — Texto (37) | inline_richtext | shared | "t:defaults.announcements.announcement_1" | no disponible | {} |
| `link` — Link (44) | url | shared | no disponible | no disponible | {} |

<a id="blocks-banner-tpl"></a>
## blocks/banner.tpl

[blocks/banner.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/banner.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `image` — Imagen (166) | image_picker | shared | no disponible | no disponible | {} |
| `use_mobile_image` — Usar otra imagen para celulares (172) | toggle | mobile | false | no disponible | {} |
| `image_mobile` — Imagen en celular (179) | image_picker | mobile | no disponible | no disponible | {"visible_if": "{{ block.settings.use_mobile_image }}"} |
| `link` — Link (186) | url | shared | no disponible | no disponible | {} |
| `alignment` — Alineación (196) | alignment | shared | "start" | start, center, end | {"vertical_default": "bottom", "vertical_options": [{"value": "top", "label": "t:options.top"}, {"value": "center", "label": "t:options.center"}, {"value": "bottom", "label": "t:options.bottom"}]} |
| `text_outside` — Ubicar el texto fuera de la imagen (215) | checkbox | shared | false | no disponible | {} |
| `text_color` — Color de textos (226) | color | shared | settings.text_color | no disponible | {} |
| `gap` — Separación entre elementos (237) | range | shared | 16 | 0…50; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (249) | range | shared | 32 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (261) | range | shared | 32 | 0…120; paso 4; px | {} |
| `show_overlay` — Fondo transparente (273) | toggle | shared | false | no disponible | {"visible_if": "{{ block.settings.text_outside == false }}", "header_toggle": true, "info": "t:settings.add_overlay"} |
| `overlay_color` — Color (283) | color | shared | "#000000" | no disponible | {"visible_if": "{{ block.settings.show_overlay }}"} |
| `overlay_opacity` — Opacidad (291) | range | shared | 30 | 0…100; paso 5; % | {"visible_if": "{{ block.settings.show_overlay }}"} |

<a id="blocks-blog-posts-list-tpl"></a>
## blocks/blog-posts-list.tpl

[blocks/blog-posts-list.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/blog-posts-list.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `posts_count` — Cantidad de publicaciones (40) | range | shared | 3 | 1…8; paso 1; sin unidad | {} |
| `columns_desktop` — Disposición en computadoras (54) | select | desktop | "3" | 3, 4 | {} |
| `gap` — Separación entre elementos (70) | range | shared | 16 | 0…50; paso 4; px | {} |

<a id="blocks-brand-group-tpl"></a>
## blocks/brand-group.tpl

[blocks/brand-group.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/brand-group.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `logo_size` — Tamaño de los logos (58) | range | shared | 80 | 40…200; paso 4; px | {} |
| `gap` — Separación entre elementos (70) | range | shared | 16 | 0…50; paso 4; px | {} |

<a id="blocks-brand-logo-tpl"></a>
## blocks/brand-logo.tpl

[blocks/brand-logo.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/brand-logo.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `image` — Logo (36) | image_picker | shared | no disponible | no disponible | {} |
| `link` — Link (42) | url | shared | no disponible | no disponible | {} |

<a id="blocks-button-tpl"></a>
## blocks/button.tpl

[blocks/button.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/button.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `label` — Texto del botón (55) | text | shared | "t:defaults.button" | no disponible | {} |
| `link` — Link del botón (62) | url | shared | "#" | no disponible | {} |
| `width` — Ancho (73) | radio | shared | "fit" | fit, fill | {} |
| `variant` — no disponible (88) | radio | shared | "primary" | primary, secondary, tertiary | {} |
| `size` — Tamaño (99) | radio | shared | "big" | small, medium, big | {} |
| `custom_background_color` — Color de fondo (111) | color | shared | settings.button_primary_background_color | no disponible | {"visible_if": "{{ block.settings.variant == 'primary' }}"} |
| `custom_text_color` — Color del texto (119) | color | shared | settings.button_primary_foreground_color | no disponible | {"visible_if": "{{ block.settings.variant == 'primary' }}"} |
| `custom_background_color_secondary` — Color de fondo (127) | color | shared | settings.button_secondary_background_color | no disponible | {"visible_if": "{{ block.settings.variant == 'secondary' }}", "disabled_if": "{{ settings.button_secondary_style == 'underlined' }}"} |
| `custom_text_color_secondary` — Color del texto (136) | color | shared | settings.button_secondary_foreground_color | no disponible | {"visible_if": "{{ block.settings.variant == 'secondary' }}"} |
| `custom_background_color_tertiary` — Color de fondo (144) | color | shared | settings.button_tertiary_background_color | no disponible | {"visible_if": "{{ block.settings.variant == 'tertiary' }}", "disabled_if": "{{ settings.button_tertiary_style == 'underlined' }}"} |
| `custom_text_color_tertiary` — Color del texto (153) | color | shared | settings.button_tertiary_foreground_color | no disponible | {"visible_if": "{{ block.settings.variant == 'tertiary' }}"} |

<a id="blocks-category-item-tpl"></a>
## blocks/category-item.tpl

[blocks/category-item.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/category-item.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `image` — Imagen (57) | image_picker | shared | no disponible | no disponible | {"visible_if": "{{ block.parent.settings.category_type == 'image_thumbnail' }}"} |
| `text` — Texto (64) | richtext | shared | no disponible | no disponible | {} |
| `link` — Link (70) | url | shared | no disponible | no disponible | {} |

<a id="blocks-category-nav-tpl"></a>
## blocks/category-nav.tpl

[blocks/category-nav.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/category-nav.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `category_type` — Tipo (19) | radio | shared | "image_thumbnail" | image_thumbnail, text_pill | {} |
| `format_text` — Formato (30) | radio | shared | "rounded" | rounded, square | {"visible_if": "{{ block.settings.category_type == 'text_pill' }}"} |
| `format_image` — Formato (42) | radio | shared | "square" | circular, square | {"visible_if": "{{ block.settings.category_type == 'image_thumbnail' }}"} |
| `image_position` — Posición de la imagen (59) | radio | shared | "left" | left, top | {"visible_if": "{{ block.settings.category_type == 'image_thumbnail' }}"} |
| `image_size` — Tamaño de imagen (71) | range | shared | 80 | 40…300; paso 4; px | {"visible_if": "{{ block.settings.category_type == 'image_thumbnail' }}"} |
| `gap` — Separación entre elementos (84) | range | shared | 16 | 0…50; paso 4; px | {} |
| `items_text_alignment` — Alineación del texto (96) | text_alignment | shared | "left" | left, center | {"visible_if": "{{ block.settings.category_type == 'image_thumbnail' and block.settings.image_position == 'top' }}"} |
| `background_color` — Color de fondo (112) | color | shared | "transparent" | no disponible | {"visible_if": "{{ block.settings.category_type == 'text_pill' }}"} |
| `text_color` — Color del texto (120) | color | shared | settings.text_color | no disponible | {} |
| `border_color` — Color del borde (127) | color | shared | settings.text_color | no disponible | {"visible_if": "{{ block.settings.category_type == 'text_pill' }}"} |
| `image_border_color` — Borde de la imagen (135) | color | shared | settings.text_color | no disponible | {"visible_if": "{{ block.settings.category_type == 'image_thumbnail' }}"} |

<a id="blocks-code-tpl"></a>
## blocks/code.tpl

[blocks/code.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/code.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `code` — Agrega HTML, CSS o JS (21) | custom_code | shared | no disponible | no disponible | {} |
| `width` — Ancho (31) | radio | shared | "fill" | fit, fill | {} |

<a id="blocks-description-tpl"></a>
## blocks/description.tpl

[blocks/description.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/description.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `show_title` — Mostrar título (36) | toggle | shared | true | no disponible | {} |
| `show_social` — Mostrar redes sociales (43) | toggle | shared | true | no disponible | {} |

<a id="blocks-divider-tpl"></a>
## blocks/divider.tpl

[blocks/divider.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/divider.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `padding` — Espaciado (38) | range | shared | 16 | 0…120; paso 4; px | {} |
| `show_line` — Línea divisoria (50) | toggle | shared | true | no disponible | {"header_toggle": true} |
| `line_color` — Color de línea (58) | color | shared | settings.text_color | no disponible | {"visible_if": "{{ block.settings.show_line }}"} |

<a id="blocks-faq-group-tpl"></a>
## blocks/faq-group.tpl

[blocks/faq-group.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/faq-group.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `gap` — Separación entre elementos (36) | range | shared | 0 | 0…50; paso 4; px | {} |

<a id="blocks-faq-item-tpl"></a>
## blocks/faq-item.tpl

[blocks/faq-item.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/faq-item.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `question` — Pregunta (28) | text | shared | "t:defaults.faq_item.question" | no disponible | {} |
| `answer` — Respuesta (35) | richtext | shared | "t:defaults.faq_item.answer" | no disponible | {} |
| `open_default` — Abierto por defecto (42) | toggle | shared | false | no disponible | {} |

<a id="blocks-faq-list-tpl"></a>
## blocks/faq-list.tpl

[blocks/faq-list.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/faq-list.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `gap` — Separación entre elementos (37) | range | shared | 0 | 0…50; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (49) | range | shared | 32 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (61) | range | shared | 32 | 0…120; paso 4; px | {} |

<a id="blocks-footer-institutional-tpl"></a>
## blocks/footer-institutional.tpl

[blocks/footer-institutional.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/footer-institutional.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `logo` — Logo del pie de página (90) | image_picker | shared | no disponible | no disponible | {} |
| `logo_height` — Altura (96) | range | shared | 30 | 20…140; paso 2; px | {} |
| `description` — Descripción (108) | richtext | shared | no disponible | no disponible | {} |
| `show_social` — Mostrar redes sociales (114) | toggle | shared | true | no disponible | {} |
| `show_contact` — Mostrar contacto (121) | toggle | shared | true | no disponible | {} |

<a id="blocks-footer-menu-tpl"></a>
## blocks/footer-menu.tpl

[blocks/footer-menu.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/footer-menu.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `title` — Título (52) | richtext | shared | no disponible | no disponible | {} |
| `menu` — Menú (58) | menu | shared | no disponible | no disponible | {} |

<a id="blocks-footer-newsletter-tpl"></a>
## blocks/footer-newsletter.tpl

[blocks/footer-newsletter.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/footer-newsletter.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `title` — Título (45) | richtext | shared | no disponible | no disponible | {} |
| `description` — Descripción (51) | richtext | shared | no disponible | no disponible | {} |

<a id="blocks-group-tpl"></a>
## blocks/group.tpl

[blocks/group.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/group.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `direction` — Dirección (85) | radio | shared | "column" | column, row | {} |
| `mobile_direction_enabled` — Dirección diferente para celulares (96) | toggle | mobile | no disponible | no disponible | {} |
| `mobile_direction` — Dirección para celulares (102) | radio | mobile | "column" | column, row | {"visible_if": "{{ block.settings.mobile_direction_enabled }}"} |
| `alignment` — Alineación (114) | alignment | shared | "start" | start, center, end | {"vertical_default": "top", "vertical_options": [{"value": "top", "label": "t:options.top"}, {"value": "center", "label": "t:options.center"}, {"value": "bottom", "label": "t:options.bottom"}]} |
| `width` — Ancho (136) | radio | shared | "fill" | fit, fill | {} |
| `gap` — Separación entre elementos (147) | range | shared | 16 | 0…50; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (159) | range | shared | 0 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (171) | range | shared | 0 | 0…120; paso 4; px | {} |
| `custom_background_color` — Color de fondo (187) | color | shared | "transparent" | no disponible | {} |
| `custom_text_color` — Color del texto (194) | color | shared | settings.text_color | no disponible | {} |

<a id="blocks-header-logo-tpl"></a>
## blocks/header-logo.tpl

[blocks/header-logo.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/header-logo.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `height` — Altura (37) | range | shared | 50 | 20…140; paso 2; px | {} |
| `use_different_mobile_height` — Usar otra altura para celulares (49) | toggle | mobile | true | no disponible | {} |
| `height_mobile` — Altura (56) | range | mobile | 30 | 20…90; paso 2; px | {"visible_if": "{{ block.settings.use_different_mobile_height }}"} |

<a id="blocks-header-navigation-tpl"></a>
## blocks/header-navigation.tpl

[blocks/header-navigation.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/header-navigation.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `nav_type_desktop` — Tipo de navegación en computadoras (183) | radio | desktop | "standard" | standard, hamburger | {"visible_if": "{{ section.settings.nav_position_desktop == 'next_to_logo' }}"} |
| `nav_uppercase` — Navegación en mayúsculas (195) | toggle | shared | true | no disponible | {"visible_if": "{{ block.settings.nav_type_desktop == 'standard' or section.settings.nav_position_desktop == 'below_logo' }}"} |
| `show_categories_link` — Mostrar un link de "Categorías" en computadoras (203) | toggle | shared | false | no disponible | {"visible_if": "{{ block.settings.nav_type_desktop == 'standard' or section.settings.nav_position_desktop == 'below_logo' }}"} |
| `show_mobile_categories` — Barra de categorías en celular (211) | toggle | mobile | true | no disponible | {} |
| `nav_alignment_desktop` — Alineación en computadoras (222) | radio | desktop | "center" | left, center | {"visible_if": "{{ section.settings.nav_position_desktop == 'below_logo' or section.settings.logo_position_desktop == 'left' }}"} |
| `vertical_padding` — Espaciado superior e inferior (238) | range | shared | 16 | 0…40; paso 2; px | {"visible_if": "{{ block.settings.nav_type_desktop == 'standard' or section.settings.nav_position_desktop == 'below_logo' }}"} |
| `items_gap` — Espacio entre links (251) | range | shared | 16 | 0…40; paso 2; px | {"visible_if": "{{ block.settings.nav_type_desktop == 'standard' or section.settings.nav_position_desktop == 'below_logo' }}"} |
| `background_color` — Color de fondo (268) | color | shared | settings.background_color | no disponible | {"visible_if": "{{ section.settings.nav_position_desktop == 'below_logo' }}"} |
| `foreground_color` — Color de textos (276) | color | shared | settings.text_color | no disponible | {"visible_if": "{{ section.settings.nav_position_desktop == 'below_logo' }}"} |
| `nav_divider_color` — Línea divisoria en computadoras (284) | color | shared | settings.background_color | no disponible | {"visible_if": "{{ section.settings.nav_position_desktop == 'below_logo' }}"} |
| `show_featured_link` — Ítem destacado (292) | toggle | shared | false | no disponible | {"visible_if": "{{ block.settings.nav_type_desktop == 'standard' or section.settings.nav_position_desktop == 'below_logo' }}", "header_toggle": true, "info": "t:info.featured_item_info"} |
| `featured_link_item` — Ítem a destacar (302) | menu_item | shared | no disponible | no disponible | {"visible_if": "{{ block.settings.show_featured_link and block.settings.nav_type_desktop == 'standard' or block.settings.show_featured_link and section.settings.nav_position_desktop == 'below_logo' }}"} |
| `featured_link_color` — Color del ítem destacado (309) | color | shared | settings.text_color | no disponible | {"visible_if": "{{ block.settings.show_featured_link and block.settings.nav_type_desktop == 'standard' or block.settings.show_featured_link and section.settings.nav_position_desktop == 'below_logo' }}"} |
| `show_secondary_menu` — Navegación secundaria (317) | toggle | shared | false | no disponible | {"header_toggle": true, "info": "t:info.secondary_navigation_info"} |
| `menu` — Menú a mostrar (330) | menu | shared | no disponible | no disponible | {"visible_if": "{{ block.settings.show_secondary_menu }}"} |

<a id="blocks-header-utilities-tpl"></a>
## blocks/header-utilities.tpl

[blocks/header-utilities.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/header-utilities.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `format` — Formato en computadoras (114) | radio | shared | "icons" | icons_text, icons | {} |
| `search_type` — Tipo de buscador (125) | radio | shared | "icon" | expanded, icon | {} |
| `use_different_mobile_search` — Usar otro tipo para celulares (136) | toggle | mobile | false | no disponible | {} |
| `search_type_mobile` — Tipo de buscador (143) | radio | mobile | "expanded" | expanded, icon | {"visible_if": "{{ block.settings.use_different_mobile_search }}"} |
| `cart_icon` — Ícono de compra (159) | radio | shared | "bag" | bag, cart | {} |
| `icon_size` — Tamaño del ícono (170) | range | shared | 20 | 16…32; paso 2; px | {} |
| `use_different_mobile_size` — Usar otro tamaño para celulares (182) | toggle | mobile | false | no disponible | {} |
| `icon_size_mobile` — Tamaño del ícono (189) | range | mobile | 20 | 16…32; paso 2; px | {"visible_if": "{{ block.settings.use_different_mobile_size }}"} |
| `items_gap` — Separación entre elementos (202) | range | shared | 20 | 0…40; paso 2; px | {} |
| `show_account_mobile` — Mostrar ícono de usuario en celulares (214) | toggle | mobile | false | no disponible | {} |
| `show_languages_header` — Mostrar idioma y monedas en el encabezado (221) | toggle | shared | true | no disponible | {"visible_if": "{{ section.settings.nav_position_desktop == 'below_logo' or block.settings.format == 'icons' }}"} |
| `icon_foreground_color` — Ícono (233) | color | shared | settings.text_color | no disponible | {} |

<a id="blocks-heading-tpl"></a>
## blocks/heading.tpl

[blocks/heading.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/heading.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `title` — Texto (53) | richtext | shared | "t:defaults.heading" | no disponible | {} |
| `width` — Ancho (64) | radio | shared | "fill" | fit, fill | {} |
| `size` — Estilo (79) | heading_select | shared | "h4" | h1, h2, h3, h4, h5, h6, custom | {} |
| `custom_font` — Fuente (95) | font_picker | shared | settings.font_headings | "Albert Sans", sans-serif, "Almarai", sans-serif, "Archivo", sans-serif, "Archivo Black", sans-serif, "Arimo", sans-serif, "Arvo", serif, "Big Shoulders Display", sans-serif, "Bitter", serif, "Braah One", sans-serif, "Bree Serif", serif, "Buenard", serif, "Chakra Petch", sans-serif, "Chivo", sans-serif, "Corben", serif, "DM Sans", sans-serif, "Domine", serif, "Droid Sans", sans-serif, "Droid Serif", serif, "Figtree", sans-serif, "Fraunces", serif, "Fredoka One", sans-serif, "Gabarito", sans-serif, "Gilda Display", serif, "Golos Text", sans-serif, "Handlee", cursive, "IBM Plex Sans", sans-serif, "IBM Plex Serif", serif, "Instrument Sans", sans-serif, "Inter", sans-serif, "Istok Web", sans-serif, "Italiana", serif, "Josefin Sans", sans-serif, "Kanit", sans-serif, "Karla", sans-serif, "Lato", sans-serif, "League Spartan", sans-serif, "Lexend", sans-serif, "Lexend Exa", sans-serif, "Libre Baskerville", serif, "Libre Franklin", sans-serif, "Literata", serif, "Lora", serif, "Manrope", sans-serif, "Marcellus", serif, "Montserrat", sans-serif, "Muli", sans-serif, "Neuton", serif, "Niramit", sans-serif, "Nunito", sans-serif, "Onest", sans-serif, "Oooh Baby", cursive, "Open Sans", sans-serif, "Oswald", sans-serif, "Outfit", sans-serif, "Paytone One", sans-serif, "Piazzolla", serif, "Playfair Display", serif, "Pliant", sans-serif, "Plus Jakarta Sans", sans-serif, "Poppins", sans-serif, "Prata", serif, "PT Sans Narrow", sans-serif, "Public Sans", sans-serif, "Raleway", sans-serif, "Readex Pro", sans-serif, "Red Hat Display", sans-serif, "Roboto", sans-serif, "Roboto Condensed", sans-serif, "Roboto Mono", sans-serif, "Rubik", sans-serif, "Slabo 27px", serif, "Sofia Sans Extra Condensed", sans-serif, "Sora", sans-serif, "Source Sans Pro", sans-serif, "Space Grotesk", sans-serif, "Tenor Sans", sans-serif, "Ubuntu", sans-serif, "Ubuntu Mono", monospace, "Ultra", serif, "Unna", serif, "Work Sans", sans-serif, "Zalando Sans", sans-serif, "Zalando Sans Expanded", sans-serif, "Zen Kaku Gothic New", sans-serif, "Zilla Slab", serif | {"visible_if": "{{ block.settings.size == 'custom' }}"} |
| `custom_font_size` — Tamaño (190) | range | shared | 28 | 12…200; paso 1; px | {"visible_if": "{{ block.settings.size == 'custom' }}"} |
| `mobile_font_size` — Tamaño diferente para celulares (202) | toggle | mobile | no disponible | no disponible | {} |
| `mobile_size` — Tamaño para celulares (208) | heading_select | mobile | "h4" | h1, h2, h3, h4, h5, h6 | {"visible_if": "{{ block.settings.mobile_font_size and block.settings.size != 'custom' }}"} |
| `custom_mobile_font_size` — Tamaño para celulares (224) | range | mobile | 28 | 12…200; paso 1; px | {"visible_if": "{{ block.settings.mobile_font_size and block.settings.size == 'custom' }}"} |

<a id="blocks-icon-text-group-tpl"></a>
## blocks/icon-text-group.tpl

[blocks/icon-text-group.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/icon-text-group.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `show_icon` — Mostrar ícono (73) | toggle | shared | true | no disponible | {} |
| `icon_position` — Posición del ícono (80) | radio | shared | "horizontal" | vertical, horizontal | {"visible_if": "{{ block.settings.show_icon }}"} |
| `alignment` — Alineación (92) | text_alignment | shared | "left" | left, center, right | {} |
| `mobile_format` — Presentación en celulares (104) | radio | mobile | "carousel" | list, carousel | {} |
| `icon_size` — Tamaño del ícono (119) | range | shared | 32 | 16…120; paso 1; px | {"visible_if": "{{ block.settings.show_icon }}"} |
| `title_size` — Estilo del título (132) | heading_select | shared | "h6" | h1, h2, h3, h4, h5, h6, paragraph, paragraph_small, custom | {} |
| `custom_title_font` — Fuente (150) | font_picker | shared | settings.font_headings | "Albert Sans", sans-serif, "Almarai", sans-serif, "Archivo", sans-serif, "Archivo Black", sans-serif, "Arimo", sans-serif, "Arvo", serif, "Big Shoulders Display", sans-serif, "Bitter", serif, "Braah One", sans-serif, "Bree Serif", serif, "Buenard", serif, "Chakra Petch", sans-serif, "Chivo", sans-serif, "Corben", serif, "DM Sans", sans-serif, "Domine", serif, "Droid Sans", sans-serif, "Droid Serif", serif, "Figtree", sans-serif, "Fraunces", serif, "Fredoka One", sans-serif, "Gabarito", sans-serif, "Gilda Display", serif, "Golos Text", sans-serif, "Handlee", cursive, "IBM Plex Sans", sans-serif, "IBM Plex Serif", serif, "Instrument Sans", sans-serif, "Inter", sans-serif, "Istok Web", sans-serif, "Italiana", serif, "Josefin Sans", sans-serif, "Kanit", sans-serif, "Karla", sans-serif, "Lato", sans-serif, "League Spartan", sans-serif, "Lexend", sans-serif, "Lexend Exa", sans-serif, "Libre Baskerville", serif, "Libre Franklin", sans-serif, "Literata", serif, "Lora", serif, "Manrope", sans-serif, "Marcellus", serif, "Montserrat", sans-serif, "Muli", sans-serif, "Neuton", serif, "Niramit", sans-serif, "Nunito", sans-serif, "Onest", sans-serif, "Oooh Baby", cursive, "Open Sans", sans-serif, "Oswald", sans-serif, "Outfit", sans-serif, "Paytone One", sans-serif, "Piazzolla", serif, "Playfair Display", serif, "Pliant", sans-serif, "Plus Jakarta Sans", sans-serif, "Poppins", sans-serif, "Prata", serif, "PT Sans Narrow", sans-serif, "Public Sans", sans-serif, "Raleway", sans-serif, "Readex Pro", sans-serif, "Red Hat Display", sans-serif, "Roboto", sans-serif, "Roboto Condensed", sans-serif, "Roboto Mono", sans-serif, "Rubik", sans-serif, "Slabo 27px", serif, "Sofia Sans Extra Condensed", sans-serif, "Sora", sans-serif, "Source Sans Pro", sans-serif, "Space Grotesk", sans-serif, "Tenor Sans", sans-serif, "Ubuntu", sans-serif, "Ubuntu Mono", monospace, "Ultra", serif, "Unna", serif, "Work Sans", sans-serif, "Zalando Sans", sans-serif, "Zalando Sans Expanded", sans-serif, "Zen Kaku Gothic New", sans-serif, "Zilla Slab", serif | {"visible_if": "{{ block.settings.title_size == 'custom' }}"} |
| `custom_title_size` — Tamaño (245) | range | shared | 18 | 12…120; paso 1; px | {"visible_if": "{{ block.settings.title_size == 'custom' }}"} |
| `custom_title_mobile` — Tamaño diferente para celulares (257) | toggle | mobile | no disponible | no disponible | {"visible_if": "{{ block.settings.title_size == 'custom' }}"} |
| `custom_title_mobile_size` — Tamaño para celulares (264) | range | mobile | 18 | 12…120; paso 1; px | {"visible_if": "{{ block.settings.title_size == 'custom' and block.settings.custom_title_mobile }}"} |
| `description_size` — Tamaño de la descripción (276) | select | shared | "paragraph_small" | paragraph_small, paragraph, paragraph_big | {} |
| `gap` — Separación entre elementos (288) | range | shared | 16 | 0…50; paso 4; px | {} |

<a id="blocks-icon-text-item-tpl"></a>
## blocks/icon-text-item.tpl

[blocks/icon-text-item.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/icon-text-item.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `icon_source` — Tipo de ícono (79) | radio | shared | "design" | design, custom | {} |
| `icon` — Ícono (90) | icon_picker | shared | "shipping" | shipping, card, security, returns, cash, promotions, bag, cart, store, gift, heart, star, phone, email, location, world, calendar, check, whatsapp | {"visible_if": "{{ block.settings.icon_source == 'design' }}"} |
| `custom_image` — Imagen (119) | image_picker | shared | no disponible | no disponible | {"visible_if": "{{ block.settings.icon_source == 'custom' }}"} |
| `title` — Título (126) | richtext | shared | "t:defaults.icon_text.item_1_title" | no disponible | {} |
| `description` — Descripción (133) | richtext | shared | "t:defaults.icon_text.item_1_description" | no disponible | {} |
| `link` — Link (140) | url | shared | no disponible | no disponible | {} |

<a id="blocks-image-with-text-tpl"></a>
## blocks/image-with-text.tpl

[blocks/image-with-text.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/image-with-text.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `gap` — Separación entre elementos (80) | range | shared | 0 | 0…50; paso 4; px | {} |

<a id="blocks-image-tpl"></a>
## blocks/image.tpl

[blocks/image.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/image.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `image` — Imagen (77) | image_picker | shared | no disponible | no disponible | {} |
| `use_mobile_image` — Usar otra imagen para celulares (83) | toggle | mobile | false | no disponible | {} |
| `image_mobile` — Imagen en celular (90) | image_picker | mobile | no disponible | no disponible | {"visible_if": "{{ block.settings.use_mobile_image }}"} |
| `link` — Link (97) | url | shared | no disponible | no disponible | {} |
| `width` — Ancho (107) | radio | shared | "fill" | fit, fill | {} |

<a id="blocks-instagram-posts-tpl"></a>
## blocks/instagram-posts.tpl

[blocks/instagram-posts.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/instagram-posts.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `posts_count` — Cantidad de publicaciones (52) | select | shared | "4" | 4, 6, 8, 10, 12 | {} |
| `columns` — Disposición en computadoras (66) | select | shared | "4" | 2, 3, 4 | {} |
| `columns_mobile` — Disposición en celulares (79) | select | mobile | "2" | 1, 2 | {} |
| `gap` — Separación entre elementos (95) | range | shared | 16 | 0…50; paso 4; px | {} |

<a id="blocks-label-tpl"></a>
## blocks/label.tpl

[blocks/label.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/label.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `text` — Texto de la etiqueta (45) | text | shared | "t:defaults.label" | no disponible | {} |
| `variant` — Estilo (56) | radio | shared | "primary" | primary, secondary | {} |
| `custom_background_color` — Color de fondo (67) | color | shared | settings.label_background_color | no disponible | {"visible_if": "{{ block.settings.variant == 'primary' }}"} |
| `custom_text_color` — Color del texto (75) | color | shared | settings.label_foreground_color | no disponible | {"visible_if": "{{ block.settings.variant == 'primary' }}"} |
| `custom_background_color_secondary` — Color de fondo (83) | color | shared | settings.label_shipping_background_color | no disponible | {"visible_if": "{{ block.settings.variant == 'secondary' }}"} |
| `custom_text_color_secondary` — Color del texto (91) | color | shared | settings.label_shipping_foreground_color | no disponible | {"visible_if": "{{ block.settings.variant == 'secondary' }}"} |

<a id="blocks-menu-tpl"></a>
## blocks/menu.tpl

[blocks/menu.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/menu.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `menu` — Menú (39) | menu | shared | "main-menu" | no disponible | {} |
| `heading` — Título (46) | text | shared | no disponible | no disponible | {} |
| `show_as_accordion` — Mostrar submenús (52) | toggle | shared | false | no disponible | {} |

<a id="blocks-nav-announcements-tpl"></a>
## blocks/nav-announcements.tpl

[blocks/nav-announcements.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/nav-announcements.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `alignment` — Alineación en computadoras (41) | text_alignment | shared | "center" | left, center, right | {} |
| `gap` — Separación entre elementos (57) | range | shared | 16 | 0…120; paso 2; px | {} |

<a id="blocks-nav-contact-tpl"></a>
## blocks/nav-contact.tpl

[blocks/nav-contact.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/nav-contact.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `show_phone` — Mostrar teléfono (60) | toggle | shared | true | no disponible | {} |
| `show_whatsapp` — Mostrar WhatsApp (67) | toggle | shared | true | no disponible | {} |
| `show_email` — Mostrar e-mail (74) | toggle | shared | true | no disponible | {} |
| `alignment` — Alineación en computadoras (85) | text_alignment | shared | "right" | left, center, right | {} |
| `gap` — Separación entre elementos (101) | range | shared | 16 | 0…120; paso 2; px | {} |

<a id="blocks-nav-icon-text-group-tpl"></a>
## blocks/nav-icon-text-group.tpl

[blocks/nav-icon-text-group.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/nav-icon-text-group.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `alignment` — Alineación en computadoras (45) | text_alignment | shared | "center" | left, center, right | {} |
| `gap` — Separación entre elementos (61) | range | shared | 16 | 0…120; paso 2; px | {} |

<a id="blocks-nav-icon-text-item-tpl"></a>
## blocks/nav-icon-text-item.tpl

[blocks/nav-icon-text-item.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/nav-icon-text-item.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `icon_source` — Tipo de ícono (56) | radio | shared | "design" | design, custom | {} |
| `icon` — Ícono (67) | icon_picker | shared | "shipping" | shipping, card, security, returns, cash, promotions, bag, cart, store, gift, heart, star, phone, email, location, world, calendar, check, whatsapp | {"visible_if": "{{ block.settings.icon_source == 'design' }}"} |
| `custom_image` — Imagen (96) | image_picker | shared | no disponible | no disponible | {"visible_if": "{{ block.settings.icon_source == 'custom' }}"} |
| `description` — Descripción (103) | richtext | shared | "t:defaults.icon_text.item_1_description" | no disponible | {} |
| `link` — Link (110) | url | shared | no disponible | no disponible | {} |

<a id="blocks-nav-menu-tpl"></a>
## blocks/nav-menu.tpl

[blocks/nav-menu.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/nav-menu.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `menu` — Menú a mostrar (30) | menu | shared | no disponible | no disponible | {} |
| `alignment` — Alineación en computadoras (40) | text_alignment | shared | "center" | left, center, right | {} |
| `gap` — Separación entre elementos (56) | range | shared | 16 | 0…120; paso 2; px | {} |

<a id="blocks-nav-social-tpl"></a>
## blocks/nav-social.tpl

[blocks/nav-social.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/nav-social.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `alignment` — Alineación en computadoras (41) | text_alignment | shared | "right" | left, center, right | {} |
| `gap` — Separación entre elementos (57) | range | shared | 16 | 0…120; paso 2; px | {} |

<a id="blocks-navigation-banner-tpl"></a>
## blocks/navigation-banner.tpl

[blocks/navigation-banner.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/navigation-banner.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `menu_item` — Ítem de la navegación principal (66) | menu_item | shared | no disponible | no disponible | {} |
| `show_on_mobile` — Mostrar en celulares (72) | toggle | mobile | true | no disponible | {} |
| `image` — no disponible (83) | image_picker | shared | no disponible | no disponible | {} |
| `use_mobile_image` — Usar otra imagen para celulares (88) | toggle | mobile | false | no disponible | {} |
| `image_mobile` — Imagen en celular (95) | image_picker | mobile | no disponible | no disponible | {"visible_if": "{{ block.settings.use_mobile_image }}"} |
| `title` — Título (102) | text | shared | no disponible | no disponible | {} |
| `url` — Link (108) | url | shared | no disponible | no disponible | {} |

<a id="blocks-newsletter-form-tpl"></a>
## blocks/newsletter-form.tpl

[blocks/newsletter-form.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/newsletter-form.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `text_and_lines_color` — Textos y líneas (26) | color | shared | settings.text_color | no disponible | {} |

<a id="blocks-payment-icons-tpl"></a>
## blocks/payment-icons.tpl

[blocks/payment-icons.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/payment-icons.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `title` — Título (37) | text | shared | no disponible | no disponible | {} |

<a id="blocks-product-info-tpl"></a>
## blocks/product-info.tpl

[blocks/product-info.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/product-info.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `gap` — Separación entre elementos (43) | range | shared | 40 | 0…80; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (55) | range | shared | 8 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (67) | range | shared | 0 | 0…120; paso 4; px | {} |
| `show_title` — Mostrar título (89) | toggle | shared | true | no disponible | {} |
| `show_social` — Mostrar redes sociales (96) | toggle | shared | true | no disponible | {} |
| `icon_size` — Tamaño del ícono (147) | range | shared | 24 | 16…120; paso 1; px | {} |
| `title_size` — Tamaño del título (159) | select | shared | "paragraph" | h1, h2, h3, h4, h5, h6, paragraph, paragraph_small | {} |
| `description_size` — Tamaño de la descripción (176) | select | shared | "paragraph_small" | paragraph_small, paragraph, paragraph_big | {} |
| `gap` — Separación entre elementos (188) | range | shared | 24 | 0…50; paso 4; px | {} |
| `text_color` — Color de textos (204) | color | shared | settings.text_color | no disponible | {} |
| `icon_color` — Color del ícono (211) | color | shared | settings.text_color | no disponible | {} |

<a id="blocks-product-media-tpl"></a>
## blocks/product-media.tpl

[blocks/product-media.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/product-media.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `format` — Formato en computadoras (20) | radio | shared | "slider" | grid, slider | {} |
| `columns` — Disposición en computadoras (31) | select | shared | "1" | 1, 2, 1_and_2 | {"visible_if": "{{ block.settings.format == 'grid' }}"} |
| `gap` — Separación entre elementos (45) | range | shared | 16 | 0…80; paso 4; px | {"visible_if": "{{ block.settings.format == 'grid' }}"} |
| `show_thumbnails` — Miniaturas (58) | toggle | shared | true | no disponible | {"header_toggle": true} |
| `thumbnail_position` — Posición en computadoras (66) | radio | shared | "left" | left, bottom | {"visible_if": "{{ block.settings.show_thumbnails and block.settings.format == 'slider' }}"} |

<a id="blocks-product-recommendations-tpl"></a>
## blocks/product-recommendations.tpl

[blocks/product-recommendations.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/product-recommendations.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `columns` — Disposición en computadoras (47) | select | shared | "4" | 3, 4, 5, 6 | {} |
| `columns_mobile` — Disposición en celulares (61) | select | mobile | "2" | 1, 2 | {} |

<a id="blocks-products-tpl"></a>
## blocks/products.tpl

[blocks/products.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/products.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `products_source` — Origen de productos (96) | product_list | shared | {"kind": "collection", "id": "primary"} | no disponible | {} |
| `max_products` — Cantidad de productos (103) | range | shared | 12 | 1…20; paso 1; sin unidad | {} |
| `format` — Formato (117) | radio | shared | "grid" | grid, slider | {} |
| `use_different_mobile_format` — Usar otro formato para celulares (128) | toggle | mobile | false | no disponible | {} |
| `format_mobile` — Formato en celulares (135) | radio | mobile | "slider" | grid, slider | {"visible_if": "{{ block.settings.use_different_mobile_format }}"} |
| `columns` — Disposición en computadoras (147) | select | shared | "4" | 3, 4, 5, 6 | {} |
| `columns_mobile` — Disposición en celulares (161) | select | mobile | "2" | 1, 2 | {} |

<a id="blocks-purchase-info-tpl"></a>
## blocks/purchase-info.tpl

[blocks/purchase-info.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/purchase-info.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `icon_size` — Tamaño del ícono (74) | range | shared | 24 | 16…120; paso 1; px | {} |
| `title_size` — Estilo del título (86) | heading_select | shared | "paragraph" | h1, h2, h3, h4, h5, h6, paragraph, paragraph_small, custom | {} |
| `custom_title_font` — Fuente (104) | font_picker | shared | settings.font_headings | "Albert Sans", sans-serif, "Almarai", sans-serif, "Archivo", sans-serif, "Archivo Black", sans-serif, "Arimo", sans-serif, "Arvo", serif, "Big Shoulders Display", sans-serif, "Bitter", serif, "Braah One", sans-serif, "Bree Serif", serif, "Buenard", serif, "Chakra Petch", sans-serif, "Chivo", sans-serif, "Corben", serif, "DM Sans", sans-serif, "Domine", serif, "Droid Sans", sans-serif, "Droid Serif", serif, "Figtree", sans-serif, "Fraunces", serif, "Fredoka One", sans-serif, "Gabarito", sans-serif, "Gilda Display", serif, "Golos Text", sans-serif, "Handlee", cursive, "IBM Plex Sans", sans-serif, "IBM Plex Serif", serif, "Instrument Sans", sans-serif, "Inter", sans-serif, "Istok Web", sans-serif, "Italiana", serif, "Josefin Sans", sans-serif, "Kanit", sans-serif, "Karla", sans-serif, "Lato", sans-serif, "League Spartan", sans-serif, "Lexend", sans-serif, "Lexend Exa", sans-serif, "Libre Baskerville", serif, "Libre Franklin", sans-serif, "Literata", serif, "Lora", serif, "Manrope", sans-serif, "Marcellus", serif, "Montserrat", sans-serif, "Muli", sans-serif, "Neuton", serif, "Niramit", sans-serif, "Nunito", sans-serif, "Onest", sans-serif, "Oooh Baby", cursive, "Open Sans", sans-serif, "Oswald", sans-serif, "Outfit", sans-serif, "Paytone One", sans-serif, "Piazzolla", serif, "Playfair Display", serif, "Pliant", sans-serif, "Plus Jakarta Sans", sans-serif, "Poppins", sans-serif, "Prata", serif, "PT Sans Narrow", sans-serif, "Public Sans", sans-serif, "Raleway", sans-serif, "Readex Pro", sans-serif, "Red Hat Display", sans-serif, "Roboto", sans-serif, "Roboto Condensed", sans-serif, "Roboto Mono", sans-serif, "Rubik", sans-serif, "Slabo 27px", serif, "Sofia Sans Extra Condensed", sans-serif, "Sora", sans-serif, "Source Sans Pro", sans-serif, "Space Grotesk", sans-serif, "Tenor Sans", sans-serif, "Ubuntu", sans-serif, "Ubuntu Mono", monospace, "Ultra", serif, "Unna", serif, "Work Sans", sans-serif, "Zalando Sans", sans-serif, "Zalando Sans Expanded", sans-serif, "Zen Kaku Gothic New", sans-serif, "Zilla Slab", serif | {"visible_if": "{{ block.settings.title_size == 'custom' }}"} |
| `custom_title_size` — Tamaño (199) | range | shared | 16 | 12…120; paso 1; px | {"visible_if": "{{ block.settings.title_size == 'custom' }}"} |
| `custom_title_mobile` — Tamaño diferente para celulares (211) | toggle | mobile | no disponible | no disponible | {"visible_if": "{{ block.settings.title_size == 'custom' }}"} |
| `custom_title_mobile_size` — Tamaño para celulares (218) | range | mobile | 16 | 12…120; paso 1; px | {"visible_if": "{{ block.settings.title_size == 'custom' and block.settings.custom_title_mobile }}"} |
| `description_size` — Tamaño de la descripción (230) | select | shared | "paragraph_small" | paragraph_small, paragraph, paragraph_big | {} |
| `gap` — Separación entre elementos (242) | range | shared | 24 | 0…50; paso 4; px | {} |
| `text_color` — Color de textos (258) | color | shared | settings.text_color | no disponible | {} |
| `icon_color` — Color del ícono (265) | color | shared | settings.text_color | no disponible | {} |

<a id="blocks-slide-tpl"></a>
## blocks/slide.tpl

[blocks/slide.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/slide.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `image` — Imagen (141) | image_picker | shared | no disponible | no disponible | {} |
| `use_mobile_image` — Usar otra imagen para celulares (147) | toggle | mobile | false | no disponible | {} |
| `image_mobile` — Imagen en celular (154) | image_picker | mobile | no disponible | no disponible | {"visible_if": "{{ block.settings.use_mobile_image }}"} |
| `link` — Link (161) | url | shared | no disponible | no disponible | {} |
| `alignment` — Alineación (171) | alignment | shared | "center" | start, center, end | {"vertical_default": "center", "vertical_options": [{"value": "top", "label": "t:options.top"}, {"value": "center", "label": "t:options.center"}, {"value": "bottom", "label": "t:options.bottom"}]} |
| `text_color` — Color de textos (193) | color | shared | settings.text_color | no disponible | {} |
| `gap` — Separación entre elementos (204) | range | shared | 16 | 0…50; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (216) | range | shared | 32 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (228) | range | shared | 32 | 0…120; paso 4; px | {} |
| `show_overlay` — Fondo transparente (240) | toggle | shared | false | no disponible | {"header_toggle": true, "info": "t:settings.add_overlay"} |
| `overlay_color` — Color (249) | color | shared | "#000000" | no disponible | {"visible_if": "{{ block.settings.show_overlay }}"} |
| `overlay_opacity` — Opacidad (257) | range | shared | 30 | 0…100; paso 5; % | {"visible_if": "{{ block.settings.show_overlay }}"} |

<a id="blocks-testimonial-group-tpl"></a>
## blocks/testimonial-group.tpl

[blocks/testimonial-group.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/testimonial-group.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `alignment` — Alineación (73) | text_alignment | shared | "center" | left, center, right | {} |
| `format` — Formato (85) | radio | shared | "grid" | grid, carousel | {} |
| `columns` — Disposición en computadoras (96) | select | shared | "3" | 2, 3 | {} |
| `gap` — Separación entre elementos (112) | range | shared | 16 | 0…50; paso 4; px | {} |
| `image_style` — Forma de la imagen (128) | radio | shared | "rounded" | square, rounded | {} |
| `avatar_layout` — Posición de la imagen (139) | radio | shared | "top" | top, left | {} |

<a id="blocks-testimonial-tpl"></a>
## blocks/testimonial.tpl

[blocks/testimonial.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/testimonial.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `image` — Imagen (62) | image_picker | shared | no disponible | no disponible | {} |
| `name` — Nombre (68) | text | shared | "t:defaults.testimonial.name" | no disponible | {} |
| `rating` — Calificación (75) | select | shared | "5" | none, 1, 2, 3, 4, 5 | {} |
| `title` — Título del testimonio (90) | richtext | shared | "t:defaults.testimonial.title" | no disponible | {} |
| `content` — Descripción (97) | richtext | shared | "t:defaults.testimonial.content" | no disponible | {} |

<a id="blocks-text-group-tpl"></a>
## blocks/text-group.tpl

[blocks/text-group.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/text-group.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `alignment` — Alineación (68) | alignment | shared | "start" | start, center, end | {"vertical_default": "center", "vertical_options": [{"value": "top", "label": "t:options.top"}, {"value": "center", "label": "t:options.center"}, {"value": "bottom", "label": "t:options.bottom"}]} |
| `gap` — Separación entre elementos (90) | range | shared | 16 | 0…50; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (102) | range | shared | 32 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (114) | range | shared | 32 | 0…120; paso 4; px | {} |
| `custom_background_color` — Color de fondo (130) | color | shared | "transparent" | no disponible | {} |
| `custom_text_color` — Color del texto (137) | color | shared | settings.text_color | no disponible | {} |

<a id="blocks-text-tpl"></a>
## blocks/text.tpl

[blocks/text.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/text.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `text` — Texto (26) | richtext | shared | "t:defaults.text" | no disponible | {} |
| `width` — Ancho (37) | radio | shared | "fill" | fit, fill | {} |
| `size` — Tamaño (52) | radio | shared | "paragraph" | paragraph_small, paragraph, paragraph_big | {} |

<a id="blocks-timer-counter-tpl"></a>
## blocks/timer-counter.tpl

[blocks/timer-counter.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/timer-counter.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `background_color` — Color de fondo (46) | color | shared | "#000000" | no disponible | {} |
| `text_color` — Color de textos (54) | color | shared | "#FFFFFF" | no disponible | {} |

<a id="blocks-timer-products-tpl"></a>
## blocks/timer-products.tpl

[blocks/timer-products.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/timer-products.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `title` — Título (54) | text | shared | "t:defaults.timer_products" | no disponible | {} |
| `products_source` — Origen de productos (61) | product_list | shared | {"kind": "collection", "id": "timer_offers"} | no disponible | {} |

<a id="blocks-timer-tpl"></a>
## blocks/timer.tpl

[blocks/timer.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/timer.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `show_background_image` — Imagen de fondo (75) | toggle | shared | true | no disponible | {"header_toggle": true} |
| `image` — Imagen (83) | image_picker | shared | no disponible | no disponible | {"visible_if": "{{ block.settings.show_background_image }}"} |
| `alignment` — Alineación (94) | alignment | shared | "center" | start, center, end | {"vertical_default": "center", "vertical_options": [{"value": "top", "label": "t:options.top"}, {"value": "center", "label": "t:options.center"}, {"value": "bottom", "label": "t:options.bottom"}]} |
| `gap` — Separación entre elementos (116) | range | shared | 16 | 0…50; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (128) | range | shared | 60 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (140) | range | shared | 32 | 0…120; paso 4; px | {} |
| `background_color` — Color de fondo (156) | color | shared | "#FFFFFF" | no disponible | {} |
| `text_color` — Color de textos (164) | color | shared | "#000000" | no disponible | {} |

<a id="blocks-video-tpl"></a>
## blocks/video.tpl

[blocks/video.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/video.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `video_url` — Link de YouTube o Vimeo (90) | video_url | shared | no disponible | no disponible | {"info": "t:info.video_url"} |
| `show_cover_image` — Imagen de portada (98) | toggle | shared | true | no disponible | {"header_toggle": true, "info": "t:info.video_cover_image"} |
| `cover_image` — Imagen (107) | image_picker | shared | no disponible | no disponible | {"visible_if": "{{ block.settings.show_cover_image }}"} |
| `video_type` — Tipo de reproducción (118) | select | shared | "autoplay" | autoplay, manual | {} |
| `aspect_ratio` — Formato (129) | select | shared | "16by9" | 16by9, 4by3, 1by1 | {} |
| `use_different_mobile_format` — Usar otro formato para celulares (141) | toggle | mobile | false | no disponible | {} |
| `format_mobile` — Formato en celulares (148) | select | mobile | "16by9" | 16by9, 4by3, 1by1, 9by16 | {"visible_if": "{{ block.settings.use_different_mobile_format }}"} |

<a id="blocks-view-all-button-tpl"></a>
## blocks/view-all-button.tpl

[blocks/view-all-button.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/blocks/view-all-button.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `label` — Texto del botón (56) | text | shared | "t:defaults.view_all_button" | no disponible | {} |
| `width` — Ancho (67) | radio | shared | "fit" | fit, fill | {} |
| `variant` — no disponible (82) | radio | shared | "tertiary" | primary, secondary, tertiary | {} |
| `size` — Tamaño (93) | radio | shared | "medium" | small, medium, big | {} |
| `custom_background_color` — Color de fondo (105) | color | shared | settings.button_primary_background_color | no disponible | {"visible_if": "{{ block.settings.variant == 'primary' }}"} |
| `custom_text_color` — Color del texto (113) | color | shared | settings.button_primary_foreground_color | no disponible | {"visible_if": "{{ block.settings.variant == 'primary' }}"} |
| `custom_background_color_secondary` — Color de fondo (121) | color | shared | settings.button_secondary_background_color | no disponible | {"visible_if": "{{ block.settings.variant == 'secondary' }}", "disabled_if": "{{ settings.button_secondary_style == 'underlined' }}"} |
| `custom_text_color_secondary` — Color del texto (130) | color | shared | settings.button_secondary_foreground_color | no disponible | {"visible_if": "{{ block.settings.variant == 'secondary' }}"} |
| `custom_background_color_tertiary` — Color de fondo (138) | color | shared | settings.button_tertiary_background_color | no disponible | {"visible_if": "{{ block.settings.variant == 'tertiary' }}", "disabled_if": "{{ settings.button_tertiary_style == 'underlined' }}"} |
| `custom_text_color_tertiary` — Color del texto (147) | color | shared | settings.button_tertiary_foreground_color | no disponible | {"visible_if": "{{ block.settings.variant == 'tertiary' }}"} |

<a id="config-settings-schema-json"></a>
## config/settings_schema.json

[config/settings_schema.json:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/config/settings_schema.json:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `background_color` — Color de fondo (14) | color | shared | "#FFFFFF" | no disponible | {} |
| `text_color` — Color de textos (21) | color | shared | "#3F3D38" | no disponible | {} |
| `accent_color` — Color de acento (28) | color | shared | no disponible | no disponible | {"info": "t:info.accent_color"} |
| `font_headings` — Fuente (46) | font_picker | shared | "\"Instrument Sans\", sans-serif" | "Albert Sans", sans-serif, "Almarai", sans-serif, "Archivo", sans-serif, "Archivo Black", sans-serif, "Arimo", sans-serif, "Arvo", serif, "Big Shoulders Display", sans-serif, "Bitter", serif, "Braah One", sans-serif, "Bree Serif", serif, "Buenard", serif, "Chakra Petch", sans-serif, "Chivo", sans-serif, "Corben", serif, "DM Sans", sans-serif, "Domine", serif, "Droid Sans", sans-serif, "Droid Serif", serif, "Figtree", sans-serif, "Fraunces", serif, "Fredoka One", sans-serif, "Gabarito", sans-serif, "Gilda Display", serif, "Golos Text", sans-serif, "Handlee", cursive, "IBM Plex Sans", sans-serif, "IBM Plex Serif", serif, "Instrument Sans", sans-serif, "Inter", sans-serif, "Istok Web", sans-serif, "Italiana", serif, "Josefin Sans", sans-serif, "Kanit", sans-serif, "Karla", sans-serif, "Lato", sans-serif, "League Spartan", sans-serif, "Lexend", sans-serif, "Lexend Exa", sans-serif, "Libre Baskerville", serif, "Libre Franklin", sans-serif, "Literata", serif, "Lora", serif, "Manrope", sans-serif, "Marcellus", serif, "Montserrat", sans-serif, "Muli", sans-serif, "Neuton", serif, "Niramit", sans-serif, "Nunito", sans-serif, "Onest", sans-serif, "Oooh Baby", cursive, "Open Sans", sans-serif, "Oswald", sans-serif, "Outfit", sans-serif, "Paytone One", sans-serif, "Piazzolla", serif, "Playfair Display", serif, "Pliant", sans-serif, "Plus Jakarta Sans", sans-serif, "Poppins", sans-serif, "Prata", serif, "PT Sans Narrow", sans-serif, "Public Sans", sans-serif, "Raleway", sans-serif, "Readex Pro", sans-serif, "Red Hat Display", sans-serif, "Roboto", sans-serif, "Roboto Condensed", sans-serif, "Roboto Mono", sans-serif, "Rubik", sans-serif, "Slabo 27px", serif, "Sofia Sans Extra Condensed", sans-serif, "Sora", sans-serif, "Source Sans Pro", sans-serif, "Space Grotesk", sans-serif, "Tenor Sans", sans-serif, "Ubuntu", sans-serif, "Ubuntu Mono", monospace, "Ultra", serif, "Unna", serif, "Work Sans", sans-serif, "Zalando Sans", sans-serif, "Zalando Sans Expanded", sans-serif, "Zen Kaku Gothic New", sans-serif, "Zilla Slab", serif | {} |
| `headings_size` — Tamaño (140) | range | shared | 48 | 32…100; paso 2; px | {} |
| `headings_bold` — Negrita (151) | toggle | shared | false | no disponible | {"info": "t:info.headings_bold"} |
| `font_rest` — Fuente (163) | font_picker | shared | "\"Instrument Sans\", sans-serif" | "Albert Sans", sans-serif, "Almarai", sans-serif, "Archivo", sans-serif, "Archivo Black", sans-serif, "Arimo", sans-serif, "Arvo", serif, "Big Shoulders Display", sans-serif, "Bitter", serif, "Braah One", sans-serif, "Bree Serif", serif, "Buenard", serif, "Chakra Petch", sans-serif, "Chivo", sans-serif, "Corben", serif, "DM Sans", sans-serif, "Domine", serif, "Droid Sans", sans-serif, "Droid Serif", serif, "Figtree", sans-serif, "Fraunces", serif, "Fredoka One", sans-serif, "Gabarito", sans-serif, "Gilda Display", serif, "Golos Text", sans-serif, "Handlee", cursive, "IBM Plex Sans", sans-serif, "IBM Plex Serif", serif, "Instrument Sans", sans-serif, "Inter", sans-serif, "Istok Web", sans-serif, "Italiana", serif, "Josefin Sans", sans-serif, "Kanit", sans-serif, "Karla", sans-serif, "Lato", sans-serif, "League Spartan", sans-serif, "Lexend", sans-serif, "Lexend Exa", sans-serif, "Libre Baskerville", serif, "Libre Franklin", sans-serif, "Literata", serif, "Lora", serif, "Manrope", sans-serif, "Marcellus", serif, "Montserrat", sans-serif, "Muli", sans-serif, "Neuton", serif, "Niramit", sans-serif, "Nunito", sans-serif, "Onest", sans-serif, "Oooh Baby", cursive, "Open Sans", sans-serif, "Oswald", sans-serif, "Outfit", sans-serif, "Paytone One", sans-serif, "Piazzolla", serif, "Playfair Display", serif, "Pliant", sans-serif, "Plus Jakarta Sans", sans-serif, "Poppins", sans-serif, "Prata", serif, "PT Sans Narrow", sans-serif, "Public Sans", sans-serif, "Raleway", sans-serif, "Readex Pro", sans-serif, "Red Hat Display", sans-serif, "Roboto", sans-serif, "Roboto Condensed", sans-serif, "Roboto Mono", sans-serif, "Rubik", sans-serif, "Slabo 27px", serif, "Sofia Sans Extra Condensed", sans-serif, "Sora", sans-serif, "Source Sans Pro", sans-serif, "Space Grotesk", sans-serif, "Tenor Sans", sans-serif, "Ubuntu", sans-serif, "Ubuntu Mono", monospace, "Ultra", serif, "Unna", serif, "Work Sans", sans-serif, "Zalando Sans", sans-serif, "Zalando Sans Expanded", sans-serif, "Zen Kaku Gothic New", sans-serif, "Zilla Slab", serif | {} |
| `font_rest_size` — Tamaño (257) | range | shared | 12 | 12…14; paso 1; px | {} |
| `font_base_size` — Tamaño (276) | range | shared | 16 | 12…16; paso 1; px | {} |
| `primary` — no disponible (302) | button_preview | shared | no disponible | no disponible | {} |
| `button_primary_background_color` — Color de fondo (307) | color | shared | "#000000" | no disponible | {} |
| `button_primary_foreground_color` — Color de textos (314) | color | shared | "#FFFFFF" | no disponible | {} |
| `button_primary_style` — Estilo (324) | radio | shared | "filled" | filled, outline | {} |
| `button_primary_border_radius` — Redondeado (335) | range | shared | 8 | 0…40; paso 1; px | {} |
| `secondary` — no disponible (351) | button_preview | shared | no disponible | no disponible | {} |
| `button_secondary_background_color` — Color de fondo (356) | color | shared | "#FFFFFF" | no disponible | {"disabled_if": "{{ settings.button_secondary_style == 'underlined' }}"} |
| `button_secondary_foreground_color` — Color de textos (364) | color | shared | "#000000" | no disponible | {} |
| `button_secondary_style` — Estilo (374) | radio | shared | "outline" | filled, outline, underlined | {} |
| `button_secondary_border_radius` — Redondeado (386) | range | shared | 8 | 0…40; paso 1; px | {"disabled_if": "{{ settings.button_secondary_style == 'underlined' }}"} |
| `tertiary` — no disponible (403) | button_preview | shared | no disponible | no disponible | {} |
| `button_tertiary_background_color` — Color de fondo (408) | color | shared | "transparent" | no disponible | {"disabled_if": "{{ settings.button_tertiary_style == 'underlined' }}"} |
| `button_tertiary_foreground_color` — Color de textos (416) | color | shared | "#000000" | no disponible | {} |
| `button_tertiary_style` — Estilo (426) | radio | shared | "underlined" | filled, outline, underlined | {} |
| `button_tertiary_border_radius` — Redondeado (438) | range | shared | 8 | 0…40; paso 1; px | {"disabled_if": "{{ settings.button_tertiary_style == 'underlined' }}"} |
| `primary_label` — no disponible (466) | label_preview | shared | no disponible | no disponible | {} |
| `label_background_color` — Color de fondo (471) | color | shared | "#000000" | no disponible | {} |
| `label_foreground_color` — Color de textos (478) | color | shared | "#FFFFFF" | no disponible | {} |
| `label_style` — Estilo (488) | radio | shared | "filled" | filled, outline | {} |
| `label_border_radius` — Redondeado (499) | range | shared | 4 | 0…20; paso 1; px | {} |
| `shipping_label` — no disponible (519) | label_preview | shared | no disponible | no disponible | {} |
| `label_shipping_background_color` — Color de fondo (524) | color | shared | "#FFFFFF" | no disponible | {} |
| `label_shipping_foreground_color` — Color de textos (531) | color | shared | "#000000" | no disponible | {} |
| `label_shipping_style` — Estilo (541) | radio | shared | "filled" | filled, outline | {} |
| `label_shipping_border_radius` — Redondeado (552) | range | shared | 4 | 0…20; paso 1; px | {} |
| `page_width` — Ancho en computadoras (575) | range | shared | 1300 | 960…1600; paso 20; px | {} |
| `cart_favicon` — Favicon (597) | image_picker | shared | no disponible | no disponible | {"info": "t:info.cart_favicon"} |
| `inactive_tab_message` — Mostrar mensaje al cambiar de pestaña (608) | toggle | shared | true | no disponible | {} |
| `inactive_tab_message_01` — Mensaje 1 (615) | text | shared | "t:defaults.inactive_tab_message_01" | no disponible | {"visible_if": "{{ settings.inactive_tab_message }}"} |
| `inactive_tab_message_02` — Mensaje 2 (623) | text | shared | "t:defaults.inactive_tab_message_02" | no disponible | {"visible_if": "{{ settings.inactive_tab_message }}"} |
| `promotional_popup_enabled` — Mostrar un pop-up promocional (642) | toggle | shared | false | no disponible | {} |
| `promotional_popup_newsletter` — Mostrar un formulario de newsletter dentro del pop up (649) | toggle | shared | true | no disponible | {"visible_if": "{{ settings.promotional_popup_enabled }}"} |
| `promotional_popup_image` — no disponible (662) | image_picker | shared | no disponible | no disponible | {"visible_if": "{{ settings.promotional_popup_enabled }}"} |
| `promotional_popup_use_mobile_image` — Usar otra imagen para celulares (668) | toggle | mobile | false | no disponible | {"visible_if": "{{ settings.promotional_popup_enabled }}"} |
| `promotional_popup_image_mobile` — Imagen en celular (676) | image_picker | mobile | no disponible | no disponible | {"visible_if": "{{ settings.promotional_popup_enabled and settings.promotional_popup_use_mobile_image }}"} |
| `promotional_popup_url` — Link (683) | url | shared | no disponible | no disponible | {"visible_if": "{{ settings.promotional_popup_enabled }}"} |
| `promotional_popup_title` — no disponible (695) | inline_richtext | shared | "t:defaults.newsletter.heading" | no disponible | {"visible_if": "{{ settings.promotional_popup_enabled }}"} |
| `promotional_popup_title_style` — Estilo del título (702) | heading_select | shared | "h4" | h1, h2, h3, h4, h5, h6 | {"visible_if": "{{ settings.promotional_popup_enabled }}"} |
| `promotional_popup_title_mobile_style` — Tamaño para celulares (718) | toggle | mobile | false | no disponible | {"visible_if": "{{ settings.promotional_popup_enabled }}"} |
| `promotional_popup_title_style_mobile` — Tamaño para celulares (726) | heading_select | mobile | "h3" | h1, h2, h3, h4, h5, h6 | {"visible_if": "{{ settings.promotional_popup_enabled and settings.promotional_popup_title_mobile_style }}"} |
| `promotional_popup_description` — no disponible (747) | richtext | shared | "t:defaults.newsletter.description" | no disponible | {"visible_if": "{{ settings.promotional_popup_enabled }}"} |
| `promotional_popup_description_style` — Estilo (754) | select | shared | "paragraph" | paragraph_small, paragraph, paragraph_big | {"visible_if": "{{ settings.promotional_popup_enabled }}"} |
| `promotional_popup_button_text` — Texto del botón (772) | text | shared | "t:defaults.newsletter.button" | no disponible | {"visible_if": "{{ settings.promotional_popup_enabled }}"} |
| `promotional_popup_button_link` — Link del botón (780) | url | shared | no disponible | no disponible | {"visible_if": "{{ settings.promotional_popup_enabled and not settings.promotional_popup_newsletter }}"} |
| `promotional_popup_image_position` — Posición de la imagen (792) | radio | shared | "left" | left, right | {"visible_if": "{{ settings.promotional_popup_enabled }}"} |
| `promotional_popup_alignment` — Alineación (804) | text_alignment | shared | "left" | left, center, right | {"visible_if": "{{ settings.promotional_popup_enabled }}"} |
| `promotion_labels_position` — Posición de las etiquetas promocionales (828) | radio | shared | "below" | below, over | {} |
| `labels_on_image_position` — Ubicación de las etiquetas (839) | radio | shared | "top" | top, bottom | {"visible_if": "{{ settings.promotion_labels_position == 'over' }}"} |
| `product_installments` — Mostrar información de meses sin intereses (851) | toggle | shared | true | no disponible | {} |
| `quick_shop` — Permitir compra rápida (858) | toggle | shared | true | no disponible | {} |
| `product_color_variants` — Mostrar variantes de color (865) | toggle | shared | true | no disponible | {} |
| `product_aspect_ratio` — Formato de la foto (876) | select | shared | "original" | original, square, horizontal, vertical | {} |
| `product_hover` — Mostrar la segunda foto al pasar el mouse (890) | toggle | shared | true | no disponible | {} |
| `product_item_slider` — Mostrar las fotos en un carrusel para cada producto (897) | toggle | shared | false | no disponible | {"info": "t:info.product_slider"} |
| `last_product_category` — Advertencia de últimas unidades (909) | toggle | shared | true | no disponible | {} |
| `variant_format` — Formato (927) | radio | shared | "buttons" | dropdown, buttons | {} |
| `image_color_variants` — Mostrar la foto de variante de color como botón (938) | toggle | shared | false | no disponible | {} |
| `size_guide_url` — Guía de tallas (945) | url | shared | no disponible | no disponible | {"info": "t:info.size_guide"} |
| `compare_price_saved_money` — Mostrar monto ahorrado en productos con precio promocional (956) | toggle | shared | true | no disponible | {"info": "t:info.show_savings"} |
| `payment_discount_price` — Mostrar el precio descuento por medio de pago (964) | toggle | shared | true | no disponible | {} |
| `product_detail_installments` — Mostrar información de meses sin intereses (971) | toggle | shared | true | no disponible | {} |
| `products_sold` — Mostrar cantidad de productos vendidos (982) | toggle | shared | true | no disponible | {} |
| `quantity_products_sold` — A partir de (989) | number | shared | 10 | no disponible | {"visible_if": "{{ settings.products_sold }}"} |
| `product_sku` — Mostrar código SKU (997) | toggle | shared | false | no disponible | {} |
| `product_stock` — Mostrar stock disponible (1008) | toggle | shared | false | no disponible | {} |
| `last_product` — Mostrar mensaje de últimas unidades en stock (1015) | toggle | shared | true | no disponible | {} |
| `latest_products_available` — Cuando queden menos de (1022) | number | shared | 5 | no disponible | {"visible_if": "{{ settings.last_product }}"} |
| `stock_foreground_color` — Color de texto del mensaje de stock (1030) | color | shared | no disponible | no disponible | {"visible_if": "{{ settings.last_product }}"} |
| `last_product_text` — Mensaje de últimas unidades (1037) | text | shared | "t:defaults.last_product_text" | no disponible | {"visible_if": "{{ settings.last_product }}"} |
| `shipping_calculator_product_page` — Mostrar calculador de envío (1049) | toggle | shared | true | no disponible | {} |
| `cart_minimum_value` — Monto mínimo de compra (1063) | number | shared | no disponible | no disponible | {"info": "t:info.cart_minimum_value"} |
| `ajax_cart` — Permitir que tus clientes agreguen productos al carrito sin necesidad de ir a otra página (1074) | toggle | shared | true | no disponible | {} |
| `cart_open_type` — Acción al agregar un producto al carrito (1081) | radio | shared | "show_notification" | show_notification, show_cart | {"visible_if": "{{ settings.ajax_cart }}"} |
| `add_to_cart_recommendations` — Mostrar productos recomendados al agregar un producto al carrito (1093) | toggle | shared | true | no disponible | {"visible_if": "{{ settings.ajax_cart }}"} |
| `cart_coupon` — Permitir que tus clientes apliquen un cupón de descuento en el carrito (1105) | toggle | shared | false | no disponible | {} |
| `shipping_calculator_cart_page` — Mostrar calculador de envío (1116) | toggle | shared | true | no disponible | {} |
| `checkout_main_background` — Color de fondo (1134) | color | shared | settings.background_color | no disponible | {} |
| `checkout_main_foreground` — Color del texto (1141) | color | shared | settings.text_color | no disponible | {} |
| `checkout_accent_color` — Color de acento (1148) | color | shared | settings.accent_color | no disponible | {} |
| `checkout_button_background` — Color de fondo (1159) | color | shared | settings.button_primary_background_color | no disponible | {} |
| `checkout_button_foreground` — Color del texto (1166) | color | shared | settings.button_primary_foreground_color | no disponible | {} |
| `checkout_header_background` — Color de fondo (1183) | color | shared | settings.background_color | no disponible | {} |
| `checkout_header_foreground` — Color del texto (1190) | color | shared | settings.text_color | no disponible | {} |
| `css_code` — Código CSS personalizado (1208) | custom_css | shared | no disponible | no disponible | {"info": "t:info.css_code"} |

<a id="sections-announcement-bar-tpl"></a>
## sections/announcement-bar.tpl

[sections/announcement-bar.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/announcement-bar.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `background_color` — Color de fondo (111) | color | shared | "#000000" | no disponible | {} |
| `text_color` — Color de textos (118) | color | shared | "#ffffff" | no disponible | {} |
| `animation` — Modo de visualización (129) | select | shared | "slider" | none, slider, marquee | {} |
| `animation_speed` — Velocidad de animación (141) | range | shared | 5 | 1…10; paso 1; sin unidad | {"visible_if": "{{ section.settings.animation == 'marquee' }}"} |
| `slider_speed` — Velocidad (152) | range | shared | 5 | 1…10; paso 1; s | {"visible_if": "{{ section.settings.animation == 'slider' }}"} |
| `section_width` — Ancho (169) | radio | shared | "full" | page, full | {"visible_if": "{{ section.settings.animation != 'marquee' }}"} |
| `vertical_padding` — Espaciado superior e inferior (181) | range | shared | 8 | 0…24; paso 2; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (193) | range | shared | 32 | 0…120; paso 4; px | {"visible_if": "{{ section.settings.animation != 'marquee' }}", "disabled_if": "{{ section.settings.section_width == 'page' }}"} |
| `use_different_mobile_spacing` — Espaciado diferente para celulares (207) | toggle | mobile | false | no disponible | {} |
| `mobile_vertical_padding` — Espaciado superior e inferior en celulares (214) | range | mobile | 16 | 0…24; paso 2; px | {"visible_if": "{{ section.settings.use_different_mobile_spacing }}"} |
| `mobile_horizontal_padding` — Espaciado izquierdo y derecho en celulares (227) | range | mobile | 20 | 0…120; paso 4; px | {"visible_if": "{{ section.settings.use_different_mobile_spacing and section.settings.animation != 'marquee' }}", "disabled_if": "{{ section.settings.section_width == 'page' }}"} |

<a id="sections-banners-tpl"></a>
## sections/banners.tpl

[sections/banners.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/banners.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `format` — Formato (120) | radio | shared | "grid" | grid, slider | {} |
| `use_different_mobile_format` — Usar otro formato para celulares (131) | toggle | mobile | false | no disponible | {} |
| `format_mobile` — Formato en celulares (138) | radio | mobile | "slider" | grid, slider | {"visible_if": "{{ section.settings.use_different_mobile_format }}"} |
| `columns` — Disposición en computadoras (150) | select | shared | "3" | 1, 2, 3, 4 | {} |
| `columns_mobile` — Disposición en celulares (164) | select | mobile | "1" | 1, 2 | {} |
| `section_width` — Ancho (180) | radio | shared | "page" | page, full | {} |
| `banner_aspect_ratio` — Formato de la imagen (191) | select | shared | "original" | original, square, horizontal, vertical, custom | {} |
| `banner_aspect_ratio_height` — Alto de la imagen (206) | range | shared | 100 | 5…200; paso 5; % | {"visible_if": "{{ section.settings.banner_aspect_ratio == 'custom' }}"} |
| `use_different_mobile_aspect_ratio` — Usar otro formato para celulares (219) | toggle | mobile | false | no disponible | {} |
| `banner_aspect_ratio_mobile` — Formato de la imagen en celulares (226) | select | mobile | "original" | original, square, horizontal, vertical, custom | {"visible_if": "{{ section.settings.use_different_mobile_aspect_ratio }}"} |
| `banner_aspect_ratio_mobile_height` — Alto de la imagen en celulares (242) | range | mobile | 100 | 5…200; paso 5; % | {"visible_if": "{{ section.settings.use_different_mobile_aspect_ratio and section.settings.banner_aspect_ratio_mobile == 'custom' }}"} |
| `gap` — Separación entre elementos (255) | range | shared | 16 | 0…50; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (267) | range | shared | 64 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (279) | range | shared | 0 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |
| `background_color` — Color de fondo (296) | color | shared | "transparent" | no disponible | {} |

<a id="sections-blog-posts-tpl"></a>
## sections/blog-posts.tpl

[sections/blog-posts.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/blog-posts.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `alignment` — Alineación (73) | text_alignment | shared | "left" | left, center, right | {} |
| `section_width` — Ancho (89) | radio | shared | "page" | page, full | {} |
| `gap` — Separación entre elementos (100) | range | shared | 32 | 0…50; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (112) | range | shared | 64 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (124) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |
| `background_color` — Color de fondo (141) | color | shared | "transparent" | no disponible | {} |
| `text_color` — Color del texto (148) | color | shared | settings.text_color | no disponible | {} |

<a id="sections-category-hero-tpl"></a>
## sections/category-hero.tpl

[sections/category-hero.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/category-hero.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `image` — Imagen (86) | image_picker | shared | no disponible | no disponible | {} |
| `use_mobile_image` — Usar otra imagen para celulares (92) | toggle | mobile | false | no disponible | {} |
| `image_mobile` — Imagen (99) | image_picker | mobile | no disponible | no disponible | {"visible_if": "{{ section.settings.use_mobile_image }}"} |
| `show_category_image` — Imagen de categoría (106) | toggle | shared | true | no disponible | {"header_toggle": true} |
| `section_width` — Ancho (123) | radio | shared | "full" | page, full | {} |
| `vertical_padding` — Espaciado superior e inferior (134) | range | shared | 0 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (146) | range | shared | 0 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |

<a id="sections-custom-tpl"></a>
## sections/custom.tpl

[sections/custom.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/custom.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `direction` — Dirección (95) | radio | shared | "row" | column, row | {} |
| `mobile_direction_enabled` — Dirección diferente para celulares (106) | toggle | mobile | true | no disponible | {} |
| `mobile_direction` — Dirección para celulares (113) | radio | mobile | "column" | column, row | {"visible_if": "{{ section.settings.mobile_direction_enabled }}"} |
| `alignment` — Alineación (125) | alignment | shared | "start" | start, center, end | {"vertical_default": "center", "vertical_options": [{"value": "top", "label": "t:options.top"}, {"value": "center", "label": "t:options.center"}, {"value": "bottom", "label": "t:options.bottom"}]} |
| `section_width` — Ancho (147) | radio | shared | "page" | page, full | {} |
| `gap` — Separación entre elementos (158) | range | shared | 16 | 0…50; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (170) | range | shared | 64 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (182) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |
| `custom_background_color` — Color de fondo (199) | color | shared | "transparent" | no disponible | {} |
| `custom_text_color` — Color del texto (206) | color | shared | settings.text_color | no disponible | {} |

<a id="sections-divider-tpl"></a>
## sections/divider.tpl

[sections/divider.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/divider.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `section_width` — Ancho (47) | radio | shared | "page" | page, full | {} |
| `vertical_padding` — Espaciado superior e inferior (58) | range | shared | 64 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (70) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |
| `background_color` — Color de fondo (87) | color | shared | "transparent" | no disponible | {} |
| `show_line` — Línea divisoria (94) | toggle | shared | true | no disponible | {"header_toggle": true} |
| `line_color` — Color de línea (102) | color | shared | settings.text_color | no disponible | {"visible_if": "{{ section.settings.show_line }}"} |

<a id="sections-faq-tpl"></a>
## sections/faq.tpl

[sections/faq.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/faq.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `alignment` — Alineación (61) | text_alignment | shared | "left" | left, center, right | {} |
| `section_width` — Ancho (77) | radio | shared | "page" | page, full | {} |
| `gap` — Separación entre elementos (88) | range | shared | 32 | 0…50; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (100) | range | shared | 64 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (112) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |
| `background_color` — Color de fondo (129) | color | shared | "transparent" | no disponible | {} |
| `text_color` — Color de textos (136) | color | shared | settings.text_color | no disponible | {} |

<a id="sections-featured-brands-tpl"></a>
## sections/featured-brands.tpl

[sections/featured-brands.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/featured-brands.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `text_alignment` — Alineación (84) | alignment | shared | "center" | left, center, right | {} |
| `use_different_mobile_alignment` — Alineación móvil diferente (96) | toggle | mobile | false | no disponible | {} |
| `text_alignment_mobile` — Alineación (103) | alignment | mobile | "center" | left, center, right | {"visible_if": "{{ section.settings.use_different_mobile_alignment }}"} |
| `section_width` — Ancho (120) | radio | shared | "page" | page, full | {} |
| `gap` — Separación entre elementos (131) | range | shared | 32 | 0…50; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (143) | range | shared | 64 | 0…100; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (155) | range | shared | 32 | 0…100; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |
| `background_color` — Color de fondo (172) | color | shared | "transparent" | no disponible | {} |
| `text_color` — Color del texto (179) | color | shared | settings.text_color | no disponible | {} |

<a id="sections-featured-categories-tpl"></a>
## sections/featured-categories.tpl

[sections/featured-categories.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/featured-categories.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `orientation` — Orientación (179) | radio | shared | "horizontal" | vertical, horizontal | {} |
| `use_different_mobile_orientation` — Orientación móvil diferente (190) | toggle | mobile | false | no disponible | {} |
| `orientation_mobile` — Orientación (197) | radio | mobile | "horizontal" | vertical, horizontal | {"visible_if": "{{ section.settings.use_different_mobile_orientation }}"} |
| `text_alignment` — Alineación (209) | text_alignment | shared | "left" | left, center, right | {} |
| `section_width` — Ancho (225) | radio | shared | "page" | page, full | {} |
| `gap` — Separación entre elementos (236) | range | shared | 32 | 0…50; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (248) | range | shared | 64 | 0…100; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (260) | range | shared | 32 | 0…100; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |
| `background_color` — Color de fondo (277) | color | shared | "transparent" | no disponible | {} |

<a id="sections-featured-product-tpl"></a>
## sections/featured-product.tpl

[sections/featured-product.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/featured-product.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `product_type` — Tipo de producto (89) | select | shared | "first" | first, random | {} |
| `section_width` — Ancho (104) | radio | shared | "page" | page, full | {} |
| `gap` — Separación entre elementos (115) | range | shared | 20 | 0…50; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (127) | range | shared | 64 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (139) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |
| `background_color` — Color de fondo (156) | color | shared | "transparent" | no disponible | {} |

<a id="sections-footer-tpl"></a>
## sections/footer.tpl

[sections/footer.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/footer.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `background_color` — Color de fondo (101) | color | shared | settings.text_color | no disponible | {} |
| `text_color` — Color de textos (108) | color | shared | settings.background_color | no disponible | {} |
| `section_width` — Ancho (119) | radio | shared | "page" | page, full | {} |
| `vertical_padding` — Espaciado superior e inferior (130) | range | shared | 32 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (142) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |
| `menus_toggle` — Menús colapsables en celular (159) | toggle | shared | true | no disponible | {"info": "t:info.menus_toggle"} |
| `footer_payments_show` — Mostrar medios de pago (171) | toggle | shared | true | no disponible | {} |
| `footer_shipping_show` — Mostrar medios de envío (178) | toggle | shared | true | no disponible | {} |
| `footer_seal_img` — Imagen del sello personalizado (189) | image_picker | shared | no disponible | no disponible | {} |
| `footer_seal_url` — Link del sello (195) | url | shared | no disponible | no disponible | {"visible_if": "{{ section.settings.footer_seal_img }}"} |
| `footer_custom_seal_code` — Código del sello personalizado (JS/HTML) (202) | custom_code | shared | no disponible | no disponible | {} |

<a id="sections-header-tpl"></a>
## sections/header.tpl

[sections/header.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/header.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `logo_position_desktop` — Posición del logo en escritorio (211) | radio | desktop | "left" | left, center | {} |
| `use_different_mobile_position` — Usar otra posición para celulares (222) | toggle | mobile | false | no disponible | {} |
| `logo_position_mobile` — Posición del logo en celular (229) | radio | mobile | "center" | left, center | {"visible_if": "{{ section.settings.use_different_mobile_position }}"} |
| `nav_position_desktop` — Posición del menú en computadoras (241) | radio | desktop | "below_logo" | below_logo, next_to_logo | {} |
| `section_width` — Ancho (256) | radio | shared | "page" | page, full | {} |
| `vertical_padding` — Espaciado superior e inferior (267) | range | shared | 24 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (279) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |
| `use_different_mobile_padding` — Espaciado diferente para celulares (292) | toggle | mobile | false | no disponible | {} |
| `vertical_padding_mobile` — Espaciado superior e inferior en celulares (299) | range | mobile | 16 | 0…120; paso 4; px | {"visible_if": "{{ section.settings.use_different_mobile_padding }}"} |
| `horizontal_padding_mobile` — Espaciado izquierdo y derecho en celulares (312) | range | mobile | 20 | 0…120; paso 4; px | {"visible_if": "{{ section.settings.use_different_mobile_padding }}", "disabled_if": "{{ section.settings.section_width == 'page' }}"} |
| `head_fix_desktop` — Encabezado fijo (326) | toggle | desktop | true | no disponible | {} |
| `background_color` — Color de fondo (337) | color | shared | settings.background_color | no disponible | {} |
| `text_color` — Color de textos (344) | color | shared | settings.text_color | no disponible | {} |
| `transparent_header` — Encabezado transparente (351) | toggle | shared | false | no disponible | {"header_toggle": true, "info": "t:info.transparent_header"} |
| `transparent_text_color` — Color de textos e íconos (360) | color | shared | settings.text_color | no disponible | {"visible_if": "{{ section.settings.transparent_header }}"} |
| `transparent_logo` — Logo alternativo (368) | image_picker | shared | no disponible | no disponible | {"visible_if": "{{ section.settings.transparent_header }}"} |

<a id="sections-hero-divided-tpl"></a>
## sections/hero-divided.tpl

[sections/hero-divided.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/hero-divided.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `image` — Primera imagen (182) | image_picker | shared | no disponible | no disponible | {} |
| `use_mobile_image` — Usar otra imagen para celulares (188) | toggle | mobile | false | no disponible | {} |
| `image_mobile` — Imagen en celular (195) | image_picker | mobile | no disponible | no disponible | {"visible_if": "{{ section.settings.use_mobile_image }}"} |
| `image_2` — Segunda imagen (202) | image_picker | shared | no disponible | no disponible | {} |
| `use_mobile_image_2` — Usar otra imagen para celulares (208) | toggle | mobile | false | no disponible | {} |
| `image_mobile_2` — Imagen en celular (215) | image_picker | mobile | no disponible | no disponible | {"visible_if": "{{ section.settings.use_mobile_image_2 }}"} |
| `link` — Link (222) | url | shared | no disponible | no disponible | {} |
| `alignment` — Alineación (232) | alignment | shared | "center" | start, center, end | {"vertical_default": "center", "vertical_options": [{"value": "top", "label": "t:options.top"}, {"value": "center", "label": "t:options.center"}, {"value": "bottom", "label": "t:options.bottom"}]} |
| `height` — Altura (254) | range | shared | 80 | 0…100; paso 5; % | {} |
| `gap` — Separación entre elementos (266) | range | shared | 16 | 0…50; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (278) | range | shared | 0 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (290) | range | shared | 0 | 0…120; paso 4; px | {} |
| `text_color` — Color de textos (306) | color | shared | settings.text_color | no disponible | {} |
| `show_overlay` — Fondo transparente (313) | toggle | shared | false | no disponible | {"header_toggle": true, "info": "t:settings.add_overlay"} |
| `overlay_color` — Color (322) | color | shared | "#000000" | no disponible | {"visible_if": "{{ section.settings.show_overlay }}"} |
| `overlay_opacity` — Opacidad (330) | range | shared | 30 | 0…100; paso 5; % | {"visible_if": "{{ section.settings.show_overlay }}"} |
| `content_animation` — Animación al aparecer el contenido (346) | select | shared | "none" | none, fade, slide-up, slide-down | {} |
| `parallax` — Efecto de profundidad al hacer scroll (359) | toggle | shared | false | no disponible | {} |

<a id="sections-hero-tpl"></a>
## sections/hero.tpl

[sections/hero.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/hero.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `image` — Imagen (129) | image_picker | shared | no disponible | no disponible | {} |
| `use_mobile_image` — Usar otra imagen para celulares (135) | toggle | mobile | false | no disponible | {} |
| `image_mobile` — Imagen en celular (142) | image_picker | mobile | no disponible | no disponible | {"visible_if": "{{ section.settings.use_mobile_image }}"} |
| `link` — Link (149) | url | shared | no disponible | no disponible | {} |
| `alignment` — Alineación (159) | alignment | shared | "center" | start, center, end | {"vertical_default": "center", "vertical_options": [{"value": "top", "label": "t:options.top"}, {"value": "center", "label": "t:options.center"}, {"value": "bottom", "label": "t:options.bottom"}]} |
| `height` — Altura (181) | range | shared | 100 | 0…100; paso 5; % | {"disabled_if": "{{ section.settings.auto_height }}"} |
| `auto_height` — Alto automático (194) | checkbox | shared | false | no disponible | {} |
| `gap` — Separación entre elementos (201) | range | shared | 16 | 0…50; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (213) | range | shared | 0 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (225) | range | shared | 0 | 0…120; paso 4; px | {} |
| `text_color` — Color de textos (241) | color | shared | settings.text_color | no disponible | {} |
| `show_overlay` — Fondo transparente (248) | toggle | shared | false | no disponible | {"header_toggle": true, "info": "t:settings.add_overlay"} |
| `overlay_color` — Color (257) | color | shared | "#000000" | no disponible | {"visible_if": "{{ section.settings.show_overlay }}"} |
| `overlay_opacity` — Opacidad (265) | range | shared | 30 | 0…100; paso 5; % | {"visible_if": "{{ section.settings.show_overlay }}"} |
| `content_animation` — Animación al aparecer el contenido (281) | select | shared | "none" | none, fade, slide-up, slide-down | {} |
| `parallax` — Efecto de profundidad al hacer scroll (294) | toggle | shared | false | no disponible | {} |

<a id="sections-icon-text-tpl"></a>
## sections/icon-text.tpl

[sections/icon-text.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/icon-text.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `alignment` — Alineación (63) | text_alignment | shared | "center" | left, center, right | {} |
| `section_width` — Ancho (79) | radio | shared | "page" | page, full | {} |
| `gap` — Separación entre elementos (90) | range | shared | 32 | 0…50; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (102) | range | shared | 64 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (114) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |
| `background_color` — Color de fondo (131) | color | shared | "transparent" | no disponible | {} |
| `text_color` — Color de textos (138) | color | shared | settings.text_color | no disponible | {} |
| `icon_color` — Color del ícono (145) | color | shared | settings.text_color | no disponible | {} |

<a id="sections-image-with-text-tpl"></a>
## sections/image-with-text.tpl

[sections/image-with-text.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/image-with-text.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `section_width` — Ancho (63) | radio | shared | "page" | page, full | {} |
| `gap` — Separación entre elementos (74) | range | shared | 32 | 0…50; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (86) | range | shared | 64 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (98) | range | shared | 0 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |
| `background_color` — Color de fondo (115) | color | shared | "transparent" | no disponible | {} |
| `text_color` — Color del texto (122) | color | shared | settings.text_color | no disponible | {} |

<a id="sections-instagram-feed-tpl"></a>
## sections/instagram-feed.tpl

[sections/instagram-feed.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/instagram-feed.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `alignment` — Alineación (61) | text_alignment | shared | "center" | left, center, right | {} |
| `background_color` — Color de fondo (77) | color | shared | "transparent" | no disponible | {} |
| `text_color` — Color de textos (84) | color | shared | settings.text_color | no disponible | {} |
| `section_width` — Ancho (95) | radio | shared | "page" | page, full | {} |
| `gap` — Separación entre elementos (106) | range | shared | 32 | 0…50; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (118) | range | shared | 64 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (130) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |

<a id="sections-main-404-tpl"></a>
## sections/main-404.tpl

[sections/main-404.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-404.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `section_width` — Ancho (46) | radio | shared | "page" | page, full | {} |
| `vertical_padding` — Espaciado superior e inferior (57) | range | shared | 0 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (69) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |

<a id="sections-main-account-address-tpl"></a>
## sections/main-account-address.tpl

[sections/main-account-address.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-account-address.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `section_width` — Ancho (144) | radio | shared | "page" | page, full | {} |
| `vertical_padding` — Espaciado superior e inferior (155) | range | shared | 0 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (167) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |

<a id="sections-main-account-addresses-tpl"></a>
## sections/main-account-addresses.tpl

[sections/main-account-addresses.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-account-addresses.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `section_width` — Ancho (74) | radio | shared | "page" | page, full | {} |
| `vertical_padding` — Espaciado superior e inferior (85) | range | shared | 0 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (97) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |

<a id="sections-main-account-info-tpl"></a>
## sections/main-account-info.tpl

[sections/main-account-info.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-account-info.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `section_width` — Ancho (72) | radio | shared | "page" | page, full | {} |
| `vertical_padding` — Espaciado superior e inferior (83) | range | shared | 0 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (95) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |

<a id="sections-main-account-order-tpl"></a>
## sections/main-account-order.tpl

[sections/main-account-order.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-account-order.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `section_width` — Ancho (197) | radio | shared | "page" | page, full | {} |
| `vertical_padding` — Espaciado superior e inferior (208) | range | shared | 0 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (220) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |

<a id="sections-main-account-orders-tpl"></a>
## sections/main-account-orders.tpl

[sections/main-account-orders.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-account-orders.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `section_width` — Ancho (213) | radio | shared | "page" | page, full | {} |
| `vertical_padding` — Espaciado superior e inferior (224) | range | shared | 0 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (236) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |

<a id="sections-main-account-subscription-address-tpl"></a>
## sections/main-account-subscription-address.tpl

[sections/main-account-subscription-address.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-account-subscription-address.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `section_width` — Ancho (44) | radio | shared | "page" | page, full | {} |
| `vertical_padding` — Espaciado superior e inferior (55) | range | shared | 0 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (67) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |

<a id="sections-main-account-subscription-product-tpl"></a>
## sections/main-account-subscription-product.tpl

[sections/main-account-subscription-product.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-account-subscription-product.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `section_width` — Ancho (43) | radio | shared | "page" | page, full | {} |
| `vertical_padding` — Espaciado superior e inferior (54) | range | shared | 0 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (66) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |

<a id="sections-main-blog-post-tpl"></a>
## sections/main-blog-post.tpl

[sections/main-blog-post.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-blog-post.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `section_width` — Ancho (42) | radio | shared | "page" | page, full | {} |
| `vertical_padding` — Espaciado superior e inferior (53) | range | shared | 0 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (65) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |

<a id="sections-main-blog-tpl"></a>
## sections/main-blog.tpl

[sections/main-blog.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-blog.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `section_width` — Ancho (52) | radio | shared | "page" | page, full | {} |
| `vertical_padding` — Espaciado superior e inferior (63) | range | shared | 0 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (75) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |

<a id="sections-main-cart-tpl"></a>
## sections/main-cart.tpl

[sections/main-cart.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-cart.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `section_width` — Ancho (112) | radio | shared | "page" | page, full | {} |
| `vertical_padding` — Espaciado superior e inferior (123) | range | shared | 0 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (135) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |

<a id="sections-main-contact-tpl"></a>
## sections/main-contact.tpl

[sections/main-contact.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-contact.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `section_width` — Ancho (183) | radio | shared | "page" | page, full | {} |
| `vertical_padding` — Espaciado superior e inferior (194) | range | shared | 0 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (206) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |

<a id="sections-main-login-tpl"></a>
## sections/main-login.tpl

[sections/main-login.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-login.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `section_width` — Ancho (53) | radio | shared | "page" | page, full | {} |
| `vertical_padding` — Espaciado superior e inferior (64) | range | shared | 0 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (76) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |

<a id="sections-main-newpass-tpl"></a>
## sections/main-newpass.tpl

[sections/main-newpass.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-newpass.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `section_width` — Ancho (76) | radio | shared | "page" | page, full | {} |
| `vertical_padding` — Espaciado superior e inferior (87) | range | shared | 0 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (99) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |

<a id="sections-main-page-tpl"></a>
## sections/main-page.tpl

[sections/main-page.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-page.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `section_width` — Ancho (43) | radio | shared | "page" | page, full | {} |
| `vertical_padding` — Espaciado superior e inferior (54) | range | shared | 0 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (66) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |

<a id="sections-main-password-tpl"></a>
## sections/main-password.tpl

[sections/main-password.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-password.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `section_width` — Ancho (57) | radio | shared | "page" | page, full | {} |
| `vertical_padding` — Espaciado superior e inferior (68) | range | shared | 0 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (80) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |

<a id="sections-main-product-tpl"></a>
## sections/main-product.tpl

[sections/main-product.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-product.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `section_width` — Ancho (59) | radio | shared | "page" | page, full | {} |
| `column_gap` — Separación entre elementos (70) | range | shared | 24 | 0…80; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (82) | range | shared | 24 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (94) | range | shared | 24 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |
| `background_color` — Color de fondo (111) | color | shared | "transparent" | no disponible | {} |

<a id="sections-main-products-grid-tpl"></a>
## sections/main-products-grid.tpl

[sections/main-products-grid.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-products-grid.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `columns` — Disposición en computadoras (189) | select | shared | "4" | 4, 5, 6 | {} |
| `columns_mobile` — Disposición en celulares (202) | select | mobile | "2" | 1, 2 | {} |
| `pagination` — Navegación de productos (214) | select | shared | "classic" | classic, infinite | {} |
| `section_width` — Ancho (229) | radio | shared | "page" | page, full | {} |
| `vertical_padding` — Espaciado superior e inferior (240) | range | shared | 64 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (252) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |

<a id="sections-main-register-tpl"></a>
## sections/main-register.tpl

[sections/main-register.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-register.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `section_width` — Ancho (51) | radio | shared | "page" | page, full | {} |
| `vertical_padding` — Espaciado superior e inferior (62) | range | shared | 0 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (74) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |

<a id="sections-main-reset-tpl"></a>
## sections/main-reset.tpl

[sections/main-reset.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/main-reset.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `section_width` — Ancho (60) | radio | shared | "page" | page, full | {} |
| `vertical_padding` — Espaciado superior e inferior (71) | range | shared | 0 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (83) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |

<a id="sections-navigation-bar-tpl"></a>
## sections/navigation-bar.tpl

[sections/navigation-bar.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/navigation-bar.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `mobile_placement` — Ubicación en celulares (96) | radio | mobile | "header" | header, menu | {} |
| `section_width` — Ancho (111) | radio | shared | "page" | page, full | {} |
| `item_gap` — Separación entre elementos (122) | range | shared | 32 | 0…48; paso 2; px | {} |
| `vertical_padding` — Espaciado superior e inferior (134) | range | shared | 8 | 0…32; paso 2; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (146) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |
| `use_different_mobile_spacing` — Espaciado diferente para celulares (159) | toggle | mobile | false | no disponible | {} |
| `mobile_vertical_padding` — Espaciado superior e inferior en celulares (166) | range | mobile | 16 | 0…32; paso 2; px | {"visible_if": "{{ section.settings.use_different_mobile_spacing }}"} |
| `mobile_horizontal_padding` — Espaciado izquierdo y derecho en celulares (179) | range | mobile | 20 | 0…120; paso 4; px | {"visible_if": "{{ section.settings.use_different_mobile_spacing }}", "disabled_if": "{{ section.settings.section_width == 'page' }}"} |
| `background_color` — Color de fondo (197) | color | shared | "#000000" | no disponible | {} |
| `text_color` — Color de textos (204) | color | shared | "#ffffff" | no disponible | {} |

<a id="sections-newsletter-tpl"></a>
## sections/newsletter.tpl

[sections/newsletter.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/newsletter.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `image` — Imagen (155) | image_picker | shared | no disponible | no disponible | {} |
| `use_mobile_image` — Usar otra imagen para celulares (161) | toggle | mobile | false | no disponible | {} |
| `image_mobile` — Imagen en celular (168) | image_picker | mobile | no disponible | no disponible | {"visible_if": "{{ section.settings.use_mobile_image }}"} |
| `image_position` — Posición de la imagen (179) | radio | shared | "background" | background, left, right | {} |
| `text_alignment` — Alineación (191) | text_alignment | shared | "center" | left, center, right | {} |
| `background_color` — Color de fondo (207) | color | shared | settings.background_color | no disponible | {} |
| `text_color` — Color del texto (214) | color | shared | settings.text_color | no disponible | {} |
| `section_width` — Ancho (225) | radio | shared | "page" | page, full | {} |
| `vertical_gap` — Separación vertical de elementos (236) | range | shared | 32 | 0…50; paso 4; px | {"visible_if": "{{ section.settings.image_position != 'background' }}"} |
| `horizontal_gap` — Separación horizontal de elementos (249) | range | shared | 16 | 0…50; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (261) | range | shared | 64 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (273) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |
| `show_overlay` — Agrega una capa de transparencia sobre la imagen. (291) | toggle | shared | false | no disponible | {"visible_if": "{{ section.settings.image_position == 'background' }}"} |
| `overlay_color` — Color (299) | color | shared | "#000000" | no disponible | {"visible_if": "{{ section.settings.image_position == 'background' }}", "disabled_if": "{{ section.settings.show_overlay == false }}"} |
| `overlay_opacity` — Opacidad (308) | range | shared | 30 | 0…100; paso 5; % | {"visible_if": "{{ section.settings.image_position == 'background' }}", "disabled_if": "{{ section.settings.show_overlay == false }}"} |

<a id="sections-page-header-tpl"></a>
## sections/page-header.tpl

[sections/page-header.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/page-header.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `section_width` — Ancho (125) | radio | shared | "page" | page, full | {} |
| `vertical_padding` — Espaciado superior e inferior (136) | range | shared | 32 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (148) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |
| `background_color` — Fondo (165) | color | shared | "transparent" | no disponible | {} |
| `text_color` — Color del texto (172) | color | shared | settings.text_color | no disponible | {} |

<a id="sections-product-description-tpl"></a>
## sections/product-description.tpl

[sections/product-description.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/product-description.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `show_title` — Mostrar título (65) | toggle | shared | true | no disponible | {} |
| `show_social` — Mostrar redes sociales (72) | toggle | shared | true | no disponible | {} |
| `background_color` — Color de fondo (83) | color | shared | "transparent" | no disponible | {} |
| `text_color` — Color de textos (90) | color | shared | settings.text_color | no disponible | {} |
| `section_width` — Ancho (101) | radio | shared | "page" | page, full | {} |
| `vertical_padding` — Espaciado superior e inferior (112) | range | shared | 32 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (124) | range | shared | 0 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |

<a id="sections-product-list-tpl"></a>
## sections/product-list.tpl

[sections/product-list.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/product-list.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `alignment` — Alineación (104) | text_alignment | shared | "left" | left, center, right | {} |
| `section_width` — Ancho (120) | radio | shared | "page" | page, full | {} |
| `gap` — Separación entre elementos (131) | range | shared | 32 | 0…50; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (143) | range | shared | 64 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (155) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |
| `background_color` — Color de fondo (172) | color | shared | "transparent" | no disponible | {} |

<a id="sections-related-products-tpl"></a>
## sections/related-products.tpl

[sections/related-products.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/related-products.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `section_width` — Ancho (130) | radio | shared | "page" | page, full | {} |
| `gap` — Separación entre elementos (141) | range | shared | 32 | 0…50; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (153) | range | shared | 32 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (165) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |
| `background_color` — Color de fondo (182) | color | shared | "transparent" | no disponible | {} |

<a id="sections-rich-text-tpl"></a>
## sections/rich-text.tpl

[sections/rich-text.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/rich-text.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `alignment` — Alineación (64) | text_alignment | shared | "center" | left, center, right | {} |
| `background_color` — Color de fondo (80) | color | shared | "transparent" | no disponible | {} |
| `text_color` — Color de textos (87) | color | shared | settings.text_color | no disponible | {} |
| `section_width` — Ancho (98) | radio | shared | "page" | page, full | {} |
| `gap` — Separación entre elementos (109) | range | shared | 16 | 0…50; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (121) | range | shared | 64 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (133) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |

<a id="sections-slideshow-tpl"></a>
## sections/slideshow.tpl

[sections/slideshow.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/slideshow.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `section_width` — Ancho (102) | radio | shared | "full" | page, full | {} |
| `height` — Altura (113) | range | shared | 400 | 200…800; paso 20; px | {"visible_if": "{{ section.settings.section_width == 'page' }}", "disabled_if": "{{ section.settings.auto_height }}"} |
| `height_full` — Altura (127) | range | shared | 90 | 0…100; paso 5; % | {"visible_if": "{{ section.settings.section_width == 'full' }}", "disabled_if": "{{ section.settings.auto_height }}"} |
| `auto_height` — Alto automático (141) | checkbox | shared | true | no disponible | {} |
| `vertical_padding` — Espaciado superior e inferior (148) | range | shared | 0 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (160) | range | shared | 0 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |
| `autoplay` — Automática (177) | toggle | shared | true | no disponible | {} |
| `autoplay_speed` — Velocidad (184) | range | shared | 5 | 3…10; paso 1; s | {"disabled_if": "{{ section.settings.autoplay == false }}"} |
| `content_animation` — Animación al aparecer el contenido (196) | select | shared | "none" | none, fade, slide-up, slide-down | {} |

<a id="sections-testimonials-tpl"></a>
## sections/testimonials.tpl

[sections/testimonials.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/testimonials.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `alignment` — Alineación (62) | text_alignment | shared | "center" | left, center, right | {} |
| `background_color` — Color de fondo (78) | color | shared | "transparent" | no disponible | {} |
| `text_color` — Color de textos (85) | color | shared | settings.text_color | no disponible | {} |
| `section_width` — Ancho (96) | radio | shared | "page" | page, full | {} |
| `gap` — Separación entre elementos (107) | range | shared | 32 | 0…50; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (119) | range | shared | 64 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (131) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |

<a id="sections-timer-offers-tpl"></a>
## sections/timer-offers.tpl

[sections/timer-offers.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/timer-offers.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `start_date` — Fecha de inicio (127) | date | shared | no disponible | no disponible | {} |
| `start_time` — Hora de inicio (133) | time | shared | no disponible | no disponible | {} |
| `end_date` — Fecha de finalización (139) | date | shared | no disponible | no disponible | {} |
| `end_time` — Hora de finalización (145) | time | shared | no disponible | no disponible | {} |
| `section_width` — Ancho (155) | radio | shared | "page" | page, full | {} |
| `gap` — Separación entre elementos (166) | range | shared | 16 | 0…50; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (178) | range | shared | 64 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (190) | range | shared | 32 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |
| `background_color` — Color de fondo (207) | color | shared | "transparent" | no disponible | {} |

<a id="sections-video-with-text-tpl"></a>
## sections/video-with-text.tpl

[sections/video-with-text.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/video-with-text.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `section_width` — Ancho (93) | radio | shared | "page" | page, full | {} |
| `gap` — Separación entre elementos (104) | range | shared | 0 | 0…50; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (116) | range | shared | 64 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (128) | range | shared | 0 | 0…120; paso 4; px | {"disabled_if": "{{ section.settings.section_width == 'page' }}"} |
| `background_color` — Color de fondo (145) | color | shared | "transparent" | no disponible | {} |

<a id="sections-video-tpl"></a>
## sections/video.tpl

[sections/video.tpl:1](</home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/sections/video.tpl:1>)

| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |
|---|---|---|---|---|---|
| `video_url` — Link de YouTube o Vimeo (161) | video_url | shared | no disponible | no disponible | {} |
| `cover_image` — Imagen de portada (168) | image_picker | shared | no disponible | no disponible | {"info": "t:info.video_cover_image"} |
| `link` — Link (175) | url | shared | no disponible | no disponible | {"visible_if": "{{ section.settings.video_type == 'autoplay' }}"} |
| `video_type` — Tipo de reproducción (186) | select | shared | "autoplay" | autoplay, manual | {} |
| `format_mobile` — Formato en celulares (197) | select | mobile | "16by9" | 16by9, 4by3, 1by1, 9by16 | {} |
| `alignment` — Alineación (214) | alignment | shared | "center" | start, center, end | {"vertical_default": "center", "vertical_options": [{"value": "top", "label": "t:options.top"}, {"value": "center", "label": "t:options.center"}, {"value": "bottom", "label": "t:options.bottom"}]} |
| `gap` — Separación entre elementos (236) | range | shared | 16 | 0…50; paso 4; px | {} |
| `vertical_padding` — Espaciado superior e inferior (248) | range | shared | 0 | 0…120; paso 4; px | {} |
| `horizontal_padding` — Espaciado izquierdo y derecho (260) | range | shared | 0 | 0…120; paso 4; px | {} |
| `text_color` — Color de textos (276) | color | shared | settings.text_color | no disponible | {} |
| `show_overlay` — Fondo transparente (283) | toggle | shared | false | no disponible | {"header_toggle": true, "info": "t:settings.add_overlay"} |
| `overlay_color` — Color (292) | color | shared | "#000000" | no disponible | {"visible_if": "{{ section.settings.show_overlay }}"} |
| `overlay_opacity` — Opacidad (300) | range | shared | 30 | 0…100; paso 5; % | {"visible_if": "{{ section.settings.show_overlay }}"} |
