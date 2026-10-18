---
id: python-sldb-sldb-core-exceptions-store_error-storeerror
system: sldb
module: sldb.core.exceptions.store_error
qualname: StoreError
kind: ClassDef
source_path: sldb/core/exceptions/store_error.py
source_span: '1:10'
source_sha256: 4235274219b2904e41e2ade71c705195cf96aa7fc709bb7a3c02d75661038207
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.core.exceptions.store_error:StoreError; contract-sha256:0502e51ef7dcddefcde0dd53364e8ef79bddb88ac617b8ff11733174097b9e24
---

# StoreError

## Signature

Not applicable.

## Docstring

Base error for anything owned by the store layer.

Defined in the core and not in the store because the core needs to name it:
`SLDBStoreError` inherits from it, and `core.exceptions` re-exports that, so
importing it from the store made every core import pull in the whole
persistence layer — 46 extra modules to use the text converter.

An exception hierarchy belongs to the lowest layer that mentions it.

## Imports

[]

## Purpose

Not documented.

## Architecture

Not documented.
