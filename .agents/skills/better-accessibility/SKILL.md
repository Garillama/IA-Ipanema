---
name: better-accessibility
description: Auditar, diagnosticar y corregir accesibilidad web conforme a WCAG 2.2 Nivel A y AA (semántica HTML, navegación por teclado, gestión de foco, ARIA, nombres accesibles, formularios, anuncios dinámicos, modales/drawers, movimiento reducido, áreas táctiles 24x24px, zoom 200% y reflow 320px) en Shopify Liquid, Hydrogen/Remix, React y Tiendanube/Ipanema, separando fallos verificados de recomendaciones sin alterar contratos comerciales ni diseño de marca.
---

# Better Accessibility — Ingeniería y Auditoría de Accesibilidad WCAG 2.2 (A / AA)

Esta skill es el **módulo especializado de accesibilidad web (`better-accessibility`)** de `IA-Ipanema`, integrado desde `jakubkrehel/skills` (`skills/better-accessibility`) y adaptado a comercio electrónico (Shopify Liquid, Shopify Hydrogen, Remix, React y Tiendanube/Ipanema).

## 1. Procedencia Verificada e Integridad Criptográfica

- **Repositorio de origen:** `https://github.com/jakubkrehel/skills`
- **Ruta original:** `skills/better-accessibility/`
- **Commit inmutable:** `547d415dc10a23e66088eba5aa6664e6e772432c`
- **Licencia:** `MIT`
- **Artefactos verificados mediante `git hash-object` y `SHA-256`:**
  - `SKILL.md`: Git blob SHA-1 `b5293ecc20e4356a50a55e1a1eadd3db9a0019a7` · SHA-256 `6a6465c044783968bae9896fd9e2e78437b90578fe3309b6dee6ef6a920e45f9` (10452 bytes)
  - `agents/openai.yaml`: Git blob SHA-1 `36b942fb8e5b86916b006c2fe4e07fdbde24a112` · SHA-256 `98699206d4fb00b72bcaf69bb446f541644cc0cc3d23967e266731e100a55563` (121 bytes)
  - `focus-and-keyboard.md`: Git blob SHA-1 `361ad8e51c83249d9dc16a97b4ae01883de08131` · SHA-256 `ace66413242a31df97f1d5101bddc98d871c97716cbc936a439291ea5fda7e54` (6356 bytes)
  - `forms.md`: Git blob SHA-1 `8f960cbb59f6dfd27cb47f6a962198659ff66dcd` · SHA-256 `ed63f7424eb1d3515e4261504467d77840317dda7c0df86c965ee334b3499589` (3628 bytes)
  - `hit-areas.md`: Git blob SHA-1 `9f9aa538683a0ba68b6164a8508164dd6109ca42` · SHA-256 `c723a5c5a0935148dbf54dcc1b9fa140251f50a6e953ed79f77af498eae3b615` (3385 bytes)
  - `motion-and-zoom.md`: Git blob SHA-1 `e184315a5060f86107d4fb2951e884bf697cc399` · SHA-256 `743bae6a93843ff07ebb283d8de31e3ecd184e04f8de639b0e3b0949088fc13a` (2055 bytes)
  - `reporting.md`: Git blob SHA-1 `46d221bad48a6e0992d13377a285ed6f9002f794` · SHA-256 `6203f74162d308d844bd6db8b677502757da922b274ef72cacdba63819073659` (1174 bytes)
  - `screen-readers.md`: Git blob SHA-1 `7da1b74995ee8bb6374e2aa17e694e7d55dc21bd` · SHA-256 `a65faa6f28ef972b71328d5aaafb1c13fc9796b02bfa0557ae23a02569267c3b` (4450 bytes)
  - `semantics-and-aria.md`: Git blob SHA-1 `24ab05c1d7fbdbd5900b5e7758bae23d06e91866` · SHA-256 `dfbadab983f65cd5f666ee4e1aecdf9a243ea206876a3f575a12f0b1314f6e37` (4380 bytes)

---

