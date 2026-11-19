# Etapa 6 — Integración de Vercel Web Design Guidelines (`web-design-guidelines`)

## 1. Procedencia Verificada e Integridad Criptográfica

La sexta skill externa integrada en `IA-Ipanema` proviene de dos repositorios oficiales de Vercel Labs con referencias inmutables verificadas contra `.local/upstream/web-design-guidelines/manifest.json`:

| Artefacto | Repositorio | Commit inmutable | Git blob SHA-1 | SHA-256 | Tamaño | Licencia |
|---|---|---|---|---|---|---|
| `skills/web-design-guidelines/SKILL.md` | `https://github.com/vercel-labs/agent-skills` | `1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62` | `ceae92ab319216a68274168fba9b63b998b65997` | `f4647ca866a3accf763777f83e7682954f0187cd6bea7eea0399796652414e8f` | 1231 bytes | `MIT` |
| `command.md` | `https://github.com/vercel-labs/web-interface-guidelines` | `434b7f91364665f2f733b310ec54809bf8f37937` | `3eb3a212b7b89493922ea418489d4c6f67ae8bd5` | `d246b026f4f29b5823a9cc857f9edf3d2507002e055e32040cadeaf3b38e0234` | 8055 bytes | `MIT` |

### Eliminación de Descarga Dinámica en Tiempo de Ejecución (`WebFetch` a `/main/`)

El `SKILL.md` original de Vercel instruía al agente a consultar en cada revisión la URL mutable `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` mediante `WebFetch`. En cumplimiento estricto de `AGENTS.md` y de la política de seguridad de la Etapa 6:

1. **Sin llamadas externas en runtime**: `dynamic_fetch_enabled = False` y `dynamic_fetch_performed = False`.
2. **Incorporación estática y versionada**: Las reglas del commit inmutable `434b7f91364665f2f733b310ec54809bf8f37937` están incorporadas de forma estática y verificable en [`.agents/skills/web-design-guidelines/SKILL.md`](../../.agents/skills/web-design-guidelines/SKILL.md) y en el motor local `audit_web_design_guidelines` ([`tools/ipanema/performance/model.py`](../../tools/ipanema/performance/model.py)).

---

## 2. Arquitectura de Coexistencia con las 5 Skills Anteriores

| Skill | Dominio Principal | Relación con `web-design-guidelines` |
|---|---|---|
| `cloudflare-web-perf` | Rendimiento web y Core Web Vitals (LCP, CLS, INP, TTFB, FCP, TBT) | `web-design-guidelines` evalúa dimensiones explícitas de imágenes (`width`/`height`), `prefers-reduced-motion` y lecturas síncronas de layout en UI; delega el análisis de cascadas de red y métricas en `cloudflare-web-perf`. |
| `web-quality-audit` | Auditoría integral de calidad web | `web-design-guidelines` puede reutilizar un informe previo de `web-quality-audit` (`--quality-report`) para incorporar hallazgos de accesibilidad e interacción sin duplicar ejecuciones. |
| `seo-audit` | SEO técnico, on-page e internacional | `web-design-guidelines` verifica la jerarquía visual de encabezados (`<h1>`–`<h6>`) y enlaces semánticos `<a href>` sin solapar sitemaps, robots ni canonicals. |
| `schema` | Datos estructurados Schema.org / JSON-LD | Dominio ortogonal; ninguna mejora visual o de interfaz modifica bloques JSON-LD. |
| `vercel-react-best-practices` | Arquitectura React/Hydrogen/Remix/Next.js (waterfalls, bundles, hooks) | `web-design-guidelines` audita la capa de interfaz, estados interactivos, formularios y consistencia visual; `vercel-react-best-practices` optimiza la ejecución de componentes y carga de datos. |

---

## 3. Capacidades del Motor `audit_web_design_guidelines` (`performance design-audit`)

El motor [`audit_web_design_guidelines`](../../tools/ipanema/performance/model.py) evalúa cinco áreas funcionales clave y separa todos los hallazgos en tres niveles de evidencia (`verified_by_tool`, `code_hypothesis`, `requires_external_verification`):

1. **Jerarquía Visual (`visual-hierarchy`)**:
   - Encabezado primario `<h1>` visible y ausencia de saltos en jerarquía (`H1` -> `H3`).
   - Claridad y especificidad de etiquetas de CTA (detección de etiquetas ambiguas como `"Continue"`, `"Continuar"`, `"Submit"`, `"Click"`).
   - Uso de `font-variant-numeric: tabular-nums` en precios, subtotales y comparaciones numéricas.
   - Microcopy tipográfico (`…` frente a `...` en estados de carga y placeholders).
2. **UX de E-commerce (`ecommerce-ux`)**:
   - Controles de formulario y selectores de PDP/carrito con `<label>` clicable o `aria-label`.
   - Imágenes de producto y galería con `width` y `height` explícitos para prevenir CLS.
   - Modales y drawers de carrito con `overscroll-behavior: contain`.
3. **Estados Interactivos (`interactive-states`)**:
   - Prohibición de `outline: none` / `outline-none` sin reemplazo `:focus-visible`.
   - Prohibición de `transition: all` / `transition-all`.
   - Detección de elementos no semánticos `<div onClick>` / `<span onClick>` en lugar de `<button>` o `<a href>`.
   - Botones de solo icono sin `aria-label`.
   - Bloqueo de pegado (`onPaste` con `preventDefault`).
   - Soporte de `@media (prefers-reduced-motion: reduce)` en animaciones.
4. **Responsive y Táctil (`responsive`)**:
   - Detección de desbordamiento horizontal real en viewport (`scrollWidth > innerWidth`).
   - Prohibición de `user-scalable=no` y `maximum-scale=1` en meta viewport.
   - Verificación de tamaño mínimo de área táctil (`44x44px`) en botones y selectores.
   - Detección de `autoFocus` sin restricción desktop y lecturas de layout en render (`getBoundingClientRect`, `offsetWidth`).
5. **Consistencia Visual y Protección de Marca/Comercio (`visual-consistency`)**:
   - Inventario automático de tokens CSS del sistema de diseño (`--color-*`, `--font-*`, `--space-*`, `--radius-*`) y detección de colores hexadecimales hardcodeados que ignoran tokens existentes.
   - Inventario y protección explícita de contratos comerciales (`js-*`, `data-store`, `LS.*`, `CartForm`, `cartLinesAdd`, `/cart/add`, `checkoutUrl`).

### Uso desde CLI

```bash
python3 tools/ia.py --project ipanema performance design-audit \
  --source-file ruta/al/componente.liquid \
  --framework shopify-liquid
```
