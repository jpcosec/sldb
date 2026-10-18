---
id: python-sldb-sldb-api-stores-store_skeleton-register_in_global_catalog
system: sldb
module: sldb.api.stores.store_skeleton
qualname: register_in_global_catalog
kind: FunctionDef
source_path: sldb/api/stores/store_skeleton.py
source_span: '32:46'
source_sha256: c58c3ca23d06cd2ced56d7d766aa5aec8c85935928c0d8b48d60a6b705add407
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.stores.store_skeleton:register_in_global_catalog;
  contract-sha256:dc8a7bf11103e238c77f0c710e45cd1336af72afc644cdad5d44869df9cf17a0
---

# register_in_global_catalog

## Signature

register_in_global_catalog(store_path: Path)

## Docstring

Record a project store in the global store, creating the global store when missing.

Only stores under HOME are recorded (see `register_project_store`); the global store
itself is never registered in itself.

Args:
    store_path: The project's `.sldb` directory.

## Imports

["__future__", "pathlib", "sldb.store.catalog", "sldb.store.hashing", "sldb.store.io", "sldb.store.models", "sldb.store.predicates", "sldb.store.resolver"]

## Purpose

Not documented.

## Architecture

Not documented.
