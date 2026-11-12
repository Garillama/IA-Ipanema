"""Resuelve en aislamiento la objeción nueva de Claude; no aplica al workspace."""
from pathlib import Path
import difflib,hashlib,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
v2=json.loads((OUT/'revision-validation.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert all(sha(ROOT/n)==v for n,v in v2['base_source_hashes'].items())
assert sha(ROOT/v2['patch'])==v2['patch_sha256']
work=Path(tempfile.mkdtemp(prefix='seo-v4-v3-',dir=ROOT/'.local'))
for name in ('tools','tests'):shutil.copytree(ROOT/name,work/name,ignore=shutil.ignore_patterns('__pycache__'))
env={k:v for k,v in os.environ.items() if not k.startswith('IPANEMA_')};env['IPANEMA_ALLOW_NETWORK']='0'
def run(label,args,cwd=work,runenv=None):
 p=subprocess.run(args,cwd=cwd,env=runenv or env,capture_output=True,text=True,timeout=90)
 d={'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};(OUT/(label+'.json')).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return d
assert run('v3-base-v2-apply',['patch','--batch','--forward','-p1','-i',str(ROOT/v2['patch'])])['exit_code']==0
name='tests/unit/test_seo_review_additional_v4.py';(work/name).write_text((OUT/'cases.py').read_text())
boot='import socket,unittest,sys;socket.socket.connect=lambda *a,**k: (_ for _ in ()).throw(AssertionError("network_forbidden_in_fixture"));r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName("tests.unit.test_seo_review_additional_v4"));sys.exit(not r.wasSuccessful())'
before=run('before-v3-on-v2-extended',[sys.executable,'-c',boot])
policy='tools/ipanema/seo/crawl_policy.py';p=work/policy
old="ACTIONS = re.compile(r'/(?:add[-_.]to[-_.]cart|agregar[-_.]al[-_.]carrito|comprar)(?:/|$|[.;])', re.I)"
new="ACTIONS = re.compile(r'/(?:add[-_.]?to[-_.]?cart|agregar[-_.]?al[-_.]?carrito|comprar)', re.I)"
s=p.read_text();assert old in s;p.write_text(s.replace(old,new))
# Conservative private prefixes: punctuation/digits block, longer alphabetic public words remain allowed.
s=p.read_text();assert "suscripciones)(?:/|$|[.;])" in s;p.write_text(s.replace("suscripciones)(?:/|$|[.;])","suscripciones)(?![a-z])"))
crawler=work/'tools/ipanema/seo/crawler.py';s=crawler.read_text()
s=s.replace("{s['source'] for s in result['sitemaps'] if s.get('kind') and not s.get('errors')}","{s.get('source') for s in result['sitemaps'] if s.get('source') and s.get('kind') and not s.get('errors')}")
# Reject missing Location explicitly in robots, sitemap and HTML redirect branches.
import re
pattern=r"(?m)^([ ]*)if response\['status'\] in \(301, 302, 303, 307, 308\):$"
s,count=re.subn(pattern,lambda m:m[0]+"\n"+m[1]+"    if not response['headers'].get('location'):\n"+m[1]+"        raise IpanemaError('Redirección sin Location.')",s)
assert count==3,count
s=s.replace(" and\n                    set(result['sitemap_urls']).issubset({n['url'] for n in result['urls']})","")
crawler.write_text(s)
robots=work/'tools/ipanema/seo/robots.py';s=robots.read_text();needle="                if value:\n                    agents.append(value.lower())"
replacement="                if value:\n                    if not re.fullmatch(r'[A-Za-z_-]+|\\*', value):\n                        self.errors.append({'line': number + 1, 'reason': 'invalid_product_token'})\n                        continue\n                    agents.append(value.lower())"
assert needle in s;s=s.replace(needle,replacement);robots.write_text(s)
extended=run('after-v3-extended',[sys.executable,'-c',boot])
unit=run('after-v3-seo-unit',[sys.executable,'-m','unittest','discover','-s','tests/unit','-p','test_seo*.py','-q'])
integration=run('after-v3-seo-integration',[sys.executable,'-m','unittest','discover','-s','tests/integration','-p','test_seo*.py','-q'])
tls=run('after-v3-local-tls',[sys.executable,str(OUT/'tls_fixture.py')],runenv={**env,'PYTHONPATH':str(work/'tools')})
files=sorted(v2['candidate_source_hashes']);lines=[];delta=[]
# Read the exact v2 artifact via a fresh, separate copy to calculate a clean delta.
v2tree=Path(tempfile.mkdtemp(prefix='seo-v4-v2-reference-',dir=ROOT/'.local'))
for folder in ('tools','tests'):shutil.copytree(ROOT/folder,v2tree/folder,ignore=shutil.ignore_patterns('__pycache__'))
assert run('v3-v2-reference-apply',['patch','--batch','--forward','-p1','-i',str(ROOT/v2['patch'])],cwd=v2tree)['exit_code']==0
for name in files:
 old=(ROOT/name).read_text() if (ROOT/name).exists() else '';s=(work/name).read_text()
 lines.extend(difflib.unified_diff(old.splitlines(keepends=True),s.splitlines(keepends=True),fromfile='a/'+name if old else '/dev/null',tofile='b/'+name))
 old2=(v2tree/name).read_text();delta.extend(difflib.unified_diff(old2.splitlines(keepends=True),s.splitlines(keepends=True),fromfile='a/'+name,tofile='b/'+name))
proposal=ROOT/'reports/seo/v4-review-corrections-v3.patch';proposal.write_text(''.join(lines))
(ROOT/'reports/seo/v4-review-v2-to-v3.patch').write_text(''.join(delta))
# Fresh artifact application and equality to the tested tree; no mutation to ROOT source.
fresh=Path(tempfile.mkdtemp(prefix='seo-v4-v3-fresh-',dir=ROOT/'.local'))
for folder in ('tools','tests'):shutil.copytree(ROOT/folder,fresh/folder,ignore=shutil.ignore_patterns('__pycache__'))
assert run('v3-fresh-dry-run',['patch','--batch','--forward','--dry-run','-p1','-i',str(proposal)],cwd=fresh)['exit_code']==0
assert run('v3-fresh-apply',['patch','--batch','--forward','-p1','-i',str(proposal)],cwd=fresh)['exit_code']==0
assert all(sha(fresh/name)==sha(work/name) for name in files)
result={'kind':'seo-v4-v3-isolated-review-candidate','patch':str(proposal.relative_to(ROOT)),'patch_sha256':sha(proposal),'parent_patch_sha256':v2['patch_sha256'],'source_hashes':v2['base_source_hashes'],'candidate_hashes':{name:sha(work/name) for name in files},'new_claude_objection_reproduced_on_v2':before['exit_code']!=0,'extended_exit':extended['exit_code'],'seo_unit_exit':unit['exit_code'],'seo_integration_exit':integration['exit_code'],'local_tls_exit':tls['exit_code'],'fresh_patch_applies_and_matches_tested_tree':True,'workspace_source_unchanged':all(sha(ROOT/n)==v for n,v in v2['base_source_hashes'].items()),'patch_applied_to_workspace':False,'theme_modified':False,'production_modified':False,'external_crawl_authorized':False,'storefront_network_requests':0,'independent_review':'v2: Claude changes_requested, Codex unavailable/inactivity; v3 delta pending review','human_approval':'pending'}
(OUT/'v3-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
