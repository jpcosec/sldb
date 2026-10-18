---
id: python-sldb-sldb-store-io-shards-prune_shards
system: sldb
module: sldb.store.io.shards
qualname: prune_shards
kind: FunctionDef
source_path: sldb/store/io/shards.py
source_span: 120:126
source_sha256: 06c3fe7900d88e52e7539ef533eb6bed2d1ba9ba9c2f574542944038ff68e6f7
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.io.shards:prune_shards; contract-sha256:5262b5afbb10bfd6f36770fa957e988178c4b4391eedbd105c511683e7e896a8
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

Delete every shard whose document is no longer tracked (PLAN 15 capa 5: a document untracked or deleted loses its semantic/sections shard right away, not just its entry in an aggregate that happens to get rebuilt without it).

## Architecture

Not documented.
