---
id: python-sldb-sldb-store-runtime_cache_disk-forget
system: sldb
module: sldb.store.runtime_cache_disk
qualname: forget
kind: FunctionDef
source_path: sldb/store/runtime_cache_disk.py
source_span: 77:89
source_sha256: 53c815c1e872fef35964554eadff51bb1e63c753adc7343530396b79c213f62e
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.runtime_cache_disk:forget; contract-sha256:a904f8190774675b99e186d8d0507c69f8a1033050445704c8199a999178ddb7
---

# forget

## Signature

forget(s_path: Path, predicate: Any)

## Docstring

Drop every cache entry whose key matches, and rewrite the file. Returns how many.

For deletions: a document that no longer exists keeps its entry here until some
process does a full load and `flush` rewrites the whole file.

## Imports

["__future__", "json", "pathlib", "sldb.store", "typing"]

## Purpose

Drop every cache entry whose key matches, and rewrite the file. Returns how many.

## Architecture

Not documented.
