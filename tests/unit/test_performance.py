"""Offline: fixtures sintéticos. No certifican conectividad ni cobertura de Google."""
import copy
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch, Mock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from support import make_project, ROOT
from ipanema.core import Project, IpanemaError
from ipanema.performance import model, providers
from ipanema.performance.service import Service, options, checked_url, persist

FIXTURES = ROOT/'tests/fixtures/performance'


class PerformanceTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=make_project(Path(self.temp.name),theme=False)
        self.project=Project(root=self.root)
        self.project.data['google']={'performance':{'pagespeed_key_env':'IPANEMA_SAMPLE_PSI_KEY','crux_key_env':'IPANEMA_SAMPLE_CRUX_KEY'}}
        self.env=patch.dict(os.environ,{'IPANEMA_SAMPLE_PSI_KEY':'fixture-secret+/','IPANEMA_SAMPLE_CRUX_KEY':'fixture-crux'})
        self.env.start();self.addCleanup(self.env.stop)
        self.payload=json.loads((FIXTURES/'pagespeed-mobile.json').read_text())
        self.crux=json.loads((FIXTURES/'crux-mobile.json').read_text())
        self.transport=Mock(return_value=self.payload)
        self.service=Service(self.project,transport=self.transport,sleep=lambda _:None)

    def read(self,source='pagespeed',**kw):
        return self.service.read(source,authorized=True,**kw)

    def test_complete_psi_and_profiles(self):
        r=self.read();self.assertEqual(r['status'],'observed');self.assertEqual(r['metrics']['lcp'],2400)
        self.assertIsNone(r['field_inp']);self.assertEqual(r['profile']['chrome_version'],'130.1.2.3')

    def test_partial_not_zero(self):
        del self.payload['lighthouseResult']['audits']['largest-contentful-paint']
        r=self.read();self.assertEqual(r['status'],'partial');self.assertIsNone(r['metrics']['lcp'])

    def test_runtime_and_warnings(self):
        self.payload['lighthouseResult']['runtimeError']={'code':'ERRORED_DOCUMENT_REQUEST','message':'unsafe fixture-secret+/'}
        r=self.read();self.assertEqual(r['status'],'runtime_error');self.assertNotIn('fixture-secret',json.dumps(r))

    def test_permission_before_transport_or_cache(self):
        self.read()
        with self.assertRaises(IpanemaError):self.service.read('pagespeed')
        self.assertEqual(self.transport.call_count,1)

    def test_missing_key_no_anonymous(self):
        with patch.dict(os.environ,{},clear=True):self.assertEqual(self.read()['status'],'credentials_unavailable')
        self.transport.assert_not_called()

    def test_sensitive_encoded_url_and_domain(self):
        for url in ['https://evil.invalid/','https://example.invalid/?%2561pi_key=x','https://example.invalid/?token=x','https://example.invalid/checkout/']:
            with self.assertRaises(IpanemaError):self.read(url=url)
        self.transport.assert_not_called()

    def test_private_origin_rejected(self):
        self.project.data['public_url']='https://127.0.0.1'
        with self.assertRaises(IpanemaError):checked_url(self.project,'https://127.0.0.1/')

    def test_foreign_final_url_not_saved(self):
        self.payload['lighthouseResult']['finalUrl']='https://foreign.invalid/'
        self.assertEqual(self.read()['status'],'redirect_not_authorized')

    def test_request_identity_mismatch(self):
        self.payload['lighthouseResult']['requestedUrl']='https://example.invalid/other'
        self.assertEqual(self.read()['status'],'identity_mismatch')

    def test_stop_403_429_no_retry_persistent(self):
        for status,http in [('forbidden_stop',403),('quota_stop',429)]:
            self.transport.side_effect=providers.Failure(status,http)
            self.assertEqual(self.read()['status'],status)
            self.assertEqual(self.read()['status'],'provider_stopped')
            self.service.policy.stop_path('psi').unlink() # operator fixture cleanup only
        self.assertEqual(self.transport.call_count,2)

    def test_bounded_retry_counts_budget(self):
        self.transport.side_effect=[providers.Failure('http_error',503),self.payload]
        r=self.read();self.assertEqual(r['status'],'observed');self.assertEqual(r['network_attempts'],2)
        self.assertEqual(json.loads((self.service.root/'budget-psi.json').read_text())['count'],2)

    def test_daily_and_run_budget(self):
        self.project.data['google']['performance']['daily_request_limit']=1
        self.read();self.assertEqual(self.read(device='desktop')['status'],'daily_budget_exhausted')
        self.assertEqual(self.transport.call_count,1)
        other=Service(self.project,transport=self.transport,max_calls=1)
        other.attempts=1;self.assertEqual(other.read('crux',authorized=True)['status'],'run_budget_exhausted')

    def test_cache_ttl_and_no_secret(self):
        self.assertFalse(self.read()['cache_hit']);self.assertTrue(self.read()['cache_hit'])
        self.assertEqual(self.transport.call_count,1)
        self.service.clock=lambda:9999999999
        self.assertFalse(self.read()['cache_hit']);self.assertEqual(self.transport.call_count,2)
        self.assertNotIn('fixture-secret', ''.join(p.read_text() for p in self.service.root.glob('*.json')))

    def test_cache_invalidates_configuration(self):
        self.read();self.project.data['google']['performance']['timeout_seconds']=60
        self.assertFalse(self.read()['cache_hit']);self.assertEqual(self.transport.call_count,2)

    def test_cache_unsafe_file_rejected(self):
        self.read()
        path=next(p for p in self.service.root.glob('*.json') if not p.name.startswith('budget'))
        path.chmod(0o644)
        with self.assertRaises(IpanemaError):self.read()

    def test_cache_corrupt_is_not_success(self):
        self.read()
        path=next(p for p in self.service.root.glob('*.json') if not p.name.startswith('budget'))
        path.write_text('{')
        self.assertFalse(self.read()['cache_hit']);self.assertEqual(self.transport.call_count,2)

    def test_crux_real_scope_and_inp(self):
        self.transport.return_value=self.crux
        r=self.read('crux');self.assertEqual(r['status'],'observed');self.assertEqual(r['metrics']['inp']['p75'],190)
        self.assertEqual(r['scope'],'url');self.assertEqual(r['returned_identity']['url'],'https://example.invalid')

    def test_crux_origin_never_url_fallback(self):
        self.transport.return_value=self.crux
        self.assertEqual(self.read('crux',scope='origin')['status'],'identity_mismatch')
        self.crux['record']['key']={'origin':'https://example.invalid','formFactor':'PHONE'}
        r=self.read('crux',scope='origin');self.assertEqual(r['status'],'observed');self.assertEqual(r['scope'],'origin')

    def test_crux_insufficient_does_not_query_origin(self):
        self.transport.side_effect=providers.Failure('not_found',404)
        r=self.read('crux');self.assertEqual(r['status'],'insufficient_field_data');self.assertEqual(self.transport.call_count,1)

    def test_crux_form_factor_and_partial(self):
        self.transport.return_value=self.crux
        self.assertEqual(self.read('crux',device='desktop')['status'],'identity_mismatch')
        del self.crux['record']['metrics']['interaction_to_next_paint']
        self.assertEqual(self.read('crux')['status'],'partial')

    def test_history_null_and_alignment(self):
        raw=json.loads((FIXTURES/'crux-history.json').read_text());self.transport.return_value=raw
        r=self.read('crux_history');self.assertEqual(r['metrics']['lcp']['p75s'],[2400,None])
        self.assertEqual(r['status'],'partial')
        raw['record']['metrics']['largest_contentful_paint']['percentilesTimeseries']['p75s']=[1]
        self.assertEqual(self.read('crux_history',period_count=3)['status'],'invalid_response')

    def test_comparison_identity_unknown_and_cross_source(self):
        a=self.read();b=copy.deepcopy(a);b['metrics']['lcp']=2000;b['measured_at']='2026-11-10T01:00:00Z'
        self.assertEqual(model.compare(a,b)['delta_after_minus_before']['lcp'],-400)
        b['profile']['chrome_version']=None;self.assertEqual(model.compare(a,b)['status'],'not_comparable')
        b=copy.deepcopy(a);b['source']='lighthouse_local';self.assertEqual(model.compare(a,b)['status'],'not_comparable')

    def test_median_range_and_partial_sample(self):
        a=self.read();b=copy.deepcopy(a);c=copy.deepcopy(a)
        b['metrics']['lcp']=6000;c['metrics']['lcp']=3000
        r=model.summarize([a,b,c]);self.assertEqual(r['metrics']['lcp'],3000)
        self.assertEqual(r['statistics']['lcp']['max'],6000)
        b['profile']['cache']=True;self.assertEqual(model.summarize([a,b])['status'],'not_comparable')

    def test_secret_echoes_encoded_and_private_nodes(self):
        raw={'message':'https://example.invalid/?key=fixture-secret%2B%2F','snippet':'<input value=private>',
             'url':'https://user:pass@example.invalid/?%2561pi_key=secret'}
        clean=json.dumps(model.sanitize(raw,('fixture-secret+/',)))
        for value in ['fixture-secret','private','user:pass','api_key=secret']:self.assertNotIn(value,clean)

    def test_repeated_categories_fixed_endpoint(self):
        response=Mock();response.read.return_value=b'{}';response.__enter__=Mock(return_value=response);response.__exit__=Mock(return_value=False)
        opener=Mock();opener.open.return_value=response
        with patch('ipanema.performance.providers.build_opener',return_value=opener):
            providers.request('pagespeed',options(self.project,'pagespeed'),'fixture',5)
        request=opener.open.call_args.args[0]
        from urllib.parse import parse_qs,urlsplit
        self.assertEqual(len(parse_qs(urlsplit(request.full_url).query)['category']),4)
        self.assertTrue(request.full_url.startswith(providers.ENDPOINTS['pagespeed']))
        self.assertEqual(request.method,'GET')

    def test_history_uses_post_with_exclusive_identity(self):
        response=Mock();response.read.return_value=b'{}';response.__enter__=Mock(return_value=response);response.__exit__=Mock(return_value=False)
        opener=Mock();opener.open.return_value=response
        with patch('ipanema.performance.providers.build_opener',return_value=opener):
            providers.request('crux_history',options(self.project,'crux_history',scope='origin'),'fixture',5)
        request=opener.open.call_args.args[0];payload=json.loads(request.data)
        self.assertEqual(request.method,'POST');self.assertNotIn('url',payload);self.assertEqual(payload['collectionPeriodCount'],25)

    def test_http_error_never_exposes_key(self):
        from urllib.error import HTTPError
        opener=Mock();opener.open.side_effect=HTTPError('https://example.invalid/?key=fixture-secret+/',403,'private',{},None)
        with patch('ipanema.performance.providers.build_opener',return_value=opener):
            with self.assertRaises(providers.Failure) as caught:providers.request('pagespeed',options(self.project,'pagespeed'),'fixture-secret+/',5)
        self.assertEqual(str(caught.exception),'forbidden_stop')


