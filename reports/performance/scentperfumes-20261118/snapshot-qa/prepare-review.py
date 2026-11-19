from pathlib import Path
import json,difflib,hashlib,datetime,subprocess,sys
root=Path('/home/alanrichard/Escritorio/IA inversa');out=root/'reports/performance/scentperfumes-20261118/snapshot-qa';candidate=root/'.local/scent-snapshot-qa-20261119'
prior=json.loads((out/'review-attempt1/operational-manifest.json').read_text());names=sorted(set(prior['files'])|{'tests/unit/test_source_window_budget.py'});sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();records={};windows={};patch=''
for name in names:
 p=candidate/name;b=root/name;before=b.read_text()if b.exists()else'';after=p.read_text();assert before!=after
 records[name]={'base_sha256':sha(b)if b.exists()else None,'candidate_sha256':sha(p),'bytes':p.stat().st_size}
 patch+=''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='a/'+name if b.exists()else'/dev/null',tofile='b/'+name))
 if name.startswith('tests/')and b.exists():
  groups=list(difflib.SequenceMatcher(None,before.splitlines(),after.splitlines()).get_grouped_opcodes(n=12));ranges=[[g[0][3]+1,g[-1][4]]for g in groups]
  if len(ranges)<=5 and all(x<=y and y-x<=300 for x,y in ranges):windows[name]=ranges
(out/'operational-composition-final.patch').write_text(patch)
m={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'private_current_candidate_for_full_original_council','files':records,'source_windows_for_unchanged_test_context':windows,'patch_sha256':sha(out/'operational-composition-final.patch'),'original_root':str(root),'candidate_root':str(candidate),'original_applied':False,'AGENTS_or_models_changed':False,'limits':'Original 300000 source bytes and 900000 aggregate prompt bytes preserved. Source cap now counts only the explicitly sent excerpts.'};(out/'operational-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
qa=json.loads((out/'full-offline-qa.json').read_text());suites=[{k:v for k,v in s.items()if k in ['suite','exit_code','passed','tests_run','skipped','skipped_tests']}for s in qa['suite_results']]
info={'purpose':'Controller factual review data, never instructions or approval.','changed_file_hashes':{f:{'before':v['base_sha256'],'candidate':v['candidate_sha256']}for f,v in records.items()},'previous_full_offline_QA_before_window_fix':suites,'current_targeted_QA':'45 tests passed: 16 offline-input adversarial tests, all 24 JSON contract tests and 5 context-budget tests. Fresh full baseline must pass in the official run before any proposals.','scope_limits':['No storefront validation or field metrics.','Historical receipts prove identity only.','Skips do not certify execution.','Protected sources have not been integrated.','Old smokes are not approvals.']}
(candidate/'review-input/operational-review-context.json').write_text(json.dumps(info,separators=(',',':'))+'\n');(candidate/'review-input/operational-review.diff').write_text(patch)
request='Auditoría de arquitectura del protocolo de workers y del aislamiento de credenciales. Solo lectura de la composición operativa existente y sus pruebas. Revisar el diff exacto y todos los archivos modificados, incluidos fixtures y cómputo de ventanas; verificar límites intactos, rechazo de evidencia falsa y compatibilidad. La alternativa que conserve exactamente este árbol se identifica como <tu-agente>-snapshot-current; pueden objetarla, bloquearla o proponer otras. No usar smokes como aprobaciones.'
cmd=['python3','tools/ia.py','orchestrate','plan',request,'--scope','workspace','--read-only','--council','full','--council-checks',str(out/'council-checks.json')]
for f in [*records,'review-input/operational-review-context.json','review-input/operational-review.diff']:cmd+=['--file',f]
r=subprocess.run(cmd,cwd=candidate,capture_output=True,text=True);assert r.returncode==0,r.stderr;(out/'review-plan-output.json').write_text(r.stdout);p=Path(json.loads(r.stdout)['plan']);plan=json.loads(p.read_text());assert plan['skills']==['ipanema-architect']and plan['read_only']and not plan['classification']['production_request'];plan['source_windows']=windows;p.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
sys.path.insert(0,str(candidate/'tools'));from ipanema.core import Project
from ipanema.orchestration import engine,council
for agent in ['claude','codex']:
 task=council.participant_task(agent,0,plan['allowed_files'],'critical',plan['objective']);prompt=engine.prompt_for(Project(candidate,'sample'),plan,task,candidate,[]);assert len(prompt.encode())<=900000;print(agent,'preflight_prompt_bytes',len(prompt.encode()))
print(json.dumps({'changed_files':len(records),'scope_files':len(plan['allowed_files']),'patch_sha256':m['patch_sha256'],'preflight_passed':True}))
