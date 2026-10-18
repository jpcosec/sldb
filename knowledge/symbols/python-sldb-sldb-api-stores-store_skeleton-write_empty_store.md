---
id: python-sldb-sldb-api-stores-store_skeleton-write_empty_store
system: sldb
module: sldb.api.stores.store_skeleton
qualname: write_empty_store
kind: FunctionDef
source_path: sldb/api/stores/store_skeleton.py
source_span: '18:29'
source_sha256: c58c3ca23d06cd2ced56d7d766aa5aec8c85935928c0d8b48d60a6b705add407
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.stores.store_skeleton:write_empty_store; contract-sha256:2be59605304020cb4e834afc342410bae74dadceb1c738405011040cd2bef4b6
---

# write_empty_store

## Signature

write_empty_store(store_path: Path)

## Docstring

Write a store index seeded with the default predicates, an empty DAG and semantic index.

The root hash is sealed over the empty model layer, so a new store (or one that only
links others) passes `stores check` without a `stores update`.

Args:
    store_path: The `.sldb` directory to create.

## Imports

["__future__", "pathlib", "sldb.store.catalog", "sldb.store.hashing", "sldb.store.io", "sldb.store.models", "sldb.store.predicates", "sldb.store.resolver"]

## Purpose

Not documented.

## Architecture

Not documented.
