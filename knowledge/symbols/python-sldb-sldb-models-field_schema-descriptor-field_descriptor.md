---
id: python-sldb-sldb-models-field_schema-descriptor-field_descriptor
system: sldb
module: sldb.models.field_schema.descriptor
qualname: field_descriptor
kind: FunctionDef
source_path: sldb/models/field_schema/descriptor.py
source_span: '14:30'
source_sha256: f2d99a84dff05a210101bb78b606f903c9d3f270335aec14d9af51f7c3d0d116
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.models.field_schema.descriptor:field_descriptor;
  contract-sha256:22175f5e868fe325c8b771885c2652fbfb289ed2b785a74ba4e7cacc0f64a433
---

# field_descriptor

## Signature

field_descriptor(name: str, field: Any)

## Docstring

JSON-ready descriptor `{name, kind, required, description[, enum]}`.

Args:
    name: Field name.
    field: The pydantic `FieldInfo`.

Returns:
    The descriptor; `enum` is present only for Literal/Enum fields.

`description` is not decoration: `StructuredNLDoc` refuses to define a model with a
field that lacks one, so it is part of the contract. Omitting it here made the schema
endpoint the one place a consumer could not read what the contract guarantees.

## Imports

["__future__", "sldb.models.field_schema.kinds", "typing"]

## Purpose

JSON-ready descriptor `{name, kind, required, description[, enum]}`.

## Architecture

Not documented.
