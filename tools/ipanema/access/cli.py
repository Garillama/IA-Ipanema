"""Interfaz del controlador; OAuth solo mediante consentimiento explícito por proyecto."""
from __future__ import annotations

import os
from pathlib import Path
import re
import shutil
import sys

from ..core import IpanemaError, read_json
from ..seo.adapters import OPERATIONS
from .devtools import DevTools, VERSION, installation
from .gateway import Gateway
from .policy import AGENTS, CAPABILITIES, Policy


def add_parser(sub):
    parser = sub.add_parser('access', help='Acceso compartido MCP/REST con permisos por tarea')
    commands = parser.add_subparsers(dest='access_command', required=True)
    doctor = commands.add_parser('doctor')
    doctor.add_argument('--probe-devtools', action='store_true', help='Iniciar MCP y consultar herramientas reales, sin abrir Chrome')
    agents = commands.add_parser('probe-agents', help='Invocación real aislada de los clientes; consume inferencia')
    agents.add_argument('--url', required=True)
    agents.add_argument('--browser-profile', choices=['security','audit'], default='security')
    agents.add_argument('--execute', action='store_true')
    agents.add_argument('--agent', dest='agents', choices=AGENTS, action='append')
    oauth = commands.add_parser('oauth', help='Consentimiento Google PKCE; token solo en memoria')
    oauth.add_argument('--client', type=Path, required=True)
    oauth.add_argument('--url', required=True)
    oauth.add_argument('--probe-agents', action='store_true')
    oauth.add_argument('--execute', action='store_true')
    grant = commands.add_parser('grant', help='Operador: emitir permiso explícito, local y temporal')
    grant.add_argument('--agent', choices=AGENTS, required=True)
    grant.add_argument('--task', required=True, help='Identificador de tarea, sin texto privado')
    grant.add_argument('--capability', choices=list(CAPABILITIES), action='append', required=True)
    grant.add_argument('--minutes', type=int, default=60)
    grant.add_argument('--max-calls', type=int, default=30)
    grant.add_argument('--browser-profile', choices=['security', 'audit'], default='security')
    grant.add_argument('--allow-network', action='store_true')
    grant.add_argument('--allow-account-read', action='store_true')
    for command in ('revoke', 'config', 'call'):
        p = commands.add_parser(command)
        p.add_argument('--grant', required=True)
        if command == 'call':
            p.add_argument('--tool', required=True)
            p.add_argument('--arguments', type=Path, required=True)


def doctor(project, *, probe=False):
    from ..orchestration.adapters import agent_policy
    result = {'project': project.id, 'execution_policy':agent_policy(),'runtimes_installed': {a: bool(shutil.which(a)) for a in AGENTS},
              'repeatable_qa': 'Puppeteer/Lighthouse existentes; no se reemplazan',
              'credentials_written_by_doctor': False, 'providers': {}}
    try:
        installation(project.root)
        devtools = {'installed': True, 'pinned_version': VERSION, 'server_available': None,
                    'tools_verified': [], 'account_access_tested': False}
        if probe:
            browser = DevTools(project)
            try:
                devtools.update(browser.discovery())
            finally:
                browser.close()
    except (IpanemaError, OSError, ValueError) as exc:
        devtools = {'installed': False, 'server_available': False, 'tools_verified': [],
                    'status': str(exc) if isinstance(exc, IpanemaError) else 'runtime_unavailable'}
    result['providers']['devtools'] = devtools
    for provider in ('gsc', 'analytics', 'merchant'):
        cfg = project.data.get('google', {}).get(provider, {})
        env_name = cfg.get('oauth_token_env', '')
        token_present = bool(re.fullmatch(r'IPANEMA_[A-Z0-9_]+_TOKEN', env_name) and os.getenv(env_name))
        credential_source = 'environment' if token_present else None
        if provider == 'gsc' and not token_present:
            from .credentials import load_token
            token_present = bool(load_token(project))
            credential_source = 'private_project_store' if token_present else None
        resource = cfg.get({'gsc': 'site_url', 'analytics': 'property', 'merchant': 'account'}[provider])
        result['providers'][provider] = {'transport': 'existing_official_rest', 'mcp_required': False,
            'configured': bool(resource), 'credential_available': token_present,
            'credential_source': credential_source,
            'account_access_tested': False, 'api_available': None,
            'default_enabled': False, 'operations': list(OPERATIONS[provider]),
            'status': 'not_tested' if resource and token_present else 'configuration_or_credentials_required'}
    result['limitations'] = ['CLI instalada no acredita autenticación ni uso del MCP por el modelo.',
        'Los permisos gobiernan esta puerta, no procesos que el mismo usuario ejecute fuera de ella.',
        'Workers aislados existentes no reciben credenciales ni nuevos montajes automáticamente.']
    return result


