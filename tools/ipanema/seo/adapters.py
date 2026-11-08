"""Adaptadores de lectura: transporte inyectable, REST oficial y MCP sin instalación.

No inicia OAuth, procesos MCP ni cuentas. Los resultados son datos no confiables;
solo se proyectan campos conocidos. La API de inspección consulta el índice conocido.
"""
from __future__ import annotations

import datetime as dt
import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler

from ..core import IpanemaError, now, safe_url


SCOPES = {
    'gsc': 'https://www.googleapis.com/auth/webmasters.readonly',
    'analytics': 'https://www.googleapis.com/auth/analytics.readonly',
    # Merchant has no general read-only OAuth scope; operations are allowlisted here.
    'merchant': 'https://www.googleapis.com/auth/content',
}
OPERATIONS = {'gsc': ('search_analytics', 'inspect_url', 'sitemaps'),
              'analytics': ('run_report',), 'merchant': ('products',),
              'devtools': ('take_snapshot', 'list_network_requests', 'list_console_messages')}
MCP_READ_TOOLS = {
    ('gsc', 'search_analytics'): {'get_search_analytics', 'get_advanced_search_analytics', 'gsc_search_analytics'},
    ('gsc', 'inspect_url'): {'inspect_url_enhanced', 'gsc_inspect_url'},
    ('gsc', 'sitemaps'): {'get_sitemaps', 'list_sitemaps_enhanced', 'gsc_list_sitemaps'},
    ('analytics', 'run_report'): {'run_report'},
    ('devtools', 'take_snapshot'): {'take_snapshot'},
    ('devtools', 'list_network_requests'): {'list_network_requests'},
    ('devtools', 'list_console_messages'): {'list_console_messages'},
}


class ProviderError(Exception):
    def __init__(self, status, category='provider_error'):
        self.status, self.category = status, category
        super().__init__(category)  # Never include provider bodies/credentials in logs.


def _host(project):
    return urlsplit(safe_url(project.data.get('public_url', ''))).hostname


def authorize_url(project, url):
    safe_url(url)
    own = urlsplit(project.data.get('public_url', ''))
    dest = urlsplit(url)
    if (dest.scheme, dest.netloc) != (own.scheme, own.netloc):
        raise IpanemaError('Dominio/origen ajeno al proyecto activo.')
    return url


def _period(request):
    try:
        start, end = (dt.date.fromisoformat(request[k]) for k in ('startDate', 'endDate'))
    except (ValueError, KeyError, TypeError):
        raise IpanemaError('Se requieren startDate/endDate ISO reales.') from None
    if start > end:
        raise IpanemaError('Periodo invertido.')


