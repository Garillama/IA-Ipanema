"""OAuth escritorio PKCE en memoria; Google credentials nunca se escriben en evidencia."""
from __future__ import annotations

import base64
import datetime as dt
import hashlib
import hmac
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import Path
import secrets
import time
from urllib.parse import parse_qs, urlencode, urlsplit
from urllib.request import Request, build_opener
import webbrowser

from ..core import IpanemaError, now, read_json, write_json
from ..seo.adapters import OfficialREST, ProviderError, ReadOnlyAdapter, SCOPES, _NoRedirect, prepare
from .policy import Policy


def client_config(path):
    if not path.is_file() or path.is_symlink():
        raise IpanemaError('Cliente OAuth de escritorio no disponible.')
    cfg = read_json(path).get('installed', {})
    if not cfg.get('client_id') or not cfg.get('client_secret'):
        raise IpanemaError('Se necesita un cliente OAuth de tipo escritorio.')
    if cfg.get('auth_uri') != 'https://accounts.google.com/o/oauth2/auth' and cfg.get('auth_uri') != 'https://accounts.google.com/o/oauth2/v2/auth':
        raise IpanemaError('Endpoint OAuth no admitido.')
    if cfg.get('token_uri') != 'https://oauth2.googleapis.com/token':
        raise IpanemaError('Endpoint de token no admitido.')
    return cfg


def authorization_url(client_id, redirect, state, verifier):
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b'=').decode()
    return 'https://accounts.google.com/o/oauth2/v2/auth?' + urlencode({
        'client_id': client_id, 'redirect_uri': redirect, 'response_type': 'code',
        'scope': SCOPES['gsc'], 'state': state, 'code_challenge': challenge,
        'code_challenge_method': 'S256', 'access_type': 'online', 'include_granted_scopes': 'false'})


def callback_code(query, state):
    values = parse_qs(query)
    supplied = values.get('state', [''])
    if len(supplied) != 1 or not hmac.compare_digest(supplied[0], state):
        raise IpanemaError('OAuth state inválido.')
    if 'error' in values or len(values.get('code', [])) != 1:
        raise IpanemaError('Consentimiento no concedido.')
    return values['code'][0]


def authorize(path, *, timeout=300):
    cfg = client_config(path)
    state, verifier = secrets.token_urlsafe(32), secrets.token_urlsafe(48)
    outcome = {}
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            request = urlsplit(self.path)
            if request.path == '/start':
                self.send_response(302)
                self.send_header('Location', authorization)
                self.send_header('Cache-Control', 'no-store')
                self.end_headers()
                return
            if request.path != '/oauth/callback':
                self.send_error(404)
                return
            try:
                outcome['code'] = callback_code(request.query, state)
                message = b'Autorizacion recibida. Puedes cerrar esta pestana.'
                self.send_response(200)
            except IpanemaError:
                outcome['error'] = True
                message = b'Autorizacion no concedida o estado invalido.'
                self.send_response(400)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(message)
        def log_message(self, *args):
            pass
    with HTTPServer(('127.0.0.1', 0), Handler) as server:
        redirect = f'http://127.0.0.1:{server.server_port}/oauth/callback'
        authorization = authorization_url(cfg['client_id'], redirect, state, verifier)
        start = f'http://127.0.0.1:{server.server_port}/start'
        opened = webbrowser.open(start)
        print(json.dumps({'status': 'waiting_for_user_consent', 'local_authorization_url': start,
                          'browser_opened': opened, 'scope': SCOPES['gsc']}), flush=True)
        server.timeout = 1
        deadline = time.monotonic() + timeout
        while not outcome and time.monotonic() < deadline:
            server.handle_request()
    if 'code' not in outcome:
        raise IpanemaError('OAuth no autorizado o espera agotada; no se consulto Search Console.')
    body = urlencode({'client_id': cfg['client_id'], 'client_secret': cfg['client_secret'],
                      'grant_type': 'authorization_code', 'code': outcome.pop('code'),
                      'redirect_uri': redirect, 'code_verifier': verifier}).encode()
    try:
        request = Request('https://oauth2.googleapis.com/token', data=body,
                          headers={'Content-Type': 'application/x-www-form-urlencoded'})
        with build_opener(_NoRedirect()).open(request, timeout=30) as response:
            payload = json.loads(response.read(100000))
    except Exception:
        raise IpanemaError('Intercambio OAuth fallido; respuesta privada descartada.') from None
    if payload.get('scope') != SCOPES['gsc'] or not payload.get('access_token'):
        raise IpanemaError('Google no confirmo exclusivamente el scope de lectura solicitado.')
    return {'access_token': payload['access_token'], 'expires_in': payload.get('expires_in')}


def verify_live(project, token, url):
    policy = Policy(project)
    if policy.stop_path('gsc').exists():
        raise IpanemaError('GSC detenido previamente; revisar causa antes de nueva lectura.')
    req = prepare(project, 'gsc', 'sitemaps', {})
    transport = OfficialREST(lambda: token)
    try:
        site = transport.call('gsc', 'site_info', req)
    except ProviderError as exc:
        if exc.status in (403, 429):
            policy.stop('gsc', 'forbidden_stop' if exc.status == 403 else 'quota_stop')
        raise IpanemaError('No se pudo verificar acceso a la propiedad GSC; respuesta privada descartada.') from None
    if site.get('siteUrl') != req['siteUrl'] or site.get('permissionLevel') not in ('siteOwner', 'siteFullUser', 'siteRestrictedUser'):
        raise IpanemaError('Propiedad no verificada o cuenta sin acceso de lectura.')
    adapter = ReadOnlyAdapter(project, 'gsc', transport, authorized=True, max_calls=3)
    end = dt.date.today() - dt.timedelta(days=3)
    start = end - dt.timedelta(days=27)
    requests = [('search_analytics', {'startDate': str(start), 'endDate': str(end), 'dimensions': ['page'], 'rowLimit': 100}),
                ('inspect_url', {'inspectionUrl': url}), ('sitemaps', {})]
    observations = []
    try:
        for operation, request in requests:
            observation = adapter.read(operation, request)
            metadata = {'operation': operation, 'status': observation['status'],
                'observed_at': observation['at'], 'http_status': observation.get('http_status'),
                'live_google_api': getattr(transport, 'kind', None) == 'official_rest',
                'mock': getattr(transport, 'kind', None) != 'official_rest'}
            data = observation.get('data')
            if isinstance(data, dict):
                if operation == 'search_analytics':
                    metadata['row_count'] = len(data.get('rows', []))
                elif operation == 'inspect_url':
                    metadata['index_verdict'] = data.get('index_status', {}).get('verdict')
                    metadata['live_inspection'] = False
                else:
                    metadata['sitemap_count'] = len(data.get('sitemaps', []))
            observations.append(metadata)
            if observation['status'] in ('forbidden_stop', 'quota_stop'):
                policy.stop('gsc', observation['status'])
            if observation['status'] != 'observed':
                break
    finally:
        adapter.disconnect()
    return {'property_access_verified': True, 'permission_level': site['permissionLevel'],
            'scope': SCOPES['gsc'], 'operations': observations,
            'all_reads_observed': len(observations) == 3 and all(o['status']=='observed' for o in observations)}
