"""Tokenizador consciente de Liquid y parser estructural HTML basado en Python stdlib para análisis y transformaciones seguras."""
from __future__ import annotations

from dataclasses import dataclass, field
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
from typing import Any

VOID_HTML_TAGS = frozenset({
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
    'link', 'meta', 'param', 'source', 'track', 'wbr',
})

BLOCK_OR_INTERACTIVE_TAGS = frozenset({
    'a', 'address', 'article', 'aside', 'blockquote', 'button', 'details', 'dialog',
    'div', 'dl', 'fieldset', 'figcaption', 'figure', 'footer', 'form', 'h1', 'h2',
    'h3', 'h4', 'h5', 'h6', 'header', 'hr', 'input', 'li', 'main', 'nav', 'ol',
    'p', 'pre', 'section', 'select', 'summary', 'table', 'textarea', 'ul',
})

LIQUID_CONTROL_FLOW_RE = re.compile(
    r'^\{%-?\s*(?:if|elsif|else|endif|unless|endunless|for|endfor|case|when|endcase)\b'
)
_JSX_EXTS = frozenset({'.jsx', '.tsx'})
_JS_TS_EXTS = frozenset({'.js', '.ts', '.mjs', '.cjs'})
_LIQUID_EXTS = frozenset({'.liquid', '.tpl'})


@dataclass
class LiquidSpan:
    start: int
    end: int
    kind: str  # 'output', 'tag', 'comment', 'schema', 'raw'
    raw: str
    is_control_flow: bool = False


@dataclass
class HtmlNode:
    tag: str
    attrs: list[tuple[str, str | None]]
    attr_map: dict[str, str | None]
    line: int
    open_start: int
    open_end: int
    start_tag_raw: str
    self_closing: bool = False
    is_void: bool = False
    close_start: int | None = None
    close_end: int | None = None
    has_liquid_attr: bool = False
    has_jsx_syntax: bool = False
    spans_liquid_branch: bool = False
    misnested: bool = False
    parent: HtmlNode | None = field(default=None, repr=False, compare=False)
    text_chunks: list[str] = field(default_factory=list)
    children: list[HtmlNode] = field(default_factory=list)

    def has_attr(self, name: str) -> bool:
        return name.lower() in self.attr_map

    def get_attr(self, name: str) -> str | None:
        return self.attr_map.get(name.lower())

    def has_ancestor(self, tag_name: str) -> bool:
        cur = self.parent
        target = tag_name.lower()
        while cur is not None:
            if cur.tag == target:
                return True
            cur = cur.parent
        return False

    def collect_visible_text(self) -> str:
        """Recopila texto accesible visible (excluye aria-hidden='true' y elementos vacíos), preservando texto en .sr-only."""
        if str(self.get_attr('aria-hidden') or '').lower() == 'true':
            return ''
        parts = [c for c in self.text_chunks if c.strip()]
        for child in self.children:
            if str(child.get_attr('aria-hidden') or '').lower() == 'true':
                continue
            if child.tag == 'img':
                alt_v = child.get_attr('alt')
                if isinstance(alt_v, str) and alt_v.strip():
                    parts.append(alt_v.strip())
                continue
            if child.tag == 'svg':
                svg_label = child.get_attr('aria-label')
                if isinstance(svg_label, str) and svg_label.strip():
                    parts.append(svg_label.strip())
                continue
            sub = child.collect_visible_text()
            if sub:
                parts.append(sub)
        return ' '.join(parts).strip()

    def iter_descendants(self):
        for child in self.children:
            yield child
            yield from child.iter_descendants()


