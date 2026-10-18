---
id: python-sldb-sldb-sldb-store-query-_resolve_model_type
system: sldb
module: sldb.sldb.store.query
qualname: _resolve_model_type
kind: FunctionDef
source_path: sldb/store/query.py
source_span: '36:49'
source_sha256: 441b74a92bf88e1691d36312d2dd7c6cf78ce1308baa2ff7a1baf84950ff7f71
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.query:_resolve_model_type; contract-sha256:1a15f7af21b7c13149a03d66401867582fe1f092ec66d5ae0687e0b7f310c6de
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
