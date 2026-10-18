---
id: python-sldb-sldb-sldb-store-runtime_cache_disk-from_disk
system: sldb
module: sldb.sldb.store.runtime_cache_disk
qualname: from_disk
kind: FunctionDef
source_path: sldb/store/runtime_cache_disk.py
source_span: '44:52'
source_sha256: 53c815c1e872fef35964554eadff51bb1e63c753adc7343530396b79c213f62e
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.runtime_cache_disk:from_disk; contract-sha256:6b68deb5e5b58a0be2fed91a612fe4cfcabd18af5232c09d3d353e02720c459b
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

Not documented.

## Architecture

Not documented.
