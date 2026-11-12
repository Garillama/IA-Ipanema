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
        self.groups, self.maps, self.errors, self.warnings = [], [], [], []

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
                    if not re.fullmatch(r'[A-Za-z_-]+|\*', value):
                        issue = {'line': number + 1, 'reason': 'invalid_product_token'}
                        relevant = '*' in value or any(agent in value.lower() for agent in ('googlebot', 'iaipanemaaudit'))
                        (self.errors if relevant else self.warnings).append(issue)
                        continue
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
        ranked = [(max((len(a) for a in g['agents'] if a != '*' and a == product), default=0), g) for g in self.groups]
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


def _quoted_end(text, start):
    quote, cursor = text[start], start + 1
    while cursor < len(text):
        if text[cursor] == '\\':
            cursor += 2
        elif text[cursor] == quote:
            return cursor + 1, True
        else:
            cursor += 1
    return len(text), False


def _header_parts(text):
    start = cursor = 0
    while cursor < len(text):
        if text[cursor] in ('"', "'"):
            cursor, _ = _quoted_end(text, cursor)
        elif text[cursor] == ',':
            yield text[start:cursor]
            cursor += 1
            start = cursor
        else:
            cursor += 1
    yield text[start:]


_VALUE_RULES = frozenset(('unavailable_after', 'max-snippet', 'max-image-preview', 'max-video-preview'))
_FLAG_RULES = frozenset(('all', 'index', 'follow', 'noindex', 'none', 'nofollow', 'nosnippet',
    'indexifembedded', 'notranslate', 'noimageindex', 'noarchive', 'nocache', 'nositelinkssearchbox'))


# Retention limits do not stop semantic evaluation of permitted input.
MAX_SOURCE_BYTES = 2_000_000
MAX_TOTAL_BYTES = 4_000_000
MAX_PROCESS_SOURCES = 128
MAX_RETAINED_SOURCES = 16
MAX_SAMPLES = 8
MAX_EVIDENCE_BYTES = 65_536


class _Samples(list):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.reasons = {}

    def append(self, value):
        self.count += 1
        if isinstance(value, dict):
            value = {k: v[:96] if isinstance(v, str) else v for k, v in value.items()}
            if 'reason' in value:
                self.reasons.setdefault(value['reason'], value)
        if len(self) < MAX_SAMPLES:
            super().append(value)

    def __iadd__(self, values):
        for value in values:
            self.append(value)
        return self


def _parse_directive_source(text):
    """One physical source only. Quote state can never escape this call."""
    flags, parameters, errors, unknown = set(), _Samples(), _Samples(), _Samples()
    ambiguous_parameter = False
    delimiters = ',; \t\r\n'
    names = re.compile(r'[A-Za-z][A-Za-z0-9_-]*')
    length, cursor = len(text), 0
    def atom_end(start):
        while start < length and text[start] not in delimiters:
            if text[start] in ('"', "'"):
                position = start
                start, closed = _quoted_end(text, start)
                if not closed:
                    errors.append({'reason': 'unclosed_quote', 'selected_offset': position})
            elif text[start] == '\\':
                if start + 1 == length:
                    errors.append({'reason': 'incomplete_escape', 'selected_offset': start})
                start = min(length, start + 2)
            else:
                start += 1
        return start
    while cursor < length:
        if text[cursor] in delimiters:
            cursor += 1
            continue
        match = names.match(text, cursor)
        if match is None:
            end = atom_end(cursor)
            unknown.append({'kind': 'unrecognized_atom', 'selected_offset': cursor})
            cursor = end
            continue
        key, end = match[0].lower(), match.end()
        probe = end
        while probe < length and text[probe].isspace():
            probe += 1
        if probe < length and text[probe] in ':=':
            probe += 1
            while probe < length and text[probe].isspace():
                probe += 1
            finish = atom_end(probe)
            quoted_separators = any(q in text[probe:finish] for q in ('\"', "'")) and any(c.isspace() or c in ',;' for c in text[probe:finish])
            ambiguous_parameter |= key not in _VALUE_RULES and quoted_separators
            parameters.append({'name': key, 'has_value': finish > probe, 'known': key in _VALUE_RULES,
                               'quoted_separators': quoted_separators})
            if finish == probe:
                errors.append({'reason': 'missing_value', 'directive': key, 'selected_offset': cursor})
            if key in ('noindex', 'none', 'index', 'all'):
                errors.append({'reason': 'flag_has_value', 'directive': key, 'selected_offset': cursor})
            cursor = finish
        elif end == length or text[end] in delimiters:
            if key in _FLAG_RULES:
                flags.add(key)
            elif key in _VALUE_RULES:
                errors.append({'reason': 'missing_value', 'directive': key, 'selected_offset': cursor})
            else:
                unknown.append({'kind': 'unknown_directive', 'name': key, 'selected_offset': cursor})
            cursor = end
        else:
            finish = atom_end(end)
            errors.append({'reason': 'invalid_directive_token', 'selected_offset': cursor})
            cursor = finish
    return {'flags': sorted(flags), 'parameters': parameters, 'errors': errors, 'unknown': unknown,
            'noindex': bool(flags & {'noindex', 'none'}), 'ambiguous_parameter': ambiguous_parameter,
            'grammar_errors': list(errors.reasons.values()),
            'counts': {k: v.count for k, v in [('parameters', parameters), ('errors', errors), ('unknown', unknown)]},
            'truncated': any(v.count > len(v) for v in (parameters, errors, unknown))}


