# Matriz de objeciones V4 — entrega previa a aplicación

Estado: **needs_evidence / no aplicado**. Motor, AGENTS.md, tema y producción sin cambios en esta revisión. No hay permiso de rastreo externo.

Propuesta actual: [v3](../v4-review-corrections-v3.patch), SHA-256 `384deeb0673e607712f734130a0895a6fb3129d6c61564ffd93c219378c9eb19`.

El parche original se conserva. La v2 también se conserva para vincular la revisión de Claude a su hash. La v3 sustituye ambos para una futura aplicación: no apilar los parches. [Delta v2 → v3](../v4-review-v2-to-v3.patch).

| Objeción | Evidencia y prueba | Estado de propuesta v3 |
|---|---|---|
| O1: max-image-preview:none produce falso noindex | indexability.classify y page_audit; meta/cabeceras · `test_O1_preview_none_is_not_noindex; test_headers_multiple_and_scope` | corregido/control probado en candidato aislado; no aplicado |
| O2: Selección de robots por subcadena en vez de product token | Robots._selected; Googlebot frente a bot · `test_O2_robot_product_token_not_substring; test_robots_merge_exact_groups_case_and_fallback` | corregido/control probado en candidato aislado; no aplicado |
| O3: Exclusiones críticas perdidas tras truncar 2000 filas | excluded_total/log frente a excluded_by_reason · `test_O3_late_exclusion_partial` | corregido/control probado en candidato aislado; no aplicado |
| O4: max_urls puede ocultar URLs del sitemap sin verificar | set sitemap frente a URLs comprobadas · `test_O4_unchecked_sitemap_partial` | corregido/control probado en candidato aislado; no aplicado |
| O5: Palabra comprar en contenido editorial tratada como acción | Policy.check sobre /blog/posts/como-comprar-x · `test_O5_editorial_action_word_allowed` | corregido/control probado en candidato aislado; no aplicado |
| A1: Ciclo de redirects del sitemap descartado sin error | sitemap_seen y cadenas sin documento final · `test_sitemap_redirect_cycle_not_complete` | corregido/control probado en candidato aislado; no aplicado |
| A2: Límite de redirects del sitemap descarta destino sin marcar parcial | max_redirects=0 con Location pendiente · `test_sitemap_redirect_limit_not_complete` | corregido/control probado en candidato aislado; no aplicado |
| A3: Enlaces de página sitemap-only quedan sin HTTP pero complete=True | depth=None añade arista sin comprobar destino · `test_disconnected_sitemap_outgoing_required_unchecked` | corregido/control probado en candidato aislado; no aplicado |
| A4: NAT64 global puede incorporar IPv4 privada | Python 3.12 is_global=True para 64:ff9b::7f00:1; sin conexión real · `test_dns_transition_prefix_private_not_accepted` | corregido/control probado en candidato aislado; no aplicado |
| A5: Sufijos y parámetros de ruta comerciales pasan el filtro | /cart.json; /checkout;step=1; /cart%3Bfoo/add · `test_commercial_suffix_and_matrix_routes_excluded` | corregido/control probado en candidato aislado; no aplicado |
| A6: Espera del scheduler agota deadline antes de iniciar request | Clock inyectado excede max_seconds durante sleep · `test_deadline_rechecked_after_scheduler_delay` | corregido/control probado en candidato aislado; no aplicado |
| S1: HTTP GET, certificado/SNI y ausencia de Cookie/Authorization | Servidor TLS real 127.0.0.1; certificado de fixture; host incorrecto rechazado · `tls_fixture.LocalTLS; TransportV4` | corregido/control probado en candidato aislado; no aplicado |
| S2: Mismo origen HTTPS y rutas privadas tras decodificación | Sin red de storefront; fixtures verifican destinos nunca solicitados · `test_domain_schemes_and_actions_in_query; test_actions_private_multiencoded_and_ambiguous; test_redirect_to_private_external_never_requested` | corregido/control probado en candidato aislado; no aplicado |
| S3: 403/429/challenge y robots desconocido detienen operaciones | Contador real de llamadas de transporte inyectado · `test_403_429_stop_from_sitemap_no_home; test_robots_unreachable_and_challenge_no_crawl` | corregido/control probado en candidato aislado; no aplicado |
| S4: Transferencia, gzip, presupuesto y DNS fijado | Pruebas del transporte actual reutilizadas; no benchmark remoto · `tests/unit/test_seo_transport_v4.py; PolicyV4.test_permissions_limits_stop_and_rate` | corregido/control probado en candidato aislado; no aplicado |
| A7: Regresión v2: acciones con sufijos admitidas (/add-to-cart-123, /comprar-ahora) | Claude v2 + contraejemplo reproducido en copia aislada · `test_action_prefix_suffix_regression` | pasa en propuesta v3; no aplicado ni aprobado |
| A8: PRIVATE deja pasar delimitadores como checkout-step y cart,1; acción addtocart compacta | Claude v2 + contraejemplo reproducido en copia aislada · `test_private_prefix_delimiters_and_action_compact` | pasa en propuesta v3; no aplicado ni aprobado |
| A9: Location ausente debe producir error explícito en home, sitemap y robots | Claude v2 + contraejemplo reproducido en copia aislada · `test_missing_location_is_explicit_error` | pasa en propuesta v3; no aplicado ni aprobado |
| A10: Registro de parser sin source no debe lanzar KeyError ni completar inventario | Claude v2 + contraejemplo reproducido en copia aislada · `test_malformed_sitemap_parser_record_fails_closed` | pasa en propuesta v3; no aplicado ni aprobado |
| A11: User-agent con versión en robots no debe quedar silenciosamente permitido | Claude v2 + contraejemplo reproducido en copia aislada · `test_invalid_robots_agent_with_version_fails_closed` | pasa en propuesta v3; no aplicado ni aprobado |
| R1: Revisión independiente y aprobación correspondientes | Orquestador dual; no mayoría ni aprobación por pasar tests · `ADR y recibos del consejo` | v2: Claude cambios solicitados; Codex inactividad; v3 pendiente de revisión y aprobación |

