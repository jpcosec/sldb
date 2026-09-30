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
from sldb.api.schema.store_schema import StoreSchema
from sldb.api.schema.unavailable_model import UnavailableModel
from sldb.cli.model_utils import resolve_model_ref
from sldb.models.structured_doc import StructuredNLDoc
from sldb.store.io import load_store_index


def schema_models(store_path: Path, pythonpath: str) -> list[dict[str, Any]]:
    store_index = load_store_index(store_path)
    return [schema_model(entry, pythonpath) for entry in store_index.models]


def store_schema(store_path: Path, pythonpath: str) -> StoreSchema:
    """Describe every registered model, declaring the ones that cannot load.

    A model whose module does not import must not take the listing down: a store
    with twenty models and one broken has nineteen describable models and one
    reportable failure, not zero models.

    Args:
        store_path: An already resolved ``.sldb`` directory.
        pythonpath: Directory to import the model modules from.

    Returns:
        The describable models and the unavailable ones with their reasons.
    """
    described: list[dict[str, Any]] = []
    unavailable: list[UnavailableModel] = []
    for entry in load_store_index(store_path).models:
        _describe_into(entry, pythonpath, described, unavailable)
    return StoreSchema(models=described, unavailable=unavailable)


def _describe_into(entry: Any, pythonpath: str, described: list[dict[str, Any]], unavailable: list[UnavailableModel]) -> None:
    """Describe one model into ``described``, or record why it could not be.

    Args:
        entry: The store index entry of the model.
        pythonpath: Directory to import the model module from.
        described: Accumulator of successful descriptors, mutated in place.
        unavailable: Accumulator of failures, mutated in place.
    """
    try:
        described.append(schema_model(entry, pythonpath))
    except Exception as exc:  # noqa: BLE001 - one broken model must not hide the rest
        unavailable.append(UnavailableModel(model=entry.name, model_ref=entry.model_ref, error=str(exc)))


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