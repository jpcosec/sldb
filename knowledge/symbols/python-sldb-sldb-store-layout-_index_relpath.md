---
id: python-sldb-sldb-store-layout-_index_relpath
system: sldb
module: sldb.store.layout
qualname: _index_relpath
kind: FunctionDef
source_path: sldb/store/layout.py
source_span: '50:56'
source_sha256: 5426bd05eb9d838ff5b7575a37c92ebc23b4da123ed19302fe13e0158dd44cdf
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.layout:_index_relpath; contract-sha256:ea193f8ea4a8035df48e8a58e5f323fa1a00ebb7aaac75d0e7283a4794c27678
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

A store index's path relative to the project root, derived from the store's real directory name: a store named `.sldb_custom` records `.sldb_custom/core/...` relpaths, not a phantom `.sldb/core/...` nobody reads. The default name `.sldb` yields exactly the paths stores have always persisted, so nothing migrates for them.

## Architecture

Not documented.