def find_verified_jsx_ast_parser() -> dict[str, Any]:
    """Comprueba si existe algún parser AST JSX/TSX verificado ya instalado en el entorno, sin instalar nada."""
    probe = (
        "import {createRequire} from 'node:module';\n"
        "import fs from 'node:fs';\n"
        "import path from 'node:path';\n"
        "const reqs = [];\n"
        "for (const base of [process.cwd(), '/usr/lib/node_modules', '/usr/local/lib/node_modules', '/usr/lib/node_modules/@tiendanube/cli/node_modules']) {\n"
        "  if (fs.existsSync(base)) reqs.push(createRequire(path.join(base, '__probe.cjs')));\n"
        "}\n"
        "for (const pkg of ['typescript', '@babel/parser', 'acorn-jsx']) {\n"
        "  for (const r of reqs) { try { const p = r.resolve(pkg); console.log(JSON.stringify({available: true, parser: pkg, path: p})); process.exit(0); } catch {} }\n"
        "}\n"
        "console.log(JSON.stringify({available: false, parser: null}));\n"
    )
    try:
        res = subprocess.run(['node', '--input-type=module', '-e', probe], capture_output=True, text=True, timeout=5)
        if res.returncode == 0 and res.stdout.strip():
            return json.loads(res.stdout.strip().splitlines()[-1])
    except Exception:
        pass
    return {'available': False, 'parser': None}


def classify_source_file(path: str, content: str) -> str:
    """Clasifica el archivo en 'jsx', 'tsx', 'css', 'liquid' o 'html' según extensión y sintaxis real."""
    low_path = path.lower()
    if low_path.endswith('.tsx'):
        return 'tsx'
    if low_path.endswith('.jsx'):
        return 'jsx'
    if low_path.endswith(('.css', '.scss')):
        return 'css'
    if any(low_path.endswith(ext) for ext in _LIQUID_EXTS) or '{{' in content or '{%' in content:
        if low_path.endswith(tuple(_JS_TS_EXTS)):
            return 'tsx' if low_path.endswith('.ts') else 'jsx'
        return 'liquid'
    if low_path.endswith(tuple(_JS_TS_EXTS)):
        if re.search(r'(?:on[A-Z]\w*\s*=\s*\{|className\s*=|return\s*\(?\s*<[A-Za-z])', content):
            return 'tsx' if low_path.endswith('.ts') else 'jsx'
        return 'js'
    if re.search(r'\bclassName\s*=|\bon[A-Z]\w*\s*=\s*\{|=>\s*[^"\']*</', content):
        return 'jsx'
    return 'html'


def _same_len_mask(segment: str, prefix: str) -> str:
    """Devuelve un relleno ASCII sin < > " ' & de exactamente la misma longitud, conservando los saltos de línea."""
    n = len(segment)
    if n == 0:
        return ''
    chars = []
    idx = 0
    for ch in segment:
        if ch == '\n':
            chars.append('\n')
        elif idx < len(prefix):
            chars.append(prefix[idx])
            idx += 1
        else:
            chars.append('l')
    return ''.join(chars)


def _find_matching_liquid_block_end(text: str, start: int, end_tag_name: str) -> int | None:
    pattern = re.compile(r'\{%-?\s*' + re.escape(end_tag_name) + r'\s*-?%\}')
    m = pattern.search(text, start)
    return m.end() if m else None


def mask_liquid_constructs(text: str) -> tuple[str, list[LiquidSpan]]:
    """Enmascara sintaxis Liquid ({{ ... }}, {% ... %}, comment, schema, raw) preservando offsets y líneas exactas."""
    spans: list[LiquidSpan] = []
    out: list[str] = []
    i = 0
    n = len(text)
    counter = 0

    while i < n:
        if text.startswith('{{', i):
            close = text.find('}}', i + 2)
            if close == -1:
                out.append(text[i])
                i += 1
                continue
            end = close + 2
            raw = text[i:end]
            counter += 1
            spans.append(LiquidSpan(i, end, 'output', raw, False))
            out.append(_same_len_mask(raw, f'LIQOUT{counter:04d}'))
            i = end
            continue

        if text.startswith('{%', i):
            close = text.find('%}', i + 2)
            if close == -1:
                out.append(text[i])
                i += 1
                continue
            end = close + 2
            tag_raw = text[i:end]
            block_m = re.match(r'^\{%-?\s*(comment|schema|raw)\b', tag_raw)
            if block_m:
                bname = block_m.group(1)
                block_end = _find_matching_liquid_block_end(text, end, f'end{bname}')
                if block_end is not None:
                    full_raw = text[i:block_end]
                    counter += 1
                    spans.append(LiquidSpan(i, block_end, bname, full_raw, False))
                    # Reemplazar manteniendo longitud/líneas con espacios para no simular un elemento visible
                    out.append(''.join('\n' if ch == '\n' else ' ' for ch in full_raw))
                    i = block_end
                    continue
            counter += 1
            is_flow = bool(LIQUID_CONTROL_FLOW_RE.match(tag_raw))
            spans.append(LiquidSpan(i, end, 'tag', tag_raw, is_flow))
            out.append(''.join('\n' if ch == '\n' else ' ' for ch in tag_raw))
            i = end
            continue

        out.append(text[i])
        i += 1

    return ''.join(out), spans


