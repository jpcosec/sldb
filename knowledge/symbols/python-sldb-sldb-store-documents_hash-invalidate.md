---
id: python-sldb-sldb-store-documents_hash-invalidate
system: sldb
module: sldb.store.documents_hash
qualname: invalidate
kind: FunctionDef
source_path: sldb/store/documents_hash.py
source_span: '39:43'
source_sha256: de6994baeaab28e795023d120138da542eb07f60061eb2e1d773b66d226e7eda
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.documents_hash:invalidate; contract-sha256:fda36e365c873dee3ae9703ec45c6960258729f96bc4559c726402a59a62076a
---

# invalidate

## Signature

invalidate(s_path: Path, model_name: str)

## Docstring

Drop one model's cache and every namespace's dirty baseline: something moved a document's
hashes outside `note`/`forget`, so both rebuild (full comparison, not a dirty set) next.

## Imports

["__future__", "pathlib", "sldb.store", "sldb.store.hashing", "sldb.store.models"]

## Purpose

Drop one model's cache and every namespace's dirty baseline: something moved a document's hashes outside `note`/`forget`, so both rebuild (full comparison, not a dirty set) next.

## Architecture

Not documented.
