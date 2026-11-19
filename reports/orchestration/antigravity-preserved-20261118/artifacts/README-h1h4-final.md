# IA-Ipanema V3 candidate — H1–H4 corrections

Status: `needs_evidence` (isolated implementation only; no provider execution, integration, or activation).

## Identity and scope

The cumulative baseline is the previously frozen candidate patch `8a0685f35de7391e5f421b202d566c771b5e54d4e46b92a9d4cd08f98c2e43be` (`artifacts/full-candidate.patch` in the preceding candidate). This incremental correction is in a separate working copy and applies only to five files:

- `tools/ipanema/orchestration/models.json`
- `tools/ipanema/orchestration/adapters.py`
- `tools/ipanema/orchestration/engine.py`
- `tests/unit/test_antigravity_integration.py`
- `tests/unit/test_antigravity_json_contract.py`

The base cumulative patch was SHA256-checked before editing. The incremental patch applies cleanly to that exact prior candidate (`git apply --check` passed). No operational controller, Rhino files, credentials, or provider processes were accessed.

## Corrections

### H1 — Keep V2 dual by default

`models.json:council` now names Claude and Codex as the enabled members and leaves Antigravity and CommandCode disabled. Antigravity remains in the model registry with unverified profiles. The mandatory B1/B2 and model/tool-readiness blockers remain. The engine also preflights all required runtime binaries before central QA or workers when an explicitly configured multi-agent policy is ever presented. With current B1/B2 unresolved, any triad execution is rejected before QA/provider startup. No automatic V2-to-triad policy change was introduced.

### H2 — Explicit prompt-size rejection

The Antigravity adapter retains a 96,000-byte UTF-8 prompt limit. It rejects empty or over-limit prompts before a worker starts; it neither truncates nor silently splits. This is intentionally narrower than the controller's 300 KB serialized source-context ceiling, so a task can be accepted by generic planning and then safely rejected by the Antigravity adapter. Claude and Codex limits are unchanged. The documented `stream-json` input route is not substituted because it changes the output format and requires a distinct parser contract.

### H3 — Schema-required roles

Antigravity is restricted to council proposal, objection, and defense roles, each of which has a controller JSON Schema. The worker rejects all other Antigravity roles. The adapter refuses a missing schema and has no free-text-to-approval fallback. Claude and Codex parsing and role contracts remain unchanged.

### H4 — Strict JSON envelope

The Antigravity parser requires a successful documented JSON envelope, validates field types and token counters, rejects duplicate JSON keys and non-finite constants, rejects failure/cancelled/nonterminal statuses and success envelopes containing `error`, requires schema-bound `structured_output`, verifies the echoed schema, checks response/structured-output agreement, validates the payload, and rejects reserved identity claims. It does not derive identity from provider output or grant integration/publication permission.

The required envelope fields follow the documented JSON output shape. `error` is treated as failure-only; `structured_output` and `json_schema` are required only for schema-enabled calls. Official CLI reference: [Antigravity CLI headless mode](https://antigravity.google/docs/cli/headless/).

## Focused verification

Executed once after the final edits:

```text
PYTHONPATH=tools python3 -m py_compile \
  tools/ipanema/orchestration/adapters.py \
  tools/ipanema/orchestration/engine.py \
  tests/unit/test_antigravity_json_contract.py \
  tests/unit/test_antigravity_integration.py

PYTHONPATH=tools python3 -m unittest -v \
  tests.unit.test_antigravity_json_contract \
  tests.unit.test_antigravity_integration.AntigravityAdapterTests.test_registry_and_profiles_are_separate_from_runtime_readiness \
  tests.unit.test_antigravity_integration.AntigravityAdapterTests.test_cli_argv_uses_only_help_documented_interface_and_closed_json \
  tests.unit.test_antigravity_integration.AntigravityAdapterTests.test_output_parser_accepts_only_direct_structured_json_and_rejects_unknown_envelopes \
  tests.unit.test_antigravity_integration.AntigravityAdapterTests.test_three_agent_policy_and_cross_review_route_without_self_review \
  tests.unit.test_antigravity_integration.AntigravityAdapterTests.test_three_agent_execution_stops_before_qa_or_any_worker \
  tests.unit.test_antigravity_integration.AntigravityAdapterTests.test_readonly_and_dual_v2_policy_contract_remain_representable \
  tests.unit.test_antigravity_integration.AntigravityAdapterTests.test_mocked_three_agent_council_runs_independent_proposals_debate_and_defense

Result: 22 tests passed. `git diff --check`: passed.
```

The tests are local/synthetic. The L3/L4 fixture proves default plans keep `required_agents=[claude,codex]`; the triad blocker fixture proves B1/B2 reject before `central_qa` or `run_council`; an additional mocked readiness test proves missing triad runtime detection occurs before QA. These are controller tests, not evidence that Antigravity is secure or operable against a real provider.

Prompt boundary fixtures cover 95,999, 96,000, and 96,001 UTF-8 bytes, plus multibyte input exceeding the byte cap. They call only the argv builder with synthetic runtime/path stubs; they do not invoke `agy`.

## Remaining blockers and risks

- B1 remains: credential separation for the CLI identity is not proven.
- B2 remains: destination-specific egress control is not proven.
- Model/account availability and real provider envelope are still unverified.
- Tool and subagent disablement is not independently proven.
- No provider was invoked, and no Antigravity execution is authorized by this candidate.
- The 96 KB cap can reject a valid council prompt whose serialized context is larger; this is explicit/fail-closed and does not affect Claude/Codex.
- A future triad requires an explicit policy change, all required runtimes, and separate human authorization; passing synthetic tests is not activation permission.

## Integration and rollback

Do not copy this patch to the operational controller as part of this task. For a future authorized integration, first preserve the current operational files and hashes, apply the incremental patch to the exact `8a0685f...` candidate, review the resulting diff and run the focused checks. Roll back only by restoring the exact pre-integration versions of the five listed files after verifying their hashes and ensuring no later edits conflict. Do not activate Antigravity or clear B1/B2 as part of that operation.
