# Adaptación del piloto V4 integrada — QA posterior

12 de noviembre de 2026. **Integración local completada y QA aprobado.** Únicamente el parche autorizado SHA256 `59d76bf8b54285dab38271aaedb78bba777fe61efd9edfc4500fec75759bf459`: tres modificaciones y dos altas, sin eliminaciones. El piloto real no se ejecutó. Cero solicitudes HTTP a Rhino o Google.

## Verificación e integración

Coincidieron el SHA256 del parche, las tres preimágenes, la ausencia de las dos altas y los respaldos aprobados. Se verificó de nuevo el payload de cinco archivos y se ejecutó git apply --check antes de aplicar. Los cambios sin commit de V4 anteriores se preservaron: la comparación fue contra sus hashes aprobados, no contra un estado Git limpio.

Los cinco hashes posteriores coinciden con el manifiesto, también después del QA. Los demás archivos versionados conservaron sus hashes durante integración y pruebas. No se modificaron tema, menús, catálogo, canonicals, paginación publicada, modelos, orquestador ni AGENTS.md. No hubo watch, force, sincronización global, staging o despliegue remoto.

[Preflight](preflight.json) · [aplicación](application.json) · [hashes y respaldos](hashes.json) · [diff y revisión independiente previos](../closed-pilot-candidate/README.md).

## Archivos integrados

| Archivo | SHA256 posterior |
|---|---|
| `tests/integration/test_seo_pilot_cli_v4.py` | `7e8e6ea49211d4258f82b69e992aa74e97c4b84add1140f02ad9cffbc43203cd` |
| `tests/unit/test_seo_pilot_v4.py` | `88eb5a4d173f43d6ccb1165ff35f5f1ddf24e32d4d889481b131584b282cb116` |
| `tools/ipanema/seo/crawl_policy.py` | `d30c444a60853ee482934515c2d628238cca26c5eb9dc364aa44542e5daaa4e9` |
| `tools/ipanema/seo/crawler.py` | `f6e5de5fd60c16eb3e464dd5b10111bf60eb9e4289dcc05f00503805f056415f` |
| `tools/ipanema/seo/engineering.py` | `1c6c0534755723cfac59e4395ad0fc44af6dc5df35dd88a1da98eb6c4ab7bd8d` |

Las tres preimágenes y los respaldos íntegros se conservan en hashes.json y en el run. Las dos altas no sustituyeron archivos existentes. La revisión previa de Claude y Codex corresponde a estos hashes exactos; no se repitió el consejo ni se atribuyeron revisiones nuevas a los agentes.

## QA posterior sobre el workspace integrado

| Control | Resultado |
|---|---|
| Unitarias SEO | **209 aprobadas** |
| Integración general y nuevas pruebas cortas | **22 aprobadas**: 13 generales y 9 nuevas |
| Prueba larga, ejecutada aparte | **Aprobada**, con presupuesto real de 120 s |
| Hashes posteriores | **5/5 coinciden** después de todas las pruebas |
| Selector cerrado | Solo robots y los cinco destinos de la fixture |
| Home, sitemap y enlaces fuera de selección | Ningún GET en la fixture |
| Parada global | Sin peticiones posteriores al error simulado |
| Presupuestos | Fetcher único, máximo12 GET,0,5/s,3saltos globales y límites de tiempo/cuerpo |
| Checkpoint | Pendientes, iniciadas sin resultado confirmado y completadas preservadas |
| Parsing/exportación/interrupción | Cancelación comprobada por las pruebas cortas de procesos |
| Modo general | Regresión y semilla home/BFS conservadas en las pruebas existentes |

El skipped del test largo en el lote corto es intencional: se ejecutó separadamente, no se dejó sin probar.

[209 unitarias](seo-unit.json) · [integraciones cortas](seo-integration.json) · [controles adicionales](controller-checks.json) · [ayuda CLI instalada](installed-cli-help.txt).

Estas pruebas usan respuestas inyectadas y proyectos sintéticos. El manifiesto real de cinco URLs se validó localmente sin solicitarlas. No se presentan como verificación HTTP de producción ni como prueba de indexación en Google.

## Cancelación real y checkpoint

El recibo largo anterior no incluía una huella completa del entorno. Se decidió **repetir** la fixture larga en el código integrado, en vez de dar por demostrada equivalencia. La nueva evidencia registra binario/versión Python, sistema, boot y hashes de los módulos/test relevantes; permanecieron iguales tras la ejecución.

