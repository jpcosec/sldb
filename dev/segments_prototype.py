"""Prototipo de referencia: segmentos de un documento SLDB por render instrumentado.

NO es código para commitear tal cual: parchea el renderer en runtime para probar el
diseño sin tocar el repo. La implementación real (ver HANDOFF) mete el recorder como
dependencia explícita del renderer.

Idea: durante el render, cada marcador emite su valor envuelto en centinelas de uso
privado (U+E000..U+E002) con un id. Un post-proceso quita los centinelas y registra
los offsets de carácter en el texto canónico. Como el render es la inversa del
extract, los offsets son exactos por construcción.
"""

from __future__ import annotations

import contextvars
import difflib
from pathlib import Path
from typing import Any

from sldb.core.handlers.utils import parse_marker
from sldb.core.renderer import SLDBRenderer
from sldb.core.renderer_engine.base import BaseRenderer
from sldb.core.renderer_engine.list import ListRenderer
from sldb.core.renderer_engine.yaml import YamlRenderer
from sldb.models.structured_doc import StructuredNLDoc

OPEN, SEP, CLOSE = "\ue000", "\ue001", "\ue002"
_recorder: contextvars.ContextVar[list[dict] | None] = contextvars.ContextVar("rec", default=None)
_compositions: contextvars.ContextVar[dict] = contextvars.ContextVar("compositions", default={})
_prefix: contextvars.ContextVar[tuple[str, str | None]] = contextvars.ContextVar("prefix", default=("", None))


def _wrap(text: str, meta: dict) -> str:
    rec = _recorder.get()
    if rec is None:
        return text
    rec.append(meta)
    return f"{OPEN}{len(rec) - 1}{SEP}{text}{CLOSE}"


# --- instrumentación -----------------------------------------------------------

_orig_sub = BaseRenderer._sub_marker
_orig_items = ListRenderer._render_items
_orig_fm_line = YamlRenderer._render_frontmatter_line
_orig_compose = StructuredNLDoc.compose_field


def _sub_marker(self, match, data):
    out = _orig_sub(self, match, data)
    if _recorder.get() is None or out == match.group(0):
        return out
    marker = parse_marker(match.group(1))
    prefix, scalar_root = _prefix.get()
    if not prefix:
        path = marker.name
    elif scalar_root == marker.name:
        path = prefix
    else:
        path = f"{prefix}/{marker.name}"
    meta = {"path": path, "marker": marker.kind, "traits": marker.traits}
    spec = _compositions.get().get(marker.name) if marker.kind == "render" else None
    if spec:
        meta["composition"] = {"name": marker.name, "source_field": spec.get("source_field"),
                               "model": _model_label(spec.get("model")), "ref": "document"}
    return _wrap(out, meta)


def _model_label(value):
    if isinstance(value, type):
        return value.__name__
    return str(value).split(":")[-1] if value else None


def _render_items(self, item_text, list_items, root_prop):
    if _recorder.get() is None or not isinstance(list_items, list) or not list_items:
        return _orig_items(self, item_text, list_items, root_prop)
    parts = []
    for i, item in enumerate(list_items):
        scalar = None if isinstance(item, dict) else root_prop
        token = _prefix.set((f"{root_prop}/{i}", scalar))
        try:
            d = item if isinstance(item, dict) else {root_prop: item}
            parts.append(self.replace_markers(item_text, d))
        finally:
            _prefix.reset(token)
    return "\n".join(parts)


def _render_frontmatter_line(self, line, data):
    from sldb.core.renderer_engine.yaml import _FRONTMATTER_OPTREV_KEY
    out = _orig_fm_line(self, line, data)
    match = _FRONTMATTER_OPTREV_KEY.match(line)
    if _recorder.get() is None or out is None or match is None or OPEN in out:
        return out
    key, marker = match.group(1), parse_marker(match.group(2))
    head = f"{key}:"
    rest = out[len(head):]
    lead = len(rest) - len(rest.lstrip(" "))
    meta = {"path": marker.name, "marker": marker.kind, "traits": marker.traits}
    return head + rest[:lead] + _wrap(rest[lead:], meta)


def _compose_field(self, name):
    if _recorder.get() is None:
        return _orig_compose(self, name)
    spec = self.__compositions__.get(name, {})
    refs = getattr(self, spec.get("source_field") or "", []) or []
    model_type = self._resolve_composition_model(spec.get("model"))
    if not spec.get("source_field") or not isinstance(refs, list) or model_type is None:
        return ""
    pieces = [_compose_piece(self, spec, model_type, ref, i) for i, ref in enumerate(refs)]
    return spec.get("separator", "\n").join(p for p in pieces if p)


