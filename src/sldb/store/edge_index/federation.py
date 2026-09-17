"""Each store has its own index; a federated read walks the linked stores (as
`load_runtime_documents(include_linked=True)` does) and qualifies what is theirs with the
name they are linked under: `sldb://document/<store>:Model:name`."""

from __future__ import annotations

from pathlib import Path

from sldb.store.edge_index.node_ids import STORE_NODE_ID
from sldb.store.models import EdgeContribution, EdgeNodeRecord, EdgeRecord

_QUALIFIED_KINDS = ("sldb://document/", "sldb://section/")


def federated_stores(store_path: Path, include_linked: bool) -> list[tuple[Path, str | None]]:
    """(store path, link name) of the store itself (name None) and, breadth first and once
    each, of every store reachable through links."""
    from sldb.store.query import _linked_stores

    found: list[tuple[Path, str | None]] = [(store_path.resolve(), None)]
    for current, _ in found if include_linked else []:
        known = {path for path, _ in found}
        found += [(path, name) for path, name in _linked_stores(current) if path not in known]
    return found


def qualify_id(node_id: str, store_name: str | None) -> str:
    """The id as read from a linked store's shard, made absolute: documents and sections get
    the store's name unless they already name a store; models, fields, tags, relation types
    and anchors are one vocabulary across stores and stay as they are."""
    if store_name is None:
        return node_id
    if node_id == STORE_NODE_ID:
        return f"{STORE_NODE_ID}/{store_name}"
    prefix = next((p for p in _QUALIFIED_KINDS if node_id.startswith(p)), None)
    if prefix is None or node_id[len(prefix):].split("#", 1)[0].count(":") != 1:
        return node_id
    return f"{prefix}{store_name}:{node_id[len(prefix):]}"


def qualify(part: EdgeContribution, store_name: str | None) -> EdgeContribution:
    """A linked store's contribution with every id qualified; the local store's, untouched."""
    if store_name is None:
        return part
    nodes = [_qualified_node(n, store_name) for n in part.nodes]
    edges = [EdgeRecord(source=qualify_id(e.source, store_name), target=qualify_id(e.target, store_name), relation=e.relation, metadata=e.metadata) for e in part.edges]
    return EdgeContribution(nodes=nodes, edges=edges)


def _qualified_node(node: EdgeNodeRecord, store_name: str) -> EdgeNodeRecord:
    new_id = qualify_id(node.id, store_name)
    if new_id == node.id:
        return node
    return EdgeNodeRecord(id=new_id, node_type=node.node_type, semantics={**node.semantics, "store": store_name})
