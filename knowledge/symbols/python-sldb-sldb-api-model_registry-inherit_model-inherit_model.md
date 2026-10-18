---
id: python-sldb-sldb-api-model_registry-inherit_model-inherit_model
system: sldb
module: sldb.api.model_registry.inherit_model
qualname: inherit_model
kind: FunctionDef
source_path: sldb/api/model_registry/inherit_model.py
source_span: '20:49'
source_sha256: 5d783eb4a01a532d4e4c8ed57e475eed1a1eda83cbd3d9d788363fa71bcbb831
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.model_registry.inherit_model:inherit_model;
  contract-sha256:05cf7208e45a1245f5f4ae727e1ede98d3ff199bf69ae2c519d3e51f41378391
---

# inherit_model

## Signature

inherit_model(store: str | Path | None, ref: str, pythonpath: str | None=None, actor: str | None=None)

## Docstring

Register `alias:ModelName` as inherited from the store linked as `alias`.

A copy of that model already registered here (same `model_ref`) is converted in place:
its documents, roster and signed contract stay; only the source path goes, and the class
imports from the owner's project root from then on. If the owner's class has moved since
this store signed it, `stores check` reports `contract moved` and `stores update` fixes it.

Args:
    store: The store (path, alias, or None to discover it).
    ref: `alias:ModelName`, the alias being a store this store links (`stores add`).
    pythonpath: Directory to import the store's other models from (indexes are rebuilt).
    actor: Optional label recorded in the store journal for this write.

Returns:
    The inherited entry's registry record.

Raises:
    SLDBStoreError: The alias is not linked, or the linked store does not own the model.
    SLDBModelError: A model of that name here is another class (an override: give it a name
        of its own that extends the owner's), or it already inherits from another store.

## Imports

["__future__", "pathlib", "sldb.api.journal", "sldb.api.model_registry.federated_registration", "sldb.api.model_registry.model_reference", "sldb.api.model_registry.model_registration", "sldb.api.stores.open_store", "sldb.core.exceptions", "sldb.store.derived_rebuild", "sldb.store.io", "sldb.store.layout", "sldb.store.model_origin", "sldb.store.ops"]

## Purpose

Register `alias:ModelName` as inherited from the store linked as `alias`.

## Architecture

Not documented.
