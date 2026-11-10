"""Un único upstream DevTools fijado; perfil efímero por sesión, sin perfil personal."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import selectors
from urllib.parse import urlsplit

from ..core import IpanemaError, read_json
from .mcp import StdioClient

VERSION = '1.12.0'
INTEGRITY = 'sha512-lAGpH0zXT1ZdaPefP1KK/MvxwihOlu7VGQ7p4wbhD9OhN17vUC4KWk/ImUYR9DE4s+7r4r0ySV4xr2OkTa7ZMA=='
TOOLS = ('new_page', 'list_pages', 'take_snapshot', 'list_network_requests',
         'list_console_messages', 'performance_start_trace', 'performance_analyze_insight')


def installation(root):
    base = root / '.local/devtools'
    package = base / 'node_modules/chrome-devtools-mcp'
    entry = package / 'build/src/bin/chrome-devtools-mcp.js'
    if not entry.is_file():
        raise IpanemaError('DevTools no instalado; consulta reports/access/README.md.')
    metadata = read_json(package / 'package.json')
    lock = read_json(base / 'package-lock.json')
    pinned = lock.get('packages', {}).get('node_modules/chrome-devtools-mcp', {})
    if metadata.get('version') != VERSION or pinned.get('version') != VERSION or pinned.get('integrity') != INTEGRITY:
        raise IpanemaError('Versión/integridad registrada de DevTools no coincide con el pin.')
    if not shutil.which('node'):
        raise IpanemaError('Node no disponible.')
    return entry


def page_origin(project):
    value = project.data.get('qa_base_url') or project.data.get('public_url', '')
    u = urlsplit(value)
    if u.scheme not in ('http', 'https') or not u.hostname or u.username or u.password:
        raise IpanemaError('Origen de navegador no configurado.')
    return f'{u.scheme}://{u.netloc}'


def profile_origins(project, profile):
    origins = [page_origin(project)]
    if profile not in ('security', 'audit'):
        raise IpanemaError('Perfil desconocido.')
    if profile == 'audit':
        configured = project.data.get('browser', {}).get('devtools_audit_origins')
        if not isinstance(configured, list) or not configured:
            raise IpanemaError('Auditoría requiere orígenes de recursos comprobados y registrados.')
        for value in configured:
            u = urlsplit(value)
            if u.scheme not in ('https', 'http') or u.scheme == 'http' and u.hostname not in ('localhost', '127.0.0.1') or u.username or u.password or u.path or u.query or u.fragment or not u.hostname or '*' in value:
                raise IpanemaError('Origen de auditoría inválido; no se admiten comodines.')
            origins.append(value)
    return sorted(set(origins))


class BrowserController:
    def __init__(self, project, home, origins):
        env = {k: os.environ[k] for k in ('PATH', 'LANG', 'LC_ALL') if k in os.environ}
        env.update({'HOME': str(home), 'IPANEMA_PUBLIC_URL': page_origin(project),
                    'IPANEMA_ALLOWED_ORIGINS': page_origin(project), 'IPANEMA_ALLOW_NETWORK': '1',
                    'IPANEMA_RESOURCE_ORIGINS': ','.join(origins),
                    'IPANEMA_EVIDENCE_DIR': str(home / 'browser-evidence')})
        chrome = project.data.get('browser', {}).get('chrome_path')
        if chrome:
            env['IPANEMA_CHROME_PATH'] = chrome
        self.process = subprocess.Popen([shutil.which('node'), str(project.root / 'tools/access_browser.mjs')],
            cwd=home, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, start_new_session=True)
        try:
            self.metadata = self.receive()
        except Exception:
            self.close()
            raise

    def receive(self):
        with selectors.DefaultSelector() as selector:
            selector.register(self.process.stdout, selectors.EVENT_READ)
            if not selector.select(45):
                raise IpanemaError('browser_controller_timeout')
            raw = self.process.stdout.readline(10001)
        if not raw or len(raw) > 10000:
            raise IpanemaError('browser_controller_unavailable')
        return json.loads(raw)

    def open(self, url):
        self.process.stdin.write((json.dumps({'id': 1, 'operation': 'open', 'url': url}) + '\n').encode())
        self.process.stdin.flush()
        return self.receive()

    def close(self):
        import signal
        if self.process.poll() is None:
            os.killpg(self.process.pid, signal.SIGTERM)
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(self.process.pid, signal.SIGKILL)
                self.process.wait(timeout=5)
        self.process.stdin.close()
        self.process.stdout.close()


class DevTools:
    def __init__(self, project, *, profile='security'):
        self.project = project
        self.profile, self.origins = profile, profile_origins(project, profile)
        self.temporary = tempfile.TemporaryDirectory(prefix='ipanema-devtools-')
        self.home = Path(self.temporary.name)
        self.client = None
        self.controller = None
        try:
            entry = installation(project.root)
            chrome = project.data.get('browser', {}).get('chrome_path') or shutil.which('google-chrome')
            if not chrome:
                raise IpanemaError('Google Chrome no disponible.')
            version = subprocess.run([chrome, '--version'], capture_output=True, text=True, timeout=5)
            match = re.search(r'(\d+)\.', version.stdout)
            # allowedUrlPattern enforces subresources and redirects starting with Chrome 149.
            if not match or int(match[1]) < 149:
                raise IpanemaError('Chrome >=149 requerido para restringir red por origen; no se desactiva el sandbox.')
            env = {k: os.environ[k] for k in ('PATH', 'LANG', 'LC_ALL', 'TMPDIR') if k in os.environ}
            env.update({'HOME': str(self.home), 'CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS': '1',
                        'CHROME_DEVTOOLS_MCP_NO_UPDATE_CHECKS': '1'})
            # Discovery remains lazy; the protected dedicated browser starts on open.
            self.entry, self.env, self.chrome = entry, env, chrome
            self.start_client()
            self.page_id = None
        except Exception:
            self.close()
            raise

    def start_client(self, endpoint=None):
            command = [shutil.which('node'), str(self.entry),
                       '--no-usage-statistics', '--no-performance-crux', '--no-javascript-evaluation',
                       '--no-file-navigations', '--redact-network-headers', '--no-source-maps',
                       '--workspace=' + str(self.home),
                       '--no-category-input', '--no-category-emulation', '--no-category-memory']
            if endpoint:
                command.append('--ws-endpoint=' + endpoint)
            else:
                command += ['--headless', '--isolated', '--executable-path=' + self.chrome]
            command += ['--allowed-url-pattern=' + value + '/*' for value in self.origins]
            self.client = StdioClient(command, cwd=self.home, env=self.env)
            if self.client.initialized.get('serverInfo', {}).get('version') != VERSION:
                raise IpanemaError('El servidor no confirmó la versión fijada.')
            self.schemas = {t['name']: t for t in self.client.tools()}
            missing = set(TOOLS) - set(self.schemas)
            if missing:
                raise IpanemaError('Herramientas DevTools ausentes: ' + ', '.join(sorted(missing)))

    def discovery(self):
        return {'server_available': True, 'version': VERSION, 'tools_verified': list(TOOLS),
                'schemas_sha256': hashlib.sha256(json.dumps({n: self.schemas[n]['inputSchema'] for n in TOOLS}, sort_keys=True).encode()).hexdigest(),
                'browser_started': False, 'account_access_tested': False,
                'usage_statistics': False, 'performance_crux': False,
                'profile': self.profile, 'profile_isolation': 'ephemeral', 'resource_origins': self.origins,
                'allowed_origin': page_origin(self.project), 'writes_blocked': True}

    def raw(self, name, args):
        schema = self.schemas[name]['inputSchema']
        if set(args) - set(schema.get('properties', {})) or set(schema.get('required', [])) - set(args):
            raise IpanemaError('Contrato DevTools cambió; operación detenida.')
        return self.client.call(name, args)

    @staticmethod
    def pages(result):
        structured = result.get('structuredContent', {}).get('pages')
        if isinstance(structured, list):
            return {row['id']: row['url'] for row in structured
                    if type(row.get('id')) is int and isinstance(row.get('url'), str)}
        text = '\n'.join(c.get('text', '') for c in result.get('content', []) if c.get('type') == 'text')
        # 1.12.0 emits "id: title (URL) [selected]", or "id: URL" without title.
        pages = {}
        for match in re.finditer(r'(?m)^(\d+): (.+)$', text):
            label = re.sub(r' \[selected\]$', '', match[2])
            if label.endswith(')') and ' (' in label:
                label = label.rsplit(' (', 1)[1][:-1]
            if re.fullmatch(r'(?:https?://\S+|about:blank)', label):
                if int(match[1]) in pages:
                    raise IpanemaError('Lista de páginas ambigua.')
                pages[int(match[1])] = label
        return pages

    def check_page(self):
        if self.page_id is None:
            raise IpanemaError('Abre primero una URL con devtools_open en esta sesión.')
        pages = self.pages(self.raw('list_pages', {}))
        u = urlsplit(pages.get(self.page_id, ''))
        if f'{u.scheme}://{u.netloc}' != page_origin(self.project):
            raise IpanemaError('La página activa está fuera del origen autorizado.')

    def http_stop(self):
        args = {'pageId': self.page_id}
        result = self.raw('list_network_requests', args)
        text = '\n'.join(c.get('text', '') for c in result.get('content', []) if c.get('type') == 'text')
        statuses = re.findall(r'(?m)^reqid=\d+ [A-Z]+ \S+ \[(403|429)\]', text)
        if statuses:
            return {'status': 'forbidden_stop' if '403' in statuses else 'quota_stop', 'data': None}
        return None

    def call(self, tool, arguments):
        if tool == 'devtools_open':
            u = urlsplit(arguments['url'])
            if f'{u.scheme}://{u.netloc}' != page_origin(self.project) or u.username or u.password:
                raise IpanemaError('URL fuera del origen autorizado.')
            if self.controller is None:
                self.client.close()
                self.controller = BrowserController(self.project, self.home, self.origins)
                self.start_client(self.controller.metadata['endpoint'])
            if self.page_id is None:
                initial = self.pages(self.raw('list_pages', {}))
                blank = [pid for pid, value in initial.items() if value == 'about:blank']
                if len(blank) != 1:
                    raise IpanemaError('Navegador dedicado sin una pestaña inicial inequívoca.')
                self.raw('take_snapshot', {'pageId': blank[0]})
            opened = self.controller.open(arguments['url'])
            if opened.get('error'):
                return {'status': opened['error'], 'data': None}
            result = self.raw('list_pages', {})
            pages = self.pages(result)
            candidates = [pid for pid, url in pages.items() if url == arguments['url']]
            if len(candidates) != 1:
                raise IpanemaError('No se confirmó la URL exacta abierta; redirección o contrato diferente.')
            self.page_id = candidates[0]
        else:
            self.check_page()
            stopped = self.http_stop()
            if stopped:
                return stopped
            names = {'devtools_snapshot': 'take_snapshot', 'devtools_network': 'list_network_requests',
                     'devtools_console': 'list_console_messages', 'devtools_trace': 'performance_start_trace',
                     'devtools_insight': 'performance_analyze_insight'}
            name = names[tool]
            args = dict(arguments)
            if tool == 'devtools_trace':
                args = {'reload': True, 'autoStop': True}
            if 'pageId' in self.schemas[name]['inputSchema'].get('properties', {}):
                args['pageId'] = self.page_id
            result = self.raw(name, args)
            self.check_page()
        stopped = self.http_stop()
        if stopped:
            return stopped
        return {'status': 'observed', 'untrusted_external_data': True, 'data': result,
                'browser_profile': self.profile, 'resource_origins': self.origins,
                'limitations': ['Diagnóstico de laboratorio; no demuestra indexación ni INP de campo.',
                                'Solo recursos de orígenes registrados; comparar con el mismo perfil y política de lectura.']}

    def close(self):
        if self.client:
            self.client.close()
        if self.controller:
            self.controller.close()
        self.temporary.cleanup()
