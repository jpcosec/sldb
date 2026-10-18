---
id: python-sldb-sldb-api-documents-data_values-parse_data_value
system: sldb
module: sldb.api.documents.data_values
qualname: parse_data_value
kind: FunctionDef
source_path: sldb/api/documents/data_values.py
source_span: '14:29'
source_sha256: ac7fbf344a931ac23fdaaf764b5cc82447647176b6d5172348603320f5020c25
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.documents.data_values:parse_data_value; contract-sha256:cefbb71f1f165e26473465c8b69cb41bcdc532502e373546bd2a6e3f14a7fdf1
---

# parse_data_value

## Signature

parse_data_value(raw: str)

## Docstring

Parse JSON/YAML scalars or objects from a string.

Args:
    raw: Text such as `5`, `"Pending"`, `[a, b]` or `{k: v}`.

Returns:
    The parsed value.

Raises:
    yaml.YAMLError: When the text is neither valid JSON nor valid YAML.

## Imports

["__future__", "json", "typing", "yaml"]

## Purpose

Not documented.

## Architecture

Not documented.
