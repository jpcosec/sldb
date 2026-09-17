"""Read a value inside a document payload by a dotted path (`items.0.name`).

Moved here from `sldb.cli.dict_utils`, which re-exports these names.
"""

from __future__ import annotations

from typing import Any


def _split_path(path: str) -> list[str]:
    """The non-empty segments of a dotted path; an empty path is a missing key."""
    parts = [part for part in path.split(".") if part]
    if not parts:
        raise KeyError(path)
    return parts


def _get_part(value: Any, part: str, path: str) -> Any:
    """Step into a dict key or a list index."""
    if isinstance(value, dict):
        if part not in value:
            raise KeyError(path)
        return value[part]
    if isinstance(value, list):
        return value[int(part)]
    raise KeyError(path)


def deep_get(payload: Any, path: str) -> Any:
    """The value at a dotted path; numeric segments index into lists.

    Args:
        payload: A document payload (nested dicts and lists).
        path: Dotted path such as `address.city` or `items.0.name`.

    Returns:
        The value found at the path.

    Raises:
        KeyError: When a key is missing or a scalar is stepped into.
        IndexError: When a list index is out of range.
    """
    value = payload
    for part in _split_path(path):
        value = _get_part(value, part, path)
    return value


def ensure_list(payload: Any, path: str) -> list[Any]:
    """The list at a dotted path.

    Raises:
        KeyError: When the path does not exist.
        TypeError: When the value there is not a list.
    """
    value = deep_get(payload, path)
    if not isinstance(value, list):
        raise TypeError(f"Target '{path}' is not a list field.")
    return value