def _compose_piece(doc, spec, model_type, raw_ref, index):
    from sldb.runtime.validation import Validator
    path = Path(str(raw_ref).strip().strip("`"))
    if not path.exists():
        return ""
    payload = doc._extract_composed_payload(model_type, path)
    source = {"path": str(raw_ref), "model": model_type.__name__, "doc": None}
    rev = Validator(model_type)._get_rev_fields()
    wrapped = {k: _wrap(str(v), {"path": k, "marker": "rev" if k in rev else "render", "traits": [],
                                  "source": source}) if isinstance(v, str) else v
               for k, v in payload.items()}
    body = spec.get("template", "- {title}").format(**wrapped)
    return _wrap(body, {"path": "", "marker": "compose", "traits": [], "source": source,
                        "piece": True, "ref_index": index, "ref": str(raw_ref)})


BaseRenderer._sub_marker = _sub_marker
ListRenderer._render_items = _render_items
YamlRenderer._render_frontmatter_line = _render_frontmatter_line
StructuredNLDoc.compose_field = _compose_field


# --- decodificación --------------------------------------------------------------

def _decode(raw: str) -> tuple[str, list[tuple[int, int, int]]]:
    out, spans, stack, i = [], [], [], 0
    while i < len(raw):
        ch = raw[i]
        if ch == OPEN:
            j = raw.index(SEP, i)
            stack.append((int(raw[i + 1:j]), len(out)))
            i = j + 1
            continue
        if ch == CLOSE:
            sid, start = stack.pop()
            spans.append((sid, start, len(out)))
        else:
            out.append(ch)
        i += 1
    return "".join(out), spans


def _strip_with_offsets(text, spans):
    lead = len(text) - len(text.lstrip())
    stripped = text.strip()
    clamp = lambda x: max(0, min(len(stripped), x - lead))
    return stripped, [(sid, clamp(s), clamp(e)) for sid, s, e in spans]


def render_with_spans(model_type: type[StructuredNLDoc], payload: dict[str, Any]):
    """Texto canónico + lista de (meta, start, end)."""
    rec: list[dict] = []
    token = _recorder.set(rec)
    ctoken = _compositions.set(dict(getattr(model_type, "__compositions__", {}) or {}))
    try:
        r = SLDBRenderer()
        model = model_type(**payload)
        blocks = r.ast_handler.split_nodes(model.__template__)
        parts = r._render_blocks(blocks, model.__template__.splitlines(), model.render_payload())
        raw = "\n\n".join(parts)
    finally:
        _recorder.reset(token)
        _compositions.reset(ctoken)
    text, spans = _decode(raw)
    text, spans = _strip_with_offsets(text, spans)
    return text, [({**rec[sid], "_order": sid}, s, e) for sid, s, e in spans]


# --- árbol de segmentos -----------------------------------------------------------

def _value_at(payload: Any, path: str) -> Any:
    cur = payload
    for part in [p for p in path.split("/") if p]:
        if isinstance(cur, list) and part.isdigit() and int(part) < len(cur):
            cur = cur[int(part)]
        elif isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur


def _display(text: str, start: int, end: int) -> str:
    starts_line = start == 0 or text[start - 1] == "\n"
    ends_line = end == len(text) or text[end] == "\n"
    own_block = (start == 0 or text[max(0, start - 2):start] == "\n\n") and \
                (end == len(text) or text[end:end + 2] == "\n\n")
    return "block" if starts_line and ends_line and own_block else "inline"


def _field_kind(model_type, path: str) -> str:
    from sldb.api.schema.field_kinds import field_kind, unwrap_annotation
    parts = path.split("/")
    info = model_type.model_fields.get(parts[0])
    if info is None:
        return "unknown"
    kind = field_kind(unwrap_annotation(info.annotation))
    if len(parts) >= 2 and parts[1].isdigit():
        return {"stringlist": "string", "enumlist": "enum"}.get(kind, "unknown")
    return kind


