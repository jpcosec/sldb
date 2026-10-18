---
id: python-sldb-sldb-api-model_registry-model_lineage-model_family
system: sldb
module: sldb.api.model_registry.model_lineage
qualname: model_family
kind: FunctionDef
source_path: sldb/api/model_registry/model_lineage.py
source_span: '11:21'
source_sha256: 7cd5ab2cb50ce291642cc427f146016805735f27060abfcab3176694d1767c33
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.model_registry.model_lineage:model_family;
  contract-sha256:351540bbdfbf7a7fdb62a837812502bf6e5ff7f71ad2b0b08e42a2eb40095ff9
---

# model_family

## Signature

model_family(model_type: type)

## Docstring

The model's declared `__family__`, the root branch it belongs to.

Args:
    model_type: The model class.

Returns:
    The family name, or None when the model declares none.

## Imports

["__future__", "sldb.models.structured_doc"]

## Purpose

The model's declared `__family__`, the root branch it belongs to.

## Architecture

Not documented.
