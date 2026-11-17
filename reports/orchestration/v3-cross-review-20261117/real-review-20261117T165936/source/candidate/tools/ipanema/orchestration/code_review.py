"""Optional exact-candidate review gate. No inference, activation or remote effects.

All identity/preflight/QA/resolution receipts must be supplied by the trusted
controller, never merged from a model response. This validates review evidence;
it is not a universal semantic-clone detector or proof that a reviewer is honest.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path

from ..core import IpanemaError, digest, beneath
from .adapters import validate_schema
from .planner import safe_path

PARTICIPANTS = frozenset(('claude', 'codex', 'antigravity'))
CHALLENGES = ('architecture', 'duplication', 'performance', 'regression', 'maintainability')
SEVERITIES = ('BLOCKER', 'HIGH', 'MEDIUM', 'LOW', 'INFO')


def _hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':')).encode()).hexdigest()


def _require(condition, message):
    if not condition:
        raise IpanemaError('Code review: ' + message)


def _text_schema():
    return {'type': 'string', 'minLength': 1, 'maxLength': 3000}


def _obj(properties):
    return {'type': 'object', 'properties': properties, 'required': list(properties),
            'additionalProperties': False}


def _list(items, minimum=0, maximum=64):
    return {'type': 'array', 'items': items, 'minItems': minimum, 'maxItems': maximum}


def response_schema():
    text = _text_schema()
    refs = _list(text)
    site = _obj({'file': text, 'function': text,
                 'start': {'type': 'number', 'minimum': 1},
                 'end': {'type': 'number', 'minimum': 1}})
    challenge = _obj({'status': {'type': 'string', 'enum': ['pass', 'fail', 'needs_evidence']},
                      'evidence_refs': refs, 'notes': text})
    objection = _obj({'id': text, 'severity': {'type': 'string', 'enum': list(SEVERITIES)},
                     'challenge': {'type': 'string', 'enum': list(CHALLENGES)},
                     'sites': _list(site, 1, 8), 'evidence_refs': _list(text, 1),
                     'claim': text, 'impact': text, 'recommendation': text,
                     'resolution_condition': text,
                     'duplication_kind': {'type': 'string', 'enum':
                                          ['exact', 'semantic', 'legitimate', 'not_applicable']}})
    return _obj({'candidate_sha256': text, 'reviewed_files': _list(text, 1),
                 'decision': {'type': 'string', 'enum':
                              ['approve', 'changes_requested', 'needs_evidence', 'blocked']},
                 'challenges': _obj({key: challenge for key in CHALLENGES}),
                 'objections': _list(objection, maximum=32), 'summary': text})


def fingerprint(candidate):
    """Controller candidate includes authorship, diff, scope, QA and source context."""
    return _hash(candidate)


def independent_packet(candidate, source_files, diff, tests, permissions):
    """First-pass packet excludes author's narrative and other review results."""
    _require(_hash(permissions) == candidate['context']['permissions_sha256'], 'permission packet mismatch')
    _require(hashlib.sha256(diff.encode()).hexdigest() == candidate['diff_sha256'],
             'diff bytes do not match candidate')
    _require(set(source_files) == set(candidate['context']['files']), 'incomplete source packet')
    for name, content in source_files.items():
        expected = candidate['context']['files'][name]
        _require((content is None and expected is None) or
                 (isinstance(content, str) and hashlib.sha256(content.encode()).hexdigest() == expected),
                 'source packet hash mismatch')
    safe_candidate = {k: copy.deepcopy(candidate[k]) for k in
                      ('author', 'contributors', 'objective', 'risk', 'diff_sha256', 'context',
                       'preflight', 'required_qa') if k in candidate}
    return {'candidate': safe_candidate, 'sources': copy.deepcopy(source_files), 'diff': diff,
            'tests': copy.deepcopy(tests), 'permissions': copy.deepcopy(permissions),
            'protocol': 'ipanema-code-review-candidate-1', 'phase': 'independent_code_review'}


