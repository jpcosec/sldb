---
id: python-sldb-sldb-api-stores-index_refresh-_process_models
system: sldb
module: sldb.api.stores.index_refresh
qualname: _process_models
kind: FunctionDef
source_path: sldb/api/stores/index_refresh.py
source_span: '20:34'
source_sha256: 52ff82f50024af90f44606255ea3e419ec7c3bf6b714754debcb1a825838e1fc
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.stores.index_refresh:_process_models; contract-sha256:670dc6c1febe1598043d4286f32d7c7a6d88f9c7cc4d3a216d3b3f14fba0d31c
---

# _process_models

## Signature

_process_models(idx: StoreIndex, root: Path, pypath: str | None, skipped_models: list[str], skipped_docs: list[str], pending: list[tuple[Any, Any, Any]], changed: dict[str, list[Any]])

## Docstring

Rehash every model's documents; a model whose class fails to import is recorded as skipped.

The broad catch isolates one broken model module (it may raise anything on import)
from the rest of the store, and records it in `skipped_models` for the report. Its
documents are not rehashed, but its roster still is: see `_queue_roster_only`.

## Imports

["__future__", "pathlib", "sldb.api.model_registry.model_reference", "sldb.api.stores.document_field_hashes", "sldb.store.field_set_drift", "sldb.store.hashing", "sldb.store.io", "sldb.store.model_node", "sldb.store.models.store_index", "typing"]

## Purpose

Rehash every model's documents; a model whose class fails to import is recorded as skipped.

## Architecture

Not documented.
