# Preflight offline de validación nativa — hero H1/S1/T1

**Estado:** `needs_evidence`; el comando remoto sigue sin autorización y este paquete no lo ejecuta.

## Candidato fijado

| Ruta candidata | SHA256 esperado y observado en vista virtual | Tamaño |
|---|---|---:|
| `sections/hero.tpl` | `06dded46e359d68648c05253eff315e5c124e9c1d30313b0ea0b8e2c7ac7062c` | 12,854 bytes |
| `snippets/image.tpl` | `447a9b23e2cbe7ac752f804a754d8e99ad87cd32449c41aa658fa919e18a32b5` | 14,305 bytes |

La copia de [vista virtual](virtual-workspace/) contiene exactamente esas dos rutas visibles; directorios y archivos están en modo solo lectura (`0555`/`0444`). No contiene `.nuvem`, `.nube`, otros archivos del tema ni credenciales. Las hashes del checkout local original son diferentes (`hero.tpl` `5362f1b4ddab56feabc95ad23486cc1b439b02d06a0479a2fcb8deb96fa8861c`, `snippets/image.tpl` `f45641d2f4cd4e9fea775cf1aa19f806686130f79cb191e2a2140436919e178b`), así que ejecutar el CLI desde el checkout validaría otro contenido.

## Qué hace el CLI oficial

CLI observado localmente: `tiendanube` **2.5.1**, `dist/cli.js` SHA256 `0e5b412e40613a7c2521dccf4651e83b52404d23def4c997b6b9504c69b6558c`; `package.json` SHA256 `08d303ae04caebfb12f708af05bdaf4153fd698d70c3b1f30e23750378b19242`.

Comando oficial de validación:

```bash
tiendanube theme check --theme-id 14828608
```

El comando escanea el CWD con `readdirp`, filtra mediante `shouldSync`, obtiene metadata de la instalación y hashes remotos, y pasa a `files/validate` únicamente `diff.toCreate` y `diff.toUpdate`; no pasa `toDelete`. El endpoint recibe `POST { upsert: [...] }`, definido por el CLI como validación de las comprobaciones al guardar sin escribir archivos. El comando no tiene una opción `--file`; el CWD aislado es el límite que restringe sus candidatos.

El preflight [offline](offline-preflight-results.json), usando `readdirp` de la instalación del CLI y las reglas de `SYNC_PREFIXES`/`shouldSync`, vio exactamente los dos archivos. La fuente confirma que no se puede introducir una ruta de otro componente desde esta vista. La inclusión de esos dos archivos en el POST **depende además de que ambos difieran de los hashes remotos**. Los hashes remotos no se consultaron; si uno coincide, `theme check` enviaría solo el otro. Una futura guardia debe bloquear el POST salvo que su cuerpo tenga las dos rutas exactas y sus contenidos den las SHA256 fijadas.

La vista virtual puede usar en la futura ejecución un `.nuvem` **oculto** como symlink de solo lectura a la configuración ya existente: el filtro del CLI excluye rutas con segmento oculto del escaneo; `theme check` solo necesita leer esa configuración. No se creó el symlink ni se leyó/copió la credencial en esta preparación. Debe existir `.nuvem` desde el inicio para evitar cualquier migración de `.nube`; no colocar `.nube` en la vista.

## Efectos y riesgos del CLI

La inspección estática encontró estas llamadas en la ruta de `theme check` con un `--theme-id` explícito:

1. `GET /v1/7400935/theme-installations/14828608` (metadata).
2. `GET /v1/7400935/theme-installations/14828608/file-hashes` (hashes).
3. `POST /v1/7400935/theme-installations/14828608/files/validate` (cuerpo `upsert` de validación).

El uso explícito de `--theme-id` evita el listado de instalaciones. La fuente de `theme check` no invoca `push`, `publish`, `watch`, fork ni delete y no escribe archivos del tema. Hay dos salvedades que impiden ejecutar el CLI sin controles adicionales:

- `ThemeApiClient.request` habilita **hasta 6 intentos** por solicitud, con timeout de **120 s por intento**. `validateFiles` no desactiva los reintentos. El comando no ofrece flag para anularlos.
- `fetch` no fija `redirect: "error"`; Node sigue redirects por defecto. La herramienta tampoco limita por sí sola el host al endpoint permitido.

