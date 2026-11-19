#!/usr/bin/env python3
"""Read-only audit: reviewer evidence refs must exist in the same run ledger/binding."""
import argparse
import json
from pathlib import Path


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def walk_refs(value, path=""):
    if isinstance(value, dict):
        for key, child in value.items():
            current = f"{path}/{key}"
            if key.endswith("evidence_refs") and isinstance(child, list):
                for index, reference in enumerate(child):
                    yield f"{current}/{index}", reference if isinstance(reference, str) else None
            elif key.endswith("evidence_ref"):
                yield current, child if isinstance(child, str) else None
            yield from walk_refs(child, current)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_refs(child, f"{path}/{index}")


def audit(run_dir):
    council_dir = run_dir / "council"
    context = load(council_dir / "context.json")
    binding = context.get("source_binding")
    ledger = load(council_dir / "evidence.json")
    ids = [row.get("id") for row in ledger if isinstance(row, dict)]
    known = set(ids)
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    mismatches = [row.get("id") for row in ledger if row.get("context") != binding]
    references = []
    for path in sorted(council_dir.glob("*.json")):
        if path.name in {"context.json", "evidence.json"}:
            continue
        try:
            document = load(path)
        except (OSError, ValueError):
            continue
        for pointer, reference in walk_refs(document):
            references.append({"file": path.name, "pointer": pointer, "id": reference,
                               "known": isinstance(reference, str) and reference in known})
    unknown = [item for item in references if not item["known"]]
    passed = isinstance(binding, dict) and not duplicates and not mismatches and not unknown
    return {
        "kind": "controller-evidence-reference-audit",
        "run_id": binding.get("run_id") if isinstance(binding, dict) else None,
        "binding_present": isinstance(binding, dict),
        "ledger_entries": len(ledger), "unique_ids": len(known),
        "duplicate_ids": duplicates, "ledger_binding_mismatches": mismatches,
        "reviewer_reference_count": len(references),
        "unknown_or_malformed_references": unknown,
        "status": "pass_for_this_recorded_run" if passed else "reject",
        "scope_note": "Audits only this persisted run; it does not enforce validation inside the active orchestration route."
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit(args.run_dir)
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    raise SystemExit(0 if result["status"] == "pass_for_this_recorded_run" else 2)


if __name__ == "__main__":
    main()
