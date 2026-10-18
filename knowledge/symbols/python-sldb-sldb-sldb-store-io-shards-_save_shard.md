---
id: python-sldb-sldb-sldb-store-io-shards-_save_shard
system: sldb
module: sldb.sldb.store.io.shards
qualname: _save_shard
kind: FunctionDef
source_path: sldb/store/io/shards.py
source_span: 53:61
source_sha256: 06c3fe7900d88e52e7539ef533eb6bed2d1ba9ba9c2f574542944038ff68e6f7
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.io.shards:_save_shard; contract-sha256:7af02fafc95e6ad4ec22726eb9335bc338aafc73cc4fff9d646c9c5aaa92b9dd
---

# _save_shard

## Signature

_save_shard(path: Path, value: Any, loader: Callable[[], T])

## Docstring

Write only when the content differs from the shard already there (the same "leave the
file alone" guarantee the single-file indexes always gave): a rebuild or a re-save of the
same value costs a read of the cached/on-disk shard, not a write.

## Imports

["__future__", "pathlib", "sldb.store.io.utils", "sldb.store.models", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
