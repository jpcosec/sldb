---
id: python-sldb-sldb-sldb-api-stores-index_refresh-_queue_roster_only
system: sldb
module: sldb.sldb.api.stores.index_refresh
qualname: _queue_roster_only
kind: FunctionDef
source_path: sldb/api/stores/index_refresh.py
source_span: '37:49'
source_sha256: 52ff82f50024af90f44606255ea3e419ec7c3bf6b714754debcb1a825838e1fc
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.stores.index_refresh:_queue_roster_only;
  contract-sha256:4fbdfa51f9ab706222112435e94c784a5a120fd4320f8ab4525cbdfc2573a7c5
---

# _queue_roster_only

## Signature

_queue_roster_only(m_entry: Any, root: Path, pending: list[tuple[Any, Any, Any, Any]])

## Docstring

Queue a skipped model with no class, so the commit re-signs its roster and count.

Skipping the model whole left a stale roster as `roster stale` in `stores check` for
good. The indexes are reloaded, dropping anything a failed pass half changed;
`stamp_model_node` with no class keeps the contract the model signed.

## Imports

["__future__", "pathlib", "sldb.api.model_registry.model_reference", "sldb.api.stores.document_field_hashes", "sldb.store.field_set_drift", "sldb.store.hashing", "sldb.store.io", "sldb.store.model_node", "sldb.store.models.store_index", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