def prepare(project, provider, operation, request):
    """Contrato canónico independiente del proveedor; rechaza parámetros desconocidos."""
    if operation not in OPERATIONS.get(provider, ()):
        raise IpanemaError('Operación no permitida; el adaptador solo expone lecturas declaradas.')
    if not isinstance(request, dict):
        raise IpanemaError('La petición debe ser un objeto.')
    cfg = project.data.get('google', {}).get(provider, {})
    if not isinstance(cfg, dict):
        raise IpanemaError('Configuración Google incompatible.')
    req = dict(request)
    if provider == 'gsc':
        site = req.get('siteUrl') or cfg.get('site_url')
        if not isinstance(site, str) or site != cfg.get('site_url'):
            raise IpanemaError('Propiedad Search Console no registrada para este proyecto.')
        if site.startswith('sc-domain:'):
            if site[10:] != _host(project):
                raise IpanemaError('La propiedad de dominio debe coincidir exactamente con la tienda.')
        else:
            authorize_url(project, site)
        req['siteUrl'] = site
        if operation == 'inspect_url':
            if set(req) - {'siteUrl', 'inspectionUrl', 'languageCode'}:
                raise IpanemaError('Campos de inspección desconocidos.')
            authorize_url(project, req.get('inspectionUrl', ''))
            if not site.startswith('sc-domain:') and not req['inspectionUrl'].startswith(site.rstrip('/') + '/') and req['inspectionUrl'] != site:
                raise IpanemaError('URL fuera del prefijo registrado en Search Console.')
        elif operation == 'search_analytics':
            if set(req) - {'siteUrl', 'startDate', 'endDate', 'dimensions', 'rowLimit', 'startRow', 'type', 'dataState', 'dimensionFilterGroups'}:
                raise IpanemaError('Campos Search Analytics desconocidos.')
            _period(req)
            dims = req.get('dimensions', ['page'])
            if not isinstance(dims, list) or set(dims) - {'query', 'page', 'country', 'device', 'date', 'searchAppearance', 'hour'}:
                raise IpanemaError('Dimensiones Search Analytics no admitidas.')
            req['dimensions'] = dims
            req.setdefault('rowLimit', 1000); req.setdefault('startRow', 0)
            if type(req['rowLimit']) is not int or not 1 <= req['rowLimit'] <= 25000 or type(req['startRow']) is not int or req['startRow'] < 0:
                raise IpanemaError('Límites de filas inválidos.')
            # Prefix properties already scope the API; domain properties are exact host.
            # Filter expressions never cause navigation or shell execution.
        elif set(req) != {'siteUrl'}:
            raise IpanemaError('sitemaps solo admite la propiedad registrada.')
    elif provider == 'analytics':
        if set(req) - {'property', 'startDate', 'endDate', 'dimensions', 'metrics', 'limit', 'dimensionFilter'}:
            raise IpanemaError('Campos de Analytics desconocidos.')
        prop = req.get('property') or cfg.get('property')
        if not re.fullmatch(r'properties/[0-9]+', str(prop)) or prop != cfg.get('property'):
            raise IpanemaError('Propiedad Analytics no registrada.')
        _period(req); req['property'] = prop
        req.setdefault('dimensions', ['landingPagePlusQueryString', 'hostName'])
        req.setdefault('metrics', ['sessions', 'engagedSessions', 'keyEvents', 'ecommercePurchases', 'purchaseRevenue'])
        allowed_dims = {'landingPagePlusQueryString', 'hostName', 'date', 'deviceCategory', 'country', 'sessionDefaultChannelGroup', 'sessionSourceMedium'}
        allowed_metrics = {'sessions', 'totalUsers', 'engagedSessions', 'engagementRate', 'keyEvents', 'ecommercePurchases', 'purchaseRevenue'}
        if not isinstance(req['dimensions'], list) or set(req['dimensions']) - allowed_dims or not isinstance(req['metrics'], list) or set(req['metrics']) - allowed_metrics:
            raise IpanemaError('Dimensiones/métricas Analytics fuera del contrato comprobado.')
        # The server applies an exact host filter, including properties shared by stores.
        own = {'filter': {'fieldName': 'hostName', 'stringFilter': {'matchType': 'EXACT', 'value': _host(project), 'caseSensitive': False}}}
        requested_filter = req.get('dimensionFilter')
        req['dimensionFilter'] = {'andGroup': {'expressions': [own, requested_filter]}} if requested_filter else own
        req.setdefault('limit', 1000)
        if type(req['limit']) is not int or not 1 <= req['limit'] <= 10000:
            raise IpanemaError('Límite Analytics inválido.')
    elif provider == 'merchant':
        if set(req) - {'account', 'pageSize', 'pageToken'}:
            raise IpanemaError('Campos Merchant desconocidos.')
        account = req.get('account') or cfg.get('account')
        if not re.fullmatch(r'accounts/[0-9]+', str(account)) or account != cfg.get('account'):
            raise IpanemaError('Cuenta Merchant no registrada.')
        req['account'] = account; req.setdefault('pageSize', 100)
        if type(req['pageSize']) is not int or not 1 <= req['pageSize'] <= 1000:
            raise IpanemaError('Tamaño de página Merchant inválido.')
    else:
        if not cfg.get('dedicated_profile') or not cfg.get('read_only_transport'):
            raise IpanemaError('DevTools requiere perfil dedicado y transporte de lectura declarado.')
        # A callback must check its current page, not navigate/attach to a personal browser.
        authorize_url(project, req.get('page_url', ''))
        if set(req) != {'page_url'}:
            raise IpanemaError('No se permiten scripts, navegación ni acciones desde este adaptador.')
    return req


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None  # Never forward OAuth credentials to redirected hosts.


