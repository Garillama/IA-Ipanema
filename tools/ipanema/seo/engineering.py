"""CLI incremental V4: parsers, crawler explícito, capas y gates sobre motor existente."""
from __future__ import annotations

from dataclasses import fields
import json
from pathlib import Path
import re

from ..core import IpanemaError, digest, now, read_json, redact, write_json
from . import reports
from .adapters import authorize_url, import_observation
from .crawl_policy import Limits, Policy, normalize
from .crawler import crawl, export, save_csv, pilot_limits
from .extractor import extract
from .indexability import Content, classify, layers, page_type, pagination, readiness, template_checks
from .regression import compare
from .robots import Robots
from .sitemaps import parse_sitemap

COMMANDS = {'sitemap', 'crawl', 'readiness', 'enrich', 'gate', 'coverage-import'}


def add_parser(commands):
    sitemap = commands.add_parser('sitemap', help='Parsear sitemap nativo offline, sin reemplazarlo')
    sitemap.add_argument('--xml', type=Path, required=True)
    sitemap.add_argument('--source-url', required=True)
    crawler = commands.add_parser('crawl', help='BFS solo lectura; red requiere permiso y límites')
    mode = crawler.add_mutually_exclusive_group(required=True)
    mode.add_argument('--allow-network', action='store_true')
    mode.add_argument('--responses', type=Path, help='Fixture/export local explícito; no hace red')
    crawler.add_argument('--targets-manifest', type=Path, help='Piloto cerrado de cinco URLs, supervisado y con checkpoint')
    crawler.add_argument('--targets-sha256', help='SHA256 exacto del manifiesto autorizado')
    for field in fields(Limits):
        option = '--' + field.name.replace('_', '-')
        crawler.add_argument(option, type=float if field.name in ('requests_per_second', 'max_seconds', 'timeout') else int,
                             default=field.default)
    ready = commands.add_parser('readiness', help='Evaluación observable de captura existente, sin red')
    ready.add_argument('--capture', type=Path, required=True)
    ready.add_argument('--no-js', type=Path)
    ready.add_argument('--robots', type=Path)
    ready.add_argument('--facts', type=Path)
    enrich = commands.add_parser('enrich', help='Enriquecer crawl con capturas QA y exportaciones Google del mismo proyecto')
    enrich.add_argument('--crawl', type=Path, required=True)
    enrich.add_argument('--capture', type=Path, action='append', default=[])
    enrich.add_argument('--no-js', type=Path, action='append', default=[])
    enrich.add_argument('--google-observation', type=Path, action='append', default=[])
    enrich.add_argument('--coverage-export', type=Path, action='append', default=[])
    coverage = commands.add_parser('coverage-import', help='CSV exportado con mapping, propiedad y fecha explícitos; no conecta Google')
    coverage.add_argument('--csv', type=Path, required=True)
    coverage.add_argument('--mapping', type=Path, required=True)
    coverage.add_argument('--site-url', required=True)
    coverage.add_argument('--observed-at', required=True)
    coverage.add_argument('--max-rows', type=int, default=10000)
    gate = commands.add_parser('gate', help='SEO regression gate offline; no inicia crawls en CI')
    gate.add_argument('--before', type=Path, required=True)
    gate.add_argument('--after', type=Path, required=True)
    gate.add_argument('--important-url', action='append')
    gate.add_argument('--allow-removed-url', action='append', default=[])


class OfflineResponses:
    def __init__(self, project, path):
        document = json.loads(reports.read_text(path))
        if document.get('project') != project.id or normalize(document.get('home')) != normalize(project.data['public_url']):
            raise IpanemaError('Respuestas offline de otro proyecto/origen.')
        self.responses = document.get('responses')
        if not isinstance(self.responses, dict) or len(self.responses) > 2000:
            raise IpanemaError('Manifest de respuestas inválido o excedido.')
        self.time = 0

    def clock(self):
        return self.time

    def sleep(self, seconds):
        self.time += seconds

    def __call__(self, url, **kwargs):
        row = self.responses.get(url, {'status': 404, 'body': '', 'headers': {}})
        if not isinstance(row, dict) or type(row.get('status')) is not int or not 100 <= row['status'] <= 599 or not isinstance(row.get('body', ''), str):
            raise IpanemaError('Respuesta offline inválida.')
        return {'headers': {'content-type': 'text/html'}, **row}


