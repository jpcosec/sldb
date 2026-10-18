---
id: python-sldb-sldb-sldb-api-stores-store_check-_classified
system: sldb
module: sldb.sldb.api.stores.store_check
qualname: _classified
kind: FunctionDef
source_path: sldb/api/stores/store_check.py
source_span: 64:77
source_sha256: ae685aaf2819655d86bdc81c2ef092ed5403833ebacc062e01469191d3deeac5
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.stores.store_check:_classified; contract-sha256:f332f4f9d640411d99895cbe3f9d98af5a4537b73eaaf5763b061cb33b7308be
---

# _classified

## Signature

_classified(diagnosis: Any)

## Docstring

The verdict split by category.

`mismatched` lists every hash that moved, including the expected ones (text moved,
fields held still). `damaged` is the subset that actually invalidates the store,
which is what `is_valid` reports.

## Imports

["__future__", "pathlib", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
