---
name: web-design-guidelines
description: Auditar, revisar y mejorar el diseño de interfaces web, jerarquía visual, UX de e-commerce, estados interactivos, responsive y consistencia visual conforme a Vercel Web Interface Guidelines en Shopify Liquid, Hydrogen/Remix, React y Tiendanube/Ipanema, conservando la identidad visual de la marca y sin realizar descargas dinámicas de reglas.
---

# Vercel Web Design Guidelines — Revisión de Interfaz, UX y Diseño E-commerce

Esta skill es la **capacidad especializada de revisión de interfaz y experiencia de usuario (`web-design-guidelines`)** del sistema, integrada desde `vercel-labs/agent-skills` y `vercel-labs/web-interface-guidelines` y adaptada a la arquitectura determinista, segura y basada en evidencia de Ipanema.

## 1. Procedencia Verificada y Reglas Incorporadas Estáticamente

- **Repositorio de la skill:** `https://github.com/vercel-labs/agent-skills`
- **Ruta original de la skill:** `skills/web-design-guidelines/SKILL.md`
- **Commit inmutable de la skill:** `1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62`
- **Git blob SHA-1 (`SKILL.md`):** `ceae92ab319216a68274168fba9b63b998b65997`
- **SHA-256 (`SKILL.md`):** `f4647ca866a3accf763777f83e7682954f0187cd6bea7eea0399796652414e8f` (1231 bytes)
- **Repositorio de las reglas:** `https://github.com/vercel-labs/web-interface-guidelines`
- **Ruta original de las reglas:** `command.md`
- **Commit inmutable de las reglas:** `434b7f91364665f2f733b310ec54809bf8f37937` (`2026-10-05T20:49:16Z`)
- **Git blob SHA-1 (`command.md`):** `3eb3a212b7b89493922ea418489d4c6f67ae8bd5`
- **SHA-256 (`command.md`):** `d246b026f4f29b5823a9cc857f9edf3d2507002e055e32040cadeaf3b38e0234` (8055 bytes)
- **Licencia:** `MIT`

> **Restricción de seguridad crítica (sin descarga dinámica en tiempo de ejecución):**
> El `SKILL.md` original de Vercel indica consultar `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` mediante `WebFetch` antes de cada revisión. **En Ipanema está terminantemente prohibido descargar reglas remotas desde `/main/` o desde Internet en tiempo de ejecución.** Todas las reglas del commit `434b7f91364665f2f733b310ec54809bf8f37937` están incorporadas de forma estática, versionada y auditada en esta skill y en el motor local (`audit_web_design_guidelines` / `performance design-audit`).

---

## 2. Cuándo Activar Esta Skill y Relación con las Otras Skills

Activa `web-design-guidelines` cuando la solicitud pida:
- Revisar o auditar el diseño de una página, interfaz o componente (`review my UI`, `audit design`, `review UX`, `web-design-guidelines`).
- Evaluar UX, jerarquía visual, claridad de CTA, formularios, navegación, estados interactivos (`hover`, `focus-visible`, `disabled`, `loading`, errores inline) y consistencia visual.
- Auditar páginas de producto (PDP), listados/colecciones, tarjetas de producto, selectores de variantes, carrito/drawer, barras de progreso, productos relacionados o bloques promocionales.
- Detectar problemas visuales, de layout, truncamiento, áreas táctiles o responsive en Shopify Liquid, Shopify Hydrogen, Remix, React o Tiendanube/Ipanema.

### Coordinación y No Duplicación con las 5 Skills Anteriores

| Skill | Dominio Principal | Relación con `web-design-guidelines` |
|---|---|---|
| [`cloudflare-web-perf`](../cloudflare-web-perf/SKILL.md) | Core Web Vitals, red, LCP/CLS/INP, TTFB/FCP/TBT | `web-design-guidelines` evalúa dimensiones de imagen/CLS visual y `prefers-reduced-motion` en UI; delega el diagnóstico profundo de cascadas de red y CWV en `cloudflare-web-perf`. |
| [`web-quality-audit`](../web-quality-audit/SKILL.md) | Auditoría general multi-categoría (Lighthouse/calidad global) | Si el usuario pide una revisión general de calidad web, usa `web-quality-audit`. Si pide revisión de interfaz, UX, jerarquía visual o componentes UI, usa `web-design-guidelines` y reutiliza hallazgos verificados cuando existan. |
| [`seo-audit`](../seo-audit/SKILL.md) | SEO técnico, indexabilidad, canonicals, sitemaps, hreflang | `web-design-guidelines` revisa jerarquía visual de encabezados (`<h1>`–`<h6>`) y enlaces `<a href>` interactivos sin duplicar rastreo ni sitemaps. |
| [`schema`](../schema/SKILL.md) | Datos estructurados JSON-LD / Schema.org | Dominios ortogonales; nunca modifiques bloques JSON-LD durante ajustes de interfaz. |
| [`vercel-react-best-practices`](../vercel-react-best-practices/SKILL.md) | Arquitectura React/Hydrogen/Remix (waterfalls, bundles, hooks) | `web-design-guidelines` revisa la capa de interfaz, estados interactivos, hidratación de inputs (`value`/`onChange`) y UX; `vercel-react-best-practices` optimiza loaders, bundles y re-renders. |

