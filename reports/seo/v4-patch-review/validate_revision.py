"""Verifica el artefacto v2 exacto sobre una copia nueva con hashes comprobados."""
from pathlib import Path
import hashlib,json,os,re,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
r=json.loads((OUT/'revision-validation.json').read_text());patch=ROOT/r['patch']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(patch)==r['patch_sha256']
assert all(sha(ROOT/name)==value for name,value in r['base_source_hashes'].items())
allowed=set(r['candidate_source_hashes'])
for name in re.findall(r'^\+\+\+ b/(.+)$',patch.read_text(),re.M):assert name in allowed and '..' not in Path(name).parts
work=Path(tempfile.mkdtemp(prefix='seo-v4-v2-fresh-',dir=ROOT/'.local'))
for name in ('tools','tests'):shutil.copytree(ROOT/name,work/name,ignore=shutil.ignore_patterns('__pycache__'))
env={k:v for k,v in os.environ.items() if not k.startswith('IPANEMA_')};env['IPANEMA_ALLOW_NETWORK']='0'
def run(label,args,runenv=None):
 p=subprocess.run(args,cwd=work,env=runenv or env,capture_output=True,text=True,timeout=90)
 d={'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};(OUT/(label+'.json')).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return d
assert run('v2-fresh-dry-run',['patch','--batch','--forward','--dry-run','-p1','-i',str(patch)])['exit_code']==0
assert run('v2-fresh-apply',['patch','--batch','--forward','-p1','-i',str(patch)])['exit_code']==0
assert all(sha(work/name)==value for name,value in r['candidate_source_hashes'].items())
boot='import socket,unittest,sys;socket.socket.connect=lambda *a,**k: (_ for _ in ()).throw(AssertionError("network_forbidden_in_fixture"));r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName("tests.unit.test_seo_review_additional_v4"));sys.exit(not r.wasSuccessful())'
extended=run('v2-fresh-extended',[sys.executable,'-c',boot])
unit=run('v2-fresh-seo-unit',[sys.executable,'-m','unittest','discover','-s','tests/unit','-p','test_seo*.py','-q'])
integration=run('v2-fresh-seo-integration',[sys.executable,'-m','unittest','discover','-s','tests/integration','-p','test_seo*.py','-q'])
# Existing transport, real TLS locally; fixture routing is explicit, only loopback sockets.
tlsenv={**env,'PYTHONPATH':str(work/'tools')}
tls=run('v2-fresh-local-tls',[sys.executable,str(OUT/'tls_fixture.py')],tlsenv)
r.update({'fresh_artifact_verified':True,'fresh_source_hashes_match':True,'fresh_extended_exit':extended['exit_code'],'fresh_seo_unit_exit':unit['exit_code'],'fresh_seo_integration_exit':integration['exit_code'],'fresh_local_tls_exit':tls['exit_code'],'workspace_source_unchanged':all(sha(ROOT/name)==value for name,value in r['base_source_hashes'].items()),'fixture_network':'TLS test uses only 127.0.0.1 with test socket routing; extended fixtures forbid sockets','patch_applied_to_workspace':False})
(OUT/'revision-validation.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(r,ensure_ascii=False,indent=2))
