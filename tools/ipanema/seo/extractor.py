"""Extracción SEO de un documento HTML ya capturado (HTML inicial o DOM serializado).

Solo biblioteca estándar. No hace red: recibe texto. Devuelve un diccionario serializable
(`snapshot`) que consumen validador, grafo, rastreo y reportes.
"""
from __future__ import annotations

from html.parser import HTMLParser
import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlsplit

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
CAROUSEL_RE = re.compile(r"(carousel|swiper|slider|slideshow|slick|splide|flickity|glide)", re.I)
DUPLICATE_SLIDE_RE = re.compile(r"(swiper-slide-duplicate|slick-cloned|splide__slide--clone|is-clone)", re.I)
LINK_CONTRACTS=json.loads(Path(__file__).with_name('link_contracts.json').read_text(encoding='utf-8'))
ACTION_RE=re.compile(LINK_CONTRACTS['native_action_pattern'],re.I)


def locate(text: str, pos: int):
    line = text.count("\n", 0, pos) + 1
    return line, pos - (text.rfind("\n", 0, pos) + 1) + 1


def trailing_commas(text: str):
    """Posiciones de comas seguidas solo de espacio y `}`/`]`, fuera de cadenas JSON."""
    found, in_str, esc, last_comma = [], False, False, None
    for i, ch in enumerate(text):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str, last_comma = True, None
        elif ch == ",":
            last_comma = i
        elif ch in "}]":
            if last_comma is not None:
                found.append(last_comma)
            last_comma = None
        elif not ch.isspace():
            last_comma = None
    return found


def parse_json_ld(raw: str):
    """Devuelve (datos, error|None). El error incluye línea/columna y una pista de causa."""
    try:
        def strict_constant(value):
            raise ValueError("Constante no JSON: " + value)
        def unique(pairs):
            result = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError("Propiedad JSON duplicada: " + key)
                result[key] = value
            return result
        return json.loads(raw, parse_constant=strict_constant, object_pairs_hook=unique), None
    except ValueError as exc:
        hint = "unknown"
        if trailing_commas(raw):
            hint = "trailing_comma"
        elif not raw.strip():
            hint = "empty"
        elif "Expecting ',' delimiter" in str(exc):
            hint = "missing_comma_or_unescaped_quote"
        elif "Invalid control character" in str(exc):
            hint = "unescaped_control_character"
        return None, {"message": getattr(exc, "msg", str(exc)), "line": getattr(exc, "lineno", 1), "column": getattr(exc, "colno", 1), "hint": hint}


