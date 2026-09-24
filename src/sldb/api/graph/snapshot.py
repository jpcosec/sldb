"""Portable snapshot read/write and the ingest-sldb route."""

from __future__ import annotations

from typing import Any, Iterable

from sldb.api.edges.edge_reading import load_edge_index
from sldb.api.stores.open_store import open_store
from sldb.store.edge_index.federation import federated_stores
from sldb.store.export import export_kgdb_semantic_payload
from sldb.store.graph.convert import snapshot_from_index
from sldb.store.graph.graph_io import load_graph, save_graph
from sldb.store.graph.ingest_sldb import sldb_semantic_export_to_snapshot
from sldb.store.graph.snapshot import GraphSnapshot


def snapshot_save(store, path, include_linked: bool = True, exclude_tags: Iterable[str] = ()) -> None:
    """Save the store's graph as portable node-link JSON, generated from the source indexes.

    The graph is built from the source indexes (store index, models, documents, sections and
    the semantic DAG) through `SemanticExporter` -> `sldb_semantic_export_to_snapshot`, never
    from the `runtime/edges/` shards. Two legacy cases keep the old shard-composed route on
    purpose, until their retirement gaps close: `exclude_tags` (GAP G6: no snapshot-side tag
    filter yet) and `include_linked` with linked stores (GAP G5: no snapshot federation yet).
    """
    location = open_store(store, mode="readonly")
    excluded = tuple(exclude_tags)
    linked = include_linked and len(federated_stores(location.store_path, True)) > 1
    if excluded or linked:
        # GAP G5 (federation) / GAP G6 (exclude_tags): not expressible from the source
        # indexes yet; keep the legacy shard-composed behaviour for exactly these cases.
        save_graph(snapshot_from_index(load_edge_index(location.store_path, include_linked, excluded)), path)
        return
    payload = export_kgdb_semantic_payload(location.store_path, location.project_root, command=["graph", "snapshot", "save"])
    save_graph(sldb_semantic_export_to_snapshot(payload), path)


def snapshot_load(path) -> GraphSnapshot:
    """Read a node-link JSON (or native snapshot) file back into a GraphSnapshot."""
    return load_graph(path)


def ingest_sldb(payload: dict[str, Any]) -> GraphSnapshot:
    """Convert an `sldb_kgdb_semantic_export` v1 payload into a GraphSnapshot."""
    return sldb_semantic_export_to_snapshot(payload)
