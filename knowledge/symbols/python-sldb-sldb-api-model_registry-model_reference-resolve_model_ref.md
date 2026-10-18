---
id: python-sldb-sldb-api-model_registry-model_reference-resolve_model_ref
system: sldb
module: sldb.api.model_registry.model_reference
qualname: resolve_model_ref
kind: FunctionDef
source_path: sldb/api/model_registry/model_reference.py
source_span: 54:75
source_sha256: 0625ce8c4bde65eac0438f8ffc40cef6c63d88666e334386598ca12b89707406
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.model_registry.model_reference:resolve_model_ref;
  contract-sha256:3dc6062f786e57e5e4af18d1eb6018c14a156f84ab82f56bb2ca28bed13731e6
---

# resolve_model_ref

## Signature

resolve_model_ref(model_ref: str, pythonpath: str | None=None)

## Docstring

Import the StructuredNLDoc subclass a model reference names.

Args:
    model_ref: Reference of the form `module:ClassName` (the attribute may be dotted).
    pythonpath: Directory to import the module from, ahead of the working directory.

Returns:
    The model class.

Raises:
    SLDBModelError: When the reference is malformed, cannot be imported, or does not
        name a StructuredNLDoc subclass.

## Imports

["__future__", "importlib", "pathlib", "sldb.core.exceptions", "sldb.models.structured_doc", "sys", "typing"]

## Purpose

Import the StructuredNLDoc subclass a model reference names.

## Architecture

Not documented.
