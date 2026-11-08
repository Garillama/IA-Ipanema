"""Entradas de evidencia, auditorías y entregables integrados con Project.new_run."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from ..core import IpanemaError, digest, now, read_json, write_json
from .adapters import authorize_url
from .extractor import extract
from .generator import checked_facts, validation_facts
from .page_audit import PAGE_SCHEMAS, audit_html, audit_snapshot, internal_architecture
from .source_audit import audit_theme, breadcrumb_proposal, native_markers


def read_text(path):
    path = Path(path)
    if not path.is_file() or path.stat().st_size > 10_000_000:
        raise IpanemaError('Entrada SEO inexistente o mayor a 10 MB.')
    return path.read_text(encoding='utf-8')


def markdown(report):
    if report.get('kind') != 'seo-page-audit':
        return '# Informe SEO\n\nConsultar JSON para evidencia y límites de este informe.\n'
    clean = lambda value: str(value).replace('\n', ' ').replace('|', '\\|')
    lines = [f"# Auditoría SEO: {clean(report['page_type'])}", '',
             f"Proyecto: `{report['project']}` · URL: {report['url']} · Análisis: {report['at']}", '',
             f"HTTP: {report['http_status']} · Canonical: {clean(report['canonical'])}.",
             f"Señales observables: `{report['indexability_observable']}`. Indexación: **no comprobada**.", '',
             '## Datos estructurados', '',
             f"Tipos detectados: {clean(report['structured_data']['graph']['types'])}.",
             f"Estados: `{clean(report['structured_data']['states'])}`.", '',
             '## Hallazgos y acciones', '', '| Regla | Prioridad | Evidencia / problema | Acción |', '|---|---|---|---|']
    for f in report['findings']:
        lines.append(f"| {f['rule']} | {f['priority']} / {f['severity']} | {clean(f['message'])} | {clean(f.get('fix') or 'Revisar fuente/consumidores y prueba del caso.')} |")
    lines += ['', '## Límites', ''] + ['- ' + x for x in report['limitations']]
    return '\n'.join(lines) + '\n'


def save_report(project, report, label='seo-audit', inputs=None):
    run = project.new_run(label)
    report['evidence'] = {'input_files': [{'name': Path(p).name, 'sha256': digest(Path(p))} for p in inputs or []],
                          'saved_at': now(), 'remote_mutations': False}
    write_json(run / 'report.json', report)
    (run / 'report.md').write_text(markdown(report), encoding='utf-8')
    return {'kind': report['kind'], 'report': str(run / 'report.json'), 'summary': str(run / 'report.md'),
            'findings': len(report.get('findings', [])), 'external_google_validation': 'not_checked',
            'remote_mutations': False}


def from_html(project, path, url, page_type, *, rendered=None, no_js=None, facts=None, status=None, robots=None):
    authorize_url(project, url)
    data = validation_facts(checked_facts(project, read_json(facts))[0]) if facts else None
    return audit_html(project, read_text(path), url, page_type, status=status,
                      rendered_html=read_text(rendered) if rendered else None, no_js_html=read_text(no_js) if no_js else None,
                      facts=data, robots_text=read_text(robots) if robots else None)


def from_projection(project, path, *, no_js=None, facts=None):
    capture = read_json(path)
    if capture.get('kind') != 'seo-browser-projection' or capture.get('project') != project.id:
        raise IpanemaError('Captura SEO incompatible o de otro proyecto.')
    authorize_url(project, capture['url'])
    page_type = capture.get('page_type', 'page')
    if page_type not in PAGE_SCHEMAS:
        page_type = 'page'
    no_capture=read_json(no_js) if no_js else None
    if no_capture and (no_capture.get('project')!=project.id or no_capture.get('url')!=capture['url'] or no_capture.get('mode')!='no-js'):
        raise IpanemaError('Captura sin JS de otro proyecto, URL o modo.')
    no_html = no_capture['rendered']['html'] if no_capture else None
    data = validation_facts(checked_facts(project, read_json(facts))[0]) if facts else None
    report = audit_html(project, capture['initial']['html'], capture['url'], page_type, status=capture.get('status'),
                        headers=capture.get('headers'), rendered_html=capture['rendered']['html'], no_js_html=no_html, facts=data,
                        source_map=native_markers(project.theme_root) if project.theme_root and project.theme_root.is_dir() else None)
    report['observation'] = {k: capture.get(k) for k in ('at', 'width', 'mode')}
    report['limitations'] += capture['initial'].get('limitations', [])
    if capture['initial'].get('json_ld_redacted') or capture['initial'].get('projection')=='seo-public-markup-v1':
        report['structured_data']['states']['raw_original_json_syntax']='not_checked_projection_reserialized_or_redacted'
        report['limitations'].append('JSON-LD pudo ser serializado/redactado en esta proyección; la sintaxis comprobada corresponde al artefacto, no al texto original completo.')
    report['rendered_validation'] = audit_html(project, capture['rendered']['html'], capture['url'], page_type,
                                             status=capture.get('status'), headers=capture.get('headers'), facts=data)['structured_data']
    return report


def from_historical(project, record, page_type, *, observed_at=None):
    """V1 stored summaries, not reconstructable initial HTML. Do not fake a capture."""
    dom = record.get('sample') or record.get('dom') or {}
    url = record.get('final_url') or record.get('url')
    authorize_url(project, url)
    snap = extract('', url, status=record.get('status'))
    snap['title'] = dom.get('title', '')
    snap['lang'] = dom.get('lang')
    snap['headings'] = [{'level': int(h['tag'][1:]), 'text': h['text'], 'line': None, 'context': {}} for h in dom.get('headings', [])]
    for meta in dom.get('metadata', []):
        if meta.get('name') == 'canonical' and meta.get('href'):
            snap['canonical'].append(meta['href'])
        elif meta.get('name') and meta.get('content') is not None:
            snap['meta'].setdefault(meta['name'], []).append(meta['content'])
    snap['links'] = [{**link, 'absolute': link.get('href'), 'context': {}} for link in dom.get('links', [])]
    snap['images'] = dom.get('images', [])
    if 'jsonld' in dom:
        for i, block in enumerate(dom['jsonld']):
            snap['json_ld'].append({'index': i, 'data': block.get('value'), 'error': {'message': block['error']} if block.get('error') else None,
                                   'component': block.get('component'), 'line': None, 'raw': ''})
    report = audit_snapshot(project, snap, page_type)
    report['observation'] = {'at': observed_at or record.get('at'), 'source': 'historical_v1_dom', 'fresh_browser_execution': False}
    report['structured_data']['states']['syntax_valid'] = 'not_retested_raw_json_missing'
    report['limitations'] += ['Auditoría de evidencia histórica: HTML inicial y JSON-LD original no conservados íntegramente.',
                              'JSON-LD resumido por tipos/errores no se convierte en entidades completas.',
                              'Ausencia en estos campos no demuestra ausencia en la tienda actual.']
    return report


def source_report(project):
    theme = project.require_theme()
    result = audit_theme(theme)
    proposal = breadcrumb_proposal(theme)
    result.update({'kind': 'seo-source-audit', 'project': project.id, 'at': now(),
                   'native_markers': native_markers(theme),
                   'breadcrumb_proposal': proposal, 'theme_modified': False,
                   'limitations': ['Inspección de código actual y modelo abstracto de ramas, no ejecución de Twig/plataforma.',
                                  'No identifica automáticamente qué aplicación inyecta marcado en tiempo de ejecución.']})
    return result


def corpus(project, paths, sitemap=None):
    reports = [read_json(p) for p in paths]
    for report in reports:
        if report.get('project') != project.id or report.get('kind') != 'seo-page-audit':
            raise IpanemaError('El corpus necesita auditorías de página del mismo proyecto.')
        authorize_url(project, report['url'])
    urls = read_json(sitemap) if sitemap else None
    if urls is not None:
        if not isinstance(urls, list):
            raise IpanemaError('Inventario de sitemap debe ser una lista de URLs extraídas con evidencia propia.')
        for url in urls:
            authorize_url(project, url)
    return {'kind': 'seo-link-corpus', 'project': project.id, 'at': now(),
            **internal_architecture(reports, sitemap_urls=urls)}
