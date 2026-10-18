---
id: python-sldb-sldb-api-model_registry-load_registered_model-load_registered_model
system: sldb
module: sldb.api.model_registry.load_registered_model
qualname: load_registered_model
kind: FunctionDef
source_path: sldb/api/model_registry/load_registered_model.py
source_span: '14:38'
source_sha256: 1c289bdcb3da8677051717b7f9ef784ac1e85a6c910bf16fff9f65582bc70eab
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.model_registry.load_registered_model:load_registered_model;
  contract-sha256:ced81310ffa516f2e02f4a85aa33bd244f7bcb6b4d1fb91a4d804c6600a2df27
---

# load_registered_model

## Signature

load_registered_model(store_path: Path, model_name: str, pythonpath: str | None=None)

## Docstring

Resolve a registered model name to its class and registry entry.

Args:
    store_path: An already resolved `.sldb` directory (see `open_store`).
    model_name: A model name registered in the store, or `alias:ModelName` for a model
        owned by a linked store (registered locally on first use).
    pythonpath: Directory to import the model module from.

Returns:
    The model class, its entry, and the store index holding the entry.

Raises:
    SLDBStoreError: When no such model is registered.
    SLDBModelError: When the registered reference cannot be imported.

## Imports

["__future__", "pathlib", "sldb.api.model_registry.federated_lookup", "sldb.api.model_registry.model_reference", "sldb.api.model_registry.registered_model", "sldb.core.exceptions", "sldb.store.io"]

## Purpose

Not documented.

## Architecture

Not documented.
