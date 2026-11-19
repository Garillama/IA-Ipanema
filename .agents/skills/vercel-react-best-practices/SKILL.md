---
name: vercel-react-best-practices
description: Optimizar componentes React, Shopify Hydrogen, Remix, Vite/Webpack y Next.js eliminando waterfalls, reduciendo bundles, evitando re-renderizados innecesarios y mejorando SSR/hidratación con reglas adaptadas por framework.
---

# Vercel React Best Practices (`vercel-react-best-practices`)

Guía estructurada de optimización de código y arquitectura para aplicaciones React, Shopify Hydrogen, Remix, React con Vite/Webpack y Next.js. Integra y adapta la especificación oficial de Vercel Engineering (`https://github.com/vercel-labs/agent-skills`, `skills/react-best-practices/SKILL.md`, versión `1.0.0`, commit `1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62` del `2026-10-27T21:40:02Z`, `SKILL.md` SHA1 `237988de4a66dd8a71d30a2c24ebe1a86b58d04e`, `metadata.json` SHA1 `3bec38b176cc71d105895ec4678bbe79305dcb4c`, `README.md` SHA1 `f283e1c0c21c5b13c848452528c3949ff544846c`, `AGENTS.md` compilado SHA1 `4e340a50684a8e7811d5bfa4df48bd9989d0fd87`, licencia `MIT`) bajo las reglas de seguridad, permisos y evidencia de [AGENTS.md](../../../AGENTS.md).

## Coordinación y separación de responsabilidades

Esta skill se coordina con [ipanema-storefront](../ipanema-storefront/SKILL.md) y el motor de rendimiento en [model.py](../../../tools/ipanema/performance/model.py):

- **Rendimiento web medido (LCP, CLS, INP, TTFB, FCP, TBT, red)** → [cloudflare-web-perf](../cloudflare-web-perf/SKILL.md).
- **Calidad web integral** → [web-quality-audit](../web-quality-audit/SKILL.md).
- **SEO técnico y on-page** → [seo-audit](../seo-audit/SKILL.md).
- **Datos estructurados JSON-LD** → [schema](../schema/SKILL.md).
- **Patrones de código React / Hydrogen / Remix / Next.js** → `vercel-react-best-practices`.

Cuando una tarea combina medición de rendimiento web y optimización de código React/Hydrogen, `vercel-react-best-practices` consume la evidencia medida por `cloudflare-web-perf` (`--perf-report`) sin repetir trazas ni auditorías Lighthouse. **Nunca actives ni apliques esta skill a proyectos Shopify Liquid o Tiendanube/Ipanema que no utilicen React.**

## Protección funcional y de seguridad

1. **Preservar reglas de negocio y comercio**: Ninguna optimización (como caché de servidor, `startTransition`, `useDeferredValue`, memoización o carga diferida) debe alterar el comportamiento del carrito (`CartForm`, `cartLinesAdd`, `cartLinesUpdate`), precios dinámicos por variante, flujo de checkout, autenticación (`customerAccessToken`) o estado de sesión (`session.commit()`).
2. **Prohibido compartir estado mutable a nivel de módulo en SSR (`server-no-shared-module-state`)**: Nunca almacenes tokens, carritos o datos de usuario en variables globales de módulo en Hydrogen, Remix o Next.js, ya que provoca fugas de datos entre solicitudes concurrentes.
3. **Sin instalación automática de paquetes**: No instales librerías externas (`swr`, `better-all`, `lru-cache`) sin autorización explícita de Nivel 2. Prefiere siempre primitivas nativas de la plataforma (`Promise.all`, `useFetcher` de Remix/Hydrogen, `CacheShort`/`CacheLong` de Storefront API, `React.lazy` + `<Suspense>`).

## Categorías de reglas por prioridad de impacto

