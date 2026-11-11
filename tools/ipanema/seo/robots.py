"""Subconjunto RFC 9309 explícito: grupos, comodines, $, regla más específica.

No pretende imitar la infraestructura de Google. Reglas no interpretables hacen
que la política quede desconocida y el crawler no continúe.
"""
import re
from urllib.parse import urlsplit


def _octets(value):
    unreserved = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~'
    def escaped(match):
        char = chr(int(match[1], 16))
        return char if char in unreserved else '%' + match[1].upper()
    value = re.sub(r'%([a-fA-F0-9]{2})', escaped, value)
    return ''.join(c if ord(c) < 128 else ''.join('%%%02X' % b for b in c.encode()) for c in value)


def _match(target, pattern, end):
    parts = pattern.split('*')
    if not target.startswith(parts[0]):
        return False
    cursor = len(parts[0])
    if len(parts) == 1:
        return not end or cursor == len(target)
    for index, part in enumerate(parts[1:], 1):
        if end and index == len(parts) - 1 and part:
            return target.endswith(part) and len(target) - len(part) >= cursor
        offset = target.find(part, cursor)
        if offset < 0:
            return False
        cursor = offset + len(part)
    return not end or pattern.endswith('*') or cursor == len(target)


class Robots:
    def __init__(self):
        self.groups, self.maps, self.errors = [], [], []

    def parse(self, lines):
        agents, rules, delay, rate = [], [], None, None
        def flush():
            if agents:
                self.groups.append({'agents': agents[:], 'rules': rules[:], 'delay': delay, 'rate': rate})
        for number, raw in enumerate(lines):
            line = raw.lstrip('\ufeff').split('#', 1)[0].strip()
            if not line or ':' not in line:
                continue
            key, value = (x.strip() for x in line.split(':', 1))
            key = key.lower()
            if key == 'sitemap':
                self.maps.append(value)
            elif key == 'user-agent':
                if rules or delay is not None or rate is not None:
                    flush()
                    agents, rules, delay, rate = [], [], None, None
                if value:
                    agents.append(value.lower())
            elif key in ('allow', 'disallow') and agents:
                if not value:
                    continue
                if not value.startswith('/') or re.search(r'%(?![a-fA-F0-9]{2})', value):
                    self.errors.append({'line': number + 1, 'reason': 'unsupported_path_rule'})
                    continue
                pattern = _octets(value)
                if len(pattern) > 2048 or sum(len(g['rules']) for g in self.groups) + len(rules) >= 2000:
                    self.errors.append({'line': number + 1, 'reason': 'robots_rule_budget'})
                    continue
                end = pattern.endswith('$')
                if '$' in pattern[:-1]:
                    self.errors.append({'line': number + 1, 'reason': 'unsupported_anchor'})
                    continue
                source = pattern[:-1] if end else pattern
                specificity = len(re.sub(r'%[0-9A-F]{2}', 'x', source.replace('*', '')))
                rules.append((source, end, specificity, key == 'allow'))
            elif key == 'crawl-delay' and agents:
                try:
                    delay = float(value)
                    if not 0 <= delay <= 86400:
                        raise ValueError()
                except ValueError:
                    self.errors.append({'line': number + 1, 'reason': 'invalid_crawl_delay'})
            elif key == 'request-rate' and agents:
                if re.fullmatch(r'[1-9][0-9]*/[1-9][0-9]*', value):
                    requests, seconds = map(int, value.split('/'))
                    rate = seconds / requests
                else:
                    self.errors.append({'line': number + 1, 'reason': 'invalid_request_rate'})
        flush()

    def _selected(self, agent):
        product = agent.lower().split('/')[0]
        ranked = [(max((len(a) for a in g['agents'] if a != '*' and a in product), default=0), g) for g in self.groups]
        maximum = max((n for n, _ in ranked), default=0)
        return [g for n, g in ranked if n == maximum and (maximum or '*' in g['agents'])]

    def can_fetch(self, agent, url):
        if self.errors:
            return False
        u = urlsplit(url)
        target = _octets((u.path or '/') + ('?' + u.query if u.query else ''))
        matches = [(size, allow) for g in self._selected(agent) for pattern, end, size, allow in g['rules'] if _match(target, pattern, end)]
        return max(matches, default=(0, True))[1]

    def site_maps(self):
        return self.maps[:]

    def crawl_delay(self, agent):
        return max((g['delay'] or 0 for g in self._selected(agent)), default=0)

    def request_rate_interval(self, agent):
        return max((g['rate'] or 0 for g in self._selected(agent)), default=0)


def google_directives(meta, header):
    """X-Robots-Tag multivalor: los prefijos de otros bots no se heredan."""
    if isinstance(header, list):
        return ','.join([google_directives(meta, ''), *(google_directives({}, h) for h in header)])
    active, result = True, list(meta.get('robots', [])) + list(meta.get('googlebot', []))
    for part in header.split(','):
        match = re.match(r'\s*([a-zA-Z][\w-]*)\s*:\s*(.*)', part)
        if match and match[1].lower() not in ('unavailable_after', 'max-snippet', 'max-image-preview', 'max-video-preview'):
            active = match[1].lower() in ('googlebot', '*')
            part = match[2]
        if active:
            result.append(part)
    return ','.join(result).lower()
