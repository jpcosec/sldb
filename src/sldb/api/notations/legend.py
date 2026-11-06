"""The resolved legend of a notation: glyphs, links and kinds styled by spec or palette."""

from __future__ import annotations

from typing import Any

from sldb.notations.styling import resolve_line_color, resolve_style

_DRAWING = {"draw": "line", "line": "solid", "source_end": "none", "target_end": "open-arrow"}


def _kind_entry(style: dict[str, Any], kind: str, palette: dict | None) -> dict[str, Any]:
    """The legend entry of a kind, with the palette's shape when it declares one."""
    entry = dict(style)
    reference = ((palette or {}).get("kinds") or {}).get(kind) or {}
    if reference.get("shape"):
        entry["shape"] = reference["shape"]
    return entry


def _kinds(nodes: list[dict], palette: dict | None) -> dict[str, dict[str, Any]]:
    """The first styled node of each kind whose style comes from the spec or the palette."""
    kinds: dict[str, dict[str, Any]] = {}
    for node in nodes:
        style = node.get("style") or {}
        if node.get("kind") and set((style.get("source") or {}).values()) & {"spec", "palette"} and node["kind"] not in kinds:
            kinds[node["kind"]] = _kind_entry(style, node["kind"], palette)
    return kinds


def _glyph_entry(g: dict, palette: dict | None) -> dict[str, Any]:
    """The legend entry of one glyph."""
    return {
        "glyph": g["ref"],
        "title": g["payload"].get("title", ""),
        "shape": g["payload"].get("shape", ""),
        "function": g["payload"].get("function", ""),
        "style": resolve_style(g["payload"], "", None, palette),
    }


def _link_entry(l: dict, palette: dict | None) -> dict[str, Any]:
    """The legend entry of one link."""
    p = l["payload"]
    return {
        "link": l["ref"],
        "title": p.get("title", ""),
        "relation": p.get("relation", ""),
        **{k: p.get(k, d) for k, d in _DRAWING.items()},
        "color": resolve_line_color(p, palette),
    }


def legend(glyphs: list[dict], links: list[dict], nodes: list[dict], palette: dict | None) -> dict[str, Any]:
    """The resolved legend of the notation: glyphs, links, and kinds styled by spec or palette."""
    return {
        "glyphs": [_glyph_entry(g, palette) for g in glyphs],
        "links": [_link_entry(l, palette) for l in links],
        "kinds": [{"kind": k, **v} for k, v in _kinds(nodes, palette).items()],
    }