## 2. Principio Rector: Criterios WCAG 2.2 (A / AA), No Convenciones Arbitrarias

1. **Criterios frente a recomendaciones (`Criteria, not conventions`)**:
   - Un **incumplimiento verificable (`wcag_violation`)** debe citar un criterio concreto de **WCAG 2.2 Nivel A o AA** por número (ej. `1.1.1`, `1.3.1`, `1.3.5`, `1.4.3`, `1.4.4`, `1.4.10`, `1.4.11`, `2.1.1`, `2.1.2`, `2.2.2`, `2.4.1`, `2.4.3`, `2.4.7`, `2.4.11`, `2.5.3`, `2.5.7`, `2.5.8`, `3.3.1`, `3.3.2`, `4.1.2`, `4.1.3`) o una tarea concreta que un usuario de tecnología de asistencia no puede completar.
   - Todo lo demás —incluidos objetivos Nivel AAA (`2.4.13`, `2.5.5` de `44×44px`), convenciones APG opcionales, esquemas estrictos de un solo `<h1>` sin saltos de nivel o preferir validar al enviar frente a botón deshabilitado— se clasifica como **recomendación (`best_practice_recommendation`)** y **nunca** como incumplimiento WCAG ni severidad `HIGH`.
   - **Nunca declares incumplimiento WCAG únicamente por preferencias de diseño.**
2. **Metodología de dos recorridos (`Two Walks`)**:
   - **Recorrido de teclado (`Keyboard-only walk`)**: Todo flujo comercial (seleccionar variante, añadir al carrito, abrir/cerrar cart drawer, filtrar colección, buscar, enviar formulario) debe completarse de principio a fin sin ratón (`Tab`, `Shift+Tab`, `Enter`, `Space`, `Escape`, flechas en widgets compuestos).
   - **Recorrido de lector de pantalla (`Screen-reader walk`)**: Todo control interactivo debe anunciar **nombre accesible (`name`)**, **rol (`role`)** y **estado (`state`)** (`aria-expanded`, `aria-selected`, `aria-checked`, `aria-invalid`, `aria-disabled`).

---

## 3. Complementariedad y Enrutamiento con las 6 Skills Anteriores

| Dominio | Skill Primaria | Relación con `better-accessibility` |
|---|---|---|
| Rendimiento y Core Web Vitals | [`cloudflare-web-perf`](../cloudflare-web-perf/SKILL.md) | Independiente; `better-accessibility` no mide LCP/TTFB/TBT. |
| Calidad web general | [`web-quality-audit`](../web-quality-audit/SKILL.md) | Auditoría global; `better-accessibility` puede reutilizar sus violaciones `axe` o de DOM renderizado sin re-ejecutar Lighthouse. |
| SEO técnico y on-page | [`seo-audit`](../seo-audit/SKILL.md) | Independiente; `better-accessibility` evalúa estructura de navegación (`<main>`, `skip link`, landmarks `<nav aria-label>`) para tecnologías de asistencia. |
| Datos estructurados JSON-LD | [`schema`](../schema/SKILL.md) | Independiente. |
| Arquitectura React / Hydrogen | [`vercel-react-best-practices`](../vercel-react-best-practices/SKILL.md) | `better-accessibility` verifica que hidratación/re-renders no pierdan el foco ni borren entradas de usuario. |
| Diseño UI/UX e interfaz | [`web-design-guidelines`](../web-design-guidelines/SKILL.md) | Cuando `web-design-guidelines` detecta o requiere análisis profundo de accesibilidad WCAG 2.2 (teclado, foco, ARIA, lectores de pantalla), delega o reutiliza la evaluación de `better-accessibility`. |

---

## 4. Reglas Técnicas WCAG 2.2 A / AA para E-commerce

