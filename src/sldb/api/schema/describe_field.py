"""Describe the fields of a model class for forms and schemas."""

from __future__ import annotations

from typing import Any

from pydantic.fields import FieldInfo

from sldb.api.schema.field_description import FieldDescription
from sldb.api.schema.field_descriptor import field_descriptor


def describe_field(name: str, field: FieldInfo) -> FieldDescription:
    """Describe one pydantic field: kind, requiredness, enum values, annotation and description.

    Args:
        name: Field name.
        field: The field's `FieldInfo`, e.g. `Model.model_fields[name]`.

    Returns:
        The field description.
    """
    annotation = getattr(field.annotation, "__name__", repr(field.annotation))
    return FieldDescription(**field_descriptor(name, field), annotation=annotation, description=field.description or "")


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
