"""Views the store resolves."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import sldb.api as api
from sldb.mcp.addresses import addressed_row, document_address, row_alias
from sldb.mcp.paging import page
from sldb.mcp.read.miss import missing


def view_items(store_path: Path) -> list[dict[str, Any]]:
    """Composed ViewDocs (by name), projection ViewDocs and SpecDocs (by export id), local and linked."""
    items: list[dict[str, Any]] = [{"kind": "composed", "view": v["name"], **v} for v in api.list_views(store_path)]
    items += [{"kind": "projection", "view": v["ref"], "address": document_address(v["ref"])} for v in api.list_projection_views(store_path)]
    specs = api.select_documents(store_path, {"model": "SpecDoc", "include_linked": True})
    return items + [{"kind": "spec", "view": r["export_id"], **addressed_row(r)} for r in specs]


def list_views(store_path: Path, offset: int, limit: int) -> dict[str, Any]:
    """The views the store can resolve."""
    items = view_items(store_path)
    return page(items, offset, limit, None if items else "the store holds no ViewDoc and no SpecDoc")


def store_of(store_path: Path, alias: str | None) -> Path:
    """The store a document lives in: this one, or the linked store recorded under `alias`."""
    if alias is None:
        return store_path
    link = next((link for link in api.store_links(store_path) if link["name"] == alias), None)
    if link is None or link.get("status") != "ok":
        raise ValueError(f"the linked store {alias!r} is not readable: {link}")
    return Path(link["resolved"])


def resolve_document_view(store_path: Path, view: str, row: dict[str, Any]) -> dict[str, Any]:
    """A SpecDoc (by its notation) or a projection ViewDoc, resolved."""
    store = store_of(store_path, row_alias(row))
    base = {"found": True, "view": view, "address": document_address(row["export_id"]), "export_id": row["export_id"]}
    if row["model"] == "SpecDoc":
        return {**base, "kind": "spec", "result": api.resolve_view(store, f"SpecDoc:{row['name']}")}
    if row["model"] == "ViewDoc":
        return {**base, "kind": "projection", "result": api.evaluate_projection_view(store, f"ViewDoc:{row['name']}")}
    return {"found": False, "view": view, "export_id": row["export_id"], "explanation": f"{row['export_id']} is a {row['model']}, not a ViewDoc or a SpecDoc"}


def resolve_view(store_path: Path, view: str, params: dict[str, str] | None = None) -> dict[str, Any]:
    """A view resolved to JSON: a composed ViewDoc by name (`run_view`), a projection ViewDoc
    (`evaluate_projection_view`) or a SpecDoc according to its notation (`resolve_view`)."""
    if view in {v["name"] for v in api.list_views(store_path)}:
        return {"found": True, "kind": "composed", "view": view, "result": api.run_view(store_path, view, params)}
    rows = api.select_documents(store_path, {"ref": view})
    if len(rows) == 1:
        return resolve_document_view(store_path, view, rows[0])
    why = "names no composed view and no document" if not rows else f"names {len(rows)} documents"
    answer = {"found": False, "view": view, "explanation": f"{view!r} {why}; list_views names the views the store can resolve"}
    return missing("unknown_view", view, answer) if not rows else answer