Además, la CLI habilita telemetría por defecto si no está deshabilitada y puede guardar un ID global. En una ejecución futura se requiere `TIENDANUBE_CLI_TELEMETRY_ENABLED=0` (y `DO_NOT_TRACK=1`) para que no envíe telemetría ni escriba su configuración de telemetría. El entorno local de preflight no modificó esa configuración.

Existe evidencia histórica de que el endpoint no persistió otros dos archivos el 12 de noviembre: [recibo anterior](../../indexability-20261112/three-issues/operations/native-template-validation.json). Ese recibo y su respuesta `valid:true` son solo precedente sobre la operación; **no validan este candidato ni prueban el estado actual del servicio**.

## Preflight offline realizado

Comando local ejecutado, sin invocar la CLI ni hacer red:

```bash
node reports/rhino-performance/performance-html-js-20261117/native-preflight-20261118/offline-preflight.mjs
```

Resultado: exit 0; SHA256 exactos, vista con dos archivos, reglas fuente de selección confirmadas y cuerpo de validación identificado. No se ejecutó `tiendanube theme check`, `theme diff`, POST, GET remoto ni Lighthouse. El primer intento del script no resolvió el espacio de la ruta (`%20`) y devolvió lista vacía; se corrigió usando `fileURLToPath`, y el resultado final es el que consta en el JSON. No se tocaron archivos de candidatos durante esa corrección.

## Secuencia futura, aún no autorizada

La invocación base debe correr con CWD en `virtual-workspace/` y el ejecutable CLI fijado por hash. Requiere un wrapper de red externo al CLI que:

- Solo permita el host API aprobado y los dos GET de metadata/hash y el POST `files/validate` especificados arriba; rechace todo lo demás.
- Fuerce redirect `error`.
- Permita una sola tentativa de red por endpoint y bloquee cualquier retry automático del CLI antes de que salga a red.
- Deshabilite telemetría mediante variables de entorno.
- Verifique antes del POST que el `upsert` incluye exactamente las dos rutas y que el SHA256 de cada contenido coincide con el manifiesto; si no, rechace y detenga.
- Capture el hash del cuerpo/resultado de file-hashes antes y después y compruebe igualdad, sin guardar el contenido remoto completo.

Si ese wrapper/egress no está disponible o falla, no ejecutar el CLI. El comando base preparado —**no ejecutar sin la futura guardia y autorización**— es:

```bash
cd reports/rhino-performance/performance-html-js-20261117/native-preflight-20261118/virtual-workspace
TIENDANUBE_CLI_TELEMETRY_ENABLED=0 DO_NOT_TRACK=1 tiendanube theme check --theme-id 14828608
```

Para la lectura posterior de integridad, `tiendanube theme diff --theme-id 14828608 --json` solo calcula diferencias; también requiere la misma guardia, telemetría desactivada y permiso expreso. No es validación de render y no debe producir POST. Los hashes pre/post deben quedar en recibos con los métodos/endpoints observados.

## Qué no valida

`theme check` valida las comprobaciones de guardado expuestas por el servidor (sintaxis Twig/schema/tamaño, según CLI/recibo anterior). No renderiza templates con contexto, no ejecuta `resolve_media`, ni comprueba HTML, `currentSrc`, `srcset` real, `loading`, prioridad, selección de breakpoint, dimensiones, `auto_height`, CLS, alt contextual, editor Ipanema ni otros consumidores en página. Para eso hace falta una fase posterior de render/QA autorizada; no se puede hacer con el endpoint de validación solamente.

## Condiciones de interrupción y reversión

Detener sin POST si cambian los hashes, el ID/host, la versión/hash del CLI, la vista contiene archivos adicionales, alguno de los dos archivos no aparece en el diff remoto, el guard no puede demostrar cero retries/redirects/telemetría o existe cambio remoto ajeno. La operación no escribe archivos, por lo que no habría reversión remota; la vista virtual se descarta únicamente después de conservar recibos. Si la lectura post muestra cualquier cambio, detenerse y reportarlo; no restaurar ni sobrescribir archivos remotos.

## Manifiesto

`manifest.json` registra hashes de candidatos, copias virtuales, CLI, script offline y resultados. El SHA256 del manifiesto está en `manifest.sha256`.
