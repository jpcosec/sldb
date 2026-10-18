---
id: python-sldb-sldb-api-stores-unlink_store-unlink_store
system: sldb
module: sldb.api.stores.unlink_store
qualname: unlink_store
kind: FunctionDef
source_path: sldb/api/stores/unlink_store.py
source_span: '18:36'
source_sha256: cc89416a37d58ae0fedd3f05660605349181c2156c9cad79c822926b6a9441ca
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.stores.unlink_store:unlink_store; contract-sha256:45abbafadb71919a5e9ee628259699a3ccc2c71f72e25580a354a8841515800b
---

# unlink_store

## Signature

unlink_store(store: str | Path | None, name: str)

## Docstring

Forget the store linked as `name`; its own store is not touched.

Args:
    store: The linking store (path, alias, or None to discover it).
    name: The link's alias.

Returns:
    The link as it was recorded.

Raises:
    SLDBStoreError: When nothing is linked as `name`, or a model here is inherited from it
        (it imports from there: point the link elsewhere with `link_store(..., replace=True)`).

## Imports

["__future__", "pathlib", "sldb.api.stores.linked_store", "sldb.api.stores.open_store", "sldb.core.exceptions", "sldb.store.io"]

## Purpose

Forget the store linked as `name`; its own store is not touched.

## Architecture

Not documented.
