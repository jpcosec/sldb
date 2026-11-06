"""Projection views: evaluate, list, and save ViewDoc projections in an SLDB store.

A ViewDoc names models, `where` predicates, relation types, and an optional notation.
When a notation is specified, `resolve_documents` is applied over the matching nodes and edges.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.notations.notation_view import ViewError, resolve_documents

VIEW_MODEL = "ViewDoc"
DIRECTIONS = ("both", "outgoing", "incoming")
DOCUMENT_PREFIX = "sldb://document/"
VIEWS_DIR = Path("sldb") / "views"


def node_id(model: str, name: str) -> str:
    """The edge-index id of a document: ``sldb://document/<Model>:<name>``."""
    return f"{DOCUMENT_PREFIX}{model}:{name}"


def _entries(view: dict[str, Any]) -> list[dict[str, str]]:
    entries = view.get("nodes") or []
    if not isinstance(entries, list) or not all(isinstance(e, dict) and e.get("model") for e in entries):
        raise ViewError("nodes must be a list of {model, where}")
    return [{"model": str(e["model"]), "where": str(e.get("where") or "")} for e in entries]


def _selected(doc: Any, entries: list[dict[str, str]]) -> bool:
    if not entries:
        return True
    from sldb.api.where import where_matches

    try:
        payload = doc.payload or {}
        # flatten payload with data keys if needed
        data = payload.get("data") or {}
        flat = dict(payload)
        if isinstance(data, dict):
            for k, v in data.items():
                flat.setdefault(k, v)
        return any(e["model"] == doc.model_name and where_matches(e["where"], flat) for e in entries)
    except Exception as exc:
        raise ViewError(f"where does not parse: {exc}") from exc


def _relation_filter(view: dict[str, Any]) -> tuple[list[str], str]:
    relations = view.get("relations") or []
    direction = view.get("direction") or "both"
    if not isinstance(relations, list) or direction not in DIRECTIONS:
        raise ViewError(f"relations must be a list and direction one of {', '.join(DIRECTIONS)}")
    return [str(r) for r in relations], direction


def _title(doc: Any) -> str:
    payload = doc.payload or {}
    return str(payload.get("title") or payload.get("name") or doc.name)


def _layout(view: dict[str, Any], documents: list[Any]) -> dict[str, Any]:
    if view.get("layout"):
        return dict(view["layout"])
    notation = str(view.get("notation") or "").split(":", 1)[-1]
    found = next((d for d in documents if d.model_name == "NotationDoc" and d.name == notation), None)
    return dict((found.payload or {}).get("layout") or {}) if found else {}


def _ink(documents: list[Any], palette: str) -> dict[str, str] | None:
    name = str(palette or "").split(":", 1)[-1]
    found = next((d for d in documents if d.model_name == "PaletteDoc" and d.name == name), None)
    ink = (found.payload or {}).get("ink") if found else None
    return {"light": ink, "dark": ink} if isinstance(ink, str) else ink


def _style_with_notation(
    store: Path,
    view: dict[str, Any],
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    documents: list[Any],
    pythonpath: str | None,
) -> dict[str, Any]:
    """Applies the view's notation over its nodes and edges."""
    notation_ref = str(view["notation"])
    doc_refs = [f"{n['model']}:{n['name']}" for n in nodes]
    try:
        resolved = resolve_documents(store, notation_ref, doc_refs, pythonpath=pythonpath)
    except Exception as exc:
        return {"error": str(exc)}

    by_doc = {n["doc"]: n for n in resolved["nodes"]}
    keys = ("glyph", "shape", "function", "keyword", "label", "style")
    styled_nodes = {
        n["id"]: {k: by_doc[ref].get(k) for k in keys}
        for n in nodes
        if (ref := f"{n['model']}:{n['name']}") in by_doc
    }
    links = {(l["source"], l["target"], l["relation"]): l for l in resolved["links"]}

    def plain(ref: str) -> str:
        return ref[len(DOCUMENT_PREFIX) :] if ref.startswith(DOCUMENT_PREFIX) else ref

    link_keys = ("link", "draw", "line", "color", "source_end", "target_end", "label")
    edge_styles = [
        {k: link.get(k) for k in link_keys}
        if (link := links.get((plain(e["source"]), plain(e["target"]), e["relation_type"])))
        else None
        for e in edges
    ]

    return {
        "notation": resolved["notation"],
        "palette": resolved.get("palette") or "",
        "ink": _ink(documents, resolved.get("palette")),
        "nodes": styled_nodes,
        "edges": edge_styles,
        "legend": resolved["legend"],
        "skipped": resolved.get("skipped") or [],
    }


