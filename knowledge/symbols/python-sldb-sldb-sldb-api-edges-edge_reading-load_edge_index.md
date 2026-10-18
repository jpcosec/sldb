---
id: python-sldb-sldb-sldb-api-edges-edge_reading-load_edge_index
system: sldb
module: sldb.sldb.api.edges.edge_reading
qualname: load_edge_index
kind: FunctionDef
source_path: sldb/api/edges/edge_reading.py
source_span: '14:28'
source_sha256: 843bafb03f66570ae4a91c980e7c72edc694998e17af5edc4882a34b62ba45b5
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.edges.edge_reading:load_edge_index; contract-sha256:4efd0652915a3973d6dcad1136b8e8dcf78d6ec52581a7850b6fef9503fec49b
---

# load_edge_index

## Signature

load_edge_index(store: str | Path | None, include_linked: bool=True, exclude_tags: Iterable[str]=())

## Docstring

The store's edge index composed from its shards (and its linked stores').

Reading never rebuilds: every sldb write keeps the shards current. `EdgeIndex.stale` names
the documents a write from outside sldb left behind; `rebuild_edges` brings them current.

Args:
    store: The store (path, alias, or None to discover it).
    include_linked: Also read the linked stores, their document ids qualified `store:Model:name`.
    exclude_tags: Leave out the documents carrying one of these tags (the index holds them all).

Returns:
    The composed index; kept and shared while the shards do not move, so read-only.

## Imports

["__future__", "pathlib", "sldb.api.stores.open_store", "sldb.store.edge_index.compose", "sldb.store.edge_index.edge_index", "sldb.store.models", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
