# Piloto cerrado SEO V4 — candidato aislado para integración

12 de noviembre de 2026. **Adaptación preparada y aprobada técnicamente para solicitar integración local.** No se aplicó al repositorio integrado ni se hizo HTTP a Rhino/Google. Se mantuvieron intactos sus11 hashes aprobados. No hubo cambios al tema,menús,canonicals,catálogo,orquestador,modelos o AGENTS.

## Paquete exacto

SHA256 del parche: `59d76bf8b54285dab38271aaedb78bba777fe61efd9edfc4500fec75759bf459`.

**Tres modificaciones y dos altas,ninguna eliminación.** [Diff](candidate.patch) · [manifiesto con hashes antes/después](manifest.json) · [ADR](ADR.json) · [controles del controlador](controller-gates.json).

| Archivo autorizado para el candidato | SHA256 después |
|---|---|
| `tests/integration/test_seo_pilot_cli_v4.py` | `7e8e6ea49211d4258f82b69e992aa74e97c4b84add1140f02ad9cffbc43203cd` |
| `tests/unit/test_seo_pilot_v4.py` | `88eb5a4d173f43d6ccb1165ff35f5f1ddf24e32d4d889481b131584b282cb116` |
| `tools/ipanema/seo/crawl_policy.py` | `d30c444a60853ee482934515c2d628238cca26c5eb9dc364aa44542e5daaa4e9` |
| `tools/ipanema/seo/crawler.py` | `f6e5de5fd60c16eb3e464dd5b10111bf60eb9e4289dcc05f00503805f056415f` |
| `tools/ipanema/seo/engineering.py` | `1c6c0534755723cfac59e4395ad0fc44af6dc5df35dd88a1da98eb6c4ab7bd8d` |

Solo crawler.py,engineering.py y crawl_policy.py cambian respecto al motor integrado;solo dos archivos nuevos contienen las pruebas. Los respaldos verificados de las tres preimágenes están en el run privado indicado al final. Las dos altas siguen ausentes en el workspace.

## Selección y transporte

El modo opcional implementa --targets-manifest y --targets-sha256. Valida hash,JSON sin duplicados,proyecto,origen y cincoURLs únicas literales antes del transporte. No cambia public_url ni falsifica sitemap. La cola contiene solo los cinco destinos y redirecciones permitidas,sin GET de home,sitemap,enlaces,imágenes,JS o CSS.

Se reutilizan el mismo loop,Robots,Policy,Fetcher,https_get,extractor y clasificadores de V4. El modo general conserva home/sitemap/BFS. El callback de checkpoint es opcional y nulo fuera del modo supervisado;no hay otro crawler ni motor de orquestación.

Se verificó que una redirección hacia otra URL seleccionada ya observada no sea declarada ciclo ni descargada de nuevo. La reproducción anterior del borrador y su test de regresión están conservados. Cualquier rechazo de seguridad,403/429,robots desconocido,bloqueo del agente o Googlebot,timeout,error de transporte,codificación/gzip inválidos,Location inválido o ciclo detiene la cola completa del modo cerrado.

## Cinco destinos conservados

1. https://rhino-performance.com/productos/pistola-de-masaje-gun-pro/
2. https://rhino-performance.com/productos/tina-de-hielo-tub-air/
3. https://rhino-performance.com/blog/posts/la-presoterapia-como-transformador-de-tu-salud-mental-relajacion-y-recuperacion-127cdc829590/
4. https://rhino-performance.com/blog/posts/el-fro-no-es-un-castigo-es-una-herramienta-cbe9a25855f8/
5. https://rhino-performance.com/blog/posts/faja-de-compresion-lumbar-el-soporte-que-tu-espalda-agradecera-047c381cf3ac/

[Manifiesto original y procedencia](../pilot-preparation/targets.json). No se abrieron estas páginas. Sus75respuestas pendientes no se transformaron en resultados HTTP.

## Presupuestos

- 12GET totales,concurrencia1,intervalo mínimo2s o mayor según robots.
- 120s para el trabajo supervisado,con hasta1s reservado dentro de ese techo para cancelación y recogida;20s por GET o restante menor.
- 2.000.000bytes por cuerpo codificado y descomprimido;el byte centinela adicional sirve para detectar y rechazar exceso,no para aceptar cuerpos mayores.
- Tres saltos GLOBALES compartidos entre robots/documentos,ratificados por la autorización de preparación. Hasta8nodos:5destinos+3saltos,pero no8destinos libres.
- Una lectura robots y cinco documentos sin saltos=6GET;con3saltos globales≤9GET. El techo12no permite rellenar presupuesto con otras páginas.
- DNS/TLS consumen tiempo,pero no son GET adicionales. No hay reintentos ni cambio de transporte para evadir bloqueos.

## Checkpoint y cancelación real

Antes de cada transporte se persiste atómicamente y se hace fsync del estado started. El checkpoint distingue peticiones pendientes,iniciadas sin resultado confirmado y completadas;una excepción conserva la incertidumbre de llegada al servidor. Si no puede persistirse ese estado,no se inicia el GET. Los saltos nuevos se registran como pendientes antes de solicitarlos.

El supervisor de la CLI crea un worker POSIX con setsid,verifica su grupo y concede go antes de permitir trabajo. Dentro están validación del manifiesto,HTTP,parsing y exportación. Al vencer el presupuesto cancela el grupo con TERM/KILL y recoge el worker. También limpia descendientes al finalizar o interrumpir la CLI. El resumen de cancelación del padre se guarda después;no continúa trabajo HTTP/análisis mientras se registra.

Prueba con presupuesto real120s y reloj real,**sin sockets ni HTTP**:

