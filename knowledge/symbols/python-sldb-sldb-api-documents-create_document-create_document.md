---
id: python-sldb-sldb-api-documents-create_document-create_document
system: sldb
module: sldb.api.documents.create_document
qualname: create_document
kind: FunctionDef
source_path: sldb/api/documents/create_document.py
source_span: '20:50'
source_sha256: 07562f9e0386f4073f011adfb675433b0c0c84363b1b2c1540ef7b2f0127d465
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.documents.create_document:create_document;
  contract-sha256:d6269d2da6f5448cc1e6490d99063215d19ee886c354c3f64218c12f9d0277b4
---

# create_document

## Signature

create_document(store: str | Path | None, model_name: str, path: str | Path, payload: dict[str, Any], name: str | None=None, pythonpath: str | None=None, actor: str | None=None)

## Docstring

Write the Markdown a model renders from `payload` and start tracking it.

Args:
    store: The store to track in (path, alias, or None to discover it).
    model_name: Registered model name, or `alias:ModelName` for a linked store's model.
    path: The Markdown file to write (parents are created, an existing file is
        overwritten); a relative path is relative to the project root, not the cwd.
    payload: The document's field values; it has no fixed schema beyond the model's own.
    name: Document name; defaults to the file stem.
    pythonpath: Directory to import the model module from.
    actor: Optional label recorded in the store journal for this write.

Returns:
    The created document.

Raises:
    SLDBStoreError: When the model is not registered.
    SLDBValidationError: When the rendered Markdown does not round-trip under the model,
        or when it carries headings the model does not declare; nothing is written then.

## Imports

["__future__", "pathlib", "sldb.api.documents.document_reference", "sldb.api.documents.frontmatter_keys", "sldb.api.documents.refuse_structural_noise", "sldb.api.journal", "sldb.api.model_registry.load_registered_model", "sldb.api.model_registry.model_reference", "sldb.api.stores.open_store", "sldb.core.exceptions", "sldb.runtime.validation", "sldb.store.ops", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
