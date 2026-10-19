---
id: python-sldb-sldb-store-edge_rebuild-rebuild_edges_indexes
system: sldb
module: sldb.store.edge_rebuild
qualname: rebuild_edges_indexes
kind: FunctionDef
source_path: sldb/store/edge_rebuild.py
source_span: '27:39'
source_sha256: 7f2cc97ef06264e2fd1d5e896d4869aa7123ad7334505b0744f0e3fa53108880
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.edge_rebuild:rebuild_edges_indexes; contract-sha256:b2de08555ccc6f44674eb631bf878a98de8efffa1bad054409ba12256d449bee
---

# rebuild_edges_indexes

## Signature

rebuild_edges_indexes(store_path: Path, project_root: Path, resolve_model_ref, pythonpath: str | None=None, report: EdgeRebuildReport | None=None, full: bool=False)

## Docstring

Every shard of the store's edge index, current; only what moved is rewritten. `full`
compares every document's shard instead of trusting the per-model cache and dirty set.

## Imports

["__future__", "logging", "pathlib", "sldb.store.codec", "sldb.store.edge_index.cache_keys", "sldb.store.edge_index.doc_contribution", "sldb.store.edge_index.edge_rebuild_report", "sldb.store.edge_index.shard_signature", "sldb.store.edge_index.store_contribution", "sldb.store.edge_sync", "sldb.store.exceptions", "sldb.store.io", "sldb.store.io.shards", "sldb.store.layout", "typing"]

## Purpose

Every shard of the store's edge index, current; only what moved is rewritten. `full` compares every document's shard instead of trusting the per-model cache and dirty set.

## Architecture

Not documented.
