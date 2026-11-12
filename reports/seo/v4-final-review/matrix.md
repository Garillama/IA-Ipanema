# Matriz final V4 — previa a aprobación y aplicación

Estado: **candidato probado, sin aplicar, aprobación humana explícita pendiente**.

[Parche final único](../v4-review-corrections-final.patch): 32393 bytes, UTF-8/LF, SHA-256:
`4369d84d3a84bd99808d92eb12ad13bcf185f300615817bb6eedd517412acc6f`.

No apilar v1/v2/v3. El diff final parte directamente de los hashes actuales acreditados. Solo afecta cinco módulos existentes y dos archivos de pruebas nuevos. No modifica arquitectura, tema, producción, cuentas ni configuración de AGENTS.md.

| Objeción | Evidencia / prueba | Estado técnico | Aceptación |
|---|---|---|---|
| O1: max-image-preview:none produce falso noindex | test_O1_preview_none_is_not_noindex; test_headers_multiple_and_scope | prueba/control aprobado en candidato final aislado | pendiente aprobación humana; no aplicado |
| O2: Selección de robots por subcadena en vez de product token | test_O2_robot_product_token_not_substring; test_robots_merge_exact_groups_case_and_fallback | prueba/control aprobado en candidato final aislado | pendiente aprobación humana; no aplicado |
| O3: Exclusiones críticas perdidas tras truncar 2000 filas | test_O3_late_exclusion_partial | prueba/control aprobado en candidato final aislado | pendiente aprobación humana; no aplicado |
| O4: max_urls puede ocultar URLs del sitemap sin verificar | test_O4_unchecked_sitemap_partial | prueba/control aprobado en candidato final aislado | pendiente aprobación humana; no aplicado |
| O5: Palabra comprar en contenido editorial tratada como acción | test_O5_editorial_action_word_allowed | prueba/control aprobado en candidato final aislado | pendiente aprobación humana; no aplicado |
| A1: Ciclo de redirects del sitemap descartado sin error | test_sitemap_redirect_cycle_not_complete | prueba/control aprobado en candidato final aislado | pendiente aprobación humana; no aplicado |
| A2: Límite de redirects del sitemap descarta destino sin marcar parcial | test_sitemap_redirect_limit_not_complete | prueba/control aprobado en candidato final aislado | pendiente aprobación humana; no aplicado |
| A3: Enlaces de página sitemap-only quedan sin HTTP pero complete=True | test_disconnected_sitemap_outgoing_required_unchecked | prueba/control aprobado en candidato final aislado | pendiente aprobación humana; no aplicado |
| A4: NAT64 global puede incorporar IPv4 privada | test_dns_transition_prefix_private_not_accepted | prueba/control aprobado en candidato final aislado | pendiente aprobación humana; no aplicado |
| A5: Sufijos y parámetros de ruta comerciales pasan el filtro | test_commercial_suffix_and_matrix_routes_excluded | prueba/control aprobado en candidato final aislado | pendiente aprobación humana; no aplicado |
| A6: Espera del scheduler agota deadline antes de iniciar request | test_deadline_rechecked_after_scheduler_delay | prueba/control aprobado en candidato final aislado | pendiente aprobación humana; no aplicado |
| S1: HTTP GET, certificado/SNI y ausencia de Cookie/Authorization | tls_fixture.LocalTLS; TransportV4 | prueba/control aprobado en candidato final aislado | pendiente aprobación humana; no aplicado |
| S2: Mismo origen HTTPS y rutas privadas tras decodificación | test_domain_schemes_and_actions_in_query; test_actions_private_multiencoded_and_ambiguous; test_redirect_to_private_external_never_requested | prueba/control aprobado en candidato final aislado | pendiente aprobación humana; no aplicado |
| S3: 403/429/challenge y robots desconocido detienen operaciones | test_403_429_stop_from_sitemap_no_home; test_robots_unreachable_and_challenge_no_crawl | prueba/control aprobado en candidato final aislado | pendiente aprobación humana; no aplicado |
| S4: Transferencia, gzip, presupuesto y DNS fijado | tests/unit/test_seo_transport_v4.py; PolicyV4.test_permissions_limits_stop_and_rate | prueba/control aprobado en candidato final aislado | pendiente aprobación humana; no aplicado |
| A7: Regresión v2: acciones con sufijos admitidas (/add-to-cart-123, /comprar-ahora) | test_action_prefix_suffix_regression | prueba/control aprobado en candidato final aislado | pendiente aprobación humana; no aplicado |
| A8: PRIVATE deja pasar delimitadores como checkout-step y cart,1; acción addtocart compacta | test_private_prefix_delimiters_and_action_compact | prueba/control aprobado en candidato final aislado | pendiente aprobación humana; no aplicado |
| A9: Location ausente debe producir error explícito en home, sitemap y robots | test_missing_location_is_explicit_error | prueba/control aprobado en candidato final aislado | pendiente aprobación humana; no aplicado |
| A10: Registro de parser sin source no debe lanzar KeyError ni completar inventario | test_malformed_sitemap_parser_record_fails_closed | prueba/control aprobado en candidato final aislado | pendiente aprobación humana; no aplicado |
| A11: User-agent con versión en robots no debe quedar silenciosamente permitido | test_invalid_robots_agent_with_version_fails_closed | prueba/control aprobado en candidato final aislado | pendiente aprobación humana; no aplicado |
| H1: foo="noindex" interpretado como directiva | before-parser-on-exact-v3.json: 22 fallos de subcaso; after-final-specific.json: pasa | corregido en candidato; tests de =, :, comillas, escapes, flags y agentes | pendiente revisión humana final |
| H2: Identidad del texto exportado distinta de v3 | identity-v3.json; manifiesto original; copia nueva aplicada y hashes del candidato iguales | v3 original acreditada; copia exportada excluida como artefacto aplicable | original sin modificar; causa de diferencia de copia no determinada |
| H3: El artefacto final debe coincidir con código realmente probado | final-artifact-dry-run.json; final-artifact-apply-isolated.json; validation.json | parche único aplicado a base nueva; todos los hashes iguales al árbol probado | no aplicado en workspace |
| R1: Revisión y aprobación correspondientes antes de aplicar | Petición actual punto 6: revisión independiente o aprobación humana explícita; AGENTS.md sin cambios | se elige solicitar aprobación humana explícita del hash final; no se afirma aprobación dual | pendiente; no aplicar |