class OfficialREST:
    """Opt-in OAuth token callback. No refresh, login, retry or background request."""
    kind = 'official_rest'

    def __init__(self, token_provider):
        self.token_provider = token_provider

    def call(self, provider, operation, req):
        body = None; method = 'GET'
        if provider == 'gsc':
            site = quote(req['siteUrl'], safe='')
            if operation == 'inspect_url':
                url = 'https://searchconsole.googleapis.com/v1/urlInspection/index:inspect'
                body = req
            else:
                url = f'https://www.googleapis.com/webmasters/v3/sites/{site}/' + ('searchAnalytics/query' if operation == 'search_analytics' else 'sitemaps')
                if operation == 'search_analytics':
                    body = {k: v for k, v in req.items() if k != 'siteUrl'}
        elif provider == 'analytics':
            url = 'https://analyticsdata.googleapis.com/v1beta/' + req['property'] + ':runReport'
            body = {'dateRanges': [{'startDate': req['startDate'], 'endDate': req['endDate']}],
                    'dimensions': [{'name': x} for x in req['dimensions']], 'metrics': [{'name': x} for x in req['metrics']],
                    'dimensionFilter': req['dimensionFilter'], 'limit': req['limit']}
        elif provider == 'merchant':
            from urllib.parse import urlencode
            url = 'https://merchantapi.googleapis.com/products/v1/' + req['account'] + '/products?' + urlencode({k: v for k, v in req.items() if k != 'account'})
        else:
            raise ProviderError(None, 'unsupported_api')
        if body is not None:
            method = 'POST'  # These documented POSTs query reports; no platform writes.
        token = self.token_provider()
        if not isinstance(token, str) or not token or '\n' in token or '\r' in token:
            raise ProviderError(401, 'credentials_unavailable')
        request = Request(url, method=method, headers={'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'},
                          data=json.dumps(body, allow_nan=False).encode() if body is not None else None)
        try:
            with build_opener(_NoRedirect()).open(request, timeout=30) as response:
                raw = response.read(4_000_001)
                if len(raw) > 4_000_000:
                    raise ProviderError(None, 'response_too_large')
                return json.loads(raw)
        except HTTPError as exc:
            raise ProviderError(exc.code) from None
        except (URLError, TimeoutError, ValueError):
            raise ProviderError(None, 'transport_or_json_error') from None

    def disconnect(self):
        self.token_provider = lambda: None


class MCPTransport:
    """Host-supplied callbacks, discovered input schemas, explicit read-only bindings.

    bindings={(provider, operation): {'tool': actual_name, 'arguments': callable}}.
    No guessed provider signatures: actual list_tools schemas are mandatory.
    """
    kind = 'mcp_callback'

    def __init__(self, list_tools, call_tool, bindings, *, active_page_url=None):
        self.tools = {t['name']: t for t in list_tools() if isinstance(t, dict) and isinstance(t.get('name'), str)}
        self.call_tool, self.bindings = call_tool, bindings
        self.active_page_url = active_page_url

    def supports(self, provider, operation):
        return ((provider, operation) in self.bindings
                and self.bindings[(provider, operation)]['tool'] in self.tools
                and self.bindings[(provider, operation)]['tool'] in MCP_READ_TOOLS.get((provider, operation), set()))

    def call(self, provider, operation, req):
        if not self.supports(provider, operation):
            raise ProviderError(None, 'unsupported_api')
        if provider=='devtools' and (not callable(self.active_page_url) or self.active_page_url()!=req['page_url']):
            raise ProviderError(403,'wrong_browser_context')
        binding = self.bindings[(provider, operation)]; tool = self.tools[binding['tool']]
        # Only positively bound tools may run; a discovered tool is not authorization.
        schema = tool.get('inputSchema')
        if not isinstance(schema, dict) or schema.get('type') != 'object':
            raise ProviderError(None, 'provider_schema_changed')
        arguments = binding['arguments'](req)
        props = schema.get('properties', {})
        if not isinstance(arguments, dict) or set(schema.get('required', [])) - set(arguments) or set(arguments) - set(props):
            raise ProviderError(None, 'provider_schema_changed')
        for key, value in arguments.items():
            expected = props[key].get('type')
            types = {'string': str, 'integer': int, 'number': (int, float), 'object': dict, 'array': list, 'boolean': bool}
            if expected in types and (not isinstance(value, types[expected]) or expected == 'integer' and type(value) is not int):
                raise ProviderError(None, 'provider_schema_changed')
            if 'enum' in props[key] and value not in props[key]['enum']:
                raise ProviderError(None, 'provider_schema_changed')
        result = self.call_tool(tool['name'], arguments)
        if not isinstance(result, dict) or result.get('isError'):
            # Do not infer HTTP status from arbitrary natural-language error bodies.
            raise ProviderError(result.get('status') if isinstance(result, dict) and type(result.get('status')) is int else None, 'mcp_error')
        if 'structuredContent' in result:
            payload=result['structuredContent']
        else:
            texts = [b.get('text', '') for b in result.get('content', []) if b.get('type') == 'text']
            if len(texts) != 1:
                raise ProviderError(None, 'provider_schema_changed')
            try:
                payload=json.loads(texts[0])
            except ValueError:
                raise ProviderError(None, 'provider_schema_changed') from None
        return binding['normalize'](payload,req) if binding.get('normalize') else payload

    def disconnect(self):
        self.call_tool = None; self.bindings = {}; self.tools = {}
        self.active_page_url = None


