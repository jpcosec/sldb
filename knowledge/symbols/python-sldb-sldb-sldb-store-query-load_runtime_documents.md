---
id: python-sldb-sldb-sldb-store-query-load_runtime_documents
system: sldb
module: sldb.sldb.store.query
qualname: load_runtime_documents
kind: FunctionDef
source_path: sldb/store/query.py
source_span: 64:73
source_sha256: 441b74a92bf88e1691d36312d2dd7c6cf78ce1308baa2ff7a1baf84950ff7f71
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.query:load_runtime_documents; contract-sha256:ea8f69ee6c6f8286beb544b759359f4ac34e791be48cd39293631f60e617b810
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

Not documented.

## Architecture

Not documented.