## Observación humana 1: parser

La expresión de v3 recorría palabras dentro de valores con `=` y dentro de comillas. Se reproduce el fallo sobre el parche original verificado. Se reemplaza exclusivamente la lógica léxica del parser por consumo de átomos/valores y se usa separación de cabeceras por comas fuera de comillas. No se cambian clasificación, entidades SEO, contratos comerciales ni motor de rastreo.

| Entrada | Resultado esperado y comprobado |
|---|---|
| `foo="noindex"`, `foo=noindex`, `foo: noindex` | No contienen una directiva independiente noindex |
| `max-image-preview:none` | No es noindex |
| `noindex`, `none`, `foo="noindex", noindex` | Conservan restricción |
| `otherbot: noindex` | No restringe Googlebot |
| Cabeceras repetidas o nombres de agente dentro de valores entrecomillados | Mantienen el alcance correcto sin tomar valores por agentes |

Se cubren escapes, comillas simples/dobles, valores no entrecomillados, mayúsculas, metadatos globales/específicos y datos mal formados seleccionados. Es un parser técnico acotado; no una ejecución de Googlebot. Un valor sin cierre consume su resto como valor y no genera directivas a partir de palabras internas. Se mantiene un noindex independiente anterior.

La comparación v3→final también corrige el escape HTML del helper de pruebas para que un valor con comillas llegue intacto al extractor. El test previo no acreditaba por sí solo ese subcaso entrecomillado. La corrección afecta solo al fixture, no al tema.

