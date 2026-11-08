"""Comando QA único; repo/fixtures offline y storefront con autorización explícita."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import sys
from urllib.parse import urljoin, urlsplit

from . import VERSION
from .core import IpanemaError, Project, digest, now, origin, read_json, run_command, safe_url, write_json
from .evals import evaluate
from .validation import validate


def browser_job(project: Project, run_dir: Path, *, pages=None, full=False, component=None, allow_network=False, lighthouse=False):
    base_url = project.data.get("qa_base_url") or project.data.get("public_url")
    if not base_url:
        raise IpanemaError("Configura public_url o qa_base_url para ejecutar navegador.")
    safe_url(base_url)
    loopback = urlsplit(base_url).hostname in ("localhost", "127.0.0.1", "::1")
    if not loopback and not allow_network:
        raise IpanemaError("QA remoto requiere --allow-network; el QA local no necesita acceso a tiendas.")
    configured = project.qa.get("pages", {})
    selected = pages or list(configured)
    if not selected or len(selected) > project.qa.get("max_pages", 10):
        raise IpanemaError("Selecciona páginas configuradas dentro del máximo permitido.")
    jobs = []
    for name in selected:
        if name not in configured:
            raise IpanemaError("Página no configurada: " + name)
        spec = configured[name]
        spec = {"path": spec} if isinstance(spec, str) else spec
        if not isinstance(spec, dict) or not isinstance(spec.get("path"), str):
            raise IpanemaError("Página incompleta: " + name)
        url = urljoin(base_url, spec["path"])
        if origin(url) != origin(base_url):
            raise IpanemaError("La página debe pertenecer al origen del proyecto.")
        jobs.append({**spec, "name": name, "url": safe_url(url)})
    job = {"project": project.id, "pages": jobs, "output": str(run_dir / "browser"),
           "widths": project.qa.get("widths", [360, 390, 768, 1024, 1440, 1920]) if full else [390, 1440],
           "mode": "full" if full else "quick", "axe": project.qa.get("axe", True),
           "component_selector": component, "interactions": project.qa.get("interactions", []),
           "masks": project.qa.get("visual", {}).get("masks", []), "budgets": project.qa.get("budgets", {}),
           "lighthouse": lighthouse, "capture_seo": True, "coverage": full, "cpu_rate": project.qa.get("cpu_rate"), "network": project.qa.get("network")}
    return job


def execute(project: Project, suite="quick", *, pages=None, component=None, allow_network=False, lighthouse=False):
    # Preparar y validar permisos ANTES de iniciar navegador o crear evidencias.
    needs_browser = suite in ("browser", "page", "component", "full")
    if suite == "component" and not component:
        raise IpanemaError("QA por componente requiere --component con el selector real.")
    if suite == "page" and not pages:
        raise IpanemaError("QA por página requiere --page con una página registrada.")
    if needs_browser:
        browser_job(project, project.evidence_root / "pending", pages=pages, full=suite == "full", component=component, allow_network=allow_network, lighthouse=lighthouse)
    run_dir = project.new_run(suite)
    result = {"kind": "qa", "agent_version": VERSION, "project": project.id, "suite": suite, "at": now(),
              "checks": [], "limitations": [], "remote_mutations_performed": False}
    workspace_files = [*project.root.joinpath("tools").rglob("*.py"), *project.root.joinpath("tools").glob("*.mjs"),
                       *project.root.joinpath(".agents/skills").rglob("SKILL.md"), project.root / "AGENTS.md"]
    workspace_files += [project.root / "README.md", project.root / "package.json"]
    workspace_files += list(project.root.joinpath('tools/ipanema/seo').glob('*.json'))
    workspace_files += [p for p in project.root.joinpath("projects").glob("*.json") if not p.name.endswith(".local.json")]
    workspace_files += list(project.root.joinpath("tests").rglob("*.py"))
    workspace_files += list(project.root.joinpath("reusable").rglob("*.json"))
    workspace_hashes = {str(p.relative_to(project.root)): digest(p) for p in workspace_files if p.is_file()}
    theme_hashes = {}
    if project.theme_root and project.theme_root.is_dir():
        for area in ("layouts", "sections", "blocks", "snippets", "config", "templates", "static", "translations"):
            for p in (project.theme_root / area).rglob("*"):
                if p.is_file() and not p.is_symlink():
                    theme_hashes[str(p.relative_to(project.theme_root))] = digest(p)
        manifest = project.theme_root / "manifest.json"
        if manifest.is_file():
            theme_hashes["manifest.json"] = digest(manifest)
    result["verification_state"] = {"workspace": workspace_hashes, "theme": theme_hashes}
    def record(name, success, details):
        result["checks"].append({"name": name, "status": "passed" if success else "failed", "details": details})
    if suite in ("repo", "quick", "full"):
        validation = validate(project)
        record("repository", not validation["errors"], validation)
    if suite == "source":
        theme = project.require_theme()
        tested = run_command([sys.executable, str(project.root / "tools/audit_source.py"), "--source", str(theme), "--output", str(run_dir / "source")], cwd=project.root)
        summary = read_json(run_dir / "source/source-summary.json") if tested["exit_code"] == 0 else {}
        record("source-schema-inventory", tested["exit_code"] == 0 and not summary.get("json_schema_errors"), tested)
        if tested["exit_code"] == 0:
            inventory = read_json(run_dir / "source/source-inventory.json")
            asset_metrics = {"page": "theme-assets", "profile": "static-uncompressed", "at": now(),
                             "metrics": {"js_bytes": sum(e["bytes"] for e in inventory if e["path"].endswith((".js", ".js.tpl"))),
                                         "css_bytes": sum(e["bytes"] for e in inventory if e["path"].endswith((".css", ".css.tpl")))},
                             "limitations": ["Bytes de archivo sin comprimir; no equivalen a transferencia ni ejecución."]}
            write_json(run_dir / "asset-metrics.json", asset_metrics)
    if suite in ("unit", "quick", "full"):
        command = [sys.executable, "-m", "unittest", "discover", "-s", "tests/unit", "-v"]
        tested = run_command(command, cwd=project.root, timeout=180)
        record("unit-tests", tested["exit_code"] == 0, tested)
    if suite in ("integration", "quick", "full"):
        tested = run_command([sys.executable, "-m", "unittest", "discover", "-s", "tests/integration", "-v"], cwd=project.root, timeout=180)
        record("integration-tests", tested["exit_code"] == 0, tested)
    if suite == "fixtures":
        fixture_env = os.environ.copy()
        fixture_env["IPANEMA_FIXTURE_ARTIFACT_DIR"] = str(run_dir / "fixtures")
        tested = run_command([sys.executable, "-m", "unittest", "discover", "-s", "tests/browser", "-v"], cwd=project.root, timeout=300, env=fixture_env)
        skipped = "skipped=" in tested.get("stderr", "")
        record("browser-fixtures", tested["exit_code"] == 0 and not skipped, tested)
        if skipped:
            result["outcome"] = "blocked"
            result["limitations"].append("Fixtures no ejecutadas por dependencia opcional ausente.")
    if suite in ("evals", "quick", "full"):
        evaluation = evaluate(project)
        write_json(run_dir / "agent-evals.json", evaluation)
        record("coordinator-evals", evaluation["outcome"] == "passed", {"file": "agent-evals.json", "cases": len(evaluation["cases"])})
        result["limitations"].append("Evaluación del coordinador determinista; evaluación externa del modelo no ejecutada.")
    if suite in ('seo', 'quick', 'full'):
        from .seo.evals import evaluate as evaluate_seo
        if suite == 'seo':
            for area in ('unit', 'integration'):
                tested = run_command([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests/' + area, '-p', 'test_seo*.py', '-v'], cwd=project.root, timeout=180)
                record('seo-' + area, tested['exit_code'] == 0, tested)
        seo_evaluation = evaluate_seo()
        write_json(run_dir / 'seo-evals.json', seo_evaluation)
        record('seo-action-evals', seo_evaluation['outcome'] == 'passed', {'file': 'seo-evals.json', 'cases': len(seo_evaluation['cases'])})
        result['limitations'].append('Evaluaciones SEO con fixtures, sin conexión real a cuentas Google.')
    if needs_browser:
        node = shutil.which("node")
        if not node:
            raise IpanemaError("Node no está instalado; no se ejecutó QA de navegador.")
        job = browser_job(project, run_dir, pages=pages, full=suite == "full", component=component, allow_network=allow_network, lighthouse=lighthouse)
        write_json(run_dir / "job.json", job)
        env = os.environ.copy()
        env.update({"IPANEMA_PUBLIC_URL": project.data.get("qa_base_url") or project.data["public_url"],
                    "IPANEMA_ALLOWED_ORIGINS": origin(job["pages"][0]["url"]),
                    "IPANEMA_ALLOW_NETWORK": "1" if allow_network else "0",
                    "IPANEMA_EVIDENCE_DIR": str(run_dir / "browser")})
        if project.theme_root:
            env["IPANEMA_THEME_ROOT"] = str(project.theme_root)
        browser_config = project.data.get("browser", {})
        if browser_config.get("chrome_path"):
            env["IPANEMA_CHROME_PATH"] = browser_config["chrome_path"]
        command = [node, str(project.root / "tools/qa_browser.mjs"), str(run_dir / "job.json")]
        tested = run_command(command, cwd=project.root, timeout=600 if lighthouse else 300, env=env)
        report_path = run_dir / "browser/browser-report.json"
        report = read_json(report_path) if report_path.exists() else {"outcome": "blocked", "error": "Navegador sin reporte final."}
        record("browser", tested["exit_code"] == 0 and report["outcome"] == "passed", {"process": tested, "report": report})
        if report["outcome"] == "blocked":
            result["outcome"] = "blocked"
    stable = all((project.root / rel).is_file() and digest(project.root / rel) == sha for rel, sha in workspace_hashes.items())
    if project.theme_root:
        stable = stable and all((project.theme_root / rel).is_file() and digest(project.theme_root / rel) == sha for rel, sha in theme_hashes.items())
    record("sources-stable-during-qa", stable, {"workspace_files": len(workspace_hashes), "theme_files": len(theme_hashes)})
    result.setdefault("outcome", "passed" if all(c["status"] == "passed" for c in result["checks"]) else "failed")
    result["finished_at"] = now()
    result["report"] = str(run_dir / "report.json")
    write_json(run_dir / "report.json", result)
    return result
