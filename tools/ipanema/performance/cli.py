"""CLI del servicio compartido; sin consultas implícitas ni credenciales en argumentos."""
import json
import os
from pathlib import Path
from ..core import IpanemaError, beneath, read_json
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
    diagnose = commands.add_parser('diagnose', help='Diagnóstico offline Cloudflare Web Performance sobre evidencia capturada.')
    diagnose.add_argument('report', type=Path)
    diagnose.add_argument('--rendered', type=Path)
    diagnose.add_argument('--preconnect', action='append', default=[])
    qaudit = commands.add_parser('quality-audit', help='Auditoría integral offline Web Quality Audit reutilizando Cloudflare Web Performance.')
    qaudit.add_argument('report', type=Path)
    qaudit.add_argument('--rendered', type=Path)
    qaudit.add_argument('--source-file', type=Path, action='append', default=[])
    qaudit.add_argument('--framework', choices=('shopify-liquid', 'shopify-hydrogen', 'remix', 'nextjs', 'react-web', 'tiendanube-ipanema'))
    qaudit.add_argument('--preconnect', action='append', default=[])
    raudit = commands.add_parser('react-audit', help='Auditoría offline Vercel React Best Practices (React, Hydrogen, Remix, Next.js).')
    raudit.add_argument('--source-file', type=Path, action='append', required=True)
    raudit.add_argument('--framework', choices=('shopify-liquid', 'shopify-hydrogen', 'remix', 'nextjs', 'react-web', 'tiendanube-ipanema'))
    raudit.add_argument('--perf-report', type=Path)
    daudit = commands.add_parser('design-audit', help='Auditoría offline Vercel Web Design Guidelines (UI/UX, jerarquía, estados, responsive y consistencia).')
    daudit.add_argument('--source-file', type=Path, action='append', default=[])
    daudit.add_argument('--rendered', type=Path)
    daudit.add_argument('--framework', choices=('shopify-liquid', 'shopify-hydrogen', 'remix', 'nextjs', 'react-web', 'tiendanube-ipanema'))
    daudit.add_argument('--quality-report', type=Path)
    daudit.add_argument('--accessibility-report', type=Path)
    aaudit = commands.add_parser('accessibility-audit', help='Auditoría offline Better Accessibility (WCAG 2.2 Nivel A/AA, teclado, foco, ARIA, formularios, reflow y lectores de pantalla).')
    aaudit.add_argument('--source-file', type=Path, action='append', default=[])
    aaudit.add_argument('--rendered', type=Path)
    aaudit.add_argument('--framework', choices=('shopify-liquid', 'shopify-hydrogen', 'remix', 'nextjs', 'react-web', 'tiendanube-ipanema'))
    aaudit.add_argument('--quality-report', type=Path)
    aaudit.add_argument('--design-report', type=Path)
    aaudit.add_argument('--propose-fixes', action='store_true', help='Genera propuestas mínimas seguras sin modificar archivos en disco.')


def _read_authorized_sources(project, source_paths):
    allowed_roots = [project.root] + ([project.theme_root] if project.theme_root else [])
    source_files = {}
    for sf in source_paths or ():
        resolved = sf.resolve()
        if not any(beneath(resolved, r) for r in allowed_roots) or not resolved.is_file():
            raise IpanemaError('Archivo fuente fuera del alcance autorizado o inexistente.')
        source_files[sf.name] = resolved.read_text(encoding='utf-8')
    return source_files


def execute(project, args):
    op = args.performance_operation
    if op == 'doctor':
        cfg = project.data.get('google', {}).get('performance', {})
        credentials = {provider: {'configured':bool(cfg.get(field)), 'environment_present':bool(os.getenv(cfg.get(field,'')))}
                       for provider,field in (('pagespeed','pagespeed_key_env'),('crux','crux_key_env'))}
        return {'project':project.id, 'credentials':credentials, 'network_tested':False,
                'local_lighthouse':'Usa doctor general para versiones instaladas.',
                'production_operations':False}, 0
    if op == 'diagnose':
        payload = read_json(args.report)
        rendered = read_json(args.rendered) if args.rendered else payload.get('rendered')
        network = payload.get('navigation_network') or (rendered.get('navigation_network') if isinstance(rendered, dict) else None)
        return model.diagnose_web_perf(payload, network_records=network, rendered=rendered, preconnect_origins=args.preconnect), 0
    if op == 'quality-audit':
        payload = read_json(args.report)
        rendered = read_json(args.rendered) if args.rendered else payload.get('rendered')
        network = payload.get('navigation_network') or (rendered.get('navigation_network') if isinstance(rendered, dict) else None)
        console_msgs = payload.get('console_messages') or (rendered.get('console_messages') if isinstance(rendered, dict) else None)
        source_files = _read_authorized_sources(project, args.source_file)
        return model.audit_web_quality(
            payload,
            network_records=network,
            rendered=rendered,
            console_messages=console_msgs,
            source_files=source_files,
            preconnect_origins=args.preconnect,
            framework=args.framework,
        ), 0
    if op == 'react-audit':
        source_files = _read_authorized_sources(project, args.source_file)
        perf_rep = read_json(args.perf_report) if args.perf_report else None
        return model.audit_react_best_practices(
            source_files,
            framework=args.framework,
            perf_report=perf_rep,
        ), 0
    if op == 'design-audit':
        source_files = _read_authorized_sources(project, args.source_file)
        rendered = read_json(args.rendered) if args.rendered else None
        q_rep = read_json(args.quality_report) if args.quality_report else None
        a_rep = read_json(args.accessibility_report) if args.accessibility_report else None
        return model.audit_web_design_guidelines(
            source_files,
            rendered=rendered,
            framework=args.framework,
            quality_audit_report=q_rep,
            accessibility_report=a_rep,
        ), 0
    if op == 'accessibility-audit':
        source_files = _read_authorized_sources(project, args.source_file)
        rendered = read_json(args.rendered) if args.rendered else None
        q_rep = read_json(args.quality_report) if args.quality_report else None
        d_rep = read_json(args.design_report) if args.design_report else None
        result = model.audit_better_accessibility(
            source_files,
            rendered=rendered,
            framework=args.framework,
            quality_audit_report=q_rep,
            design_report=d_rep,
        )
        if args.propose_fixes and source_files:
            result['proposed_fixes'] = model.propose_safe_accessibility_fixes(source_files)
        return result, 0
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
