---
id: python-sldb-sldb-sldb-store-documents_hash-dirty_names
system: sldb
module: sldb.sldb.store.documents_hash
qualname: dirty_names
kind: FunctionDef
source_path: sldb/store/documents_hash.py
source_span: 113:117
source_sha256: de6994baeaab28e795023d120138da542eb07f60061eb2e1d773b66d226e7eda
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.documents_hash:dirty_names; contract-sha256:31815861daf0161a924d8eca7160e3b99e42d08df7bd4aea4f3f77123ef05c1c
---

# dirty_names

## Signature

dirty_names(s_path: Path, model_name: str, namespace: str)

## Docstring

Names noted/forgotten in `namespace` ("semantic", "sections", ...) since its last
`clear_dirty` — or None with no baseline to trust: the caller's cue to compare every
document once instead.

## Imports

["__future__", "pathlib", "sldb.store", "sldb.store.hashing", "sldb.store.models"]

## Purpose

Not documented.

## Architecture

Not documented.
