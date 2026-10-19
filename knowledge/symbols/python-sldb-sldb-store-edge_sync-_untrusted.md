---
id: python-sldb-sldb-store-edge_sync-_untrusted
system: sldb
module: sldb.store.edge_sync
qualname: _untrusted
kind: FunctionDef
source_path: sldb/store/edge_sync.py
source_span: '39:42'
source_sha256: 5fd6f57efb17f19c2862f456d18cc176660084d1711fc47c9007c6576b43752b
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.edge_sync:_untrusted; contract-sha256:83b4a0a4279d46956b5d3a2fc2492be7a95ce56b01d4c098759382dda02a1a18
---

# _untrusted

## Signature

_untrusted(store_path: Path, model: str, contract: str, model_shard: Path)

## Docstring

No shards to trust (neither the cache key nor the dirty set): none were written, or they
were under another contract, which moves every document's edges without moving its hashes.

## Imports

["__future__", "pathlib", "sldb.store", "sldb.store.edge_doc_contribution", "sldb.store.edge_index.cache_keys", "sldb.store.edge_index.edge_rebuild_report", "sldb.store.edge_index.model_contribution", "sldb.store.io", "sldb.store.io.shards", "sldb.store.layout", "typing"]

## Purpose

No shards to trust (neither the cache key nor the dirty set): none were written, or they were under another contract, which moves every document's edges without moving its hashes.

## Architecture

Not documented.
