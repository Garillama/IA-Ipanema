import unittest
from datetime import date

from tests.support import ROOT
from ipanema.core import IpanemaError
from ipanema.seo.sitemaps import parse_sitemap


class SitemapsV4(unittest.TestCase):
    def parse(self, text, **kw):
        return parse_sitemap(text, source='https://example.invalid/sitemap.xml', **kw)

    def test_native_urlset_duplicates_lastmod(self):
        result = self.parse('''<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url><loc>https://example.invalid/a</loc><lastmod>2026-01-01</lastmod></url>
        <url><loc>https://example.invalid/a</loc><lastmod>2099-01-01</lastmod></url>
        <url><loc>https://example.invalid/b</loc><lastmod>bad</lastmod></url></urlset>''', today=date(2026, 11, 11))
        self.assertEqual(result['kind'], 'urlset')
        self.assertEqual(result['duplicates'], ['https://example.invalid/a'])
        self.assertEqual([r['lastmod_state'] for r in result['entries']], ['valid_declared_date', 'future', 'invalid'])

    def test_index(self):
        self.assertEqual(self.parse('<sitemapindex><sitemap><loc>https://example.invalid/child.xml</loc></sitemap></sitemapindex>')['kind'], 'sitemapindex')

    def test_invalid_dtd_encoding_and_bounds(self):
        for xml in ['<urlset>', '<html/>', '<!DOCTYPE x [<!ENTITY x "abc">]><urlset/>', '<!ENTITY x "abc"><urlset/>', '<urlset/>'.encode('utf-16')]:
            with self.subTest(xml=xml), self.assertRaises(IpanemaError):
                self.parse(xml)
        with self.assertRaises(IpanemaError):
            self.parse('<urlset><url/><url/></urlset>', max_entries=1)
        with self.assertRaises(IpanemaError):
            self.parse('<urlset/>', max_bytes=3)

    def test_bad_entries_and_secrets_not_persisted(self):
        result = self.parse('<urlset><url/><url><loc>https://example.invalid/?token=secret</loc></url><url><loc>https://example.invalid/a</loc><loc>https://example.invalid/b</loc></url></urlset>')
        self.assertEqual(len(result['errors']), 3)
        self.assertNotIn('secret', str(result))
