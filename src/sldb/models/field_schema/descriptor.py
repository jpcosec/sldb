"""The plain descriptor of one model field that sldb serve's schema endpoint returns.

Moved here from `sldb.api.schema.field_descriptor` (and before that `sldb.cli.serve.schema`), which re-export
these names: the store describes fields too, and must not reach up into the operations layer.
"""

from __future__ import annotations

from typing import Any

from sldb.models.field_schema.kinds import enum_values, field_kind, unwrap_annotation


def field_descriptor(name: str, field: Any) -> dict[str, Any]:
    """JSON-ready descriptor `{name, kind, required, description[, enum]}`.

    Args:
        name: Field name.
        field: The pydantic `FieldInfo`.

    Returns:
        The descriptor; `enum` is present only for Literal/Enum fields.

    `description` is not decoration: `StructuredNLDoc` refuses to define a model with a
    field that lacks one, so it is part of the contract. Omitting it here made the schema
    endpoint the one place a consumer could not read what the contract guarantees.
    """
    annotation = unwrap_annotation(field.annotation)
    data = {"name": name, "kind": field_kind(annotation), "required": field.is_required(), "description": field.description or ""}
    return add_enum_values(data, annotation)


def add_enum_values(data: dict[str, Any], annotation: Any) -> dict[str, Any]:
    """Add the allowed `enum` values to a descriptor when the annotation has them."""
    values = enum_values(annotation)
    if values is not None:
        data["enum"] = values
    return data
