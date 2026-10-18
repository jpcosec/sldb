---
id: python-sldb-sldb-store-migration-_model_canonical
system: sldb
module: sldb.store.migration
qualname: _model_canonical
kind: FunctionDef
source_path: sldb/store/migration.py
source_span: 49:60
source_sha256: a5e14561f69f4aef068095bfaf7af6b7ee4393388167753439969f2af46be039
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.migration:_model_canonical; contract-sha256:f958a0b807bb98a38b821e17bc70325411573db9e82c3368a1fa0595189b1771
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

PLAN 15 capa 5/7: a model's sections and documents are canonical once their old single per-model files are gone (sharded into `<store>/{runtime/sections,core/documents}/<model>/`, or a section-less model that never had one).

## Architecture

Not documented.
