---
id: python-sldb-sldb-sldb-store-runtime_cache_disk-flush
system: sldb
module: sldb.sldb.store.runtime_cache_disk
qualname: flush
kind: FunctionDef
source_path: sldb/store/runtime_cache_disk.py
source_span: '47:54'
source_sha256: fd8f4f04316af3f276c987e975d93464ec96316a2d3ec5eabf403a20378ff503
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.sldb.store.runtime_cache_disk:flush; contract-sha256:8d8305869ca75bdbe70eee2d4edb055a06b4d3bdf3ad19fa778db797f4ea00aa
---

# flush

## Signature

flush(s_path: Path, docs: dict[tuple, Any])

## Docstring

Write the file from every document of this store in memory: a full load just happened,
so that is the whole store, and stale signatures fall away.

## Imports

["__future__", "json", "pathlib", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
