"""Layout and notation styling of an evaluated projection view."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.notations.projection_constants import DOCUMENT_PREFIX
from sldb.api.notations.resolve_documents import resolve_documents

_NODE_KEYS = ("glyph", "shape", "function", "keyword", "label", "style")
_LINK_KEYS = ("link", "draw", "line", "color", "source_end", "target_end", "label")


def view_layout(view: dict[str, Any], documents: list[Any]) -> dict[str, Any]:
    """The view's own layout, else the layout of its notation, else empty."""
    if view.get("layout"):
        return dict(view["layout"])
    notation = str(view.get("notation") or "").split(":", 1)[-1]
    found = next((d for d in documents if d.model_name == "NotationDoc" and d.name == notation), None)
    return dict((found.payload or {}).get("layout") or {}) if found else {}


def _ink(documents: list[Any], palette: str) -> dict[str, str] | None:
    """The ink of the palette as `{light, dark}`."""
    name = str(palette or "").split(":", 1)[-1]
    found = next((d for d in documents if d.model_name == "PaletteDoc" and d.name == name), None)
    ink = (found.payload or {}).get("ink") if found else None
    return {"light": ink, "dark": ink} if isinstance(ink, str) else ink


def _styled_nodes(nodes: list[dict[str, Any]], resolved: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Style fields by node id for the nodes the notation resolved."""
    by_doc = {n["doc"]: n for n in resolved["nodes"]}
    return {
        n["id"]: {k: by_doc[ref].get(k) for k in _NODE_KEYS}
        for n in nodes
        if (ref := f"{n['model']}:{n['name']}") in by_doc
    }


def _plain(ref: str) -> str:
    """The `Model:name` of an edge-index id."""
    return ref[len(DOCUMENT_PREFIX) :] if ref.startswith(DOCUMENT_PREFIX) else ref


def _edge_styles(edges: list[dict[str, Any]], resolved: dict[str, Any]) -> list[dict[str, Any] | None]:
    """The style of each edge, None when the notation drew no such link."""
    links = {(l["source"], l["target"], l["relation"]): l for l in resolved["links"]}
    found = [links.get((_plain(e["source"]), _plain(e["target"]), e["relation_type"])) for e in edges]
    return [{k: link.get(k) for k in _LINK_KEYS} if link else None for link in found]


def _applied(resolved: dict[str, Any], result: dict[str, Any], documents: list[Any]) -> dict[str, Any]:
    """The `notation` block of the evaluated view."""
    return {
        "notation": resolved["notation"],
        "palette": resolved.get("palette") or "",
        "ink": _ink(documents, resolved.get("palette")),
        "nodes": _styled_nodes(result["nodes"], resolved),
        "edges": _edge_styles(result["edges"], resolved),
        "legend": resolved["legend"],
        "skipped": resolved.get("skipped") or [],
    }


def style_with_notation(store: Path, view: dict[str, Any], result: dict[str, Any], documents: list[Any], pythonpath: str | None) -> dict[str, Any]:
    """Applies the view's notation over its nodes and edges."""
    doc_refs = [f"{n['model']}:{n['name']}" for n in result["nodes"]]
    try:
        resolved = resolve_documents(store, str(view["notation"]), doc_refs, pythonpath=pythonpath)
    except Exception as exc:
        return {"error": str(exc)}
    return _applied(resolved, result, documents)
