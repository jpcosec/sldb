---
id: python-sldb-sldb-store-runtime_cache_signature-new_operation
system: sldb
module: sldb.store.runtime_cache_signature
qualname: new_operation
kind: FunctionDef
source_path: sldb/store/runtime_cache_signature.py
source_span: '39:43'
source_sha256: a53e7e05b193da104d58d7c75cd063563ac5c01177f1a3e334133091364d1058
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.runtime_cache_signature:new_operation; contract-sha256:a8ecba1b65e79d8757b4dbde6b94c8f52d214679cd8d8458b3529e973faf23a6
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

The start of a top-level operation on this store: the next `signature()`/`leaf()` call re-stats every tracked document once; calls within the same operation reuse those stats.

## Architecture

Not documented.
