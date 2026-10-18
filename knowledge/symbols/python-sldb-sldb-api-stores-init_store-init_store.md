---
id: python-sldb-sldb-api-stores-init_store-init_store
system: sldb
module: sldb.api.stores.init_store
qualname: init_store
kind: FunctionDef
source_path: sldb/api/stores/init_store.py
source_span: '14:34'
source_sha256: 093bd3453d72151b1d8fb6afa508d3b6d7ec7c929e92ef28238a78eb783e6671
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.stores.init_store:init_store; contract-sha256:8d84aa8d664b129375037cc000e7f3fbcadfbd877d03957647c438e0331420e3
---

# init_store

## Signature

init_store(path: str | Path='.', force: bool=False)

## Docstring

Create `<path>/.sldb` and register it in the global store's catalog when it is under HOME.

Args:
    path: The project root that will hold the `.sldb` directory.
    force: Delete an existing store there and create it again, empty.

Returns:
    The new store's `.sldb` directory and project root.

Raises:
    SLDBStoreError: When a store already exists at `path` and `force` is False, or the
        store cannot be written there (`StoreInitError`; nothing is left behind).

## Imports

["__future__", "pathlib", "shutil", "sldb.api.stores.store_location", "sldb.api.stores.store_skeleton", "sldb.core.exceptions", "sldb.store.layout"]

## Purpose

Not documented.

## Architecture

Not documented.
