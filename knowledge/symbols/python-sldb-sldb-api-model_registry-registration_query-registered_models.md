---
id: python-sldb-sldb-api-model_registry-registration_query-registered_models
system: sldb
module: sldb.api.model_registry.registration_query
qualname: registered_models
kind: FunctionDef
source_path: sldb/api/model_registry/registration_query.py
source_span: '16:22'
source_sha256: 90efa11245be48e7c63c873a9d451278ab8f21066c1c5f37ea2939eb5415c0d1
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.model_registry.registration_query:registered_models;
  contract-sha256:51cf62ed82427f6dbb60c07f948e4cf241e6f6f428574b1b7588314f74b1b570
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

Every model the store registers (its own and the ones it inherits), sorted by name.

## Architecture

Not documented.
