---
id: python-sldb-sldb-api-segments-payload_values-value_at
system: sldb
module: sldb.api.segments.payload_values
qualname: value_at
kind: FunctionDef
source_path: sldb/api/segments/payload_values.py
source_span: '18:33'
source_sha256: a39d5165f9da7956b8203c06eeb7395918ae01dafc4379360934af42674f4ece
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.segments.payload_values:value_at; contract-sha256:e93749ce78bb4f3c5514cbe92671fe5ce252db2e05850a6a62c5f154d7628ed1
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

The value ``path`` addresses inside ``payload``, or None when absent.

## Architecture

Not documented.
