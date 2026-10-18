---
id: python-sldb-sldb-sldb-store-io-shards-prune_shards
system: sldb
module: sldb.sldb.store.io.shards
qualname: prune_shards
kind: FunctionDef
source_path: sldb/store/io/shards.py
source_span: 120:126
source_sha256: 06c3fe7900d88e52e7539ef533eb6bed2d1ba9ba9c2f574542944038ff68e6f7
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.io.shards:prune_shards; contract-sha256:80d4eacc059f72dcfe0fa8c6dff20323fce492c19aea694d9539e32f81c41f0e
---

# prune_shards

## Signature

prune_shards(shards_dir: Path, current_names: set)

## Docstring

Delete every shard whose document is no longer tracked (PLAN 15 capa 5: a document
untracked or deleted loses its semantic/sections shard right away, not just its entry
in an aggregate that happens to get rebuilt without it).

## Imports

["__future__", "pathlib", "sldb.store.io.utils", "sldb.store.models", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
