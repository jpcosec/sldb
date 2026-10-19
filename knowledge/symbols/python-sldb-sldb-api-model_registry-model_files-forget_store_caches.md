---
id: python-sldb-sldb-api-model_registry-model_files-forget_store_caches
system: sldb
module: sldb.api.model_registry.model_files
qualname: forget_store_caches
kind: FunctionDef
source_path: sldb/api/model_registry/model_files.py
source_span: '25:29'
source_sha256: da591706804f1183166df962c481f51b111f0ed2400ad01204144945d46b6dfb
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.model_registry.model_files:forget_store_caches;
  contract-sha256:28ab5b499181566db9d53222a0303b7aadd7dcd2013489b5efa19db4bf9fdb42
---

# forget_store_caches

## Signature

forget_store_caches(sp: Path, name: str)

## Docstring

Drop every in-memory copy of the store's indexes and of one model's shards.

## Imports

["__future__", "pathlib", "shutil", "sldb.store", "sldb.store.io", "sldb.store.io.shards", "sldb.store.layout"]

## Purpose

Drop every in-memory copy of the store's indexes and of one model's shards.

## Architecture

Not documented.
