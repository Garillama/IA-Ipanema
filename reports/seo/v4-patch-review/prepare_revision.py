"""Prepara una revisión adicional solo en la copia aislada y exporta el diff."""
from pathlib import Path
import difflib,hashlib,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
base=json.loads((OUT/'validation.json').read_text());work=ROOT/base['isolated_directory']
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==value for p,value in base['source_hashes'].items())
files=set(base['source_hashes'])
def replace(name,old,new):
 p=work/name;data=p.read_text();assert old in data,(name,old);p.write_text(data.replace(old,new));files.add(name)
crawler='tools/ipanema/seo/crawler.py'
replace(crawler,'sitemap_seen, sitemap_urls, normalized_sitemap = set(), [], set()', 'sitemap_seen, sitemap_urls, normalized_sitemap = set(), [], set()\n        sitemap_redirect_targets = {}')
replace(crawler,"result['sitemaps'].append({'url': url, 'status': response['status'], 'redirect': target})", "result['sitemaps'].append({'url': url, 'status': response['status'], 'redirect': target})\n                    sitemap_redirect_targets[url] = target")
replace(crawler,"        if sitemap_queue:\n", """        resolved_documents = {s['source'] for s in result['sitemaps'] if s.get('kind') and not s.get('errors')}
        unresolved_documents = []
        for document in sorted(sitemap_seen):
            cursor, chain = document, set()
            while cursor in sitemap_redirect_targets and cursor not in chain:
                chain.add(cursor)
                cursor = sitemap_redirect_targets[cursor]
            if cursor not in resolved_documents:
                unresolved_documents.append(document)
        result['sitemap_documents_unverified'] = unresolved_documents
        if unresolved_documents:
            result['errors'].append({'operation': 'sitemap', 'reason': 'unresolved_sitemap_documents'})
        if sitemap_queue:
""")
replace(crawler,"    complete = bool(robots_known", """    verified_urls = {n['url'] for n in result['urls'] if n.get('status') is not None and not n.get('error')}
    required_urls = {policy.home, *result['sitemap_urls'], *(e['target'] for e in result['edges'])}
    result['verification_coverage'] = {'required_count': len(required_urls), 'verified_count': len(required_urls & verified_urls),
                                       'unverified_required_urls': sorted(required_urls - verified_urls),
                                       'meaning': 'home, accepted sitemap URLs and observed permitted internal/redirect targets; HTTP 404 is checked, not healthy'}
    complete = bool(not result['verification_coverage']['unverified_required_urls'] and robots_known""")
policy='tools/ipanema/seo/crawl_policy.py'
replace(policy,"suscripciones)(?:/|$)","suscripciones)(?:/|$|[.;])")
replace(policy,"carrito|comprar)(?:/|$)","carrito|comprar)(?:/|$|[.;])")
replace(policy,"def public_addresses(host):", """def _public_address(value):
    address = ipaddress.ip_address(value)
    if not address.is_global or address.is_multicast:
        return False
    if isinstance(address, ipaddress.IPv6Address):
        # Conservative: no translated/tunnel IPv4, even with globally classified IPv6 prefixes.
        if address.ipv4_mapped or address.sixtofour or address.teredo:
            return False
        if address in ipaddress.ip_network('64:ff9b::/96') or address in ipaddress.ip_network('64:ff9b:1::/48'):
            return False
    return True


def public_addresses(host):""")
replace(policy,"any(not ipaddress.ip_address(ip).is_global or ipaddress.ip_address(ip).is_multicast for ip in addresses)","any(not _public_address(ip) for ip in addresses)")
replace(policy,"        self.sleep(delay)\n        self.last, self.calls", """        self.sleep(delay)
        remaining = limits.max_seconds - (self.clock() - self.started)
        if remaining <= 0:
            self.stop_reason = 'time_budget'
            raise IpanemaError('Presupuesto agotado durante la espera; no se inicia otra solicitud.')
        self.last, self.calls""")
replace(policy,"timeout=min(limits.timeout, limits.max_seconds - (self.clock() - self.started))", "timeout=min(limits.timeout, remaining)")
# Integrate extended cases without inheriting pre-existing test classes or inflating counts.
newtest='tests/unit/test_seo_review_additional_v4.py';(work/newtest).write_text((OUT/'cases.py').read_text());files.add(newtest)
# Remove the isolated duplicate to avoid duplicate discovery during broad QA.
(work/'tests/unit/test_v4_patch_extended.py').unlink()
# Original inherited test module is replaced by actual O1-O5 cases in the added module.
(work/'tests/unit/test_seo_review_findings_v4.py').unlink()
patch=[]
for name in sorted(files):
 old=(ROOT/name).read_text() if (ROOT/name).exists() else '';new=(work/name).read_text()
 patch.extend(difflib.unified_diff(old.splitlines(keepends=True),new.splitlines(keepends=True),fromfile='a/'+name if old else '/dev/null',tofile='b/'+name))
# No original artifact or engine source is overwritten.
revision=ROOT/'reports/seo/v4-review-corrections-v2.patch';revision.write_text(''.join(patch))
env={k:v for k,v in os.environ.items() if not k.startswith('IPANEMA_')};env['IPANEMA_ALLOW_NETWORK']='0'
def run(label,args):
 p=subprocess.run(args,cwd=work,env=env,capture_output=True,text=True,timeout=90)
 d={'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};(OUT/(label+'.json')).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return d
boot='import socket,unittest,sys;socket.socket.connect=lambda *a,**k: (_ for _ in ()).throw(AssertionError("network_forbidden_in_fixture"));r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName("tests.unit.test_seo_review_additional_v4"));sys.exit(not r.wasSuccessful())'
extended=run('after-v2-extended',[sys.executable,'-c',boot])
unit=run('after-v2-seo-unit',[sys.executable,'-m','unittest','discover','-s','tests/unit','-p','test_seo*.py','-q'])
integration=run('after-v2-seo-integration',[sys.executable,'-m','unittest','discover','-s','tests/integration','-p','test_seo*.py','-q'])
result={'kind':'seo-v4-revised-isolated-candidate','patch':str(revision.relative_to(ROOT)),'patch_sha256':hashlib.sha256(revision.read_bytes()).hexdigest(),'base_source_hashes':base['source_hashes'],'candidate_source_hashes':{name:hashlib.sha256((work/name).read_bytes()).hexdigest() for name in sorted(files)},'workspace_source_unchanged':all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==value for p,value in base['source_hashes'].items()),'patch_applied_to_workspace':False,'external_crawl_authorized':False,'storefront_network_requests':0,'extended_exit':extended['exit_code'],'seo_unit_exit':unit['exit_code'],'seo_integration_exit':integration['exit_code'],'independent_review':'pending; original patch review does not approve this revised diff','human_approval':'pending'}
(OUT/'revision-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
