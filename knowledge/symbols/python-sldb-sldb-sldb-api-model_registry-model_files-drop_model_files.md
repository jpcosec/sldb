---
id: python-sldb-sldb-sldb-api-model_registry-model_files-drop_model_files
system: sldb
module: sldb.sldb.api.model_registry.model_files
qualname: drop_model_files
kind: FunctionDef
source_path: sldb/api/model_registry/model_files.py
source_span: '16:22'
source_sha256: da591706804f1183166df962c481f51b111f0ed2400ad01204144945d46b6dfb
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.model_registry.model_files:drop_model_files;
  contract-sha256:da708a3427099d400d3dd8bc3520c878d0d04c2c1de7ee011bb59247cef71e1b
---

# drop_model_files

## Signature

drop_model_files(sp: Path, root: Path, name: str, models_index: str, documents_index: str)

## Docstring

Delete the model's indexes and shard directories; the caller holds the store lock.

## Imports

["__future__", "pathlib", "shutil", "sldb.store", "sldb.store.io", "sldb.store.io.shards", "sldb.store.layout"]

## Purpose

Not documented.

## Architecture

Not documented.
