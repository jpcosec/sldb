---
id: python-sldb-sldb-api-stores-doc_status-doc_status
system: sldb
module: sldb.api.stores.doc_status
qualname: doc_status
kind: FunctionDef
source_path: sldb/api/stores/doc_status.py
source_span: '18:33'
source_sha256: a436b0ded3673764444131fc25579aaa903b469740bd916b94b78fb0b39c5082
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.stores.doc_status:doc_status; contract-sha256:c46b6eee5e4ef208b60b95130c0b6874ef228386f35ba7ddfe7fbfb50a2da981
---

# doc_status

## Signature

doc_status(store: str | Path | None, ref: str)

## Docstring

The state of `ref` read from `store`: `ok`, `missing`, `ambiguous`, `link-missing` or `link-broken`.

Args:
    store: The store the reference is written in (path, alias, or None to discover it).
    ref: `name`, `Model/name` or a tracked path, optionally behind `alias:` (see `doc_ref`).

## Imports

["__future__", "pathlib", "sldb.api.stores.doc_ref", "sldb.api.stores.doc_ref_status", "sldb.api.stores.indexed_documents", "sldb.api.stores.open_store", "sldb.api.stores.store_links"]

## Purpose

Not documented.

## Architecture

Not documented.
