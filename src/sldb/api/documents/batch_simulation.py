"""The edge index after a batch is applied in memory: its nodes, relations and relation types."""

from __future__ import annotations

from typing import Any

from sldb.store.edge_index.doc_kinds import relation_edge, relation_type_contribution
from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.edge_index.node_ids import RELATION_MODEL, RELATION_TYPE_MODEL, doc_node_id
from sldb.store.edge_index.resolve import resolve_authored
from sldb.store.models import EdgeNodeRecord, EdgeRecord


def simulated(base: EdgeIndex, changes: list[dict[str, Any]]) -> tuple[EdgeIndex, dict[str, dict[str, Any]], list[str]]:
    """The index after the batch, the batch's live relations (doc name -> payload) and the
    problems composing them found."""
    nodes, relations, edges, added = dict(base.nodes), {}, list(base.edges), []
    replaced = _apply_changes(nodes, relations, edges, added, changes)
    if not replaced and not relations and nodes == base.nodes and not added:
        return base, {}, []
    edges = [e for e in edges if e.metadata.get("relation_doc") not in replaced or e.metadata.get("origin") != "relation_doc"] + added
    edges, problems = _compose(nodes, edges, relations)
    return EdgeIndex(nodes=nodes, edges=edges), relations, problems


def _compose(nodes: dict[str, EdgeNodeRecord], edges: list[EdgeRecord], relations: dict[str, Any]) -> tuple[list[EdgeRecord], list[str]]:
    """`edges` plus the edges the batch's relations compose, and the problems composing them found."""
    problems: list[str] = []
    for name, payload in relations.items():
        composed, bad = resolve_authored(relation_edge(name, payload), nodes)
        edges += composed
        problems += bad
    return edges, problems


def _apply_changes(nodes: dict[str, EdgeNodeRecord], relations: dict[str, Any], edges: list[EdgeRecord], added: list[EdgeRecord], changes: list[dict[str, Any]]) -> set[str]:
    """Fold the batch into `nodes`, `relations` and `added` in place; the relation docs it replaces."""
    replaced = {c["id"] for c in changes if _is_relation_change(c)}
    for change in changes:
        if _is_relation_change(change):
            _set_relation(relations, change)
        elif change.get("model") == RELATION_TYPE_MODEL:
            added += _relation_type(nodes, edges, change)
        elif change["action"] == "create" and isinstance(change.get("model"), str):
            _add_node(nodes, change["id"], change["model"])
    return replaced


def _is_relation_change(change: dict[str, Any]) -> bool:
    return change.get("model") == RELATION_MODEL and change["action"] in ("create", "update", "delete")


def _add_node(nodes: dict[str, EdgeNodeRecord], name: str, model: str) -> None:
    """The node of a document the batch creates, unless the index already has it."""
    node_id = doc_node_id(f"{model}:{name}")
    nodes.setdefault(node_id, EdgeNodeRecord(id=node_id, node_type=model, semantics={"name": name, "model": model}))


def _set_relation(relations: dict[str, Any], change: dict[str, Any]) -> None:
    """The batch's live relation `change` names: replaced by its payload, or gone on a delete."""
    relations.pop(change["id"], None)
    if change["action"] != "delete" and isinstance(change.get("payload"), dict):
        relations[change["id"]] = change["payload"]


def _drop_relation_type(nodes: dict[str, EdgeNodeRecord], edges: list[EdgeRecord], name: str) -> None:
    """Remove, in place, the nodes (and their outgoing edges) the RelationTypeDoc `name` contributed."""
    gone = {k for k, n in nodes.items() if n.node_type == "relation_type" and n.semantics.get("doc") == name}
    for key in gone:
        del nodes[key]
    edges[:] = [e for e in edges if e.source not in gone]


def _relation_type(nodes: dict[str, EdgeNodeRecord], edges: list[EdgeRecord], change: dict[str, Any]) -> list[EdgeRecord]:
    """A RelationTypeDoc of the batch: its node (and schema edges) replace the document's old
    ones; `edges` without the old, the new edges returned."""
    name = change["id"]
    _drop_relation_type(nodes, edges, name)
    payload = change.get("payload")
    if change["action"] == "delete" or not isinstance(payload, dict) or not payload.get("name"):
        return []
    part = relation_type_contribution(name, payload)
    nodes.update({n.id: n for n in part.nodes})
    return part.edges