def execute(project, args):
    if args.access_command == 'oauth':
        if not args.execute:
            raise IpanemaError('OAuth y consultas reales requieren --execute.')
        from .oauth import authorize, verify_live
        from ..core import beneath, write_json, now
        from ..seo.adapters import authorize_url
        authorize_url(project, args.url)
        path = args.client.resolve()
        if beneath(path, project.root) and not beneath(path, project.root / '.local'):
            raise IpanemaError('Guarda el cliente OAuth fuera de Git, en .local o fuera del repositorio.')
        from .credentials import store_token
        authorization = authorize(path)
        token = authorization.pop('access_token')
        result = verify_live(project, token, args.url)
        if result['all_reads_observed']:
            store_token(project, token, authorization['expires_in'])
        if args.probe_agents and result['all_reads_observed']:
            from .agents import probe_agents
            env_name = project.data.get('google', {}).get('gsc', {}).get('oauth_token_env', '')
            if not re.fullmatch(r'IPANEMA_[A-Z0-9_]+_TOKEN', env_name):
                raise IpanemaError('Variable de token no configurada.')
            previous = os.environ.get(env_name)
            os.environ[env_name] = token
            try:
                result['agents'] = probe_agents(project, args.url, profile='audit', include_gsc=True)
            finally:
                if previous is None:
                    os.environ.pop(env_name, None)
                else:
                    os.environ[env_name] = previous
        token = None
        destination = project.new_run('access-google-live') / 'verification.json'
        write_json(destination, {'at': now(), 'project': project.id, **result, 'tokens_in_evidence': False,
                                'credential_storage': 'private_project_store' if result['all_reads_observed'] else 'not_saved'})
        return {'report': str(destination), **result}, 0 if result['all_reads_observed'] else 2
    if args.access_command == 'probe-agents':
        if not args.execute:
            raise IpanemaError('Las invocaciones reales requieren --execute.')
        from .agents import probe_agents
        from .devtools import page_origin
        from urllib.parse import urlsplit
        url = urlsplit(args.url)
        if f'{url.scheme}://{url.netloc}' != page_origin(project):
            raise IpanemaError('URL fuera del proyecto.')
        from ..orchestration.adapters import enabled_agents
        selected = args.agents or list(enabled_agents())
        result = probe_agents(project, args.url, profile=args.browser_profile, agents=selected)
        return result, 0 if set(selected) <= {r.get('agent') for r in result['results'] if r['status']=='verified'} else 2
    if args.access_command == 'doctor':
        result = doctor(project, probe=args.probe_devtools)
        return result, 2 if args.probe_devtools and not result['providers']['devtools'].get('server_available') else 0
    policy = Policy(project)
    if args.access_command == 'grant':
        result = policy.issue(args.agent, args.task, args.capability, minutes=args.minutes,
                              max_calls=args.max_calls, allow_network=args.allow_network,
                              allow_account_read=args.allow_account_read, browser_profile=args.browser_profile)
        return result, 0
    if args.access_command == 'revoke':
        policy.revoke(args.grant)
        return {'revoked': args.grant}, 0
    if args.access_command == 'config':
        grant = policy.load(args.grant)
        argv = [str(project.root / 'tools/access_mcp.py'), '--project', project.id, '--grant', args.grant]
        name = 'ipanema-' + grant['task']
        server = {'command': sys.executable, 'args': argv}
        return {'agent': grant['agent'], 'project': project.id, 'task': grant['task'],
                'expires_at': grant['expires_at'], 'mcpServers': {name: server},
                'register_command': ([grant['agent'], 'mcp', 'add', name, '--', sys.executable, *argv]
                    if grant['agent'] != 'commandcode' else
                    ['commandcode', 'mcp', 'add-json', name, __import__('json').dumps(server)]),
                'registered': False, 'note': 'Configuración revisable; no modifica la configuración del cliente. No pasar tokens en env de MCP.'}, 0
    gateway = Gateway(project, args.grant)
    try:
        result = gateway.call(args.tool, read_json(args.arguments))
        return result, 0 if result.get('status') == 'observed' else 2
    finally:
        gateway.close()
