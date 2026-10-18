---
id: python-sldb-sldb-sldb-store-documents_hash-new_operation
system: sldb
module: sldb.sldb.store.documents_hash
qualname: new_operation
kind: FunctionDef
source_path: sldb/store/documents_hash.py
source_span: '27:36'
source_sha256: de6994baeaab28e795023d120138da542eb07f60061eb2e1d773b66d226e7eda
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.documents_hash:new_operation; contract-sha256:6b1aa96fcb2d8ee73a1cd8a7cd8440aac5a03fa08c4e2056d3d7771ea2e6ed38
---

# new_operation

## Signature

new_operation(s_path: Path | None=None)

## Docstring

Bumps this store's operation generation (or, with no store, drops everything): a cache
entry from a prior generation is re-validated against the on-disk roster hash before its
next use — reused untouched if nothing moved it, recomposed otherwise.

## Imports

["__future__", "pathlib", "sldb.store", "sldb.store.hashing", "sldb.store.models"]

## Purpose

Not documented.

## Architecture

Not documented.