def gsc_mcp_bindings(version):
    """AminForou/mcp-gsc 0.4.2, fuente revisada; no tratarla como API oficial.

    El servidor redondea CTR/posición y reformatea fechas; conserva esa limitación.
    Sus errores de texto no se convierten a códigos HTTP mediante heurísticas.
    """
    if version != '0.4.2':
        raise IpanemaError('Versión MCP GSC no revisada; inspecciona contratos antes de habilitarla.')
    def inspection(payload,req):
        if not isinstance(payload,dict) or payload.get('page_url')!=req['inspectionUrl'] or payload.get('site_url')!=req['siteUrl'] or 'verdict' not in payload:
            raise ProviderError(None,'provider_schema_changed')
        mapping={'verdict':'verdict','coverage_state':'coverageState','page_fetch_state':'pageFetchState','robots_txt_state':'robotsTxtState',
                 'indexing_state':'indexingState','google_canonical':'googleCanonical','user_canonical':'userCanonical','crawled_as':'crawledAs','referring_urls':'referringUrls'}
        # last_crawled has already lost precision/timezone; do not label it API lastCrawlTime.
        return {'inspectionResult':{'indexStatusResult':{b:payload[a] for a,b in mapping.items() if payload.get(a) is not None}}}
    def search(payload,req):
        if not isinstance(payload,dict) or payload.get('site_url')!=req['siteUrl'] or payload.get('dimensions')!=req['dimensions'] or payload.get('date_range')!={'start':req['startDate'],'end':req['endDate']}:
            raise ProviderError(None,'provider_schema_changed')
        rows=[]
        for row in payload.get('rows',[]):
            if any(k not in row for k in req['dimensions']+['clicks','impressions','ctr','position']):
                raise ProviderError(None,'incomplete_data')
            rows.append({'keys':[row[d] for d in req['dimensions']],**{k:row[k] for k in ('clicks','impressions','ctr','position')}})
        return {'rows':rows,'metadata':{'provider_projection':'AminForou/mcp-gsc 0.4.2 rounds ctr/position; not raw Google API'}}
    def search_args(req):
        if req.get('dimensionFilterGroups'):
            raise ProviderError(None,'unsupported_api')  # Do not silently drop API filters.
        return {'site_url':req['siteUrl'],'start_date':req['startDate'],'end_date':req['endDate'],'dimensions':','.join(req['dimensions']),
                'row_limit':req['rowLimit'],'start_row':req['startRow'],'search_type':req.get('type','web').upper(),'data_state':req.get('dataState','final')}
    def sitemaps(payload,req):
        if not isinstance(payload,dict) or payload.get('site_url')!=req['siteUrl'] or not isinstance(payload.get('sitemaps'),list):
            raise ProviderError(None,'provider_schema_changed')
        return {'sitemap':[{k:row[k] for k in ('path','errors','warnings') if k in row} for row in payload['sitemaps']]}
    return {('gsc','inspect_url'):{'tool':'inspect_url_enhanced','arguments':lambda r:{'site_url':r['siteUrl'],'page_url':r['inspectionUrl']},'normalize':inspection},
            ('gsc','search_analytics'):{'tool':'get_advanced_search_analytics','arguments':search_args,'normalize':search},
            ('gsc','sitemaps'):{'tool':'list_sitemaps_enhanced','arguments':lambda r:{'site_url':r['siteUrl']},'normalize':sitemaps}}


