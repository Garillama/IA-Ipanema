"""OAuth local y contratos simulados; nunca representa consentimiento Google real."""
import json
from pathlib import Path
import tempfile
import unittest
from urllib.parse import parse_qs, urlsplit
from unittest.mock import patch

from tests.support import make_project, put
from ipanema.core import IpanemaError, Project
from ipanema.access.oauth import authorization_url, callback_code, client_config, verify_live
from ipanema.seo.adapters import SCOPES
from ipanema.access.devtools import profile_origins
from ipanema.access.credentials import store_token, load_token, credential_path


class OAuthTests(unittest.TestCase):
    def test_pkce_only_readonly_no_offline_token(self):
        uri = authorization_url('synthetic-client', 'http://127.0.0.1:123/callback', 'random-state', 'v'*64)
        values = parse_qs(urlsplit(uri).query)
        self.assertEqual(values['scope'], [SCOPES['gsc']])
        self.assertEqual(values['code_challenge_method'], ['S256'])
        self.assertEqual(values['access_type'], ['online'])
        self.assertNotIn('v'*64, uri)

    def test_callback_rejects_csrf_duplicates_and_denial(self):
        self.assertEqual(callback_code('code=synthetic-code&state=good', 'good'), 'synthetic-code')
        for query in ('code=x&state=bad', 'code=x&state=good&state=bad', 'error=access_denied&state=good'):
            with self.assertRaises(IpanemaError):
                callback_code(query, 'good')

    def test_reject_external_oauth_endpoint(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'client.json'
            put(path, {'installed': {'client_id':'synthetic', 'client_secret':'synthetic',
                                     'auth_uri':'https://attacker.invalid/auth','token_uri':'https://oauth2.googleapis.com/token'}})
            with self.assertRaises(IpanemaError):
                client_config(path)

    def test_mock_google_property_and_three_reads_explicitly(self):
        with tempfile.TemporaryDirectory() as folder:
            project = Project(make_project(Path(folder)))
            project.data['google'] = {'gsc': {'site_url':'https://example.invalid/'}}
            calls = []
            class MockREST:
                kind = 'mock_rest'
                def __init__(self, callback): pass
                def call(self, provider, operation, request):
                    calls.append(operation)
                    return {'site_info': {'siteUrl':'https://example.invalid/','permissionLevel':'siteFullUser'},
                            'search_analytics': {'rows':[]},
                            'inspect_url': {'inspectionResult':{'indexStatusResult':{'verdict':'PASS'}}},
                            'sitemaps': {'sitemap':[]}}[operation]
                def disconnect(self): pass
            with patch('ipanema.access.oauth.OfficialREST', MockREST):
                result = verify_live(project, 'synthetic-token', 'https://example.invalid/')
            self.assertTrue(result['all_reads_observed'])
            self.assertTrue(all(o['mock'] and not o['live_google_api'] for o in result['operations']))
            self.assertEqual(calls, ['site_info','search_analytics','inspect_url','sitemaps'])
            self.assertNotIn('synthetic-token', json.dumps(result))

    def test_profile_denies_wildcards_and_does_not_expand_security(self):
        with tempfile.TemporaryDirectory() as folder:
            project = Project(make_project(Path(folder)))
            project.data['browser'] = {'devtools_audit_origins':['https://cdn.example.invalid']}
            self.assertEqual(profile_origins(project, 'security'), ['https://example.invalid'])
            self.assertIn('https://cdn.example.invalid', profile_origins(project, 'audit'))
            project.data['browser']['devtools_audit_origins'] = ['https://*.invalid']
            with self.assertRaises(IpanemaError):
                profile_origins(project, 'audit')

    def test_private_token_is_bound_to_property_expires_and_never_world_readable(self):
        with tempfile.TemporaryDirectory() as folder:
            project = Project(make_project(Path(folder)))
            project.data['google'] = {'gsc': {'site_url':'https://example.invalid/'}}
            store_token(project,'synthetic-not-a-real-token',60)
            path = credential_path(project)
            self.assertEqual(path.stat().st_mode & 0o777,0o600)
            self.assertEqual(path.parent.stat().st_mode & 0o777,0o700)
            self.assertEqual(load_token(project),'synthetic-not-a-real-token')
            project.data['google']['gsc']['site_url']='sc-domain:another.invalid'
            with self.assertRaises(IpanemaError):load_token(project)
            project.data['google']['gsc']['site_url']='https://example.invalid/'
            data=json.loads(path.read_text());data['expires_at']='2000-01-01T00:00:00+00:00';path.write_text(json.dumps(data))
            self.assertIsNone(load_token(project))
            path.chmod(0o644)
            with self.assertRaises(IpanemaError):load_token(project)


if __name__ == '__main__':
    unittest.main()
