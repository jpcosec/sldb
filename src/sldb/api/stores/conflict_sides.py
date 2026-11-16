"""Both sides of a file git left with conflict markers, and the by-name union of two lists.

What the hand procedure did ("take a side"), done for both sides at once: outside the hunks
the text is common, inside each hunk `ours` keeps the first part and `theirs` the last (a diff3
base part, after `|||||||`, is dropped). The merge driver and `stores rebuild-index` share it."""

from __future__ import annotations

from typing import Any

_ROLE = {"<<<<<<<": "ours", "|||||||": "base", "=======": "theirs", ">>>>>>>": "both"}


def conflict_sides(text: str) -> tuple[str, str]:
    """`(ours, theirs)`: the text each branch had, rebuilt from the conflict hunks."""
    sides: dict[str, list[str]] = {"ours": [], "theirs": []}
    role = "both"
    for line in text.splitlines(keepends=True):
        marker = line[:7]
        if marker in _ROLE:
            role = _ROLE[marker]
            continue
        _keep(sides, role, line)
    return "".join(sides["ours"]), "".join(sides["theirs"])


def _keep(sides: dict[str, list[str]], role: str, line: str) -> None:
    for side in (("ours", "theirs") if role == "both" else (role,)):
        if side in sides:
            sides[side].append(line)


def union_by(ours: list[Any], theirs: list[Any], key: str) -> list[Any]:
    """`ours`, then each item of `theirs` whose `key` none of `ours` has (ours wins a tie)."""
    seen = {_key(item, key) for item in ours}
    return list(ours) + [item for item in theirs if _key(item, key) not in seen]


def _key(item: Any, key: str) -> Any:
    return item.get(key) if isinstance(item, dict) else item
