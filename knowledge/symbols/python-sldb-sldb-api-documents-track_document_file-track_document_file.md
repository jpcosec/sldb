---
id: python-sldb-sldb-api-documents-track_document_file-track_document_file
system: sldb
module: sldb.api.documents.track_document_file
qualname: track_document_file
kind: FunctionDef
source_path: sldb/api/documents/track_document_file.py
source_span: '19:48'
source_sha256: 3a634c8ce898154af6bda2f7a29dd8bdbbc892e92d6988ff05052d6c3d2856c8
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.documents.track_document_file:track_document_file;
  contract-sha256:af86b096c112afa1efc3d0585470d0e95e6cc91ce026b5db232579d1d602952e
---

# track_document_file

## Signature

track_document_file(store: str | Path | None, model_name: str, path: str | Path, name: str | None=None, pythonpath: str | None=None, force: bool=False, actor: str | None=None)

## Docstring

Index a Markdown file as a document of a model.

Args:
    store: The store to track in (path, alias, or None to discover it).
    model_name: Registered model name, or `alias:ModelName` for a linked store's model.
    path: The Markdown file; a relative path is relative to the project root, not the cwd.
    name: Document name; defaults to the file stem.
    pythonpath: Directory to import the model module from.
    force: Track without checking that the file round-trips under the model.
    actor: Optional label recorded in the store journal for this write.

Returns:
    The tracked document.

Raises:
    SLDBStoreError: When the model is not registered.
    SLDBValidationError: When the file does not round-trip, or when it carries
        headings the model does not declare, and `force` is False.

## Imports

["__future__", "pathlib", "sldb.api.documents.document_reference", "sldb.api.documents.frontmatter_keys", "sldb.api.documents.refuse_structural_noise", "sldb.api.journal", "sldb.api.model_registry.load_registered_model", "sldb.api.model_registry.model_reference", "sldb.api.stores.open_store", "sldb.core.exceptions", "sldb.runtime.validation", "sldb.store.ops"]

## Purpose

Not documented.

## Architecture

Not documented.
