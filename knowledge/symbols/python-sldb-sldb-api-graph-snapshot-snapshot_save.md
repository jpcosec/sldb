---
id: python-sldb-sldb-api-graph-snapshot-snapshot_save
system: sldb
module: sldb.api.graph.snapshot
qualname: snapshot_save
kind: FunctionDef
source_path: sldb/api/graph/snapshot.py
source_span: '17:35'
source_sha256: f1ee6bb4d5245aab04d5624bc080beaa849e3eeb903896ca16e9278dd0ec747e
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.graph.snapshot:snapshot_save; contract-sha256:4f01f76526035df65fa8f827ba06cd6ae907d43c33744fd17a6fbe302d065f1a
---

# snapshot_save

## Signature

snapshot_save(store, path, include_linked: bool=True, exclude_tags: Iterable[str]=())

## Docstring

Save the store's graph as portable node-link JSON, generated from the source indexes.

The graph is built from the source indexes (store index, models, documents, sections and
the semantic DAG) through `SemanticExporter` -> `sldb_semantic_export_to_snapshot`, never
from the `runtime/edges/` shards. Two legacy cases keep the old shard-composed route on
purpose, until their retirement gaps close: `exclude_tags` (GAP G6: no snapshot-side tag
filter yet) and `include_linked` with linked stores (GAP G5: no snapshot federation yet).

## Imports

["__future__", "sldb.api.edges.edge_reading", "sldb.api.stores.open_store", "sldb.store.edge_index.federation", "sldb.store.export", "sldb.store.graph.convert", "sldb.store.graph.graph_io", "sldb.store.graph.ingest_sldb", "sldb.store.graph.snapshot", "typing"]

## Purpose

Save the store's graph as portable node-link JSON, generated from the source indexes.

## Architecture

Not documented.
