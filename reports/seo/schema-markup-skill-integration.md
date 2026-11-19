# Integración Etapa 4 — Schema Markup (`schema`)

Fecha: 2026-11-18  
Estado: **`integrated_and_verified`**  
Rama de trabajo: `feat/schema-markup` (creada desde `feat/seo-audit`, commit `80a9e08`)

## 1. Procedencia exacta y análisis de origen (Sección 7)

- **Repositorio original**: `https://github.com/coreyhaines31/marketingskills`
- **Archivo principal**: `skills/schema/SKILL.md` (versión `2.0.5`, `6,914` bytes, SHA1 `a152e5e59496740caf18ba0f0c74f4ef0e383c39`)
- **Commit verificado**: `73573e94a06a39965978b3fa1f9c1eace8cebc7c` (`2026-11-18T01:16:03Z`)
- **Licencia**: `MIT`
- **Archivos de referencia auditados en el origen**:
  - `references/schema-examples.md` (`9,298` bytes, SHA1 `014b5292ce46184a5cde223d3a528b3e48397b8f`)
  - `evals/evals.json` (`9,815` bytes, SHA1 `c679cb253c26f81166b068b4e52cf04acd0cb093`)
- **Dependencias nuevas instaladas**: `0` (sin paquetes externos ni ejecución de scripts remotos).

## 2. Reutilización del motor SEO y enrutamiento bajo demanda (Sección 5)

- **Ampliación del motor de datos estructurados existente**:
  - Se amplió [tools/ipanema/seo/schema_validator.py](../../tools/ipanema/seo/schema_validator.py) con `audit_and_propose_schema(...)`, `SCHEMA_FRAMEWORK_CANDIDATES`, `EXTERNAL_APP_MARKERS` y `RETIRED_GOOGLE_FEATURES`, reutilizando directamente `extract` ([extractor.py](../../tools/ipanema/seo/extractor.py)), `validate`, `build_graph` ([schema_graph.py](../../tools/ipanema/seo/schema_graph.py)), `check_consistency` ([consistency.py](../../tools/ipanema/seo/consistency.py)), `generate` / `repair_trailing_json` / `checked_facts` ([generator.py](../../tools/ipanema/seo/generator.py)) e `infer_framework` ([performance/model.py](../../tools/ipanema/performance/model.py)).
- **Enrutamiento diferenciado en [coordinator.py](../../tools/ipanema/coordinator.py)**:
  - Rendimiento exclusivamente → [cloudflare-web-perf](../../.agents/skills/cloudflare-web-perf/SKILL.md).
  - Calidad web general → [web-quality-audit](../../.agents/skills/web-quality-audit/SKILL.md).
  - Auditoría SEO general → [seo-audit](../../.agents/skills/seo-audit/SKILL.md).
  - Datos estructurados / JSON-LD / Schema.org → [schema](../../.agents/skills/schema/SKILL.md) (junto con [ipanema-seo-expert](../../.agents/skills/ipanema-seo-expert/SKILL.md)), sin activar innecesariamente otras skills ni confundirse con el `{% schema %}` del editor de secciones.

## 3. Adaptación para Shopify, 5 dimensiones de validación y 3 niveles de evidencia (Secciones 4, 6 y 8)

1. **Detección de procedencia de Schema en Shopify, Hydrogen, React y Tiendanube**:
   - Identifica bloques procedentes de plantillas/secciones del tema (`theme_or_template`), inyección por JS en cliente (`client_js_injected`) y aplicaciones SEO/reseñas externas (`external_seo_app`: `Judge.me`, `Loox`, `Yotpo`, `Stamped`, `Smart SEO`, `JSON-LD for SEO`, `Yoast`, `Avada`) marcando `auto_modify_allowed: False` para evitar eliminar o sobrescribir bloques de apps externas sin autorización.
   - Analiza plantillas fuente (`source_files`) para detectar `{{ product | structured_data }}`, `metafields.*`, objetos Liquid (`product.selected_or_first_available_variant`) y componentes Hydrogen (`<Seo />`, `getSeoMeta`, `storefront.query`).
2. **Cinco dimensiones de validación explícitas (`validation_dimensions`)**:
   - `syntactic_validity` (Nivel A)
   - `semantic_validity` (Nivel B, incluyendo `Product`, `ProductGroup`, `Offer`, `AggregateOffer`, `AggregateRating`, `Review`, `Brand`, `MerchantReturnPolicy`, `OfferShippingDetails`, `Organization`, `WebSite`, `BreadcrumbList`, `Article`, `BlogPosting` y `LocalBusiness`)
   - `visible_and_fact_consistency` (Nivel D: H1, canonical, imagen, SKU, precio, moneda y disponibilidad contra HTML visible y `facts`)
   - `documented_google_eligibility` (Nivel C + aviso explícito de funciones retiradas por Google: `FAQPage` retirado el `2026-05-07`, `HowTo` en `2023-09`, `SearchAction` sitelinks searchbox en `2024-11`)
   - `search_console_real_result` (`requires_external_verification`)
3. **Tres niveles de evidencia**:
   - `verified_by_tool`: Errores sintácticos/semánticos, duplicados (`G001`), contradicciones (`G002`), discrepancias comerciales (`D020`, `D040`), `AggregateOffer` con rango invertido, `LocalBusiness` sin `address` y propiedades con placeholders o sin fuente de reseñas/políticas (`D080`, `D090`, `SCHEMA-UNBACKED-PLACEHOLDER`).
   - `code_hypothesis`: Duplicación entre `{{ product | structured_data }}` y `Product` manual, `ratingValue` o `InStock` hardcodeados en plantilla, e interpolación Liquid sin filtro `| json`.
   - `requires_external_verification`: Necesidad de DOM renderizado cuando el HTML estático no contiene JSON-LD (`SCHEMA-EXT-RENDERED-DOM-REQUIRED`), propiedad de bloques de apps externas (`SCHEMA-EXT-APP-OWNERSHIP`) y validación en Rich Results Test / Search Console (`SCHEMA-EXT-GOOGLE-RRT-AND-GSC`).

## 4. Pruebas y verificación (Secciones 9 y 11)

- Suite unitaria de Etapa 4: [tests/unit/test_schema_markup_skill.py](../../tests/unit/test_schema_markup_skill.py) (18 pruebas obligatorias + prueba funcional de la Sección 11).
- Suite integral del agente: `python3 tools/ia.py qa --suite quick`.
