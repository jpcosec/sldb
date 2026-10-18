---
id: python-sldb-sldb-sldb-api-stores-update_store_indexes-update_store_indexes
system: sldb
module: sldb.sldb.api.stores.update_store_indexes
qualname: update_store_indexes
kind: FunctionDef
source_path: sldb/api/stores/update_store_indexes.py
source_span: '16:27'
source_sha256: 358bda31a39ba9b75a1b27ff8f50e7a1635bd8c3fe59895948030ae4d02a1ffd
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.stores.update_store_indexes:update_store_indexes;
  contract-sha256:3f9a56d7fbd9b86bddbf803a638cde03a47e20b689a7d964f08e5fb521e038aa
---

# update_store_indexes

## Signature

update_store_indexes(store: str | Path | None, pythonpath: str | None=None, wait: bool=False)

## Docstring

Rehash changed documents, save model indexes and rebuild the derived indexes.

Args:
    store: The store to refresh (path, alias, or None to discover it).
    pythonpath: Import root for the store's model modules.
    wait: Wait for the store lock instead of failing when another writer holds it.

Returns:
    What was refreshed and which models or documents had to be skipped.

## Imports

["__future__", "pathlib", "sldb.api.stores.index_commit", "sldb.api.stores.index_refresh", "sldb.api.stores.open_store", "sldb.api.stores.store_location", "sldb.api.stores.store_update_report", "sldb.store.io", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
