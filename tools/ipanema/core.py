"""Configuración portable, archivos de evidencia y límites comunes (stdlib)."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import uuid
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


class IpanemaError(ValueError):
    pass


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise IpanemaError(f"No se puede leer JSON: {path.name} ({type(exc).__name__}).") from exc


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def agent_fingerprint(root: Path) -> str:
    paths = [*root.joinpath("tools").rglob("*.py"), *root.joinpath("tools").glob("*.mjs"),
             *root.joinpath(".agents/skills").rglob("SKILL.md"), root / "AGENTS.md"]
    payload = "\n".join(str(p.relative_to(root)) + ":" + digest(p) for p in sorted(paths) if p.is_file())
    return hashlib.sha256(payload.encode()).hexdigest()


def beneath(path: Path, parent: Path) -> bool:
    return path.resolve() == parent.resolve() or parent.resolve() in path.resolve().parents


def resolve_path(value: str, root: Path) -> Path:
    expanded = os.path.expandvars(os.path.expanduser(value))
    if re.search(r"\$\{|\$[A-Za-z_]", expanded):
        raise IpanemaError("Una ruta usa una variable de entorno sin definir.")
    p = Path(expanded)
    return (p if p.is_absolute() else root / p).resolve()


def check_id(value: str) -> str:
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", value):
        raise IpanemaError("Identificador inválido; usa letras minúsculas, números y guiones.")
    return value


def safe_url(url: str, *, local=True) -> str:
    u = urlsplit(url)
    if not u.hostname or u.username or u.password or u.fragment:
        raise IpanemaError("URL inválida: sin credenciales, fragmentos ni secretos.")
    loopback = u.hostname in ("localhost", "127.0.0.1", "::1")
    if u.scheme != "https" and not (local and loopback and u.scheme == "http"):
        raise IpanemaError("Se requiere HTTPS; HTTP solo para fixtures de loopback.")
    if any(re.search(r"token|secret|auth|session|password|email|phone|api.?key", k, re.I)
           for k, _ in parse_qsl(u.query)):
        raise IpanemaError("La URL contiene parámetros confidenciales.")
    return url


def origin(url: str) -> str:
    u = urlsplit(safe_url(url))
    return f"{u.scheme}://{u.netloc}"


def redact(value, *, mask_env=True):
    """No imprimir secretos de configuración/entorno ni consultas sensibles."""
    if isinstance(value, dict):
        return {k: ("[redacted]" if re.search(r"password|cookie|authorization|access.?token|api.?key|secret", k, re.I)
                    and not k.endswith("_env") else redact(v, mask_env=mask_env or k in {"error", "stdout", "stderr", "objective", "request", "prompt"})) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v, mask_env=mask_env) for v in value]
    if isinstance(value, str):
        for k, v in os.environ.items():
            if mask_env and len(v) >= 6 and re.search(r"PASSWORD|SECRET|TOKEN|API_KEY", k):
                value = value.replace(v, "[redacted]")
        if value.startswith(("http://", "https://")):
            u = urlsplit(value)
            host = u.netloc.rsplit("@", 1)[-1]
            query = [(k, "[redacted]" if re.search(r"token|key|secret|auth|session|email|phone|password", k, re.I) else v)
                     for k, v in parse_qsl(u.query)]
            value = urlunsplit((u.scheme, host, u.path, urlencode(query), ""))
        return value
    return value


def write_json(path: Path, data, *, overwrite=False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(redact(data, mask_env=False), ensure_ascii=False, indent=2) + "\n"
    if not overwrite:
        with path.open("x", encoding="utf-8") as f:
            f.write(payload)
    else:
        temporary = path.with_name(path.name + ".tmp-" + uuid.uuid4().hex)
        try:
            temporary.write_text(payload, encoding="utf-8")
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)


def reject_secrets(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if re.search(r"password|cookie|access.?token|authorization|secret|api.?key", key, re.I) and not key.endswith("_env"):
                if value not in (None, "", False):
                    raise IpanemaError("No guardes credenciales en la configuración de proyectos.")
            reject_secrets(value)
    elif isinstance(data, list):
        for value in data:
            reject_secrets(value)


class Project:
    def __init__(self, root: Path | None = None, project_id: str | None = None):
        self.root = (root or repo_root()).resolve()
        registry = read_json(self.root / "projects/registry.json")
        if registry.get("schema_version") != 2 or not isinstance(registry.get("projects"), dict):
            raise IpanemaError("Registro de proyectos incompatible; consulta projects/README.md.")
        local_path = self.root / ".local/config.json"
        local = read_json(local_path) if local_path.exists() else {}
        self.id = check_id(project_id or os.getenv("IPANEMA_PROJECT") or local.get("active_project") or registry.get("default", ""))
        entry = registry["projects"].get(self.id)
        if not isinstance(entry, str):
            raise IpanemaError(f"Proyecto no registrado: {self.id}.")
        config_path = resolve_path(entry, self.root)
        if not beneath(config_path, self.root / "projects") or config_path.name.endswith(".local.json"):
            raise IpanemaError("El registro debe apuntar a un JSON compartido dentro de projects/.")
        self.data = read_json(config_path)
        if not isinstance(self.data, dict) or self.data.get("id") != self.id or self.data.get("schema_version") != 2:
            raise IpanemaError("Configuración de proyecto incompleta: id/schema_version.")
        override = self.root / "projects" / f"{self.id}.local.json"
        overrides = read_json(override) if override.exists() else {}
        if not isinstance(overrides, dict):
            raise IpanemaError("La configuración local debe ser un objeto JSON.")
        if set(overrides) - {"theme_root", "browser", "qa_base_url"}:
            raise IpanemaError("Override local desconocido; solo theme_root, browser y qa_base_url.")
        self.data = {**self.data, **overrides}
        reject_secrets(self.data)
        raw_theme = os.getenv("IPANEMA_THEME_ROOT") or self.data.get("theme_root")
        self.theme_root = resolve_path(raw_theme, self.root) if raw_theme else None
        self.knowledge_root = resolve_path(self.data.get("discovery_root", "ipanema-discovery"), self.root)
        self.evidence_root = resolve_path(self.data.get("evidence_dir", f"reports/runs/{self.id}"), self.root)
        if not beneath(self.knowledge_root, self.root):
            raise IpanemaError("discovery_root debe estar dentro del repositorio; el tema externo se configura por separado.")
        if beneath(self.root, self.evidence_root) or ".git" in self.evidence_root.parts:
            raise IpanemaError("El directorio de evidencia no puede ser la raíz, un ancestro del repositorio ni .git.")
        if beneath(self.evidence_root, self.knowledge_root):
            raise IpanemaError("La evidencia nueva no debe sobrescribir el discovery histórico.")
        if self.theme_root and (beneath(self.evidence_root, self.theme_root) or beneath(self.theme_root, self.evidence_root)):
            raise IpanemaError("Evidencia y tema deben estar en árboles separados.")
        self.qa = self.data.get("qa", {})
        if not isinstance(self.qa, dict) or not isinstance(self.qa.get("pages", {}), dict):
            raise IpanemaError("qa/pages debe ser un objeto.")
        widths = self.qa.get("widths", [360, 390, 768, 1024, 1440, 1920])
        if not isinstance(widths, list) or not widths or any(type(w) is not int or not 240 <= w <= 3840 for w in widths):
            raise IpanemaError("Anchos QA inválidos (240–3840 px).")
        if self.data.get("public_url"):
            safe_url(self.data["public_url"])
        if self.data.get("qa_base_url"):
            safe_url(self.data["qa_base_url"])

    def require_theme(self) -> Path:
        if not self.theme_root:
            raise IpanemaError(f"Configura theme_root en projects/{self.id}.local.json o IPANEMA_THEME_ROOT.")
        for rel in ("layouts/layout.tpl", "config/settings_schema.json", "templates/pages/home.json"):
            if not (self.theme_root / rel).is_file():
                raise IpanemaError(f"Tema no disponible o incompatible: falta {rel}. No se descargará automáticamente.")
        return self.theme_root

    def new_run(self, label="qa") -> Path:
        path = self.evidence_root / (dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S") + "-" + label + "-" + uuid.uuid4().hex[:8])
        path.mkdir(parents=True, exist_ok=False)
        return path

    def public_status(self):
        return {"project": self.id, "name": self.data.get("name"), "theme_configured": bool(self.theme_root),
                "theme_available": bool(self.theme_root and self.theme_root.is_dir()),
                "environment": self.data.get("environment", "not_configured"),
                "connection": {"status": "not_checked", "remote_observation": self.data.get("remote_observation")},
                "evidence_dir": str(self.evidence_root), "knowledge_root": str(self.knowledge_root)}


def doctor(project: Project):
    dependencies = {k: shutil.which(k) for k in ("git", "node", "npm", "tiendanube")}
    problems, warnings = [], []
    if sys.version_info < (3, 10):
        problems.append("Se requiere Python >= 3.10.")
    try:
        project.require_theme()
    except IpanemaError as exc:
        warnings.append(str(exc))
    if not dependencies["node"]:
        warnings.append("Node no disponible; QA navegador y Lighthouse no se ejecutarán.")
    return {"at": now(), "os": sys.platform, "python": sys.version.split()[0],
            **project.public_status(), "dependencies": {k: bool(v) for k, v in dependencies.items()},
            "errors": problems, "warnings": warnings, "network_performed": False}


def run_command(command: list[str], *, cwd: Path, timeout=120, env=None):
    start = dt.datetime.now(dt.timezone.utc)
    try:
        r = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
        return {"command": command, "exit_code": r.returncode, "stdout": r.stdout[-20000:], "stderr": r.stderr[-4000:],
                "duration_s": (dt.datetime.now(dt.timezone.utc) - start).total_seconds()}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"command": command, "exit_code": 2, "error": type(exc).__name__,
                "duration_s": (dt.datetime.now(dt.timezone.utc) - start).total_seconds()}
