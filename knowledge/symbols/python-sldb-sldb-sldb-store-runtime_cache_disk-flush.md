---
id: python-sldb-sldb-sldb-store-runtime_cache_disk-flush
system: sldb
module: sldb.sldb.store.runtime_cache_disk
qualname: flush
kind: FunctionDef
source_path: sldb/store/runtime_cache_disk.py
source_span: 55:62
source_sha256: 53c815c1e872fef35964554eadff51bb1e63c753adc7343530396b79c213f62e
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.runtime_cache_disk:flush; contract-sha256:6a64d12852744c359510e44a4bf21071cf4967c4745ee5a344414e542009b0e4
---

# flush

## Signature

flush(s_path: Path, docs: dict[tuple, Any])

## Docstring

Write the file from every document of this store in memory: a full load just happened,
so that is the whole store, and stale signatures fall away.

## Imports

["__future__", "json", "pathlib", "sldb.store", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
