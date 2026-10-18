---
id: python-sldb-sldb-sldb-api-model_registry-federated_registration-_do_ensure_federated_model
system: sldb
module: sldb.sldb.api.model_registry.federated_registration
qualname: _do_ensure_federated_model
kind: FunctionDef
source_path: sldb/api/model_registry/federated_registration.py
source_span: 48:61
source_sha256: cb4870b6d4bfe1ec68122f61bc45b010bc99d9bfb249bc1d1e2e13184bbdbdfa
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.model_registry.federated_registration:_do_ensure_federated_model;
  contract-sha256:e9327669426c0750ff79ef026a3f2146e566ac57ebceea4a287b772ada448f4b
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

Not documented.

## Architecture

Not documented.
