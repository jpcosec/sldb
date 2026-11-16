"""A derived index (`core/store_index.yaml`, `core/models/*.yaml`) that git left with conflict
markers, or that no longer parses, fails with the one command that regenerates it instead of a
bare YAML or validation error: `sldb stores rebuild-index` rebuilds both levels from the shards."""

from __future__ import annotations

from pathlib import Path
from typing import Callable, TypeVar

from sldb.core.exceptions import SLDBStoreError

T = TypeVar("T")
CONFLICT_PREFIXES = ("<<<<<<<", "|||||||", "=======", ">>>>>>>")


def has_conflict_markers(text: str) -> bool:
    """Whether a line of `text` opens, splits or closes a git conflict hunk."""
    return any(line.startswith(CONFLICT_PREFIXES) for line in text.splitlines())


def unmerged_index_error(path: Path) -> SLDBStoreError:
    """The error every reader of a derived index raises when git could not merge it."""
    return SLDBStoreError(f"{path} is a derived index that git could not merge: run `sldb stores rebuild-index` (and `sldb stores merge-driver --install` once per clone)")


def guarded_load(path: Path, loader: Callable[[], T]) -> T:
    """`loader()`, or the rebuild-index error when `path` holds conflict markers or does not parse.
    A missing file keeps its own error: that is not a merge problem."""
    if path.is_file() and has_conflict_markers(path.read_text(encoding="utf-8", errors="replace")):
        raise unmerged_index_error(path)
    try:
        return loader()
    except (FileNotFoundError, SLDBStoreError):
        raise
    except Exception as exc:  # yaml.YAMLError, a pydantic ValidationError, a TypeError on a non-mapping
        raise unmerged_index_error(path) from exc