def evaluate_projection_view(
    store: Path | str,
    view_or_ref: dict[str, Any] | str,
    pythonpath: str | None = None,
) -> dict[str, Any]:
    """Evaluates a projection view over `store`.

    `view_or_ref` can be a ViewDoc reference (e.g. 'ViewDoc:arch' or 'arch') or a view dict.
    Returns `{view, nodes, edges, layout, [notation]}`.
    """
    store_path = Path(store)
    import sldb.api as api
    from sldb.api.graph import RelationFilter, StructuredQuery, execute_query

    documents = api.load_runtime_documents(store_path, pythonpath, include_linked=False)

    if isinstance(view_or_ref, str):
        target_name = view_or_ref.split(":", 1)[-1]
        found = next((d for d in documents if d.model_name == VIEW_MODEL and d.name == target_name), None)
        if found is None:
            raise ViewError(f"ViewDoc '{view_or_ref}' is not in the store")
        view = dict(found.payload or {})
    else:
        view = dict(view_or_ref)

    entries = _entries(view)
    relations, direction = _relation_filter(view)

    selected = {node_id(d.model_name, d.name): d for d in documents if _selected(d, entries)}

    seen: set[tuple[str, str, str]] = set()
    if relations:
        query = StructuredQuery(relations=[RelationFilter(relation_types=relations, direction=direction)])
        for n in execute_query(store_path, query, include_linked=False):
            for e in n.edges:
                if n.id in selected and e.source in selected and e.target in selected:
                    seen.add((e.source, e.target, e.relation))
    else:
        # If no relations filter specified, gather all edges between selected documents from index
        edge_index = api.load_edge_index(store_path)
        for doc_id in selected:
            for edge in edge_index.edges_from(doc_id):
                if edge.target in selected:
                    seen.add((edge.source, edge.target, edge.relation))

    result = {
        "view": view,
        "nodes": [
            {"id": key, "model": d.model_name, "name": d.name, "title": _title(d), "payload": d.payload}
            for key, d in sorted(selected.items())
        ],
        "edges": [{"source": s, "target": t, "relation_type": r} for s, t, r in sorted(seen)],
        "layout": _layout(view, documents),
    }

    if view.get("notation"):
        result["notation"] = _style_with_notation(
            store_path, view, result["nodes"], result["edges"], documents, pythonpath
        )

    return result


def list_projection_views(
    store: Path | str,
    pythonpath: str | None = None,
) -> list[dict[str, Any]]:
    """List all `ViewDoc`s in the store as `[{ref, payload}]`."""
    store_path = Path(store)
    import sldb.api as api

    documents = api.load_runtime_documents(store_path, pythonpath, include_linked=False)
    return [
        {"ref": f"{VIEW_MODEL}:{d.name}", "payload": d.payload}
        for d in sorted(documents, key=lambda d: d.name)
        if d.model_name == VIEW_MODEL
    ]


def save_projection_view(
    store: Path | str,
    name: str,
    view: dict[str, Any],
    pythonpath: str | None = None,
    actor: str | None = None,
) -> dict[str, Any]:
    """Save or update a `ViewDoc` in the store."""
    store_path = Path(store)
    import sldb.api as api

    clean_name = name.split(":", 1)[-1]
    # Ensure ViewDoc model registered
    try:
        api.load_registered_model(store_path, VIEW_MODEL, pythonpath)
    except Exception:
        api.add_model(store_path, "sldb.models.notation_models:ViewDoc", pythonpath, actor=actor)

    open_res = api.open_store(store_path)
    root = Path(open_res.project_root).resolve()
    target_path = root / VIEWS_DIR / f"{clean_name}.md"

    # Validate view structure
    _entries(view)
    _relation_filter(view)

    payload = dict(view)
    payload.setdefault("id", clean_name)
    payload.setdefault("name", clean_name)
    payload.setdefault("title", clean_name)

    exists = api.doc_exists(store_path, f"{VIEW_MODEL}/{clean_name}")
    if exists:
        api.save_document_payload(store_path, VIEW_MODEL, clean_name, payload, pythonpath=pythonpath, actor=actor)
    else:
        api.create_document(store_path, VIEW_MODEL, target_path, payload, name=clean_name, pythonpath=pythonpath, actor=actor)

    return {"ref": f"{VIEW_MODEL}:{clean_name}", "saved": True}


__all__ = [
    "evaluate_projection_view",
    "list_projection_views",
    "save_projection_view",
    "ViewError",
    "node_id",
]
