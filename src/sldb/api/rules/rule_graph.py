"""The store a rule is evaluated over: its edge index, loaded once into the store's
`GraphBackend`, and which documents are the local store's own. The index holds the linked
stores, except for the rules' own evaluations (`rule_graph(store, None)`), which compose them
only when the rules may read them (`rule_reach`): otherwise the index is the store's own, and a
local document reads exactly as it would in the composed one.

`with_payload(node, payload)` is the same graph where `node` reads `payload` instead of its
projection (GO08: the payload a write is about to persist, or the subject a transition reads);
paths still follow the index's edges."""

from __future__ import annotations

from dataclasses import dataclass, replace
from functools import cached_property
from pathlib import Path
from typing import Any

from sldb.api.edges.edge_reading import load_edge_index
from sldb.api.graph.analyze import backend_for
from sldb.api.rules.rule_reach import needs_linked
from sldb.api.stores.open_store import open_store
from sldb.store.edge_index.node_ids import bare, kind
from sldb.store.graph.backend.index_view import index_view
from sldb.store.graph.language.predicate_api import node_finding
from sldb.store.graph.language.predicate_view import node as view_node, with_node


@dataclass(frozen=True)
class RuleGraph:
    """`eval` over one store: `holds` is the finding of a predicate on one document."""

    backend: Any
    index: Any
    local: frozenset[str]
    store_path: Path
    override: tuple[str, dict[str, Any]] | None = None
    linked: bool = True

    def holds(self, predicate: str, node: str) -> dict[str, Any]:
        """The eval finding (node, holds, clause, seen) of `predicate` on the document `node`."""
        if self.override is None or node != self.override[0]:
            return self.backend.eval(predicate, node)[0]
        view, item = self.located(node)
        return node_finding(predicate, view, item)

    def located(self, node: str) -> tuple[dict[str, Any], dict[str, Any]]:
        """The graph view and the element of `node` an evaluation reads (the override's payload)."""
        known = self._view["node"](node) or self._unindexed(node)
        if self.override is None or node != self.override[0]:
            return self._view, known
        item = {**known, "payload": self.override[1]}
        return with_node(self._view, item), item

    def _unindexed(self, node: str) -> dict[str, Any]:
        """A document the index does not hold yet: its family from the store's model registry
        (`indexed_model_bases`, no class imported), so `model <= Base` reads as for an indexed one."""
        from sldb.api.stores.resolve_indexed_document import indexed_model_bases

        model = node.rsplit(":", 1)[0].rsplit(":", 1)[-1]
        return view_node(node, model, {}, indexed_model_bases(self.store_path).get(model, []))

    def with_payload(self, node: str, payload: dict[str, Any]) -> "RuleGraph":
        """This graph, with `node` reading `payload` (its model and edges stay the index's)."""
        return replace(self, override=(node, payload))

    @cached_property
    def index_documents(self) -> list[str]:
        """Every document of the index (the linked stores' too when `linked`), by export id."""
        return [bare(n.id) for n in self.index.nodes.values() if kind(n.id) == "document"]

    @cached_property
    def _view(self) -> dict[str, Any]:
        return index_view(self.index)

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


def rule_graph(store: str | Path | None, linked: bool | None = True) -> RuleGraph:
    """The store's graph with its linked stores, every document's projection loaded. With
    `linked` None (the rules' evaluations) they are composed only when the store's rules may
    read them (`rule_reach.needs_linked`); with False, never."""
    store_path = open_store(store, mode="readonly").store_path
    own = load_edge_index(store_path, False)
    local = _documents(own)
    if linked is None:
        graph = _loaded(own, local, store_path, False)
        linked = needs_linked(graph)
        if not linked:
            return graph
    return _loaded(load_edge_index(store_path, True) if linked else own, local, store_path, linked)


def reading(graph: RuleGraph, node: str) -> RuleGraph:
    """`graph`, or the store's graph with its linked stores when `node` is not a local document
    (a subject behind `alias:`): a rule on it reads what the composed index says."""
    return graph if graph.linked or node in graph.local else rule_graph(graph.store_path, True)


def _loaded(index: Any, local: frozenset[str], store_path: Path, linked: bool) -> RuleGraph:
    backend = backend_for(store_path)
    backend.load(index, {bare(n.id): n.payload for n in index.nodes.values() if kind(n.id) == "document"})
    return RuleGraph(backend, index, local, store_path, linked=linked)


def _documents(index: Any) -> frozenset[str]:
    return frozenset(bare(n.id) for n in index.nodes.values() if kind(n.id) == "document")