def clean(value):
    if isinstance(value, dict):
        return {k: '[redacted]' if re.search(r'(?:^|_)(?:token|password|cookie|secret|authorization)(?:$|_)', k, re.I)
                else clean(v) for k, v in value.items() if k not in ('raw', 'raw_html')}
    if isinstance(value, list):
        return [clean(v) for v in value]
    if isinstance(value, str):
        return re.sub(r'ndp_pub_[A-Za-z0-9_-]+', '[public-content-token]', redact(value, mask_env=False))
    return value


def _capture(project, path, *, no_js=False):
    data = read_json(path)
    if data.get('kind') != 'seo-browser-projection' or data.get('project') != project.id:
        raise IpanemaError('Captura de otro proyecto o formato.')
    authorize_url(project, data.get('url', ''))
    if no_js and data.get('mode') != 'no-js':
        raise IpanemaError('Se requiere captura con mode=no-js, no simulación de HTML inicial.')
    return data


def captured_readiness(project, capture_path, no_js_path=None, robots_path=None, facts_path=None):
    captured = _capture(project, capture_path)
    without = _capture(project, no_js_path, no_js=True) if no_js_path else None
    if without and without['url'] != captured['url']:
        raise IpanemaError('Capturas no corresponden a la misma URL.')
    if without and without.get('width') != captured.get('width'):
        raise IpanemaError('Capturas de anchos diferentes; perfiles no comparables.')
    url = captured['url']
    initial_html, rendered_html = captured['initial']['html'], captured['rendered']['html']
    snap = extract(initial_html, url, status=captured.get('status'), headers=captured.get('headers'))
    content = Content(initial_html).evidence()
    kind, basis = page_type(url, content)
    robot = Robots()
    if robots_path:
        robot.parse(reports.read_text(robots_path).splitlines())
    google_allowed = robot.can_fetch('Googlebot', url) if robots_path and not robot.errors else None
    audit = reports.from_projection(project, capture_path, no_js=no_js_path, facts=facts_path)
    node = {'url': url, 'status': captured.get('status'), 'page_type': kind, 'type_basis': basis,
            'canonical': snap['canonical'], 'content': content, 'outgoing_links': [l['absolute'] for l in audit['crawl']['links']],
            'pagination': pagination(snap), 'indexability': classify(snap, googlebot_allowed=google_allowed,
                robots_known=bool(robots_path and not robot.errors), content=content), 'template_audit': audit}
    node['navigation_without_href'] = sum(not l.get('href') and not l.get('action_hint') and not l.get('disabled') for l in snap['links'])
    rendered, no_js_snap = extract(rendered_html, url), extract(without['rendered']['html'], url) if without else None
    node['layers'] = layers(snap, rendered, no_js_snap)
    node['layers']['main_content'] = {'initial': content, 'rendered': Content(rendered_html).evidence(),
                                     'no_js': Content(without['rendered']['html']).evidence() if without else None}
    node['readiness'] = readiness(node, audit, rendered=rendered,
        no_js={'links_removed': node['layers']['initial_to_no_js']['links_removed_after_js']} if without else None)
    node['template_checks'] = template_checks(snap, kind, content, audit)
    return {'kind': 'seo-readiness-v4', 'project': project.id, 'at': now(), 'observation_at': captured.get('at'),
            'outcome': node['readiness']['approval'],
            'capture_provenance': {'capture': digest(capture_path), 'no_js': digest(no_js_path) if no_js_path else None},
            'node': node, 'remote_mutations': False,
            'limitations': audit['limitations'] + ['Esta comparación no es una ejecución de Googlebot.']}


