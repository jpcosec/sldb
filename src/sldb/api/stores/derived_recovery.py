"""The data a derived index held before git broke it, read without trusting any hash in it.

A file that parses is taken as is. One with conflict markers becomes the union of its two
sides (`conflict_sides`), lists by name. One that parses on neither path falls back to the
version the last commit holds (`git show HEAD:<path>`). The caller recomputes every hash."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from sldb.api.stores.conflict_sides import conflict_sides
from sldb.core.exceptions import SLDBStoreError
from sldb.ports.git import committed_file
from sldb.store.io.derived_guard import has_conflict_markers
from sldb.store.io.utils import yaml_load

Merge = Callable[[dict, dict], dict]


def recovered_data(path: Path, merge: Merge) -> tuple[dict[str, Any], bool]:
    """`(data, repaired)`: what `path` declares, and whether it had to be repaired."""
    text = path.read_text(encoding="utf-8", errors="replace")
    if has_conflict_markers(text):
        merged = _merged_sides(text, merge)
        if merged is not None:
            return merged, True
    data = _parsed(text)
    if data is not None:
        return data, False
    return _committed(path), True


def _merged_sides(text: str, merge: Merge) -> dict[str, Any] | None:
    ours, theirs = (_parsed(side) for side in conflict_sides(text))
    if ours is None or theirs is None:
        return ours or theirs
    return merge(ours, theirs)


def _parsed(text: str) -> dict[str, Any] | None:
    try:
        data = yaml_load(text)
    except Exception:
        return None
    return data if isinstance(data, dict) and not has_conflict_markers(text) else None


def _committed(path: Path) -> dict[str, Any]:
    """The file as HEAD has it; the error says so when there is no such version either."""
    text = committed_file(path)
    data = _parsed(text) if text is not None else None
    if data is None:
        raise SLDBStoreError(f"{path} does not parse and HEAD has no readable version of it: restore it from git (`git checkout <branch> -- {path}`) and run `sldb stores rebuild-index` again")
    return data
