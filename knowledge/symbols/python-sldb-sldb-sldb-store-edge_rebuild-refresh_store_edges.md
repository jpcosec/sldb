---
id: python-sldb-sldb-sldb-store-edge_rebuild-refresh_store_edges
system: sldb
module: sldb.sldb.store.edge_rebuild
qualname: refresh_store_edges
kind: FunctionDef
source_path: sldb/store/edge_rebuild.py
source_span: '42:45'
source_sha256: 7f2cc97ef06264e2fd1d5e896d4869aa7123ad7334505b0744f0e3fa53108880
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.edge_rebuild:refresh_store_edges; contract-sha256:02fc22097806686185d3e247f3292ae4409429dd82bf9acc1a98051cedfabe99
---

# refresh_store_edges

## Signature

refresh_store_edges(store_path: Path)

## Docstring

Rewrite only the store's own shard: what a change to the semantic DAG moves, and nothing
else. A document's shard does not depend on the DAG, so there is nothing else to redo.

## Imports

["__future__", "logging", "pathlib", "sldb.store.codec", "sldb.store.edge_index.cache_keys", "sldb.store.edge_index.doc_contribution", "sldb.store.edge_index.edge_rebuild_report", "sldb.store.edge_index.shard_signature", "sldb.store.edge_index.store_contribution", "sldb.store.edge_sync", "sldb.store.exceptions", "sldb.store.io", "sldb.store.io.shards", "sldb.store.layout", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