### 4.1 Semántica HTML y ARIA (`4.1.2 Name, Role, Value`, `1.3.1 Info and Relationships`)
- **Elementos nativos primero**: `<button>` para acciones (agregar al carrito, abrir drawer, cambiar variante) y `<a href="...">` para navegación (ir a PDP o colección). Prohibido `<div onClick>` o `<span onClick>`.
- **Menos ARIA es mejor que mal ARIA**:
  - Prohibido `aria-label` en `<div>` o `<span>` sin rol interactivo (ARIA 1.2 prohíbe nombrar el rol `generic`).
  - Prohibido `<button role="button">` redundante o `role="menu"` en listas de navegación web (`<nav><ul>`).
  - Prohibido `aria-labelledby` o `aria-describedby` apuntando a un `id` inexistente en el documento.
  - Prohibido combinar `disabled` y `aria-disabled="true"` en el mismo elemento.
- **Landmarks y estructura (`2.4.1 Bypass Blocks`)**:
  - Un único `<main id="main">` primario visible y enlace `"Saltar al contenido"` (`skip-link`) como primer elemento enfocable cuando precede navegación repetida.
  - Cuando existen múltiples `<nav>` (primaria, breadcrumbs, footer), distinguirlos con `aria-label` único.

### 4.2 Navegación por Teclado y Gestión del Foco (`2.1.1 Keyboard`, `2.1.2 No Keyboard Trap`, `2.4.3 Focus Order`, `2.4.7 Focus Visible`, `2.4.11 Focus Not Obscured`)
- **Anillo de foco visible (`2.4.7 AA`)**:
  - Estilizar `:focus-visible` (preferiblemente conservando el indicador nativo con `outline-offset: 2px` o token de foco `outline: 2px solid var(--focus-ring)` con contraste >= 3:1 bajo `1.4.11`).
  - **Prohibido** `outline: none` / `outline-none` sin reemplazo `:focus-visible` verificado.
- **Foco no oculto (`2.4.11 AA`)**: Ningún elemento enfocado debe quedar oculto detrás de un header/footer `sticky`; usar `scroll-padding-block-start` o `scroll-margin-block-start`.
- **Reglas de `tabindex` (`2.4.3 A`)**:
  - Usar únicamente `tabindex="0"` (orden natural) y `tabindex="-1"` (foco programático / roving tabindex). **Prohibido `tabindex` positivo (`tabindex="1"`, `2`, etc.)**.
  - Todo elemento con `role="button"`, `role="tab"`, `role="switch"` o `role="menuitem"` no nativo exige `tabindex="0"` y manejador de teclado (`onKeyDown` con `Enter`/`Space` o flechas).
- **Modales, Cart Drawers y Menús Móviles (`2.1.2 A`, `2.4.3 A`)**:
  - Preferir `<dialog>` con `showModal()` o contenedor con `role="dialog"`, `aria-modal="true"`, nombre accesible (`aria-labelledby` / `aria-label`), fondo con atributo `inert`, cierre con tecla `Escape`, traslado de foco al abrir y restauración de foco al botón disparador al cerrar.

### 4.3 Nombres Accesibles, Lectores de Pantalla y Textos Alternativos (`1.1.1 Non-text Content`, `2.5.3 Label in Name`, `4.1.2 Name, Role, Value`, `4.1.3 Status Messages`)
- **Botones de icono y SVG (`4.1.2 A`, `1.1.1 A`)**:
  - Todo botón de solo icono (cerrar drawer, carrito, buscar, eliminar línea) requiere `aria-label` descriptivo de la acción y `<svg aria-hidden="true">`.
- **Label in Name (`2.5.3 A`)**: Cuando un control tiene texto visible (ej. `"Comprar"`), su `aria-label` (si existe) debe comenzar con o contener exactamente ese texto visible para no romper control por voz.
- **Peligro de `aria-hidden="true"` en elementos enfocables (`4.1.2 A`)**:
  - **Nunca** colocar `aria-hidden="true"` en un `<button>`, `<a href>`, `<input>` o en un ancestro de elementos enfocables sin `inert` / `tabindex="-1"`.