class _Collector(HTMLParser):
    def __init__(self, text: str, base_url: str):
        super().__init__(convert_charrefs=True)
        self.text, self.base = text, base_url
        self.stack = []
        self.snap = {"title": None, "lang": None, "meta": {}, "links_rel": [], "headings": [], "links": [], "images": [],
                     "json_ld": [], "microdata": [], "rdfa": {"typeof": 0, "property": 0, "vocab": 0},
                     "noscript": 0, "scripts_external": 0, "inline_script_ld_count": 0}
        self._title = False
        self._script = None
        self._heading = None
        self._anchor = None
        self._micro = []

    def _ctx(self):
        names = [e["tag"] for e in self.stack]
        return {"nav": "nav" in names, "header": "header" in names, "footer": "footer" in names, "main": "main" in names,
                "list": "li" in names, "noscript": "noscript" in names,
                "carousel": any(e["carousel"] for e in self.stack), "clone": any(e["clone"] for e in self.stack),
                "pagination": any(e.get('pagination') for e in self.stack),
                "hidden": any(e["hidden"] for e in self.stack)}

    def handle_starttag(self, tag, attrs):
        a = {k: (v if v is not None else "") for k, v in attrs}
        pos = self.getpos()
        cls = a.get("class", "")
        marker = " ".join([cls, a.get("id", ""), a.get("data-component", ""), a.get("data-store", "")])
        entry = {"tag": tag, "carousel": bool(CAROUSEL_RE.search(marker)), "clone": bool(DUPLICATE_SLIDE_RE.search(cls)),
                 "hidden": "hidden" in a or a.get("aria-hidden") == "true" or "display:none" in a.get("style", "").replace(" ", "")}
        entry['user_content'] = 'user-content' in cls.split() or 'elementor' in cls
        entry['carousel'] = entry['carousel'] or 'data-qa-carousel' in a
        entry['pagination'] = bool(re.search(r'pagination|js-load-more|infinite-scroll',marker,re.I))
        if tag == "html":
            self.snap["lang"] = a.get("lang")
        elif tag == "title":
            self._title = True
        elif tag == 'base' and a.get('href'):
            self.base = urljoin(self.base, a['href'])
        elif tag == "meta":
            key = a.get("name") or a.get("property") or a.get("http-equiv")
            if key:
                self.snap["meta"].setdefault(key.lower(), []).append(a.get("content", ""))
        elif tag == "link":
            self.snap["links_rel"].append({"rel": a.get("rel", "").lower(), "href": a.get("href", ""), "hreflang": a.get("hreflang")})
        elif tag == "script":
            if a.get("type", "").lower() == "application/ld+json":
                self._script = {"attrs": a, "start": pos, "buf": []}
                self.snap["inline_script_ld_count"] += 1
            elif a.get("src"):
                self.snap["scripts_external"] += 1
        elif tag == "noscript":
            self.snap["noscript"] += 1
        elif re.fullmatch(r"h[1-6]", tag):
            context = self._ctx()
            context['user_content'] = any(e.get('user_content') for e in self.stack) or entry['user_content']
            self._heading = {"level": int(tag[1]), "text": [], "context": context, 'line':pos[0]}
        elif tag == "a":
            self._anchor = {"href": a.get('href'), "rel": a.get("rel", ""), "aria_label": a.get("aria-label", ""), "title": a.get("title", ""),
                            "text": [], "img_alt": [], "context": self._ctx(), "target": a.get("target", ""), "class": cls,
                            "action_hint":bool(ACTION_RE.search(cls)) or a.get('role')=='button', 'disabled':a.get('aria-disabled')=='true' or 'disabled' in cls.split()}
            self._anchor['context']['pagination']=self._anchor['context']['pagination'] or entry['pagination']
        elif tag == "img":
            src = a.get("src") or a.get("data-src") or ""
            rec = {"src": src, "alt": a.get("alt"), "loading": a.get("loading"), "width": a.get("width"), "height": a.get("height"),
                   "srcset": bool(a.get("srcset") or a.get("data-srcset")), "context": self._ctx()}
            self.snap["images"].append(rec)
            if self._anchor is not None:
                self._anchor["img_alt"].append(a.get("alt") or "")
        for attr in ("typeof", "property", "vocab"):
            if attr in a and tag not in ("meta", "link"):
                self.snap["rdfa"][attr] += 1
        if "itemscope" in a:
            item = {"type": a.get("itemtype", ""), "id": a.get("itemid", ""), "props": [], "depth": len(self._micro)}
            self._micro.append({"item": item, "tag": tag, "stack_len": len(self.stack)})
            self.snap["microdata"].append(item)
        if "itemprop" in a and self._micro:
            value = a.get("content") or a.get("href") or a.get("src") or a.get("datetime") or a.get("value")
            self._micro[-1]["item"]["props"].append({"name": a["itemprop"], "value": value, "tag": tag})
        if tag not in VOID:
            self.stack.append(entry)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag == "title":
            self._title = False
        elif tag == "script" and self._script is not None:
            raw = "".join(self._script["buf"])
            data, err = parse_json_ld(raw)
            line, col = self._script["start"]
            self.snap["json_ld"].append({"index": len(self.snap["json_ld"]), "component": self._script["attrs"].get("data-component"),
                                         "line": line, "bytes": len(raw.encode("utf-8")), "data": data, "error": err, "raw": raw})
            self._script = None
        elif re.fullmatch(r"h[1-6]", tag) and self._heading is not None:
            self._heading["text"] = " ".join("".join(self._heading["text"]).split())
            self.snap["headings"].append(self._heading)
            self._heading = None
        elif tag == "a" and self._anchor is not None:
            an = self._anchor
            text = " ".join("".join(an.pop("text")).split())
            an["text"] = text
            an["img_alt"] = " ".join(x for x in an["img_alt"] if x).strip()
            an["absolute"] = urljoin(self.base, an["href"]) if an['href'] and self.base else an["href"]
            self.snap["links"].append(an)
            self._anchor = None
        if tag in VOID:
            return
        while self.stack:
            top = self.stack.pop()
            if top["tag"] == tag:
                break
        while self._micro and len(self.stack) <= self._micro[-1]["stack_len"]:
            self._micro.pop()

    def handle_data(self, data):
        if self._title:
            self.snap["title"] = (self.snap["title"] or "") + data
        if self._script is not None:
            self._script["buf"].append(data)
        if self._heading is not None:
            self._heading["text"].append(data)
        if self._anchor is not None:
            self._anchor["text"].append(data)


