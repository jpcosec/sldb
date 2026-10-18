---
id: python-sldb-sldb-api-graph-snapshot-snapshot_save
system: sldb
module: sldb.api.graph.snapshot
qualname: snapshot_save
kind: FunctionDef
source_path: sldb/api/graph/snapshot.py
source_span: '17:35'
source_sha256: b6e270110f9a653d8829398407f7fb772e5e89185df06dfbc3feb8f6415ca4bd
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.graph.snapshot:snapshot_save; contract-sha256:36d724f4690e048fa14efb887276ba9131399f33e44ce98a322643320e962188
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
