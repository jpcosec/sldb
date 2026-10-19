---
id: python-sldb-sldb-api-stores-migrate_hash_names-migrate_store_hash_names
system: sldb
module: sldb.api.stores.migrate_hash_names
qualname: migrate_store_hash_names
kind: FunctionDef
source_path: sldb/api/stores/migrate_hash_names.py
source_span: '14:16'
source_sha256: 716a4c20bd6513f9a2e82a0a233cae6bb1ea6ea78b323d342c4350225c40300f
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.stores.migrate_hash_names:migrate_store_hash_names;
  contract-sha256:2965dc1c3664f1ddab0ea5f19c0c3c0d1f684007483271fa9e31b1e55b72dee5
---

# migrate_store_hash_names

## Signature

migrate_store_hash_names(store_path: Path)

## Docstring

Rename hash_a..hash_d to store/model/source/content across `.sldb/core/`; return changed files.

## Imports

["__future__", "pathlib", "sldb.store.migration_hash_names"]

## Purpose

Rename hash_a..hash_d to store/model/source/content across `.sldb/core/`; return changed files.

## Architecture

Not documented.
