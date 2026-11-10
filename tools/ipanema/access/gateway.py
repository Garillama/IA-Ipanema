"""Mismo servicio para cualquier cliente MCP; REST SEO y DevTools se reutilizan."""
from __future__ import annotations

import json
import os
import re

from ..core import IpanemaError, now, redact, write_json
from ..seo.adapters import OfficialREST, ReadOnlyAdapter, prepare
from .devtools import DevTools
from .policy import Policy


def schema(properties=None, required=None):
    return {'type': 'object', 'properties': properties or {}, 'required': required or [], 'additionalProperties': False}


REQUEST = schema({'request': {'type': 'object'}}, ['request'])
DEFINITIONS = {
    'devtools_open': ('Abrir una URL del origen autorizado en perfil aislado. Sin interacciones comerciales.', schema({'url': {'type': 'string'}}, ['url'])),
    'devtools_snapshot': ('Leer snapshot accesible de la página autorizada.', schema()),
    'devtools_network': ('Listar peticiones de red; sin cuerpos ni cabeceras.', schema()),
    'devtools_console': ('Leer mensajes de consola.', schema()),
    'devtools_trace': ('Traza de carga con recarga y parada automática; CrUX desactivado.', schema()),
    'devtools_insight': ('Analizar insight de una traza de esta sesión.', schema({'insightSetId': {'type': 'string'}, 'insightName': {'type': 'string'}}, ['insightSetId', 'insightName'])),
    'gsc_search_analytics': ('Consultar Search Analytics en la propiedad registrada; filas parciales.', REQUEST),
    'gsc_inspect_url': ('Consultar estado conocido de indexación; no es inspección en vivo.', REQUEST),
    'gsc_sitemaps': ('Listar metadatos de sitemaps registrados; sin envío ni eliminación.', REQUEST),
    'analytics_run_report': ('Lectura opcional GA; requiere permiso específico de tarea.', REQUEST),
    'merchant_products': ('Lectura opcional de productos procesados Merchant.', REQUEST),
}


def validate_arguments(name, args):
    if name not in DEFINITIONS or not isinstance(args, dict):
        raise IpanemaError('Herramienta o argumentos inválidos.')
    contract = DEFINITIONS[name][1]
    if set(args) - set(contract['properties']) or set(contract['required']) - set(args):
        raise IpanemaError('Argumentos fuera del contrato permitido.')
    for key, value in args.items():
        expected = dict if contract['properties'][key]['type'] == 'object' else str
        if not isinstance(value, expected) or isinstance(value, str) and len(value) > 4000:
            raise IpanemaError('Tipo/tamaño de argumento inválido.')