- Ejecución supervisada observada: **119.506s**,incluida la gracia dentro del techo.
- Worker recogido: **sí**. Descendiente activo después: **no**.
- Petición simulada conservada como **started_without_confirmed_result**;no se afirmó que no hubiese llegado a un servidor.

[Recibo real120](real-120-second-receipt.json) · [resultado de unittest](full-120-test-result.json) · [binding exacto](real-120-binding-verification.json). La prueba120aparece skipped por diseño en el batch corto,se ejecutó aparte y pasó. No se sumó un mock de reloj como si fueran120s reales.

El módulo engineering.py permaneció idéntico después de esa prueba. Se añadió cobertura de CLI/interrupción y se corrigió convergencia en crawler.py;la función de test120no cambió. El controlador verificó ese binding con el manifiesto final. [Resolución de la observación sobre binding](binding-resolution.json).

La cancelación está acotada a los procesos del cliente actual que permanecen en el grupo. No se certifican procesos que deliberadamente ejecuten setsid/doblefork para escapar;el cliente https_get no lo hace. Un zombie,si el reaper del sistema todavía lo conserva,no está activo ni puede seguir haciendo solicitudes. POSIX/Linux es el entorno probado,no una garantía multiplataforma ni de sistema operativo de tiempo real.

## Pruebas aisladas y reversión

- **209unitarias SEO aprobadas**:191anteriores+18nuevas del piloto.
- **13integraciones generales aprobadas** en el candidato;se reutilizó ese recibo mientras sus módulos permanecieron iguales.
- **9integraciones cortas nuevas aprobadas**,incluida CLI real con --responses,checkpoint,errores de manifiesto,parsing/export detenidos e interrupción SIGTERM del supervisor.
- **1prueba larga de120s aprobada** separadamente.
- Aplicación del parche en otro worktree privado de herramientas:cinco hashes iguales al árbol probado. Reversión aislada:restauró las tres preimágenes y retiró únicamente las dos altas;no tocó el workspace integrado.

[QA del controlador](controller-qa.json) · [regresión aislada](final-isolated-tests.json) · [integraciones nuevas finales](final-pilot-integration-tests.json). Se repitió la regresión SEO al cambiar sus consumidores compartidos;no se reabrió discovery ni se repitieron quick/TLS local sin necesidad. Las pruebas no demuestran indexación ni funcionamiento de producción.

## Revisión Claude + Codex

Ambos proveedores originales revisaron independientemente el mismo hash con modelos balanced y aprobaron **solicitar integración local**,sin autorizar aplicación ni red. [Codex](codex-closed-review.json) · [Claude válido](claude-closed-review-recovery.json).

La primera salida de Claude pasó el schema JSON nativo,pero el normalizador del consejo rechazó objections[].id. No es evidencia de fallo de autenticación/cuota ni un rechazo técnico del candidato. Se conserva [ese fallo](claude-closed-review.json);su contenido no se contó como voto. Un único reintento con IDs ASCII explícitos,sin cambiar modelos,orquestador o validaciones,produjo revisión válida. El valor concreto del primer ID no se conservó antes de la normalización;esa limitación se registra,no se inventa.

La observación media de Claude sobre binding quedó verificada por el controlador:el hash exacto de engineering.py ya estaba en el recibo y coincide con el manifiesto final;se comprobó además la función AST del test largo. No se alteró su respuesta para simular que el modelo hubiese ejecutado esa comprobación.

Seguimientos aceptados:el checkpoint conserva top-level state=running y project=null;**su autoridad son los estados por petición y supervision.json para el estado terminal**. No debe interpretarse ese campo general como un worker todavía activo. También quedan límites de portabilidad y de señales/descendientes no probados universalmente. No hay objeciones críticas o altas abiertas en las revisiones válidas.

## Integración propuesta, todavía NO autorizada

Se solicita autorización específica para aplicar solo este parche de5archivos al repositorio IA-Ipanema y ejecutar QA local posterior. Antes:hash del parche,tres preimágenes,dos altas ausentes,respaldo íntegro y ausencia de modificaciones ajenas. Si hay discrepancia,detener.

Después de autorizar:aplicar solo el diff,verificar5hashes y ejecutar pruebas relevantes sobre el workspace,conservando recibos. Reversión propuesta limitada a las3preimágenes/2altas,solo si los hashes siguen siendo los propios posteriores y se autoriza expresamente;no sobrescribir cambios ajenos. No usar watch,force,sincronización global o despliegue remoto.

## Comando exacto previsto para el piloto futuro

**NO ejecutado y NO autorizado.** Estos flags existen solo en el candidato,hasta integrar y pasar QA. La siguiente orden requiere otra autorización independiente de red,con el manifiesto y hashes otra vez comprobados:

```bash
python3 tools/ia.py --project rhino-performance seo crawl --targets-manifest reports/rhino-performance/indexability-20261112/site-continuation/coverage-closure/pilot-preparation/targets.json --targets-sha256 3b14fcb031ae57ab43ef247ff087c6d8df0b0c400ca12ac3694edfc654a38bb6 --allow-network --max-urls 8 --max-depth 0 --max-requests 12 --requests-per-second 0.5 --max-seconds 120 --timeout 20 --max-bytes 2000000 --max-sitemaps 0 --max-redirects 3 --concurrency 1
```

[Orden prevista](pilot-command-NOT-AUTHORIZED.txt) · [argv y hash de manifiesto](pilot-operation.json). No corresponde ejecutarla ahora. No autoriza75URLs ni consultas GSC.

Run de evidencias y respaldo: `reports/runs/rhino-performance/20261112T-closed-pilot-candidate-1794519330364720500`.
