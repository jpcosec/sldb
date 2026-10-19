---
id: python-sldb-sldb-store-migration_legacy_layout-_relocate_root_files
system: sldb
module: sldb.store.migration_legacy_layout
qualname: _relocate_root_files
kind: FunctionDef
source_path: sldb/store/migration_legacy_layout.py
source_span: '47:53'
source_sha256: 6afccfe9b23571a9e09e78d0fcd41b026d61ae18b31d4c522711db3850161326
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.migration_legacy_layout:_relocate_root_files;
  contract-sha256:469d632318ed71e73244cfd94a9c1e9362f26b21ae8120013a03a00eaf3b7e0e
---

# _relocate_root_files

## Signature

_relocate_root_files(store_path: Path)

## Docstring

Move the store-wide legacy files next to their canonical paths and drop the old dirs.

## Imports

["__future__", "contextlib", "pathlib", "shutil", "sldb.store.io", "sldb.store.io.utils", "sldb.store.layout", "sldb.store.models"]

## Purpose

Move the store-wide legacy files next to their canonical paths and drop the old dirs.

## Architecture

Not documented.
