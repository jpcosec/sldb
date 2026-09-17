from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.schema.field_descriptor import add_enum_values, field_descriptor  # noqa: F401 - moved to sldb.api.schema
from sldb.api.schema.field_kinds import enum_values, field_kind, list_kind, scalar_kind, unwrap_annotation  # noqa: F401 - moved to sldb.api.schema
from sldb.cli.model_utils import resolve_model_ref
from sldb.store.io import load_store_index


def schema_models(store_path: Path, pythonpath: str) -> list[dict[str, Any]]:
    store_index = load_store_index(store_path)
    return [schema_model(entry, pythonpath) for entry in store_index.models]


def schema_model(entry: Any, pythonpath: str) -> dict[str, Any]:
    model_type = resolve_model_ref(entry.model_ref, pythonpath)
    return {"id": entry.name, "model_ref": entry.model_ref, "fields": field_descriptors(model_type)}


def field_descriptors(model_type: type) -> list[dict[str, Any]]:
    return [field_descriptor(name, field) for name, field in model_type.model_fields.items()]
