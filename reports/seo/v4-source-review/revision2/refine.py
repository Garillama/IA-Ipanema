from pathlib import Path
import difflib,hashlib,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent;P=OUT.parent
old=json.loads((P/'revision1/validation.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(ROOT/'reports/seo/v4-robots-sources-review1.patch')==old['patch_sha256']
assert all(sha(ROOT/n)==h for n,h in old['base_hashes'].items())
oldtree=ROOT/old['candidate_directory'];assert all(sha(oldtree/n)==h for n,h in old['candidate_hashes'].items())
work=Path(tempfile.mkdtemp(prefix='seo-v4-source-revised-',dir=ROOT/'.local'))
for area in ('tools','tests'):shutil.copytree(oldtree/area,work/area,ignore=shutil.ignore_patterns('__pycache__'))
env={k:v for k,v in os.environ.items() if not k.startswith('IPANEMA_')};env.update(IPANEMA_ALLOW_NETWORK='0',PYTHONDONTWRITEBYTECODE='1')
def run(label,args,cwd=work,runenv=None):
 c=subprocess.run(args,cwd=cwd,env=runenv or env,capture_output=True,text=True,timeout=180)
 d={'exit_code':c.returncode,'stdout':c.stdout,'stderr':c.stderr};(OUT/(label+'.json')).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return d
new='tests/unit/test_seo_robots_sources_v4.py';p=work/new
with p.open('a') as f:f.write('''
    def test_peer_C1_malformed_other_agent_scope_unknown(self):
        self.assertEqual(self.state(headers='otherbot: foo="x, googlebot: noindex'),'insufficient_evidence')
    def test_peer_C2_ambiguous_namespace_unknown(self):
        for header in ('max_snippet: -1, noindex','max-snipet: 10, noindex'):
            with self.subTest(header=header):self.assertEqual(self.state(headers=header),'insufficient_evidence')
    def test_peer_C3_quoted_comma_restriction_is_unknown_not_flag(self):
        for value in ('foo="x, noindex, y"','foo="x, noindex"'):
            with self.subTest(value=value):
                self.assertEqual(self.state({'robots':[value]}),'insufficient_evidence')
                self.assertEqual(self.state({'googlebot':[value]}),'insufficient_evidence')
                e=robots.google_directive_evidence({},'googlebot: '+value)
                self.assertFalse(e['noindex']);self.assertEqual(e['state'],'insufficient_evidence')
    def test_peer_action_separator_regressions(self):
        from ipanema.seo.crawl_policy import Policy
        for path in ('/add%20to%20cart','/add+to+cart','/add~to~cart','/agregar%20al%20carrito'):
            with self.subTest(path=path),self.assertRaises(ValueError):Policy(HOME).check(path)
    def test_legacy_gate_marks_unknown_explicitly(self):
        with tempfile.TemporaryDirectory() as folder:
            project=Project(make_project(Path(folder),theme=False))
            report=audit_snapshot(project,self.snapshot({'robots':['index']}),'home')
            report.pop('robots_evidence');report['robots_directives']='noindex'
            gate=compare(project,report,report)
            check=next(c for c in gate['checks'] if c['name'].endswith(':noindex'))
            self.assertEqual(check['status'],'unknown')
''')
boot='import socket,unittest,sys;socket.socket.connect=lambda *a,**k: (_ for _ in ()).throw(AssertionError("network_forbidden_in_fixture"));r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(sys.argv[1:]));sys.exit(not r.wasSuccessful())'
before=run('before-peer-cases',[sys.executable,'-c',boot,'tests.unit.test_seo_robots_sources_v4']);assert before['exit_code']!=0
p=work/'tools/ipanema/seo/robots.py';s=p.read_text()
needle='def google_directive_evidence(meta, header):'
helper='''def _ambiguity_errors(value, parsed, *, header_field):
    # A diagnostic alternative, never a source of valid flags. Keep the original
    # physical field boundary even when comparing comma/quote interpretations.
    errors = []
    if header_field:
        for error in _parse_directive_source(value)['errors']:
            if error['reason'] in ('unclosed_quote', 'incomplete_escape'):
                errors.append({**error, 'reason': 'ambiguous_header_scope'})
    if ',' in value and not parsed['noindex']:
        for part in value.split(','):
            alternative = part.strip().strip('"' + "'")
            if header_field:
                alternative, _, _ = _google_header_source(alternative)
            if _parse_directive_source(alternative)['noindex']:
                errors.append({'reason': 'ambiguous_comma_interpretation'})
                break
    return errors


'''
assert needle in s;s=s.replace(needle,helper+needle)
s=s.replace("parsed['errors'] += selection_errors", "parsed['errors'] += selection_errors\n        parsed['errors'] += _ambiguity_errors(value, parsed, header_field=header_field)")
p.write_text(s)
p=work/'tools/ipanema/seo/crawl_policy.py';s=p.read_text();oldpat="(?:add[-_.]?to[-_.]?cart|agregar[-_.]?al[-_.]?carrito)|/comprar";newpat="(?:add[^a-z0-9]?to[^a-z0-9]?cart|agregar[^a-z0-9]?al[^a-z0-9]?carrito)|/comprar";assert oldpat in s;p.write_text(s.replace(oldpat,newpat))
p=work/'tools/ipanema/seo/regression.py';s=p.read_text();needle="check(url + ':noindex', not (before_state != 'noindex' and after_state == 'noindex'), after_state)";replacement="check(url + ':noindex', not (before_state != 'noindex' and after_state == 'noindex'), after_state,\n              unknown=before_state in (None, 'insufficient_evidence') or after_state in (None, 'insufficient_evidence'))";assert needle in s;p.write_text(s.replace(needle,replacement))
# Strengthen former permissive expectations after the documented ambiguity policy change.
p=work/new;s=p.read_text();s=s.replace('test_unrelated_agent_malformed_field_not_relevant','test_unrelated_agent_malformed_scope_unknown');s=s.replace("self.assertEqual(self.state(headers='otherbot: foo=\"x'),'indexable_candidate')", "self.assertEqual(self.state(headers='otherbot: foo=\"x'),'insufficient_evidence')");p.write_text(s)
p=work/'tests/unit/test_seo_robots_values_v4.py';s=p.read_text();s=s.replace("self.state(header='otherbot: foo=\"x, googlebot: none\", noindex'),'indexable_candidate'", "self.state(header='otherbot: foo=\"x, googlebot: none\", noindex'),'insufficient_evidence'");p.write_text(s)
specific=run('after-peer-specific',[sys.executable,'-c',boot,'tests.unit.test_seo_robots_sources_v4','tests.unit.test_seo_robots_values_v4','tests.unit.test_seo_review_additional_v4','tests.unit.test_seo_transport_v4'])
unit=run('after-peer-seo-unit',[sys.executable,'-m','unittest','discover','-s','tests/unit','-p','test_seo*.py','-q'])
integration=run('after-peer-seo-integration',[sys.executable,'-m','unittest','discover','-s','tests/integration','-p','test_seo*.py','-q'])
tls=run('after-peer-local-tls',[sys.executable,str(ROOT/'reports/seo/v4-patch-review/tls_fixture.py')],runenv={**env,'PYTHONPATH':str(work/'tools')})
setup='from pathlib import Path;from tests.support import make_project;make_project(Path.cwd(),identifier="fixture",theme=False)';assert run('setup',[sys.executable,'-c',setup])['exit_code']==0
qa=run('after-peer-seo-suite',[sys.executable,'tools/ia.py','--project','fixture','qa','--suite','seo']);qa_data=json.loads(qa['stdout']);shutil.copy2(qa_data['report'],OUT/'candidate-qa-report.json')
# Candidate-wide unit/integration regression; source QA receipts remain separately visible.
# General KnowledgeTests need the existing offline reference indexes. Copy only
# the six JSON indexes, never themes, local configs, accounts or new discovery.
registry=json.loads((work/'projects/registry.json').read_text())
registry['projects']['ipanema']='projects/ipanema.json'
(work/'projects/registry.json').write_text(json.dumps(registry))
(work/'projects/ipanema.json').write_text(json.dumps({'schema_version':2,'id':'ipanema','name':'offline knowledge fixture','theme_root':None,'public_url':'https://example.invalid','discovery_root':'ipanema-discovery','knowledge_reference_project':'ipanema','evidence_dir':'reports/runs/ipanema','qa':{'pages':{'home':'/'}}}))
for relative in ('13-evidence/measurements/source-baseline/source-summary.json','13-evidence/measurements/source-baseline/components.json','13-evidence/measurements/source-baseline/dependency-graph.json','13-evidence/measurements/source-baseline/settings.json','13-evidence/measurements/source-baseline/source-inventory.json','11-opportunities/findings.json'):
    target=work/'ipanema-discovery'/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/'ipanema-discovery'/relative,target)
general=run('general-unit',[sys.executable,'-m','unittest','discover','-s','tests/unit','-q'])
assert all(d['exit_code']==0 for d in (specific,unit,integration,tls,qa,general)), 'Unresolved failure, do not export success'
files=sorted(old['candidate_hashes']);expected={n:sha(work/n) for n in files};diff=[]
for name in files:
 previous=(ROOT/name).read_text() if (ROOT/name).exists() else '';current=(work/name).read_text()
 diff.extend(difflib.unified_diff(previous.splitlines(keepends=True),current.splitlines(keepends=True),fromfile='a/'+name if previous else '/dev/null',tofile='b/'+name))
final=ROOT/'reports/seo/v4-robots-sources-final.patch';final.write_text(''.join(diff))
fresh=Path(tempfile.mkdtemp(prefix='seo-v4-source-revised-artifact-',dir=ROOT/'.local'))
for name in old['base_hashes']:
 f=fresh/name;f.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/name,f)
assert run('artifact-dry-run',['patch','--batch','--forward','--fuzz=0','--dry-run','-p1','-i',str(final)],cwd=fresh)['exit_code']==0
assert run('artifact-apply-isolated',['patch','--batch','--forward','--fuzz=0','-p1','-i',str(final)],cwd=fresh)['exit_code']==0
assert all(sha(fresh/n)==h for n,h in expected.items());assert all(sha(ROOT/n)==h for n,h in old['base_hashes'].items())
result={**old,'patch_sha256':sha(final),'patch_bytes':final.stat().st_size,'candidate_hashes':expected,'specific_exit':specific['exit_code'],'unit_exit':unit['exit_code'],'integration_exit':integration['exit_code'],'tls_exit':tls['exit_code'],'qa_outcome':qa_data['outcome'],'general_unit_exit':general['exit_code'],'candidate_directory':str(work.relative_to(ROOT)),'all_checks_pass':True,'reviewed_predecessor_sha256':old['patch_sha256'],'peer_critical_cases_reproduced_before':True,'review':'new hash requires fresh independent review; previous changes requested are not approval'}
(OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
