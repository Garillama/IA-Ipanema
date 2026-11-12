"""Acredita v3, reproduce observación humana y prueba un único diff final sin aplicarlo."""
from pathlib import Path
import difflib,hashlib,json,os,re,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
v3=json.loads((ROOT/'reports/seo/v4-patch-review/v3-validation.json').read_text())
patch3=ROOT/v3['patch'];assert sha(patch3)==v3['patch_sha256']
assert all(sha(ROOT/name)==value for name,value in v3['source_hashes'].items()),'La base cambió; no aplicar ni continuar sin revalidar.'
assert not (ROOT/'tests/unit/test_seo_review_additional_v4.py').exists()
assert not (ROOT/'tests/unit/test_seo_robots_values_v4.py').exists()
original_base={n:sha(ROOT/n) for n in v3['source_hashes']}
work=Path(tempfile.mkdtemp(prefix='seo-v4-final-candidate-',dir=ROOT/'.local'))
for name in ('tools','tests'):shutil.copytree(ROOT/name,work/name,ignore=shutil.ignore_patterns('__pycache__'))
env={k:v for k,v in os.environ.items() if not k.startswith('IPANEMA_')};env['IPANEMA_ALLOW_NETWORK']='0'
def run(label,args,cwd=work,runenv=None):
 p=subprocess.run(args,cwd=cwd,env=runenv or env,capture_output=True,text=True,timeout=180)
 data={'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};(OUT/(label+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');return data
assert run('v3-identity-dry-run',['patch','--batch','--forward','--dry-run','-p1','-i',str(patch3)])['exit_code']==0
assert run('v3-identity-apply-isolated',['patch','--batch','--forward','-p1','-i',str(patch3)])['exit_code']==0
assert all(sha(work/n)==v for n,v in v3['candidate_hashes'].items())
matched=[]
for p in sorted((ROOT/'.local').glob('seo-v4-v3-*')):
 if p.is_dir() and all((p/n).is_file() and sha(p/n)==v for n,v in v3['candidate_hashes'].items()):matched.append(str(p.relative_to(ROOT)))
identity={'v3_original':{'path':v3['patch'],'bytes':patch3.stat().st_size,'sha256':sha(patch3)},'manifest_matches':True,'approval_manifest_matches':json.loads((ROOT/'reports/seo/v4-patch-review/approval-manifest.json').read_text())['patch_v3_sha256']==sha(patch3),'fresh_patch_candidate_hashes_match':True,'existing_exact_candidates':matched,'reported_export':{'path':'/mnt/data/Texto pegado (2).txt','sha256':'7fe10ce79ab0de98a078a4fe422ee277c6cfff599aa4e95606cd039dad92340d','bytes':25728,'accessible_here':Path('/mnt/data/Texto pegado (2).txt').is_file(),'authority':'user-supplied description; not a trusted application artifact','byte_difference_cause':'not_determined; not equal merely by removal of final LF'},'decision':'Use immutable original v3 and manifest only; never equate exported text by normalization.'}
(OUT/'identity-v3.json').write_text(json.dumps(identity,ensure_ascii=False,indent=2)+'\n')
values='tests/unit/test_seo_robots_values_v4.py';shutil.copy2(OUT/'value_cases.py',work/values)
# Network forbidden for all injected regression cases; real TLS is a separate explicit loopback fixture.
boot='import socket,unittest,sys;socket.socket.connect=lambda *a,**k: (_ for _ in ()).throw(AssertionError("network_forbidden_in_fixture"));r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(sys.argv[1:]));sys.exit(not r.wasSuccessful())'
before=run('before-parser-on-exact-v3',[sys.executable,'-c',boot,'tests.unit.test_seo_robots_values_v4'])
assert before['exit_code']!=0,'El caso humano debe reproducirse antes de corregir.'
robots=work/'tools/ipanema/seo/robots.py';s=robots.read_text()
assert "for part in header.split(','):" in s
s=s.replace("for part in header.split(','):","for part in _header_parts(header):")
assert '\ndef has_noindex(directives):' in s
s=s[:s.index('\ndef has_noindex(directives):')].rstrip()+'\n\n\n'+(OUT/'parser_candidate.py.txt').read_text()
robots.write_text(s)
# A quoted meta value must reach the extractor unchanged, rather than breaking the fixture attribute.
case=work/'tests/unit/test_seo_review_additional_v4.py';s=case.read_text();s='from html import escape\n'+s;s=s.replace('content="{meta}"','content="{escape(meta,quote=True)}"');case.write_text(s)
specific=run('after-final-specific',[sys.executable,'-c',boot,'tests.unit.test_seo_robots_values_v4','tests.unit.test_seo_review_additional_v4','tests.unit.test_seo_transport_v4'])
unit=run('after-final-seo-unit',[sys.executable,'-m','unittest','discover','-s','tests/unit','-p','test_seo*.py','-q'])
integration=run('after-final-seo-integration',[sys.executable,'-m','unittest','discover','-s','tests/integration','-p','test_seo*.py','-q'])
tls=run('after-final-local-tls',[sys.executable,str(ROOT/'reports/seo/v4-patch-review/tls_fixture.py')],runenv={**env,'PYTHONPATH':str(work/'tools')})
# Reuse the actual QA CLI, with an isolated synthetic project and no theme/account.
setup='from pathlib import Path;from tests.support import make_project;make_project(Path.cwd(),identifier="fixture",theme=False)'
assert run('candidate-fixture-setup',[sys.executable,'-c',setup])['exit_code']==0
qa=run('after-final-seo-suite',[sys.executable,'tools/ia.py','--project','fixture','qa','--suite','seo'])
qa_summary=json.loads(qa['stdout']);qa_path=Path(qa_summary['report'])
shutil.copy2(qa_path,OUT/'candidate-seo-qa-report.json')
assert qa_summary['outcome']=='passed',qa_summary
files=sorted({*v3['candidate_hashes'],values})
expected={n:sha(work/n) for n in files}
lines=[];delta=[]
for name in files:
 old=(ROOT/name).read_text() if (ROOT/name).exists() else '';new=(work/name).read_text()
 lines.extend(difflib.unified_diff(old.splitlines(keepends=True),new.splitlines(keepends=True),fromfile='a/'+name if old else '/dev/null',tofile='b/'+name))
