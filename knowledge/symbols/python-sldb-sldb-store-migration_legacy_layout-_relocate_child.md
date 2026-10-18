---
id: python-sldb-sldb-store-migration_legacy_layout-_relocate_child
system: sldb
module: sldb.store.migration_legacy_layout
qualname: _relocate_child
kind: FunctionDef
source_path: sldb/store/migration_legacy_layout.py
source_span: 69:73
source_sha256: 6afccfe9b23571a9e09e78d0fcd41b026d61ae18b31d4c522711db3850161326
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.migration_legacy_layout:_relocate_child;
  contract-sha256:5d4605bbd256f1f912ed538f83f435ae494a3b1c7cdfbfb41475eaae33c70764
---

# _relocate_child

## Signature

_relocate_child(index: dict, key: str, canonical_rel: str, project_root: Path)

## Docstring

Move the file `index[key]` names to `canonical_rel`, then point the key at the new path.

## Imports

["__future__", "contextlib", "pathlib", "shutil", "sldb.store.io", "sldb.store.io.utils", "sldb.store.layout", "sldb.store.models"]

## Purpose

Move the file `index[key]` names to `canonical_rel`, then point the key at the new path.

## Architecture

Not documented.
