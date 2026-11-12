"""Reproduce el parche exacto en copia temporal; nunca modifica tools/ ni el tema."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile,re
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
PATCH=ROOT/'reports/seo/v4-review-corrections.patch'
TOOLS=ROOT/'tools'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected=json.loads((ROOT/'reports/seo/v4-review-corrections-qa.json').read_text())['source_hashes']
assert all(sha(ROOT/p)==value for p,value in expected.items()), 'La base cambió: exige revalidación.'
allowed={*expected,'tests/unit/test_seo_review_findings_v4.py'}
for name in re.findall(r'^\+\+\+ b/(.+)$',PATCH.read_text(),re.M):assert name in allowed and '..' not in Path(name).parts
original_hashes={str(p.relative_to(ROOT)):sha(p) for base in ('tools','tests') for p in (ROOT/base).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
work=Path(tempfile.mkdtemp(prefix='seo-v4-exact-patch-',dir=ROOT/'.local'))
for name in ('tools','tests'):shutil.copytree(ROOT/name,work/name,ignore=shutil.ignore_patterns('__pycache__'))
shutil.copy2(OUT/'cases.py',work/'tests/unit/test_v4_patch_extended.py')
env={k:v for k,v in os.environ.items() if not k.startswith('IPANEMA_')};env['IPANEMA_ALLOW_NETWORK']='0'
def run(label,args):
 p=subprocess.run(args,cwd=work,env=env,capture_output=True,text=True,timeout=90)
 data={'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};(OUT/(label+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');return data
# Guard forbids actual sockets even if a fixture accidentally reaches the transport.
boot='import socket,unittest,sys;socket.socket.connect=lambda *a,**k: (_ for _ in ()).throw(AssertionError("network_forbidden_in_fixture"));r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName("tests.unit.test_v4_patch_extended"));sys.exit(not r.wasSuccessful())'
before=run('before-extended',[sys.executable,'-c',boot])
check=run('patch-dry-run',['patch','--batch','--forward','--dry-run','-p1','-i',str(PATCH)]);assert check['exit_code']==0
applied=run('patch-apply-isolated',['patch','--batch','--forward','-p1','-i',str(PATCH)]);assert applied['exit_code']==0
after=run('after-exact-patch-extended',[sys.executable,'-c',boot])
unit=run('after-exact-patch-seo-unit',[sys.executable,'-m','unittest','discover','-s','tests/unit','-p','test_seo*.py','-q'])
integration=run('after-exact-patch-seo-integration',[sys.executable,'-m','unittest','discover','-s','tests/integration','-p','test_seo*.py','-q'])
unchanged=all((ROOT/name).exists() and sha(ROOT/name)==value for name,value in original_hashes.items())
result={'kind':'seo-v4-exact-patch-review','patch_sha256':sha(PATCH),'source_hashes':expected,'workspace_source_unchanged':unchanged,'theme_modified':False,'storefront_network_requests':0,'patch_applied_to_workspace':False,'before_exit':before['exit_code'],'after_exact_patch_exit':after['exit_code'],'seo_unit_exit':unit['exit_code'],'seo_integration_exit':integration['exit_code'],'isolated_directory':str(work.relative_to(ROOT)),'before_failures':re.findall(r'^(?:FAIL|ERROR): (\S+)',before['stderr'],re.M),'remaining_failures':re.findall(r'^(?:FAIL|ERROR): (\S+)',after['stderr'],re.M),'policy':'No change to AGENTS, no inferred approval, no external crawl'}
(OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
