from pathlib import Path
import difflib,hashlib,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent;P=OUT.parent
old=json.loads((P/'revision2/validation.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(ROOT/'reports/seo/v4-robots-sources-review2.patch')==old['patch_sha256'];assert all(sha(ROOT/n)==h for n,h in old['base_hashes'].items())
oldtree=ROOT/old['candidate_directory'];assert all(sha(oldtree/n)==h for n,h in old['candidate_hashes'].items())
work=Path(tempfile.mkdtemp(prefix='seo-v4-source-final3-',dir=ROOT/'.local'))
for area in ('tools','tests','projects','ipanema-discovery'):shutil.copytree(oldtree/area,work/area,ignore=shutil.ignore_patterns('__pycache__'))
env={k:v for k,v in os.environ.items() if not k.startswith('IPANEMA_')};env.update(IPANEMA_ALLOW_NETWORK='0',PYTHONDONTWRITEBYTECODE='1')
def run(label,args,cwd=work,runenv=None):
 c=subprocess.run(args,cwd=cwd,env=runenv or env,capture_output=True,text=True,timeout=180);d={'exit_code':c.returncode,'stdout':c.stdout,'stderr':c.stderr};(OUT/(label+'.json')).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return d
name='tests/unit/test_seo_robots_sources_v4.py'
with (work/name).open('a') as f:f.write('''
    def test_peer_valid_other_agent_list_is_not_uncertain(self):
        self.assertEqual(self.state(headers='otherbot: nofollow, noindex'),'indexable_candidate')
        self.assertEqual(self.state(headers='otherbot: noindex, nofollow'),'indexable_candidate')
    def test_peer_quoted_separator_grammar_unknown(self):
        for value in ('foo="x; noindex"','foo="x noindex"'):
            with self.subTest(value=value):
                self.assertEqual(self.state({'robots':[value]}),'insufficient_evidence')
                self.assertFalse(robots.google_directive_evidence({'robots':[value]},'')['noindex'])
    def test_peer_gate_restrictive_after_cannot_be_only_unknown(self):
        with tempfile.TemporaryDirectory() as folder:
            project=Project(make_project(Path(folder),theme=False))
            before=audit_snapshot(project,self.snapshot({'robots':['index']}),'home')
            after=audit_snapshot(project,self.snapshot({'robots':['noindex']}),'home')
            check=next(c for c in compare(project,before,after)['checks'] if c['name'].endswith(':noindex'))
            self.assertEqual(check['status'],'failed')
    def test_unrelated_invalid_robots_agents_are_warned_not_global_abort(self):
        for value in ('MJ12bot','360Spider','Sogou web spider'):
            with self.subTest(value=value):
                r=robots.Robots();r.parse(['User-agent: '+value,'Disallow: /private','User-agent: *','Allow: /'])
                self.assertFalse(r.errors);self.assertTrue(r.warnings)
                self.assertTrue(r.can_fetch('Googlebot',HOME));self.assertTrue(r.can_fetch('IAIpanemaAudit/4.0',HOME))
        r=robots.Robots();r.parse(['User-agent: Googlebot/2.1','Disallow: /'])
        self.assertTrue(r.errors);self.assertFalse(r.can_fetch('Googlebot',HOME))
''')
boot='import socket,unittest,sys;socket.socket.connect=lambda *a,**k: (_ for _ in ()).throw(AssertionError("network_forbidden_in_fixture"));r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(sys.argv[1:]));sys.exit(not r.wasSuccessful())'
before=run('before-peer-cases',[sys.executable,'-c',boot,'tests.unit.test_seo_robots_sources_v4']);assert before['exit_code']!=0
p=work/'tools/ipanema/seo/robots.py';s=p.read_text()
needle="parameters.append({'name': key, 'has_value': finish > probe, 'known': key in _VALUE_RULES})"
replace="parameters.append({'name': key, 'has_value': finish > probe, 'known': key in _VALUE_RULES,\n                               'quoted_separators': any(q in text[probe:finish] for q in ('\\\"', \"'\")) and any(c.isspace() or c in ',;' for c in text[probe:finish])})"
assert needle in s;s=s.replace(needle,replace)
needle="    if ',' in value and not parsed['noindex']:\n"
replace='''    if any(not p['known'] and p.get('quoted_separators') for p in parsed['parameters']):
        errors.append({'reason': 'unsupported_quoted_separator_grammar'})
    # A syntactically recognized scoped rule list stays scoped across commas.
    # Do not turn a valid otherbot: nofollow, noindex list into global restrictions.
    scoped_list = False
    if header_field:
        prefix, colon, rest = value.partition(':')
        if colon and prefix.strip().lower() not in (_VALUE_RULES | _FLAG_RULES):
            _, scopes, _ = _google_header_source(value)
            first = _parse_directive_source(next(iter(_header_parts(rest)), ''))
            scoped_list = (prefix.strip().lower() in scopes and not first['errors'] and not first['unknown'] and
                           (bool(first['flags']) or bool(first['parameters']) and all(p['known'] for p in first['parameters'])))
    if ',' in value and not parsed['noindex'] and not scoped_list:
'''
assert needle in s;s=s.replace(needle,replace)
s=s.replace("self.groups, self.maps, self.errors = [], [], []", "self.groups, self.maps, self.errors, self.warnings = [], [], [], []")
needle="self.errors.append({'line': number + 1, 'reason': 'invalid_product_token'})"
replace="issue = {'line': number + 1, 'reason': 'invalid_product_token'}\n                        relevant = '*' in value or any(agent in value.lower() for agent in ('googlebot', 'iaipanemaaudit'))\n                        (self.errors if relevant else self.warnings).append(issue)"
assert needle in s;s=s.replace(needle,replace);p.write_text(s)
p=work/'tools/ipanema/seo/regression.py';s=p.read_text();needle="unknown=before_state in (None, 'insufficient_evidence') or after_state in (None, 'insufficient_evidence'))";replace="unknown=(before_state in (None, 'insufficient_evidence') or after_state in (None, 'insufficient_evidence'))\n              and not (after_state == 'noindex' and before_state != 'noindex'))";assert needle in s;p.write_text(s.replace(needle,replace))
p=work/'tools/ipanema/seo/crawler.py';s=p.read_text();needle="'crawler_agent': AGENT, 'googlebot_is_separate': True}";replace="'crawler_agent': AGENT, 'googlebot_is_separate': True,\n                                'parse_errors': robot.errors, 'parse_warnings': robot.warnings}";assert needle in s;p.write_text(s.replace(needle,replace))
# The prior test assumed an opaque value with an internal separator was
# always indexable. Strengthen it to the conservative unknown contract while
# still asserting the quoted word never becomes a valid noindex flag.
p=work/name;s=p.read_text();start=s.index('    def test_08_quoted_values_not_flags');end=s.index('    def test_09_',start)
block=s[start:end]
oldline="            with self.subTest(value=value):self.assertEqual(self.state({'robots':[value]}),'indexable_candidate')"
newline="            with self.subTest(value=value):\n                self.assertFalse(robots.google_directive_evidence({'robots':[value]},'')['noindex'])\n                expected='insufficient_evidence' if value=='foo=\"googlebot: noindex\"' else 'indexable_candidate'\n                self.assertEqual(self.state({'robots':[value]}),expected)"
assert oldline in block;s=s[:start]+block.replace(oldline,newline)+s[end:];p.write_text(s)
specific=run('after-final-specific',[sys.executable,'-c',boot,'tests.unit.test_seo_robots_sources_v4','tests.unit.test_seo_robots_values_v4','tests.unit.test_seo_review_additional_v4','tests.unit.test_seo_transport_v4'])
unit=run('after-final-seo-unit',[sys.executable,'-m','unittest','discover','-s','tests/unit','-p','test_seo*.py','-q'])
integration=run('after-final-seo-integration',[sys.executable,'-m','unittest','discover','-s','tests/integration','-p','test_seo*.py','-q'])
tls=run('after-final-local-tls',[sys.executable,str(ROOT/'reports/seo/v4-patch-review/tls_fixture.py')],runenv={**env,'PYTHONPATH':str(work/'tools')})
qa=run('after-final-seo-suite',[sys.executable,'tools/ia.py','--project','fixture','qa','--suite','seo']);qd=json.loads(qa['stdout']);shutil.copy2(qd['report'],OUT/'candidate-qa-report.json')
general=run('after-final-general-unit',[sys.executable,'-m','unittest','discover','-s','tests/unit','-q'])
assert all(x['exit_code']==0 for x in (specific,unit,integration,tls,qa,general)), 'Do not publish candidate with failures'
files=sorted(old['candidate_hashes']);expected={n:sha(work/n) for n in files};diff=[]
for n in files:
 original=(ROOT/n).read_text() if (ROOT/n).exists() else '';current=(work/n).read_text();diff.extend(difflib.unified_diff(original.splitlines(keepends=True),current.splitlines(keepends=True),fromfile='a/'+n if original else '/dev/null',tofile='b/'+n))
final=ROOT/'reports/seo/v4-robots-sources-final.patch';final.write_text(''.join(diff))
fresh=Path(tempfile.mkdtemp(prefix='seo-v4-source-artifact3-',dir=ROOT/'.local'))
for n in old['base_hashes']:
 f=fresh/n;f.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/n,f)
assert run('artifact-dry-run',['patch','--batch','--forward','--fuzz=0','--dry-run','-p1','-i',str(final)],cwd=fresh)['exit_code']==0
assert run('artifact-apply-isolated',['patch','--batch','--forward','--fuzz=0','-p1','-i',str(final)],cwd=fresh)['exit_code']==0
assert all(sha(fresh/n)==h for n,h in expected.items());assert all(sha(ROOT/n)==h for n,h in old['base_hashes'].items())
result={**old,'patch_sha256':sha(final),'patch_bytes':final.stat().st_size,'candidate_hashes':expected,'candidate_directory':str(work.relative_to(ROOT)),'reviewed_predecessor_sha256':old['patch_sha256'],'review':'new exact-hash independent review pending; prior approvals not reused','all_checks_pass':True}
(OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
