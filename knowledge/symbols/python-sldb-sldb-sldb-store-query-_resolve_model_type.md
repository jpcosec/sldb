---
id: python-sldb-sldb-sldb-store-query-_resolve_model_type
system: sldb
module: sldb.sldb.store.query
qualname: _resolve_model_type
kind: FunctionDef
source_path: sldb/store/query.py
source_span: '36:49'
source_sha256: 97c12e4ef2f6d845379fee569129cb7bfed79823b211d0b0d5d17a9628ebde23
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.sldb.store.query:_resolve_model_type; contract-sha256:12fa55077d6cd344ee22cce74f6e5c97c3670729d5d5faa3cb8a98b58791047c
---

# _resolve_model_type

## Signature

_resolve_model_type(resolver, model_ref: str, p_path, store_root: Path)

## Docstring

Resolve a model, trying the store's own project root before giving up.

Linked stores register model_refs (e.g. ``docs.models:X``) that resolve
relative to that store's repo root, not the caller's pythonpath. We try the
caller path first, then the store root, and return None if neither works so a
single unresolvable model does not abort a federated query.

## Imports

["__future__", "pathlib", "sldb.store.codec", "sldb.store.io", "sldb.store.layout", "sldb.store.query_engine.global_semantic", "sldb.store.query_engine.models", "sldb.store.query_engine.semantic", "sldb.store.query_engine.structural", "sldb.store.query_engine.structural_queries", "sldb.store.runtime_cache"]

## Purpose

Not documented.

## Architecture

Not documented.