- Presupuesto configurado: **120 s**; la gracia de terminación está incluida dentro de él.
- Tiempo supervisado observado: **119.508 s**; prueba completa: **119.790 s**.
- Worker recogido: **sí**. Descendiente activo después: **no**.
- HTTP real en esta fixture: **0**.
- Estado conservado: **started_without_confirmed_result**; no se afirmó que una petición sin respuesta no hubiera llegado al servidor.

[Recibo de cancelación](real-120-second-receipt.json) · [resultado de la prueba larga](long-test-result.json) · [entorno y hashes](long-test-environment.json).

También se conservaron ejemplos durables del checkpoint antes de empezar, después de completar las seis operaciones simuladas y tras un fallo simulado en el primer documento: [pendientes](before-fixture-checkpoint.json), [completadas](normal-fixture-checkpoint.json), [sin confirmación tras error](failed-fixture-checkpoint.json).

Límites aceptados de la revisión: entorno Linux/POSIX y limpieza del grupo del cliente actual, no de procesos que deliberadamente escapen de sesión. El checkpoint conserva top-level state=running/project=null: **no es la autoridad del estado terminal**; se consultan los estados por petición y supervision.json. La prueba no certifica cualquier plataforma o fallo del sistema operativo.

## Incidencias y reversión

No hubo discrepancias en preflight ni fallos del QA posterior. **No se ejecutó reversión del workspace.** Se validó de nuevo la reversión sobre archivos temporales: restauró únicamente las tres preimágenes y retiró las dos altas propias, sin afectar al motor integrado. [Prueba aislada de reversión](isolated-reversal-proof.json).

La reversión autorizada solo podría utilizarse si aparece una regresión crítica atribuible a esta integración y los cinco hashes posteriores siguen intactos. Ante cambios ajenos, debe detenerse sin sobrescribirlos.

## Estado definitivo y siguiente autorización

**El motor integrado está listo para solicitar autorización independiente del piloto de cinco URLs.** Las75URLs siguen pendientes de nuevas consultas; no se ejecutó el piloto ni el crawler general contra producción, no se consultó Search Console ni se alteró la tienda.

Las cinco URLs propuestas son:

1. https://rhino-performance.com/productos/pistola-de-masaje-gun-pro/
2. https://rhino-performance.com/productos/tina-de-hielo-tub-air/
3. https://rhino-performance.com/blog/posts/la-presoterapia-como-transformador-de-tu-salud-mental-relajacion-y-recuperacion-127cdc829590/
4. https://rhino-performance.com/blog/posts/el-fro-no-es-un-castigo-es-una-herramienta-cbe9a25855f8/
5. https://rhino-performance.com/blog/posts/faja-de-compresion-lumbar-el-soporte-que-tu-espalda-agradecera-047c381cf3ac/

Manifiesto exacto SHA256: `3b14fcb031ae57ab43ef247ff087c6d8df0b0c400ca12ac3694edfc654a38bb6`. [Procedencia y destinos](../pilot-preparation/targets.json).

La operación futura será una sola ejecución de la CLI instalada con ese manifiesto, origen exacto https://rhino-performance.com, máximo12GET incluyendo robots/redirecciones, concurrencia1,0,5/s o menos por robots,120s totales,20s porGET,2.000.000bytes por cuerpo codificado/decodificado y3saltos globales. No se añaden home, sitemap, enlaces, recursos ni páginas para consumir el presupuesto sobrante. No incluye GSC ni ampliación a75URLs.

**Orden prevista, NO autorizada y NO ejecutada:**

```bash
python3 tools/ia.py --project rhino-performance seo crawl --targets-manifest reports/rhino-performance/indexability-20261112/site-continuation/coverage-closure/pilot-preparation/targets.json --targets-sha256 3b14fcb031ae57ab43ef247ff087c6d8df0b0c400ca12ac3694edfc654a38bb6 --allow-network --max-urls 8 --max-depth 0 --max-requests 12 --requests-per-second 0.5 --max-seconds 120 --timeout 20 --max-bytes 2000000 --max-sitemaps 0 --max-redirects 3 --concurrency 1
```

[Operación exacta propuesta](proposed-pilot-operation.json) · [orden](pilot-command-NOT-AUTHORIZED.txt) · [estado actual](status.json).

Antes de cualquier ejecución real debe recibirse autorización específica y volver a comprobar los hashes del código, el manifiesto y sus cinco destinos. La consulta inicial de robots forma parte de esa futura autorización, no de esta integración.

Evidencias completas y respaldos: `reports/runs/rhino-performance/20261112T-closed-pilot-authorized-integration-215945624490`.
