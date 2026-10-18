---
id: python-sldb-sldb-store-runtime_cache_signature-forget
system: sldb
module: sldb.store.runtime_cache_signature
qualname: forget
kind: FunctionDef
source_path: sldb/store/runtime_cache_signature.py
source_span: '46:53'
source_sha256: a53e7e05b193da104d58d7c75cd063563ac5c01177f1a3e334133091364d1058
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.runtime_cache_signature:forget; contract-sha256:0ebb99da96aaf4a31ed2790759f20128addc092a3ce7f1d2366284f06be4f0ca
---

# forget

## Signature

forget(s_path: Path | None)

## Docstring

Drop the remembered sweep so the next signature() redoes it (invalidate_runtime_cache).

## Imports

["__future__", "os", "pathlib", "sldb.store.io", "sldb.store.layout", "typing"]

## Purpose

Drop the remembered sweep so the next signature() redoes it (invalidate_runtime_cache).

## Architecture

Not documented.
