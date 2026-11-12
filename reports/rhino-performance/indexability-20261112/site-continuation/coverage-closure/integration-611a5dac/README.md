# Integración autorizada SEO Crawler V4 — QA posterior

12 noviembre 2026. **Integración local completada y verificada** en IA-Ipanema. Se aplicó únicamente el parche autorizado SHA256 `611a5dac1e2767c0d331e42b06c60834e8a427c8bbc41671b9a81a8c977f3e2c`. Siete modificaciones, cuatro altas, ninguna eliminación. No hubo cambios al tema, orquestador, modelos o AGENTS.md, ni solicitudes a Rhino o Google.

## Controles previos y aplicación

Coincidieron el hash del parche, las siete preimágenes, la ausencia de cuatro altas y el respaldo previamente aprobado. No había cambios ajenos en el alcance. Se comprobó que el payload contenía exclusivamente los11 archivos y se ejecutó git apply --check antes de git apply, sin force ni sincronización global. Se realizó además un respaldo propio de las siete preimágenes, verificado por SHA256.

Después de aplicar y de ejecutar QA, los11 hashes siguen coincidiendo exactamente con el manifiesto autorizado. Los demás archivos versionados conservaron sus hashes durante la operación y el QA; la documentación de esta entrega se genera separadamente después de esa comprobación. No se descartaron cambios ajenos existentes en otros informes.

[Preflight](preflight.json) · [aplicación](application.json) · [hashes completos y respaldo](hashes.json) · [parche y manifiesto revisados](../final-candidate/README.md).

## Archivos integrados

| Archivo | SHA256 posterior |
|---|---|
| `tests/unit/test_seo_final_conditions_v4.py` | `524eaee578333857c3d6c88a48180b7e65f5df6719e17009140a25a7c319fcbf` |
| `tests/unit/test_seo_regression_v4.py` | `82647acd866d7a286238b39f1771be6c848ad9fe671a541d3833a924d2f7bbe0` |
| `tests/unit/test_seo_review_additional_v4.py` | `f803cc48ddd33e34184e10b62d3ade078975d51b16f2ba81ba630b7317af647e` |
| `tests/unit/test_seo_robots_sources_v4.py` | `7a85a2ff7e7de2daa8725dcf97f7384dc6cda4903aa6659cde70ccd3a10b690b` |
| `tests/unit/test_seo_robots_values_v4.py` | `6dd1dac3206bf5113f437e69209dbaf5c32a5b6015158e90d5cd8fb4bfdee1cb` |
| `tools/ipanema/seo/crawl_policy.py` | `c719ba73adb1e54141cbb04dbbc0b0a6b56407fbb1459d6f4814b23718e526c1` |
| `tools/ipanema/seo/crawler.py` | `29b42a929132bd5bb5ec07770a247dbd5b42a35747874f711617f5ff204d2e5b` |
| `tools/ipanema/seo/indexability.py` | `6f4f34d2ded8af574b3822e74e9b795a5a74b41a3f7bfd16f4b6009c981cddd1` |
| `tools/ipanema/seo/page_audit.py` | `a6b10451443aac8ea222eb0fcf8cdae673e21014b31d7431452b8fe669db6f34` |
| `tools/ipanema/seo/regression.py` | `0bf7eca8c50b906fa083f4422af7863f6a37bad7519e1dbd8349cac3a07b257e` |
| `tools/ipanema/seo/robots.py` | `57d01f9086dffa7f25f26b59976098770d585731eca3d758ee9235000399a3df` |

Los siete hashes previos y la ausencia esperada de las cuatro altas están registrados en hashes.json. El parche anterior 7a5a7066… y todos los artefactos de revisión permanecen intactos.

## QA sobre el motor integrado

| Comprobación | Resultado |
|---|---|
| Unitarias SEO | **191 aprobadas**, incluida la cobertura nueva de las tres reservas |
| Integración SEO | **13 aprobadas** |
| QA quick | **passed**: repositorio, unitarias, integración, evaluaciones del coordinador/SEO y estabilidad de fuentes |
| Hashes posteriores | **11/11 coinciden** tras QA |
| Gate robots limpio | passed únicamente en :noindex; no afirma indexación |
| Evidencia ausente o malformada | unknown |
| Aparición de noindex válido desde baseline desconocido | failed |
| Presupuesto excedido | processing_complete=false; control unknown, sin falso aprobado |
| Cola restrictiva tras200.000 parámetros | noindex conservado;200.000 parámetros procesados;retención truncada explícita |
| Objeto de evidencia de esa entrada |1588bytes;por debajo de65.536bytes;no se confunde con el informe completo |
| Contrato del helper | cuerpo AST histórico idéntico salvo docstring;fixtures exactos aprobados |
| audit_snapshot + compare con adaptador que lanzaría excepción | cero llamadas al adaptador;consumidores conocidos sin regresión observada |

[191 unitarias](seo-unit.json) · [13 integraciones](seo-integration.json) · [quick](qa-quick.json) · [controles adicionales del controlador](controller-integrated-checks.json).

El QA se ejecutó con fixtures sobre el workspace integrado. No es validación de producción, indexación en Google, certificado de seguridad ni compatibilidad universal con consumidores externos/dinámicos. El TLS local anterior no se volvió a ejecutar: el transporte conserva el hash revisado y sus tests de regresión pasaron. No hubo nuevas consultas de cuentas ni red hacia storefront/Google.

## Incidencias y reversión

No se detectaron regresiones en las pruebas ejecutadas. No fue necesario restaurar archivos ni retirar altas. La reversión autorizada se mantiene limitada a los11 archivos y exige hashes posteriores intactos; ante cambios ajenos debe detenerse. Los respaldos no se eliminaron.

La aprobación independiente anterior de Claude y Codex correspondía a estos mismos hashes; no se repitió el consejo ni se simularon revisiones nuevas. El controlador ejecutó y conservó el QA posterior requerido. El ADR histórico conserva el estado que tenía antes de la autorización; status.json registra la autorización específica y la integración realmente ejecutada.

## Estado y siguiente etapa

**Motor integrado y QA local aprobado.** Las75URLs (11productos y64artículos) siguen sin nuevas verificaciones; no se ejecutó el crawler, piloto ni operaciones remotas. Menús, canonicals, contenido, catálogo y paginación publicada permanecen fuera de esta intervención.

Antes de cualquier consulta real se debe revisar la invocación concreta del transporte integrado y contabilizar robots, posibles sitemaps, redirecciones y lecturas auxiliares. Después se solicitará una autorización independiente para el piloto de cinco destinos. La autorización de integración no permite ejecutarlo ni ampliar a75URLs.

Persisten los límites conocidos: evidencia acotada duplicada por compatibilidad del informe, presupuestos explícitos con fallo seguro y consumidores externos no inventariados exhaustivamente. No son regresiones observadas de la integración.
