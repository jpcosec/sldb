"""The plain descriptor of one model field that sldb serve's schema endpoint returns.

Moved here from `sldb.cli.serve.schema`, which re-exports these names.
"""

from __future__ import annotations

from typing import Any

from sldb.api.schema.field_kinds import enum_values, field_kind, unwrap_annotation


def field_descriptor(name: str, field: Any) -> dict[str, Any]:
    """JSON-ready descriptor `{name, kind, required[, enum]}` of a pydantic field.

    Args:
        name: Field name.
        field: The pydantic `FieldInfo`.

    Returns:
        The descriptor; `enum` is present only for Literal/Enum fields.
    """
    annotation = unwrap_annotation(field.annotation)
    data = {"name": name, "kind": field_kind(annotation), "required": field.is_required()}
    return add_enum_values(data, annotation)


def add_enum_values(data: dict[str, Any], annotation: Any) -> dict[str, Any]:
    """Add the allowed `enum` values to a descriptor when the annotation has them."""
    values = enum_values(annotation)
    if values is not None:
        data["enum"] = values
    return data
