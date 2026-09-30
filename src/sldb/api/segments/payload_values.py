"""Read a field's typed value and kind out of a payload by segment path.

Segment paths use the ``sldb fields`` space (``tags/0``, ``steps/2/title``), so
lookups walk a payload one slash-separated part at a time. The kind comes from
:mod:`sldb.api.schema.field_kinds` on the root field, then narrows for list
items: one item of a ``stringlist`` is a ``string``, not a list.
"""

from __future__ import annotations

from typing import Any

from sldb.api.schema.field_kinds import field_kind, unwrap_annotation

ITEM_KINDS = {"stringlist": "string", "enumlist": "enum"}


def value_at(payload: Any, path: str) -> Any:
    """The value ``path`` addresses inside ``payload``, or None when absent.

    Args:
        payload: The document payload to read from.
        path: Slash-separated field address, such as ``steps/2/title``.

    Returns:
        The addressed value, or None when any part of the path is missing.
    """
    current = payload
    for part in [p for p in path.split("/") if p]:
        current = _descend(current, part)
        if current is _MISSING:
            return None
    return current


_MISSING = object()


def _descend(current: Any, part: str) -> Any:
    """One step of a path walk into a mapping or a sequence.

    Args:
        current: The value reached so far.
        part: The next path part, an index for sequences.

    Returns:
        The nested value, or a sentinel when the step does not apply.
    """
    if isinstance(current, list) and part.isdigit() and int(part) < len(current):
        return current[int(part)]
    if isinstance(current, dict) and part in current:
        return current[part]
    return _MISSING


def kind_at(model_type: type, path: str) -> str:
    """The input kind of the field ``path`` addresses in ``model_type``.

    Args:
        model_type: The ``StructuredNLDoc`` subclass owning the field.
        path: Slash-separated field address, such as ``tags/0``.

    Returns:
        A kind from ``sldb.api.schema.field_kinds``, or ``"unknown"``.
    """
    parts = path.split("/")
    info = model_type.model_fields.get(parts[0])
    if info is None:
        return "unknown"
    kind = field_kind(unwrap_annotation(info.annotation))
    if len(parts) >= 2 and parts[1].isdigit():
        return ITEM_KINDS.get(kind, "unknown")
    return kind