---

## 3. Reglas de Interfaz Incorporadas Estáticamente (`command.md` @ `434b7f91364665f2f733b310ec54809bf8f37937`)

### 3.1 Jerarquía Visual, Tipografía y Manejo de Contenido (`visual-hierarchy`)
- **Encabezados y anclas:** Jerarquía lógica `<h1>`–`<h6>` con enlace de salto al contenido principal (`skip link`) y `scroll-margin-top` en encabezados con ancla.Balanceo tipográfico con `text-wrap: balance` o `text-pretty` en títulos para evitar viudas.
- **Comparación numérica (precios, cantidades, tablas):** Usar `font-variant-numeric: tabular-nums` en precios, descuentos, contadores de stock y tablas comparativas.
- **Tipografía y microcopy:** Elipsis real `…` en lugar de `...` (especialmente en estados `"Loading…"`, `"Saving…"` y placeholders); espacios de no separación (`&nbsp;`) entre cantidades y unidades (`10&nbsp;MB`); etiquetas de botón específicas (`"Agregar al carrito"`, `"Guardar dirección"`, nunca etiquetas ambiguas como `"Continuar"` o `"Click"`).
- **Contenedores de texto y estados vacíos:** Manejar textos largos con `truncate`, `line-clamp-*` o `break-words`; los hijos flexibles necesitan `min-w-0` para permitir truncamiento sin desbordar; contemplar siempre estados vacíos (`empty states`) para colecciones, carrito o búsqueda sin resultados.

### 3.2 UX de E-commerce (`ecommerce-ux`)
- **Página de producto (PDP):**
  - El título, precio, disponibilidad, selector de variantes y CTA primario (`Agregar al carrito` / `Comprar`) deben mantener una jerarquía visual clara y proximidad funcional sin competir con bloques secundarios.
  - Los selectores de variantes (talla, color, presentación) deben ser controles semánticos (`<button>`, `<input type="radio">` + `<label>` o `<select>`) con estado seleccionado explícito (`aria-checked` / `aria-pressed`), estado agotado/deshabilitado distinguible y área táctil suficiente.
- **Listados, tarjetas de producto y productos relacionados:**
  - Las tarjetas deben usar `<a href>` real para navegar al producto (soportando Cmd/Ctrl+clic y clic central) y `<button>` para acciones rápidas, evitando `<div onClick>`.
  - Todas las imágenes `<img>` requieren `width` y `height` explícitos para evitar CLS; `loading="lazy"` bajo el pliegue y `fetchpriority="high"` en la imagen principal sobre el pliegue.
- **Carrito, drawers, barras de progreso y bloques promocionales:**
  - Modales, drawers y hojas laterales de carrito deben incluir `overscroll-behavior: contain` para evitar encadenamiento de scroll al fondo y no deben tapar el elemento enfocado.
  - Las acciones destructivas (vaciar carrito, eliminar dirección guardada) requieren confirmación o ventana de deshacer (`undo`).
  - Las barras de progreso (envío gratis, pasos de checkout) y actualizaciones asíncronas (toasts de carrito, validación de cupones) deben anunciar cambios con `aria-live="polite"`.

### 3.3 Estados Interactivos, Foco, Formularios y Animación (`interactive-states`)
- **Semántica e interacción:** `<button>` para acciones y `<a>`/`<Link>` para navegación (prohibido `<div onClick>` o `<span onClick>` sin semántica ni teclado). Los botones de solo icono requieren `aria-label`; los iconos decorativos requieren `aria-hidden="true"`.
- **Estados de foco y hover:**
  - Todo elemento interactivo necesita foco visible (`:focus-visible` / `focus-visible:ring-*`) y estado `hover:` con incremento de contraste.
  - **Prohibido** usar `outline: none` o `outline-none` sin reemplazo de foco visible equivalente.
  - Agrupar controles compuestos con `:focus-within` y asegurar que cabeceras/footers `sticky` no oculten el elemento enfocado.
