---
id: python-sldb-sldb-sldb-store-migration-_model_canonical
system: sldb
module: sldb.sldb.store.migration
qualname: _model_canonical
kind: FunctionDef
source_path: sldb/store/migration.py
source_span: 49:60
source_sha256: a5e14561f69f4aef068095bfaf7af6b7ee4393388167753439969f2af46be039
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.migration:_model_canonical; contract-sha256:6f881c17823961435a038a47f87a53e89cd4e30c85146208562b9b82c4f12c8d
---

# _model_canonical

## Signature

_model_canonical(m_entry, store_path: Path, p_root: Path)

## Docstring

PLAN 15 capa 5/7: a model's sections and documents are canonical once their old single
per-model files are gone (sharded into `<store>/{runtime/sections,core/documents}/<model>/`,
or a section-less model that never had one).

## Imports

["__future__", "pathlib", "sldb.store.io", "sldb.store.layout", "sldb.store.migration_legacy_layout"]

## Purpose

Not documented.

## Architecture

Not documented.
