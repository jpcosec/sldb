---
id: python-sldb-sldb-api-edges-rebuild_edges-rebuild_edges
system: sldb
module: sldb.api.edges.rebuild_edges
qualname: rebuild_edges
kind: FunctionDef
source_path: sldb/api/edges/rebuild_edges.py
source_span: '17:38'
source_sha256: ea76eb8c0c1433100ebb05bfa856a83bba6d103769d40a4ebf301135022ceed1
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.edges.rebuild_edges:rebuild_edges; contract-sha256:90c944960ebdd51860ea4cfd1a9a8a3f31c33cae6c65f4d6bb5d3b1a7212fe06
---

# rebuild_edges

## Signature

rebuild_edges(store: str | Path | None, pythonpath: str | None=None, wait: bool=False)

## Docstring

Rebuild what moved in the edge index (after the semantic and sections indexes it reads).

Only shards whose document `source_hash` moved are rewritten; on a current store this writes
nothing. When the index reports stale documents (a shard deleted by hand, a store that
predates the index) every shard is compared instead of trusting the caches. It reads the hashes the store has recorded: for files edited outside sldb, run
`update_store_indexes` instead (it rehashes, then rebuilds this index too).

Args:
    store: The store (path, alias, or None to discover it). Linked stores keep their own index.
    pythonpath: Directory to import the store's model modules from.
    wait: Wait for the store lock instead of failing when it is held.

Returns:
    What was walked, written and reused.

## Imports

["__future__", "pathlib", "sldb.api.model_registry.model_reference", "sldb.api.stores.open_store", "sldb.store.edge_index.compose", "sldb.store.edge_index.edge_rebuild_report", "sldb.store.edge_rebuild", "sldb.store.io", "sldb.store.section_rebuild", "sldb.store.semantic"]

## Purpose

Not documented.

## Architecture

Not documented.