def extract(html: str, url: str = "", *, status: int | None = None, headers: dict | None = None):
    """Construye el snapshot. `headers` permite registrar X-Robots-Tag y similares si se capturaron."""
    if len(html.encode('utf-8')) > 10_000_000:
        raise ValueError('HTML supera el límite local de 10 MB.')
    c = _Collector(html, url)
    c.feed(html)
    c.close()
    snap = c.snap
    embedded = _EmbeddedParser()
    embedded.feed(html)
    snap['microdata'], snap['rdfa_entities'], snap['markup_limits'] = embedded.entities()
    snap["title"] = " ".join(snap["title"].split()) if snap["title"] else None
    canonical = [l["href"] for l in snap["links_rel"] if "canonical" in l["rel"].split()]
    snap.update({"url": url, "status": status, "headers": {k.lower(): v for k, v in (headers or {}).items()},
                 "canonical": [urljoin(url, h) if url else h for h in canonical], "html_bytes": len(html.encode("utf-8"))})
    return snap


class _EmbeddedParser(HTMLParser):
    """Subconjunto local de microdata/RDFa Schema.org; no expande contextos remotos."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root={'tag':'root','attrs':{},'children':[],'text':[],'parent':None}
        self.stack=[self.root]
        self.nodes=[]

    def handle_starttag(self, tag, attrs):
        if len(self.nodes)>=50000 or len(self.stack)>256:
            raise ValueError('HTML excede el presupuesto de nodos/profundidad.')
        node={'tag':tag,'attrs':dict(attrs),'children':[],'text':[],'parent':self.stack[-1]}
        self.stack[-1]['children'].append(node);self.nodes.append(node)
        if tag not in VOID:self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag,attrs)
        if tag not in VOID:self.handle_endtag(tag)

    def handle_endtag(self,tag):
        index=next((i for i in range(len(self.stack)-1,0,-1) if self.stack[i]['tag']==tag),None)
        if index is not None:self.stack=self.stack[:index]

    def handle_data(self,data):
        self.stack[-1]['text'].append(data)

    def text(self,node):
        return ' '.join(' '.join(node['text']+ [self.text(c) for c in node['children']]).split())

    def value(self,node):
        a=node['attrs']
        for key in ('content','href','src','datetime','value','resource'):
            if a.get(key) is not None:return a[key]
        return self.text(node)

    def entities(self):
        micro=[];rdfa=[];limits=[];micro_nodes={};rdfa_nodes={};nested_rdfa=set()
        def short(term):return term.rsplit('/',1)[-1].split(':')[-1]
        def add(obj,key,value):
            if key in obj:obj[key]=obj[key]+[value] if isinstance(obj[key],list) else [obj[key],value]
            else:obj[key]=value
        for node in self.nodes:
            a=node['attrs']
            if 'itemscope' in a:
                types=(a.get('itemtype') or '').split()
                item={'type':types,'id':a.get('itemid',''),'props':[],'depth':0,'obj':{'@type':[short(t) for t in types]}}
                if item['id']:item['obj']['@id']=item['id']
                micro_nodes[id(node)]=item;micro.append(item)
                if a.get('itemref'):limits.append('microdata itemref no expandido')
            if a.get('typeof'):
                ancestor=node
                vocab='';prefix=''
                while ancestor:
                    vocab=vocab or ancestor['attrs'].get('vocab','');prefix=prefix or ancestor['attrs'].get('prefix','');ancestor=ancestor['parent']
                terms=a['typeof'].split()
                supported='schema.org' in vocab or 'schema.org' in prefix or all('schema.org/' in t for t in terms)
                if not supported:limits.append('RDFa sin vocabulario Schema.org resuelto');continue
                item={'@type':[short(t) for t in terms]}
                if a.get('about') or a.get('resource'):item['@id']=a.get('about') or a['resource']
                rdfa_nodes[id(node)]=item;rdfa.append(item)
            if a.get('inlist'):limits.append('RDFa inlist no expandido')
        for node in self.nodes:
            a=node['attrs']
            if a.get('itemprop'):
                parent=node['parent']
                while parent and id(parent) not in micro_nodes:parent=parent['parent']
                if parent:
                    item=micro_nodes[id(parent)]
                    value=micro_nodes[id(node)]['obj'] if id(node) in micro_nodes else self.value(node)
                    for prop in a['itemprop'].split():add(item['obj'],prop,value);item['props'].append({'name':prop,'value':value,'tag':node['tag']})
                    if id(node) in micro_nodes:micro_nodes[id(node)]['depth']=item['depth']+1
            if a.get('property'):
                parent=node['parent']
                while parent and id(parent) not in rdfa_nodes:parent=parent['parent']
                if parent:
                    value=rdfa_nodes[id(node)] if id(node) in rdfa_nodes else self.value(node)
                    if id(node) in rdfa_nodes:nested_rdfa.add(id(node))
                    if a.get('resource') and id(node) not in rdfa_nodes:value={'@id':a['resource']}
                    for prop in a['property'].split():add(rdfa_nodes[id(parent)],short(prop),value)
        return micro,[obj for ident,obj in rdfa_nodes.items() if ident not in nested_rdfa],sorted(set(limits))


def host(url: str) -> str:
    return (urlsplit(url).hostname or "").lower()
