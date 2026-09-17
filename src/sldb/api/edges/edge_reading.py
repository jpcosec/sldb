"""Read the edge index of a store: the one door to edges and nodes."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from sldb.api.stores.open_store import open_store
from sldb.store.edge_index.compose import compose_edge_index
from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.models import EdgeNodeRecord, EdgeRecord


def load_edge_index(store: str | Path | None, include_linked: bool = True, exclude_tags: Iterable[str] = ()) -> EdgeIndex:
    """The store's edge index composed from its shards (and its linked stores').

    Reading never rebuilds: every sldb write keeps the shards current. `EdgeIndex.stale` names
    the documents a write from outside sldb left behind; `rebuild_edges` brings them current.

    Args:
        store: The store (path, alias, or None to discover it).
        include_linked: Also read the linked stores, their document ids qualified `store:Model:name`.
        exclude_tags: Leave out the documents carrying one of these tags (the index holds them all).

    Returns:
        The composed index; kept and shared while the shards do not move, so read-only.
    """
    return compose_edge_index(open_store(store, mode="readonly").store_path, include_linked, exclude_tags)


def edges_from(store: str | Path | None, export_id: str, relation: str | None = None, include_linked: bool = True, exclude_tags: Iterable[str] = ()) -> list[EdgeRecord]:
    """Edges leaving a document (`Model:name`) or any node (`sldb://<kind>/...`).

    Args:
        store: The store (path, alias, or None to discover it).
        export_id: A document's export id, or a full node id.
        relation: Only edges of this relation type; None for all.
        include_linked: As in `load_edge_index`.
        exclude_tags: As in `load_edge_index`.

    Returns:
        `{source, target, relation, metadata}` records, in a stable order.
    """
    return load_edge_index(store, include_linked, exclude_tags).edges_from(export_id, relation)


def edges_to(store: str | Path | None, export_id: str, relation: str | None = None, include_linked: bool = True, exclude_tags: Iterable[str] = ()) -> list[EdgeRecord]:
    """Edges pointing at a document or node; arguments and result as in `edges_from`."""
    return load_edge_index(store, include_linked, exclude_tags).edges_to(export_id, relation)


def edge_node(store: str | Path | None, node_id: str, include_linked: bool = True, exclude_tags: Iterable[str] = ()) -> EdgeNodeRecord | None:
    """The node with that node id (or document export id); None when the index has none."""
    return load_edge_index(store, include_linked, exclude_tags).node(node_id)


def edge_nodes_of_type(store: str | Path | None, node_type: str, include_linked: bool = True, exclude_tags: Iterable[str] = ()) -> list[EdgeNodeRecord]:
    """Nodes of one class (`sldb_model`, `semantic_tag`, `relation_type`, a model name...), by id."""
    return load_edge_index(store, include_linked, exclude_tags).nodes_of_type(node_type)
