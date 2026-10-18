---
id: python-sldb-sldb-sldb-api-model_registry-model_reference-same_model_class
system: sldb
module: sldb.sldb.api.model_registry.model_reference
qualname: same_model_class
kind: FunctionDef
source_path: sldb/api/model_registry/model_reference.py
source_span: 78:86
source_sha256: 0625ce8c4bde65eac0438f8ffc40cef6c63d88666e334386598ca12b89707406
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.model_registry.model_reference:same_model_class;
  contract-sha256:513d0432bc71d95abde2b13903d22238011f38421b7a59f95847dacec8bf4b27
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
