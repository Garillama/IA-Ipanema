"""Hallazgos, propuestas y soluciones verificadas tienen estados distintos."""
from __future__ import annotations

from pathlib import Path

from .core import IpanemaError, Project, agent_fingerprint, beneath, digest, now, read_json, reject_secrets, write_json
from . import VERSION


def effective_solutions(project: Project, query=""):
    from .knowledge import normal, query_terms
    registry = project.root / "reusable/solutions.json"
    if not registry.is_file():
        return []
    entries = read_json(registry)["solutions"]
    result = []
    words = query_terms(query)
    for entry in entries:
        if words and not any(w in normal(str(entry)) for w in words):
            continue
        reasons = []
        if entry["status"] == "verified":
            if entry["agent_version"] != VERSION:
                reasons.append("Cambió la versión del agente.")
            if entry.get("agent_fingerprint") != agent_fingerprint(project.root):
                reasons.append("Cambió la implementación o instrucciones del agente.")
            base = project.root if entry["scope"] == "workspace" else project.theme_root
            if entry["scope"] == "theme" and entry["project"] != project.id:
                reasons.append("Compatibilidad con otra tienda no comprobada.")
            if entry["scope"] == "theme":
                keys = ("theme", "version", "variant", "forked")
                previous = entry.get("remote_version_observation") or {}
                current = project.data.get("remote_observation") or {}
                if any(previous.get(k) != current.get(k) for k in keys) or entry.get("theme_installation_id") != project.data.get("theme_installation_id"):
                    reasons.append("Cambió la instalación o versión observada del tema.")
            for rel, sha in entry["source_hashes"].items():
                p = base / rel if base else None
                if not p or not p.is_file() or digest(p) != sha:
                    reasons.append("Cambió o no está disponible: " + rel)
            for evidence in entry["evidence"]:
                p = project.root / evidence["path"]
                if not beneath(p, project.root) or not p.is_file() or digest(p) != evidence["sha256"]:
                    reasons.append("Evidencia ausente o modificada.")
        result.append({**entry, "effective_status": "requires_revalidation" if reasons else entry["status"],
                       "revalidation_reasons": reasons})
    return result


def register(project: Project, entry: dict, evidence: list[Path]):
    reject_secrets(entry)
    required = {"id", "problem", "context", "component", "files", "cause", "solution", "tests", "results",
                "limitations", "risks", "compatibility", "reuse", "scope"}
    if required - entry.keys() or not entry["files"] or entry["scope"] not in ("theme", "workspace"):
        raise IpanemaError("Solución incompleta; usa el contrato de reusable/README.md.")
    if not evidence:
        raise IpanemaError("Una propuesta sin evidencia no se registra como verificada.")
    proofs = []
    for path in evidence:
        if not beneath(path, project.root):
            raise IpanemaError("Guarda el reporte QA dentro del repositorio antes de registrarlo.")
        result = read_json(path)
        if result.get("kind") != "qa" or result.get("outcome") != "passed" or not result.get("checks"):
            raise IpanemaError("Evidencia QA insuficiente o con fallos.")
        proofs.append({"path": str(path.resolve().relative_to(project.root)), "sha256": digest(path)})
    base = project.root if entry["scope"] == "workspace" else project.require_theme()
    hashes = {}
    for relative in entry["files"]:
        path = base / relative
        if not beneath(path, base) or not path.is_file():
            raise IpanemaError("Archivo de solución inexistente o fuera de alcance.")
        hashes[relative] = digest(path)
    for proof in proofs:
        report = read_json(project.root / proof["path"])
        state = report.get("verification_state", {}).get(entry["scope"], {})
        if any(state.get(rel) != sha for rel, sha in hashes.items()):
            raise IpanemaError("La evidencia no cubre la versión actual de los archivos de la solución.")
    record = {**entry, "status": "verified", "agent_version": VERSION, "agent_fingerprint": agent_fingerprint(project.root), "project": project.id,
              "theme_installation_id": project.data.get("theme_installation_id"),
              "at": now(), "source_hashes": hashes, "evidence": proofs,
              "remote_version_observation": project.data.get("remote_observation")}
    registry = project.root / "reusable/solutions.json"
    data = read_json(registry) if registry.exists() else {"schema_version": 1, "solutions": []}
    if any(s["id"] == entry["id"] for s in data["solutions"]):
        raise IpanemaError("ID ya registrado; usa una revisión nueva y conserva su historia.")
    data["solutions"].append(record)
    write_json(registry, data, overwrite=registry.exists())
    return record
