---
id: python-sldb-sldb-sldb-api-documents-document_payload-runtime_document
system: sldb
module: sldb.sldb.api.documents.document_payload
qualname: runtime_document
kind: FunctionDef
source_path: sldb/api/documents/document_payload.py
source_span: '21:34'
source_sha256: d05a80edb14e66e95b8ef0d0ec5c10d21f796e18b7b672bb1e885fac43906f7c
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.documents.document_payload:runtime_document;
  contract-sha256:a7c4861de61fba1b864e0d186332a54c504f269ef2534a14ecb12d03d4692d74
---

# runtime_document

## Signature

runtime_document(store_path: Path, pythonpath: str | None, doc_ref: str)

## Docstring

The RuntimeDocument of one doc; unknown or ambiguous refs raise SLDBDocumentTargetError.

`alias:ref` reads only the store directly linked under `alias` (see `sldb.api.stores.doc_ref`);
a bare ref reads only the local store.

## Imports

["__future__", "pathlib", "sldb.api.model_registry.model_reference", "sldb.api.stores.doc_ref", "sldb.api.stores.store_links", "sldb.core.exceptions", "sldb.store.query", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