## Resultados reproducidos

- Cinco defectos originales: fallan antes y pasan con el parche original exacto; [veredicto verificable](original-five-verdict.json).
- Casos ampliados: seis métodos siguen fallando con ese parche; se corrigen en v2.
- Revisión independiente: Claude y Codex evaluaron el parche original y respaldaron las cuatro primeras carencias adicionales. En v2 Claude solicitó cambios por ACTIONS con sufijos; Codex no completó la propuesta tras inactividad. No hay consenso dual ni aprobación.
- Nueva regresión de Claude y observaciones adicionales: fallan sobre v2; pasan con v3. Se conservan logs antes/después.
- Propuesta v3: **34 pruebas específicas, incluidas en 122 unitarias SEO**, 13 integración y una prueba TLS real en loopback aprobadas. El artefacto se aplicó a otra copia nueva y sus hashes coinciden con el árbol probado. [Manifiesto](v3-validation.json).
- QA general del motor actual: `reports/runs/rhino-performance/20261111T170127-seo-ed86ab12/report.json` aprobado; esto no prueba que los defectos conocidos estén corregidos en el workspace.

## Completitud y alcance

`complete_for_policy` exige que `unverified_required_urls` esté vacío. Son obligatorios home, URLs del sitemap aceptadas y destinos internos/redirects permitidos observados. También exige robots conocido, ausencia de parada/errores/colas pendientes, documentos de sitemap resueltos y contadores de exclusión crítica en cero. Un 404 cuenta como comprobado, no como saludable. No se declara inventario exhaustivo de la tienda.

Se conserva el alcance del crawler: las salidas de páginas comprobadas solo por sitemap no se recorren automáticamente; si falta HTTP en esos destinos, el resultado queda parcial. Un bloqueo de robots sobre una URL obligatoria también impide completitud.

## Decisiones revisables

- ACTIONS conserva anclaje al inicio de segmento para permitir `como-comprar-x`, pero rechaza prefijos de acciones y sus sufijos. Se evita la recomendación de lookahead alfanumérico porque dejaría pasar el contraejemplo explícito `add_to_cart123`.
- PRIVATE bloquea delimitadores y dígitos tras el nombre, conservando palabras públicas más largas como `cartografia`.
- Agentes de robots con sintaxis no admitida (como versión con slash) generan evidencia desconocida y detención conservadora; no se afirma imitar cómo Google recupera ese archivo inválido.
- Prefijos NAT64/túnel contemplados se rechazan por completo, incluso algunos destinos públicos. No se garantiza detectar todos los prefijos de traductores definidos por operadores. No se explotó una red real.
- Se agrega error explícito para Location ausente y acceso defensivo al campo source; se elimina la comprobación redundante de subset porque ya está contenida en verification_coverage.

## Límites y aprobación pendiente

TLS utiliza certificado efímero confiado solo por el fixture y un reenvío de socket explícito a 127.0.0.1. Comprueba SNI, certificado/hostname, GET, cabeceras y ausencia de cookies/auth; no prueba DNS/TLS de RHINO. Los demás escenarios usan transporte inyectado y prohíben sockets. GET y filtros de rutas no certifican cualquier servidor que viole la semántica de GET.

La v3 no tiene revisión independiente aprobada. No se repite indefinidamente la inferencia ni se inventa participación de Codex. Solicitud de revisión humana: evaluar esta matriz, el delta y el parche exacto; resolver las condiciones obligatorias del consejo antes de aplicación. AGENTS.md exige que «Objeciones críticas y condiciones obligatorias pendientes impiden implementar» y bloquea aprobación ante ausencia de un participante. La revisión humana no se registrará como consenso dual.

El QA posterior a aplicación no se ha ejecutado porque el código no se ha aplicado. Una futura aplicación exige hashes frescos, archivo nuevo ausente, transacción attempt/backup, únicamente diff autorizado y nuevamente QA unitario/integración/crawler. La autorización actual no incluye rastreo externo completo.

Fuentes: [RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html#section-2.2.1), [directivas Google](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag), [RFC 6052](https://www.rfc-editor.org/rfc/rfc6052.html), [RFC 8215](https://www.rfc-editor.org/rfc/rfc8215.html).

Exportaciones: [JSON](objections.json), [CSV](objections.csv).
