"""Reproduce source-boundary bug, build/test isolated candidate and emit one base diff."""
from pathlib import Path
import difflib,hashlib,json,os,re,shutil,subprocess,sys,tarfile,io,tempfile
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=json.loads((ROOT/'reports/seo/v4-final-review/manifest.json').read_text());oldpatch=ROOT/old['patch']
assert sha(oldpatch)==old['patch_sha256'];assert all(sha(ROOT/n)==h for n,h in old['base_hashes'].items())
base={**old['base_hashes'],'tools/ipanema/seo/regression.py':sha(ROOT/'tools/ipanema/seo/regression.py')}
work=Path(tempfile.mkdtemp(prefix='seo-v4-source-candidate-',dir=ROOT/'.local'))
for name in ('tools','tests'):shutil.copytree(ROOT/name,work/name,ignore=shutil.ignore_patterns('__pycache__'))
env={k:v for k,v in os.environ.items() if not k.startswith('IPANEMA_')};env['IPANEMA_ALLOW_NETWORK']='0';env['PYTHONDONTWRITEBYTECODE']='1'
def run(label,args,cwd=work,runenv=None):
 p=subprocess.run(args,cwd=cwd,env=runenv or env,capture_output=True,text=True,timeout=180)
 d={'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};(OUT/(label+'.json')).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return d
assert run('blocked-reference-apply-isolated',['patch','--batch','--forward','--fuzz=0','-p1','-i',str(oldpatch)])['exit_code']==0
assert all(sha(work/n)==h for n,h in old['candidate_hashes'].items())
newtest='tests/unit/test_seo_robots_sources_v4.py';shutil.copy2(OUT/'source_cases.py',work/newtest)
boot='import socket,unittest,sys;socket.socket.connect=lambda *a,**k: (_ for _ in ()).throw(AssertionError("network_forbidden_in_fixture"));r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(sys.argv[1:]));sys.exit(not r.wasSuccessful())'
before=run('before-source-boundaries',[sys.executable,'-c',boot,'tests.unit.test_seo_robots_sources_v4'])
assert before['exit_code']!=0
for name in ('test_original_meta_quote_cannot_mask_header_noindex','test_original_repeated_header_quote_cannot_mask_next'):
 assert 'FAIL: '+name in before['stderr'],name
robots=work/'tools/ipanema/seo/robots.py';s=robots.read_text();s=s[:s.index('\ndef google_directives(')].rstrip()+'\n\n\n'+(OUT/'directives_candidate.py.txt').read_text();robots.write_text(s)
def change(name,old,new):
 p=work/name;s=p.read_text();assert old in s,(name,old);p.write_text(s.replace(old,new))
idx='tools/ipanema/seo/indexability.py'
change(idx,'from .robots import google_directives, has_noindex','from .robots import google_directive_evidence')
change(idx,"    reasons = []\n", "    reasons = []\n    robots_evidence = None\n")
change(idx,"directives = google_directives(meta, snapshot.get('headers', {}).get('x-robots-tag', ''))\n        if has_noindex(directives):\n            state = 'noindex'", "robots_evidence = google_directive_evidence(meta, snapshot.get('headers', {}).get('x-robots-tag', ''))\n        if robots_evidence['noindex']:\n            state = 'noindex'\n        elif robots_evidence['relevant_errors']:\n            state = 'insufficient_evidence'\n            reasons.append('malformed_robots_directives')")
change(idx,"return {'state': state, 'reasons': reasons, 'indexation_observed': False,", "return {'state': state, 'reasons': reasons, 'robots_evidence': robots_evidence, 'indexation_observed': False,")
audit='tools/ipanema/seo/page_audit.py'
change(audit,'from .robots import Robots, google_directives, has_noindex','from .robots import Robots, google_directive_evidence')
change(audit,"robots=google_directives(metadata,snap.get('headers',{}).get('x-robots-tag',''))\n    noindex=has_noindex(robots)", "robots_evidence=google_directive_evidence(metadata,snap.get('headers',{}).get('x-robots-tag',''))\n    robots=','.join(robots_evidence['flags'])\n    noindex=robots_evidence['noindex']\n    if robots_evidence['relevant_errors']:\n        findings.append(F('SEO023','D','warning','Directivas robots malformadas: conservar fuentes y evidencia insuficiente sin ignorar restricciones válidas.',evidence=robots_evidence['relevant_errors']))")
change(audit,"else 'noindex_observed' if noindex else 'no_observable_noindex_not_index_proof'", "else 'noindex_observed' if noindex else 'insufficient_evidence' if robots_evidence['relevant_errors'] else 'no_observable_noindex_not_index_proof'")
change(audit,"'robots_directives':robots,'schema_matrix'", "'robots_directives':robots,'robots_evidence':robots_evidence,'schema_matrix'")
reg='tools/ipanema/seo/regression.py'
change(reg,"'noindex' if 'noindex' in report.get('robots_directives', '') else 'insufficient_evidence'", "'noindex' if report.get('robots_evidence', {}).get('noindex') else 'insufficient_evidence'")
# Close the previously reproduced commercial-action regression without weakening route filters.
policy='tools/ipanema/seo/crawl_policy.py'
change(policy,"ACTIONS = re.compile(r'/(?:add[-_.]?to[-_.]?cart|agregar[-_.]?al[-_.]?carrito|comprar)', re.I)","ACTIONS = re.compile(r'(?:add[-_.]?to[-_.]?cart|agregar[-_.]?al[-_.]?carrito)|/comprar', re.I)")
# Reuse prior contracts and append only the known embedded-action counterexamples.
tests=work/newtest
with tests.open('a') as f:f.write('''\n    def test_prior_embedded_action_objection_closed(self):
        from ipanema.seo.crawl_policy import Policy
        policy=Policy(HOME)
        for path in ('/producto-add-to-cart','/prefix_add_to_cart123','/%2570roducto-add-to-cart'):
            with self.subTest(path=path),self.assertRaises(ValueError):policy.check(path)
        self.assertEqual(policy.check('/blog/posts/como-comprar-x'),HOME+'blog/posts/como-comprar-x')
''')
specific=run('after-source-specific',[sys.executable,'-c',boot,'tests.unit.test_seo_robots_sources_v4','tests.unit.test_seo_robots_values_v4','tests.unit.test_seo_review_additional_v4','tests.unit.test_seo_transport_v4'])
unit=run('after-source-seo-unit',[sys.executable,'-m','unittest','discover','-s','tests/unit','-p','test_seo*.py','-q'])
integration=run('after-source-seo-integration',[sys.executable,'-m','unittest','discover','-s','tests/integration','-p','test_seo*.py','-q'])
tls=run('after-source-local-tls',[sys.executable,str(ROOT/'reports/seo/v4-patch-review/tls_fixture.py')],runenv={**env,'PYTHONPATH':str(work/'tools')})
setup='from pathlib import Path;from tests.support import make_project;make_project(Path.cwd(),identifier="fixture",theme=False)'
assert run('setup-fixture',[sys.executable,'-c',setup])['exit_code']==0
qa=run('after-source-seo-suite',[sys.executable,'tools/ia.py','--project','fixture','qa','--suite','seo'])
qa_data=json.loads(qa['stdout']);shutil.copy2(qa_data['report'],OUT/'candidate-qa-report.json')
files=sorted(set(old['candidate_hashes'])|{reg,newtest})
expected={n:sha(work/n) for n in files};patch=[]
for n in files:
 previous=(ROOT/n).read_text() if (ROOT/n).exists() else '';current=(work/n).read_text()
 patch.extend(difflib.unified_diff(previous.splitlines(keepends=True),current.splitlines(keepends=True),fromfile='a/'+n if previous else '/dev/null',tofile='b/'+n))
final=ROOT/'reports/seo/v4-robots-sources-final.patch';final.write_text(''.join(patch))
fresh=Path(tempfile.mkdtemp(prefix='seo-v4-source-artifact-',dir=ROOT/'.local'))
for n,h in base.items():
 q=fresh/n;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/n,q)
