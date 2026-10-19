---
id: python-sldb-sldb-store-runtime_cache_disk-flush
system: sldb
module: sldb.store.runtime_cache_disk
qualname: flush
kind: FunctionDef
source_path: sldb/store/runtime_cache_disk.py
source_span: 55:62
source_sha256: 53c815c1e872fef35964554eadff51bb1e63c753adc7343530396b79c213f62e
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.runtime_cache_disk:flush; contract-sha256:0e828f8877ea93ccc43c9518d296486585a20c75be1588cf8f15ac963dae87b2
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

Write the file from every document of this store in memory: a full load just happened, so that is the whole store, and stale signatures fall away.

## Architecture

Not documented.