class Gateway:
    def __init__(self, project, grant_id, *, devtools_factory=DevTools, rest_factory=OfficialREST):
        self.project, self.grant_id = project, grant_id
        self.policy = Policy(project)
        self.policy.load(grant_id)
        self.devtools_factory, self.rest_factory = devtools_factory, rest_factory
        self.browser = None

    def tools(self):
        grant = self.policy.load(self.grant_id)
        return [{'name': n, 'description': DEFINITIONS[n][0], 'inputSchema': DEFINITIONS[n][1],
                 'annotations': {'readOnlyHint': n not in ('devtools_open','devtools_trace'), 'destructiveHint': False}}
                for n in sorted(self.policy.tools(grant))]

    def call(self, name, arguments):
        validate_arguments(name, arguments)
        with self.policy.locked():
            grant = self.policy.consume(self.grant_id, name)
            provider, operation = name.split('_', 1)
            try:
                if provider == 'devtools':
                    if self.browser is None:
                        self.browser = self.devtools_factory(self.project, profile=grant.get('browser_profile', 'security'))
                    result = self.browser.call(name, arguments)
                else:
                    cfg = self.project.data.get('google', {}).get(provider, {})
                    env_name = cfg.get('oauth_token_env', '')
                    # Validate project/account/request before touching a credential or network.
                    prepare(self.project, provider, operation, arguments['request'])
                    token = os.getenv(env_name) if re.fullmatch(r'IPANEMA_[A-Z0-9_]+_TOKEN', env_name) else None
                    if provider == 'gsc' and token is None:
                        from .credentials import load_token
                        token = load_token(self.project)
                    if not token:
                        result = {'status': 'credentials_unavailable', 'account_access_tested': False}
                    else:
                        adapter = ReadOnlyAdapter(self.project, provider, self.rest_factory(lambda: token),
                                                  authorized=True, max_calls=1)
                        try:
                            result = adapter.read(operation, arguments['request'])
                        finally:
                            adapter.disconnect()
                if result['status'] in ('forbidden_stop', 'quota_stop'):
                    self.policy.stop(provider, result['status'])
                    if provider == 'devtools' and self.browser:
                        self.browser.close()
                        self.browser = None
                status = result.get('status', 'unknown')
            except Exception as exc:
                # No provider messages, tokens, browser text or response bodies in evidence.
                self.audit(grant, name, 'failed')
                raise IpanemaError('provider_operation_failed:' + type(exc).__name__) from None
            self.audit(grant, name, status)
            return redact(result)

    def audit(self, grant, tool, status):
        run = self.project.new_run('access')
        write_json(run / 'access.json', {'kind': 'access-observation', 'at': now(),
                   'project': self.project.id, 'agent': grant['agent'], 'task': grant['task'],
                   'tool': tool, 'status': status, 'untrusted_external_data': True,
                   'browser_profile': grant.get('browser_profile', 'security'),
                   'raw_payload_saved': False})

    def close(self):
        if self.browser:
            self.browser.close()


def serve(gateway, source, destination):
    """MCP stdio JSONL. stdout solo contiene protocolo; mensajes externos son datos."""
    initialized = False
    try:
        while True:
            line = source.readline(4_000_001)
            if not line:
                break
            if len(line) > 4_000_000:
                break
            request_id = None
            try:
                request = json.loads(line)
                if not isinstance(request, dict) or request.get('jsonrpc') != '2.0':
                    raise IpanemaError('invalid_request')
                request_id = request.get('id')
                method, params = request.get('method'), request.get('params', {})
                if 'id' not in request:
                    continue
                if method == 'initialize':
                    initialized = True
                    supported = ('2024-11-05', '2025-03-26', '2025-06-18', '2025-11-25')
                    version = params.get('protocolVersion')
                    result = {'protocolVersion': version if version in supported else '2025-06-18',
                              'capabilities': {'tools': {}}, 'serverInfo': {'name': 'ia-ipanema-access', 'version': '1.0.0'}}
                elif method == 'ping':
                    result = {}
                elif not initialized:
                    raise IpanemaError('initialize_required')
                elif method == 'tools/list':
                    result = {'tools': gateway.tools()}
                elif method == 'tools/call':
                    try:
                        data = gateway.call(params.get('name'), params.get('arguments', {}))
                        result = {'content': [{'type': 'text', 'text': json.dumps(data, ensure_ascii=False)}],
                                  'isError': data.get('status') != 'observed'}
                    except (IpanemaError, OSError, ValueError, KeyError, TypeError):
                        result = {'isError': True, 'content': [{'type': 'text', 'text': 'Operación bloqueada o proveedor no disponible. Consulta permisos y access doctor.'}]}
                else:
                    raise IpanemaError('method_not_supported')
                response = {'jsonrpc': '2.0', 'id': request_id, 'result': result}
            except (IpanemaError, ValueError, KeyError, TypeError, AttributeError):
                response = {'jsonrpc': '2.0', 'id': request_id, 'error': {'code': -32600, 'message': 'Invalid or unauthorized request'}}
            destination.write(json.dumps(response, ensure_ascii=False) + '\n')
            destination.flush()
    finally:
        gateway.close()
