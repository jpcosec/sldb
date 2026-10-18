---
id: python-sldb-sldb-sldb-api-model_drafts-source_location-locate_model_source
system: sldb
module: sldb.sldb.api.model_drafts.source_location
qualname: locate_model_source
kind: FunctionDef
source_path: sldb/api/model_drafts/source_location.py
source_span: '34:56'
source_sha256: ed7e4fe313de48f5f9555d133899b3e6b93e9a592f27835024c046ab7c4c32ec
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.model_drafts.source_location:locate_model_source;
  contract-sha256:4b5510a0b24473ad9a381d217e8c372f67225e444278c5be119ccfd5a1488dbb
---

# locate_model_source

## Signature

locate_model_source(store: str | Path | None, model_name: str, pythonpath: str | None=None)

## Docstring

Find the file and class that define a registered model.

Args:
    store: The store registering the model (path, alias, or None to discover it).
    model_name: Registered model name.
    pythonpath: Directory to import re-export modules from; defaults to the project root.

Returns:
    The defining source file, module and attribute path.

Raises:
    SLDBModelError: When the model is not registered.

## Imports

["__future__", "ast", "inspect", "pathlib", "sldb.api.model_drafts.model_source", "sldb.api.model_registry.model_reference", "sldb.api.stores.open_store", "sldb.core.exceptions", "sldb.store.io"]

## Purpose

Not documented.

## Architecture

Not documented.
