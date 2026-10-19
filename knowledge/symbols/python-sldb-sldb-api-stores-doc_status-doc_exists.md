---
id: python-sldb-sldb-api-stores-doc_status-doc_exists
system: sldb
module: sldb.api.stores.doc_status
qualname: doc_exists
kind: FunctionDef
source_path: sldb/api/stores/doc_status.py
source_span: '36:38'
source_sha256: a436b0ded3673764444131fc25579aaa903b469740bd916b94b78fb0b39c5082
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.stores.doc_status:doc_exists; contract-sha256:ee36ee3948f1efeb680c8b176ca1be1943363a360e1a939b234a7c0176028625
---

# doc_exists

## Signature

doc_exists(store: str | Path | None, ref: str)

## Docstring

True when `ref` names exactly one document (see `doc_status` for why it may not).

## Imports

["__future__", "pathlib", "sldb.api.stores.doc_ref", "sldb.api.stores.doc_ref_status", "sldb.api.stores.indexed_documents", "sldb.api.stores.open_store", "sldb.api.stores.store_links"]

## Purpose

True when `ref` names exactly one document (see `doc_status` for why it may not).

## Architecture

Not documented.
