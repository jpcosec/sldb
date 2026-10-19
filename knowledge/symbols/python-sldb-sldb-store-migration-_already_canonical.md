---
id: python-sldb-sldb-store-migration-_already_canonical
system: sldb
module: sldb.store.migration
qualname: _already_canonical
kind: FunctionDef
source_path: sldb/store/migration.py
source_span: 63:69
source_sha256: a5e14561f69f4aef068095bfaf7af6b7ee4393388167753439969f2af46be039
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.migration:_already_canonical; contract-sha256:9f90a594a45ef915b25f6fea7f066513dacecc8a69610216488dc30484f50194
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

True when every model index already sits at its canonical path, points at canonical document and section indexes (capa 5: sections already sharded, the old file gone), and the old store-wide semantic index file is gone too (capa 5: sharded): nothing to migrate.

## Architecture

Not documented.
