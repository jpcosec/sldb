---
id: python-sldb-sldb-store-edge_sync-_sync_model_docs
system: sldb
module: sldb.store.edge_sync
qualname: _sync_model_docs
kind: FunctionDef
source_path: sldb/store/edge_sync.py
source_span: '45:53'
source_sha256: 5fd6f57efb17f19c2862f456d18cc176660084d1711fc47c9007c6576b43752b
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.edge_sync:_sync_model_docs; contract-sha256:048876516366edba7dd8a94a0a74414dd2fb48736fdccd5227f29e2dbcd2a120
---

# _sync_model_docs

## Signature

_sync_model_docs(store_path: Path, m_entry, root: Path, report: EdgeRebuildReport, build_one, every: bool, contract: str='')

## Docstring

PLAN 15 capa 8, as sections does it: every document's file is cheaply checked to exist,
but only one in the dirty set (or every one, with no trustworthy baseline) has its shard
opened and compared.

## Imports

["__future__", "pathlib", "sldb.store", "sldb.store.edge_doc_contribution", "sldb.store.edge_index.cache_keys", "sldb.store.edge_index.edge_rebuild_report", "sldb.store.edge_index.model_contribution", "sldb.store.io", "sldb.store.io.shards", "sldb.store.layout", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
