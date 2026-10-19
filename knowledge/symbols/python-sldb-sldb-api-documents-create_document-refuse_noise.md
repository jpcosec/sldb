---
id: python-sldb-sldb-api-documents-create_document-refuse_noise
system: sldb
module: sldb.api.documents.create_document
qualname: refuse_noise
kind: FunctionDef
source_path: sldb/api/documents/create_document.py
source_span: '53:56'
source_sha256: 07562f9e0386f4073f011adfb675433b0c0c84363b1b2c1540ef7b2f0127d465
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.documents.create_document:refuse_noise; contract-sha256:6042500facc5c7d0037b393e1ead27cde236d9dabcb26a7be43d723c911ea566
---

# refuse_noise

## Signature

refuse_noise(model_type: type, markdown: str, name: str)

## Docstring

Refuse a document whose headings or frontmatter keys the model never declares.

## Imports

["__future__", "pathlib", "sldb.api.documents.document_reference", "sldb.api.documents.frontmatter_keys", "sldb.api.documents.refuse_structural_noise", "sldb.api.journal", "sldb.api.model_registry.load_registered_model", "sldb.api.model_registry.model_reference", "sldb.api.stores.open_store", "sldb.core.exceptions", "sldb.runtime.validation", "sldb.store.ops", "typing"]

## Purpose

Refuse a document whose headings or frontmatter keys the model never declares.

## Architecture

Not documented.
