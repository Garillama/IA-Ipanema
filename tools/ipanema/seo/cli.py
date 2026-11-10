"""Subcomandos SEO; no instaladores, OAuth, publicación ni escritura de temas."""
from __future__ import annotations

import os
from pathlib import Path

from ..core import IpanemaError, read_json, write_json
from . import reports
from .adapters import OPERATIONS, OfficialREST, ReadOnlyAdapter, import_observation
from .extractor import extract
from .generator import generate, repair_trailing_json
from .intelligence import compare_periods, correlate
from .page_audit import PAGE_SCHEMAS


def add_parser(sub):
    seo = sub.add_parser('seo', help='SEO offline, schemas y adaptadores opcionales de lectura')
    commands = seo.add_subparsers(dest='seo_command', required=True)
    commands.add_parser('source', help='Auditar snippets actuales y producir diff propuesto sin aplicarlo')
    audit = commands.add_parser('audit')
    entry = audit.add_mutually_exclusive_group(required=True)
    entry.add_argument('--html', type=Path); entry.add_argument('--capture', type=Path)
    audit.add_argument('--url'); audit.add_argument('--type', choices=list(PAGE_SCHEMAS), default='page')
    audit.add_argument('--rendered', type=Path); audit.add_argument('--no-js', type=Path)
    audit.add_argument('--facts', type=Path); audit.add_argument('--status', type=int)
    audit.add_argument('--robots', type=Path)
    gen = commands.add_parser('generate', help='Propuesta desde exportación comercial/CMS referenciada con hash')
    gen.add_argument('--facts', type=Path, required=True); gen.add_argument('--target', required=True)
    gen.add_argument('--html', type=Path); gen.add_argument('--mode', choices=['missing', 'update'], default='missing')
    gen.add_argument('--entity-id')
    repair = commands.add_parser('repair-artifact')
    repair.add_argument('path', type=Path)
    corp = commands.add_parser('corpus')
    corp.add_argument('--audit', type=Path, action='append', required=True); corp.add_argument('--sitemap-urls', type=Path)
    commands.add_parser('connections')
    imp = commands.add_parser('google-import', help='Normalizar exportación fechada, sin conexión real')
    imp.add_argument('path', type=Path)
    read = commands.add_parser('google-read', help='Consulta oficial opcional; exige autorización de cuenta explícita')
    read.add_argument('--provider', choices=['gsc', 'analytics', 'merchant'], required=True)
    read.add_argument('--operation', required=True); read.add_argument('--request', type=Path, required=True)
    read.add_argument('--allow-account-read', action='store_true')
    corr = commands.add_parser('correlate')
    corr.add_argument('--audit', type=Path, action='append', required=True)
    corr.add_argument('--observation', type=Path, action='append', default=[])
    corr.add_argument('--corrections', type=Path)
    comp = commands.add_parser('compare-periods')
    comp.add_argument('before', type=Path); comp.add_argument('after', type=Path)
    commands.add_parser('evals')


def execute(project, args):
    command = args.seo_command
    inputs = []
    if command == 'source':
        result = reports.source_report(project)
    elif command == 'audit':
        if args.capture:
            result = reports.from_projection(project, args.capture, no_js=args.no_js, facts=args.facts)
            inputs = [args.capture] + ([args.no_js] if args.no_js else [])
        else:
            if not args.url:
                raise IpanemaError('--html requiere --url del proyecto para resolver enlaces/identidades.')
            result = reports.from_html(project, args.html, args.url, args.type, rendered=args.rendered,
                                       no_js=args.no_js, facts=args.facts, status=args.status, robots=args.robots)
            inputs = [p for p in (args.html, args.rendered, args.no_js, args.facts, args.robots) if p]
    elif command == 'generate':
        doc = read_json(args.facts)
        snapshot = extract(reports.read_text(args.html), doc['url']) if args.html else None
        if snapshot is None:
            raise IpanemaError('Generar requiere --html actual para comprobar entidades nativas; no asumir que faltan.')
        result = generate(project, doc, args.target, snapshot=snapshot, mode=args.mode, entity_id=args.entity_id)
        inputs = [args.facts, args.html]
    elif command == 'repair-artifact':
        result = {'kind': 'schema-artifact-repair', 'project': project.id, **repair_trailing_json(reports.read_text(args.path))}
        inputs = [args.path]
    elif command == 'corpus':
        result = reports.corpus(project, args.audit, args.sitemap_urls)
        inputs = args.audit + ([args.sitemap_urls] if args.sitemap_urls else [])
    elif command == 'connections':
        return {'project': project.id, 'providers': [ReadOnlyAdapter(project, p).capabilities() for p in OPERATIONS],
                'runtime_discovery': 'Estos adaptadores no inician MCP. access doctor --probe-devtools comprueba el servidor compartido; un host también puede inyectar list_tools/call_tool. Configuración no equivale a conexión.',
                'shared_access': 'access grant/config: permisos por agente, proyecto y tarea; GSC reutiliza REST sin otro MCP.',
                'fallback': 'seo source/audit/corpus/evals continúan offline.'}, 0
    elif command == 'google-import':
        result = {'kind': 'google-observation', **import_observation(project, read_json(args.path))}
        inputs = [args.path]
    elif command == 'google-read':
        if not args.allow_account_read:
            raise IpanemaError('Sin autorización explícita de lectura de la cuenta; no se inicia OAuth ni se consulta la API.')
        cfg = project.data.get('google', {}).get(args.provider, {})
        env_name = cfg.get('oauth_token_env')
        if not isinstance(env_name, str) or not env_name.startswith('IPANEMA_') or not env_name.endswith('_TOKEN') or not os.getenv(env_name):
            raise IpanemaError('Configura un nombre IPANEMA_*_TOKEN y proporciona el token fuera del repositorio; no se inicia login.')
        # This option only supplies an access token, never obtains/refreshes one.
        adapter = ReadOnlyAdapter(project, args.provider, OfficialREST(lambda: os.getenv(env_name)), authorized=True, max_calls=1)
        try:
            result = {'kind': 'google-observation', **adapter.read(args.operation, read_json(args.request))}
        finally:
            adapter.disconnect()
        inputs = [args.request]
    elif command == 'correlate':
        result = correlate(project, [read_json(p) for p in args.audit], [read_json(p) for p in args.observation],
                           corrections=read_json(args.corrections) if args.corrections else None)
        inputs = args.audit + args.observation + ([args.corrections] if args.corrections else [])
    elif command == 'compare-periods':
        before,after=read_json(args.before),read_json(args.after)
        if before.get('project')!=project.id or after.get('project')!=project.id:
            raise IpanemaError('Las dos observaciones deben pertenecer al proyecto activo.')
        result = {'project': project.id, **compare_periods(before, after)}
        inputs = [args.before, args.after]
    elif command == 'evals':
        from .evals import evaluate
        result = evaluate()
    else:
        raise IpanemaError('Comando SEO desconocido.')
    saved = reports.save_report(project, result, 'seo-' + command, inputs)
    if result.get('kind') == 'seo-agent-evals':
        saved.update({'outcome': result['outcome'], 'cases': len(result['cases'])})
        return saved, 0 if result['outcome'] == 'passed' else 1
    if result.get('status') and result['status'] not in ('observed', 'imported_observation', 'already_parseable', 'repaired_artifact_only'):
        return {**saved, 'status': result['status']}, 2
    # Findings are reported, not swallowed by a successful process exit.
    errors = sum(f['severity'] == 'error' for f in result.get('findings', []))
    return {**saved, 'error_findings': errors}, 1 if errors else 0
