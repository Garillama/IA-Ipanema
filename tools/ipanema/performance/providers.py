"""Transporte de clave API: endpoints oficiales fijos, sin redirects ni errores privados."""
import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, build_opener
from ..seo.adapters import _NoRedirect

ENDPOINTS = {'pagespeed': 'https://pagespeedonline.googleapis.com/pagespeedonline/v5/runPagespeed',
             'crux': 'https://chromeuxreport.googleapis.com/v1/records:queryRecord',
             'crux_history': 'https://chromeuxreport.googleapis.com/v1/records:queryHistoryRecord'}


class Failure(Exception):
    def __init__(self, status, http=None):
        self.status, self.http = status, http
        super().__init__(status)


def request(source, options, key, timeout=90):
    pairs = [('key', key)]
    body = None
    if source == 'pagespeed':
        pairs += [('url', options['url']), ('strategy', options['device']), ('locale', options['locale'])]
        pairs += [('category', category) for category in options['categories']]
    else:
        payload = {options['scope']: options['url'] if options['scope'] == 'url' else options['origin'],
                   'formFactor': options['form_factor'], 'metrics': options['metrics']}
        if source == 'crux_history':
            payload['collectionPeriodCount'] = options['period_count']
        body = json.dumps(payload).encode()
    req = Request(ENDPOINTS[source] + '?' + urlencode(pairs), data=body,
                  headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
                  method='GET' if source == 'pagespeed' else 'POST')
    try:
        with build_opener(_NoRedirect()).open(req, timeout=timeout) as response:
            raw = response.read(10_000_001)
            if len(raw) > 10_000_000:
                raise Failure('response_too_large')
            result = json.loads(raw, parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
            if not isinstance(result, dict):
                raise Failure('invalid_response')
            return result
    except HTTPError as error:
        code = error.code
        # Never stringify HTTPError: it includes a credential-bearing URL.
        raise Failure({403:'forbidden_stop', 429:'quota_stop', 404:'not_found', 401:'authentication_failed'}.get(code, 'http_error'), code) from None
    except (URLError, TimeoutError, OSError):
        raise Failure('network_error') from None
    except (ValueError, UnicodeError):
        raise Failure('invalid_response') from None