## Observación humana 2: identidad

V3 original: **25729 bytes**, SHA-256 `384deeb0673e607712f734130a0895a6fb3129d6c61564ffd93c219378c9eb19`. Coincide con v3-validation.json y approval-manifest.json. El parche se aplicó sobre copia nueva y los seis archivos resultantes coinciden con los hashes del candidato v3 que pasó pruebas. También se encontraron copias aisladas previas con esos mismos hashes.

La copia exportada declarada por el usuario tiene 25.728 bytes y SHA-256 `7fe10ce79ab0de98a078a4fe422ee277c6cfff599aa4e95606cd039dad92340d`. `/mnt/data/Texto pegado (2).txt` no está accesible en esta máquina. No se certifica la causa de su diferencia; quitar solo el LF final del original no produce ese hash. No se modifica ni normaliza el original para igualar la exportación. La copia exportada no es artefacto válido de aplicación. El usuario confirmó usar original y manifiesto como referencia.

Para la nueva entrega se incluye un ZIP con los bytes exactos y SHA256SUMS; descargar/revisar el archivo, no reconstruirlo desde un pegado o renderizado HTML. Una copia con hash diferente debe quedar bloqueada.

## QA ejecutado sobre candidato final

- 12 métodos nuevos de parser: el antes reproduce 22 fallos de subcaso sobre v3; después pasan.
- 50 pruebas específicas: 12 nuevas de parser, 34 previas y 4 de transporte. Están incluidas en las 134 unitarias SEO; no se suman como pruebas distintas.
- 134 unitarias SEO y 13 integración aprobadas.
- HTTPS/TLS real en loopback aprobado: GET, hostname/SNI, cabeceras repetidas, ausencia de cookies/auth y rechazo de hostname incorrecto.
- `python3 tools/ia.py --project fixture qa --suite seo` aprobado en el candidato aislado: unitarias, integración, evaluaciones SEO y estabilidad de fuentes. [Reporte real](candidate-seo-qa-report.json). El proyecto fixture es sintético y no consulta RHINO/Google.
- Dry-run y aplicación del parche final exacto sobre otra copia de la base; hashes finales iguales a los archivos probados.

Se revalidan robots/agentes, rutas comerciales y codificación múltiple, DNS global/prefijos traducidos, fijación de IP, TLS, redirects/ciclos, presupuestos de tiempo/bytes/URLs y paradas 403/429. El TLS real se limita a loopback, con routing de socket de test explícito; no prueba la red de RHINO. Las otras pruebas usan transporte inyectado. No se ejecutó el crawler externo.

## Aprobación requerida y siguiente paso

La revisión humana preliminar de v3 no se usa como aprobación de este artefacto nuevo. Se solicita aprobación humana explícita del parche final y su SHA-256, opción admitida por el punto 6 de la petición actual. No se presenta como revisión independiente completada ni como consenso dual. AGENTS.md permanece intacto y se registra su hash. Las condiciones técnicas están respaldadas por esta evidencia; la aceptación/revisión humana de ellas sigue pendiente.

Antes de aplicar: confirmar aprobación concreta, revalidar hashes de los cinco módulos y ausencia de las dos pruebas nuevas; crear attempt/backup local y detener ante diferencias. Aplicar únicamente el diff final aprobado. Después repetir QA unitario, integración y específico, comparar hashes y aceptar solo sin fallos. Ese QA posterior en el workspace aún no se ejecutó: no se aplicó el parche.

El permiso solicitado se limita a código local de IA-Ipanema. No autoriza tema, producción, catálogo, cuentas ni rastreo externo.

Entregables: [manifiesto](manifest.json), [validación](validation.json), [identidad v3](identity-v3.json), [delta para revisión v3→final](v3-to-final.diff), [JSON](objections.json), [CSV](objections.csv).
