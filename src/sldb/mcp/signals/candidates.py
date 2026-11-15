"""The names a store has, per class of signal: what suggestions are drawn from."""

from __future__ import annotations

from pathlib import Path

import sldb.api as api
from sldb.mcp.read.views import view_items

DOCUMENT_PREFIX = "sldb://document/"


def models(store_path: Path) -> list[str]:
    return [entry.name for entry in api.registered_models(store_path)]


def documents(store_path: Path) -> list[str]:
    return [row["export_id"] for row in api.select_documents(store_path, {"include_linked": True})]


def relations(store_path: Path) -> list[str]:
    return [api.bare(node.id) for node in api.edge_nodes_of_type(store_path, "relation_type")]


def views(store_path: Path) -> list[str]:
    return [item["view"] for item in view_items(store_path)]


LOOKUPS = {"unknown_model": models, "unknown_document": documents, "unknown_relation": relations, "unknown_view": views}


def candidates_for(store_path: Path, signal_class: str) -> list[str]:
    """The names of the kind `signal_class` asks for; classes the store cannot enumerate have none."""
    lookup = LOOKUPS.get(signal_class)
    return lookup(store_path) if lookup else []
