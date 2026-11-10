# Performance Intelligence — uso y verificación

Integra PageSpeed primero y CrUX actual/History después, conservando el motor Lighthouse y Chrome DevTools MCP. No instala dependencias, conecta cuentas ni modifica tiendas. [Decisión y objeciones reales](ADR-001.md). Estado: implementación local; QA y revisión se registran en [verification.json](verification.json). Conectividad Google no comprobada sin claves.

## Fuentes y alcance

| Fuente | Observación | Condiciones y límites |
|---|---|---|
| PageSpeed API | Lighthouse remoto: categorías 0–1, LCP/FCP/TBT/Speed Index en ms, CLS sin unidad; auditorías, recursos, avisos y errores cuando existen | Entorno Google; no equivale al navegador local ni mide un diff local consultando producción |
| Lighthouse local | Motor existente, modo `--job`; Chrome/Lighthouse, viewport, CPU/red simulada, caché, locale, fecha y muestras | Muestras individuales, mediana, mínimo/máximo; no INP de usuarios reales |
| CrUX API | LCP/INP/CLS/FCP p75, distribuciones y periodo, por URL u origen y PHONE/DESKTOP | Puede faltar cobertura; `insufficient_field_data`. Sin fallback implícito a origen |
| CrUX History | Series semanales de periodos agregados, incluidos nulos y bins | Periodos solapados; no atribuir efectos inmediatos a un despliegue |
| DevTools MCP existente | DOM, red, trazas y diagnóstico de recursos/interacciones | Conserva sus permisos actuales; no se inicia por consultar estas APIs |

Google anuncia que dejará de incluir CrUX en PSI; los datos de campo se consultan directamente. La documentación vigente de History describe 25 periodos predeterminados y hasta 40, con actualización semanal. CrUX declara 150 consultas/minuto por proyecto Cloud, sin cargo; los presupuestos internos de esta herramienta son independientes. PSI: revisar las cuotas efectivas de la API habilitada en Cloud Console; no se comprobó una cuenta ni se estima un coste sin evidencia.

