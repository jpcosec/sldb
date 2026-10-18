---
id: python-sldb-sldb-api-stores-open_store-open_store
system: sldb
module: sldb.api.stores.open_store
qualname: open_store
kind: FunctionDef
source_path: sldb/api/stores/open_store.py
source_span: '16:42'
source_sha256: 647aef25b8551a07a8a535f52947c5a5cad564ef438f14942449a0d067bd5e63
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.stores.open_store:open_store; contract-sha256:b5326c6d4bd96fe502b02ecada6b64c3a649b76a25af1a3c75a775a9b9ae7d6c
---

# open_store

## Signature

open_store(store: str | Path | None=None, mode: str='default')

## Docstring

Resolve a store argument and start a new operation over that store.

Every library operation opens its store this way, exactly as each sldb CLI command
does: the layout is migrated if needed and the per-operation document re-check
(PLAN 15 capa 6) is scheduled.

Args:
    store: A `.sldb` directory path, the alias of a linked store, or None/"" to
        discover the nearest project store from the working directory.
    mode: "readonly" lets discovery fall back to the global store with a warning;
        any other value refuses that fallback.

Returns:
    The resolved store directory and its project root.

Raises:
    SLDBStoreError: When no store is given and none can be discovered.

## Imports

["__future__", "pathlib", "sldb.api.stores.store_discovery", "sldb.api.stores.store_location", "sldb.store.documents_hash", "sldb.store.layout", "sldb.store.migration", "sldb.store.model_origin", "sldb.store.runtime_cache_signature"]

## Purpose

Resolve a store argument and start a new operation over that store.

## Architecture

Not documented.
