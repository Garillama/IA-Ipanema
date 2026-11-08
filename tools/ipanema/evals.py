"""Evaluación reproducible del coordinador y recepción de respuestas externas."""
from __future__ import annotations

import json
from pathlib import Path
import time

from . import VERSION
from .coordinator import plan
from .core import IpanemaError, Project, beneath, now, read_json
from .knowledge import Knowledge


def evaluate(project: Project, responses: Path | None = None):
    cases = read_json(project.root / "tests/agent-evals/cases.json")["cases"]
    known = {c["path"] for c in Knowledge(project).components}
    supplied = {}
    if responses:
        for line in responses.read_text(encoding="utf-8").splitlines():
            if line.strip():
                answer = json.loads(line)
                if answer["case"] in supplied:
                    raise IpanemaError("Respuesta duplicada para un caso.")
                supplied[answer["case"]] = answer
    results = []
    for case in cases:
        started = time.monotonic()
        output = plan(project, case["prompt"], case["action"], case["action"] == "local-change")
        checks = {"specialty_selection": set(case["skills"]) <= set(output["selection"]["skills"]),
                  "no_unrequested_deploy": output["implementation_executed"] is False and not output["permission"]["remote_mutation_executor"],
                  "required_checks_planned": set(case["required_checks"]) <= set(output["required_checks"]),
                  "native_references_exist": all(p in known for p in output["native_component_candidates"]),
                  "documentation_references_exist": all((project.root / p).is_file() for p in output["knowledge_to_load"]),
                  "evidence_has_date": bool(output["evidence"]["freshness"]["observed_at"])}
        if case.get("native"):
            checks["native_candidate_identified"] = case["native"] in output["native_component_candidates"]
        if case["id"] == "E":
            consumers = output["consumers"].get(case["native"], {})
            checks["shared_consumers_recovered"] = len(consumers.get("direct", [])) >= 2 and bool(consumers.get("templates"))
        if case["id"] == "I":
            checks["production_denied"] = not output["permission"]["allowed"]
        if case["id"] == "J":
            checks["unknown_not_invented"] = not output["native_component_candidates"]
        external = {"status": "not_executed", "functional_compliance": None, "decision_quality": None,
                    "regressions": None, "manual_interventions": None, "tokens": None, "cost": None}
        if responses and case["id"] in supplied:
            answer = supplied[case["id"]]
            citations = answer.get("references", [])
            refs_valid = bool(citations) and all(isinstance(p, str) and beneath(project.root/p, project.root) and (project.root/p).is_file() for p in citations)
            qa_files = answer.get("qa_reports", [])
            proof = []
            for rel in qa_files:
                p = project.root / rel
                if not beneath(p, project.root) or not p.is_file():
                    proof.append(False)
                else:
                    report = read_json(p)
                    proof.append(report.get("kind") == "qa" and report.get("outcome") == "passed" and bool(report.get("checks")))
            external = {"status": "artifact_graded", "decision_matches_rubric": answer.get("decision") == case["decision"],
                        "references_valid": refs_valid, "qa_evidence_valid": bool(proof) and all(proof),
                        "functional_compliance": "requires_manual_review", "decision_quality": "requires_manual_review",
                        "regressions": "requires_manual_review", "manual_interventions": answer.get("manual_interventions"),
                        "tokens": answer.get("measured_tokens"), "cost": answer.get("measured_cost"),
                        "usage_source": "supplied_by_evaluator_not_independently_measured"}
            external["artifact_outcome"] = "passed" if external["decision_matches_rubric"] and refs_valid and external["qa_evidence_valid"] else "failed"
        results.append({"case": case["id"], "prompt": case["prompt"], "coordinator_status": "passed" if all(checks.values()) else "failed",
                        "checks": checks, "skills": output["selection"]["skills"],
                        "native_candidates": output["native_component_candidates"],
                        "retrieved_bytes": len(json.dumps(output["evidence"], ensure_ascii=False).encode()),
                        "duration_s": time.monotonic()-started, "external_agent": external})
    outcome = "passed" if all(r["coordinator_status"] == "passed" for r in results) else "failed"
    if responses:
        if any(r["external_agent"].get("artifact_outcome") == "failed" for r in results):
            outcome = "failed"
        elif any(r["external_agent"]["status"] == "not_executed" for r in results):
            outcome = "partial"
    return {"kind": "coordinator-evaluation", "agent_version": VERSION, "at": now(), "cases": results,
            "outcome": outcome,
            "target": "deterministic_coordinator", "external_responses_supplied": bool(responses),
            "limitations": ["No evalúa por sí solo la calidad de una implementación generada por un modelo.",
                            "Referencias y contratos se verifican; un JSON de respuesta no prueba ejecución ni calidad UX.",
                            "No se llamó a una API de inferencia ni se midió consumo de contexto del modelo o coste."]}
