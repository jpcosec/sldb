---
id: python-sldb-sldb-store-documents_hash-dirty_names
system: sldb
module: sldb.store.documents_hash
qualname: dirty_names
kind: FunctionDef
source_path: sldb/store/documents_hash.py
source_span: 113:117
source_sha256: de6994baeaab28e795023d120138da542eb07f60061eb2e1d773b66d226e7eda
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.documents_hash:dirty_names; contract-sha256:c1f922c0600647b6a31a1408713bece10229e9db1b94b8ebd8e0b23ddea4597d
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

Names noted/forgotten in `namespace` ("semantic", "sections", ...) since its last `clear_dirty` — or None with no baseline to trust: the caller's cue to compare every document once instead.

## Architecture

Not documented.
