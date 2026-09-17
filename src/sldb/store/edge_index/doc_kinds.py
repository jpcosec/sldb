"""The three kinds of document that are not nodes themselves: a RelationTypeDoc becomes a
`relation_type` node, an anchor document an `anchor` node, a RelationDoc one authored edge."""

from __future__ import annotations

from typing import Any, Callable

from sldb.store.edge_index.anchor_targets import anchor_targets
from sldb.store.edge_index.node_ids import ANCHOR_TAG, RELATION_MODEL, RELATION_TYPE_MODEL, anchor_node_id, doc_node_id, model_node_id, relation_type_node_id
from sldb.store.edge_index.records import edge
from sldb.store.models import DocumentEntry, EdgeContribution, EdgeNodeRecord

Payload = dict[str, Any]


def special_contribution(model_name: str, doc: DocumentEntry, payload_of: Callable[[], Payload | None]) -> EdgeContribution | None:
    """The contribution of a relation type, relation or anchor document; None for a plain one
    (or one whose payload cannot be read: it stays a plain document, as it did in kgdb)."""
    builder = _builder_for(model_name, doc)
    payload = payload_of() if builder is not None else None
    if builder is None or payload is None:
        return None
    return builder(doc, payload)


def _builder_for(model_name: str, doc: DocumentEntry) -> Callable[[DocumentEntry, Payload], EdgeContribution | None] | None:
    if model_name == RELATION_TYPE_MODEL:
        return _relation_type
    if model_name == RELATION_MODEL:
        return _relation
    return _anchor if ANCHOR_TAG in doc.semantic_tags else None


def _relation_type(doc: DocumentEntry, p: Payload) -> EdgeContribution:
    rid = relation_type_node_id(p["name"])
    node = EdgeNodeRecord(id=rid, node_type="relation_type", semantics={**p, "doc": doc.name})
    edges = [edge(rid, model_node_id(cls), kind, "schema") for kind, key in (("applies_to_source", "source_types"), ("applies_to_target", "target_types")) for cls in p.get(key, [])]
    return EdgeContribution(nodes=[node], edges=edges)


def _relation(doc: DocumentEntry, p: Payload) -> EdgeContribution:
    """The authored edge, with its own condition; the type's condition, axis and direction are
    another document's and are applied when the index is composed."""
    metadata = {"relation_doc": doc.name, "condition": p.get("condition") or "", "axis": ""}
    authored = edge(doc_node_id(p["source_id"]), doc_node_id(p["target_id"]), p["relation_type"], "relation_doc", **metadata)
    return EdgeContribution(edges=[authored])


def _anchor(doc: DocumentEntry, p: Payload) -> EdgeContribution | None:
    if "symbol" not in p or "ref" not in p:
        return None
    aid = anchor_node_id(str(p["symbol"]))
    node = EdgeNodeRecord(id=aid, node_type="anchor", semantics={**p, "doc": doc.name})
    return EdgeContribution(nodes=[node], edges=[edge(aid, target, "names", "alias") for target in anchor_targets(p)])
