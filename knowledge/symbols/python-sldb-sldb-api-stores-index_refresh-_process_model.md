---
id: python-sldb-sldb-api-stores-index_refresh-_process_model
system: sldb
module: sldb.api.stores.index_refresh
qualname: _process_model
kind: FunctionDef
source_path: sldb/api/stores/index_refresh.py
source_span: 52:65
source_sha256: 52ff82f50024af90f44606255ea3e419ec7c3bf6b714754debcb1a825838e1fc
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.stores.index_refresh:_process_model; contract-sha256:fdbea9d6b6febf6b35067a17c6de85b6642cca32d8471c7485a1fbeb3c6af1fd
---

# _process_model

## Signature

_process_model(m_entry: Any, mtype: Any, root: Path, skipped_docs: list[str], pending: list[tuple[Any, Any, Any, Any]], changed: dict[str, list[Any]])

## Docstring

Rehash one model's documents and queue its indexes to be saved.

A contract that moved forces every document of the model through extraction again, even
where the Markdown is untouched: a field added to the class, or a changed template, makes
the same text yield a different payload, and no `source_hash` moves to say so.

## Imports

["__future__", "pathlib", "sldb.api.model_registry.model_reference", "sldb.api.stores.document_field_hashes", "sldb.store.field_set_drift", "sldb.store.hashing", "sldb.store.io", "sldb.store.model_node", "sldb.store.models.store_index", "typing"]

## Purpose

Rehash one model's documents and queue its indexes to be saved.

## Architecture

Not documented.
