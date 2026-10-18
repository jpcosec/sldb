---
id: python-sldb-sldb-store-runtime_cache-leaf_of
system: sldb
module: sldb.store.runtime_cache
qualname: leaf_of
kind: FunctionDef
source_path: sldb/store/runtime_cache.py
source_span: 85:89
source_sha256: 870a33b2e031d380c875372e22bbf508b533af2cbd6dae4f59d6ddb6e563db78
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.runtime_cache:leaf_of; contract-sha256:fc0986bb2ff8864caaca2120666f1abb0343c4fd1b5502097a115a4a8ff8230d
---

# leaf_of

## Signature

leaf_of(key: tuple)

## Docstring

The document leaf inside a runtime cache key: what the disk cache keys on — the file
state (path, source_hash[, mtime, size]) plus the model's model_hash, so a contract that moved
misses the disk cache too.

## Imports

["__future__", "dataclasses", "pathlib", "sldb.store", "sldb.store.hashing", "sldb.store.runtime_cache_signature", "typing"]

## Purpose

The document leaf inside a runtime cache key: what the disk cache keys on — the file state (path, source_hash[, mtime, size]) plus the model's model_hash, so a contract that moved misses the disk cache too.

## Architecture

Not documented.
