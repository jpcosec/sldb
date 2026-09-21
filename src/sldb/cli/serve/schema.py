"""GET /schema payload: one model entry per registered model.

Each entry carries the field descriptors plus the model-level graph metadata
declared by the model class (``__containment__``, ``__references__``,
``__semantics__``, ``__template__``). Models that do not declare a dunder
inherit the ``StructuredNLDoc`` defaults, never ``None``.
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Any

from pydantic_core import PydanticUndefined

from sldb.api.schema.field_descriptor import add_enum_values, field_descriptor  # noqa: F401 - moved to sldb.api.schema
from sldb.api.schema.field_kinds import enum_values, field_kind, list_kind, scalar_kind, unwrap_annotation  # noqa: F401 - moved to sldb.api.schema
from sldb.cli.model_utils import resolve_model_ref
from sldb.models.structured_doc import StructuredNLDoc
from sldb.store.io import load_store_index


def schema_models(store_path: Path, pythonpath: str) -> list[dict[str, Any]]:
    store_index = load_store_index(store_path)
    return [schema_model(entry, pythonpath) for entry in store_index.models]


def schema_model(entry: Any, pythonpath: str) -> dict[str, Any]:
    model_type = resolve_model_ref(entry.model_ref, pythonpath)
    return {
        "id": entry.name,
        "model_ref": entry.model_ref,
        "fields": field_descriptors(model_type),
        "containment": dunder(model_type, "__containment__", StructuredNLDoc.__containment__),
        "references": dunder(model_type, "__references__", StructuredNLDoc.__references__),
        "semantics": dunder(model_type, "__semantics__", StructuredNLDoc.__semantics__),
        "template": dunder(model_type, "__template__", StructuredNLDoc.__template__),
    }


def dunder(model_type: type, name: str, fallback: Any) -> Any:
    """Class-level dunder of the model, or the StructuredNLDoc default."""
    value = getattr(model_type, name, fallback)
    return fallback if value is None else value


def field_descriptors(model_type: type) -> list[dict[str, Any]]:
    return [field_descriptor_with_default(name, field) for name, field in model_type.model_fields.items()]


def field_descriptor_with_default(name: str, field: Any) -> dict[str, Any]:
    """Field descriptor plus the declared default when the field has one.

    ``PydanticUndefined`` (required or ``default_factory``) omits the key;
    enum defaults serialize as their value.
    """
    descriptor = field_descriptor(name, field)
    if field.is_required() or field.default is PydanticUndefined:
        return descriptor
    default = field.default.value if isinstance(field.default, Enum) else field.default
    descriptor["default"] = default
    return descriptor