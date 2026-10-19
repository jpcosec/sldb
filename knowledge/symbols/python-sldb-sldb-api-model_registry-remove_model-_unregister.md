---
id: python-sldb-sldb-api-model_registry-remove_model-_unregister
system: sldb
module: sldb.api.model_registry.remove_model
qualname: _unregister
kind: FunctionDef
source_path: sldb/api/model_registry/remove_model.py
source_span: '49:59'
source_sha256: c74f8174a85521bc8296eee2045d247a2369edd3c5531240a6360569f2461436
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.model_registry.remove_model:_unregister; contract-sha256:56e253f5ff7a9518c78d951adeb20c1125663a94caf48c63d242d12318d63f81
---

# _unregister

## Signature

_unregister(sp: Path, root: Path, idx, entry, pythonpath: str | None)

## Docstring

Registry first, files last: if a rebuild raises, the store index is put back and the
model's files were never touched.

## Imports

["__future__", "pathlib", "sldb.api.journal", "sldb.api.model_registry.model_files", "sldb.api.model_registry.model_reference", "sldb.api.model_registry.model_registration", "sldb.api.stores.open_store", "sldb.core.exceptions", "sldb.store", "sldb.store.derived_rebuild", "sldb.store.io", "sldb.store.io.rollback", "sldb.store.layout", "sldb.store.ops"]

## Purpose

Registry first, files last: if a rebuild raises, the store index is put back and the model's files were never touched.

## Architecture

Not documented.
