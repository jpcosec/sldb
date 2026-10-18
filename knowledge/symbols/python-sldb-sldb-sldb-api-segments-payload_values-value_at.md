---
id: python-sldb-sldb-sldb-api-segments-payload_values-value_at
system: sldb
module: sldb.sldb.api.segments.payload_values
qualname: value_at
kind: FunctionDef
source_path: sldb/api/segments/payload_values.py
source_span: '18:33'
source_sha256: a39d5165f9da7956b8203c06eeb7395918ae01dafc4379360934af42674f4ece
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.segments.payload_values:value_at; contract-sha256:26c0b3d3eecd6847e7de9f3a74fe6c873984cfc529aa3bdf1729e90ae4e9574d
---

# value_at

## Signature

value_at(payload: Any, path: str)

## Docstring

The value ``path`` addresses inside ``payload``, or None when absent.

Args:
    payload: The document payload to read from.
    path: Slash-separated field address, such as ``steps/2/title``.

Returns:
    The addressed value, or None when any part of the path is missing.

## Imports

["__future__", "sldb.api.schema.field_kinds", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