| Prioridad | Categoría | Impacto | Prefijo |
|---|---|---|---|
| 1 | Eliminación de Waterfalls (Carga secuencial) | `CRITICAL` | `async-` |
| 2 | Optimización de Tamaño de Bundle | `CRITICAL` | `bundle-` |
| 3 | Rendimiento del Servidor (SSR / Loaders / RSC) | `HIGH` | `server-` |
| 4 | Fetching de Datos y Eventos en Cliente | `MEDIUM-HIGH` | `client-` |
| 5 | Optimización de Re-renderizados | `MEDIUM` | `rerender-` |
| 6 | Rendimiento de Renderizado e Hidratación | `MEDIUM` | `rendering-` |
| 7 | Rendimiento de JavaScript | `LOW-MEDIUM` | `js-` |
| 8 | Patrones Avanzados de Hooks y Refs | `LOW` | `advanced-` |

## Adaptación de reglas por framework (Hydrogen / Remix / React vs. Next.js)

**Prohibido aplicar APIs exclusivas de Next.js a proyectos Shopify Hydrogen, Remix o React (Vite/Webpack).** Verifica siempre el framework detectado antes de proponer código:

| Regla / Objetivo | En Next.js (`nextjs`) | En Shopify Hydrogen (`shopify-hydrogen`) / Remix (`remix`) / React (`react-web`) |
|---|---|---|
| `bundle-dynamic-imports` (Carga diferida de componentes pesados) | `import dynamic from 'next/dynamic'` | **Descartar `next/dynamic`** → Usar `React.lazy(() => import('./Component'))` dentro de `<Suspense fallback={...}>` |
| `async-suspense-boundaries` (Streaming de datos no críticos) | React Server Components con `<Suspense>` | Retornar promesas no bloqueantes en `loader` (`defer({...})`) y renderizar con `<Suspense><Await resolve={...}>` |
| `server-after-nonblocking` (Trabajo post-respuesta no bloqueante) | `after()` de `next/server` | **Descartar `next/server`** → Usar `context.waitUntil(promise)` del runtime Oxygen/Workers en Hydrogen |
| `server-cache-react` / `server-cache-lru` (Caché de consultas en servidor) | `React.cache()` / caché de fetch | En Hydrogen usar `context.storefront.query(QUERY, { cache: context.storefront.CacheLong() \| CacheShort() })` y cabeceras `Cache-Control` del `loader` |
| `client-swr-dedup` (Deduplicación de peticiones en cliente) | `useSWR` (si ya está instalado) | Reutilizar `useFetcher()` y revalidación nativa de Remix/Hydrogen sin instalar `swr` |

## Reglas prioritarias de inspección y refactorización

### 1. Eliminación de Waterfalls (`async-*`, CRITICAL)
- **`async-parallel`**: Detectar `await` secuenciales independientes en `loader`, `action` o funciones asíncronas (`const a = await fetchA(); const b = await fetchB();`) y paralelizarlos con `const [a, b] = await Promise.all([fetchA(), fetchB()])`.
- **`async-cheap-condition-before-await` y `async-defer-await`**: Evaluar guardas síncronas o validaciones de parámetros antes de ejecutar consultas remotas, y mover el `await` únicamente a la rama condicional que lo necesita.
- **`async-suspense-boundaries`**: En Hydrogen/Remix, esperar (`await`) en el `loader` únicamente los datos críticos above-the-fold (producto principal, SEO, precio) y diferir datos secundarios (reseñas, productos recomendados) con `<Suspense>` + `<Await>`.

### 2. Optimización de Bundle (`bundle-*`, CRITICAL)
- **`bundle-barrel-imports`**: Evitar archivos barril (`index.ts` que reexportan decenas de componentes) e importaciones completas de bibliotecas (`import _ from 'lodash'`, `import * as Icons from 'lucide-react'`). Importar directamente submódulos específicos.
- **`bundle-dynamic-imports` y `bundle-conditional`**: Cargar modales, visores 3D, gráficos o editores pesados solo cuando el usuario interactúa, usando `React.lazy` (o `next/dynamic` únicamente en Next.js).
- **`bundle-defer-third-party`**: Posponer scripts de terceros no esenciales (analítica, widgets de chat, mapas) para después de la hidratación.
- **`bundle-preload`**: Pre-cargar chunks pesados en `onMouseEnter` / `onFocus` del botón que los abre.

