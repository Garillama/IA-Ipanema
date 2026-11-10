"""Servicio común CLI/MCP: origen, permiso, parada, caché privada y presupuesto."""
from __future__ import annotations
from contextlib import nullcontext
import datetime as dt
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import re
import subprocess
import time
from urllib.parse import urlsplit, urlunsplit, parse_qsl, unquote
from ..core import IpanemaError, now
from ..seo.adapters import authorize_url
from ..access.policy import Policy, fingerprint
from . import model, providers


def checked_url(project, value):
    authorize_url(project, value)
    u = urlsplit(value)
    if u.scheme != 'https' or u.username or u.password or u.fragment or u.port not in (None,443):
        raise IpanemaError('Se requiere URL pública HTTPS del origen registrado, sin credenciales ni fragmento.')
    host = (u.hostname or '').lower()
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        address = None
    if address is not None and not address.is_global or address is None and ('.' not in host or host.endswith(('.local','.localhost'))):
        raise IpanemaError('Destino privado no permitido.')
    for key, _ in parse_qsl(u.query):
        if model.SENSITIVE.search(unquote(unquote(key))):
            raise IpanemaError('La URL contiene parámetros sensibles; no se enviará a Google.')
    if re.search(r'/(?:admin|checkout|password|logout)(?:/|$)', unquote(u.path), re.I):
        raise IpanemaError('Ruta privada/comercial no permitida.')
    return value


def url_identity(value):
    u = urlsplit(value)
    return urlunsplit((u.scheme, u.netloc, u.path or '/', u.query, ''))


def options(project, source, url=None, device='mobile', categories=None, locale='es', scope='url', period_count=25):
    if source not in providers.ENDPOINTS or device not in ('mobile','desktop') or scope not in ('url','origin'):
        raise IpanemaError('Fuente, dispositivo o granularidad inválidos.')
    url = checked_url(project, url or project.data.get('public_url') or '')
    categories = sorted(set(categories or model.CATEGORIES))
    if not categories or set(categories) - set(model.CATEGORIES) or not re.fullmatch(r'[a-z]{2,3}(?:[-_][A-Za-z]{2,8})?', locale):
        raise IpanemaError('Categorías o locale inválidos.')
    if type(period_count) is not int or not 1 <= period_count <= 40:
        raise IpanemaError('History admite 1–40 periodos con el contrato verificado.')
    u = urlsplit(url)
    return {'source': source, 'url': url, 'origin': u.scheme + '://' + u.netloc,
            'device': device, 'categories': categories, 'locale': locale, 'scope': scope,
            'form_factor': 'PHONE' if device == 'mobile' else 'DESKTOP', 'period_count': period_count,
            'metrics': list(model.FIELD_METRICS.values()), 'contract': '2026-11-10-v1'}


def private_dir(path, root):
    for candidate in reversed([path, *path.parents]):
        if candidate == root or root in candidate.parents:
            if candidate.is_symlink():
                raise IpanemaError('Almacén privado con symlink rechazado.')
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    path.chmod(0o700)
    return path