class _StructuralHTMLParser(HTMLParser):
    def __init__(self, original_text: str, masked_text: str, liquid_spans: list[LiquidSpan]):
        super().__init__(convert_charrefs=False)
        self.original_text = original_text
        self.masked_text = masked_text
        self.liquid_spans = liquid_spans
        self.line_starts = self._build_line_starts(masked_text)
        self.nodes: list[HtmlNode] = []
        self.roots: list[HtmlNode] = []
        self.stack: list[HtmlNode] = []
        self.misnested_events: list[dict[str, Any]] = []
        self.unclosed_tags: list[str] = []

    @staticmethod
    def _build_line_starts(text: str) -> list[int]:
        starts = [0]
        for idx, ch in enumerate(text):
            if ch == '\n':
                starts.append(idx + 1)
        return starts

    def _abs_offset(self, lineno: int, col: int) -> int:
        if lineno - 1 < len(self.line_starts):
            return self.line_starts[lineno - 1] + col
        return len(self.masked_text)

    def _liquid_overlapping(self, start: int, end: int) -> list[LiquidSpan]:
        return [s for s in self.liquid_spans if not (s.end <= start or s.start >= end)]

    def _create_node(self, tag: str, attrs: list[tuple[str, str | None]], self_closing: bool) -> HtmlNode:
        lineno, col = self.getpos()
        abs_start = self._abs_offset(lineno, col)
        raw_masked = self.get_starttag_text() or ''
        abs_end = abs_start + len(raw_masked)
        orig_start_tag = self.original_text[abs_start:abs_end]
        attr_map: dict[str, str | None] = {}
        for k, v in attrs:
            kl = k.lower()
            if kl not in attr_map:
                # Restaurar valores originales si tenían Liquid enmascarado
                attr_map[kl] = v
        # Recuperar valores originales exactos desde orig_start_tag cuando hay Liquid en el tag
        overlapping_lq = self._liquid_overlapping(abs_start, abs_end)
        has_liquid_attr = bool(overlapping_lq)
        if has_liquid_attr:
            for k in list(attr_map):
                m_attr = re.search(
                    r'(?:^|\s)' + re.escape(k) + r'\s*=\s*(?:"([^"]*)"|\'([^\']*)\')',
                    orig_start_tag,
                    re.I,
                )
                if m_attr:
                    attr_map[k] = m_attr.group(1) if m_attr.group(1) is not None else m_attr.group(2)

        # Comprobar expresiones JSX fuera de bloques Liquid {{ ... }} / {% ... %}
        unmasked_no_liquid = orig_start_tag
        for s in reversed(overlapping_lq):
            if abs_start <= s.start and s.end <= abs_end:
                rel_s = s.start - abs_start
                rel_e = s.end - abs_start
                unmasked_no_liquid = unmasked_no_liquid[:rel_s] + unmasked_no_liquid[rel_e:]
        has_jsx = bool(re.search(r'=\s*\{|=>', unmasked_no_liquid))

        is_void = tag.lower() in VOID_HTML_TAGS
        node = HtmlNode(
            tag=tag.lower(),
            attrs=[(k.lower(), attr_map[k.lower()]) for k, _ in attrs],
            attr_map=attr_map,
            line=lineno,
            open_start=abs_start,
            open_end=abs_end,
            start_tag_raw=orig_start_tag,
            self_closing=self_closing or raw_masked.rstrip().endswith('/>'),
            is_void=is_void,
            close_start=abs_end if (self_closing or is_void) else None,
            close_end=abs_end if (self_closing or is_void) else None,
            has_liquid_attr=has_liquid_attr,
            has_jsx_syntax=has_jsx,
            parent=self.stack[-1] if self.stack else None,
        )
        self.nodes.append(node)
        if self.stack:
            self.stack[-1].children.append(node)
        else:
            self.roots.append(node)
        if not (node.self_closing or node.is_void):
            self.stack.append(node)
        return node

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._create_node(tag, attrs, self_closing=False)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._create_node(tag, attrs, self_closing=True)

    def handle_endtag(self, tag: str) -> None:
        tl = tag.lower()
        if tl in VOID_HTML_TAGS:
            return
        lineno, col = self.getpos()
        abs_start = self._abs_offset(lineno, col)
        m_close = re.match(r'</\s*' + re.escape(tag) + r'\s*>', self.masked_text[abs_start:], re.I)
        abs_end = abs_start + (len(m_close.group(0)) if m_close else len(f'</{tag}>'))
        # Buscar coincidencia en pila
        for pos in range(len(self.stack) - 1, -1, -1):
            if self.stack[pos].tag == tl:
                if pos != len(self.stack) - 1:
                    # Hay elementos abiertos sin cerrar antes -> etiquetas cruzadas / desbalanceadas
                    for unclosed in self.stack[pos + 1:]:
                        unclosed.misnested = True
                    self.stack[pos].misnested = True
                    self.misnested_events.append({'tag': tl, 'line': lineno})
                node = self.stack[pos]
                node.close_start = abs_start
                node.close_end = abs_end
                if any(s.is_control_flow for s in self._liquid_overlapping(node.open_start, abs_end)):
                    node.spans_liquid_branch = True
                del self.stack[pos:]
                return
        self.misnested_events.append({'orphan_end_tag': tl, 'line': lineno})

    def handle_data(self, data: str) -> None:
        if self.stack:
            lineno, col = self.getpos()
            abs_start = self._abs_offset(lineno, col)
            orig_slice = self.original_text[abs_start:abs_start + len(data)]
            self.stack[-1].text_chunks.append(orig_slice)

    def finalize(self) -> None:
        for leftover in self.stack:
            leftover.misnested = True
            self.unclosed_tags.append(leftover.tag)