def _google_header_source(value):
    """Apply agent scopes within one header field; reset for the next field."""
    active, selected, scopes, errors = True, [], set(), _Samples()
    for part in _header_parts(value):
        match = re.match(r'\s*([a-zA-Z][\w-]*)\s*:\s*(.*)', part)
        if match and match[1].lower() not in (_VALUE_RULES | _FLAG_RULES):
            scope = match[1].lower()
            scopes.add(scope)
            active = scope == 'googlebot'
            part = match[2]
            if active and not part.strip():
                errors.append({'reason': 'missing_agent_directive'})
        if active:
            selected.append(part)
    return ','.join(selected), sorted(scopes), errors


def _ambiguity_errors(value, parsed, *, header_field):
    # A diagnostic alternative, never a source of valid flags. Keep the original
    # physical field boundary even when comparing comma/quote interpretations.
    errors = []
    if header_field:
        for error in _parse_directive_source(value)['grammar_errors']:
            if error['reason'] in ('unclosed_quote', 'incomplete_escape'):
                errors.append({**error, 'reason': 'ambiguous_header_scope'})
    if parsed['ambiguous_parameter']:
        errors.append({'reason': 'unsupported_quoted_separator_grammar'})
    # A syntactically recognized scoped rule list stays scoped across commas.
    # Do not turn a valid otherbot: nofollow, noindex list into global restrictions.
    scoped_list = False
    if header_field:
        prefix, colon, rest = value.partition(':')
        if colon and prefix.strip().lower() not in (_VALUE_RULES | _FLAG_RULES):
            _, scopes, _ = _google_header_source(value)
            first = _parse_directive_source(next(iter(_header_parts(rest)), ''))
            scoped_list = (prefix.strip().lower() in scopes and not first['errors'] and not first['unknown'] and
                           (bool(first['flags']) or bool(first['parameters']) and all(p['known'] for p in first['parameters'])))
    # No alternative can contain a restrictive token if neither word occurs.
    # Avoid reparsing every comma atom in large parameter-only fields.
    if (',' in value and not parsed['noindex'] and not scoped_list
            and re.search(r'\b(?:noindex|none)\b', value, re.I)):
        for match in re.finditer(r'[^,]+', value):
            part = match[0]
            alternative = part.strip().strip('"' + "'")
            if header_field:
                alternative, _, _ = _google_header_source(alternative)
            if _parse_directive_source(alternative)['noindex']:
                errors.append({'reason': 'ambiguous_comma_interpretation'})
                break
    return errors


