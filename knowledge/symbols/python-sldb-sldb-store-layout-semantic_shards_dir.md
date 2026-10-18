---
id: python-sldb-sldb-store-layout-semantic_shards_dir
system: sldb
module: sldb.store.layout
qualname: semantic_shards_dir
kind: FunctionDef
source_path: sldb/store/layout.py
source_span: 71:74
source_sha256: 5426bd05eb9d838ff5b7575a37c92ebc23b4da123ed19302fe13e0158dd44cdf
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.layout:semantic_shards_dir; contract-sha256:4a40638e0d400a0b561345651da3fad818c74c13e3f82ce069abf941e8a18534
---

# semantic_shards_dir

## Signature

semantic_shards_dir(store_path: Path, model_name: str)

## Docstring

One document's semantic contribution per file (PLAN 15 capa 5): a write touches only
its own shard, never the whole store's.

## Imports

["__future__", "pathlib"]

## Purpose

One document's semantic contribution per file (PLAN 15 capa 5): a write touches only its own shard, never the whole store's.

## Architecture

Not documented.
