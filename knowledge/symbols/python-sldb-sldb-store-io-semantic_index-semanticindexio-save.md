---
id: python-sldb-sldb-store-io-semantic_index-semanticindexio-save
system: sldb
module: sldb.store.io.semantic_index
qualname: SemanticIndexIO.save
kind: FunctionDef
source_path: sldb/store/io/semantic_index.py
source_span: 57:68
source_sha256: 7957ac2d25ea890531650f1a22dbb53ad34435c53ecc46f44ae7b9284b91c5ff
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.io.semantic_index:SemanticIndexIO.save; contract-sha256:75d0e80b592ce3e73b4a460c3bda12a19e46234f49d0807b66d42285b1376b14
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
