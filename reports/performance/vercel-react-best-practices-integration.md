# Integración Etapa 5 — Preflight Conjunto (Etapas 1–4) y Vercel React Best Practices (`vercel-react-best-practices`)

Fecha: 2026-11-18  
Estado: **`integrated_and_verified`**  
Rama de trabajo: `feat/vercel-react-best-practices` (creada desde `feat/schema-markup`, commit `a7f49ff`)

## 1. Resultado del Preflight Conjunto de las 4 Skills (Secciones 1 y 2)

Se ejecutó y verificó la interoperabilidad de las cuatro skills previas antes de integrar la quinta:

| Caso | Solicitud | Skill externa activada | Verificación de aislamiento y motor | Resultado |
|---|---|---|---|---|
| **Caso A — Rendimiento** | `"Analiza el LCP y los scripts que ralentizan una tienda Shopify"` | `cloudflare-web-perf` | No carga `web-quality-audit`, `seo-audit` ni `schema`; usa `diagnose_web_perf` separando campo y laboratorio | `PASSED` |
| **Caso B — Calidad web** | `"Realiza una auditoría integral de calidad de esta página"` | `web-quality-audit` | Reutiliza `cloudflare-web-perf` internamente sin repetir mediciones; prioriza hallazgos | `PASSED` |
| **Caso C — SEO** | `"Audita el SEO técnico de una colección Shopify"` | `seo-audit` | Reutiliza extractores SEO; evalúa metadatos/canonicals/indexabilidad con `indexation_claimed: False` | `PASSED` |
| **Caso D — Datos estructurados** | `"Revisa el JSON-LD de un producto Shopify"` | `schema` | Reutiliza validadores A–D; detecta duplicados y bloquea edición automática de apps externas (`auto_modify_allowed: False`) | `PASSED` |
| **Caso E — Solicitud ambigua** | `"Optimiza mi tienda Shopify"` | Ninguna externa forzada (`ipanema-architect`) | Plan proporcional sin activar las 4 skills indiscriminadamente ni inventar métricas | `PASSED` |
| **Caso F — Seguridad y B1/B2** | Controles de frontera, redacción, rutas y consejo | Catálogo cerrado (`AUTHORIZED_SKILLS`) | `models.json:council` conserva `["claude", "codex"]`, `commandcode` deshabilitado, Antigravity y bloqueos B1/B2 intactos | `PASSED` |

## 2. Procedencia exacta de Vercel React Best Practices (Sección 3)

- **Repositorio original**: `https://github.com/vercel-labs/agent-skills`
- **Directorio**: `skills/react-best-practices`
- **Commit verificado**: `1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62` (`2026-10-27T21:40:02Z`)
- **Licencia**: `MIT` (declarada en frontmatter de `SKILL.md`)
- **Archivos e identificadores SHA1 auditados**:
  - `SKILL.md` (`7,251` bytes, SHA1 `237988de4a66dd8a71d30a2c24ebe1a86b58d04e`)
  - `metadata.json` (`921` bytes, SHA1 `3bec38b176cc71d105895ec4678bbe79305dcb4c`)
  - `README.md` (`3,360` bytes, SHA1 `f283e1c0c21c5b13c848452528c3949ff544846c`)
  - `AGENTS.md` compilado (`108,261` bytes, SHA1 `4e340a50684a8e7811d5bfa4df48bd9989d0fd87`)
  - `rules/` (tree SHA1 `0af4bf7cbb25560321d127d270fd787875b8ea89`)
- **Dependencias nuevas instaladas**: `0` (no se ejecutó `pnpm install` ni `pnpm build`, ni se instalaron paquetes externos como `better-all`, `swr` o `lru-cache`).

## 3. Reglas adaptadas y reglas descartadas por compatibilidad de framework (Sección 4)

- **Reglas universales incorporadas (React, Shopify Hydrogen, Remix, Vite/Webpack, Next.js)**:
  - `async-*` (`CRITICAL`): `async-parallel` (`Promise.all`), `async-cheap-condition-before-await`, `async-defer-await`, `async-suspense-boundaries` (`<Suspense>` + `<Await>`).
  - `bundle-*` (`CRITICAL`): `bundle-barrel-imports` (detección de `lodash`, `moment`, `lucide-react`, `/index`), `bundle-analyzable-paths`, `bundle-conditional`, `bundle-defer-third-party`, `bundle-preload`.
  - `server-*` (`HIGH`): `server-no-shared-module-state` (prevención de fuga de sesión/carrito en variables globales de módulo en SSR), `server-serialization`, `server-parallel-fetching`, `server-auth-actions`.
  - `rerender-*` (`MEDIUM`): `rerender-derived-state-no-effect` (prohibición de `setState` derivado en `useEffect`), `rerender-no-inline-components`, `rerender-lazy-state-init`, `rerender-functional-setstate`, `rerender-dependencies`, `rerender-transitions`, `rerender-use-deferred-value`.
  - `rendering-*`, `client-*`, `js-*`: `rendering-conditional-render` (prevención de fuga del literal `0` con `.length && <JSX>`), `client-passive-event-listeners` (`{ passive: true }`), `js-set-map-lookups` (`Set`/`Map` en vez de `.includes()`/`.find()` O(n²)).
- **Reglas adaptadas o descartadas fuera de Next.js**:
  - `next/dynamic` (`bundle-dynamic-imports`): **Descartado en Hydrogen, Remix y React Vite/Webpack** → Adaptado a `React.lazy(() => import(...))` con `<Suspense>`, y se añade la regla `RBP-FW-INCOMPATIBLE-NEXT-API` para alertar si se importa `next/*` en proyectos no Next.js.
  - `after()` de `next/server` (`server-after-nonblocking`): **Descartado en Hydrogen/Workers** → Adaptado a `context.waitUntil(promise)`.
  - `React.cache()` (`server-cache-react`): **Adaptado en Hydrogen** a `context.storefront.CacheShort()` / `CacheLong()` / `CacheCustom()`.
  - Instalación de `swr` / `better-all` / `lru-cache`: **Descartada la instalación automática** → Se priorizan `useFetcher()` de Remix/Hydrogen y `Promise.all` nativo.
  - **Descartado el archivo compilado `AGENTS.md` de 108 KB**: Para proteger el presupuesto de tokens y no colisionar con el [AGENTS.md](../../AGENTS.md) raíz del repositorio, se sintetizaron las 8 categorías en [.agents/skills/vercel-react-best-practices/SKILL.md](../../.agents/skills/vercel-react-best-practices/SKILL.md).

## 4. Implementación y pruebas (Secciones 5 y 6)

- **Skill**: [.agents/skills/vercel-react-best-practices/SKILL.md](../../.agents/skills/vercel-react-best-practices/SKILL.md).
- **Motor**: `audit_react_best_practices` e `infer_framework` ampliado (`shopify-hydrogen`, `remix`, `nextjs`, `react-web`, `shopify-liquid`, `tiendanube-ipanema`) en [tools/ipanema/performance/model.py](../../tools/ipanema/performance/model.py).
- **CLI**: `python3 tools/ia.py performance react-audit --source-file <archivo> [--framework <fw>] [--perf-report <report.json>]` en [tools/ipanema/performance/cli.py](../../tools/ipanema/performance/cli.py).
- **Suite de pruebas**: [tests/unit/test_vercel_react_best_practices.py](../../tests/unit/test_vercel_react_best_practices.py) (preflight conjunto Casos A–F + 14 pruebas obligatorias).