- **Anuncios dinámicos (`4.1.3 AA`)**:
  - Errores por campo: `aria-invalid="true"` + `aria-describedby="id-error"`.
  - Actualizaciones no urgentes (contador de carrito, `"Producto agregado"`, resultados de filtro/búsqueda): región estable en el DOM con `role="status"` (o `aria-live="polite"`). No usar `aria-live="assertive"` para mensajes de éxito ni montar la región junto con el texto de forma efímera.
  - Errores urgentes de nivel formulario/sesión: `role="alert"`.
- **Textos alternativos (`1.1.1 A`)**:
  - Imágenes decorativas: `alt=""`. Imágenes informativas (fotos de producto/variante): `alt` con significado. Imágenes funcionales (dentro de enlace/botón): `alt` con la acción o destino. Prohibido omitir el atributo `alt`.

### 4.4 Formularios Accesibles (`3.3.2 Labels or Instructions`, `1.3.5 Identify Input Purpose`, `3.3.1 Error Identification`)
- Todo `<input>`, `<select>`, `<textarea>` requiere `<label for="...">` explícito o `<label>` envolvente; un `placeholder` nunca sustituye a un `<label>`.
- Campos de datos personales del comprador (nombre, email, teléfono, dirección, código postal) requieren token `autocomplete` válido (`1.3.5 AA`), `name` descriptivo y `type`/`inputmode` apropiado.
- Nunca bloquear el pegado (`onPaste` con `preventDefault`).
- Validar al enviar; marcar campos con fallo mediante `aria-invalid="true"` y `aria-describedby`, mostrando texto/icono además del color (`1.4.1 A`).

### 4.5 Áreas Táctiles, Gestos, Movimiento Reducido, Zoom y Reflow (`2.5.8 Target Size Minimum`, `2.5.7 Dragging Movements`, `2.2.2 Pause, Stop, Hide`, `1.4.4 Resize Text`, `1.4.10 Reflow`, `1.4.3` / `1.4.11` Contrast)
- **Tamaño de objetivo (`2.5.8 AA` vs recomendación `44×44px`)**:
  - El umbral obligatorio **WCAG 2.5.8 Nivel AA es `24×24px`** (salvo excepciones de espaciado/inline).
  - Un tamaño entre `24px` y `43px` se reporta únicamente como **recomendación de ergonomía táctil (`44×44px` AAA / HIG)**, nunca como violación WCAG AA.
  - Las capas decorativas superpuestas (glows, scrims decorativos) deben llevar `pointer-events: none` para no interceptar clics.
- **Alternativa a arrastre (`2.5.7 AA`)**: Todo slider/drag requiere alternativa de puntero simple (botones o inputs).
- **Movimiento reducido y autoplay (`2.2.2 A`)**:
  - Respetar `@media (prefers-reduced-motion: no-preference)` o `prefers-reduced-motion: reduce`.
  - Carruseles con autoplay o vídeos en bucle (>5s) requieren botón visible de pausa/detención (`2.2.2 A`).
- **Zoom y reflow (`1.4.4 AA`, `1.4.10 AA`)**:
  - Prohibido `user-scalable=no` o `maximum-scale=1` en meta viewport (`1.4.4 AA`).
  - La página debe hacer reflow a `320px` de ancho sin scroll horizontal (`1.4.10 AA`).
- **Contraste medible (`1.4.3 AA`, `1.4.11 AA`)**:
  - Texto normal >= `4.5:1`; texto grande (`>=24px` o `>=18.67px` bold) >= `3:1`; bordes de componentes UI e indicadores de foco/estado >= `3:1`. Solo se declara fallo cuando existe evidencia medible de la pareja de colores; sin modificar la paleta de la marca salvo solicitud expresa.

---

## 5. Uso del Motor Local (`performance accessibility-audit`)

```bash
python3 tools/ia.py --project <proyecto> performance accessibility-audit \
  --source-file <ruta-autorizada-1> \
  --framework <shopify-liquid|shopify-hydrogen|remix|nextjs|react-web|tiendanube-ipanema>
```

Admite opcionalmente `--rendered <rendered.json>` y `--design-report <wdg.json>` / `--quality-report <wqa.json>` para reutilizar hallazgos previos sin duplicar análisis.
