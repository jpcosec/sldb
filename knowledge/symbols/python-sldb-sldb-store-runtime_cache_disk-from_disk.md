---
id: python-sldb-sldb-store-runtime_cache_disk-from_disk
system: sldb
module: sldb.store.runtime_cache_disk
qualname: from_disk
kind: FunctionDef
source_path: sldb/store/runtime_cache_disk.py
source_span: '44:52'
source_sha256: 53c815c1e872fef35964554eadff51bb1e63c753adc7343530396b79c213f62e
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.runtime_cache_disk:from_disk; contract-sha256:961dc84cffe95d9f4006d50ae3a5a9f22c7dc470585763736435f4f3124e5efa
---

# from_disk

## Signature

from_disk(s_path: Path, s_name: str, m_name: str, entry: Any, leaf: tuple, model_type: type)

## Docstring

A document whose payload the cache file already holds: no extraction. `leaf` is the
key material `runtime_cache.leaf_of` hands over — the document's file state plus the
model's model_hash — so a contract change misses here exactly like in memory.

## Imports

["__future__", "json", "pathlib", "sldb.store", "typing"]

## Purpose

A document whose payload the cache file already holds: no extraction. `leaf` is the key material `runtime_cache.leaf_of` hands over — the document's file state plus the model's model_hash — so a contract change misses here exactly like in memory.

## Architecture

Not documented.
