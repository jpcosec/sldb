---
id: python-sldb-sldb-store-edge_rebuild-_model_type
system: sldb
module: sldb.store.edge_rebuild
qualname: _model_type
kind: FunctionDef
source_path: sldb/store/edge_rebuild.py
source_span: 53:62
source_sha256: 7f2cc97ef06264e2fd1d5e896d4869aa7123ad7334505b0744f0e3fa53108880
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.edge_rebuild:_model_type; contract-sha256:594d5cff7b5688d9d72a5254be52e0d4dd0a8af9d475ae95c2ef22b75de5f87f
---

# _model_type

## Signature

_model_type(resolver, m_entry, pythonpath: str | None, root: Path, report: EdgeRebuildReport)

## Docstring

The model class, tried from the caller's path and then the store's own root (a linked
store's models import from there); None, and reported, when neither works.

## Imports

["__future__", "logging", "pathlib", "sldb.store.codec", "sldb.store.edge_index.cache_keys", "sldb.store.edge_index.doc_contribution", "sldb.store.edge_index.edge_rebuild_report", "sldb.store.edge_index.shard_signature", "sldb.store.edge_index.store_contribution", "sldb.store.edge_sync", "sldb.store.exceptions", "sldb.store.io", "sldb.store.io.shards", "sldb.store.layout", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
