"""Auditoría estática de los snippets JSON-LD de un tema Tiendanube (Twig) mediante simulación de ramas.

No es un intérprete de Twig. Recorre las ramas `if/elseif/else/for` del snippet con un dominio modelado
(plantilla, flags de include, bucles de 0 o 2 iteraciones, condiciones desconocidas decididas de forma
consistente por camino), sustituye cada `{{ }}` por un marcador y comprueba si cada camino produce JSON válido.
Un camino fallido demuestra que *esa combinación de decisiones* rompe la sintaxis; si la combinación ocurre en
la plataforma (p. ej. `breadcrumbs` vacío) depende de datos que el tema no controla: el informe lo indica.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import re
import difflib

from .extractor import parse_json_ld

TEMPLATES = ["home", "category", "product", "cart", "page", "search", "blog", "post", "contact", "404", "password",
             "account.login", "account.register", "account.index", "account.order", "account.orders"]
MAX_PATHS = 4096
TOKEN = re.compile(r"(\{#.*?#\}|\{%-?\s*(.*?)\s*-?%\}|\{\{-?\s*(.*?)\s*-?\}\})", re.S)
FREE_TEXT = re.compile(r"(name|title|description|brand|author|summary|handle|seo_|\|\s*t\b|replace\()", re.I)
PROTECTED = re.compile(r"json_string|json_description|json_encode")


class NeedDecision(Exception):
    def __init__(self, key, options):
        self.key, self.options = key, options


class Unknown:
    def __init__(self, key):
        self.key = key


# ---------------------------------------------------------------- parser

def parse(source: str):
    """Árbol mínimo: ('text',s) ('print',expr,line) ('if',[(cond,body)…]) ('for',var,iter,body) ('include',path,flags,line)."""
    root, stack, pos = [], [], 0
    stack = [("root", root)]
    macro_depth = 0

    def body():
        return stack[-1][1]

    for m in TOKEN.finditer(source):
        line = source.count("\n", 0, m.start()) + 1
        text = source[pos:m.start()]
        if text and macro_depth == 0:
            body().append(("text", text))
        pos = m.end()
        tag, expr = m.group(2), m.group(3)
        if m.group(1).startswith("{#"):
            continue
        if tag is None:
            if macro_depth == 0:
                body().append(("print", expr, line))
            continue
        word, _, rest = tag.partition(" ")
        rest = rest.strip()
        if word == "macro":
            macro_depth += 1
        elif word == "endmacro":
            macro_depth = max(0, macro_depth - 1)
        elif macro_depth:
            continue
        elif word == "if":
            node = ["if", [(rest, [])], line]
            body().append(node)
            stack.append(("if", node[1][-1][1], node))
        elif word in ("elseif", "else") and len(stack) > 1 and stack[-1][0] == "if":
            node = stack[-1][2]
            node[1].append((rest if word == "elseif" else None, []))
            stack[-1] = ("if", node[1][-1][1], node)
        elif word == "endif" and len(stack) > 1 and stack[-1][0] == "if":
            stack.pop()
        elif word == "for":
            mm = re.match(r"(\w+)(?:\s*,\s*\w+)?\s+in\s+(.+)", rest, re.S)
            node = ["for", mm.group(1) if mm else "_", mm.group(2).strip() if mm else rest, [], line]
            body().append(node)
            stack.append(("for", node[3], node))
        elif word == "endfor" and len(stack) > 1 and stack[-1][0] == "for":
            stack.pop()
        elif word == "include":
            path = re.match(r"['\"]([^'\"]+)['\"]", rest)
            flags = {k: v == "true" for k, v in re.findall(r"['\"](\w+)['\"]\s*:\s*(true|false)", rest)}
            body().append(("include", path.group(1) if path else None, flags, line))
    tail = source[pos:]
    if tail and macro_depth == 0:
        root.append(("text", tail))
    return root


# ---------------------------------------------------------------- expresiones (lógica de tres valores por decisión)

TOK = re.compile(r"\s*(?:(?P<str>'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\")|(?P<num>\d+(?:\.\d+)?)|(?P<op>==|!=|>=|<=|b-or|b-and|=>|[<>()\[\]|~+\-*/,?:.=%{}])|(?P<id>[A-Za-z_]\w*))")


def tokens(expr):
    out, i = [], 0
    while i < len(expr):
        m = TOK.match(expr, i)
        if not m:
            if expr[i:].strip() == "":
                break
            raise ValueError("token")
        i = m.end()
        kind = m.lastgroup
        out.append((kind, m.group(kind)))
    return out


class Evaluator:
    def __init__(self, env, decisions):
        self.env, self.decisions = env, decisions

    def decide(self, key, options=(True, False)):
        if key not in self.decisions:
            raise NeedDecision(key, options)
        return self.decisions[key]

    def truthy(self, v):
        if isinstance(v, Unknown):
            return bool(self.decide("cond:" + v.key))
        return bool(v)

    def evaluate(self, expr):
        try:
            self.t, self.i, self.src = tokens(expr), 0, expr
            v = self.p_or()
            if self.i != len(self.t):
                raise ValueError("trailing")
            return v
        except (ValueError, IndexError):
            return Unknown(expr.strip())

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else (None, None)

    def eat_word(self, word):
        k, v = self.peek()
        if k == "id" and v == word:
            self.i += 1
            return True
        return False

    def p_or(self):
        v = self.p_and()
        while self.peek() == ("id", "or"):
            self.i += 1
            right = self.p_and()
            v = True if self.truthy(v) else self.truthy(right)
        return v

    def p_and(self):
        v = self.p_not()
        while self.peek() == ("id", "and"):
            self.i += 1
            if not self.truthy(v):
                self.p_not_skip()
                v = False
            else:
                v = self.truthy(self.p_not())
        return v

    def p_not_skip(self):
        # consumir el operando derecho sin evaluar decisiones
        saved = self.decisions
        self.decisions = _AnyDecisions()
        try:
            self.p_not()
        finally:
            self.decisions = saved

    def p_not(self):
        if self.eat_word("not"):
            return not self.truthy(self.p_not())
        return self.p_cmp()

    def p_cmp(self):
        left = self.p_add()
        k, v = self.peek()
        if k == "op" and v in ("==", "!=", ">", "<", ">=", "<="):
            self.i += 1
            right = self.p_add()
            if isinstance(left, Unknown) or isinstance(right, Unknown):
                key = "cmp:" + self.src.strip()
                return bool(self.decide(key))
            try:
                return {"==": left == right, "!=": left != right, ">": left > right, "<": left < right, ">=": left >= right, "<=": left <= right}[v]
            except TypeError:
                return Unknown(self.src)
        if k == "id" and v in ("is", "in", "matches", "starts", "ends"):
            raise ValueError("unsupported")
        return left

    def p_add(self):
        v = self.p_atom()
        while self.peek()[0] == "op" and self.peek()[1] in ("+", "-", "*", "/", "~", "%"):
            op = self.peek()[1]
            self.i += 1
            r = self.p_atom()
            if isinstance(v, Unknown) or isinstance(r, Unknown) or op == "~":
                v = Unknown(self.src)
            else:
                try:
                    v = {"+": v + r, "-": v - r, "*": v * r, "/": v / r if r else 0, "%": v % r if r else 0}[op]
                except TypeError:
                    v = Unknown(self.src)
        return v

    def p_atom(self):
        k, v = self.peek()
        if k == "op" and v == "(":
            self.i += 1
            r = self.p_or()
            if self.peek() != ("op", ")"):
                raise ValueError("paren")
            self.i += 1
            return r
        if k == "str":
            self.i += 1
            return v[1:-1]
        if k == "num":
            self.i += 1
            return float(v) if "." in v else int(v)
        if k == "id":
            self.i += 1
            if v in ("true", "false", "null", "none"):
                return {"true": True, "false": False}.get(v)
            name = v
            while self.peek() == ("op", "."):
                self.i += 1
                name += "." + self.peek()[1]
                self.i += 1
            known = name in self.env
            call = self.peek() == ("op", "(")
            if call:
                self.skip_group()
            filt = False
            resolved = self.env.get(name)
            while self.peek() == ("op", "|"):
                self.i += 1
                filter_name = self.peek()[1]
                self.i += 1
                if self.peek() == ("op", "("):
                    self.skip_group()
                filt = True
                if known and filter_name == 'length':
                    resolved = len(resolved) if resolved is not None and hasattr(resolved,'__len__') else 0
                else:known=False
            if known and not call and not filt:
                return self.env[name]
            if known and not call and filt:return resolved
            if not known and not call and not filt and name in ("item", "blog_item"):
                return False
            return Unknown(name + ("(…)" if call else "") + ("|f" if filt else ""))
        raise ValueError("atom")

    def skip_group(self):
        depth = 0
        while self.i < len(self.t):
            k, v = self.t[self.i]
            self.i += 1
            if (k, v) == ("op", "("):
                depth += 1
            elif (k, v) == ("op", ")"):
                depth -= 1
                if depth == 0:
                    return
        raise ValueError("group")


class _AnyDecisions(dict):
    def __contains__(self, key):
        return True

    def __getitem__(self, key):
        return True


# ---------------------------------------------------------------- render

def has_output(nodes):
    for n in nodes:
        if n[0] == "print" or n[0] == "for":
            return True
        if n[0] == "text" and n[1].strip():
            return True
        if n[0] == "if" and any(has_output(b) for _, b in n[1]):
            return True
    return False


class Renderer:
    def __init__(self, env, decisions):
        self.env, self.decisions = dict(env), decisions
        self.out, self.in_str, self.esc = [], False, False
        self.prints = {}

    def emit(self, text):
        for ch in text:
            if self.in_str:
                if self.esc:
                    self.esc = False
                elif ch == "\\":
                    self.esc = True
                elif ch == '"':
                    self.in_str = False
            elif ch == '"':
                self.in_str = True
        self.out.append(text)

    def render(self, nodes):
        ev = Evaluator(self.env, self.decisions)
        for n in nodes:
            kind = n[0]
            if kind == "text":
                self.emit(n[1])
            elif kind == "print":
                expr = n[1]
                protected = bool(PROTECTED.search(expr))
                rec = self.prints.setdefault(expr, {"in_string": self.in_str, "protected": protected, "line": n[2]})
                rec["in_string"] = rec["in_string"] or self.in_str
                if self.in_str:
                    self.emit("x")
                else:
                    self.emit('"s"' if protected else "1")
            elif kind == "if":
                if not any(has_output(b) for _, b in n[1]):
                    continue
                for cond, body in n[1]:
                    if cond is None or ev.truthy(ev.evaluate(cond)):
                        self.render(body)
                        break
            elif kind == "for":
                _, var, it, body, _line = n
                v = ev.evaluate(it)
                count = ev.decide("iter:" + it, (0, 2)) if isinstance(v, Unknown) else (2 if v else 0)
                for idx in range(count):
                    saved = dict(self.env)
                    self.env.update({"loop.index": idx + 1, "loop.index0": idx, "loop.length": count, "loop.first": idx == 0,
                                     "loop.last": idx == count - 1, var + ".last": idx == count - 1})
                    self.render(body)
                    self.env = saved
        return "".join(self.out)


def explore(nodes, env):
    """DFS sobre decisiones; devuelve [(decisions, rendered_text, prints)]."""
    results, stack = [], [{}]
    truncated = False
    while stack:
        d = stack.pop()
        r = Renderer(env, d)
        try:
            text = r.render(nodes)
        except NeedDecision as nd:
            for opt in nd.options:
                stack.append({**d, nd.key: opt})
            continue
        results.append((d, text, r.prints))
        if len(results) >= MAX_PATHS:
            truncated = bool(stack)
            break
    return results, truncated


LD = re.compile(r"<script[^>]*application/ld\+json[^>]*>(.*?)</script>", re.S | re.I)
COMP = re.compile(r"data-component=['\"]([^'\"]+)['\"]")


def consumers(theme: Path, target_rel: str):
    """Includes del snippet con sus flags y las condiciones envolventes (para determinar plantillas alcanzables)."""
    found = []
    for tpl in theme.rglob("*.tpl"):
        if tpl.is_symlink() or tpl.stat().st_size>10_000_000:continue
        rel = tpl.relative_to(theme).as_posix()
        if rel == target_rel:
            continue
        src = tpl.read_text(encoding="utf-8", errors="replace")
        if target_rel not in src:
            continue

        def walk(nodes, conds):
            for n in nodes:
                if n[0] == "include" and n[1] == target_rel:
                    found.append({"file": rel, "line": n[3], "flags": n[2], "conditions": list(conds)})
                elif n[0] == "if":
                    prev = []
                    for cond, body in n[1]:
                        walk(body, conds + [(c, False) for c in prev] + ([(cond, True)] if cond else []))
                        if cond:
                            prev.append(cond)
                elif n[0] == "for":
                    walk(n[3], conds)
        walk(parse(src), [])
    return found


def feasible(conds, template):
    """False solo si una condición modelada (plantilla) la descarta con certeza."""
    for cond, polarity in conds:
        ev = Evaluator({"template": template}, {})
        try:
            v = ev.evaluate(cond)
            t = ev.truthy(v)
        except NeedDecision:
            continue
        if t != polarity:
            return False
    return True


def audit_snippet(theme: Path, rel: str, templates=None):
    src = (theme / rel).read_text(encoding="utf-8")
    nodes = parse(src)
    cons = consumers(theme, rel)
    if re.search(r"layout\.tpl$", "".join(c["file"] for c in cons)) is None and not cons:
        cons = []
    contexts = []
    for c in cons:
        for t in templates or TEMPLATES:
            if feasible(c["conditions"], t):
                contexts.append({"consumer": f"{c['file']}:{c['line']}", "flags": c["flags"], "template": t})
    failures, hashes, blocks, prints_all, truncated_any = {}, set(), {}, {}, False
    for ctx in contexts:
        env = {"template": ctx["template"], "item": bool(ctx["flags"].get("item")), "blog_item": bool(ctx["flags"].get("blog_item"))}
        results, truncated = explore(nodes, env)
        truncated_any = truncated_any or truncated
        for decisions, text, prints in results:
            for expr, rec in prints.items():
                prints_all.setdefault(expr, rec)
            for raw in LD.findall(text):
                comp = COMP.search(text[: text.find(raw)][-300:] if raw in text else "")
                data, err = parse_json_ld(raw)
                if data is not None:
                    continue
                sig = (comp.group(1) if comp else "?", err["hint"], err["message"])
                f = failures.setdefault(sig, {"component": sig[0], "hint": err["hint"], "message": err["message"], "contexts": {}, "example_decisions": decisions, "example": raw.strip()[:900]})
                f["contexts"].setdefault(f"{ctx['consumer']} flags={ctx['flags']}", set()).add(ctx["template"])
    for f in failures.values():
        f["contexts"] = {k: sorted(v) for k, v in f["contexts"].items()}
    scripts = []
    for m in LD.finditer(src):
        comp = COMP.search(src[max(0, m.start() - 10):m.start() + 200])
        scripts.append({"component": comp.group(1) if comp else None, "types": sorted(set(re.findall(r'"@type"\s*:\s*"(\w+)"', m.group(1)))), "line": src.count("\n", 0, m.start()) + 1})
    return {"snippet": rel, "sha256": hashlib.sha256(src.encode()).hexdigest()[:16], "scripts": scripts,
            "consumers": [{"file": c["file"], "line": c["line"], "flags": c["flags"], "conditions": [f"{'' if p else 'not '}({x})" for x, p in c["conditions"]]} for c in cons],
            "contexts_simulated": len(contexts), "invalid_paths": sorted(failures.values(), key=lambda f: f["component"]),
            "paths_truncated": truncated_any,
            "interpolations": [{"expr": e, **r} for e, r in sorted(prints_all.items(), key=lambda kv: kv[1]["line"])]}


STATIC_PATTERNS = [
    ("S001", "warning", r'"@type"\s*:\s*"Thing"', "Brand declarado como `Thing`; Google documenta `Brand`."),
    ("S002", "optional", r'"@context"\s*:\s*"http://schema\.org"', "@context con http://."),
    ("S003", "optional", r'http://schema\.org/\{\{', "availability con prefijo http://schema.org/."),
    ("S004", "recommendation", r'"author"\s*:\s*\{\{\s*_self\.json_string', "`author` como texto plano en BlogPosting."),
    ("S005", "optional", r'inventoryLevel', "Se publica inventoryLevel (existencias numéricas)."),
    ("S006", "warning", r'"image"\s*:\s*"\{\{\s*\'https:\'\s*~', "image se construye como 'https:' + valor; si el valor está vacío queda `https:`."),
    ("S007", "recommendation", r'"price"\s*:\s*"\{\{[^}]*/\s*100', "price se calcula dividiendo centavos entre 100 en Twig; el formato numérico depende del motor (verificar en HTML real)."),
]


def audit_theme(theme: Path, templates=None):
    snippets = sorted({p.relative_to(theme).as_posix() for p in theme.rglob("*.tpl") if not p.is_symlink() and p.stat().st_size<=10_000_000 and LD.search(p.read_text(encoding="utf-8", errors="replace"))})
    report = {"theme_root_name": theme.name, "ld_json_files": snippets, "audits": [], "static": [], "microdata_in_templates": []}
    for rel in snippets:
        src = (theme / rel).read_text(encoding="utf-8")
        report["audits"].append(audit_snippet(theme, rel, templates))
        for rule, sev, pat, msg in STATIC_PATTERNS:
            for m in re.finditer(pat, src):
                report["static"].append({"rule": rule, "severity": sev, "file": rel, "line": src.count("\n", 0, m.start()) + 1, "message": msg})
        if re.search(r"escape_text", src):
            report["static"].append({"rule": "S010", "severity": "warning", "file": rel, "line": 1,
                                     "message": "Escape manual (`replace` encadenado) en lugar de json_encode: no reemplaza los caracteres de control U+0000–U+001F salvo \\n, \\r, \\t; los valores en `sameAs` se interpolan sin escape."})
    for p in theme.rglob("*.tpl"):
        if p.is_symlink() or p.stat().st_size>10_000_000:continue
        s = p.read_text(encoding="utf-8", errors="replace")
        if re.search(r"\bitemscope\b|\bitemprop\b", s):
            report["microdata_in_templates"].append(p.relative_to(theme).as_posix())
    return report


def breadcrumb_proposal(theme: Path):
    """Diff mínimo de un patrón encontrado, sin escribir en el tema real."""
    rel='snippets/structured-data/structured-data.tpl'
    path=theme/rel
    if not path.is_file() or path.is_symlink():
        return {'status':'native_snippet_not_available','file':rel,'theme_modified':False}
    before=path.read_text(encoding='utf-8')
    old="}{% if template != 'home' %},{% endif %}"
    new="}{% if breadcrumbs | length > 0 or template == 'page' or template == 'cart' or template == 'search' or template == 'account.order' %},{% endif %}"
    if before.count(old)!=1:
        return {'status':'not_applicable_pattern_changed','file':rel,'source_sha256':hashlib.sha256(before.encode()).hexdigest()}
    after=before.replace(old,new,1)
    # Se prueban las ramas explícitas del archivo actual con breadcrumbs correlacionados al bucle.
    rows=[]
    for template in ('home','category','product','blog','post','cart','search','page','account.order','404','password'):
        for crumbs in ([],[{},{}]):
            results=[]
            for text in (before,after):
                env={'template':template,'item':False,'blog_item':False,'breadcrumbs':crumbs}
                paths,truncated=explore(parse(text),env)
                invalid=sum(parse_json_ld(raw)[1] is not None for _,rendered,_ in paths for raw in LD.findall(rendered))
                results.append({'paths':len(paths),'invalid_json_blocks':invalid,'truncated':truncated})
            rows.append({'template':template,'breadcrumb_count':len(crumbs),'before':results[0],'after':results[1]})
    return {'status':'proposal_only','file':rel,'source_sha256':hashlib.sha256(before.encode()).hexdigest(),
            'patch':''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='a/'+rel,tofile='b/'+rel)),
            'cases':rows,'method':'Modelo abstracto de ramas del snippet actual; no ejecuta Twig ni filtros de plataforma.',
            'limitations':['Los valores interpolados son marcadores sintéticos, no datos de productos.','La corrección de la fuente requiere revisión y render real en un tema aislado autorizado.'],
            'theme_modified':False}


def native_markers(theme: Path):
    """Marcadores literales de scripts: candidatos de fuente, no iniciador de red."""
    result={}
    for path in theme.rglob('*.tpl'):
        if path.is_symlink() or path.stat().st_size>10_000_000:continue
        text=path.read_text(encoding='utf-8',errors='replace')
        for match in re.finditer(r'<script\b[^>]*>',text,re.I):
            tag=match.group()
            if not re.search(r'type\s*=\s*[\"\']application/ld\+json[\"\']',tag,re.I):continue
            marker=re.search(r'data-component\s*=\s*[\"\']([^\"\']+)[\"\']',tag,re.I)
            if marker:
                result.setdefault(marker[1],[]).append(str(path.relative_to(theme))+':'+str(text.count('\n',0,match.start())+1))
    return result
