---
id: python-sldb-sldb-sldb-store-migration-_already_canonical
system: sldb
module: sldb.sldb.store.migration
qualname: _already_canonical
kind: FunctionDef
source_path: sldb/store/migration.py
source_span: 63:69
source_sha256: a5e14561f69f4aef068095bfaf7af6b7ee4393388167753439969f2af46be039
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.migration:_already_canonical; contract-sha256:22314b4d3fa323e5a690915dc0e82abcf4c4ff3e5e017df9a353021c2db97032
---

# _already_canonical

## Signature

_already_canonical(store_index, store_path: Path, p_root: Path)

## Docstring

True when every model index already sits at its canonical path, points at canonical
document and section indexes (capa 5: sections already sharded, the old file gone), and
the old store-wide semantic index file is gone too (capa 5: sharded): nothing to migrate.

## Imports

["__future__", "pathlib", "sldb.store.io", "sldb.store.layout", "sldb.store.migration_legacy_layout"]

## Purpose

Not documented.

## Architecture

Not documented.
