---
id: python-sldb-sldb-api-model_registry-registration_query-is_model_registered
system: sldb
module: sldb.api.model_registry.registration_query
qualname: is_model_registered
kind: FunctionDef
source_path: sldb/api/model_registry/registration_query.py
source_span: '25:28'
source_sha256: 90efa11245be48e7c63c873a9d451278ab8f21066c1c5f37ea2939eb5415c0d1
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.model_registry.registration_query:is_model_registered;
  contract-sha256:ff9a0d8618359ecbf5d93adf360d670670361b07590d9f63dc5835a7dad09e0d
---

# is_model_registered

## Signature

is_model_registered(store: str | Path | None, model: str)

## Docstring

Whether `model` is registered: by name (`TaskDoc`), or by reference
(`deskops.models:TaskDoc` or `deskops.models.TaskDoc`).

## Imports

["__future__", "pathlib", "sldb.api.stores.open_store", "sldb.store.io", "sldb.store.models.model_entry"]

## Purpose

Whether `model` is registered: by name (`TaskDoc`), or by reference (`deskops.models:TaskDoc` or `deskops.models.TaskDoc`).

## Architecture

Not documented.
