"""Valida repositorio y, si está disponible, integridad del tema configurado."""
from __future__ import annotations

from pathlib import Path
import re
import subprocess
from urllib.parse import unquote

from .core import IpanemaError, Project, beneath, digest, read_json, reject_secrets


def validate(project: Project, *, strict_source=False):
    root, doc = project.root, project.knowledge_root
    base = doc / "13-evidence/measurements/source-baseline"
    errors, warnings = [], []
    summary = read_json(base / "source-summary.json")
    files = read_json(base / "source-inventory.json")
    checked, unchanged, unavailable_links, links = 0, 0, 0, 0
    theme = project.theme_root
    source_status = "not_configured"
    if theme:
        try:
            project.require_theme()
            source_status = "checked"
            for entry in files:
                path = theme / entry["path"]
                checked += 1
                if not beneath(path, theme) or not path.is_file():
                    (errors if strict_source else warnings).append("Archivo de origen ausente/fuera del tema: " + entry["path"])
                elif digest(path) != entry["sha256"]:
                    (errors if strict_source else warnings).append("Origen cambió desde baseline: " + entry["path"])
                else:
                    unchanged += 1
            if (theme / ".git").exists():
                try:
                    status = subprocess.run(["git", "-C", str(theme), "status", "--porcelain=v1"], capture_output=True, text=True)
                    if status.returncode or status.stdout:
                        warnings.append("El tema tiene cambios o Git no pudo comprobarse; se conservaron.")
                except FileNotFoundError:
                    warnings.append("Git no está instalado; hashes comprobados sin estado Git.")
        except IpanemaError as exc:
            source_status = "unavailable"
            (errors if strict_source else warnings).append(str(exc))
    elif strict_source:
        errors.append("La verificación estricta requiere configurar el tema.")
    else:
        warnings.append("Tema sin configurar: no se acredita integridad del origen; sí se valida el repositorio.")
    managed_json = [*doc.rglob("*.json"), *(root / "projects").glob("*.json"),
                    *(root / "reusable").rglob("*.json"), *(root / "tests/agent-evals").glob("*.json"),
                    *(root / "tools/ipanema/seo").glob("*.json")]
    for path in managed_json:
        try:
            value = read_json(path)
            if path.parent == root / "projects":
                reject_secrets(value)
                if not path.name.endswith(".local.json") and isinstance(value, dict) and value.get("theme_root"):
                    if Path(value["theme_root"]).is_absolute():
                        errors.append("Ruta personal en configuración compartida: " + path.name)
        except IpanemaError as exc:
            errors.append(str(exc))
    managed_md = [root / "README.md", root / "AGENTS.md", *doc.rglob("*.md"),
                  *(root / ".agents/skills").rglob("*.md"), *(root / "projects").glob("*.md"),
                  *(root / "reusable").rglob("*.md"), *(root / "reports/v2").glob("*.md"), *(root / "reports/seo").rglob("*.md")]
    for path in managed_md:
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            errors.append("Markdown vacío: " + str(path.relative_to(root)))
        for match in re.finditer(r"(?<!!)\[[^\]]+\]\((<[^>]+>|[^\s)]+)\)", text):
            raw = match.group(1).strip("<>")
            if re.match(r"^[a-zA-Z]+://|^mailto:|^app:", raw):
                continue
            raw, _, anchor = raw.partition("#")
            raw = unquote(raw)
            line = None
            m = re.search(r":(\d+)$", raw)
            if m:
                line, raw = int(m[1]), raw[:m.start()]
            external = Path(raw).is_absolute() and not beneath(Path(raw), root)
            links += 1
            if external:
                unavailable_links += not Path(raw).is_file()
                continue
            destination = (path.parent / raw).resolve() if raw else path.resolve()
            if not destination.exists():
                errors.append(f"Enlace roto {path.relative_to(root)} -> {raw}")
                continue
            if line and destination.is_file():
                try:
                    if line > len(destination.read_text(encoding="utf-8").splitlines()):
                        errors.append("Línea inexistente: " + raw)
                except UnicodeDecodeError:
                    errors.append("Referencia de línea a un binario: " + raw)
            if anchor and destination.suffix == ".md":
                content = destination.read_text(encoding="utf-8")
                headings = [re.sub(r"[^\w\- ]", "", h.lower()).replace(" ", "-")
                            for h in re.findall(r"^#+\s+(.+)$", content, re.M)]
                if f'id="{anchor}"' not in content and anchor not in headings:
                    errors.append("Ancla no encontrada: " + raw + "#" + anchor)
    components = read_json(base / "components.json")
    sheets = list((doc / "02-native-components/specifications").glob("*.md"))
    if len(sheets) != len(components):
        errors.append("Número de fichas diferente al inventario.")
    settings = read_json(base / "settings.json")
    if len(settings) != summary["settings"]:
        errors.append("Número de settings inconsistente.")
    skills = list((root / ".agents/skills").glob("*/SKILL.md"))
    for path in skills:
        text = path.read_text(encoding="utf-8")
        if not re.search(r"\A---\nname: " + re.escape(path.parent.name) + r"\n", text):
            errors.append("Frontmatter/name inválido: " + path.parent.name)
        if not re.search(r"^description: .+", text, re.M):
            errors.append("Skill sin descripción: " + path.parent.name)
    return {"source_status": source_status, "source_files_unchanged": unchanged, "source_files_checked": checked,
            "markdown_links_checked": links, "historical_external_links_unavailable": unavailable_links,
            "component_sheets": len(sheets), "settings": len(settings), "skills": len(skills),
            "errors": errors, "warnings": warnings}