def enrich_report(project, report, capture_paths, no_js_paths, observations, coverage_exports=()):
    if report.get('kind') != 'seo-crawl-v4' or report.get('project') != project.id:
        raise IpanemaError('Crawl de otro proyecto o formato.')
    captures = {_capture(project, p)['url']: p for p in capture_paths}
    no_js = {_capture(project, p, no_js=True)['url']: p for p in no_js_paths}
    for node in report['urls']:
        if node['url'] not in captures:
            continue
        data = captured_readiness(project, captures[node['url']], no_js.get(node['url']))
        # Capas separadas: no reemplaza las observaciones HTTP/robots de otro momento.
        node['capture_analysis'] = data
        node['layers'] = data['node']['layers']
        node['capture_provenance'] = data['capture_provenance']
        node['capture_observed_at'] = data.get('observation_at')
        node['readiness'] = readiness(node, node.get('template_audit'), rendered=data['node']['layers'],
            no_js={'links_removed': node['layers']['initial_to_no_js']['links_removed_after_js']} if node['url'] in no_js else None)
    report['google'] = {'connection': 'offline_exports_only', 'observations': [], 'exhaustive_index_inventory': False}
    for path in observations:
        # Reutiliza validación de propiedad, dominio, operación y payload del adaptador actual.
        observation = import_observation(project, read_json(path))
        report['google']['observations'].append(observation)
        if observation['provider'] == 'gsc' and observation['operation'] == 'inspect_url':
            data = observation['data']
            for node in report['urls']:
                if normalize(node['url']) == normalize(data['url']):
                    node['google_known_index'] = {'observed_at': observation['observed_at'], **data}
                    node['indexability']['google_selected_canonical'] = data.get('index_status', {}).get('googleCanonical')
    from .coverage_import import validate_export
    report['google']['coverage_exports'] = []
    by_normalized_url = {normalize(n['url']): n for n in report['urls']}
    for path in coverage_exports:
        document = validate_export(project, read_json(path))
        report['google']['coverage_exports'].append({'observed_at': document['observed_at'], 'sha256': digest(path), 'rows': len(document['rows']), 'exhaustive': False})
        for row in document['rows']:
            node = by_normalized_url.get(normalize(row['url']))
            if node is not None:
                node['google_coverage_export'] = {'observed_at': document['observed_at'], **row, 'live_query': False}
    by = {n['url']: n for n in report['urls']}
    for node in report['graph']['nodes']:
        if node['url'] in by:
            node.update(by[node['url']])
    report['enriched_at'] = now()
    return report


