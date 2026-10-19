---
id: python-sldb-sldb-api-model_registry-federated_registration-_ensure_federated_model_entry
system: sldb
module: sldb.api.model_registry.federated_registration
qualname: _ensure_federated_model_entry
kind: FunctionDef
source_path: sldb/api/model_registry/federated_registration.py
source_span: 64:71
source_sha256: cb4870b6d4bfe1ec68122f61bc45b010bc99d9bfb249bc1d1e2e13184bbdbdfa
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.model_registry.federated_registration:_ensure_federated_model_entry;
  contract-sha256:0e448739fa5788f6f14e03381e7ecffb3bd9318ac248067c2a50118bf8899279
---

# _ensure_federated_model_entry

## Signature

_ensure_federated_model_entry(store_path: Path, root: Path, store_index: Any, model_type: type[StructuredNLDoc], model_ref: str, model_path: Path, origin: str | None=None)

## Docstring

The destination store's entry for the model, registering it first when missing.

## Imports

["__future__", "pathlib", "sldb.models.structured_doc", "sldb.store.hashing", "sldb.store.io", "sldb.store.layout", "sldb.store.model_node", "sldb.store.models.documents_index", "sldb.store.models.model_entry", "sldb.store.models.models_index", "sldb.store.ops", "sldb.store.semantic_tags", "typing"]

## Purpose

The destination store's entry for the model, registering it first when missing.

## Architecture

Not documented.
