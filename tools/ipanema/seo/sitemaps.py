"""Sitemaps nativos: parser offline acotado, sin red ni sustitución del XML."""
from __future__ import annotations

from datetime import date, datetime, timezone
import re
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

from ..core import IpanemaError, safe_url


def parse_sitemap(xml, *, source, max_entries=2000, max_bytes=2_000_000, today=None):
    if not isinstance(max_entries, int) or not 1 <= max_entries <= 50000:
        raise IpanemaError('Límite de entradas XML inválido.')
    raw = xml if isinstance(xml, bytes) else xml.encode('utf-8')
    if len(raw) > max_bytes:
        raise IpanemaError('Sitemap supera presupuesto de bytes.')
    try:
        text = raw.decode('utf-8-sig')
    except UnicodeError:
        raise IpanemaError('Sitemap requiere UTF-8 verificable.') from None
    if '\x00' in text or re.search(r'<!\s*(DOCTYPE|ENTITY)', text, re.I):
        raise IpanemaError('DTD y entidades no están permitidos en sitemaps.')
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        raise IpanemaError('XML de sitemap inválido.') from None
    local = lambda tag: tag.rsplit('}', 1)[-1]
    kind = local(root.tag)
    if kind not in ('urlset', 'sitemapindex'):
        raise IpanemaError('Se esperaba urlset o sitemapindex.')
    expected = 'url' if kind == 'urlset' else 'sitemap'
    entries, errors, duplicates, seen = [], [], [], set()
    rows = list(root)
    if len(rows) > max_entries:
        raise IpanemaError('Sitemap supera límite de entradas; no se trunca silenciosamente.')
    today = today or datetime.now(timezone.utc).date()
    for index, node in enumerate(rows):
        if local(node.tag) != expected:
            errors.append({'entry': index, 'reason': 'unexpected_element'})
            continue
        values = {}
        for child in node:
            values.setdefault(local(child.tag), []).append((child.text or '').strip())
        locations = values.get('loc', [])
        if len(locations) != 1:
            errors.append({'entry': index, 'reason': 'missing_or_multiple_loc'})
            continue
        url = locations[0]
        try:
            safe_url(url, local=False)
            if urlsplit(url).fragment:
                raise IpanemaError('Fragmento no permitido.')
        except (IpanemaError, ValueError):
            errors.append({'entry': index, 'reason': 'unsafe_or_invalid_url'})
            continue
        if url in seen:
            duplicates.append(url)
        seen.add(url)
        lastmod = values.get('lastmod', [None])[0]
        validity = 'absent'
        if lastmod:
            try:
                parsed = date.fromisoformat(lastmod) if len(lastmod) == 10 else datetime.fromisoformat(lastmod.replace('Z', '+00:00')).date()
                validity = 'future' if parsed > today else 'valid_declared_date'
            except ValueError:
                validity = 'invalid'
        entries.append({'url': url, 'source_sitemap': source, 'entry': index,
                        'lastmod': lastmod, 'lastmod_state': validity})
    return {'kind': kind, 'source': source, 'entries': entries, 'duplicates': duplicates,
            'errors': errors, 'lastmod_authority': 'publisher_declaration_not_verified',
            'ranking_assumptions': 'priority/changefreq are not ranking guarantees'}
