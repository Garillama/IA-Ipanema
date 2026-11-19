from pathlib import Path
from types import SimpleNamespace
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[5]
SNAPSHOT = Path(__file__).resolve().parents[1] / 'logical-review-snapshot'
ALLOWED = ['sections/hero.tpl', 'snippets/image.tpl']
EXPECTED = {
    'sections/hero.tpl': '1e70c54c4c5bc38711272284843d8881c4354ac7725e9de56c0223b599c3e65d',
    'snippets/image.tpl': 'e4e622e0c561c4450138e7717a1e5af95cf19d0184aee5cbcb89990f7ada767e',
}
sys.path.insert(0, str(ROOT / 'tools'))
from ipanema.core import IpanemaError
from ipanema.orchestration.council import _files, validate_objections
from ipanema.orchestration.council_runtime import binding
from ipanema.orchestration.engine import validate_response

sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
checks = []
assert {f: sha(SNAPSHOT / f) for f in ALLOWED} == EXPECTED
checks.append('logical paths contain the exact corrected file hashes')
assert _files(ALLOWED, ALLOWED) == ALLOWED
checks.append('candidate citations with logical names are accepted')
try:
    _files(['sections/hero.tpl', 'static/js/store.js'], ALLOWED)
except IpanemaError:
    checks.append('out-of-scope file citation is rejected')
else:
    raise AssertionError('out-of-scope citation unexpectedly accepted')
plan = {
    'allowed_files': ALLOWED,
    'objective': 'synthetic logical-path preflight only',
    'council_required_constraints': ['responsive'],
    'council': {'max_rounds': 2, 'require_defense': True},
}
context = binding(SimpleNamespace(id='rhino-performance'), plan, SNAPSHOT, Path('synthetic-run'))
assert context['files'] == EXPECTED
assert context['run_id'] == 'synthetic-run'
checks.append('binding binds both files to their exact hashes and run id')
source_ids = {'source:' + f for f in context['files']}
refs = ['source:sections/hero.tpl', 'source:snippets/image.tpl']
assert set(refs) <= source_ids
objection = {
    'decision': 'changes_requested', 'summary': 'synthetic schema probe only', 'changes': [],
    'preferred_alternative': 'candidate-delta', 'questions': [],
    'objections': [{
        'id': 'O-preflight', 'alternative_id': 'candidate-delta', 'category': 'responsive',
        'severity': 'high', 'claim': 'synthetic objection bound to candidate evidence',
        'status': 'open', 'evidence_refs': refs, 'resolution_evidence_refs': [],
    }],
}
normalized = validate_objections(objection, ALLOWED)
assert normalized['objections'][0]['evidence_refs'] == refs
checks.append('synthetic objection can carry controller source ids tied to candidate file hashes')
invalid_ref_objection = {**objection, 'objections': [{**objection['objections'][0], 'evidence_refs': ['invented-evidence-id'] }]}
invalid_ref_result = validate_objections(invalid_ref_objection, ALLOWED)
assert invalid_ref_result['objections'][0]['evidence_refs'] == ['invented-evidence-id']
checks.append('LIMITATION: objection normalizer does not reject evidence refs absent from controller ledger')
try:
    validate_response(
        {'role': 'audit', 'allowed_files': []},
        {'decision': 'changes_requested', 'changes': [{
            'path': 'sections/hero.tpl', 'before_sha256': EXPECTED['sections/hero.tpl'], 'content': 'forbidden'
        }]},
        SNAPSHOT,
    )
except IpanemaError:
    checks.append('read-only audit cannot propose file modifications')
else:
    raise AssertionError('read-only audit write unexpectedly accepted')
# The existing controller requires all read_files to be members of the global plan.allowed_files.
assert 'if any(safe_path(n) not in plan[\'allowed_files\'] for n in task[\'read_files\']+task[\'allowed_files\'])' in (ROOT / 'tools/ipanema/orchestration/engine.py').read_text()
assert 'blocks/slide.tpl' not in ALLOWED
checks.append('read-only dependency source cannot be supplied as read_file while global allowed_files is exactly the two candidates')
result = {
    'kind': 'local-orchestration-contract-preflight',
    'providers_invoked': False,
    'controller_modified': False,
    'allowed_files': ALLOWED,
    'candidate_hashes': EXPECTED,
    'source_binding_sha256': context['source_sha256'],
    'checks': checks,
    'dependency_context': {
        'example_dependency': 'blocks/slide.tpl',
        'readable_under_exact_two_global_allowed_files': False,
        'read_only_tasks_have_write_allowance': [],
        'controller_invariant': 'task read_files and task allowed_files must be members of plan.allowed_files',
    },
    'status': 'candidate_binding_and_out_of_scope_guards_pass; evidence-ref integrity and dependency-source-context blocked',
}
out = Path(__file__).resolve().parents[1] / 'logical-contract-preflight-results.json'
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