assert run('source-artifact-dry-run',['patch','--batch','--forward','--fuzz=0','--dry-run','-p1','-i',str(final)],cwd=fresh)['exit_code']==0
assert run('source-artifact-apply-isolated',['patch','--batch','--forward','--fuzz=0','-p1','-i',str(final)],cwd=fresh)['exit_code']==0
assert all(sha(fresh/n)==h for n,h in expected.items());assert all(sha(ROOT/n)==h for n,h in base.items())
result={'kind':'seo-v4-robots-source-boundary-candidate','patch':str(final.relative_to(ROOT)),'patch_sha256':sha(final),'patch_bytes':final.stat().st_size,'blocked_reference_sha256':old['patch_sha256'],'base_hashes':base,'candidate_hashes':expected,'new_files_expected_absent':[n for n in files if not (ROOT/n).exists()],'original_two_failures_reproduced_before':True,'specific_exit':specific['exit_code'],'unit_exit':unit['exit_code'],'integration_exit':integration['exit_code'],'tls_exit':tls['exit_code'],'qa_outcome':qa_data['outcome'],'all_checks_pass':all(x['exit_code']==0 for x in (specific,unit,integration,tls,qa)),'direct_single_patch_from_base':True,'artifact_matches_tested_tree':True,'workspace_base_unchanged':True,'applied_to_workspace':False,'theme_modified':False,'production_modified':False,'external_crawl_executed':False,'review':'new independent review pending; no previous approval reused','candidate_directory':str(work.relative_to(ROOT)),'sources':['https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag','https://developers.google.com/search/docs/crawling-indexing/block-indexing']}
assert result['all_checks_pass'], 'Do not publish a successful candidate with failing QA'
(OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
