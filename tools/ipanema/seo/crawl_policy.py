"""Frontera de red del crawler: GET, origen exacto, IP pública fijada y presupuestos."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import base64
import http.client
import ipaddress
import math
import re
import socket
import ssl
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import parse_qsl, unquote, urlencode, urljoin, urlsplit, urlunsplit
import zlib

from ..core import IpanemaError, safe_url

AGENT = 'IAIpanemaAudit/4.0'
PRIVATE = re.compile(r'/(?:account|accounts|customer|customers|cuenta|mi-cuenta|cart|carrito|checkout|checkouts|admin|login|logout|password|register|orders|pedidos|subscriptions|suscripciones)(?:/|$)', re.I)
ACTIONS = re.compile(r'(?:add.to.cart|cart/add|cart/update|cart/remove|agregar.al.carrito|comprar|add_to_cart)', re.I)
ASSET = re.compile(r'\.(?:jpg|jpeg|png|webp|avif|gif|svg|ico|mp4|webm|mp3|pdf|zip|css|js|woff2?|ttf)(?:$|/)', re.I)


def normalize(url, base=None):
    """No inventa páginas ni elimina parámetros de negocio para crear equivalencias."""
    if not isinstance(url, str) or len(url) > 2048 or re.search(r'[\x00-\x20\x7f\\]', url):
        raise IpanemaError('URL inválida o demasiado larga.')
    value = urljoin(base, url) if base else url
    u = urlsplit(value)
    if not u.hostname or '%' in u.netloc or u.hostname.endswith('.'):
        raise IpanemaError('Host ambiguo.')
    value = urlunsplit((u.scheme.lower(), u.netloc.lower(), u.path or '/', u.query, ''))
    safe_url(value, local=False)
    u = urlsplit(value)
    if u.port not in (None, 443):
        raise IpanemaError('Puerto no permitido en rastreo real.')
    host = u.hostname.encode('idna').decode('ascii')
    query = parse_qsl(u.query, keep_blank_values=True, max_num_fields=12)
    if len({k for k, _ in query}) != len(query):
        raise IpanemaError('Parámetros repetidos no permitidos.')
    return urlunsplit(('https', host, u.path or '/', urlencode(sorted(query)), ''))


@dataclass(frozen=True)
class Limits:
    max_urls: int = 30
    max_depth: int = 4
    max_requests: int = 60
    requests_per_second: float = 0.5
    max_seconds: float = 120
    timeout: float = 10
    max_bytes: int = 2_000_000
    max_sitemaps: int = 6
    max_sitemap_entries: int = 2000
    max_variants_per_path: int = 4
    max_redirects: int = 5
    max_discovered_urls: int = 2000
    max_edges: int = 10000
    concurrency: int = 1

    def validate(self):
        bounds = {'max_urls': (1, 500), 'max_depth': (0, 12), 'max_requests': (1, 1000),
                  'max_bytes': (100, 5_000_000), 'max_sitemaps': (0, 20),
                  'max_sitemap_entries': (1, 10000), 'max_variants_per_path': (1, 20),
                  'max_redirects': (0, 10), 'max_discovered_urls': (1, 10000),
                  'max_edges': (1, 50000), 'concurrency': (1, 1)}
        for key, (low, high) in bounds.items():
            value = getattr(self, key)
            if type(value) is not int or not low <= value <= high:
                raise IpanemaError('Límite inválido: ' + key)
        for key, low, high in [('requests_per_second', 0.05, 2), ('max_seconds', 1, 1800), ('timeout', 0.1, 30)]:
            value = getattr(self, key)
            if not isinstance(value, (int, float)) or not math.isfinite(value) or not low <= value <= high:
                raise IpanemaError('Límite inválido: ' + key)
        return self


class Policy:
    def __init__(self, home, limits=None, *, allow_query=('page', 'page_part')):
        self.home = normalize(home)
        self.origin = urlunsplit((*urlsplit(self.home)[:2], '', '', ''))
        if urlsplit(self.home).path != '/' or urlsplit(self.home).query:
            raise IpanemaError('El crawler comienza en la home del origen registrado.')
        self.limits = (limits or Limits()).validate()
        if any(not re.fullmatch(r'[a-zA-Z_][a-zA-Z0-9_]{0,39}', k) for k in allow_query):
            raise IpanemaError('Allowlist de parámetros inválida.')
        self.allow_query = frozenset(allow_query)

    def check(self, url, *, document=False):
        value = normalize(url, self.home)
        u = urlsplit(value)
        if urlunsplit((u.scheme, u.netloc, '', '', '')) != self.origin:
            raise IpanemaError('Origen externo no autorizado.')
        path = u.path
        for _ in range(3):
            path = unquote(path)
        if '\\' in path or re.search(r'[\x00-\x1f\x7f]', path) or PRIVATE.search(path) or ACTIONS.search(path):
            raise IpanemaError('Área privada o acción excluida.')
        if any(part in ('.', '..') for part in path.split('/')) or '//' in path:
            raise IpanemaError('Ruta ambigua.')
        query = parse_qsl(u.query, keep_blank_values=True)
        for key, value_part in query:
            if key not in self.allow_query or not value_part or len(value_part) > 256:
                raise IpanemaError('Filtro, búsqueda o parámetro no autorizado.')
            if key == 'page' and (not value_part.isdigit() or not 1 <= int(value_part) <= 1000):
                raise IpanemaError('Página fuera del contrato acotado.')
        if not document and ASSET.search(path):
            raise IpanemaError('Recurso no HTML excluido del crawler.')
        return value


def public_addresses(host):
    try:
        addresses = sorted({row[4][0] for row in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)})
    except OSError:
        raise IpanemaError('No se pudo resolver el host autorizado.') from None
    if not addresses or any(not ipaddress.ip_address(ip).is_global or ipaddress.ip_address(ip).is_multicast for ip in addresses):
        raise IpanemaError('IP privada, reservada o no global: red bloqueada.')
    return addresses


class _PinnedTLS(http.client.HTTPSConnection):
    def __init__(self, host, address, timeout):
        super().__init__(host, timeout=timeout, context=ssl.create_default_context())
        self.address = address

    def connect(self):
        # La conexión utiliza exactamente la IP validada, con SNI/certificado del host.
        sock = socket.create_connection((self.address, 443), self.timeout)
        try:
            self.sock = self._context.wrap_socket(sock, server_hostname=self.host)
        except Exception:
            sock.close()
            raise


def _https_get_once(url, *, timeout, max_bytes):
    u = urlsplit(url)
    address = public_addresses(u.hostname)[0]
    connection = _PinnedTLS(u.hostname, address, timeout)
    try:
        connection.request('GET', urlunsplit(('', '', u.path or '/', u.query, '')),
                           headers={'User-Agent': AGENT, 'Accept': 'text/html,application/xml,text/plain', 'Accept-Encoding': 'identity'})
        response = connection.getresponse()
        headers = {}
        for key, value in response.getheaders():
            key = key.lower()
            if key in ('content-type', 'content-encoding', 'location', 'x-robots-tag'):
                if key == 'location' and key in headers:
                    raise IpanemaError('Location múltiple: no se sigue una redirección ambigua.')
                if key == 'x-robots-tag' and key in headers:
                    headers[key] = [*(headers[key] if isinstance(headers[key], list) else [headers[key]]), value]
                else:
                    headers[key] = value
        if response.status in (403, 429):
            return {'status': response.status, 'headers': headers, 'body': b''}
        body = response.read(max_bytes + 1)
        if len(body) > max_bytes:
            raise IpanemaError('Respuesta supera el presupuesto de bytes.')
        if headers.get('content-encoding') == 'gzip' or body.startswith(b'\x1f\x8b'):
            decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
            body = decoder.decompress(body, max_bytes + 1)
            if len(body) > max_bytes or decoder.unconsumed_tail or not decoder.eof:
                raise IpanemaError('Respuesta gzip excedida o incompleta.')
        elif headers.get('content-encoding', 'identity') != 'identity':
            raise IpanemaError('Codificación HTTP no admitida.')
        return {'status': response.status, 'headers': headers, 'body': body}
    except (OSError, http.client.HTTPException, zlib.error):
        raise IpanemaError('Fallo de transporte; sin reintentos.') from None
    finally:
        connection.close()


def https_get(url, *, timeout, max_bytes):
    """Deadline real también durante DNS/TLS/headers; no proxy ni auth heredados.

    El hijo ejecuta únicamente nuestro cliente GET y muere al agotarse el timeout.
    No es un runtime de modelos ni ejecuta contenido descargado.
    """
    boot = ('import sys,json,base64;sys.path.insert(0,sys.argv[1]);'
            'from ipanema.seo.crawl_policy import _https_get_once;'
            'r=_https_get_once(sys.argv[2],timeout=float(sys.argv[3]),max_bytes=int(sys.argv[4]));'
            'r["body"]=base64.b64encode(r["body"]).decode("ascii");print(json.dumps(r))')
    try:
        result = subprocess.run([sys.executable, '-I', '-c', boot, str(Path(__file__).resolve().parents[2]),
                                 url, str(timeout), str(max_bytes)], env={}, capture_output=True,
                                timeout=timeout, check=False)
        if result.returncode or len(result.stdout) > max_bytes * 2 + 200000:
            raise IpanemaError('Fallo del cliente GET acotado; sin reintentos.')
        row = __import__('json').loads(result.stdout)
        row['body'] = base64.b64decode(row['body'], validate=True)
        return row
    except (subprocess.TimeoutExpired, OSError, ValueError, KeyError):
        raise IpanemaError('Deadline o fallo de transporte; sin reintentos.') from None


class Fetcher:
    def __init__(self, policy, *, allow_network=False, transport=None, clock=time.monotonic, sleep=time.sleep):
        if not allow_network and transport is None:
            raise IpanemaError('Red deshabilitada: se requiere --allow-network.')
        self.policy, self.transport = policy, transport or https_get
        self.clock, self.sleep = clock, sleep
        self.started, self.last = clock(), None
        self.calls, self.stop_reason = 0, None
        self.interval = 1 / policy.limits.requests_per_second
        self.log = []

    def get(self, url, *, document=False):
        url = self.policy.check(url, document=document)
        limits = self.policy.limits
        if self.stop_reason:
            raise IpanemaError('Run detenido; no se permiten nuevas solicitudes.')
        if self.calls >= limits.max_requests:
            self.stop_reason = 'request_budget'
            raise IpanemaError('Presupuesto de solicitudes agotado.')
        delay = max(0, self.interval - (self.clock() - self.last)) if self.last is not None else 0
        if self.clock() - self.started + delay >= limits.max_seconds:
            self.stop_reason = 'time_budget'
            raise IpanemaError('Presupuesto de tiempo agotado.')
        self.sleep(delay)
        self.last, self.calls = self.clock(), self.calls + 1
        try:
            row = self.transport(url, timeout=min(limits.timeout, limits.max_seconds - (self.clock() - self.started)), max_bytes=limits.max_bytes)
            status, body = row['status'], row.get('body', b'')
            if status in (403, 429):
                self.stop_reason = 'http_' + str(status)
                body = b''
            if isinstance(body, str):
                body = body.encode('utf-8')
            if len(body) > limits.max_bytes:
                raise IpanemaError('Respuesta supera el presupuesto de bytes.')
            self.log.append({'url': url, 'status': status, 'bytes': len(body), 'method': 'GET'})
            if status in (403, 429):
                self.stop_reason = 'http_' + str(status)
            if re.search(rb'(?:<title[^>]*>[^<]*(?:captcha|just a moment|access denied)|cf-chl-|g-recaptcha|hcaptcha)', body[:200000], re.I):
                self.stop_reason = self.stop_reason or 'access_challenge'
            if self.clock() - self.started >= limits.max_seconds:
                self.stop_reason = self.stop_reason or 'time_budget'
            return {'url': url, 'status': status, 'headers': {k.lower(): v for k, v in row.get('headers', {}).items()
                    if k.lower() in ('content-type', 'location', 'x-robots-tag')}, 'body': body}
        except IpanemaError:
            raise
        except Exception:
            raise IpanemaError('Transporte fallido; cuerpo y secretos no se registran.') from None

    def provenance(self):
        return {'limits': asdict(self.policy.limits), 'requests': self.calls,
                'elapsed_seconds': round(self.clock() - self.started, 3), 'stop_reason': self.stop_reason,
                'concurrency_actual': 1, 'remote_mutations': False, 'request_log': self.log}
