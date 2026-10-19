---
id: python-sldb-sldb-api-documents-document_payload-runtime_document
system: sldb
module: sldb.api.documents.document_payload
qualname: runtime_document
kind: FunctionDef
source_path: sldb/api/documents/document_payload.py
source_span: '21:34'
source_sha256: d05a80edb14e66e95b8ef0d0ec5c10d21f796e18b7b672bb1e885fac43906f7c
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.documents.document_payload:runtime_document;
  contract-sha256:c424685235a72e0bdb6fe9d15c461581f756107d686cec929fcbf6dca4ad89d0
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

The RuntimeDocument of one doc; unknown or ambiguous refs raise SLDBDocumentTargetError.

## Architecture

Not documented.
