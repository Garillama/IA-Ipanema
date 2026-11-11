import gzip
import subprocess
import unittest
from unittest.mock import MagicMock, patch

from tests.support import ROOT
from ipanema.core import IpanemaError
from ipanema.seo.crawl_policy import _PinnedTLS, _https_get_once, https_get


class TransportV4(unittest.TestCase):
    def test_pinned_connection_retains_tls_hostname(self):
        connection = _PinnedTLS('example.invalid', '8.8.8.8', 2)
        connection._context = MagicMock()
        with patch('socket.create_connection') as create:
            connection.connect()
            create.assert_called_once_with(('8.8.8.8', 443), 2)
            connection._context.wrap_socket.assert_called_once_with(create.return_value, server_hostname='example.invalid')

    def test_get_only_no_auth_proxy_and_header_boundaries(self):
        response = MagicMock(status=200)
        response.getheaders.return_value = [('X-Robots-Tag', 'otherbot: noindex'), ('X-Robots-Tag', 'noindex'), ('Set-Cookie', 'private')]
        response.read.return_value = b'<main>Fixture</main>'
        connection = MagicMock(); connection.getresponse.return_value = response
        with patch('ipanema.seo.crawl_policy.public_addresses', return_value=['8.8.8.8']), patch('ipanema.seo.crawl_policy._PinnedTLS', return_value=connection):
            result = _https_get_once('https://example.invalid/a?page=2', timeout=2, max_bytes=1000)
        args, kw = connection.request.call_args
        self.assertEqual(args, ('GET', '/a?page=2'))
        self.assertNotIn('Cookie', kw['headers']); self.assertNotIn('Authorization', kw['headers'])
        self.assertEqual(result['headers']['x-robots-tag'], ['otherbot: noindex', 'noindex'])
        self.assertNotIn('set-cookie', result['headers'])
        connection.close.assert_called_once()

    def test_real_deadline_dns_headers_and_no_env_proxy(self):
        with patch('subprocess.run', side_effect=subprocess.TimeoutExpired('client', 1)) as run:
            with self.assertRaises(IpanemaError): https_get('https://example.invalid/', timeout=1, max_bytes=1000)
        self.assertEqual(run.call_args.kwargs['timeout'], 1)
        self.assertEqual(run.call_args.kwargs['env'], {})

    def test_gzip_bomb_and_403_body_never_read(self):
        response = MagicMock(status=200)
        response.getheaders.return_value = [('Content-Encoding', 'gzip')]
        response.read.return_value = gzip.compress(b'x' * 2000)
        connection = MagicMock(); connection.getresponse.return_value = response
        with patch('ipanema.seo.crawl_policy.public_addresses', return_value=['8.8.8.8']), patch('ipanema.seo.crawl_policy._PinnedTLS', return_value=connection):
            with self.assertRaises(IpanemaError): _https_get_once('https://example.invalid/', timeout=2, max_bytes=100)
            response.status = 403
            response.read.reset_mock()
            result = _https_get_once('https://example.invalid/', timeout=2, max_bytes=100)
            self.assertEqual(result['status'], 403)
            response.read.assert_not_called()
