---
id: python-sldb-sldb-store-query-load_runtime_documents
system: sldb
module: sldb.store.query
qualname: load_runtime_documents
kind: FunctionDef
source_path: sldb/store/query.py
source_span: 64:73
source_sha256: 441b74a92bf88e1691d36312d2dd7c6cf78ce1308baa2ff7a1baf84950ff7f71
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.query:load_runtime_documents; contract-sha256:e74a5af6de6121ca883d1497e3e498b5ae9d619e2c13437a7936a4d443f356f2
---

# load_runtime_documents

## Signature

load_runtime_documents(store_path: Path, resolve_model_ref, pythonpath: str | None=None, include_linked: bool=False, codec: StoreCodec=default_codec, store_name: str='local')

## Docstring

The tracked documents of a store, extracted. With the default codec the load is cached
by the state of the files it comes from (sldb.store.runtime_cache), so repeated queries
do not read the store again. The list is fresh per call; the documents are shared.
`store_name` is the name the documents carry: the alias when a linked store is read alone.

## Imports

["__future__", "pathlib", "sldb.store.codec", "sldb.store.io", "sldb.store.layout", "sldb.store.query_engine.global_semantic", "sldb.store.query_engine.models", "sldb.store.query_engine.semantic", "sldb.store.query_engine.structural", "sldb.store.query_engine.structural_queries", "sldb.store.runtime_cache"]

## Purpose

The tracked documents of a store, extracted. With the default codec the load is cached by the state of the files it comes from (sldb.store.runtime_cache), so repeated queries do not read the store again. The list is fresh per call; the documents are shared. `store_name` is the name the documents carry: the alias when a linked store is read alone.

## Architecture

Not documented.
