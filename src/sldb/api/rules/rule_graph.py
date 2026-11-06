"""The store a rule is evaluated over: its edge index (with its linked stores), loaded once into
the store's `GraphBackend`, and which documents are the local store's own."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sldb.api.edges.edge_reading import load_edge_index
from sldb.api.graph.analyze import backend_for
from sldb.api.stores.open_store import open_store
from sldb.store.edge_index.node_ids import bare, kind


@dataclass(frozen=True)
class RuleGraph:
    """`eval` over one store: `holds` is the finding of a predicate on one document."""

    backend: Any
    index: Any
    local: frozenset[str]
    store_path: Path

    def holds(self, predicate: str, node: str) -> dict[str, Any]:
        """The eval finding (node, holds, clause, seen) of `predicate` on the document `node`."""
        return self.backend.eval(predicate, node)[0]

    def domain(self, predicate: str) -> list[str]:
        """The local documents `predicate` holds on, over its domain (rules-language.md §6)."""
        return [f["node"] for f in self.backend.eval(predicate) if f["holds"] == "true" and f["node"] in self.local]

    def semantics(self, node: str) -> dict[str, Any]:
        """What the index records of a document: its name, model and path."""
        record = self.index.node(node)
        return dict(record.semantics) if record is not None else {}

    def payload(self, node: str) -> dict[str, Any]:
        record = self.index.node(node)
        return dict(record.payload) if record is not None else {}


def rule_graph(store: str | Path | None) -> RuleGraph:
    """The store's graph with its linked stores, every document's projection loaded."""
    index = load_edge_index(store, True)
    store_path = open_store(store, mode="readonly").store_path
    backend = backend_for(store_path)
    backend.load(index, {bare(n.id): n.payload for n in index.nodes.values() if kind(n.id) == "document"})
    return RuleGraph(backend, index, _documents(load_edge_index(store, False)), store_path)


def _documents(index: Any) -> frozenset[str]:
    return frozenset(bare(n.id) for n in index.nodes.values() if kind(n.id) == "document")
