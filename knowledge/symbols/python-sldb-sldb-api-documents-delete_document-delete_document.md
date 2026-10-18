---
id: python-sldb-sldb-api-documents-delete_document-delete_document
system: sldb
module: sldb.api.documents.delete_document
qualname: delete_document
kind: FunctionDef
source_path: sldb/api/documents/delete_document.py
source_span: '12:37'
source_sha256: 780f3c87ffb4bfd447b262dfdf1851ad54fdeeeb1c127b214cfac6d9c71e12b3
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.documents.delete_document:delete_document;
  contract-sha256:a64a3ab3608e7dc22ca359ff2bf85e4fbf4d2c80e91a78aa02584100750bab3c
---

# delete_document

## Signature

delete_document(store: str | Path | None, document: str, pythonpath: str | None=None, actor: str | None=None)

## Docstring

Untrack a document and delete the Markdown file it was tracking.

`untrack_document` is the half of this that keeps the file: it drops the document
from the store indexes and leaves the Markdown alone, which is what you want when a
document should stop being tracked but stay on disk. When the document should be
gone, untracking alone leaves the file behind, and re-tracking the store picks it up
again. This deletes both, and purges the extraction cache entry that would otherwise
keep describing a file that no longer exists.

Args:
    store: The store tracking the document (path, alias, or None to discover it).
    document: Document name, or its path as recorded in the store.
    pythonpath: Directory to import the store's model modules from.
    actor: Optional label recorded in the store journal for this write.

Returns:
    The document that was deleted, including the path the file used to have.

Raises:
    SLDBError: When no model tracks such a document.

## Imports

["__future__", "pathlib", "sldb.api.documents.document_reference", "sldb.api.documents.untrack_document", "sldb.store"]

## Purpose

Untrack a document and delete the Markdown file it was tracking.

## Architecture

Not documented.
