# Etapa 7 — Integración de Better Accessibility (`better-accessibility`)

## 1. Procedencia Verificada e Integridad Criptográfica

La séptima skill integrada en `IA-Ipanema` procede del repositorio oficial `https://github.com/jakubkrehel/skills`, en el directorio `skills/better-accessibility/` del commit inmutable `547d415dc10a23e66088eba5aa6664e6e772432c` bajo licencia `MIT`. Los nueve archivos originales alojados en `.local/upstream/better-accessibility/` fueron verificados dentro del sandbox (`BypassSandbox: false`) mediante hash de objeto Git (`blob <len>\0<content>`) y `SHA-256`:

| Archivo | Git blob SHA-1 | SHA-256 | Bytes |
|---|---|---|---|
| `SKILL.md` | `b5293ecc20e4356a50a55e1a1eadd3db9a0019a7` | `6a6465c044783968bae9896fd9e2e78437b90578fe3309b6dee6ef6a920e45f9` | 10452 |
| `agents/openai.yaml` | `36b942fb8e5b86916b006c2fe4e07fdbde24a112` | `98699206d4fb00b72bcaf69bb446f541644cc0cc3d23967e266731e100a55563` | 121 |
| `focus-and-keyboard.md` | `361ad8e51c83249d9dc16a97b4ae01883de08131` | `ace66413242a31df97f1d5101bddc98d871c97716cbc936a439291ea5fda7e54` | 6356 |
| `forms.md` | `8f960cbb59f6dfd27cb47f6a962198659ff66dcd` | `ed63f7424eb1d3515e4261504467d77840317dda7c0df86c965ee334b3499589` | 3628 |
| `hit-areas.md` | `9f9aa538683a0ba68b6164a8508164dd6109ca42` | `c723a5c5a0935148dbf54dcc1b9fa140251f50a6e953ed79f77af498eae3b615` | 3385 |
| `motion-and-zoom.md` | `e184315a5060f86107d4fb2951e884bf697cc399` | `743bae6a93843ff07ebb283d8de31e3ecd184e04f8de639b0e3b0949088fc13a` | 2055 |
| `reporting.md` | `46d221bad48a6e0992d13377a285ed6f9002f794` | `6203f74162d308d844bd6db8b677502757da922b274ef72cacdba63819073659` | 1174 |
| `screen-readers.md` | `7da1b74995ee8bb6374e2aa17e694e7d55dc21bd` | `a65faa6f28ef972b72bcaf69bb446f541644cc0cc3d23967e266731e100a55563` | 4450 |
| `semantics-and-aria.md` | `24ab05c1d7fbdbd5900b5e7758bae23d06e91866` | `dfbadab983f65cd5f666ee4e1aecdf9a243ea206876a3f575a12f0b1314f6e37` | 4380 |

- **Dependencias nuevas**: Ninguna (cero paquetes `npm` o `pip` añadidos; implementación en Python puro estándar).
- **Scripts externos ejecutados**: Ninguno; `agents/openai.yaml` y las guías originales se trataron exclusivamente como datos de origen no confiables.
- **Riesgos identificados y mitigados**:
  - Falsos positivos por confundir preferencias de diseño o heurísticas AAA (objetivo táctil de 44×44px, único `<h1>`) con incumplimientos WCAG 2.2 AA (`24×24px` para 2.5.8). Mitigado mediante separación explícita entre `wcag_violation` y `best_practice_recommendation`.
  - Falsas certificaciones de accesibilidad total basadas en análisis estático. Mitigado mediante `static_certification_claimed = False` y entradas obligatorias en `requires_external_verification` para recorrido real por teclado, lector de pantalla y contraste computado.
  - Ruptura de selectores de carrito, variantes o identidad visual. Mitigado mediante `brand_and_commerce_guards` en evaluación y correcciones mínimas (`propose_safe_accessibility_fixes`).

---

## 2. Complementariedad y Enrutamiento entre las 7 Skills

| Dominio | Skill Integrada | Rol y Coordinación |
|---|---|---|
| Rendimiento y CWV | `cloudflare-web-perf` | Métricas de laboratorio y campo, red e imágenes. |
| Calidad web general | `web-quality-audit` | Evaluación global multi-categoría; `better-accessibility` reutiliza sus hallazgos si existe informe previo. |
| SEO técnico | `seo-audit` | Rastreo, canonicals, sitemaps y metadatos. |
| Datos estructurados | `schema` | JSON-LD / Schema.org y microdata. |
| React / Hydrogen / Remix / Next | `vercel-react-best-practices` | Waterfalls, bundles y re-renders. |
| UI/UX y diseño visual | `web-design-guidelines` | Jerarquía visual, UX y consistencia; delega en `better-accessibility` (`delegated_accessibility`) al detectar señales de accesibilidad. |
| **Accesibilidad WCAG 2.2 A/AA** | **`better-accessibility`** | Especialista en semántica HTML, teclado, gestión del foco, ARIA, lectores de pantalla, formularios, live regions, modales/drawers, movimiento reducido, áreas táctiles 24px/44px, zoom/reflow y contraste medible. |

---

## 3. Capacidades Técnicas, Adaptación E-commerce y Evidencia

El motor [`tools/ipanema/performance/accessibility.py`](../../tools/ipanema/performance/accessibility.py) (reexportado por [`tools/ipanema/performance/model.py`](../../tools/ipanema/performance/model.py) y expuesto en CLI como `performance accessibility-audit`) soporta:

- **Superficies E-commerce reconocidas**: Shopify PDP (`/cart/add`, `product-form`), selectores de variantes, `cart-drawer`, menús móviles, buscadores, formularios de contacto/newsletter, filtros de colecciones, carruseles, modales/diálogos, estados de disponibilidad y mensajes de error.
- **Separación estricta de evidencia**:
  - `verified_by_tool`: fallos y mediciones confirmadas en DOM renderizado, árbol de accesibilidad, viewport y pares medibles `fg`/`bg` (`contrast_ratio`).
  - `code_hypothesis`: hallazgos en código fuente con `location` (`file:line`), `element`, `wcag_criterion`, `wcag_level`, `impact`, `evidence`, `recommendation` y `required_verification`.
  - `best_practice_recommendation`: recomendaciones ergonómicas/heurísticas (44×44px, outline único `<h1>`, `disabled={!isValid}` en submit, `role` redundante) nunca etiquetadas como `wcag_violation` ni severidad `HIGH`.
  - `requires_external_verification`: contraste computado (cuando no se aportan pares medibles) y recorridos manuales reales de teclado + lector de pantalla (NVDA / VoiceOver).

### Uso CLI

```bash
python3 tools/ia.py --project ipanema performance accessibility-audit \
  --source-file ruta/al/componente.liquid \
  --framework shopify-liquid \
  --propose-fixes
```
