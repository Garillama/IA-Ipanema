#!/usr/bin/env python3
"""Verifica enlaces, datos e integridad del origen sin escribir en el tema."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote

root=Path(__file__).resolve().parents[1]
doc=root/'ipanema-discovery'
base=doc/'13-evidence/measurements/source-baseline'
errors=[]
summary=json.loads((base/'source-summary.json').read_text())
origin=Path(summary['source'])
files=json.loads((base/'source-inventory.json').read_text())
for entry in files:
    p=origin/entry['path']
    if not p.is_file():errors.append('Archivo de origen ausente: '+entry['path'])
    elif hashlib.sha256(p.read_bytes()).hexdigest()!=entry['sha256']:
        errors.append('Origen cambió desde baseline: '+entry['path'])
managed_json=[*doc.rglob('*.json'),*(root/'projects').rglob('*.json')]
for p in managed_json:
    if 'node_modules' in p.parts:continue
    try:json.loads(p.read_text())
    except (ValueError,UnicodeDecodeError) as e:errors.append(f'JSON inválido {p.relative_to(root)}: {e}')
links=0
managed_md=[root/'README.md',root/'AGENTS.md',*doc.rglob('*.md'),*(root/'.agents/skills/ipanema-storefront').rglob('*.md')]
for p in managed_md:
    text=p.read_text()
    if not text.strip():errors.append('Markdown vacío: '+str(p.relative_to(root)))
    for match in re.finditer(r'(?<!!)\[[^\]]+\]\((<[^>]+>|[^\s)]+)\)',text):
        target=match.group(1).strip('<>')
        if re.match(r'^[a-zA-Z]+://|^mailto:|^app:',target):continue
        raw,_,anchor=target.partition('#')
        raw=unquote(raw)
        line=None
        m=re.search(r':(\d+)$',raw)
        if m:line=int(m.group(1));raw=raw[:m.start()]
        dest=(p.parent/raw).resolve() if raw else p.resolve()
        links+=1
        if not dest.exists():errors.append(f'Enlace roto {p.relative_to(root)} -> {target}');continue
        if line and dest.is_file():
            try:
                if line>len(dest.read_text().splitlines()):errors.append(f'Línea inexistente: {target}')
            except UnicodeDecodeError:errors.append(f'Línea en binario: {target}')
        if anchor and dest.suffix=='.md':
            content=dest.read_text()
            headings=[]
            for h in re.findall(r'^#+\s+(.+)$',content,re.M):
                clean=re.sub(r'[^\w\- ]','',h.lower()).replace(' ','-')
                headings.append(clean)
            if f'id="{anchor}"' not in content and anchor not in headings:
                errors.append(f'Ancla no verificada: {p.relative_to(root)} -> {target}')
components=json.loads((base/'components.json').read_text())
sheets=list((doc/'02-native-components/specifications').glob('*.md'))
if len(sheets)!=len(components):errors.append('Número de fichas diferente al inventario')
settings=json.loads((base/'settings.json').read_text())
if len(settings)!=summary['settings']:errors.append('Número de settings inconsistente')
status=subprocess.run(['git','-C',str(origin),'status','--porcelain=v1'],capture_output=True,text=True)
if status.returncode or status.stdout:errors.append('Git del origen ya no está limpio; revisar, sin descartar cambios')
result={'source_files_unchanged':len(files)-sum(x.startswith(('Origen cambió','Archivo de origen')) for x in errors),'source_files_checked':len(files),'markdown_links_checked':links,'component_sheets':len(sheets),'settings':len(settings),'errors':errors}
print(json.dumps(result,ensure_ascii=False,indent=2))
sys.exit(1 if errors else 0)
