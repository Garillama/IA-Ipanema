#!/usr/bin/env python3
"""IA-Ipanema V2: configuración, búsqueda, planes, QA y evidencia local."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

from ipanema import VERSION
from ipanema.core import IpanemaError, Project, check_id, doctor, read_json, redact, repo_root, run_command, safe_url, write_json


def cli():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version=VERSION)
    parser.add_argument("--project")
    sub = parser.add_subparsers(dest="command", required=True)
    from ipanema.seo.cli import add_parser as add_seo_parser
    add_seo_parser(sub)
    sub.add_parser("doctor")
    projects = sub.add_parser("projects")
    project_sub = projects.add_subparsers(dest="operation", required=True)
    project_sub.add_parser("list")
    for name in ("use", "register"):
        p = project_sub.add_parser(name)
        p.add_argument("id")
        if name == "register":
            p.add_argument("--name", required=True)
            p.add_argument("--theme-root")
            p.add_argument("--url")
            p.add_argument("--environment", default="development")
    for name in ("search", "plan", "route"):
        p = sub.add_parser(name)
        p.add_argument("request")
        if name == "search":
            p.add_argument("--limit", type=int, default=3)
        if name == "plan":
            p.add_argument("--action", choices=["read", "local-change", "environment", "production"], default="read")
            p.add_argument("--authorize-local", action="store_true")
            p.add_argument("--save", action="store_true")
    qa = sub.add_parser("qa")
    qa.add_argument("--suite", choices=["repo", "source", "unit", "integration", "quick", "evals", "fixtures", "seo", "browser", "page", "component", "full"], default="quick")
    qa.add_argument("--page", action="append")
    qa.add_argument("--component")
    qa.add_argument("--allow-network", action="store_true")
    qa.add_argument("--lighthouse", action="store_true")
    ev = sub.add_parser("evals")
    ev.add_argument("--responses", type=Path)
    compare = sub.add_parser("compare")
    compare.add_argument("kind", choices=["visual", "metrics"])
    compare.add_argument("before", type=Path)
    compare.add_argument("after", type=Path)
    compare.add_argument("--pixel-threshold", type=int)
    compare.add_argument("--max-changed-ratio", type=float)
    compare.add_argument("--mask", action="append", help="x,y,ancho,alto")
    attempt = sub.add_parser("attempt")
    attempt_sub = attempt.add_subparsers(dest="operation", required=True)
    b = attempt_sub.add_parser("begin")
    b.add_argument("--file", action="append", required=True)
    b.add_argument("--scope", choices=["theme", "workspace"], default="theme")
    b.add_argument("--max-attempts", type=int, default=2)
    b.add_argument("--authorize-local", action="store_true")
    for name in ("apply", "accept", "revert", "verify"):
        p = attempt_sub.add_parser(name)
        p.add_argument("id")
        if name == "apply":
            p.add_argument("--patch", type=Path, required=True)
        if name == "accept":
            p.add_argument("--evidence", type=Path, required=True)
            p.add_argument("--baseline", type=Path, required=True)
        if name == "verify":
            p.add_argument("--suite", choices=["repo", "unit", "integration", "quick", "fixtures"], default="quick")
            p.add_argument("--baseline", type=Path, required=True)
    solution = sub.add_parser("solutions")
    solution.add_argument("--register", type=Path)
    solution.add_argument("--evidence", type=Path, action="append", default=[])
    args = parser.parse_args()
    root = repo_root()
    if args.command == "projects":
        registry_path = root / "projects/registry.json"
        registry = read_json(registry_path)
        if args.operation == "list":
            return {"active": Project(project_id=args.project).id, "projects": list(registry["projects"])}, 0
        project_id = check_id(args.id)
        if args.operation == "use":
            Project(project_id=project_id)
            write_json(root / ".local/config.json", {"active_project": project_id}, overwrite=True)
            return {"active": project_id, "stored": "local-only"}, 0
        if project_id in registry["projects"] or (root / "projects" / f"{project_id}.json").exists():
            raise IpanemaError("Proyecto ya registrado; no se sobrescribirá.")
        url = safe_url(args.url) if args.url else None
        data = {"schema_version": 2, "id": project_id, "name": args.name, "theme_root": None,
                "environment": args.environment, "public_url": url, "discovery_root": "ipanema-discovery",
                "knowledge_reference_project": "ipanema", "evidence_dir": f"reports/runs/{project_id}",
                "remote_observation": None, "qa": {"pages": {"home": "/"} if url else {},
                "widths": [360, 390, 768, 1024, 1440, 1920]}}
        if args.theme_root:
            from ipanema.core import resolve_path
            theme = resolve_path(args.theme_root, root)
            if not (theme / "layouts/layout.tpl").is_file():
                raise IpanemaError("La ruta del tema no existe o no contiene layouts/layout.tpl.")
            write_json(root / "projects" / f"{project_id}.local.json", {"theme_root": str(theme)})
        write_json(root / "projects" / f"{project_id}.json", data)
        registry["projects"][project_id] = f"projects/{project_id}.json"
        write_json(registry_path, registry, overwrite=True)
        return {"registered": project_id, "remote_connection_checked": False}, 0
    project = Project(project_id=args.project)
    if args.command == 'seo':
        from ipanema.seo.cli import execute as seo_execute
        return seo_execute(project, args)
    if args.command == "doctor":
        result = doctor(project)
        import shutil
        if shutil.which("node"):
            r = run_command(["node", str(root / "tools/browser_runtime.mjs"), "--doctor"], cwd=root, timeout=15)
            try:
                result["browser"] = json.loads(r["stdout"])
            except (ValueError, KeyError):
                result["browser"] = {"status": "unavailable", "exit_code": r["exit_code"]}
        return result, 1 if result["errors"] else 0
    if args.command == "search":
        from ipanema.knowledge import Knowledge
        if not 1 <= args.limit <= 15:
            raise IpanemaError("limit debe estar entre 1 y 15.")
        return Knowledge(project).retrieve(args.request, args.limit), 0
    if args.command in ("plan", "route"):
        from ipanema.coordinator import plan, route
        if args.command == "route":
            return route(args.request), 0
        result = plan(project, args.request, args.action, args.authorize_local)
        if args.save:
            destination = project.new_run("plan") / "plan.json"
            write_json(destination, result)
            result["saved"] = str(destination)
        return result, 0
    if args.command == "qa":
        from ipanema.qa import execute
        result = execute(project, args.suite, pages=args.page, component=args.component, allow_network=args.allow_network, lighthouse=args.lighthouse)
        summary = {k: result[k] for k in ("kind", "suite", "at", "outcome", "report", "limitations")}
        summary["checks"] = [{"name": c["name"], "status": c["status"]} for c in result["checks"]]
        return summary, 0 if result["outcome"] == "passed" else 2 if result["outcome"] == "blocked" else 1
    if args.command == "evals":
        from ipanema.evals import evaluate
        result = evaluate(project, args.responses)
        destination = project.new_run("evals") / "evaluation.json"
        write_json(destination, result)
        result["report"] = str(destination)
        return result, 0 if result["outcome"] == "passed" else 1
    if args.command == "compare":
        from ipanema.compare import metrics, visual
        if args.kind == "metrics":
            result = metrics(args.before, args.after)
        else:
            config = project.qa.get("visual", {})
            result = visual(args.before, args.after,
                            pixel_threshold=args.pixel_threshold if args.pixel_threshold is not None else config.get("pixel_threshold", 12),
                            max_changed_ratio=args.max_changed_ratio if args.max_changed_ratio is not None else config.get("max_changed_ratio", .005),
                            masks=[list(map(int, m.split(","))) for m in args.mask or []])
        return result, 0 if result["status"] == "passed" else 1
    if args.command == "attempt":
        from ipanema import transactions
        if args.operation == "begin":
            result = transactions.begin(project, args.file, scope=args.scope, max_attempts=args.max_attempts, authorized=args.authorize_local)
        elif args.operation == "apply":
            result = transactions.apply(project, args.id, read_json(args.patch))
        elif args.operation == "verify":
            from ipanema.qa import execute
            _, attempt = transactions.load(project, args.id)
            if attempt["status"] != "applied":
                raise IpanemaError("No hay un intento aplicado que verificar.")
            qa = execute(project, args.suite)
            result = transactions.finish(project, args.id, accept=qa["outcome"] == "passed",
                                         evidence=Path(qa["report"]) if qa["outcome"] == "passed" else None, baseline=args.baseline)
            result["qa_report"] = qa["report"]
            result["qa_outcome"] = qa["outcome"]
            return result, 0 if qa["outcome"] == "passed" else 1
        else:
            result = transactions.finish(project, args.id, accept=args.operation == "accept", evidence=getattr(args, "evidence", None), baseline=getattr(args, "baseline", None))
        return result, 0
    if args.command == "solutions":
        from ipanema.solutions import effective_solutions, register
        return register(project, read_json(args.register), args.evidence) if args.register else effective_solutions(project), 0
    raise IpanemaError("Comando no implementado.")


if __name__ == "__main__":
    try:
        result, code = cli()
        print(json.dumps(redact(result), ensure_ascii=False, indent=2))
    except (IpanemaError, OSError, ValueError, KeyError) as exc:
        print(json.dumps({"error": redact(str(exc)), "status": "not_executed"}, ensure_ascii=False), file=sys.stderr)
        code = 2
    sys.exit(code)
