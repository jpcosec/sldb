"""Portable snapshot read/write and the ingest-sldb route."""

from __future__ import annotations

from typing import Any, Iterable

from sldb.api.edges.edge_reading import load_edge_index
from sldb.store.graph.convert import snapshot_from_index
from sldb.store.graph.graph_io import load_graph, save_graph
from sldb.store.graph.ingest_sldb import sldb_semantic_export_to_snapshot
from sldb.store.graph.snapshot import GraphSnapshot


def snapshot_save(store, path, include_linked: bool = True, exclude_tags: Iterable[str] = ()) -> None:
    """Export the store's edge index to a portable node-link JSON file."""
    save_graph(snapshot_from_index(load_edge_index(store, include_linked, exclude_tags)), path)


def snapshot_load(path) -> GraphSnapshot:
    """Read a node-link JSON (or native snapshot) file back into a GraphSnapshot."""
    return load_graph(path)


def ingest_sldb(payload: dict[str, Any]) -> GraphSnapshot:
    """Convert an `sldb_kgdb_semantic_export` v1 payload into a GraphSnapshot."""
    return sldb_semantic_export_to_snapshot(payload)
