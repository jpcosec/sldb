"""The read surface over one SLDB store (its linked stores read through it)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import sldb.api as api
from sldb.mcp.paging import DEFAULT_LIMIT
from sldb.mcp.read import documents, graph, integrity, models, views


class ReadTools:
    """Each method is a thin adapter over `sldb.api`: it shapes the answer as JSON with the
    stable address of every document and pages every set. A question about something the
    store does not declare answers an empty set (or `found: false`) with an `explanation`,
    marked as a signal for the server to log; it is not an opaque error."""

    def __init__(self, store: str | Path) -> None:
        location = api.open_store(Path(store), mode="readonly")
        self.store_path = location.store_path
        self.project_root = location.project_root

    def list_models(self, offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        """List the models the store registers (its own and the inherited ones)."""
        return models.list_models(self.store_path, offset, limit)

    def describe_model(self, model: str, offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        """Describe a model: its fields with their types, and a page of its documents."""
        return models.describe_model(self.store_path, model, offset, limit)

    def list_relation_types(self, offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        """List the relation types of the edge index with their endpoint types."""
        return models.list_relation_types(self.store_path, offset, limit)

    def describe_relation_type(self, name: str) -> dict[str, Any]:
        """Describe one relation type: endpoints, direction, cardinality, description."""
        return models.describe_relation_type(self.store_path, name)

    def read_document(self, ref: str, field: str | None = None) -> dict[str, Any]:
        """Read a document (`Model:name` or `alias:Model:name`): its payload, or one dotted field path."""
        return documents.read_document(self.store_path, ref, field)

    def select_documents(self, model: str | None = None, where: str | None = None, ref: str | None = None, prefix: str | None = None, path_glob: str | None = None, include_linked: bool = False, offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        """Select documents by model, rules-language predicate (`where`), ref, name prefix or path glob."""
        return documents.select_documents(self.store_path, model, where, ref, prefix, path_glob, include_linked, offset, limit)

    def neighbors(self, node: str, direction: str = "outgoing", relation: str | None = None, offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        """Edges leaving (`outgoing`) or reaching (`incoming`) a document or node, optionally of one relation type."""
        return graph.neighbors(self.store_path, node, direction, relation, offset, limit)

    def neighborhood(self, node: str, direction: str = "outgoing", depth: int = 1, offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        """Node ids within `depth` hops in one direction (`outgoing`, `incoming`, `both`), over every relation type."""
        return graph.neighborhood(self.store_path, node, direction, depth, offset, limit)

    def list_views(self, offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        """List the views the store resolves: composed ViewDocs, projection ViewDocs and SpecDocs."""
        return views.list_views(self.store_path, offset, limit)

    def resolve_view(self, view: str, params: dict[str, str] | None = None) -> dict[str, Any]:
        """Resolve a view to JSON: a composed ViewDoc by name, or a ViewDoc/SpecDoc by export id."""
        return views.resolve_view(self.store_path, view, params)

    def check_integrity(self, offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        """Check the store's integrity and its edge index; findings come as one page."""
        return integrity.check_integrity(self.store_path, self.project_root, offset, limit)
