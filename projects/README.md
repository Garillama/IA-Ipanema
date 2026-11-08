# Configuración de proyectos

`registry.json` contiene IDs y rutas a JSON compartidos. `ipanema.json` conserva la observación original, no una conexión viva. No almacenes credenciales en ninguno de estos archivos.

Selección: `python3 tools/ia.py --project ID …` → `IPANEMA_PROJECT` → `.local/config.json` → default del registro. `projects use ID` modifica únicamente la selección local ignorada.

La ruta del tema se resuelve desde la raíz del repositorio si es relativa, y admite `~` o variables de entorno definidas. Configura una ruta real con `IPANEMA_THEME_ROOT` o `projects/ID.local.json`:

```json
{"theme_root": "/ruta/real/al/tema"}
```

Ese archivo está ignorado; el compartido puede dejar `theme_root: null`. No se usa como fallback la ruta absoluta de la captura histórica. Al migrar este equipo se conservó su ubicación comprobada exclusivamente en el override local.

```bash
python3 tools/ia.py projects register tienda-dos --name "Tienda dos" --theme-root /ruta/real --url https://ejemplo.mitiendanube.com
python3 tools/ia.py projects use tienda-dos
python3 tools/ia.py doctor
```

Registrar no se conecta a Tiendanube ni descarga el tema. Sin tema se puede consultar el conocimiento; operaciones de código exigen `require_theme`. Un proyecto nuevo hereda referencias históricas Ipanema, señaladas como compatibilidad no comprobada, no conclusiones automáticamente válidas para esa tienda.

El JSON compartido admite name, id, environment, public_url, theme_installation_id, discovery_root, evidence_dir, qa y remote_observation. La observación remota contiene versión/variante/fork y fecha `verified_on`; el estado de conexión de doctor sigue `not_checked` hasta una comprobación nueva. No se invoca el CLI remoto automáticamente.

`qa.pages` mapea nombres a rutas reales: `"home":"/"` o `{"path":"/ruta/","expected_status":404,"expected_h1":1,"expect_canonical":false}`. No se deriva la URL de un template. `qa.widths`, `max_pages`, `budgets`, `visual` e `interactions` controlan pruebas. Los presupuestos son objetivos propuestos; las mediciones se guardan en runs nuevos.

Un override local también puede definir `qa_base_url` para un servidor de pruebas propio y `browser.chrome_path`. Los paquetes se buscan en node_modules local, `IPANEMA_NODE_MODULE_ROOT` y la instalación global del CLI existente; Chrome en caché de Puppeteer, PATH o `IPANEMA_CHROME_PATH`. No se instala nada automáticamente.

`qa.interactions` contiene pasos declarativos `click`, `press`, `select`, `assert_visible`, `assert_hidden`, `assert_focus`. Configura selectores después de inspeccionar la página. Enter/envío de formulario y acciones comerciales se rechazan. Ejemplo de fixture, no selectores universales Ipanema:

```json
{"name":"menu","page":"home","widths":[390],"steps":[
  {"action":"click","selector":"#menu-toggle"},
  {"action":"assert_visible","selector":"#menu"},
  {"action":"assert_focus","selector":"#menu"},
  {"action":"press","key":"Escape"},
  {"action":"assert_hidden","selector":"#menu"}
]}
```

Los runs deben estar fuera del tema y del discovery. No guardes cookies/headers/valores de campos; una contraseña de acceso autorizada se recibe solo por `IPANEMA_AUDIT_PASSWORD`, nunca como argumento CLI, JSON o URL. `--allow-network` es una constancia operativa del acceso autorizado, no autorización para escribir en la tienda.