# Diff of only the human-observation correction, against a verified v3 tree.
v3tree=Path(tempfile.mkdtemp(prefix='seo-v4-final-v3-reference-',dir=ROOT/'.local'))
for name in ('tools','tests'):shutil.copytree(ROOT/name,v3tree/name,ignore=shutil.ignore_patterns('__pycache__'))
assert run('v3-reference-apply',['patch','--batch','--forward','-p1','-i',str(patch3)],cwd=v3tree)['exit_code']==0
for name in files:
 old=(v3tree/name).read_text() if (v3tree/name).exists() else '';new=(work/name).read_text()
 delta.extend(difflib.unified_diff(old.splitlines(keepends=True),new.splitlines(keepends=True),fromfile='a/'+name if old else '/dev/null',tofile='b/'+name))
final=ROOT/'reports/seo/v4-review-corrections-final.patch';final.write_text(''.join(lines))
(OUT/'v3-to-final.diff').write_text(''.join(delta))
# The final artifact is not a stack: check and apply it directly to a fresh base.
fresh=Path(tempfile.mkdtemp(prefix='seo-v4-final-artifact-',dir=ROOT/'.local'))
for name in ('tools','tests'):shutil.copytree(ROOT/name,fresh/name,ignore=shutil.ignore_patterns('__pycache__'))
assert run('final-artifact-dry-run',['patch','--batch','--forward','--dry-run','-p1','-i',str(final)],cwd=fresh)['exit_code']==0
assert run('final-artifact-apply-isolated',['patch','--batch','--forward','-p1','-i',str(final)],cwd=fresh)['exit_code']==0
assert all(sha(fresh/n)==v for n,v in expected.items())
assert all(sha(ROOT/n)==v for n,v in original_base.items())
assert all(c['exit_code']==0 for c in (specific,unit,integration,tls,qa))
report={'kind':'seo-v4-final-isolated-validation','patch':str(final.relative_to(ROOT)),'patch_bytes':final.stat().st_size,'patch_sha256':sha(final),'v3_reference_sha256':sha(patch3),'base_hashes':original_base,'new_files_expected_absent':[n for n in files if not (ROOT/n).exists()],'candidate_hashes':expected,'identity_v3_verified':True,'single_patch_applies_to_fresh_base':True,'artifact_matches_tested_tree':True,'parser_defect_reproduced_before':before['exit_code']!=0,'specific_exit':specific['exit_code'],'unit_exit':unit['exit_code'],'integration_exit':integration['exit_code'],'local_tls_exit':tls['exit_code'],'seo_suite_outcome':qa_summary['outcome'],'workspace_declared_source_unchanged':True,'original_v3_unchanged':sha(patch3)==v3['patch_sha256'],'patch_applied_to_workspace':False,'theme_modified':False,'production_modified':False,'storefront_network_requests':0,'external_crawl_authorized':False,'review':'explicit human approval pending; no independent approval claimed','reproducibility':{'runner':str(Path(__file__).relative_to(ROOT)),'runner_sha256':sha(Path(__file__)),'inputs':{str(p.relative_to(ROOT)):sha(p) for p in (OUT/'value_cases.py',OUT/'parser_candidate.py.txt')},'candidate_directory':str(work.relative_to(ROOT))}}
(OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
