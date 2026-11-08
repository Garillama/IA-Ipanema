# Métricas y alcance de medición

Fecha: 2026-11-08. Los umbrales de referencia para el percentil 75 de visitas son LCP ≤2.5 s, INP ≤200 ms y CLS ≤0.1; los datos de laboratorio ayudan a diagnosticar, pero no sustituyen mediciones de usuarios reales. [Web Vitals](https://web.dev/articles/vitals).

Después del acceso autorizado se ejecutaron seis Lighthouse de home, categoría y PDP, mobile/desktop, sin redirecciones ni advertencias. Sus métricas son la referencia actual del storefront: [tabla y reportes](storefront-lighthouse-results.md). Las mediciones de password siguientes se conservan como contexto histórico independiente.

## Línea inicial sin acceso

Se ejecutaron Lighthouse 13.6.0 mobile y desktop con perfiles estándar, ambos redirigidos a `/password/`. Estas mediciones pertenecen a esa pantalla y a sus recursos de otra instalación; no caracterizan home ni PDP del checkout auditado.

| Métrica | Mobile, simulado | Desktop, simulado |
|---|---:|---:|
| FCP | 1.463 s | 0.431 s |
| LCP | 4.024 s | 1.063 s |
| CLS | 0 | 0.296 |
| Total Blocking Time | 355 ms | 1 ms |
| Speed Index | 2.005 s | 0.581 s |
| Respuesta servidor auditada | 114 ms | 107 ms |
| Performance / accesibilidad / SEO | 79 / 92 / 75 | 83 / 92 / 75 |

Fuente: [mobile JSON](../13-evidence/measurements/lighthouse/mobile-summary.json), [desktop JSON](../13-evidence/measurements/lighthouse/desktop-summary.json), con informes HTML en el mismo directorio. Una muestra por perfil; no se calculó mediana. Lighthouse advirtió la redirección. El viewport mobile de Lighthouse fue 412×823 DPR 1.75; desktop 1350×940 DPR 1. No confundirlos con la matriz separada de seis anchos.

Las capturas de navegador registran paint, candidatos LCP, layout shifts y long tasks. No se reporta INP: no se midieron interacciones de usuarios reales. TBT tampoco es INP. Las sumas brutas de shifts no equivalen a CLS sin excluir entradas recientes de interacción y aplicar ventanas de sesión. Los registros sin JS no proporcionaron una medida utilizable de esos observers, por lo que no se presentan como cero.

CrUX, Search Console, PageSpeed Insights y WebPageTest no se ejecutaron. No se inventan datos de campo ni cobertura móvil real. Las mediciones adicionales después de desbloquear se documentan en la [matriz QA](../10-quality/testing-matrix.md), manteniendo separada esta línea inicial.
