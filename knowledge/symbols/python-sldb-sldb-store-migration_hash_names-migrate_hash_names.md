---
id: python-sldb-sldb-store-migration_hash_names-migrate_hash_names
system: sldb
module: sldb.store.migration_hash_names
qualname: migrate_hash_names
kind: FunctionDef
source_path: sldb/store/migration_hash_names.py
source_span: '19:23'
source_sha256: 8755f2a3457726c0760302ab6b18e751e54b617ee54f093b21eb4b9a8c1ad668
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.migration_hash_names:migrate_hash_names;
  contract-sha256:0274b222875918290734c87ff5ec1ef251bf881bfe625d944f0a493fd7078296
---

# migrate_hash_names

## Signature

migrate_hash_names(store_path: Path)

## Docstring

Rewrite every `.sldb/core/**.yaml` still carrying a letter key; return the changed files.

## Imports

["__future__", "pathlib", "sldb.store.io.utils", "typing"]

## Purpose

Rewrite every `.sldb/core/**.yaml` still carrying a letter key; return the changed files.

## Architecture

Not documented.