def normalize(project, provider, operation, payload, request):
    """Discard unknown/instruction fields; do not interpret messages as actions."""
    if not isinstance(payload, dict):
        raise ProviderError(None, 'provider_schema_changed')
    if 'error' in payload:
        err = payload['error']
        raise ProviderError(err.get('code') if isinstance(err, dict) else None)
    if provider == 'gsc' and operation == 'inspect_url':
        result = payload.get('inspectionResult')
        if not isinstance(result, dict) or not isinstance(result.get('indexStatusResult'), dict):
            raise ProviderError(None, 'incomplete_data')
        index = result['indexStatusResult']
        keys = ('verdict', 'coverageState', 'robotsTxtState', 'indexingState', 'lastCrawlTime', 'pageFetchState', 'googleCanonical', 'userCanonical', 'referringUrls', 'sitemap', 'crawledAs')
        return {'url': request['inspectionUrl'], 'index_status': {k: index[k] for k in keys if k in index},
                'rich_results': result.get('richResultsResult'), 'live_inspection': False,
                'limitations': ['Estado conocido del índice; no es inspección en vivo ni todos los informes de la interfaz.']}
    if provider == 'gsc' and operation == 'search_analytics':
        rows = payload.get('rows', [])
        if not isinstance(rows, list):
            raise ProviderError(None, 'provider_schema_changed')
        clean = []
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get('keys'), list) or len(row['keys']) != len(request['dimensions']) or any(type(row.get(k)) not in (int, float) for k in ('clicks', 'impressions', 'ctr', 'position')):
                raise ProviderError(None, 'incomplete_data')
            dims = dict(zip(request['dimensions'], row['keys']))
            if 'page' in dims:
                authorize_url(project, dims['page'])
            clean.append({'dimensions': dims, **{k: row[k] for k in ('clicks', 'impressions', 'ctr', 'position')}})
        return {'rows': clean, 'aggregation': payload.get('responseAggregationType'), 'metadata': payload.get('metadata'),
                'period': {k: request[k] for k in ('startDate', 'endDate')}, 'timezone': 'America/Los_Angeles',
                'dimensions': request['dimensions'], 'filters': request.get('dimensionFilterGroups', []),
                'search_type': request.get('type', 'web'), 'data_state': request.get('dataState', 'final'),
                'start_row': request['startRow'], 'row_limit': request['rowLimit'],
                'limitations': ['La API devuelve filas principales, no garantiza inventario completo; consultas anonimizadas/agrupación pueden faltar.']}
    if provider == 'gsc' and operation == 'sitemaps':
        rows = payload.get('sitemap', [])
        if not isinstance(rows, list):
            raise ProviderError(None, 'provider_schema_changed')
        result = []
        for row in rows:
            if not isinstance(row, dict) or not row.get('path'):
                raise ProviderError(None, 'incomplete_data')
            authorize_url(project, row['path'])
            result.append({k: row[k] for k in ('path', 'lastSubmitted', 'lastDownloaded', 'isPending', 'isSitemapsIndex', 'type', 'warnings', 'errors', 'contents') if k in row})
        return {'sitemaps': result, 'url_inventory': None, 'limitations': ['Metadatos de sitemaps registrados; no contiene todas sus URLs ni demuestra indexación.']}
    if provider == 'analytics':
        dh, mh = payload.get('dimensionHeaders', []), payload.get('metricHeaders', [])
        if not dh or not mh or [x.get('name') for x in dh] != request['dimensions'] or [x.get('name') for x in mh] != request['metrics']:
            raise ProviderError(None, 'provider_schema_changed')
        rows = []
        for row in payload.get('rows', []):
            dims, mets = row.get('dimensionValues', []), row.get('metricValues', [])
            if len(dims) != len(dh) or len(mets) != len(mh):
                raise ProviderError(None, 'incomplete_data')
            dimensions = {h['name']: v['value'] for h, v in zip(dh, dims)}
            if 'hostName' in dimensions and dimensions['hostName'].lower() != _host(project):
                raise IpanemaError('Analytics devolvió otro dominio; se rechaza todo el lote.')
            rows.append({'dimensions': dimensions, 'metrics': {h['name']: v['value'] for h, v in zip(mh, mets)}})
        return {'rows': rows, 'row_count': payload.get('rowCount'), 'metadata': payload.get('metadata', {}),
                'period': {k: request[k] for k in ('startDate', 'endDate')}, 'dimensions': request['dimensions'],
                'metrics': request['metrics'], 'filters': request['dimensionFilter'],
                'limitations': ['Verificar umbrales, agregación, moneda y zona horaria en metadata; no demuestra causalidad.']}
    if provider == 'merchant':
        products = []
        for row in payload.get('products', []):
            if not isinstance(row, dict):
                raise ProviderError(None, 'provider_schema_changed')
            attrs = row.get('productAttributes', {})
            link = attrs.get('link')
            if not link:
                raise ProviderError(None, 'incomplete_data')
            authorize_url(project, link)
            products.append({k: row[k] for k in ('name', 'offerId', 'contentLanguage', 'feedLabel', 'productStatus', 'productAttributes') if k in row})
        return {'products': products, 'next_page_token': payload.get('nextPageToken'),
                'limitations': ['Diagnóstico de Merchant observado, no de la totalidad de resultados de Google Search.']}
    return {'observation': payload, 'limitations': ['Snapshot DevTools no demuestra indexación ni datos de campo.']}


