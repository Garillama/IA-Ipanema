#!/usr/bin/env python3
"""Inventario estático de un tema autorizado. Solo lee el origen; escribe evidencia aparte."""
import argparse
import collections
import datetime as dt
import hashlib
import gzip
import json
from pathlib import Path
import re
import subprocess

AREAS = ('blocks', 'config', 'layouts', 'sections', 'snippets', 'static', 'templates', 'translations')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def line_of(text, position):
    return text.count('\n', 0, position) + 1


def walk_settings(obj):
    if isinstance(obj, dict):
        if 'id' in obj and ('setting_type' in obj or obj.get('type') == 'setting'):
            yield obj
        for k, v in obj.items():
            if k not in ('options', 'presets'):
                yield from walk_settings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk_settings(v)


def instances(obj, location, results):
    if not isinstance(obj, dict):
        return
    for group, kind in [('sections', 'section'), ('blocks', 'block')]:
        values = obj.get(group, {})
        entries = values.items() if isinstance(values, dict) else enumerate(values) if isinstance(values, list) else []
        for key, val in entries:
            if not isinstance(val, dict):
                continue
            key = str(key)
            entry = dict(file=location.split('#')[0], location=location + '/' + key,
                         kind=kind, type=val.get('type'), disabled=val.get('disabled', False),
                         settings=val.get('settings', {}), order=obj.get('order', obj.get('block_order', [])))
            results.append(entry)
            instances(val, location + '/' + key, results)


