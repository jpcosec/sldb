---
id: python-sldb-sldb-sldb-store-layout-_index_relpath
system: sldb
module: sldb.sldb.store.layout
qualname: _index_relpath
kind: FunctionDef
source_path: sldb/store/layout.py
source_span: '50:56'
source_sha256: 5426bd05eb9d838ff5b7575a37c92ebc23b4da123ed19302fe13e0158dd44cdf
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.layout:_index_relpath; contract-sha256:3eca74bf2dc64e47c8bf0da1cdbe208c7f3dc7035ff6cfc0e8beb4d6ad9379bf
---

# _index_relpath

## Signature

_index_relpath(store_path: Path, *parts: str)

## Docstring

A store index's path relative to the project root, derived from the store's real
directory name: a store named `.sldb_custom` records `.sldb_custom/core/...` relpaths,
not a phantom `.sldb/core/...` nobody reads. The default name `.sldb` yields exactly the
paths stores have always persisted, so nothing migrates for them.

## Imports

["__future__", "pathlib"]

## Purpose

Not documented.

## Architecture

Not documented.
