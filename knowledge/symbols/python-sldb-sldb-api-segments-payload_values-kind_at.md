---
id: python-sldb-sldb-api-segments-payload_values-kind_at
system: sldb
module: sldb.api.segments.payload_values
qualname: kind_at
kind: FunctionDef
source_path: sldb/api/segments/payload_values.py
source_span: 56:73
source_sha256: a39d5165f9da7956b8203c06eeb7395918ae01dafc4379360934af42674f4ece
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.segments.payload_values:kind_at; contract-sha256:a13fa48b879196cea774336527356f08da3a331609c04a8771451e1d77b0394a
---

# kind_at

## Signature

kind_at(model_type: type, path: str)

## Docstring

The input kind of the field ``path`` addresses in ``model_type``.

Args:
    model_type: The ``StructuredNLDoc`` subclass owning the field.
    path: Slash-separated field address, such as ``tags/0``.

Returns:
    A kind from ``sldb.api.schema.field_kinds``, or ``"unknown"``.

## Imports

["__future__", "sldb.api.schema.field_kinds", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
