---
id: python-sldb-sldb-store-documents_hash-new_operation
system: sldb
module: sldb.store.documents_hash
qualname: new_operation
kind: FunctionDef
source_path: sldb/store/documents_hash.py
source_span: '27:36'
source_sha256: de6994baeaab28e795023d120138da542eb07f60061eb2e1d773b66d226e7eda
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.documents_hash:new_operation; contract-sha256:cc97de59c5bf32f915b7ca605789e9fddcd06527e9197be59b3a3f9fdb26b53d
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

Bumps this store's operation generation (or, with no store, drops everything): a cache entry from a prior generation is re-validated against the on-disk roster hash before its next use — reused untouched if nothing moved it, recomposed otherwise.

## Architecture

Not documented.
