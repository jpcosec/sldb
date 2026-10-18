---
id: python-sldb-sldb-cli-serve-schema-field_descriptor_with_default
system: sldb
module: sldb.cli.serve.schema
qualname: field_descriptor_with_default
kind: FunctionDef
source_path: sldb/cli/serve/schema.py
source_span: 76:87
source_sha256: 76f8b45e5120c346a3c61e1323aee0a30ab7eea163c4cb893e47708b9fcb0f31
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.cli.serve.schema:field_descriptor_with_default;
  contract-sha256:15e7fce42c6cfc418379104199dc540b8a9c6e46323d54930d7e3ed8b63e98ee
---

# field_descriptor_with_default

## Signature

field_descriptor_with_default(name: str, field: Any)

## Docstring

Field descriptor plus the declared default when the field has one.

``PydanticUndefined`` (required or ``default_factory``) omits the key;
enum defaults serialize as their value.

## Imports

["__future__", "enum", "pathlib", "pydantic_core", "sldb.api.schema.field_descriptor", "sldb.api.schema.field_kinds", "sldb.api.schema.store_schema", "sldb.api.schema.unavailable_model", "sldb.cli.model_utils", "sldb.models.structured_doc", "sldb.store.io", "typing"]

## Purpose

Field descriptor plus the declared default when the field has one.

## Architecture

Not documented.
