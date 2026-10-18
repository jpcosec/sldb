---
id: python-sldb-sldb-sldb-store-runtime_cache_signature-new_operation
system: sldb
module: sldb.sldb.store.runtime_cache_signature
qualname: new_operation
kind: FunctionDef
source_path: sldb/store/runtime_cache_signature.py
source_span: '39:43'
source_sha256: a53e7e05b193da104d58d7c75cd063563ac5c01177f1a3e334133091364d1058
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.runtime_cache_signature:new_operation;
  contract-sha256:f4b019c6b3f565ec08d44b3ac472682423189e808fd91904438f6a1ed87f3146
---

# new_operation

## Signature

new_operation(s_path: Path)

## Docstring

The start of a top-level operation on this store: the next `signature()`/`leaf()` call
re-stats every tracked document once; calls within the same operation reuse those stats.

## Imports

["__future__", "os", "pathlib", "sldb.store.io", "sldb.store.layout", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