- **Formularios de comercio (búsqueda, contacto, newsletter, dirección, cupón):**
  - Todo control requiere `<label>` clicable (`for`/`htmlFor` o envolvente) o `aria-label`, además de `name` significativo, `autocomplete` apropiado y `type`/`inputmode` correcto (`email`, `tel`, `url`, `number`).
  - **Nunca bloquear el pegado** (`onPaste` con `preventDefault`).
  - El botón de envío permanece habilitado hasta que inicia la solicitud y muestra indicador de carga (`spinner` / estado `loading`) durante la petición.
  - Los errores de validación se muestran inline junto al campo con indicación de cómo corregirlos, enfocando el primer error al enviar.
- **Animación y movimiento:**
  - Respetar siempre `prefers-reduced-motion: reduce`.
  - Animar únicamente `transform` y `opacity`; **nunca usar `transition: all`** (listar propiedades explícitamente).

### 3.4 Responsive, Táctil y Áreas Seguras (`responsive`)
- **Zoom y viewport:** **Prohibido** deshabilitar el zoom del usuario con `user-scalable=no` o `maximum-scale=1`.
- **Toque y gestos:** Usar `touch-action: manipulation` en controles interactivos para evitar retraso por doble toque; cualquier gesto de arrastre/swipe (carruseles, galerías PDP) debe ofrecer alternativa por clic/tap y teclado; evitar `autoFocus` en móvil.
- **Layout y desbordamiento:** Usar Flex/Grid en lugar de mediciones con JS (`getBoundingClientRect`, `offsetWidth` en render); corregir causas reales de overflow horizontal y contemplar `env(safe-area-inset-*)` en barras fijas o layouts full-bleed.

### 3.5 Consistencia Visual y Preservación de Identidad de Marca (`visual-consistency`)
- **Respeto estricto al sistema de diseño existente:**
  - **No cambies arbitrariamente colores, fuentes, paleta, tokens CSS (`--color-*`, `--font-*`), espaciados ni identidad visual de la tienda.**
  - Reutiliza las variables CSS, clases utilitarias, tokens de `settings_schema.json` y componentes nativos existentes del tema.
- **Protección de contratos funcionales y comerciales:**
  - Conserva todos los selectores `js-*`, `data-*`, `data-store`, llamadas `LS.*`, formularios de producto/carrito (`CartForm`, `/cart/add`), lógica de variantes, precios, stock, descuentos, checkout y analítica.
  - **No elimines bloques funcionales del tema** para forzar una estética minimalista ni introduzcas frameworks CSS o librerías UI externas no autorizadas.

---

## 4. Clasificación de Evidencia en 3 Niveles y Herramienta Local

Todo diagnóstico emitido por `web-design-guidelines` separa estrictamente:

1. **`verified_by_tool`**: Evidencia comprobada directamente en el DOM/viewport renderizado o en el árbol de código analizado con certeza estructural (ej. desbordamiento horizontal medido en viewport, botón de icono o input sin nombre accesible en DOM renderizado, meta viewport con `user-scalable=no`, enlace vacío).
2. **`code_hypothesis`**: Patrones o antipatrones detectados en plantillas o componentes (`transition: all`, `outline: none` sin `:focus-visible`, `<div onClick>`, `onPaste` con `preventDefault`, `<img>` sin dimensiones en plantilla, colores hexadecimales hardcodeados cuando el proyecto define tokens CSS) que deben confirmarse en el DOM/CSS compilado.
3. **`requires_external_verification`**: Comprobaciones que requieren navegador real en múltiples viewports, prueba con teclado/lector de pantalla real o validación de contraste sobre imágenes dinámicas cuando solo se dispone de código fuente estático.

### Ejecución del Motor Local de Auditoría de Diseño e Interfaz

```bash
python3 tools/ia.py --project <proyecto> performance design-audit \
  --source-file <ruta-autorizada-1> \
  --framework <shopify-liquid|shopify-hydrogen|remix|nextjs|react-web|tiendanube-ipanema>
```

Cuando exista captura de DOM/viewport renderizado o un informe previo de `web-quality-audit`, pásalos con `--rendered <rendered.json>` y `--quality-report <wqa.json>` para reutilizar las observaciones sin repetir mediciones.
