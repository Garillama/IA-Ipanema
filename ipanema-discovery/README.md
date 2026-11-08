# Ipanema Engineering Knowledge Base

Verificación: **2026-11-08**. Proyecto fuente: `/home/alanrichard/orca/workspaces/scentperfumesclaude/merganser`. Este discovery conserva la implementación existente.

Empieza por el [resumen ejecutivo](00-executive-summary.md), los [hallazgos priorizados](11-opportunities/critical-findings.md) y el [informe de cobertura](DISCOVERY-COMPLETENESS-REPORT.md). El inventario no equivale a certificación del funcionamiento de todos los componentes.

| Necesidad | Fuente principal |
|---|---|
| Entender renderizado y límites | [Arquitectura](01-architecture/system-overview.md) |
| Encontrar secciones, bloques y partials | [Inventario](02-native-components/component-inventory.md) y [fichas](02-native-components/component-specifications.md) |
| Buscar un setting, default o condición | [Matriz de controles](02-native-components/settings-matrix.md) |
| Diseñar desktop y mobile sin duplicación | [Responsive](03-editor/responsive-controls.md) |
| SEO de catálogo y carruseles | [SEO técnico](04-seo/technical-seo.md), [carruseles](04-seo/carousel-seo.md) |
| Evitar descargas y saltos visuales | [Imágenes](05-performance/image-loading.md), [carga estable](05-performance/loading-stability.md) |
| Animar sin bloquear la tienda | [Motion](06-motion/animation-principles.md) |
| Reutilizar comercio | [Tarjetas](07-commerce/product-cards.md), [PDP](07-commerce/product-detail.md), [carrito](07-commerce/cart.md) |
| Mantener varias tiendas | [Arquitectura reutilizable](08-design-system/component-architecture.md) y [distribución](08-design-system/multi-store-strategy.md) |
| API, SDK y eventos | [Integraciones](09-integrations/official-apis.md) y [contratos encontrados](09-integrations/events-and-hooks.md) |
| Revisar calidad y alcance real | [Matriz QA](10-quality/testing-matrix.md), [páginas](10-quality/page-audit.md) |
| Trabajar día a día | [Playbook de secciones](12-playbooks/build-new-section.md) y [checklist](12-playbooks/performance-checklist.md) |
| Revisar las pruebas | [Registro de evidencia](13-evidence/evidence-register.md), [referencias](13-evidence/references.md) |
| Resolver decisiones pendientes | [Preguntas al propietario](14-questions/questions-for-owner.md) |

**Confirmado** significa observado en una fuente indicada. **Inferido** identifica una consecuencia plausible todavía sin reproducción. **No comprobado** significa que falta una prueba. **No disponible** señala una propiedad ausente en el ámbito inspeccionado o un recurso inaccesible; no demuestra que no exista en toda Tiendanube.

Los documentos descriptivos contienen conclusiones de ingeniería. Las fichas e índices generados son una extracción estática trazable y deliberadamente conservadora. Los enlaces al código apuntan al origen; sus hashes permiten detectar si cambiaron. Las propuestas no son funcionalidades implementadas ni resultados medidos.
