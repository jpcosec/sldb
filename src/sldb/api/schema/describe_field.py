"""Describe the fields of a model class for forms and schemas."""

from __future__ import annotations

from typing import Any

from sldb.models.field_schema.describe import describe_field
from sldb.models.field_schema.description import FieldDescription


def describe_model_fields(model_type: type[Any]) -> list[FieldDescription]:
    """Describe every field of a pydantic model class, in declaration order.

    Args:
        model_type: A pydantic model class, typically a StructuredNLDoc subclass.

    Returns:
        One description per field.
    """
    return [describe_field(name, field) for name, field in model_type.model_fields.items()]


def schema_snapshot(model_type: type[Any], version: int) -> dict[str, Any]:
    """A journal-ready snapshot of a model's contract: its version and every field."""
    return {"version": version, "fields": [f.model_dump() for f in describe_model_fields(model_type)]}
