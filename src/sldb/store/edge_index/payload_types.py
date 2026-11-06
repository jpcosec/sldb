"""What the payload projection keeps: a scalar (str, int, float, bool, null) or a list of them.

Values are read as the extracted payload holds them (JSON mode), so a date or an enum already
arrives as a string. Annotations are read for `__indexed__` and for the fields a payload filter
may name: a type whose JSON form is a scalar (enums, dates, UUIDs, Literals of scalars) counts
as one; dicts, models and lists of anything else do not.
"""

from __future__ import annotations

import datetime
import enum
import types
import typing
import uuid
from typing import Any

_SCALAR_TYPES = (str, int, float, bool, type(None), enum.Enum, datetime.date, datetime.time, uuid.UUID)
_UNIONS = (typing.Union, types.UnionType)
_SEQUENCES = (list, tuple, set, frozenset)


def is_scalar(value: Any) -> bool:
    """A JSON scalar: str, int, float, bool or None."""
    return value is None or isinstance(value, (str, int, float, bool))


def is_projectable(value: Any) -> bool:
    """A scalar, or a list (possibly empty) of scalars."""
    return is_scalar(value) or (isinstance(value, list) and all(is_scalar(v) for v in value))


def projectable_annotation(tp: Any) -> bool:
    """Whether a field declared with this annotation always holds a scalar or a list of them."""
    tp = _bare(tp)
    if typing.get_origin(tp) in _UNIONS:
        return all(projectable_annotation(a) for a in typing.get_args(tp))
    if typing.get_origin(tp) in _SEQUENCES:
        items = [a for a in typing.get_args(tp) if a is not Ellipsis]
        return bool(items) and all(scalar_annotation(a) for a in items)
    return scalar_annotation(tp)


def scalar_annotation(tp: Any) -> bool:
    """Whether the annotation's JSON form is a scalar."""
    tp = _bare(tp)
    origin = typing.get_origin(tp)
    if origin is typing.Literal:
        return all(is_scalar(a) or isinstance(a, enum.Enum) for a in typing.get_args(tp))
    if origin in _UNIONS:
        return all(scalar_annotation(a) for a in typing.get_args(tp))
    return isinstance(tp, type) and issubclass(tp, _SCALAR_TYPES)


def opaque_annotation(tp: Any) -> bool:
    """`Any` (or a bare `object`): what it holds is only known per value."""
    return _bare(tp) in (Any, object)


def _bare(tp: Any) -> Any:
    """The annotation without `Annotated[...]` metadata."""
    while typing.get_origin(tp) is typing.Annotated:
        tp = typing.get_args(tp)[0]
    return tp
