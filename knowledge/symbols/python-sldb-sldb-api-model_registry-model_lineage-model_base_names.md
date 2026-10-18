---
id: python-sldb-sldb-api-model_registry-model_lineage-model_base_names
system: sldb
module: sldb.api.model_registry.model_lineage
qualname: model_base_names
kind: FunctionDef
source_path: sldb/api/model_registry/model_lineage.py
source_span: '24:39'
source_sha256: 7cd5ab2cb50ce291642cc427f146016805735f27060abfcab3176694d1767c33
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.model_registry.model_lineage:model_base_names;
  contract-sha256:71a01271f0567422d39a7ab2e740c3039a266a865e8d029f21c1d1b62b492763
---

# model_base_names

## Signature

model_base_names(model_type: type)

## Docstring

Names of the StructuredNLDoc bases above this model, nearest first.

Recorded so `st.{Base+}` families and `model <= Base` filters are legible from the
store index without importing the class.

Args:
    model_type: The model class.

Returns:
    Base class names, excluding StructuredNLDoc itself.

## Imports

["__future__", "sldb.models.structured_doc"]

## Purpose

Not documented.

## Architecture

Not documented.
