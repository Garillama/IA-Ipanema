#!/usr/bin/env python3
"""Proyecta la evidencia estática a índices y fichas; no modifica el tema."""
import collections
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'ipanema-discovery'
EVID = DOC / '13-evidence/measurements/source-baseline'
load = lambda name: json.loads((EVID / (name + '.json')).read_text())


def write(name, body):
    p = DOC / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body.rstrip() + '\n')


def cell(s):
    return str(s).replace('|', '\\|').replace('\n', ' ')


def anchor(path):
    return re.sub('[^a-z0-9]+', '-', path.lower()).strip('-')


def main():
    summary, comps, settings, edges, uses, files = [load(n) for n in ['source-summary', 'components', 'settings', 'dependency-graph', 'template-instances', 'source-inventory']]
    source = Path(summary['source'])
    date = summary['verified_at'][:10]
    def source_link(p, line=1):
        if Path(p).suffix.lower() in ['.webp','.png','.jpg','.svg','.avif','.woff2']:
            return f'[{p}](<{source / p}>)'
        return f'[{p}:{line}](<{source / p}:{line}>)'
    by_path = {c['path']: c for c in comps}
    runtime=[]
    for p in (DOC/'13-evidence/measurements/crawl').glob('*.json'):
        obj=json.loads(p.read_text())
        if isinstance(obj,dict) and 'dom' in obj:runtime.append(obj)
    relations = collections.defaultdict(set)
    for e in edges:
        if e['kind'] in ('twig-literal', 'json-instance', 'layout-template'):
            relations[e['source']].add(e['target'])
    # Resolver posibles hijos de schemas; no implica que todas las combinaciones se hayan instanciado.
    schema_edges = []
    def block_rules(obj):
        if isinstance(obj, dict):
            for rule in obj.get('blocks', []):
                if isinstance(rule, dict):
                    yield rule
                    yield from block_rules(rule)
    for c in comps:
        for rule in block_rules(c.get('schema') or {}):
            targets = [f"blocks/{rule['type']}.tpl"] if rule.get('type') else [b['path'] for b in comps if b['kind'] == 'blocks' and set(rule.get('tags', [])).intersection((b.get('schema') or {}).get('tags', []))]
            for target in targets:
                if target in by_path:
                    relations[c['path']].add(target)
                    schema_edges.append(dict(source=c['path'], target=target, kind='schema-possible-child', verified_at=date))
    (EVID / 'schema-dependencies.json').write_text(json.dumps(schema_edges, ensure_ascii=False, indent=2) + '\n')
    def reaches(start, target):
        seen, todo = set(), [start]
        while todo:
            cur = todo.pop()
            if cur in seen:
                continue
            seen.add(cur)
            if cur == target:
                return True
            todo.extend(relations[cur] - seen)
        return False
    template_names = [f['path'] for f in files if f['path'].startswith('templates/')]
    matrix = ['# Matriz completa de controles definidos en código', '', f'Verificado {date}. {len(settings)} definiciones, incluidos settings de bloques privados declarados dentro de otros schemas. No equivale a {len(settings)} controles visibles simultáneamente. La interfaz real del Admin no fue abierta.', '', 'Los ámbitos de dispositivo de esta tabla se infieren del identificador: el consumo real se explica en [responsive](../03-editor/responsive-controls.md). Sin default explícito se indica «no disponible»; no significa cero ni false. Valores guardados por instancia: [JSON de instancias](../13-evidence/measurements/source-baseline/template-instances.json). Esquemas íntegros de opciones: [settings.json](../13-evidence/measurements/source-baseline/settings.json).', '']
    grouped = collections.defaultdict(list)
    for s in settings:
        grouped[s['file']].append(s)
    for name, group in grouped.items():
        matrix.extend([f'<a id="{anchor(name)}"></a>', f'## {name}', '', source_link(name), '', '| ID y etiqueta es-MX | Tipo | Ámbito por ID | Default / referencia | Valores o rango | Condición / atributos |', '|---|---|---|---|---|---|'])
        for s in group:
            default = json.dumps(s['default'], ensure_ascii=False) if 'default' in s else ('settings.' + s['default_setting'] if 'default_setting' in s else 'no disponible')
            options = s.get('options')
            if options:
                values = ', '.join(str(o.get('value', o)) if isinstance(o, dict) else str(o) for o in options)
            elif 'min' in s:
                values = f"{s.get('min')}…{s.get('max')}; paso {s.get('step', 'no disponible')}; {s.get('unit', 'sin unidad')}"
            else:
                values = 'no disponible'
            conditions = {k:s[k] for k in ['visible_if','disabled_if','vertical_default','vertical_options','header_toggle','info'] if k in s}
            matrix.append('| ' + ' | '.join(cell(v) for v in [f"`{s['id']}` — {s['label_resolved']} ({s['line']})", s.get('setting_type'),s['scope'],default,values,json.dumps(conditions, ensure_ascii=False) or 'no disponible']) + ' |')
        matrix.append('')
    write('02-native-components/settings-matrix.md', '\n'.join(matrix))
    inv = ['# Inventario de unidades del tema', '', f'Verificado {date}; inspección estática: {summary["sections"]} secciones, {summary["blocks"]} bloques y {summary["snippets"]} snippets. Un snippet puede ser un fragmento técnico, no un componente visible autónomo. Disponibilidad visual depende del schema, del template y de datos de plataforma.', '', 'Cada ficha registra límites, evidencia y pendientes de ejecución. «Existente en código» no certifica que esté habilitado en la tienda remota.', '', '| Unidad / ficha | Identificador | Nombre del schema o archivo | Settings definidos | Instancias JSON |', '|---|---|---|---|---|']
    specs_index = ['# Fichas técnicas', '', 'Fuente principal: una ficha por unidad de archivo; los análisis de comercio, imágenes y motion profundizan los componentes compartidos. Los campos de comportamiento no ejecutado se marcan sin inventar resultados.', '']
    reuse = ['# Matriz de reutilización por unidad', '', 'A: configuración nativa declarada; B: estilos propios del tema personalizables mediante CSS (evaluar cascada); C: cambios a Twig/lógica/CSS core requieren fork autorizado; D: extensión conductual puede requerir JS; E: plataforma/app según el caso; F: patrón de interfaz reutilizable sin copiar implementación propietaria; G: no es una unidad autónoma exportable. Las letras no son permisos de redistribución.', '', '| Unidad | Clasificación | Motivo |', '|---|---|---|']
    js_text = (source / 'static/js/store.js').read_text().splitlines()
    for c in comps:
        name, kind = c['path'], c['kind']
        schema = c.get('schema') or {}
        own_settings = grouped[name]
        spec_file = 'specifications/' + name[:-4].replace('/', '--') + '.md'
        instances = [u for u in uses if ('sections/' if u['kind'] == 'section' else 'blocks/') + str(u['type']) + '.tpl' == name]
        direct = [e for e in edges if e['source'] == name and e['kind'] != 'json-instance']
        incoming = [e for e in edges if e['target'] == name and e['kind'] != 'json-instance']
        pages = [t for t in template_names if reaches(t, name)]
        hook_lines = []
        for i,l in enumerate(js_text,1):
            if any(h in l for h in c['js_hooks']):
                hook_lines.append(i)
        inv.append(f'| [{name}]({spec_file}) | `{c["id"]}` | {cell(c["name"] or "no disponible")} | {len(own_settings)} | {len(instances)} |')
        specs_index.append(f'- [{c["id"]}]({spec_file})')
        codes = 'A, B, C, F' if schema else 'B, C, F, G'
        if c['js_hooks']:
            codes += ', D'
        if any(e['kind'] == 'platform-component' for e in direct):
            codes += ', E'
        reuse.append(f'| [{name}]({spec_file}) | {codes} | ' + ('Tiene schema; reutilizar su tipo y configuración dentro de los padres permitidos.' if schema else 'Partial compartido; reutilizar con include y contexto correcto, no insertarlo como sección del editor.') + (' Contratos js-* presentes; el HTML por sí solo no replica la interacción.' if c['js_hooks'] else '') + ' |')
        limits = {k:schema[k] for k in ['tags','class','category','limit','enabled_on','disabled_on','deletable','hideable','locked_blocks','max_blocks'] if k in schema}
        tags = ', '.join(f'{k}: {v}' for k,v in c['tags'].items()) or 'no disponible (puede provenir de includes)'
        vars_ = ', '.join('`'+v+'`' for v in c['css_variables']) or 'no disponible en este archivo'
        title = c['name'] or Path(name).stem
        # Mantener los datos específicos arriba; los campos transversales son un contrato común.
        observed=[r for r in runtime if kind=='sections' and any(s.get('type')==Path(name).stem for s in r['dom'].get('sections',[]))]
        body=[f'# {title}', '', f'**Identificador:** `{c["id"]}` · **Tipo:** {kind} · **Fecha:** {date} · **Estado:** confirmado en source; ficha estática con pruebas parciales enlazadas.', '', f'**Fuente:** {source_link(name)}. **Schema:** '+(source_link(name,c['schema_line']) if c['schema_line'] else 'no disponible; partial sin schema propio')+'.', '', '| Campo | Evidencia / valor |','|---|---|',f'| Función / nombre | {cell(title)}; unidad {cell(Path(name).stem)} de {kind}; seguir consumidores para su papel en la página |', '| Consumidores literales | '+cell(', '.join(f'{e["source"]}:L{e.get("line",1)}' for e in incoming) or 'Inclusión dinámica, JSON o no disponible')+' |','| Ubicaciones posibles por grafo | '+cell(', '.join(pages) or 'no disponible')+' |','| Instancias guardadas | '+cell(', '.join(u['location'] for u in instances) or 'no disponible')+' |','| Dependencias | '+cell(', '.join(f'{e["target"]} ({e["kind"]}, L{e.get("line",1)})' for e in direct) or 'no disponible como literal')+' |','| Restricciones | '+cell(json.dumps(limits,ensure_ascii=False))+' |','| Bloques admitidos | schema.blocks en components.json, incluidos privados del padre |','| Configuración/defaults | '+(f'[Matriz exacta](../settings-matrix.md#{anchor(name)})' if own_settings else 'Sin schema propio; contexto del consumidor')+' |','| Desktop dedicado por ID | '+cell(', '.join(s['id'] for s in own_settings if s['scope']=='desktop') or 'no disponible; revisar controles compartidos')+' |','| Mobile dedicado por ID | '+cell(', '.join(s['id'] for s in own_settings if s['scope']=='mobile') or 'no disponible')+' |','| Tablet dedicado | no disponible en IDs; no implica ausencia de media queries |','| Breakpoints | [Cortes y consumo](../../03-editor/responsive-controls.md); verificar qué selector aplica |','| Variables CSS locales | '+cell(vars_)+' |','| Hooks JS | '+cell(', '.join(c['js_hooks']) or 'no disponible en marcado directo')+' |','| Referencias store.js | '+cell(', '.join('L'+str(i) for i in hook_lines) or 'no disponible por búsqueda literal; puede residir en LS')+' |','| Eventos / estados | [Contratos](../../09-integrations/events-and-hooks.md); no todos los estados de esta unidad fueron ejecutados |','| Clases candidatas | '+cell(', '.join(c['classes']) or 'no disponible')+' |','| Atributos data | '+cell(', '.join(c['data_attributes']) or 'no disponible')+' |','| Semántica directa | '+cell(tags)+'; excluye hijos y plataforma |','| Accesibilidad | [Resultados por ruta/estado](../../10-quality/accessibility.md); no certificación individual |','| SEO | [Pruebas y criterios](../../04-seo/technical-seo.md); impacto individual no aislado |','| LCP / INP / CLS | [Métricas de página](../../05-performance/core-web-vitals.md); sin atribución aislada a esta unidad ni INP de campo |',f'| Imágenes | {c["image_includes"]} includes literales de image.tpl, más posibles hijos |','| Reutilización | '+codes+'; [motivos y alcance](../reusable-components.md) |','| Presencia observada en rutas | '+str(len(observed))+' registros de crawl para este tipo de sección; '+('ver runtime-page-audit' if observed else 'no atribuible directamente para partial/bloque o no presente')+' |','| Personalización recomendada | '+('Configurar tipo/padre existente; tokens globales solo para alcance global' if schema else 'Reutilizar include y contexto de datos')+' |','| Riesgos / límites | [Contrato común de fichas](../specification-method.md); restricciones específicas en la fila Restricciones |','| Ejemplo de localización | `rg -n --fixed-strings "'+cell(Path(name).stem if schema else name)+'" templates sections blocks snippets` |','| Cómo verificar | [Matriz QA](../../10-quality/testing-matrix.md), callers y estados pertinentes; falta cobertura de todas las variantes del editor |','', '**Método:** extracción estática; el grafo incluye hijos posibles por schema y no presencia garantizada. Clases son candidatos léxicos, no selectores certificados del DOM. [Datos completos](../../13-evidence/measurements/source-baseline/components.json), [rutas ejecutadas](../../10-quality/runtime-page-audit.md).']
        write('02-native-components/' + spec_file, '\n'.join(body))
    write('02-native-components/component-inventory.md', '\n'.join(inv))
    write('02-native-components/component-specifications.md', '\n'.join(specs_index))
    write('02-native-components/reusable-components.md', '\n'.join(reuse))
    dirs = ['# Mapa de archivos verificados', '', f'Origen: `{source}`. Fecha {date}. Se excluyeron credenciales y metadatos de agentes. Tamaños de archivo sin compresión; no equivalen a transferencia de red.', '', '| Ruta | Bytes | Líneas | SHA-256 |', '|---|---:|---:|---|']
    for f in files:
        dirs.append(f'| {source_link(f["path"])} | {f["bytes"]} | {f.get("lines", "binario")} | `{f["sha256"]}` |')
    write('01-architecture/directory-map.md', '\n'.join(dirs))
    dep = ['# Dependencias', '', 'Grafo verificado de referencias literales y composición JSON. Los includes construidos con concatenación se registran como prefijos dinámicos; los hijos permitidos por schema se guardan aparte y no prueban presencia efectiva.', '', '[Grafo JSON](../13-evidence/measurements/source-baseline/dependency-graph.json) · [hijos posibles por schema](../13-evidence/measurements/source-baseline/schema-dependencies.json)', '', '| Origen | Destino | Método | Línea / instancia |', '|---|---|---|---|']
    for e in edges:
        dep.append('| '+' | '.join(cell(x) for x in [e['source'],e['target'],e['kind'],e.get('location',e.get('line','no disponible'))])+' |')
    write('01-architecture/dependency-map.md', '\n'.join(dep))
    pages = ['# Auditoría estática de todos los templates', '', 'Cada fila corresponde a un archivo encontrado; no se inventan rutas de navegación a partir de su nombre. URL concreta y disponibilidad pública de cada tipo pendientes por contraseña. El grafo de dependencias amplía los componentes de cada sección.', '', '| Template | Secciones en orden | Estado de datos | Validación funcional |', '|---|---|---|---|']
    for t in template_names:
        data = json.loads((source/t).read_text())
        order = data.get('order', [])
        types = [str(data.get('sections',{}).get(k,{}).get('type')) for k in order]
        disabled = [k for k in order if data.get('sections',{}).get(k,{}).get('disabled')]
        template_class='template-'+t.removeprefix('templates/pages/').removesuffix('.json').replace('/','-')
        tested=[r for r in runtime if template_class in r['dom'].get('bodyClass','').split()]
        state=f'{len(tested)} rutas de crawl; revisar runtime-page-audit' if tested else 'Sin recorrido público de este template; revisar límites y password inicial'
        pages.append(f'| {source_link(t)} | {cell(", ".join(types))} | {len(order)} instancias; disabled={cell(disabled)} | {state} |')
    write('10-quality/page-audit.md','\n'.join(pages))
    assets = ['# Medidas estáticas de assets', '', 'Bytes exactos del checkout local; gzip es una estimación obtenida comprimiendo localmente. No es un waterfall ni acredita coste de ejecución, CSS utilizado o entrega del CDN. libraries.js.tpl se transforma al renderizar Twig.', '', '| Archivo | Bytes | Gzip estimado | !important | reduced-motion |', '|---|---:|---:|---:|---:|']
    for f in files:
        if 'gzip_estimate_bytes' in f:
            assets.append(f'| {source_link(f["path"])} | {f["bytes"]} | {f["gzip_estimate_bytes"]} | {f["important_count"]} | {f["reduced_motion_count"]} |')
    write('05-performance/static-asset-measurements.md','\n'.join(assets))
    print(json.dumps({'component_sheets':len(comps),'settings':len(settings),'templates':len(template_names),'schema_edges':len(schema_edges)},ensure_ascii=False))


if __name__ == '__main__':
    main()
