"""Describe one field of a model class for forms, schemas and the edge index's field nodes.

Pure pydantic: it lives with the models so the store (which emits a node per field) and the
operations layer can both use it. It was in `sldb.api.schema`, and the store imported it late
to dodge the cycle (pending R4 in contracts/layers.toml).
"""

from __future__ import annotations

from pydantic.fields import FieldInfo

from sldb.models.field_schema.description import FieldDescription
from sldb.models.field_schema.descriptor import field_descriptor


def describe_field(name: str, field: FieldInfo) -> FieldDescription:
    """Describe one pydantic field: kind, requiredness, enum values, annotation and description.

    Args:
        name: Field name.
        field: The field's `FieldInfo`, e.g. `Model.model_fields[name]`.

    Returns:
        The field description.
    """
    annotation = getattr(field.annotation, "__name__", repr(field.annotation))
    return FieldDescription(**field_descriptor(name, field), annotation=annotation)
