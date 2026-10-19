---
id: python-sldb-sldb-store-documents_hash-_on_disk_hash_b
system: sldb
module: sldb.store.documents_hash
qualname: _on_disk_hash_b
kind: FunctionDef
source_path: sldb/store/documents_hash.py
source_span: '46:53'
source_sha256: de6994baeaab28e795023d120138da542eb07f60061eb2e1d773b66d226e7eda
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.documents_hash:_on_disk_hash_b; contract-sha256:7f0f74387e10e764d928e5cefef076b5ed96e6119c72fdc221505feccba9bcec
---

# _on_disk_hash_b

## Signature

_on_disk_hash_b(s_path: Path, model_name: str)

## Docstring

The roster hash the index records — its own child, not the model node (which also folds
in the contract): this cache keys on the document list only.

## Imports

["__future__", "pathlib", "sldb.store", "sldb.store.hashing", "sldb.store.models"]

## Purpose

The roster hash the index records — its own child, not the model node (which also folds in the contract): this cache keys on the document list only.

## Architecture

Not documented.