def _node(meta, start, end, text, model_type, payload):
    marker = meta["marker"]
    source = meta.get("source")
    node = {
        "type": "composition" if meta.get("piece") else "field",
        "start": start, "end": end, "text": text[start:end],
        "path": meta["path"], "marker": marker, "traits": meta["traits"],
        "editable": marker in ("rev", "optrev"),
        "display": _display(text, start, end),
        "source": source, "children": [], "_order": meta["_order"],
    }
    for extra in ("composition", "ref_index", "ref"):
        if extra in meta:
            node[extra] = meta[extra]
    if node["type"] == "field" and source is None:
        node["kind"] = _field_kind(model_type, meta["path"])
        node["value"] = _value_at(payload, meta["path"])
    return node


def _nest(nodes):
    # A igual tramo, el que se envolvió después es el de afuera.
    nodes = sorted(nodes, key=lambda n: (n["start"], -n["end"], -n["_order"]))
    roots, stack = [], []
    for n in nodes:
        while stack and not (stack[-1]["start"] <= n["start"] and n["end"] <= stack[-1]["end"]):
            stack.pop()
        (stack[-1]["children"] if stack else roots).append(n)
        stack.append(n)
    return roots


def _with_literals(nodes, text, lo, hi):
    out, cur = [], lo
    for n in nodes:
        n.pop("_order", None)
        if n["start"] > cur:
            out.append({"type": "literal", "start": cur, "end": n["start"], "text": text[cur:n["start"]]})
        n["children"] = _with_literals(n["children"], text, n["start"], n["end"]) if n["children"] else []
        out.append(n)
        cur = max(cur, n["end"])
    if cur < hi:
        out.append({"type": "literal", "start": cur, "end": hi, "text": text[cur:hi]})
    return out


def document_segments(model_type, payload, *, doc=None, source_text=None, resolve_doc=None):
    """Contrato `DocumentSegments` (ver HANDOFF §3)."""
    text, spans = render_with_spans(model_type, payload)
    for meta, _, _ in spans:
        if meta.get("source") is not None and resolve_doc is not None:
            meta["source"]["doc"] = resolve_doc(meta["source"]["path"])
    nodes = [_node(m, s, e, text, model_type, payload) for m, s, e in spans]
    return {
        "doc": doc, "model": model_type.__name__, "text": text,
        "canonical": None if source_text is None else text == source_text.strip(),
        "segments": _with_literals(_nest(nodes), text, 0, len(text)),
    }


# --- extracción sobre texto crudo ------------------------------------------------------

def _align(canonical: str, raw: str):
    sm = difflib.SequenceMatcher(None, canonical, raw, autojunk=False)
    return sm.get_opcodes()


def _map_offset(ops, pos, side_end=False):
    for tag, i1, i2, j1, j2 in ops:
        if i1 <= pos < i2 or (side_end and i1 < pos <= i2):
            if tag == "equal":
                return j1 + (pos - i1), True
            return (j2 if side_end else j1), False
    return (ops[-1][4] if ops else 0), False


def _trimmed(text: str, start: int, end: int) -> dict:
    chunk = text[start:end]
    start += len(chunk) - len(chunk.lstrip())
    end -= len(chunk) - len(chunk.rstrip())
    return {"start": start, "end": end, "text": text[start:end]}


def extraction_segments(model_type, raw_markdown: str):
    """Contrato `ExtractionSegments`: atoms detectados sobre el texto crudo."""
    from sldb.runtime.validation import extract_model_data
    payload = extract_model_data(model_type, raw_markdown)
    canonical = document_segments(model_type, payload)
    ops = _align(canonical["text"], raw_markdown)
    fields = []

    def walk(segs):
        for s in segs:
            if s["type"] == "field":
                a, ok_a = _map_offset(ops, s["start"])
                b, ok_b = _map_offset(ops, s["end"], side_end=True)
                fields.append({**{k: v for k, v in s.items() if k not in ("children", "start", "end", "text")},
                               "start": a, "end": b, "text": raw_markdown[a:b],
                               "alignment": "exact" if ok_a and ok_b else "approximate"})
            walk(s.get("children", []))

    walk(canonical["segments"])
    fields.sort(key=lambda f: f["start"])
    covered = sum(max(0, f["end"] - f["start"]) for f in fields if f["start"] < f["end"])
    body = len(raw_markdown.strip()) or 1
    unmatched = [_trimmed(raw_markdown, j1, j2) for tag, _, _, j1, j2 in ops
                 if tag in ("insert", "replace") and raw_markdown[j1:j2].strip()]
    return {
        "model": model_type.__name__, "text": raw_markdown, "payload": payload, "unmatched": unmatched,
        "canonical_text": canonical["text"], "fields": fields,
        "coverage": round(min(1.0, covered / body), 4),
    }
