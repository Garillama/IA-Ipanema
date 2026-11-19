"""A plain-link receipt must not certify line/anchor semantics: offline fixture."""
from pathlib import Path
import sys,tempfile
candidate=Path('/home/alanrichard/Escritorio/IA inversa/.local/scent-skill-contract-candidate')
sys.path[:0]=[str(candidate),str(candidate/'tools')]
from tests.support import make_project,put
from ipanema.core import Project
from ipanema.snapshot_links import capture_omitted_links
from ipanema.validation import validate
with tempfile.TemporaryDirectory() as folder:
 root=Path(folder);source=make_project(root/'source',theme=False);snapshot=make_project(root/'snapshot',theme=False)
 text='[plain](reports/runs/old/report.json) [line](reports/runs/old/report.json:999999)\n[plainmd](reports/runs/old/report.md) [anchor](reports/runs/old/report.md#inexistente)'
 for r in [source,snapshot]:(r/'README.md').write_text(text)
 for name,body in [('report.json','{}'),('report.md','# Existing')]:put(source/'reports/runs/old'/name,body)
 evidence=snapshot/'ipanema-discovery/13-evidence/measurements/source-baseline'
 for name,value in [('source-summary.json',{'settings':0}),('source-inventory.json',[]),('components.json',[]),('settings.json',[])]:put(evidence/name,value)
 (snapshot/'AGENTS.md').write_text('Fixture rules')
 receipts=capture_omitted_links(source,snapshot);result=validate(Project(snapshot),snapshot_receipts=receipts)
 print('receipt_rows',len(receipts['links']),'excluded',result['snapshot_links_excluded'],'errors',result['errors'])
 assert len(result['errors'])==2,'Qualified links incorrectly inherited plain-link identity receipts'