class PerformanceRobustness(unittest.TestCase):
    setUp = PerformanceTests.setUp
    read = PerformanceTests.read
    def test_budget_corruption_blocks_network(self):
        path=self.service.root/'budget-psi.json';path.write_text('{');path.chmod(0o600)
        self.assertEqual(self.read()['status'],'budget_invalid');self.transport.assert_not_called()

    def test_normalization_foreign_origin_denied(self):
        self.transport.return_value=self.crux
        self.crux['record']['key']['url']='https://foreign.invalid/'
        self.crux['urlNormalizationDetails']={'originalUrl':'https://example.invalid','normalizedUrl':'https://foreign.invalid/'}
        self.assertEqual(self.read('crux')['status'],'identity_mismatch')

    def test_null_field_values_partial_and_bad_period_invalid(self):
        self.transport.return_value=self.crux
        self.crux['record']['metrics']['interaction_to_next_paint']['percentiles']['p75']=None
        self.assertEqual(self.read('crux')['status'],'partial')
        self.crux['record']['collectionPeriod']['lastDate']['month']=50
        self.assertEqual(self.read('crux',device='mobile',period_count=20)['status'],'invalid_response')

    def test_concurrent_daily_budget_is_serialized(self):
        from concurrent.futures import ThreadPoolExecutor
        self.project.data['google']['performance']['daily_request_limit']=1
        def read(device):
            return Service(self.project,transport=self.transport).read('pagespeed',device=device,authorized=True)['status']
        with ThreadPoolExecutor(max_workers=2)as pool:statuses=list(pool.map(read,['mobile','desktop']))
        self.assertEqual(self.transport.call_count,1);self.assertIn('daily_budget_exhausted',statuses)

    def test_non_json_provider_response_is_not_success(self):
        response=Mock();response.read.return_value=b'{';response.__enter__=Mock(return_value=response);response.__exit__=Mock(return_value=False)
        opener=Mock();opener.open.return_value=response
        with patch('ipanema.performance.providers.build_opener',return_value=opener):
            with self.assertRaises(providers.Failure)as error:providers.request('pagespeed',options(self.project,'pagespeed'),'fixture',5)
        self.assertEqual(error.exception.status,'invalid_response')

    def test_future_cache_rejected(self):
        self.read();self.service.clock=lambda:0
        self.assertFalse(self.read()['cache_hit']);self.assertEqual(self.transport.call_count,2)

    def test_missing_versions_prevent_aggregation(self):
        a=self.read();a['profile']['chrome_version']=None
        self.assertEqual(model.summarize([a,a])['status'],'not_comparable')

    def test_root_slash_normalization(self):
        self.payload['lighthouseResult']['requestedUrl']='https://example.invalid/'
        self.assertEqual(self.read()['status'],'observed')

    def test_refresh_consumes_budget_and_cache_is_not_new_measurement(self):
        a=self.read();b=self.read()
        self.assertEqual(model.compare(a,b)['status'],'not_comparable')
        self.assertFalse(self.read(refresh=True)['cache_hit']);self.assertEqual(self.transport.call_count,2)

    def test_reduced_chrome_user_agent_blocks_comparison(self):
        self.payload['lighthouseResult']['environment']['hostUserAgent']='Chrome/130.0.0.0'
        a=self.read();self.assertEqual(a['status'],'observed');self.assertIsNone(a['profile']['chrome_version'])
        self.assertEqual(model.compare(a,a)['status'],'not_comparable')

    def test_local_incomplete_response_keeps_audit_available(self):
        from ipanema.performance.service import local
        def child(argv, **kwargs):
            job=Path(argv[-1]);folder=job.parent/'browser';folder.mkdir()
            (folder/'samples.json').write_text(json.dumps([{'requestedUrl':'https://example.invalid'}]))
            return Mock(returncode=0)
        with patch('subprocess.run',side_effect=child):
            result=local(self.project,authorized=True)
        self.assertEqual(result['status'],'local_incomplete_response')

    def test_missing_local_permission_precedes_node(self):
        from ipanema.performance.service import local
        with patch('subprocess.run')as call:
            with self.assertRaises(IpanemaError):local(self.project,authorized=False)
        call.assert_not_called()

if __name__=='__main__':unittest.main()
