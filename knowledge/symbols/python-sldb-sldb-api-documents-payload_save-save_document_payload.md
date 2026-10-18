---
id: python-sldb-sldb-api-documents-payload_save-save_document_payload
system: sldb
module: sldb.api.documents.payload_save
qualname: save_document_payload
kind: FunctionDef
source_path: sldb/api/documents/payload_save.py
source_span: '16:40'
source_sha256: 94e3bea6e7dce2f81e42e7f54b05e796e690339481fb788737f2d726b2720094
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.documents.payload_save:save_document_payload;
  contract-sha256:18ce82cb77bde7ceeb521627abde91e397591943af58bc2775b934430348d65c
---

# save_document_payload

## Signature

save_document_payload(store: str | Path | None, model_name: str, document_name: str, payload: dict[str, Any], pythonpath: str | None=None, actor: str | None=None)

## Docstring

Replace a tracked document's content with the Markdown rendered from `payload`.

Args:
    store: The store tracking the document (path, alias, or None to discover it).
    model_name: Registered model name of the document.
    document_name: Tracked document name.
    payload: The complete new payload; it has no fixed schema beyond the model's own.
    pythonpath: Directory to import the model module from; the store's project root
        is tried next, since a linked store's models import from where it lives.
    actor: Optional label recorded in the store journal for this write.

Returns:
    The document written.

Raises:
    SLDBPayloadSaveError: When the model or document is not registered, or the rendered
        Markdown does not round-trip back to the payload.

## Imports

["__future__", "pathlib", "sldb.api.documents.document_reference", "sldb.api.documents.payload_diff", "sldb.api.documents.payload_save_steps", "sldb.api.journal", "sldb.api.stores.open_store", "sldb.store.codec", "typing"]

## Purpose

Replace a tracked document's content with the Markdown rendered from `payload`.

## Architecture

Not documented.
