---
id: python-sldb-sldb-sldb-api-documents-document_serialization-doc_version
system: sldb
module: sldb.sldb.api.documents.document_serialization
qualname: doc_version
kind: FunctionDef
source_path: sldb/api/documents/document_serialization.py
source_span: '12:20'
source_sha256: 2ae5413839d6326530de076fdf3a3f5dec6fb8c92cc0ee1aa846c2fd4683aca9
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.documents.document_serialization:doc_version;
  contract-sha256:1d187bb0410918b4364b34418175a2a5d752ef7743a7ee02b5aac78d906976aa
---

# doc_version

## Signature

doc_version(doc: Any)

## Docstring

The document's field hash (`content_hash`): the version token a client echoes back on save.

`content_hash` is a pure function of the extracted payload, so it matches the payload
equality the optimistic lock in /save uses, and rotates on every field write.

## Imports

["__future__", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
