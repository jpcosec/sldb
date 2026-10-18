---
id: python-sldb-sldb-sldb-api-model_registry-describe_model-describe_model
system: sldb
module: sldb.sldb.api.model_registry.describe_model
qualname: describe_model
kind: FunctionDef
source_path: sldb/api/model_registry/describe_model.py
source_span: '19:42'
source_sha256: 689cf4d607416e15590456cce296aa1772a514d95b375da077bb1b90e7230223
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.model_registry.describe_model:describe_model;
  contract-sha256:a76661e8c4374cf75cdb533a8b13f466e5bd81602aadffbaf0212b41c700108e
---

# describe_model

## Signature

describe_model(store: str | Path | None, model_name: str, pythonpath: str | None=None)

## Docstring

Read a registered model's contract and documents.

Only this model's class is imported, so a broken sibling model does not prevent it.

Args:
    store: The store holding the model (path, alias, or None to discover it).
    model_name: Registered model name.
    pythonpath: Directory to import the model module from.

Returns:
    The model's registry record, fields and documents.

Raises:
    SLDBModelError: When the model is not registered or cannot be imported.

## Imports

["__future__", "pathlib", "sldb.api.model_registry.model_description", "sldb.api.model_registry.model_document_summary", "sldb.api.model_registry.model_field_summary", "sldb.api.model_registry.model_reference", "sldb.api.schema.field_kinds", "sldb.api.stores.open_store", "sldb.core.exceptions", "sldb.models.structured_doc", "sldb.store.io", "sldb.store.models.models_index"]

## Purpose

Not documented.

## Architecture

Not documented.
