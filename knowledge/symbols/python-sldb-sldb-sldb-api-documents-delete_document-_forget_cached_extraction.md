---
id: python-sldb-sldb-sldb-api-documents-delete_document-_forget_cached_extraction
system: sldb
module: sldb.sldb.api.documents.delete_document
qualname: _forget_cached_extraction
kind: FunctionDef
source_path: sldb/api/documents/delete_document.py
source_span: '40:52'
source_sha256: 780f3c87ffb4bfd447b262dfdf1851ad54fdeeeb1c127b214cfac6d9c71e12b3
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.documents.delete_document:_forget_cached_extraction;
  contract-sha256:9b6482a00f1f98fb85d6cc462cb3483822184aa994c2aebf81d2fa5371a947fe
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