def _execute(project, args):
    command = args.seo_command
    inputs = []
    if command == 'sitemap':
        authorize_url(project, args.source_url)
        result = {'kind': 'seo-sitemap-v4', 'project': project.id, 'at': now(),
                  **parse_sitemap(reports.read_text(args.xml), source=args.source_url), 'remote_mutations': False}
        # El tipo XML es un campo separado del tipo del informe CLI.
        result['xml_kind'], result['kind'] = result['kind'], 'seo-sitemap-v4'
        inputs = [args.xml]
    elif command == 'crawl':
        limits = Limits(**{f.name: getattr(args, f.name) for f in fields(Limits)}).validate()
        fixture = OfflineResponses(project, args.responses) if args.responses else None
        result = crawl(project, limits=limits, allow_network=args.allow_network, transport=fixture,
                       targets=getattr(args, '_closed_targets', None), on_event=getattr(args, '_closed_checkpoint', None),
                       clock=fixture.clock if fixture else None, sleep=fixture.sleep if fixture else None)
        if getattr(args, '_closed_targets', None):
            inputs.append(args.targets_manifest)
            result['pilot_manifest_sha256'] = args.targets_sha256
            result['checkpoint'] = str(args._closed_checkpoint_path)
        if fixture:
            result['provenance']['clock'] = 'virtual_offline_not_network_timing'
            inputs.append(args.responses)
    elif command == 'readiness':
        result = captured_readiness(project, args.capture, args.no_js, args.robots, args.facts)
        inputs = [p for p in [args.capture, args.no_js, args.robots, args.facts] if p]
    elif command == 'enrich':
        result = enrich_report(project, read_json(args.crawl), args.capture, args.no_js, args.google_observation, args.coverage_export)
        inputs = [args.crawl, *args.capture, *args.no_js, *args.google_observation, *args.coverage_export]
    elif command == 'coverage-import':
        from .coverage_import import import_csv
        result = import_csv(project, reports.read_text(args.csv), site_url=args.site_url,
            observed_at=args.observed_at, mapping=read_json(args.mapping), max_rows=args.max_rows)
        inputs = [args.csv, args.mapping]
    elif command == 'gate':
        result = compare(project, read_json(args.before), read_json(args.after),
                         important_urls=args.important_url, allow_removed=args.allow_removed_url)
        inputs = [args.before, args.after]
    else:
        raise IpanemaError('Comando V4 desconocido.')
    result = clean(result)
    saved = reports.save_report(project, result, 'seo-v4-' + command, inputs)
    run = Path(saved['report']).parent
    (run / 'report.md').write_text(summary_markdown(result), encoding='utf-8')
    if result['kind'] == 'seo-crawl-v4':
        export(run, result)
    elif command == 'sitemap':
        save_csv(run / 'sitemap.csv', result['entries'], ['url', 'source_sitemap', 'lastmod', 'lastmod_state'])
    write_json(run / 'phase-status.json', {'phase': command, 'state': result.get('state') or result.get('outcome') or 'observed',
               'remote_mutations': False, 'google_indexation_not_inferred': True})
    code = 1 if result.get('outcome') == 'blocked' else 2 if result.get('outcome') == 'insufficient_evidence' or result.get('state') in ('stopped', 'partial') or result.get('errors') else 0
    return {**saved, 'state': result.get('state') or result.get('outcome'), 'csv_directory': str(run)}, code


def summary_markdown(result):
    """Resumen legible; el JSON conserva la evidencia completa y su procedencia."""
    safe = lambda text: str(text).replace('\n', ' ').replace('`', "'")
    lines = ['# Auditoría técnica SEO V4', '',
        f"Proyecto: `{safe(result['project'])}`. Fecha: {safe(result.get('at') or result.get('observed_at'))}.", '',
        f"Estado: **{safe(result.get('outcome') or result.get('state') or 'observed')}**.", '',
        'Una página accesible puede ser candidata a indexación. Este informe no demuestra que Google la haya indexado.', '']
    if result['kind'] == 'seo-crawl-v4':
        lines += [f"URLs comprobadas: {len(result['urls'])}. URLs del sitemap: {len(result['sitemap_urls'])}. Enlaces observados: {len(result['edges'])}.",
            f"Enlaces rotos comprobados: {len(result['graph']['broken_internal_links'])}. Candidatos sin ruta desde Inicio: {len(result['graph']['potential_orphans'])}.",
            'Los candidatos no son páginas huérfanas confirmadas: el rastreo puede ser parcial.', '',
            'Clasificación técnica: `' + safe(result['indexability_counts']) + '`.', '',
            'Límites y solicitudes: `' + safe(result['provenance']) + '`.', '',
            f"Errores registrados: {len(result['errors'])}. Acciones priorizadas: {len(result['backlog'])}.", '',
            'Consultar urls.csv, sitemap.csv, edges.csv y backlog.csv junto al JSON.']
    elif result['kind'] == 'seo-readiness-v4':
        node = result['node']
        lines += [f"URL: {safe(node['url'])}.", '',
            'Clasificación: `' + safe(node['indexability']['state']) + '`.',
            'Bloqueos críticos: `' + safe(node['readiness']['critical_blockers']) + '`.',
            'Evidencia necesaria pendiente: `' + safe(node['readiness']['required_evidence_missing']) + '`.']
    elif result['kind'] == 'seo-regression-gate-v4':
        lines += [f"Comprobaciones: {len(result['checks'])}. Solicitudes de red: 0.", '']
        lines += ['- ' + safe(c['name']) + ': ' + c['status'] for c in result['checks'] if c['status'] != 'passed']
    elif result['kind'] == 'seo-sitemap-v4':
        lines += [f"Formato nativo: {result['xml_kind']}. Entradas: {len(result['entries'])}. Duplicados: {len(result['duplicates'])}. Errores: {len(result['errors'])}."]
    lines += ['', '## Límites', ''] + ['- ' + safe(x) for x in result.get('limitations', [])]
    lines += ['', 'Sin escrituras remotas. No se sustituyó el sitemap nativo.', '']
    return '\n'.join(lines)


