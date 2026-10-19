---
id: python-sldb-sldb-api-model_registry-federated_registration-_do_ensure_federated_model
system: sldb
module: sldb.api.model_registry.federated_registration
qualname: _do_ensure_federated_model
kind: FunctionDef
source_path: sldb/api/model_registry/federated_registration.py
source_span: 48:61
source_sha256: cb4870b6d4bfe1ec68122f61bc45b010bc99d9bfb249bc1d1e2e13184bbdbdfa
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.model_registry.federated_registration:_do_ensure_federated_model;
  contract-sha256:f005fe79b7bd1bd93e3e85ffded39def8810a3c61a6eeb033f6ffdfba339d507
---

# _do_ensure_federated_model

## Signature

_do_ensure_federated_model(store_path: Path, root: Path, model_type: type[StructuredNLDoc], model_ref: str, rel_model_path: str, origin: str | None=None)

## Docstring

Register the model unless a concurrent writer already did (checked under the lock).

With `origin` the entry is inherited from the store linked under that alias: no source
path of its own (see sldb.store.model_origin).

## Imports

["__future__", "pathlib", "sldb.models.structured_doc", "sldb.store.hashing", "sldb.store.io", "sldb.store.layout", "sldb.store.model_node", "sldb.store.models.documents_index", "sldb.store.models.model_entry", "sldb.store.models.models_index", "sldb.store.ops", "sldb.store.semantic_tags", "typing"]

## Purpose

Register the model unless a concurrent writer already did (checked under the lock).

## Architecture

Not documented.
