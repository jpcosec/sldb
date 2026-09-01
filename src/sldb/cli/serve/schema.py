from __future__ import annotations

from enum import Enum
from pathlib import Path
from types import UnionType
from typing import Any, Literal, Union, get_args, get_origin

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


def field_descriptor(name: str, field: Any) -> dict[str, Any]:
    annotation = unwrap_annotation(field.annotation)
    data = {"name": name, "kind": field_kind(annotation), "required": field.is_required()}
    return add_enum_values(data, annotation)


def add_enum_values(data: dict[str, Any], annotation: Any) -> dict[str, Any]:
    values = enum_values(annotation)
    if values is not None:
        data["enum"] = values
    return data


def unwrap_annotation(annotation: Any) -> Any:
    origin = get_origin(annotation)
    if origin not in (UnionType, Union):
        return annotation
    args = [arg for arg in get_args(annotation) if arg is not type(None)]
    return args[0] if len(args) == 1 else annotation


def field_kind(annotation: Any) -> str:
    if enum_values(annotation) is not None:
        return "enum"
    if get_origin(annotation) is list:
        return list_kind(get_args(annotation))
    return scalar_kind(annotation)


def list_kind(args: tuple[Any, ...]) -> str:
    item_type = unwrap_annotation(args[0]) if args else Any
    if item_type is str:
        return "stringlist"
    return "enumlist" if enum_values(item_type) is not None else "list"


def scalar_kind(annotation: Any) -> str:
    mapping = {str: "string", bool: "boolean", int: "integer", float: "number", dict: "object"}
    return mapping.get(annotation, "unknown")


def enum_values(annotation: Any) -> list[Any] | None:
    if get_origin(annotation) is Literal:
        return list(get_args(annotation))
    if not isinstance(annotation, type):
        return None
    if not issubclass(annotation, Enum):
        return None
    return [member.value for member in annotation]
