---
id: python-sldb-sldb-sldb-api-model_registry-reindex_model-reindex_model
system: sldb
module: sldb.sldb.api.model_registry.reindex_model
qualname: reindex_model
kind: FunctionDef
source_path: sldb/api/model_registry/reindex_model.py
source_span: '19:41'
source_sha256: 45db2b343e573f7c76efbfee630d57af9615e4cc7570ac181486b017e8c4fc9f
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.model_registry.reindex_model:reindex_model;
  contract-sha256:6e157d1f203b61e57de05b1e6085cdd2932cb4b56273916214d62585c787ad24
---

# reindex_model

## Signature

reindex_model(store: str | Path | None, model_name: str, pythonpath: str | None=None, bump_version: bool=False, actor: str | None=None)

## Docstring

Rehash every document of a model and rebuild the store's derived indexes.

Args:
    store: The store holding the model (path, alias, or None to discover it).
    model_name: Registered model name.
    pythonpath: Directory to import the model module from.
    bump_version: Increase the model's contract version (done when a draft is promoted).
    actor: Optional label recorded in the store journal for this write.

Returns:
    The model's registry record after the reindex.

Raises:
    SLDBModelError: When the model is not registered or cannot be imported.

## Imports

["__future__", "pathlib", "sldb.api.journal", "sldb.api.model_registry.model_index_writes", "sldb.api.model_registry.model_reference", "sldb.api.model_registry.model_registration", "sldb.api.schema.describe_field", "sldb.api.stores.open_store", "sldb.core.exceptions", "sldb.store.io", "sldb.store.models.model_entry", "sldb.store.models.store_index"]

## Purpose

Not documented.

## Architecture

Not documented.
