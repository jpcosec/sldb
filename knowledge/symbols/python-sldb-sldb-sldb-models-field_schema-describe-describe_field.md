---
id: python-sldb-sldb-sldb-models-field_schema-describe-describe_field
system: sldb
module: sldb.sldb.models.field_schema.describe
qualname: describe_field
kind: FunctionDef
source_path: sldb/models/field_schema/describe.py
source_span: '16:27'
source_sha256: 8c8a559bb560bc40662ff3f69a227ad8778a26b343277b09503b485add869d26
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.models.field_schema.describe:describe_field;
  contract-sha256:9e2432560a227d807d165d8d2540a8d4f2924f52fcf190b97ad8657652376bfc
---

# describe_field

## Signature

describe_field(name: str, field: FieldInfo)

## Docstring

Describe one pydantic field: kind, requiredness, enum values, annotation and description.

Args:
    name: Field name.
    field: The field's `FieldInfo`, e.g. `Model.model_fields[name]`.

Returns:
    The field description.

## Imports

["__future__", "pydantic.fields", "sldb.models.field_schema.description", "sldb.models.field_schema.descriptor"]

## Purpose

Not documented.

## Architecture

Not documented.
