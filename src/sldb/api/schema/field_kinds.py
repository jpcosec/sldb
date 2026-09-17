"""Classify a model field's annotation into the kinds forms and schemas present.

Moved here from `sldb.cli.serve.schema` (and `annotation_name` from `sldb.cli.graph_ops.utils`),
which re-export these names.
"""

from __future__ import annotations

from enum import Enum
from types import UnionType
from typing import Any, Literal, Union, get_args, get_origin


def annotation_name(annotation: Any) -> str:
    """Readable name of a type annotation ("Any" when absent)."""
    if annotation is None:
        return "Any"
    if isinstance(annotation, str):
        return annotation
    return getattr(annotation, "__name__", repr(annotation))


def unwrap_annotation(annotation: Any) -> Any:
    """The single non-None member of an Optional annotation; any other annotation as is."""
    origin = get_origin(annotation)
    if origin not in (UnionType, Union):
        return annotation
    args = [arg for arg in get_args(annotation) if arg is not type(None)]
    return args[0] if len(args) == 1 else annotation


def field_kind(annotation: Any) -> str:
    """Kind of an unwrapped annotation: enum, a list kind, or a scalar kind."""
    if enum_values(annotation) is not None:
        return "enum"
    if get_origin(annotation) is list:
        return list_kind(get_args(annotation))
    return scalar_kind(annotation)


def list_kind(args: tuple[Any, ...]) -> str:
    """Kind of a list annotation from its item type: stringlist, enumlist or list."""
    item_type = unwrap_annotation(args[0]) if args else Any
    if item_type is str:
        return "stringlist"
    return "enumlist" if enum_values(item_type) is not None else "list"


def scalar_kind(annotation: Any) -> str:
    """Kind of a scalar annotation: string, boolean, integer, number, object or unknown."""
    mapping = {str: "string", bool: "boolean", int: "integer", float: "number", dict: "object"}
    return mapping.get(annotation, "unknown")


def enum_values(annotation: Any) -> list[Any] | None:
    """Allowed values of a Literal or Enum annotation; None for any other annotation."""
    if get_origin(annotation) is Literal:
        return list(get_args(annotation))
    if not isinstance(annotation, type):
        return None
    if not issubclass(annotation, Enum):
        return None
    return [member.value for member in annotation]
