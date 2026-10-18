---
id: python-sldb-sldb-sldb-store-io-semantic_index-semanticindexio-save
system: sldb
module: sldb.sldb.store.io.semantic_index
qualname: SemanticIndexIO.save
kind: FunctionDef
source_path: sldb/store/io/semantic_index.py
source_span: 57:68
source_sha256: 7957ac2d25ea890531650f1a22dbb53ad34435c53ecc46f44ae7b9284b91c5ff
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.io.semantic_index:SemanticIndexIO.save;
  contract-sha256:9cfdc585cac170dbbb82a98e891263857d4aa5b7fd6b16923c0bf4c3176b39a0
---

# SemanticIndexIO.save

## Signature

save(store_path: Path, index: SemanticIndex)

## Docstring

Shards out every document `index` carries (store_init's empty index, migration's
one-time conversion of an old store); the fast write path (semantic_doc_contribution)
writes one shard directly instead of building a whole SemanticIndex for this.

## Imports

["contextlib", "fcntl", "os", "pathlib", "sldb.store.io.utils", "sldb.store.layout", "sldb.store.models", "tempfile", "yaml"]

## Purpose

Not documented.

## Architecture

Not documented.
