---
id: python-sldb-sldb-store-runtime_cache-invalidate_runtime_cache
system: sldb
module: sldb.store.runtime_cache
qualname: invalidate_runtime_cache
kind: FunctionDef
source_path: sldb/store/runtime_cache.py
source_span: 105:113
source_sha256: 870a33b2e031d380c875372e22bbf508b533af2cbd6dae4f59d6ddb6e563db78
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.runtime_cache:invalidate_runtime_cache; contract-sha256:9bac30a3933729e322dc773781e6ef6ca49324bb5719bf82f188b911fb60069a
---

# invalidate_runtime_cache

## Signature

invalidate_runtime_cache(store_path: Path | None=None)

## Docstring

Drop the cached documents of one store, or of every store; either way, a call to
signature() for that store sweeps document leaves fresh again next time too.

## Imports

["__future__", "dataclasses", "pathlib", "sldb.store", "sldb.store.hashing", "sldb.store.runtime_cache_signature", "typing"]

## Purpose

Drop the cached documents of one store, or of every store; either way, a call to signature() for that store sweeps document leaves fresh again next time too.

## Architecture

Not documented.
