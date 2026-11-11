"""CLI incremental V4: parsers, crawler explícito, capas y gates sobre motor existente."""
from __future__ import annotations

from dataclasses import fields
import json
from pathlib import Path
import re

from ..core import IpanemaError, digest, now, read_json, redact, write_json
from . import reports
from .adapters import authorize_url, import_observation
from .crawl_policy import Limits, normalize
from .crawler import crawl, export, save_csv
from .extractor import extract
from .indexability import Content, classify, layers, page_type, pagination, readiness, template_checks
from .regression import compare
from .robots import Robots
from .sitemaps import parse_sitemap

COMMANDS = {'sitemap', 'crawl', 'readiness', 'enrich', 'gate'}


def add_parser(commands):
    sitemap = commands.add_parser('sitemap', help='Parsear sitemap nativo offline, sin reemplazarlo')
    sitemap.add_argument('--xml', type=Path, required=True)
    sitemap.add_argument('--source-url', required=True)
    crawler = commands.add_parser('crawl', help='BFS solo lectura; red requiere permiso y límites')
    mode = crawler.add_mutually_exclusive_group(required=True)
    mode.add_argument('--allow-network', action='store_true')
    mode.add_argument('--responses', type=Path, help='Fixture/export local explícito; no hace red')
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


def enrich_report(project, report, capture_paths, no_js_paths, observations):
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
    by = {n['url']: n for n in report['urls']}
    for node in report['graph']['nodes']:
        node.update(by[node['url']])
    report['enriched_at'] = now()
    return report


def execute(project, args):
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
                       clock=fixture.clock if fixture else None, sleep=fixture.sleep if fixture else None)
        if fixture:
            result['provenance']['clock'] = 'virtual_offline_not_network_timing'
            inputs = [args.responses]
    elif command == 'readiness':
        result = captured_readiness(project, args.capture, args.no_js, args.robots, args.facts)
        inputs = [p for p in [args.capture, args.no_js, args.robots, args.facts] if p]
    elif command == 'enrich':
        result = enrich_report(project, read_json(args.crawl), args.capture, args.no_js, args.google_observation)
        inputs = [args.crawl, *args.capture, *args.no_js, *args.google_observation]
    elif command == 'gate':
        result = compare(project, read_json(args.before), read_json(args.after),
                         important_urls=args.important_url, allow_removed=args.allow_removed_url)
        inputs = [args.before, args.after]
    else:
        raise IpanemaError('Comando V4 desconocido.')
    result = clean(result)
    saved = reports.save_report(project, result, 'seo-v4-' + command, inputs)
    run = Path(saved['report']).parent
    if result['kind'] == 'seo-crawl-v4':
        export(run, result)
    elif command == 'sitemap':
        save_csv(run / 'sitemap.csv', result['entries'], ['url', 'source_sitemap', 'lastmod', 'lastmod_state'])
    write_json(run / 'phase-status.json', {'phase': command, 'state': result.get('state') or result.get('outcome') or 'observed',
               'remote_mutations': False, 'google_indexation_not_inferred': True})
    code = 1 if result.get('outcome') == 'blocked' else 2 if result.get('outcome') == 'insufficient_evidence' or result.get('state') == 'stopped' else 0
    return {**saved, 'state': result.get('state') or result.get('outcome'), 'csv_directory': str(run)}, code
