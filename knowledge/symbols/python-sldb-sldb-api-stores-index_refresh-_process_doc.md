---
id: python-sldb-sldb-api-stores-index_refresh-_process_doc
system: sldb
module: sldb.api.stores.index_refresh
qualname: _process_doc
kind: FunctionDef
source_path: sldb/api/stores/index_refresh.py
source_span: 68:86
source_sha256: 52ff82f50024af90f44606255ea3e419ec7c3bf6b714754debcb1a825838e1fc
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.stores.index_refresh:_process_doc; contract-sha256:1272f64228a545c544b218f4f8f0a093a86841112368d6384e5a623b954cf70e
---

# _process_doc

## Signature

_process_doc(doc: Any, mtype: Any, m_name: str, root: Path, skipped_docs: list[str], force: bool=False)

## Docstring

Rehash one document when its Markdown or its stored hashes say it needs it.

A hand edit is only ever seen by re-reading the file (source_hash), unavoidably, for every
tracked document — but PLAN 15 capa 8: the expensive part, extracting content_hash, only
runs for a document whose source_hash actually moved since the per-document hash map last
knew it. `force` is the one case where the text is not the trigger: the model's contract
moved, so the payload can change with the text standing still.

## Imports

["__future__", "pathlib", "sldb.api.model_registry.model_reference", "sldb.api.stores.document_field_hashes", "sldb.store.field_set_drift", "sldb.store.hashing", "sldb.store.io", "sldb.store.model_node", "sldb.store.models.store_index", "typing"]

## Purpose

Rehash one document when its Markdown or its stored hashes say it needs it.

## Architecture

Not documented.
