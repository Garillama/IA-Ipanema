"""Permisos y límites reales del gateway; Google se simula explícitamente."""
import datetime as dt
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tests.support import make_project
from ipanema.core import IpanemaError, Project
from ipanema.access.gateway import Gateway, serve
from ipanema.access.policy import Policy
from ipanema.seo.adapters import ProviderError


class AccessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='ipanema access ')
        self.addCleanup(self.tmp.cleanup)
        self.project = Project(make_project(Path(self.tmp.name)))
        self.project.data['google'] = {'gsc': {'site_url': 'https://example.invalid/',
                                               'oauth_token_env': 'IPANEMA_TEST_GSC_TOKEN'}}
        self.policy = Policy(self.project)

    def grant(self, capabilities=None, agent='codex', **kwargs):
        return self.policy.issue(agent, 'seo-123', capabilities or ['gsc.read'],
                                 allow_network=True, allow_account_read=True, **kwargs)

    def gateway(self, grant, factory):
        gateway = Gateway(self.project, grant['id'], rest_factory=factory)
        self.addCleanup(gateway.close)
        return gateway

    def test_deny_default_and_no_self_escalation_via_arguments(self):
        with self.assertRaises(IpanemaError):
            self.policy.issue('codex', 'seo', ['gsc.read'])
        with self.assertRaises(IpanemaError):
            self.policy.issue('invented', 'seo', ['gsc.read'], allow_network=True, allow_account_read=True)
        grant = self.grant()
        gateway = self.gateway(grant, lambda callback: self.fail('Network must not run'))
        self.assertEqual({t['name'] for t in gateway.tools()}, {'gsc_search_analytics', 'gsc_inspect_url', 'gsc_sitemaps'})
        for tool,args in [('merchant_products', {'request': {}}),
                          ('gsc_sitemaps', {'request': {}, 'agent': 'claude'}),
                          ('evaluate_script', {'function': 'alert(1)'})]:
            with self.assertRaises(IpanemaError):
                gateway.call(tool, args)

    def test_each_runtime_gets_separate_project_task_grant(self):
        ids = []
        for agent in ('claude', 'codex'):
            grant = self.grant(agent=agent)
            ids.append(grant['id'])
            self.assertEqual(self.policy.load(grant['id'])['agent'], agent)
            self.assertEqual(self.policy.load(grant['id'])['task'], 'seo-123')
        self.assertEqual(len(set(ids)), 2)
        wrong_project = Project(self.project.root)
        wrong_project.id = 'other'
        with self.assertRaises(IpanemaError):
            Policy(wrong_project).load(ids[0])

    def test_revoke_expire_and_changed_configuration(self):
        grant = self.grant()
        gateway = self.gateway(grant, lambda callback: self.fail('No network'))
        grant['revoked'] = True
        self.policy.save(grant)
        with self.assertRaises(IpanemaError):
            gateway.tools()
        grant['revoked'] = False
        grant['expires_at'] = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=1)).isoformat()
        self.policy.save(grant)
        with self.assertRaises(IpanemaError):
            gateway.tools()
        fresh = self.grant()
        self.project.data['google']['gsc']['site_url'] = 'https://example.invalid/blog/'
        with self.assertRaises(IpanemaError):
            self.policy.load(fresh['id'])

    def test_revoke_preserves_consumed_quota(self):
        grant = self.grant()
        with self.policy.locked():
            self.policy.consume(grant['id'], 'gsc_sitemaps')
        self.policy.revoke(grant['id'])
        final = self.policy.load(grant['id'], active=False)
        self.assertTrue(final['revoked'])
        self.assertEqual(final['calls'], 1)

    def test_live_rest_path_reuses_adapter_and_does_not_save_secret(self):
        calls = []
        class MockREST:
            kind = 'mock_rest'
            def __init__(self, callback):
                self.callback = callback
            def call(self, provider, operation, request):
                calls.append((provider, operation, request))
                self.assert_token = self.callback()
                return {'sitemap': [{'path': 'https://example.invalid/sitemap.xml'}]}
            def disconnect(self):
                pass
        grant = self.grant(max_calls=1)
        with patch.dict(os.environ, {'IPANEMA_TEST_GSC_TOKEN': 'synthetic-secret-not-real'}):
            result = self.gateway(grant, MockREST).call('gsc_sitemaps', {'request': {}})
        self.assertEqual(result['status'], 'observed')
        self.assertEqual(calls[0][2]['siteUrl'], 'https://example.invalid/')
        # Quota persists in a NEW gateway/process; no per-session reset.
        with self.assertRaises(IpanemaError):
            self.gateway(grant, MockREST).call('gsc_sitemaps', {'request': {}})
        for path in self.project.root.rglob('*.json'):
            self.assertNotIn('synthetic-secret-not-real', path.read_text())

    def test_forbidden_and_quota_stop_across_grants(self):
        for code in (403, 429):
            with self.subTest(code=code):
                self.policy.stop_path('gsc').unlink(missing_ok=True)
                class FailingREST:
                    kind = 'mock_rest'
                    def __init__(self, callback): pass
                    def call(self, *args): raise ProviderError(code)
                    def disconnect(self): pass
                with patch.dict(os.environ, {'IPANEMA_TEST_GSC_TOKEN': 'synthetic-token'}):
                    result = self.gateway(self.grant(), FailingREST).call('gsc_sitemaps', {'request': {}})
                    self.assertIn(result['status'], ('forbidden_stop', 'quota_stop'))
                    with self.assertRaises(IpanemaError):
                        self.gateway(self.grant(), FailingREST).call('gsc_sitemaps', {'request': {}})

    def test_missing_credentials_and_cross_domain_never_network(self):
        gateway = self.gateway(self.grant(), lambda callback: self.fail('Network must not run'))
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(gateway.call('gsc_sitemaps', {'request': {}})['status'], 'credentials_unavailable')
        with self.assertRaises(IpanemaError):
            gateway.call('gsc_inspect_url', {'request': {'inspectionUrl': 'https://other.invalid/'}})

    def test_mcp_protocol_lists_only_granted_tools_and_reports_errors(self):
        gateway = self.gateway(self.grant(), lambda cb: self.fail('No network'))
        source = io.StringIO('\n'.join(json.dumps(x) for x in [
            {'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-06-18'}},
            {'jsonrpc':'2.0','method':'notifications/initialized'},
            {'jsonrpc':'2.0','id':2,'method':'tools/list'},
            {'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'evaluate_script','arguments':{}}}
        ]) + '\n')
        output = io.StringIO()
        serve(gateway, source, output)
        replies = [json.loads(line) for line in output.getvalue().splitlines()]
        self.assertEqual(len(replies), 3)
        self.assertEqual(len(replies[1]['result']['tools']), 3)
        self.assertTrue(replies[2]['result']['isError'])


if __name__ == '__main__':
    unittest.main()
