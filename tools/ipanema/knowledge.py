"""Recuperación estructurada sobre el discovery existente, sin embeddings."""
from __future__ import annotations

from collections import deque
import datetime as dt
from pathlib import Path
import re
import unicodedata

from .core import Project, digest, read_json


def normal(value) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", str(value).lower()) if not unicodedata.combining(c))


ALIASES = {
    "producto": "product", "productos": "product", "tarjeta": "product-item/item.tpl",
    "tarjetas": "product-item/item.tpl", "card": "product-item/item.tpl", "pdp": "sections/main-product.tpl",
    "carrito": "cart", "imagen": "image", "imagenes": "image", "carrusel": "slider",
    "categorias": "categories", "categoria": "category", "menu": "navigation", "busqueda": "search",
    "pie": "footer", "encabezado": "heading", "cabecera": "header", "animacion": "animation",
    "espaciado": "spacing", "columnas": "columns", "agotado": "stock", "variante": "variant",
}
STOPWORDS = set("de del el la los las en un una unos unas que para por con sin y o a al es son se si no lo su sus mi mis como cual cuando donde quiero solicita solicitar necesito usar usando mediante debe deben antes despues modificar cambiar corrige agrega evita existe investiga afirmar permite activar hay disponible contenido diferente muestra comprueba reales nativos nativo componentes componente".split())


def query_terms(query):
    tokens = [t.strip(".") for t in re.findall(r"[\w./-]+", normal(query))]
    return {t for t in tokens if t and t not in STOPWORDS and t not in {"esta", "este", "estos", "estas"}}


class Knowledge:
    def __init__(self, project: Project):
        self.project = project
        self.doc = project.knowledge_root
        self.base = self.doc / "13-evidence/measurements/source-baseline"
        self.summary = read_json(self.base / "source-summary.json")
        self.components = read_json(self.base / "components.json")
        self.edges = read_json(self.base / "dependency-graph.json")
        self.settings = read_json(self.base / "settings.json")
        self.files = {f["path"]: f for f in read_json(self.base / "source-inventory.json")}
        self.reference_project = project.data.get("knowledge_reference_project", "ipanema")

    def consumers(self, path: str):
        direct = [e for e in self.edges if e.get("target") == path]
        reached, queue = set(), deque([path])
        while queue:
            child = queue.popleft()
            for edge in self.edges:
                parent = edge["source"]
                if edge.get("target") == child and parent not in reached and parent != path:
                    reached.add(parent)
                    queue.append(parent)
        return {"direct": direct, "transitive": sorted(reached),
                "templates": sorted(p for p in reached if p.startswith("templates/")),
                "limitations": ["Grafo fechado; las inclusiones dinámicas requieren buscar en el código actual."]}

    def freshness(self, path: str | None = None):
        date = self.summary["verified_at"]
        age = (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(date.replace("Z", "+00:00"))).days
        result = {"observed_at": date, "age_days": age, "reference_project": self.reference_project,
                  "active_project": self.project.id, "remote_reverified": False,
                  "status": "historical_observation", "requires_current_source_check": True}
        if path and self.project.theme_root and (self.project.theme_root / path).is_file():
            expected = self.files.get(path, {}).get("sha256")
            result["file_hash_matches"] = digest(self.project.theme_root / path) == expected
            result["status"] = "file_matches_snapshot" if result["file_hash_matches"] else "stale_file"
            result["requires_current_source_check"] = not result["file_hash_matches"]
        if self.project.id != self.reference_project:
            result["compatibility"] = "unverified_for_active_project"
            result["requires_current_source_check"] = True
        return result

    def search(self, query: str, limit=5):
        tokens = query_terms(query)
        terms = tokens | {ALIASES[t] for t in tokens if t in ALIASES}
        hits = []
        for c in self.components:
            identity = normal(c["path"] + " " + str(c.get("name")))
            context = normal(" ".join(c.get("js_hooks", []) + c.get("setting_refs", [])))
            score = sum(20 if t.endswith(".tpl") else 5 for t in terms if t in identity)
            score += sum(30 for t in terms if t == normal(Path(c["path"]).stem))
            score += sum(1 for t in terms if t in context)
            if score:
                hits.append((score, c))
        results = []
        for score, c in sorted(hits, key=lambda x: (-x[0], x[1]["path"]))[:limit]:
            settings = [s for s in self.settings if s["file"] == c["path"]]
            results.append({"score": score, "path": c["path"], "name": c.get("name"), "kind": c["kind"],
                            "sheet": str((self.doc / "02-native-components/specifications" /
                                          (c["path"][:-4].replace("/", "--") + ".md")).relative_to(self.project.root)),
                            "consumers": self.consumers(c["path"]),
                            "settings": settings[:15], "settings_total": len(settings),
                            "js_hooks": c.get("js_hooks", []), "freshness": self.freshness(c["path"])})
        return results

    def findings(self, query: str, limit=5):
        entries = read_json(self.doc / "11-opportunities/findings.json")
        tokens = query_terms(query)
        scored = [(sum(t in normal(str(e)) for t in tokens), e) for e in entries]
        return [dict(id=e["id"], title=e["title"], status=e["status"], severity=e["severity"],
                     current=e["current"], recommendation=e["recommendation"],
                     observed_at=e["date"], knowledge_kind="finding_with_proposal", evidence=e["evidence"])
                for s, e in sorted(scored, key=lambda x: (-x[0], x[1]["id"]))[:limit] if s]

    def settings_search(self, query: str, limit=10):
        terms = query_terms(query)
        scored = []
        for setting in self.settings:
            text = normal(setting["id"] + " " + str(setting.get("label_resolved", "")) + " " + setting["file"])
            score = sum(t in text for t in terms)
            if score:
                scored.append((score, setting))
        return [s for _, s in sorted(scored, key=lambda x: (-x[0], x[1]["file"], x[1]["id"]))[:limit]]

    def documents(self, query: str, limit=5):
        tokens = query_terms(query)
        terms = tokens | {ALIASES[t] for t in tokens if t in ALIASES and not ALIASES[t].endswith(".tpl")}
        hits = []
        for p in self.doc.rglob("*.md"):
            if "specifications" in p.parts or "13-evidence" in p.parts:
                continue
            body = p.read_text(encoding="utf-8")
            score = sum(5 for t in terms if t in normal(p.name)) + sum(1 for t in terms if t in normal(body))
            if score:
                lines = body.splitlines()
                index = next((i for i, line in enumerate(lines) if any(t in normal(line) for t in terms)), 0)
                hits.append((score, {"path": str(p.relative_to(self.project.root)), "line": index + 1,
                                     "excerpt": "\n".join(lines[index:index+4])[:600]}))
        return [v for _, v in sorted(hits, key=lambda x: (-x[0], x[1]["path"]))[:limit]]

    def retrieve(self, query: str, limit=5):
        from .solutions import effective_solutions
        return {"query": query, "freshness": self.freshness(), "components": self.search(query, limit),
                "settings": self.settings_search(query, limit*2),
                "documents": self.documents(query, limit), "findings": self.findings(query, limit),
                "solutions": effective_solutions(self.project, query),
                "limitations": ["Búsqueda determinista; no prueba soporte de una configuración ausente.",
                                "Un hallazgo y su recomendación no son una solución verificada."]}
