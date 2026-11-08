"""Intentos locales acotados con backups privados y detección de conflictos."""
from __future__ import annotations

import base64
from pathlib import Path
import re
import uuid

from .core import IpanemaError, Project, beneath, digest, now, read_json, write_json


def target(scope: Path, relative: str) -> Path:
    p = Path(relative)
    if p.is_absolute() or ".." in p.parts or not p.parts:
        raise IpanemaError("El archivo del intento debe ser relativo y permanecer dentro del alcance.")
    if any(part in (".git", ".local", ".nuvem", "node_modules") or part.startswith(".env") or part.endswith(".local.json") for part in p.parts):
        raise IpanemaError("El intento no puede incluir credenciales, metadatos Git o dependencias.")
    result = scope / p
    if not beneath(result, scope) or any(q.is_symlink() for q in [result, *result.parents] if beneath(q, scope)):
        raise IpanemaError("No se permiten enlaces simbólicos ni escapes del alcance.")
    if result.exists() and not result.is_file():
        raise IpanemaError("El destino no es un archivo.")
    return result


def begin(project: Project, files: list[str], *, scope="theme", max_attempts=2, authorized=False):
    if not authorized:
        raise IpanemaError("El intento requiere implementación local expresamente autorizada.")
    if not 1 <= max_attempts <= 5 or not files or len(set(files)) != len(files):
        raise IpanemaError("Declara archivos únicos y un máximo entre 1 y 5 intentos.")
    root = project.require_theme() if scope == "theme" else project.root
    entries = {}
    for name in files:
        path = target(root, name)
        content = path.read_bytes() if path.exists() else None
        if content and len(content) > 2_000_000:
            raise IpanemaError("Archivo demasiado grande para una transacción local.")
        entries[name] = {"before_sha256": digest(path) if path.exists() else None,
                         "before_base64": base64.b64encode(content).decode() if content is not None else None,
                         "before_mode": path.stat().st_mode & 0o777 if path.exists() else None}
    transaction = {"id": uuid.uuid4().hex, "project": project.id, "scope": str(root), "scope_kind": scope,
                   "at": now(), "status": "open", "max_attempts": max_attempts, "attempts": 0,
                   "files": entries, "history": []}
    path = project.root / "reports/transactions" / (transaction["id"] + ".json")
    write_json(path, transaction)
    path.chmod(0o600)
    return {k: v for k, v in transaction.items() if k != "files"}


def load(project: Project, transaction_id: str):
    if not re.fullmatch(r"[a-f0-9]{32}", transaction_id):
        raise IpanemaError("Identificador de intento inválido.")
    path = project.root / "reports/transactions" / (transaction_id + ".json")
    data = read_json(path)
    if data["project"] != project.id:
        raise IpanemaError("El intento pertenece a otro proyecto.")
    expected = project.root if data["scope_kind"] == "workspace" else project.require_theme()
    if expected.resolve() != Path(data["scope"]).resolve():
        raise IpanemaError("El alcance cambió desde el inicio del intento.")
    return path, data


def apply(project: Project, transaction_id: str, patches: dict[str, str]):
    path, data = load(project, transaction_id)
    if data["status"] not in ("open", "reverted") or data["attempts"] >= data["max_attempts"]:
        raise IpanemaError("Intento cerrado o límite de correcciones alcanzado.")
    if not patches or set(patches) - set(data["files"]) or any(not isinstance(v, str) for v in patches.values()):
        raise IpanemaError("El patch debe contener texto solo para los archivos declarados.")
    scope = Path(data["scope"])
    for name in patches:
        p = target(scope, name)
        current = digest(p) if p.exists() else None
        if current != data["files"][name]["before_sha256"]:
            raise IpanemaError(f"Conflicto antes de aplicar: {name}. Se conservan los cambios existentes.")
    written = []
    try:
        for name, content in patches.items():
            p = target(scope, name)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
            written.append(name)
            data["files"][name]["after_sha256"] = digest(p)
    except OSError:
        for name in written:
            restore(target(scope, name), data["files"][name])
        raise
    data["attempts"] += 1
    data["status"] = "applied"
    data["history"].append({"at": now(), "action": "apply", "files": list(patches), "attempt": data["attempts"]})
    write_json(path, data, overwrite=True)
    path.chmod(0o600)
    return {"id": transaction_id, "status": data["status"], "attempt": data["attempts"], "files": list(patches)}


def restore(path: Path, entry: dict):
    if entry["before_base64"] is None:
        path.unlink(missing_ok=True)
    else:
        path.write_bytes(base64.b64decode(entry["before_base64"]))
        path.chmod(entry["before_mode"])


def finish(project: Project, transaction_id: str, *, accept=False, evidence: Path | None = None, baseline: Path | None = None):
    path, data = load(project, transaction_id)
    if data["status"] != "applied":
        raise IpanemaError("No hay un cambio propio aplicado que finalizar.")
    scope = Path(data["scope"])
    changed = [(name, entry) for name, entry in data["files"].items() if "after_sha256" in entry]
    for name, entry in changed:
        p = target(scope, name)
        if not p.is_file() or digest(p) != entry["after_sha256"]:
            raise IpanemaError(f"Conflicto posterior: {name}. No se acepta ni revierte ningún archivo.")
    if accept:
        if evidence is None:
            raise IpanemaError("Aceptar requiere un reporte QA ejecutado, posterior al cambio y sin fallos.")
        proof = read_json(evidence)
        if proof.get("kind") != "qa" or proof.get("outcome") != "passed" or not proof.get("checks"):
            raise IpanemaError("La evidencia no acredita pruebas QA aprobadas.")
        if proof.get("project") != project.id or any(c.get("status") != "passed" for c in proof["checks"]):
            raise IpanemaError("La evidencia pertenece a otro proyecto o contiene pruebas sin aprobar.")
        state = proof.get("verification_state", {}).get(data["scope_kind"], {})
        if any(state.get(name) != entry["after_sha256"] for name, entry in changed):
            raise IpanemaError("El QA no acredita los hashes de los archivos modificados.")
        if proof.get("at", "") < data["history"][-1]["at"]:
            raise IpanemaError("La evidencia es anterior al intento.")
        if baseline is None:
            raise IpanemaError("La autocorrección requiere un baseline QA del fallo para comparar resultados.")
        previous = read_json(baseline)
        failed_before = {c.get("name") for c in previous.get("checks", []) if c.get("status") == "failed"}
        passed_after = {c.get("name") for c in proof["checks"] if c.get("status") == "passed"}
        if previous.get("kind") != "qa" or previous.get("project") != project.id or not failed_before or not failed_before <= passed_after:
            raise IpanemaError("La comparación no demuestra que las pruebas fallidas anteriores ahora pasen.")
        if previous.get("at", "") > data["history"][-1]["at"]:
            raise IpanemaError("El baseline del fallo debe ser anterior a la corrección.")
        data["baseline"] = {"path": str(baseline.resolve()), "sha256": digest(baseline)}
        data["evidence"] = {"path": str(evidence.resolve()), "sha256": digest(evidence)}
        data["status"] = "accepted"
    else:
        for name, entry in changed:
            restore(target(scope, name), entry)
            entry.pop("after_sha256", None)
        data["status"] = "reverted"
    data["history"].append({"at": now(), "action": data["status"]})
    write_json(path, data, overwrite=True)
    path.chmod(0o600)
    return {"id": transaction_id, "status": data["status"], "attempt": data["attempts"], "max_attempts": data["max_attempts"]}