# Closed mode has one bounded POSIX worker containing manifest parsing, HTTP,
# analysis AND report export. It reuses _execute, not another crawl loop.
def _pilot_manifest(project, args):
    import hashlib
    path = args.targets_manifest
    if not path or path.is_symlink() or not path.is_file() or path.stat().st_size > 65536:
        raise IpanemaError('Manifiesto del piloto inválido o excedido.')
    raw = path.read_bytes()
    if len(raw) > 65536 or not re.fullmatch(r'[0-9a-f]{64}', args.targets_sha256 or ''):
        raise IpanemaError('Se requiere el hash exacto del manifiesto.')
    if hashlib.sha256(raw).hexdigest() != args.targets_sha256:
        raise IpanemaError('Hash del manifiesto no coincide.')
    def unique(pairs):
        result = {}
        for k, v in pairs:
            if k in result:
                raise IpanemaError('Claves repetidas en manifiesto.')
            result[k] = v
        return result
    data = json.loads(raw, object_pairs_hook=unique)
    policy = Policy(project.data['public_url'])
    if data.get('project') != project.id or data.get('origin') != policy.origin:
        raise IpanemaError('Manifiesto de otro proyecto/origen.')
    rows = data.get('targets')
    if not isinstance(rows, list) or len(rows) != 5 or any(not isinstance(x, dict) for x in rows):
        raise IpanemaError('El piloto exige cinco destinos.')
    urls = [x.get('url') for x in rows]
    if any(not isinstance(u, str) or policy.check(u) != u for u in urls) or len(set(urls)) != 5:
        raise IpanemaError('Destinos inválidos, privados o repetidos.')
    return urls


def _checkpoint_writer(path, targets):
    import os
    data = {'project': None, 'state': 'running', 'planned': {u: 'pending' for u in targets},
            'requests': [], 'arrival_at_server_without_response': 'unknown'}
    def persist():
        write_json(path, data, overwrite=True)
        with path.open('rb') as stream:
            os.fsync(stream.fileno())
        fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    def event(row):
        url, kind = row['url'], row['event']
        if kind == 'planned':
            data['planned'].setdefault(url, 'pending')
        elif kind == 'started':
            data['planned'][url] = 'started_without_confirmed_result'
            data['requests'].append({'ordinal': row['ordinal'], 'url': url, 'state': 'started_without_confirmed_result'})
        else:
            current = data['requests'][-1]
            if current['ordinal'] != row['ordinal'] or current['url'] != url:
                raise IpanemaError('Evento de checkpoint fuera de secuencia.')
            if kind == 'completed':
                current.update(state='completed', status=row['status'], bytes=row['bytes'])
                data['planned'][url] = 'completed'
            elif kind != 'unconfirmed':
                raise IpanemaError('Evento de checkpoint desconocido.')
        persist()
    persist()
    return event


def _pilot_worker(channel, project, args, checkpoint, work):
    import os
    try:
        os.setsid()
        channel.send({'ready': os.getpid()})
        if channel.recv() != 'go':
            return
        targets = _pilot_manifest(project, args)
        args._closed_targets = targets
        args._closed_checkpoint_path = checkpoint
        args._closed_checkpoint = _checkpoint_writer(checkpoint, [normalize(project.data['public_url']) + 'robots.txt', *targets])
        result = work(project, args)
        channel.send({'result': result})
    except Exception as exc:
        channel.send({'error': type(exc).__name__, 'message': 'Piloto abortado; consultar checkpoint si existe.'})
    finally:
        channel.close()


