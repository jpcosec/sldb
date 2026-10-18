---
id: python-sldb-sldb-sldb-api-model_registry-model_lineage-model_base_names
system: sldb
module: sldb.sldb.api.model_registry.model_lineage
qualname: model_base_names
kind: FunctionDef
source_path: sldb/api/model_registry/model_lineage.py
source_span: '24:39'
source_sha256: 7cd5ab2cb50ce291642cc427f146016805735f27060abfcab3176694d1767c33
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.model_registry.model_lineage:model_base_names;
  contract-sha256:480e662dbb518f63be7d8e1d4ca2ce47a59b1308c0be6bdf20f0ce959969e12b
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
