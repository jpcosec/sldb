---
id: python-sldb-sldb-sldb-api-documents-untrack_document-forget_document
system: sldb
module: sldb.sldb.api.documents.untrack_document
qualname: forget_document
kind: FunctionDef
source_path: sldb/api/documents/untrack_document.py
source_span: 58:72
source_sha256: 4b8b7dbf33b146257f439416df941f2af3cf7a2110869f935a40636bdf01fe2e
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.documents.untrack_document:forget_document;
  contract-sha256:a2bcb503725eb444d9973f1c258a8712784ace640114fd9b6a90aed8e8275de3
---

# forget_document

## Signature

forget_document(sp: Path, root: Path, idx: StoreIndex, m_entry: ModelEntry, m_idx: ModelsIndex, doc: DocumentEntry, pythonpath: str | None, model_type: type | None=None)

## Docstring

Delete the document's shard and update model hashes and derived indexes under the store lock.

If any step raises, the shard, the models index and the store index are put back as they were.

## Imports

["__future__", "pathlib", "sldb.api.documents.document_lookup", "sldb.api.documents.document_reference", "sldb.api.journal", "sldb.api.model_registry.model_files", "sldb.api.model_registry.model_reference", "sldb.api.stores.open_store", "sldb.store", "sldb.store.edge_rebuild", "sldb.store.io", "sldb.store.io.rollback", "sldb.store.io.shards", "sldb.store.layout", "sldb.store.model_node", "sldb.store.models.document_entry", "sldb.store.models.model_entry", "sldb.store.models.models_index", "sldb.store.models.store_index", "sldb.store.ops", "sldb.store.section_rebuild", "sldb.store.semantic"]

## Purpose

Not documented.

## Architecture

Not documented.