def _supervise_pilot(project, args, *, work=None):
    import multiprocessing
    import os
    import signal
    import time
    import uuid
    if os.name != 'posix':
        raise IpanemaError('El piloto requiere supervisión POSIX; sin fallback sin límite.')
    limits = pilot_limits(Limits(**{f.name: getattr(args, f.name) for f in fields(Limits)}))
    started = time.monotonic()
    seconds = limits.max_seconds
    grace = min(1., seconds / 4)
    deadline = started + seconds
    # Pure path construction; all filesystem/manifest/report work runs in child.
    run = project.evidence_root / ('pilot-checkpoint-' + uuid.uuid4().hex)
    checkpoint = run / 'checkpoint.json'
    parent, child = multiprocessing.get_context('fork').Pipe()
    process = multiprocessing.get_context('fork').Process(target=_pilot_worker,
                args=(child, project, args, checkpoint, work or _execute))
    ready, message, stopped = False, None, False
    previous = {}
    def interrupt(signum, frame):
        raise IpanemaError('Piloto interrumpido por señal; estado de llegada no inferido.')
    try:
        for sig in (signal.SIGTERM, signal.SIGINT):
            previous[sig] = signal.signal(sig, interrupt)
        process.start()
        child.close()
        while time.monotonic() < deadline - grace:
            if parent.poll(min(.05, max(0, deadline - grace - time.monotonic()))):
                try:
                    message = parent.recv()
                except EOFError:
                    message = {'error': 'worker_eof'}
                    break
                if not ready:
                    if message != {'ready': process.pid} or os.getpgid(process.pid) != process.pid:
                        raise IpanemaError('Grupo del worker no validado.')
                    ready = True
                    parent.send('go')
                    message = None
                else:
                    break
            if not process.is_alive():
                break
        if message is None and process.is_alive():
            stopped = True
            if ready:
                os.killpg(process.pid, signal.SIGTERM)
            else:
                process.terminate()
            process.join(timeout=max(0, min(grace / 2, deadline - time.monotonic())))
    except (IpanemaError, OSError) as exc:
        message = {'error': type(exc).__name__}
    finally:
        # Always clean the verified session, even on success or Ctrl-C. Its
        # subprocesses must not outlive a completed/cancelled pilot.
        if process.pid:
            try:
                if ready:
                    os.killpg(process.pid, signal.SIGKILL)
                elif process.is_alive():
                    process.kill()
            except ProcessLookupError:
                pass
            process.join(timeout=max(.05, deadline - time.monotonic()))
        parent.close()
        child.close()
        for sig, handler in previous.items():
            signal.signal(sig, handler)
    record = {'state': 'cancelled_deadline' if stopped else 'worker_failed' if not message or 'error' in message else 'finished', 'worker_pid': process.pid,
              'worker_reaped': process.exitcode is not None, 'wall_seconds': time.monotonic() - started,
              'absolute_limit_seconds': seconds, 'termination_grace_included': grace,
              'checkpoint': str(checkpoint), 'remote_mutations': False}
    # A supervisor receipt is outside the cancelled worker's work. No HTTP or
    # analysis can continue while it is being recorded.
    write_json(run / 'supervision.json', record)
    if stopped or not message or 'error' in message or process.exitcode is None:
        return {'state': 'stopped', 'checkpoint': str(checkpoint), 'supervision': str(run / 'supervision.json'),
                'reason': 'absolute_deadline' if stopped else 'worker_failed', 'remote_mutations': False}, 2
    return message['result']


def execute(project, args):
    if args.seo_command == 'crawl' and getattr(args, 'targets_manifest', None):
        return _supervise_pilot(project, args)
    if getattr(args, 'targets_sha256', None):
        raise IpanemaError('--targets-sha256 requiere --targets-manifest.')
    return _execute(project, args)
