"""Proyectos sintéticos: no contienen código propietario ni credenciales reales."""
from __future__ import annotations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))


def put(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) if not isinstance(value, str) else value, encoding="utf-8")


def make_project(root: Path, identifier="sample", *, theme=True):
    put(root / "projects/registry.json", {"schema_version": 2, "default": identifier,
                                        "projects": {identifier: f"projects/{identifier}.json"}})
    put(root / f"projects/{identifier}.json", {"schema_version": 2, "id": identifier, "name": identifier,
        "theme_root": "theme" if theme else None, "discovery_root": "ipanema-discovery",
        "knowledge_reference_project": identifier, "evidence_dir": f"reports/runs/{identifier}",
        "public_url": "https://example.invalid", "qa": {"pages": {"home": "/"}}})
    if theme:
        put(root / "theme/layouts/layout.tpl", '<main>{% include "sections/hero.tpl" %}</main>')
        put(root / "theme/config/settings_schema.json", [])
        put(root / "theme/templates/pages/home.json", {"sections": {"hero": {"type": "hero", "settings": {}}}, "order": ["hero"]})
        put(root / "theme/sections/hero.tpl", '<section><h1>Fixture</h1></section>\n{% schema %}{"name":"Hero","settings":[{"id":"title","type":"setting","setting_type":"text","default":"Fixture"}]}{% endschema %}')
        put(root / "theme/manifest.json", {"theme": "fixture", "theme_version": "1", "forked": True})
    return root
