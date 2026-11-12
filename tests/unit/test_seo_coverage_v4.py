from pathlib import Path
import tempfile
import unittest

from tests.support import make_project
from ipanema.core import Project, IpanemaError
from ipanema.seo.coverage_import import import_csv, validate_export
from ipanema.seo.adapters import import_observation


class CoverageV4(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.project = Project(make_project(Path(self.tmp.name), theme=False))
        self.site = 'https://example.invalid/'
        self.project.data['google'] = {'gsc': {'site_url': self.site}}

    def tearDown(self): self.tmp.cleanup()

    def test_offline_export_preserves_only_real_fields(self):
        raw = 'URL,Último rastreo,Estado\nhttps://example.invalid/a,2026-11-01,Excluded\n'
        result = import_csv(self.project, raw, site_url=self.site, observed_at='2026-11-11T00:00:00Z',
                            mapping={'url': 'URL', 'last_crawl': 'Último rastreo', 'coverage_state': 'Estado'})
        self.assertEqual(result['rows'][0]['last_crawl'], '2026-11-01')
        self.assertFalse(result['live_connection_tested']); self.assertFalse(result['exhaustive_index_inventory'])
        self.assertEqual(validate_export(self.project, result), result)

    def test_foreign_property_domain_and_missing_date_rejected(self):
        for site, date, url in [('https://other.invalid/', '2026-11-11', self.site),
                                (self.site, '', self.site), (self.site, '2026-11-11', 'https://other.invalid/a')]:
            with self.subTest(site=site, date=date, url=url), self.assertRaises(IpanemaError):
                import_csv(self.project, 'URL\n' + url, site_url=site, observed_at=date, mapping={'url': 'URL'})

    def test_rows_and_headers_budget_not_silently_truncated(self):
        with self.assertRaises(IpanemaError):
            import_csv(self.project, 'URL\n'+self.site+'a\n'+self.site+'b', site_url=self.site,
                       observed_at='2026-11-11', mapping={'url': 'URL'}, max_rows=1)
        with self.assertRaises(IpanemaError):
            import_csv(self.project, 'URL,URL\na,b', site_url=self.site, observed_at='2026-11-11', mapping={'url': 'URL'})

    def test_gsc_existing_inspection_adapter_not_live_and_damar_isolation(self):
        export = {'project': 'sample', 'provider': 'gsc', 'operation': 'inspect_url', 'observed_at': '2026-11-11',
                  'request': {'siteUrl': self.site, 'inspectionUrl': self.site},
                  'payload': {'inspectionResult': {'indexStatusResult': {'verdict': 'PASS', 'googleCanonical': self.site,
                              'userCanonical': self.site, 'lastCrawlTime': '2026-11-01T00:00:00Z'}}}}
        result = import_observation(self.project, export)
        self.assertFalse(result['data']['live_inspection'])
        self.assertEqual(result['data']['index_status']['lastCrawlTime'], '2026-11-01T00:00:00Z')
        export['project'] = 'damarbeauty'
        with self.assertRaises(IpanemaError): import_observation(self.project, export)
