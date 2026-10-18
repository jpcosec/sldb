---
id: python-sldb-sldb-api-stores-update_store_indexes-storeindexrefresh-__call__
system: sldb
module: sldb.api.stores.update_store_indexes
qualname: StoreIndexRefresh.__call__
kind: FunctionDef
source_path: sldb/api/stores/update_store_indexes.py
source_span: '41:47'
source_sha256: 358bda31a39ba9b75a1b27ff8f50e7a1635bd8c3fe59895948030ae4d02a1ffd
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.stores.update_store_indexes:StoreIndexRefresh.__call__;
  contract-sha256:53236d75ac10293d519b28137a5c71d8292c306ac723aa032e8f61fd5f627815
---

# StoreIndexRefresh.__call__

## Signature

__call__(self, wait: bool)

## Docstring

Rehash, commit under the store lock (waiting for it if asked) and report.

## Imports

["__future__", "pathlib", "sldb.api.stores.index_commit", "sldb.api.stores.index_refresh", "sldb.api.stores.open_store", "sldb.api.stores.store_location", "sldb.api.stores.store_update_report", "sldb.store.io", "typing"]

## Purpose

Rehash, commit under the store lock (waiting for it if asked) and report.

## Architecture

Not documented.
