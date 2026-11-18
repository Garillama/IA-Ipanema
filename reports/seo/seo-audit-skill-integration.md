# Integración Etapa 3 — SEO Audit (`seo-audit`)

Fecha: 2026-11-18  
Estado: **`integrated_and_verified`**  
Rama de trabajo: `feat/seo-audit` (creada desde `feat/web-quality-audit`, commit `827a3a5`)

## 1. Procedencia exacta y análisis de origen (Etapa A)

- **Repositorio original**: `https://github.com/coreyhaines31/marketingskills`
- **Archivo principal**: `skills/seo-audit/SKILL.md` (versión `2.2.5`, `17,785` bytes, SHA1 `b33eecef416f2c5e5e2ae49eeafc3c81f88f445e`)
- **Commit verificado**: `73573e94a06a39965978b3fa1f9c1eace8cebc7c` (`2026-11-18T01:16:03Z`)
- **Licencia**: `MIT`
- **Archivos de referencia auditados en el origen**:
  - `references/ai-writing-detection.md` (SHA1 `cb67ece4135f4153575bbbdfbf722364babff61d`)
  - `references/international-seo.md` (SHA1 `35a7ad2aeadcbef2541563b0077d5f717e4b147d`)
  - `references/local-seo.md` (SHA1 `c2636ada98809d6ed8db588040817adc332add5e`)
  - `references/rankings-push.md` (SHA1 `5e3930e47e521cf3d27db2e7120ffde8ace3035d`)
  - `references/title-tags.md` (SHA1 `5d5eac8002179ac5288f3b4bbd2aa35b3a409a42`)
  - `evals/evals.json` (SHA1 `d569ae70cf4746f7a27e7808abbaea4878c27fd7`)
- **Dependencias nuevas instaladas**: `0` (sin paquetes externos añadidos).

## 2. Reutilización obligatoria y enrutamiento (Sección 3)

- **Ampliación del motor SEO existente sin crear otro motor**:
  - Se amplió [tools/ipanema/seo/page_audit.py](../../tools/ipanema/seo/page_audit.py) con `comprehensive_seo_audit(...)` y `SEO_FRAMEWORK_CANDIDATES`, reutilizando directamente `extract` ([extractor.py](../../tools/ipanema/seo/extractor.py)), `audit_html` / `audit_snapshot`, `Robots` ([robots.py](../../tools/ipanema/seo/robots.py)), `parse_sitemap` ([sitemaps.py](../../tools/ipanema/seo/sitemaps.py)), `Content` / `classify` / `pagination` ([indexability.py](../../tools/ipanema/seo/indexability.py)) e `infer_framework` ([performance/model.py](../../tools/ipanema/performance/model.py)).
  - Puede consumir un reporte previo de `web-quality-audit` (`--quality-report` / `quality_audit_report`) para reutilizar sus hallazgos sin repetir análisis.
- **Enrutamiento diferenciado en [coordinator.py](../../tools/ipanema/coordinator.py)**:
  - Solicitud exclusiva de rendimiento → [cloudflare-web-perf](../../.agents/skills/cloudflare-web-perf/SKILL.md).
  - Auditoría general de calidad web → [web-quality-audit](../../.agents/skills/web-quality-audit/SKILL.md).
  - Auditoría especializada de SEO → [seo-audit](../../.agents/skills/seo-audit/SKILL.md) (junto con [ipanema-seo-expert](../../.agents/skills/ipanema-seo-expert/SKILL.md)).

## 3. Exactitud de resultados y controles de seguridad (Secciones 4 y 5)

1. **Separación en tres niveles de evidencia**:
   - `verified_by_tool`: Problemas comprobados sobre el HTML/DOM capturado, estado HTTP, cadenas de redirección, `robots.txt` o `sitemap.xml`.
   - `code_hypothesis`: Posibles problemas detectados en plantillas o archivos fuente (`layout/theme.liquid`, `app/root.tsx`, `layouts/layout.tpl`, etc.) pendientes de confirmar en tiempo de ejecución.
   - `requires_external_verification`: Hallazgos que requieren Search Console (`SEO-EXT-GOOGLE-INDEXATION-STATUS`, `SEO-EXT-ORGANIC-PERFORMANCE`), rastreo multi-página (`SEO-EXT-HREFLANG-RECIPROCITY`) o captura del DOM renderizado con JavaScript (`SEO-EXT-SCHEMA-RENDERED-DOM`).
2. **Garantías explícitas**:
   - `indexation_claimed: False` (el HTML nunca se interpreta como prueba de indexación en Google).
   - No se afirma ausencia de Schema cuando solo se inspecciona HTML estático sin `--rendered`.
   - `ranking_improvement_promised: False` y `traffic_fabricated: False`.
   - `untrusted_page_data_ignored: True`, redacción de parámetros sensibles (`redact`) y confinamiento `beneath` en `--source-file`.

## 4. Pruebas y verificación (Sección 7)

- Suite unitaria de Etapa 3: [tests/unit/test_seo_audit_skill.py](../../tests/unit/test_seo_audit_skill.py) (14 pruebas obligatorias).
- Suites de Etapas 1 y 2: [tests/unit/test_cloudflare_web_perf.py](../../tests/unit/test_cloudflare_web_perf.py) y [tests/unit/test_web_quality_audit.py](../../tests/unit/test_web_quality_audit.py).
- Suite integral del agente: `python3 tools/ia.py qa --suite quick`.