### 3. Rendimiento del Servidor (`server-*`, HIGH)
- **`server-no-shared-module-state`**: Detectar y eliminar cualquier variable global mutable a nivel de módulo que almacene datos de request, sesión o carrito.
- **`server-serialization`**: En `loader` de Hydrogen/Remix o RSC, seleccionar en GraphQL y retornar al cliente solo los campos utilizados por la vista, reduciendo el tamaño del payload de hidratación (`window.__remixContext`).
- **`server-auth-actions`**: Verificar permisos, sesión y CSRF en toda `action` de Remix/Hydrogen o Server Action.

### 4. Optimización de Re-renderizados (`rerender-*`, MEDIUM)
- **`rerender-derived-state-no-effect`**: Prohibido usar `useEffect(() => { setDerived( compute(prop) ); }, [prop])`. Calcular el valor derivado directamente durante el renderizado (`const derived = useMemo(() => compute(prop), [prop])` o expresión directa).
- **`rerender-no-inline-components`**: Nunca declarar componentes (`function SubComponent()` o `const SubComponent = () => ...`) dentro del cuerpo de otro componente, ya que recrea la referencia en cada render, desmonta el DOM y destruye el estado y el foco.
- **`rerender-lazy-state-init`**: Para inicializaciones costosas (`JSON.parse`, `localStorage`), pasar una función a `useState(() => expensiveInit())`.
- **`rerender-functional-setstate` y `rerender-dependencies`**: Usar actualizaciones funcionales `setCount(c => c + 1)` para estabilizar callbacks y usar dependencias primitivas en `useEffect`/`useMemo`.
- **`rerender-transitions` y `rerender-use-deferred-value`**: En filtros de catálogo o búsquedas en vivo no críticas, usar `startTransition` o `useDeferredValue` para mantener la entrada de teclado fluida (mejorando INP), sin aplicarlo a acciones críticas de pago o checkout.

### 5. Renderizado, Hidratación y JavaScript (`rendering-*`, `client-*`, `js-*`)
- **`rendering-conditional-render`**: Evitar `count && <Component />` con números que pueden valer `0` (imprime `"0"` en el DOM); usar `count > 0 ? <Component /> : null`.
- **`client-passive-event-listeners`**: Añadir `{ passive: true }` en listeners de `scroll`, `touchstart` y `wheel`.
- **`js-set-map-lookups`**: Reemplazar búsquedas repetidas `.includes()` o `.find()` dentro de `.map()`/`.filter()` (complejidad `O(n²)`) por un `Set` o `Map` precalculado (`O(1)`).
- **`js-hoist-regexp`**: Declarar expresiones regulares constantes fuera de bucles y funciones de render.

## Comando CLI del agente

```bash
python3 tools/ia.py performance react-audit --source-file app/routes/products.\$handle.tsx --framework shopify-hydrogen
python3 tools/ia.py performance react-audit --source-file src/App.tsx --framework react-web --perf-report report.json
```

## Formato de entrega

1. **Framework y Alcance Detectado**: Plataforma (`shopify-hydrogen`, `remix`, `nextjs`, `react-web`), archivos inspeccionados y compatibilidad verificada.
2. **Hallazgos de Código Priorizados (`code_hypothesis` y `verified_by_tool`)**: Regla (`async-parallel`, `bundle-barrel-imports`, `rerender-no-inline-components`, etc.), prioridad (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`), archivo/línea y corrección compatible con el framework.
3. **Garantías de Seguridad Funcional**: Confirmación de que carrito, checkout, precios, autenticación y sesión permanecen intactos.
4. **Evidencia de Rendimiento Relacionada**: Correlación opcional con métricas medidas por `cloudflare-web-perf` (`LCP`, `INP`, `TBT`, tamaño de bundles) cuando esté disponible.
