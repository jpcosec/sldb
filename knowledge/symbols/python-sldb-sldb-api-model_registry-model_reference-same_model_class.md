---
id: python-sldb-sldb-api-model_registry-model_reference-same_model_class
system: sldb
module: sldb.api.model_registry.model_reference
qualname: same_model_class
kind: FunctionDef
source_path: sldb/api/model_registry/model_reference.py
source_span: 78:86
source_sha256: 0625ce8c4bde65eac0438f8ffc40cef6c63d88666e334386598ca12b89707406
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.model_registry.model_reference:same_model_class;
  contract-sha256:966a0842a12a48e8c54ec9e9dd9472a36fed6db511eee21137d7aeb53855a5be
---

# same_model_class

## Signature

same_model_class(ref_a: str, ref_b: str, pythonpath: str | None=None)

## Docstring

Whether two references name one class: equal strings, or both import to the same object
(`deskops.models.atom:AtomDoc` is `deskops.models:AtomDoc` when the package re-exports it).

## Imports

["__future__", "importlib", "pathlib", "sldb.core.exceptions", "sldb.models.structured_doc", "sys", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