def evaluate(candidate, reviews, *, evidence, root, answers=()):
    """Return one of four owner-facing states; never authorizes an operation.

    Trusted inputs: candidate/context/required QA and controller receipt store.
    Untrusted inputs: response bodies. Envelopes must be controller assignments.
    """
    from .council import _ledger, _proven

    _require(isinstance(candidate, dict), 'candidate missing')
    author = candidate.get('author')
    authors = candidate.get('contributors', [author])
    _require(author in PARTICIPANTS and isinstance(authors, list) and author in authors
             and len(authors) == len(set(authors)) and set(authors) <= PARTICIPANTS,
             'invalid controller authorship')
    expected_reviewers = PARTICIPANTS - set(authors)
    _require(candidate.get('risk') in ('low', 'medium', 'high'), 'risk missing')
    _require(re.fullmatch('[0-9a-f]{64}', str(candidate.get('diff_sha256', ''))), 'invalid diff hash')
    context = candidate.get('context', {})
    _require(isinstance(context, dict) and all(context.get(k) for k in
             ('project', 'run_id', 'objective_sha256', 'permissions_sha256')), 'unbound context')
    files = context.get('files')
    _require(isinstance(files, dict) and 0 < len(files) <= 64, 'source scope missing or excessive')
    _require(isinstance(candidate.get('objective'), str) and 0 < len(candidate['objective']) <= 3000
             and hashlib.sha256(candidate['objective'].encode()).hexdigest() == context['objective_sha256'],
             'objective text/hash mismatch')
    identity = fingerprint(candidate)
    ledger, invalid = _ledger(evidence, context)
    missing, changes, blockers = [], [], []
    if invalid:
        missing.append('invalid_controller_receipts')
    if len(expected_reviewers) != 2:
        blockers.append('two_non_author_providers_required')
    root = Path(root).resolve()
    sources = {}
    total = 0
    for name, sha in files.items():
        _require(safe_path(name) == name, 'unsafe source path')
        path = root / name
        _require(beneath(path, root) and not any(p.is_symlink() for p in
                 [path, *path.parents] if p != root and beneath(p, root)), 'source escapes root')
        if sha is None:
            missing.append('deleted_source_context_unavailable:' + name)
            if path.exists():
                missing.append('stale_source:' + name)
            continue
        _require(re.fullmatch('[0-9a-f]{64}', str(sha)), 'invalid source digest')
        if not path.is_file() or path.stat().st_size > 2_000_000:
            missing.append('unavailable_source:' + name)
            continue
        total += path.stat().st_size
        _require(total <= 4_000_000, 'source packet budget exceeded')
        if digest(path) != sha:
            missing.append('stale_source:' + name)
        sources[name] = path.read_text(encoding='utf-8').splitlines()

    def proof(refs, kind=None, constraint=None):
        return [r for ident in refs if (r := ledger.get(ident)) and _proven(r)
                and r.get('alternative_sha256') == identity
                and (kind is None or r['kind'] == kind)
                and (constraint is None or r.get('constraint') == constraint)]

    preflight = candidate.get('preflight', {})
    required = ['reuse_search', 'module_placement']
    if candidate['risk'] != 'low':
        required.append('implementation_plan')
    for check in required:
        if not proof([preflight.get(check)], 'constraint', check):
            missing.append('preflight:' + check)
    qa = candidate.get('required_qa')
    _require(isinstance(qa, list) and qa and all(isinstance(x, str) for x in qa), 'essential QA undeclared')
    for ident in qa:
        receipt = ledger.get(ident)
        if not receipt or receipt.get('kind') != 'qa' or not receipt.get('executed'):
            missing.append('qa:' + ident)
        elif receipt.get('alternative_sha256') != identity:
            missing.append('stale_qa:' + ident)
        elif not receipt.get('passed'):
            changes.append('failed_qa:' + ident)
    _require(isinstance(reviews, list) and len(reviews) <= 3, 'review envelopes excessive')
    seen = set()
    findings = []
    for env in reviews:
        agent = env.get('effective_agent')
        if agent in authors:
            blockers.append('self_review:' + str(agent))
            continue
        if agent not in expected_reviewers or env.get('requested_agent') != agent or agent in seen:
            blockers.append('duplicate_or_substituted_reviewer')
            continue
        seen.add(agent)
        response = env.get('response')
        validate_schema(response, response_schema())
        if response['candidate_sha256'] != identity:
            missing.append('stale_review:' + agent)
            continue
        attempts = proof([env.get('attempt_ref')], 'constraint', 'review_transport')
        if not any(r.get('reviewer') == agent and r.get('response_sha256') == _hash(response)
                   and r.get('phase') == 'independent_code_review' for r in attempts):
            missing.append('unverified_reviewer:' + agent)
            continue
        if set(response['reviewed_files']) != set(files):
            missing.append('incomplete_review_scope:' + agent)
        for key, challenge in response['challenges'].items():
            if challenge['status'] == 'needs_evidence' or not proof(challenge['evidence_refs']):
                missing.append(agent + ':' + key)
            elif challenge['status'] == 'fail':
                changes.append(agent + ':' + key)
        if response['decision'] == 'blocked':
            blockers.append('reviewer_blocked:' + agent)
        elif response['decision'] == 'changes_requested':
            changes.append('reviewer_changes:' + agent)
        elif response['decision'] == 'needs_evidence':
            missing.append('reviewer_evidence:' + agent)
        ids = set()
        for objection in response['objections']:
            key = agent + ':' + objection['id']
            _require(key not in ids, 'duplicate objection ID within reviewer')
            ids.add(key)
            _require(bool(proof(objection['evidence_refs'])), 'objection without scoped evidence')
            for site in objection['sites']:
                lines = sources.get(site['file'], [])
                _require(type(site['start']) is int and type(site['end']) is int and
                         1 <= site['start'] <= site['end'] <= len(lines), 'invalid cited location')
                _require(site['function'] == '<module>' or
                         site['function'] in '\n'.join(lines[site['start'] - 1:site['end']]),
                         'cited function absent from range')
            if objection['challenge'] == 'duplication':
                _require(objection['duplication_kind'] != 'not_applicable' and
                         len({(s['file'], s['function'], s['start'], s['end']) for s in objection['sites']}) >= 2,
                         'duplication needs two concrete implementations')
            defended = any(a.get('reviewer') == agent and a.get('objection_id') == objection['id']
                           and a.get('action') in ('accept', 'refute', 'alternative', 'request_evidence')
                           for a in answers)
            closed = defended and any(r['kind'] == 'resolution' and _proven(r)
                        and r.get('alternative_sha256') == identity and r.get('subject') == key
                        and key in r.get('resolves', []) and r.get('confirmed_by') == agent
                        for r in ledger.values())
            if objection['severity'] == 'MEDIUM' and not defended:
                missing.append('unanswered_objection:' + key)
            # Neither author answer nor status supplied by a model can close a finding.
            findings.append({'id': key, 'severity': objection['severity'], 'closed': closed})
            if not closed and objection['severity'] == 'BLOCKER':
                blockers.append(key)
            elif not closed and objection['severity'] == 'HIGH':
                changes.append(key)
    missing.extend('missing_reviewer:' + a for a in sorted(expected_reviewers - seen))
    state = ('blocked' if blockers else 'changes_requested' if changes else
             'needs_evidence' if missing else 'approved_for_authorization')
    return {'state': state, 'candidate_sha256': identity, 'findings': findings,
            'blockers': blockers, 'changes': changes, 'missing_evidence': missing,
            'implementation_allowed': False, 'production_authorized': False,
            'activation_allowed': False, 'scope': 'Optional controller review gate only'}
