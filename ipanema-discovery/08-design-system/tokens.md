# Tokens existentes y propuesta de uso

Fecha: 2026-11-08. Fuente principal: [style-tokens.tpl](/home/alanrichard/orca/workspaces/scentperfumesclaude/merganser/layouts/resources/style-tokens.tpl:1). Propuesta arquitectónica; no se creó una nueva capa de tokens en el tema.

| Área | Tokens / configuración encontrados | Decisión de reutilización |
|---|---|---|
| Color | main-background/foreground, accent, estados y opacidades derivadas | Branding desde settings; no copiar hex por cada bloque |
| Tipo | heading-font/body-font, font-base y h1–h6 | Tamaño visual separado de jerarquía HTML |
| Espacio | spacing-base 16 px; escala 4/8/16/24/48; section 64 y section-small 32 | Reutilizar ritmo; settings por instancia donde exista control |
| Contenedor | page-width, gutter y variantes md | Medir espacio real al calcular sizes |
| Radio | base 8 px; derivados y full, radios de botón/label | Mantener diferencias intencionales de comercio |
| Sombra | drop-shadow usa color derivado | Evitar sombras pesadas animadas por toda tarjeta |
| Motion | transition-fast/normal/slow con all | Reutilizar duración con cuidado; preferir propiedades explícitas en nuevos efectos |
| Iconos | Sprite SVG e icon.tpl, icon_style y tamaños | No cargar otra biblioteca de iconos para el mismo propósito |
| Botones | Primary/secondary/tertiary con colores/borde/radio | Un estilo global, variantes por rol; no otro btn completo |
| Formularios | form-input/select/radio/alert y clases existentes | Conservar labels, estados y contratos de envío |
| Z-index | Valores distribuidos en CSS | No se encontró una escala global única de tokens; propuesta a definir tras revisar overlays |
| Breakpoints | Predominio md=768 y reglas particulares | Usar el sistema existente, no cambiar cortes globales por una sección |

Distinguir token de marca, token funcional y control de instancia. Un color global beneficia todas las tiendas, pero la decisión concreta de cada marca permanece en sus datos. Los valores CSS computados pueden diferir por contexto; no sustituirlos por los defaults de un documento sin leer settings efectivos.
