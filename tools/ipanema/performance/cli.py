"""CLI del servicio compartido; sin consultas implícitas ni credenciales en argumentos."""
import json
import os
from pathlib import Path
from ..core import IpanemaError, read_json
from . import model
from .service import Service, local, persist


def add_parser(sub):
    parser = sub.add_parser('performance', help='PageSpeed, CrUX y Lighthouse separados por procedencia.')
    commands = parser.add_subparsers(dest='performance_operation', required=True)
    commands.add_parser('doctor')
    for name in ('pagespeed','crux','history','local','audit'):
        command = commands.add_parser(name)
        command.add_argument('--url')
        command.add_argument('--device', choices=('mobile','desktop'), default='mobile')
        command.add_argument('--allow-network', action='store_true')
        command.add_argument('--refresh', action='store_true', help='Nueva consulta dentro de permisos/cuotas; no reutilizar caché.')
        command.add_argument('--category', action='append', choices=model.CATEGORIES)
        command.add_argument('--locale', default='es')
        command.add_argument('--scope', choices=('url','origin'), default='url')
        command.add_argument('--period-count', type=int, default=25)
        command.add_argument('--runs', type=int, default=3)
        command.add_argument('--max-calls', type=int, default=4)
        if name == 'audit':
            command.add_argument('--all-sources', action='store_true', required=True)
            command.add_argument('--include-history', action='store_true')
    compare = commands.add_parser('compare')
    compare.add_argument('before', type=Path)
    compare.add_argument('after', type=Path)
    compare.add_argument('--source', choices=('pagespeed','lighthouse_local'), default='pagespeed')


def execute(project, args):
    op = args.performance_operation
    if op == 'doctor':
        cfg = project.data.get('google', {}).get('performance', {})
        credentials = {provider: {'configured':bool(cfg.get(field)), 'environment_present':bool(os.getenv(cfg.get(field,'')))}
                       for provider,field in (('pagespeed','pagespeed_key_env'),('crux','crux_key_env'))}
        return {'project':project.id, 'credentials':credentials, 'network_tested':False,
                'local_lighthouse':'Usa doctor general para versiones instaladas.',
                'production_operations':False}, 0
    if op == 'compare':
        before, after = read_json(args.before), read_json(args.after)
        result = model.compare(before.get('sources',{}).get(args.source,before), after.get('sources',{}).get(args.source,after))
        return result, 0 if result['status'] == 'compared' else 2
    if not args.allow_network:
        raise IpanemaError('Lectura externa desactivada; añade --allow-network con origen registrado y credenciales privadas.')
    service = Service(project, max_calls=args.max_calls)
    kwargs = dict(url=args.url, device=args.device, categories=args.category, locale=args.locale,
                  scope=args.scope, period_count=args.period_count, refresh=args.refresh)
    sources = {}
    requested = ['pagespeed','crux'] if op == 'audit' else [{'history':'crux_history'}.get(op,op)]
    if op == 'audit' and args.include_history:
        requested.append('crux_history')
    stopped = False
    for source in requested:
        if source == 'local':
            continue
        result = service.read(source, authorized=True, **kwargs)
        sources[source] = result
        if result['status'] in ('forbidden_stop','quota_stop','provider_stopped'):
            stopped = True
            break
    if op in ('audit','local') and not stopped:
        sources['lighthouse_local'] = local(project, url=args.url, device=args.device, runs=args.runs, authorized=True)
    result = persist(project, sources)
    result['status'] = 'observed' if all(v.get('status') == 'observed' for v in sources.values()) else 'partial_or_blocked'
    return result, 0 if result['status'] == 'observed' else 2
