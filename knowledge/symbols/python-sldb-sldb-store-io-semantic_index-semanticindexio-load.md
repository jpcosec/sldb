---
id: python-sldb-sldb-store-io-semantic_index-semanticindexio-load
system: sldb
module: sldb.store.io.semantic_index
qualname: SemanticIndexIO.load
kind: FunctionDef
source_path: sldb/store/io/semantic_index.py
source_span: '44:54'
source_sha256: 7957ac2d25ea890531650f1a22dbb53ad34435c53ecc46f44ae7b9284b91c5ff
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.io.semantic_index:SemanticIndexIO.load; contract-sha256:040a9d476ca924aee0e1e8287f2d2835b0541958e42a642ecf799def20fcb1f3
---

# SemanticIndexIO.load

## Signature

load(store_path: Path)

## Docstring

Composed from per-document shards (PLAN 15 capa 5); a store not migrated to
shards yet (no shards, the legacy file still there) reads that file instead —
`migrate_store_layout` is what shards it, on the next call that touches this store.

## Imports

["contextlib", "fcntl", "os", "pathlib", "sldb.store.io.utils", "sldb.store.layout", "sldb.store.models", "tempfile", "yaml"]

## Purpose

Not documented.

## Architecture

Not documented.