def google_directive_evidence(meta, header):
    """Bounded samples; complete semantic processing within explicit input budgets.

    Physical source hashes and offsets locate retained samples in the original
    capture. Missing raw captures cannot be reconstructed from a hash alone.
    Retention truncation is independent of processing incompleteness.
    """
    import hashlib
    import json
    sources, flags, errors = [], set(), _Samples()
    counts = {'sources_seen': 0, 'sources_processed': 0, 'input_bytes_processed': 0,
              'parameters': 0, 'unknown': 0, 'errors': 0}
    noindex, complete, truncated = False, True, False
    collection = hashlib.sha256()

    def add(kind, name, index, value):
        nonlocal noindex, complete, truncated
        counts['sources_seen'] += 1
        identity = {'kind': kind, 'name': name, 'index': index}
        if not isinstance(value, str):
            complete = False
            errors.append({'source': identity, 'reason': 'invalid_source_type'})
            counts['errors'] += 1
            return
        # Character guard prevents encoding arbitrarily large strings first.
        size = len(value.encode('utf-8')) if len(value) <= MAX_SOURCE_BYTES else MAX_SOURCE_BYTES + 1
        if size > MAX_SOURCE_BYTES or counts['input_bytes_processed'] + size > MAX_TOTAL_BYTES:
            complete = False
            errors.append({'source': identity, 'reason': 'directive_processing_byte_budget'})
            counts['errors'] += 1
            return
        counts['input_bytes_processed'] += size
        counts['sources_processed'] += 1
        digest = hashlib.sha256(value.encode()).hexdigest()
        collection.update(json.dumps([kind, name, index, digest]).encode())
        selected, scopes, selection_errors = _google_header_source(value) if kind == 'header' else (value, [name], [])
        parsed = _parse_directive_source(selected)
        ambiguity_errors = _ambiguity_errors(value, parsed, header_field=kind == 'header')
        parsed['errors'] += selection_errors
        parsed['errors'] += ambiguity_errors
        parsed['counts']['errors'] += (selection_errors.count if isinstance(selection_errors, _Samples) else len(selection_errors)) + len(ambiguity_errors)
        parsed['truncated'] |= parsed['counts']['errors'] > len(parsed['errors'])
        noindex |= parsed['noindex']
        flags.update(parsed['flags'])
        for key in ('parameters', 'unknown', 'errors'):
            counts[key] += parsed['counts'][key]
        for error in parsed['errors']:
            errors.append({'source': identity, **error})
        retained_scopes = [v[:96] for v in scopes[:MAX_SAMPLES]]
        record = {**identity, 'input_sha256': digest, 'input_characters': len(value), 'input_bytes': size,
                  'scopes': retained_scopes, 'scope_count': len(scopes), **parsed}
        record['truncated'] |= len(scopes) > MAX_SAMPLES or any(len(v) > 96 for v in scopes)
        if len(sources) < MAX_RETAINED_SOURCES:
            sources.append(record)
        else:
            truncated = True
        truncated |= record['truncated']

    # No unbounded source collection is constructed. If too many physical fields
    # exist, stop with explicit incomplete status; unvisited counts/hashes unknown.
    def fields():
        for name in ('robots', 'googlebot'):
            values = meta.get(name, [])
            for index, value in enumerate(values if isinstance(values, list) else [values]):
                yield 'meta', name, index, value
        values = header if isinstance(header, list) else [] if header in ('', None) else [header]
        for index, value in enumerate(values):
            yield 'header', 'x-robots-tag', index, value
    for ordinal, row in enumerate(fields()):
        if ordinal >= MAX_PROCESS_SOURCES:
            complete = False
            errors.append({'reason': 'directive_source_budget'})
            counts['errors'] += 1
            break
        add(*row)
    result = {'sources': sources, 'flags': sorted(flags), 'noindex': noindex,
              'relevant_errors': errors, 'processing_complete': complete,
              'counts': counts, 'unvisited_sources_count': 0 if complete else None,
              'processed_collection_sha256': collection.hexdigest(), 'truncated': truncated,
              'state': 'noindex' if noindex else 'insufficient_evidence' if counts['errors'] or not complete else 'no_restrictive_flag_observed',
              'scope': 'Googlebot text results; not Google rendering/index inspection'}
    # Bound the whole serialized result as well as each source. Decisions and
    # exact processed counters survive omitted samples.
    result['counts']['sources_retained'] = len(sources)
    while len(json.dumps(result, ensure_ascii=False).encode()) > MAX_EVIDENCE_BYTES and sources:
        sources.pop()
        result['counts']['sources_retained'] = len(sources)
        result['truncated'] = True
    result['counts']['sources_retained'] = len(sources)
    return result


def google_directives(meta, header):
    """Legacy display adapter, exact historical string contract; NEVER for decisions.

    Intentionally retains parameters/scopes/wildcard formatting. External callers
    must migrate decisions to google_directive_evidence. This public adapter does
    not populate crawler reports and is not a bounded evidence serializer.
    """
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

def has_noindex(directives):
    """Single-source compatibility helper; not for combining independent inputs."""
    return _parse_directive_source(directives)['noindex']