def load_private(path):
    if not path.exists() and not path.is_symlink():
        return None
    if path.is_symlink() or path.stat().st_mode & 0o077:
        raise IpanemaError('Archivo privado inseguro.')
    if path.stat().st_size > 12_000_000:
        raise IpanemaError('Archivo privado excesivo.')
    try:
        return json.loads(path.read_text(), parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
    except (ValueError, UnicodeError):
        return None


def save_private(path, value):
    # Atomic replacement; never follow an existing or temporary symlink.
    import tempfile
    if path.is_symlink():
        raise IpanemaError('Archivo privado con symlink rechazado.')
    fd, temp = tempfile.mkstemp(dir=path.parent, prefix='.write-')
    try:
        with os.fdopen(fd, 'w') as stream:
            json.dump(value, stream, ensure_ascii=False, allow_nan=False)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


class Service:
    def __init__(self, project, *, transport=providers.request, clock=time.time, sleep=time.sleep, max_calls=4):
        self.project, self.transport, self.clock, self.sleep = project, transport, clock, sleep
        self.policy = Policy(project)
        self.root = private_dir(project.root / '.local/performance' / project.id, project.root)
        self.cfg = project.data.get('google', {}).get('performance', {})
        self.attempts, self.max_calls = 0, max_calls
        if type(max_calls) is not int or not 1 <= max_calls <= 10:
            raise IpanemaError('Presupuesto de ejecución: 1–10 solicitudes.')

    def setting(self, key, default, lower, upper):
        value = self.cfg.get(key, default)
        if type(value) not in (int,float) or not lower <= value <= upper:
            raise IpanemaError('Configuración performance inválida: ' + key)
        return value

    def read(self, source, *, authorized=False, already_locked=False, refresh=False, **kwargs):
        if not authorized:
            raise IpanemaError('Requiere permiso de lectura de red explícito (--allow-network o grant MCP).')
        if type(refresh) is not bool:
            raise IpanemaError('refresh debe ser booleano.')
        self.read_start = self.attempts
        opt = options(self.project, source, **kwargs)
        provider = 'psi' if source == 'pagespeed' else 'crux'
        with nullcontext() if already_locked else self.policy.locked():
            if self.policy.stop_path(provider).exists():
                return self.envelope(opt, {'status':'provider_stopped'})
            cache_id = hashlib.sha256(json.dumps({'project':self.project.id, 'config':fingerprint(self.project), 'options':opt}, sort_keys=True).encode()).hexdigest()
            path = self.root / (cache_id + '.json')
            ttl = self.setting('cache_ttl_seconds', 86400, 0, 604800)
            cached = load_private(path)
            if (not refresh and isinstance(cached, dict) and cached.get('project') == self.project.id and cached.get('request') == opt
                    and type(cached.get('cached_at')) in (int,float) and 0 <= self.clock() - cached['cached_at'] < ttl
                    and isinstance(cached.get('result'), dict) and cached.get('result', {}).get('status') in ('observed','partial','insufficient_field_data')):
                result = cached['result']
                result['cache_hit'] = True
                result['network_attempts'] = 0
                result['retrieved_at'] = now()
                return result
            env_name = self.cfg.get('pagespeed_key_env' if source == 'pagespeed' else 'crux_key_env', '')
            key = os.environ.get(env_name) if re.fullmatch(r'IPANEMA_[A-Z0-9_]+_KEY', env_name) else None
            if not key:
                return self.envelope(opt, {'status':'credentials_unavailable', 'network_attempts':0})
            retries = int(self.setting('max_retries', 1, 0, 2))
            timeout = self.setting('timeout_seconds', 90, 5, 180)
            for retry in range(retries + 1):
                budget = self.reserve(provider)
                if budget:
                    return self.envelope(opt, {'status':budget})
                try:
                    raw = self.transport(source, opt, key, timeout)
                    if not isinstance(raw, dict):
                        raise providers.Failure('invalid_response')
                    if source == 'pagespeed':
                        lhr = raw.get('lighthouseResult')
                        if not isinstance(lhr, dict):
                            raise providers.Failure('invalid_response')
                        for url_field in (raw.get('id'), lhr.get('requestedUrl'), lhr.get('finalUrl'), lhr.get('finalDisplayedUrl')):
                            if url_field:
                                try:
                                    checked_url(self.project, url_field)
                                except IpanemaError:
                                    raise providers.Failure('redirect_not_authorized') from None
                        if not isinstance(lhr.get('requestedUrl'), str) or url_identity(lhr['requestedUrl']) != url_identity(opt['url']):
                            raise providers.Failure('identity_mismatch')
                    if source != 'pagespeed':
                        identity = (raw.get('record') or {}).get('key') or {}
                        returned = identity.get(opt['scope'])
                        if returned:
                            try:
                                checked_url(self.project, returned)
                            except IpanemaError:
                                raise providers.Failure('identity_mismatch') from None
                    safe = model.sanitize(raw, (key,))
                    result = model.lighthouse(safe, opt) if source == 'pagespeed' else model.crux(safe, opt)
                    result['response_sha256'] = hashlib.sha256(json.dumps(raw, sort_keys=True, allow_nan=False).encode()).hexdigest()
                    result = self.envelope(opt, result)
                    break
                except providers.Failure as error:
                    if error.http in (403,429):
                        self.policy.stop(provider, error.status)
                    if error.status == 'not_found' and source != 'pagespeed':
                        result = self.envelope(opt, {'status':'insufficient_field_data', 'http_status':404})
                        break
                    retryable = error.status == 'network_error' or error.http in (500,502,503,504)
                    if retryable and retry < retries:
                        self.sleep(min(2 ** retry, 4))
                        continue
                    return self.envelope(opt, {'status':error.status, 'http_status':error.http})
                except (ValueError, TypeError, KeyError, AttributeError):
                    return self.envelope(opt, {'status':'invalid_response'})
            if result['status'] in ('observed','partial','insufficient_field_data'):
                save_private(path, {'project':self.project.id, 'request':opt, 'cached_at':self.clock(), 'result':result})
            return result

    def reserve(self, provider):
        if self.attempts >= self.max_calls:
            return 'run_budget_exhausted'
        path = self.root / ('budget-' + provider + '.json')
        budget = load_private(path)
        if path.exists() and not isinstance(budget, dict):
            return 'budget_invalid'
        budget = budget or {}
        day = dt.datetime.fromtimestamp(self.clock(), dt.timezone.utc).date().isoformat()
        count = budget.get('count', 0) if budget.get('day') == day else 0
        if type(count) is not int or count < 0:
            return 'budget_invalid'
        if count >= self.setting('daily_request_limit', 20, 1, 200):
            return 'daily_budget_exhausted'
        save_private(path, {'project':self.project.id, 'day':day, 'count':count + 1})
        self.attempts += 1
        return None

    def envelope(self, opt, result):
        result.update(project=self.project.id, source=opt['source'], request=opt,
                      retrieved_at=now(), cache_hit=False, untrusted_external_data=True,
                      network_attempts=self.attempts - self.read_start)
        return result


def persist(project, sources):
    from ..core import write_json
    run = project.new_run('performance')
    findings = [f for result in sources.values() for f in model.findings(result, result.get('request',{}).get('url'), result.get('request',{}).get('device'))]
    report = {'kind':'performance-intelligence', 'project':project.id, 'at':now(), 'sources':sources,
              'findings':findings, 'proposals':[], 'validation':{'theme_changed':False,'production_changed':False,
              'external_request_attempted':any(x.get('network_attempts',0) > 0 for x in sources.values())}, 'report':str(run/'performance.json')}
    write_json(run / 'performance.json', report)
    return report


def local(project, *, url=None, device='mobile', runs=3, authorized=False):
    if not authorized:
        raise IpanemaError('Lighthouse remoto requiere --allow-network.')
    url = checked_url(project, url or project.data.get('public_url') or '')
    if device not in ('mobile','desktop') or type(runs) is not int or not 1 <= runs <= 5:
        raise IpanemaError('Perfil Lighthouse inválido (1–5 muestras).')
    run = project.new_run('lighthouse-job')
    job = {'url':url, 'device':device, 'runs':runs, 'categories':list(model.CATEGORIES), 'locale':'es'}
    (run/'job.json').write_text(json.dumps(job))
    u = urlsplit(url)
    # Deliberate whitelist: no customer credentials, API keys or browser session inherited.
    env = {k:v for k,v in os.environ.items() if k in ('PATH','LANG','LC_ALL','DISPLAY','IPANEMA_CHROME_PATH','IPANEMA_NODE_MODULE_ROOT')}
    env.update(IPANEMA_ALLOW_NETWORK='1', IPANEMA_PUBLIC_URL=url, IPANEMA_ALLOWED_ORIGINS=u.scheme+'://'+u.netloc,
               IPANEMA_EVIDENCE_DIR=str(run/'browser'))
    try:
        process = subprocess.run(['node',str(project.root/'tools/lighthouse_audit.mjs'),'--job',str(run/'job.json')],
                                 cwd=project.root, env=env, capture_output=True, timeout=180*runs+30)
    except (OSError, subprocess.TimeoutExpired):
        return {'source':'lighthouse_local','status':'local_runtime_unavailable'}
    output = run/'browser'/'samples.json'
    if process.returncode or not output.is_file():
        return {'source':'lighthouse_local','status':'local_runtime_failed','exit_code':process.returncode,
                'limitations':['Salida del proceso no persistida: puede incluir URLs o datos privados.']}
    try:
        samples = json.loads(output.read_text())
        normalized = [model.lighthouse(sample, {**job,'network_policy':'guarded-read-only'}, source='lighthouse_local') for sample in samples]
        for sample in normalized:
            for field in ('url','final_url'):
                value = sample.get('profile', {}).get(field)
                if not isinstance(value, str):
                    return {'source':'lighthouse_local','status':'local_incomplete_response'}
                checked_url(project, value)
        result = model.summarize(normalized)
    except (IpanemaError, ValueError, TypeError, KeyError, AttributeError):
        # Keep earlier PSI/CrUX results in audit; do not abort report persistence.
        return {'source':'lighthouse_local','status':'local_invalid_response'}
    result['request'] = job
    result['source'] = 'lighthouse_local'
    return result
