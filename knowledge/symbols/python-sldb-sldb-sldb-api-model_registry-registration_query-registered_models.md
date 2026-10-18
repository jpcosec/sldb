---
id: python-sldb-sldb-sldb-api-model_registry-registration_query-registered_models
system: sldb
module: sldb.sldb.api.model_registry.registration_query
qualname: registered_models
kind: FunctionDef
source_path: sldb/api/model_registry/registration_query.py
source_span: '16:22'
source_sha256: 90efa11245be48e7c63c873a9d451278ab8f21066c1c5f37ea2939eb5415c0d1
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.model_registry.registration_query:registered_models;
  contract-sha256:f44f5c3be300865f919d91d96204e57c923245f4b59a52b10ab930605d2c5c6f
---

# registered_models

## Signature

registered_models(store: str | Path | None)

## Docstring

Every model the store registers (its own and the ones it inherits), sorted by name.

Args:
    store: The store (path, alias, or None to discover it).

## Imports

["__future__", "pathlib", "sldb.api.stores.open_store", "sldb.store.io", "sldb.store.models.model_entry"]

## Purpose

Not documented.

## Architecture

Not documented.