@dataclass
class ParsedDocument:
    file_kind: str
    nodes: list[HtmlNode]
    roots: list[HtmlNode]
    liquid_spans: list[LiquidSpan]
    balanced: bool
    misnested_events: list[dict[str, Any]]
    unclosed_tags: list[str]
    jsx_parser_info: dict[str, Any]


def parse_structural_document(path: str, content: str) -> ParsedDocument:
    """Analiza estructuralmente un archivo HTML/Liquid preservando posiciones exactas, o identifica JSX/TSX/CSS."""
    file_kind = classify_source_file(path, content)
    jsx_info = find_verified_jsx_ast_parser() if file_kind in ('jsx', 'tsx') else {'available': False, 'parser': None}
    masked, liquid_spans = mask_liquid_constructs(content)
    parser = _StructuralHTMLParser(content, masked, liquid_spans)
    parser.feed(masked)
    parser.close()
    parser.finalize()
    return ParsedDocument(
        file_kind=file_kind,
        nodes=parser.nodes,
        roots=parser.roots,
        liquid_spans=liquid_spans,
        balanced=(not parser.misnested_events and not parser.unclosed_tags),
        misnested_events=parser.misnested_events,
        unclosed_tags=parser.unclosed_tags,
        jsx_parser_info=jsx_info,
    )


def apply_text_edits(content: str, edits: list[tuple[int, int, str]]) -> tuple[str, bool]:
    """Aplica reemplazos de rangos [start, end) verificando no-solapamiento estricto."""
    if not edits:
        return content, True
    ordered = sorted(edits, key=lambda e: (e[0], e[1]))
    for a, b in zip(ordered, ordered[1:]):
        if a[1] > b[0]:
            return content, False
    out = content
    for start, end, repl in reversed(ordered):
        out = out[:start] + repl + out[end:]
    return out, True