class ReadOnlyAdapter:
    def __init__(self, project, provider, transport=None, *, authorized=False, max_calls=5):
        if provider not in OPERATIONS or not 1 <= max_calls <= 50:
            raise IpanemaError('Proveedor/límite de llamadas inválido.')
        self.project, self.provider, self.transport = project, provider, transport
        self.authorized, self.max_calls, self.calls, self.stopped = authorized, max_calls, 0, False

    def capabilities(self):
        return {'provider': self.provider, 'connected': self.transport is not None, 'authorized': self.authorized,
                'operations': list(OPERATIONS[self.provider]), 'scope': SCOPES.get(self.provider),
                'transport': getattr(self.transport, 'kind', None), 'stopped': self.stopped,
                'account_access_tested': False, 'production_writes_supported': False}

    def read(self, operation, request):
        envelope = {'provider': self.provider, 'operation': operation, 'project': self.project.id, 'domain': _host(self.project),
                    'at': now(), 'untrusted_external_data': True, 'transport': getattr(self.transport, 'kind', None)}
        if not self.transport:
            return {**envelope, 'status': 'not_connected', 'data': None}
        if not self.authorized:
            return {**envelope, 'status': 'authorization_required', 'data': None}
        if self.stopped or self.calls >= self.max_calls:
            return {**envelope, 'status': 'stopped', 'data': None}
        req = prepare(self.project, self.provider, operation, request)
        self.calls += 1
        try:
            raw = self.transport.call(self.provider, operation, req)
            if len(json.dumps(raw, allow_nan=False).encode()) > 4_000_000:
                raise ProviderError(None, 'response_too_large')
            data = normalize(self.project, self.provider, operation, raw, req)
            return {**envelope, 'status': 'observed', 'request': req, 'data': data}
        except ProviderError as exc:
            if exc.status in (403, 429) or getattr(self.transport,'kind',None)=='mcp_callback' and exc.category in ('mcp_error','provider_schema_changed'):
                self.stopped = True
            state = {401: 'token_expired_or_unauthorized', 403: 'forbidden_stop', 404: 'not_found', 429: 'quota_stop', 501: 'unsupported_api'}.get(exc.status, exc.category)
            return {**envelope, 'status': state, 'http_status': exc.status, 'data': None}

    def disconnect(self):
        if self.transport and hasattr(self.transport, 'disconnect'):
            self.transport.disconnect()
        self.transport = None; self.authorized = False; self.stopped = True


def import_observation(project, document):
    """Offline exports are dated evidence, never a successful live connection."""
    if document.get('project') != project.id or not document.get('observed_at'):
        raise IpanemaError('Exportación sin proyecto/fecha de observación.')
    try:
        dt.datetime.fromisoformat(document['observed_at'].replace('Z', '+00:00'))
    except (ValueError, TypeError):
        raise IpanemaError('Fecha de evidencia inválida.') from None
    provider, operation = document.get('provider'), document.get('operation')
    req = prepare(project, provider, operation, document.get('request'))
    return {'provider': provider, 'operation': operation, 'project': project.id, 'domain': _host(project), 'at': now(),
            'observed_at': document['observed_at'], 'status': 'imported_observation', 'live_connection_tested': False,
            'request': req, 'data': normalize(project, provider, operation, document.get('payload'), req),
            'untrusted_external_data': True}
