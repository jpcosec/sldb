"""The view of one node: the first matching glyph, its label, compartments and style."""

from __future__ import annotations

from typing import Any

from sldb.api.notations.template_render import lookup, matches, render_keyword, render_template
from sldb.api.notations.view_error import ViewError
from sldb.notations.styling import resolve_style


def _pick_glyph(ref: str, payload: dict[str, Any], glyphs: list[dict], model: str) -> dict:
    """The first glyph of `model` whose `where` matches, or ViewError."""
    for glyph in glyphs:
        if glyph["payload"]["model"] == model and matches(glyph["payload"].get("where", ""), payload):
            return glyph
    raise ViewError(f"no glyph of the notation matches {ref} (the last glyph of a model must have no `where`)")


def _compartments(gp: dict[str, Any], payload: dict[str, Any]) -> list[dict[str, Any]]:
    """The non-empty compartments the glyph declares, with their items."""
    found = [(path, lookup(payload, path)) for path in gp.get("compartments") or []]
    return [
        {"path": path, "items": value if isinstance(value, list) else [value]}
        for path, value in found
        if value not in (None, [], {}, "")
    ]


def _markers(markers: list[dict], model: str, payload: dict[str, Any]) -> list[dict[str, Any]]:
    """The markers of `model` whose `where` matches the payload."""
    return [
        {"id": m["id"], "shape": m["shape"]}
        for m in markers
        if m.get("model", "SpecNodeDoc") == model and matches(m.get("where", ""), payload)
    ]


def _identity(ref: str, payload: dict[str, Any]) -> dict[str, Any]:
    """The document's own fields."""
    return {
        "doc": ref,
        "element": payload.get("element", ""),
        "title": payload.get("title", ""),
        "kind": payload.get("kind", ""),
        "collection": payload.get("collection", ""),
        "data": dict(payload.get("data") or {}),
    }


def _glyph_fields(glyph: dict, payload: dict[str, Any]) -> dict[str, Any]:
    """The fields the matching glyph contributes; `label: ""` means no label, only absence falls back to {title}."""
    gp = glyph["payload"]
    label = "{title}" if gp.get("label") is None else gp["label"]
    return {
        "glyph": glyph["ref"],
        "shape": gp.get("shape", ""),
        "function": gp.get("function", ""),
        "label": render_template(label, payload),
        "label_style": gp.get("label_style", ""),
        "keyword": render_keyword(gp.get("keyword", ""), payload),
    }


def node_view(
    ref: str,
    payload: dict[str, Any],
    glyphs: list[dict],
    markers: list[dict],
    model: str = "SpecNodeDoc",
    spec_kinds: dict | None = None,
    palette: dict | None = None,
) -> dict[str, Any]:
    """The resolved node: glyph, label, compartments, markers, refs and style (glyph > spec kinds > palette)."""
    glyph = _pick_glyph(ref, payload, glyphs, model)
    gp = glyph["payload"]
    return {
        **_identity(ref, payload),
        **_glyph_fields(glyph, payload),
        "compartments": _compartments(gp, payload),
        "markers": _markers(markers, model, payload),
        "refs": list(payload.get("refs") or []) + list(payload.get("atom_refs") or []),
        "style": resolve_style(gp, str(payload.get("kind") or ""), spec_kinds, palette),
    }
