"""Set or delete a value inside a document payload by a dotted path, in place.

Moved here from `sldb.cli.dict_utils`, which re-exports these names.
"""

from __future__ import annotations

from typing import Any

from sldb.api.documents.payload_path_reading import _split_path


def _deep_set_dict(target: dict[str, Any], part: str, create: bool, path: str) -> Any:
    """Step into a dict key, creating an empty dict there when allowed."""
    if part not in target:
        if not create:
            raise KeyError(path)
        target[part] = {}
    return target[part]


def _deep_set_traverse(target: Any, parts: list[str], create: bool, path: str) -> Any:
    """The container that holds the path's last segment."""
    for part in parts[:-1]:
        if isinstance(target, dict):
            target = _deep_set_dict(target, part, create, path)
        elif isinstance(target, list):
            target = target[int(part)]
        else:
            raise KeyError(path)
    return target


def _deep_set_leaf(target: Any, leaf: str, new_value: Any, create: bool, path: str) -> None:
    """Assign the last segment in its container."""
    if isinstance(target, dict):
        if not create and leaf not in target:
            raise KeyError(path)
        target[leaf] = new_value
        return
    if isinstance(target, list):
        target[int(leaf)] = new_value
        return
    raise KeyError(path)


def deep_set(payload: Any, path: str, new_value: Any, create: bool = False) -> Any:
    """Assign the value at a dotted path, in place.

    Args:
        payload: A document payload (nested dicts and lists).
        path: Dotted path; numeric segments index into lists.
        new_value: The value to assign.
        create: Create missing dict keys (intermediate ones as empty dicts).

    Returns:
        The same payload, mutated.

    Raises:
        KeyError: When a key is missing and `create` is False.
        IndexError: When a list index is out of range.
    """
    parts = _split_path(path)
    target = _deep_set_traverse(payload, parts, create, path)
    _deep_set_leaf(target, parts[-1], new_value, create, path)
    return payload


def _delete_leaf(target: Any, leaf: str, path: str) -> None:
    """Remove the last segment from its container (a missing dict key is ignored)."""
    if isinstance(target, dict):
        target.pop(leaf, None)
    elif isinstance(target, list):
        target.pop(int(leaf))
    else:
        raise KeyError(path)


def deep_delete(payload: Any, path: str) -> Any:
    """Remove the value at a dotted path, in place.

    Args:
        payload: A document payload (nested dicts and lists).
        path: Dotted path; numeric segments index into lists.

    Returns:
        The same payload, mutated.

    Raises:
        KeyError: When an intermediate key is missing.
        IndexError: When a list index is out of range.
    """
    parts = _split_path(path)
    target = payload
    for part in parts[:-1]:
        target = target[part] if isinstance(target, dict) else target[int(part)]
    _delete_leaf(target, parts[-1], path)
    return payload
