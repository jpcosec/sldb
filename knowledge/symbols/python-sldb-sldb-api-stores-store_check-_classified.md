---
id: python-sldb-sldb-api-stores-store_check-_classified
system: sldb
module: sldb.api.stores.store_check
qualname: _classified
kind: FunctionDef
source_path: sldb/api/stores/store_check.py
source_span: 64:77
source_sha256: ae685aaf2819655d86bdc81c2ef092ed5403833ebacc062e01469191d3deeac5
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.stores.store_check:_classified; contract-sha256:636ac46e08b16bd95a820c50e81b7c359f01d04218f54cad42be71b3974b0bb7
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

The verdict split by category.

## Architecture

Not documented.
