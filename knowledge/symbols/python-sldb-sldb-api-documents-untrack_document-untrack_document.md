---
id: python-sldb-sldb-api-documents-untrack_document-untrack_document
system: sldb
module: sldb.api.documents.untrack_document
qualname: untrack_document
kind: FunctionDef
source_path: sldb/api/documents/untrack_document.py
source_span: '29:48'
source_sha256: 4b8b7dbf33b146257f439416df941f2af3cf7a2110869f935a40636bdf01fe2e
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.documents.untrack_document:untrack_document;
  contract-sha256:27bfddec835a6c1e317ae8b76db6301404f054264e3fc2d47b687671ad5f52a8
---

# untrack_document

## Signature

untrack_document(store: str | Path | None, document: str, pythonpath: str | None=None, actor: str | None=None)

## Docstring

Remove a tracked document from its model's index and rebuild the derived indexes.

Args:
    store: The store tracking the document (path, alias, or None to discover it).
    document: Document name, or its path as recorded in the store.
    pythonpath: Directory to import the store's model modules from.
    actor: Optional label recorded in the store journal for this write.

Returns:
    The document that was untracked.

Raises:
    SLDBError: When no model tracks such a document.

## Imports

["__future__", "pathlib", "sldb.api.documents.document_lookup", "sldb.api.documents.document_reference", "sldb.api.journal", "sldb.api.model_registry.model_files", "sldb.api.model_registry.model_reference", "sldb.api.stores.open_store", "sldb.store", "sldb.store.edge_rebuild", "sldb.store.io", "sldb.store.io.rollback", "sldb.store.io.shards", "sldb.store.layout", "sldb.store.model_node", "sldb.store.models.document_entry", "sldb.store.models.model_entry", "sldb.store.models.models_index", "sldb.store.models.store_index", "sldb.store.ops", "sldb.store.section_rebuild", "sldb.store.semantic"]

## Purpose

Not documented.

## Architecture

Not documented.
