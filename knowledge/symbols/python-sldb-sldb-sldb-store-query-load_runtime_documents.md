---
id: python-sldb-sldb-sldb-store-query-load_runtime_documents
system: sldb
module: sldb.sldb.store.query
qualname: load_runtime_documents
kind: FunctionDef
source_path: sldb/store/query.py
source_span: 64:72
source_sha256: 97c12e4ef2f6d845379fee569129cb7bfed79823b211d0b0d5d17a9628ebde23
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.sldb.store.query:load_runtime_documents; contract-sha256:25f28a20270b9a4536c63c560a1edf1145acd6e792becb685ee56e639650488f
---

# load_runtime_documents

## Signature

load_runtime_documents(store_path: Path, resolve_model_ref, pythonpath: str | None=None, include_linked: bool=False, codec: StoreCodec=default_codec)

## Docstring

The tracked documents of a store, extracted. With the default codec the load is cached
by the state of the files it comes from (sldb.store.runtime_cache), so repeated queries
do not read the store again. The list is fresh per call; the documents are shared.

## Imports

["__future__", "pathlib", "sldb.store.codec", "sldb.store.io", "sldb.store.layout", "sldb.store.query_engine.global_semantic", "sldb.store.query_engine.models", "sldb.store.query_engine.semantic", "sldb.store.query_engine.structural", "sldb.store.query_engine.structural_queries", "sldb.store.runtime_cache"]

## Purpose

Not documented.

## Architecture

Not documented.
