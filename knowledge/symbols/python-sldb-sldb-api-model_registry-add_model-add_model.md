---
id: python-sldb-sldb-api-model_registry-add_model-add_model
system: sldb
module: sldb.api.model_registry.add_model
qualname: add_model
kind: FunctionDef
source_path: sldb/api/model_registry/add_model.py
source_span: '19:43'
source_sha256: 2293c64804cdef109a82bad0dc6e58e3979b08f3638ed50302d570b8537cd23b
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.model_registry.add_model:add_model; contract-sha256:2a205fb834d0228f5765a35036538142e830363106c40d94f0416b86abf58f20
---

# add_model

## Signature

add_model(store: str | Path | None, model_ref: str, pythonpath: str | None=None, canonical: bool=False, actor: str | None=None)

## Docstring

Register the model class a reference names, with an empty documents index.

Args:
    store: The store to register in (path, alias, or None to discover it).
    model_ref: `module:ClassName` reference of a StructuredNLDoc subclass.
    pythonpath: Directory to import the model module from.
    canonical: Mark the model as the canonical one of its family.
    actor: Optional label recorded in the store journal for this write.

Returns:
    The new registry record (version 1).

Raises:
    SLDBModelError: When the reference cannot be imported or the model is already registered.

## Imports

["__future__", "inspect", "pathlib", "sldb.api.journal", "sldb.api.model_registry.model_index_writes", "sldb.api.model_registry.model_reference", "sldb.api.model_registry.model_registration", "sldb.api.stores.open_store", "sldb.core.exceptions", "sldb.store.io", "sldb.store.layout", "sldb.store.models.store_index"]

## Purpose

Not documented.

## Architecture

Not documented.
