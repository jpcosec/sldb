---
id: python-sldb-sldb-api-documents-delete_document-_forget_cached_extraction
system: sldb
module: sldb.api.documents.delete_document
qualname: _forget_cached_extraction
kind: FunctionDef
source_path: sldb/api/documents/delete_document.py
source_span: '40:52'
source_sha256: 780f3c87ffb4bfd447b262dfdf1851ad54fdeeeb1c127b214cfac6d9c71e12b3
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.documents.delete_document:_forget_cached_extraction;
  contract-sha256:7a7da9e36b9a62e9e6afb8ef45e15d92188b7968c572fbf34a8a6b5bc8543ef8
---

# _forget_cached_extraction

## Signature

_forget_cached_extraction(deleted: DocumentReference)

## Docstring

Drop the cache entries whose leaf key names the deleted file.

The cache is keyed by path, hash and model, so a deleted document leaves a stale
entry until a full load rewrites the file. Harmless for correctness (the payload is
never served for a document the store no longer tracks) but it keeps a deleted path
in a file that is read as a description of the store.

## Imports

["__future__", "pathlib", "sldb.api.documents.document_reference", "sldb.api.documents.untrack_document", "sldb.store"]

## Purpose

Not documented.

## Architecture

Not documented.