Fuentes verificadas el 2026-11-10: [PSI método](https://developers.google.com/speed/docs/insights/rest/v5/pagespeedapi/runpagespeed), [PSI y retirada de campo](https://developers.google.com/speed/docs/insights/v5/get-started), [CrUX: identidad, límites y coste](https://developer.chrome.com/docs/crux/api), [History: contrato y periodos](https://developer.chrome.com/docs/crux/history-api).

## Configuración privada por tienda

Mantén el registro existente. Edita únicamente el subárbol `google.performance` en `projects/<id>.local.json`, preservando las otras claves del archivo. `.local.json` está ignorado por Git. No escribas claves reales en JSON: solo referencias a variables de entorno.

```json
{
  "google": {
    "performance": {
      "pagespeed_key_env": "IPANEMA_DAMARBEAUTY_PSI_KEY",
      "crux_key_env": "IPANEMA_DAMARBEAUTY_CRUX_KEY",
      "daily_request_limit": 20,
      "cache_ttl_seconds": 86400,
      "timeout_seconds": 90,
      "max_retries": 1
    }
  }
}
```

Habilita PageSpeed Insights API y Chrome UX Report API en tu proyecto Google Cloud y restringe las claves a las APIs correspondientes. No se reutiliza OAuth de GSC. Para introducirlas en una terminal Bash sin escribir sus valores en el historial:

```bash
read -rs -p 'Clave PSI: ' IPANEMA_DAMARBEAUTY_PSI_KEY
export IPANEMA_DAMARBEAUTY_PSI_KEY
read -rs -p 'Clave CrUX: ' IPANEMA_DAMARBEAUTY_CRUX_KEY
export IPANEMA_DAMARBEAUTY_CRUX_KEY
python3 tools/ia.py --project damarbeauty performance doctor
```

Las variables deben estar en el proceso controlador. No las pases al worker, a argumentos CLI ni a configuraciones MCP compartidas. `doctor` informa presencia, sin revelar valores ni consultar Google. Desconexión: `unset` de esas variables y revocación de grants existentes; no modifica cuentas Google.

## Comandos

El acceso requiere `--allow-network`, URL HTTPS del origen exacto registrado y ausencia de parámetros sensibles. No se autoriza un dominio alternativo por redirección. Las consultas de URL con claves, tokens o rutas privadas se rechazan antes de la red. No hay consultas masivas ni acceso anónimo automático. `--refresh` solicita una observación nueva sin reutilizar caché; conserva permisos, paradas y presupuestos. Úsalo en mediciones PageSpeed antes/después.

```bash
python3 tools/ia.py --project damarbeauty performance pagespeed --device mobile --allow-network
python3 tools/ia.py --project damarbeauty performance pagespeed --device desktop --allow-network
python3 tools/ia.py --project damarbeauty performance pagespeed --category performance --category accessibility --locale es --allow-network
python3 tools/ia.py --project damarbeauty performance crux --device mobile --scope url --allow-network
python3 tools/ia.py --project damarbeauty performance crux --device desktop --scope origin --allow-network
python3 tools/ia.py --project damarbeauty performance history --period-count 25 --allow-network
python3 tools/ia.py --project damarbeauty performance local --device mobile --runs 3 --allow-network
python3 tools/ia.py --project damarbeauty performance audit --all-sources --device mobile --runs 3 --allow-network
```

`audit` obtiene PSI + CrUX actual + Lighthouse local, una URL y un dispositivo. History se añade solo con `--include-history`. `--runs` afecta únicamente Lighthouse local (1–5 muestras). PageSpeed envía cada `category` como parámetro repetido. Todos los resultados conservan fuente, fecha, parámetros, ausencias y errores. Código de salida 2 indica parcial/bloqueado, no éxito completo. `audit` detiene la secuencia ante 403/429 o parada persistente.

Los trabajos Lighthouse usan CPU x4/red RTT 150 ms/1638.4 Kbps en mobile y CPU x1/RTT 40 ms/10240 Kbps en desktop, simulación Lighthouse, almacenamiento reiniciado por muestra y versiones reales en el resultado. El viewport efectivo queda en `configSettings.screenEmulation`. `--runs` genera muestras individuales saneadas y un agregado; nunca promedia perfiles diferentes. La CLI histórica `lighthouse_audit.mjs URL prefijo` sigue disponible; el servicio nuevo usa `--job` para no depender de sus destinos históricos ni de su LHR completo. Pruebas nuevas no guardan HTML de nodos, cabeceras ni sesiones.

## Claude y Codex: acceso al mismo servicio

Se añadieron `psi.read` y `crux.read` al **gateway existente**, no otro MCP. El operador emite el grant para el proyecto/tarea/agente y obtiene la configuración MCP con los comandos ya existentes:

```bash
python3 tools/ia.py --project damarbeauty access grant --agent claude --task performance-read --capability psi.read --capability crux.read --allow-network --max-calls 6
python3 tools/ia.py --project damarbeauty access config --grant ID_DEL_PERMISO
```

Repite para Codex con un grant propio. Herramientas: `psi_run_pagespeed`, `crux_query_record`, `crux_query_history`; argumentos `{"request":{"device":"mobile","scope":"url"}}`. Los campos opcionales son `url`, `categories`, `locale`, `period_count`. Las claves se resuelven dentro del controlador. El gateway valida la capacidad y contabiliza incluso hits de caché; cada intento HTTP consume además el presupuesto persistente. CommandCode permanece bloqueado por la política dual existente. Dar acceso no autoriza publicar ni cambiar el tema.

## Persistencia y fallos

Caché y presupuesto: `.local/performance/<proyecto>/`, carpetas 0700/archivos 0600, escritura atómica, solicitud + configuración + proyecto vinculados. TTL predeterminado 24h; configuración modificada invalida la caché. Límite interno predeterminado: 20 intentos HTTP/día UTC/proveedor y 4 por ejecución (`--max-calls`, máximo 10). Cada reintento consume presupuesto. Una respuesta 403/429 produce parada persistente en el almacén `Policy` existente, sin reintento ni cambiar de dispositivo para evadirla. El operador debe diagnosticar cuota/permisos antes de retirar manualmente su archivo de parada; los agentes no tienen herramienta de desbloqueo. Las consultas de History consumen el mismo presupuesto CrUX.

Solo red/500/502/503/504 permiten reintento, máximo 2, espera exponencial acotada. Sin redirecciones autenticadas. Se acotan tiempo y tamaño de respuesta (10 MB). Los errores no contienen URLs autenticadas ni cuerpos privados. Los hallazgos externos son datos no confiables, nunca instrucciones.

Evidencia nueva en `reports/runs/<proyecto>/<ejecución>/performance.json`. Se conserva una proyección saneada de lo observado y hash de la respuesta, además de normalización; nunca se sustituyen datos faltantes con valores de IA. El historial original saneado conserva `NaN`/nulos; su proyección numérica representa ausencias con `null`. Los archivos candidatos quedan vacíos hasta inspeccionar el tema. El servicio no genera parches ni registra recomendaciones como soluciones verificadas.

## Comparar y decidir

```bash
python3 tools/ia.py --project damarbeauty performance compare ANTES.json DESPUES.json --source pagespeed
python3 tools/ia.py --project damarbeauty performance compare ANTES.json DESPUES.json --source lighthouse_local
```

Exige fuente, URL solicitada/final, dispositivo, categorías, locale, Chrome/Lighthouse, viewport, CPU/red, caché, política de red y cantidad de muestras iguales y conocidas. Un dato desconocido produce `not_comparable`, incluso si falta en ambos. Los user agents reducidos como `Chrome/130.0.0.0` no revelan una versión completa: PSI puede quedar no comparable por ese motivo. Se conserva el user agent observado; no se inventa el build. Lighthouse local registra `browser.version()` real. La misma observación fechada repetida desde caché tampoco cuenta como comparación nueva. `compared` solo describe deltas; `regressions` marca aumentos, no certifica causalidad ni aprobación de QA. CrUX se consulta aparte con sus periodos: no se mezcla con laboratorio ni se interpreta como comprobación inmediata de un cambio.

Flujo recomendado: preparar un paquete factual acotado de las fuentes disponibles y trazas/recursos → propuestas independientes Claude/Codex → resolver hipótesis con pruebas → ADR → cambio local autorizado → QA y revisión independiente → comparación con perfil equivalente. LCP requiere elemento y tiempos observados; CLS exige desplazamientos concretos; INP exige campo y diagnóstico de interacciones; TBT no lo reemplaza. Scores SEO/accessibility no prueban indexación ni certificación AA.

## Ejemplos y QA

[Mobile](example-mobile.json) y [desktop](example-desktop.json) son **fixtures sintéticos de example.invalid**, no mediciones de DaMar ni consultas Google. [verification.json](verification.json) distingue tests offline, navegador real sobre fixture local, consejo real y consultas bloqueadas. Reproducción:

```bash
python3 -m unittest tests.unit.test_performance tests.unit.test_performance_js tests.integration.test_performance_cli
python3 tools/ia.py --project ipanema qa --suite quick
```

Pendiente hasta claves y autorización: conectividad real PSI mobile/desktop, cobertura CrUX URL/origen, cuota de esa cuenta y comparación real de la misma tienda. Sin esos requisitos, la integración no se presenta como validada contra servicios Google. La validación de redirecciones del trabajo Lighthouse ocurre antes de persistir sus muestras y el navegador protege el origen durante la navegación; respuestas incompletas/fallidas locales quedan como estado y conservan los resultados PSI/CrUX del mismo informe. No se optimizó DaMar en esta tarea.