def md(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path)
    parser.add_argument('--project')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.source:
        root = args.source.resolve()
    else:
        from ipanema.core import Project, IpanemaError
        try:
            root = Project(project_id=args.project).require_theme()
        except IpanemaError as exc:
            parser.error(str(exc))
    out = args.output.resolve()
    if root == out or root in out.parents or out in root.parents:
        parser.error('El destino debe estar fuera del árbol de origen y no ser su ancestro.')
    for required in ['layouts/layout.tpl', 'config/settings_schema.json', 'templates/pages/home.json']:
        if not (root / required).is_file():
            parser.error('No se reconoce el tema seccionable: falta ' + required)
    if out.exists() and any(out.iterdir()):
        parser.error('El destino ya contiene una captura. Usa un directorio nuevo para conservar la evidencia histórica.')
    out.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    files, components, settings, edges, uses, errors = [], [], [], [], [], []
    paths = sorted(p for area in AREAS for p in (root / area).rglob('*') if p.is_file() and not p.is_symlink() and root in p.resolve().parents)
    paths += [root / 'manifest.json'] if (root / 'manifest.json').is_file() else []
    labels_path = root / 'translations/es_MX.schema.json'
    labels = json.loads(labels_path.read_text()) if labels_path.is_file() else {}

    def label(s):
        if not isinstance(s, str) or not s.startswith('t:'):
            return s
        value = labels
        for bit in s[2:].split('.'):
            value = value.get(bit) if isinstance(value, dict) else None
        return value or s

    for p in paths:
        rel = p.relative_to(root).as_posix()
        raw = p.read_bytes()
        record = dict(path=rel, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
        files.append(record)
        if p.suffix not in ('.tpl', '.json', '.css', '.js', '.txt'):
            continue
        text = raw.decode('utf-8')
        record['lines'] = len(text.splitlines())
        if rel.startswith('static/') and p.suffix in ('.css', '.js', '.tpl'):
            record['gzip_estimate_bytes'] = len(gzip.compress(raw, mtime=0))
            record['important_count'] = text.count('!important')
            record['media_queries'] = sorted(set(re.findall(r'@media[^\{]+', text)))
            record['reduced_motion_count'] = text.count('prefers-reduced-motion')
        if p.suffix == '.json':
            try:
                data = json.loads(text)
                if rel.startswith('templates/'):
                    instances(data, rel + '#', uses)
            except ValueError as e:
                errors.append(dict(path=rel, error=str(e)))
        for m in re.finditer(r"\{%[-\s]*(?:include|embed|extends|import|from)\s+['\"]([^'\"]+)['\"]", text):
            target = m.group(1)
            dynamic = text[m.end():].lstrip().startswith('~')
            edges.append(dict(source=rel, target=target, line=line_of(text, m.start()),
                              kind='twig-dynamic-prefix' if dynamic else 'twig-literal',
                              exists=None if dynamic else (root / target).is_file()))
        for m in re.finditer(r"component\(\s*['\"]([^'\"]+)['\"]", text):
            edges.append(dict(source=rel, target=m.group(1), line=line_of(text, m.start()), kind='platform-component'))
        for m in re.finditer(r"\{%\s*layout_template\s+['\"]([^'\"]+)['\"]", text):
            edges.append(dict(source=rel, target='templates/layout/' + m.group(1) + '.json', line=line_of(text, m.start()), kind='layout-template'))
        schema_match = re.search(r'\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}', text, re.S)
        schema, schema_line = None, None
        if schema_match:
            try:
                schema = json.loads(schema_match.group(1))
                schema_line = line_of(text, schema_match.start())
            except ValueError as e:
                errors.append(dict(path=rel, error='schema: ' + str(e)))
        if rel == 'config/settings_schema.json':
            schema, schema_line = json.loads(text), 1
        if schema is not None:
            locations = collections.defaultdict(list)
            offsets = collections.Counter()
            schema_start = schema_match.start(1) if schema_match else 0
            for found in re.finditer(r'"id"\s*:\s*"([^"\\]+)"', text[schema_start:]):
                locations[found.group(1)].append(line_of(text, schema_start + found.start()))
            for setting in walk_settings(schema):
                positions = locations[setting['id']]
                index = offsets[setting['id']]
                offsets[setting['id']] += 1
                setting_line = positions[index] if index < len(positions) else schema_line
                settings.append(dict(file=rel, line=setting_line,
                                     label_resolved=label(setting.get('label', 'no disponible')),
                                     scope='mobile' if re.search('mobile', setting['id']) else 'desktop' if 'desktop' in setting['id'] else 'tablet' if 'tablet' in setting['id'] else 'shared',
                                     **setting))
        if p.suffix == '.tpl' and rel.split('/')[0] in ('sections', 'blocks', 'snippets'):
            body = text[:schema_match.start()] if schema_match else text
            components.append(dict(id=rel[:-4].replace('/', ':'), path=rel,
                                   kind=rel.split('/')[0], name=label(schema.get('name')) if isinstance(schema, dict) else p.stem,
                                   name_key=schema.get('name') if isinstance(schema, dict) else None,
                                   schema_line=schema_line, schema=schema,
                                   classes=sorted(set(re.findall(r'(?<![\w-])(?:js-)?[a-zA-Z][a-zA-Z0-9_-]+', ' '.join(re.findall(r'class="([^"]*)"', body))))),
                                   data_attributes=sorted(set(re.findall(r'data-([\w-]+)', body))),
                                   css_variables=sorted(set(re.findall(r'--[a-zA-Z][\w-]*', body))),
                                   setting_refs=sorted(set(re.findall(r'(?:settings|section\.settings|block\.settings)\.([\w]+)', body))),
                                   tags=dict(collections.Counter(re.findall(r'<(h[1-6]|main|header|footer|nav|section|article|aside|a|button|img|picture|form|input|select|video|iframe|ul|li|dialog)\b', body))),
                                   image_includes=body.count('snippets/image.tpl'),
                                   js_hooks=sorted(set(re.findall(r'js-[\w-]+', body))),
                                   raw_count=body.count('| raw'),
                                   block_attributes='block_attributes' in body,
                                   section_attributes='section_attributes' in body))
    for item in uses:
        if item.get('type'):
            edges.append(dict(source=item['file'], target=('sections/' if item['kind'] == 'section' else 'blocks/') + item['type'] + '.tpl', kind='json-instance', location=item['location']))
    try:
        status = subprocess.run(['git', '-C', str(root), 'status', '--porcelain=v1'], capture_output=True, text=True, check=True).stdout
        head = subprocess.run(['git', '-C', str(root), 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        status, head = 'no disponible', 'no disponible'
    manifest = json.loads((root / 'manifest.json').read_text()) if (root / 'manifest.json').exists() else {}
    safe_manifest = {k: manifest.get(k) for k in ('theme', 'theme_version', 'forked')}
    summary = dict(verified_at=now, source=str(root), head=head, git_clean=status == '',
                   local_status=status, manifest=safe_manifest, files=len(files),
                   sections=sum(c['kind'] == 'sections' for c in components),
                   blocks=sum(c['kind'] == 'blocks' for c in components),
                   snippets=sum(c['kind'] == 'snippets' for c in components),
                   templates=sum(f['path'].startswith('templates/') for f in files),
                   settings=len(settings), instances=len(uses), dependencies=len(edges),
                   json_schema_errors=errors,
                   exclusions=['.nuvem', '.git', '.agents', 'secciones.md'],
                   limitations=['Análisis estático; no ejecuta Twig ni prueba editor, red o navegador.',
                                'Las clases extraídas son candidatas; Twig puede producir clases dinámicas.',
                                'Scopes responsive inferidos de IDs; revisar su consumo CSS/Twig.',
                                'Referencias dinámicas no resueltas por este inventario.'])
    for name, data in [('source-inventory', files), ('components', components), ('settings', settings),
                       ('dependency-graph', edges), ('template-instances', uses), ('source-summary', summary)]:
        (out / (name + '.json')).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
