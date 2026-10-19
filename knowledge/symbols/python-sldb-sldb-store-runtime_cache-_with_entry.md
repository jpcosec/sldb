---
id: python-sldb-sldb-store-runtime_cache-_with_entry
system: sldb
module: sldb.store.runtime_cache
qualname: _with_entry
kind: FunctionDef
source_path: sldb/store/runtime_cache.py
source_span: 72:82
source_sha256: 870a33b2e031d380c875372e22bbf508b533af2cbd6dae4f59d6ddb6e563db78
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.runtime_cache:_with_entry; contract-sha256:1f7f99978c7e9af67fe746d137c1e870547eb3030fcee162ea364f6502138f49
---

# _with_entry

## Signature

_with_entry(key: tuple, hit: Any, entry: Any)

## Docstring

The name, the tags and the two index hashes come from the index and can change without
the text changing; the cached object is stamped with the entry's current values.

## Imports

["__future__", "dataclasses", "pathlib", "sldb.store", "sldb.store.hashing", "sldb.store.runtime_cache_signature", "typing"]

## Purpose

The name, the tags and the two index hashes come from the index and can change without the text changing; the cached object is stamped with the entry's current values.

## Architecture

Not documented.
