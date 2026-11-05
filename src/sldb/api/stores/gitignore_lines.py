"""The lines sldb owns in the project's `.gitignore`: `.sldb_cache/` in, `.sldb/core/` and `.sldb/runtime/` out.

The file edited is the one at the project root, the parent of `.sldb/`. `stores init` adds the
cache line when no line already says it; `stores migrate-layout` also drops the two lines that
ignored the old split. Every other line, comments included, is kept as it is: this file is
the owner's, and sldb only tends its own three patterns.
"""

from __future__ import annotations

from pathlib import Path

CACHE_LINE = ".sldb_cache/"
_OLD_SPLIT = frozenset({".sldb/core", ".sldb/runtime"})


def pattern_of(line: str) -> str | None:
    """A line's pattern without leading or trailing slashes; None for a blank line or a comment."""
    text = line.strip()
    if not text or text.startswith("#"):
        return None
    return text.strip("/")


def ensure_cache_ignored(gitignore: Path) -> bool:
    """Add `.sldb_cache/` unless a line already names it; True when the line was added."""
    lines = _lines(gitignore)
    if any(pattern_of(line) == CACHE_LINE.strip("/") for line in lines):
        return False
    _write(gitignore, [*lines, CACHE_LINE])
    return True


def rewrite_for_split(gitignore: Path) -> dict:
    """Drop the lines ignoring `.sldb/core/` or `.sldb/runtime/`, add `.sldb_cache/` where the
    first of them was (at the end when there was none), keep everything else verbatim."""
    kept, removed, slot = _without_old_split(_lines(gitignore))
    added = not any(pattern_of(line) == CACHE_LINE.strip("/") for line in kept)
    if added:
        kept.insert(len(kept) if slot is None else slot, CACHE_LINE)
    if removed or added:
        _write(gitignore, kept)
    return {"path": str(gitignore), "removed": removed, "added": added}


def _without_old_split(lines: list[str]) -> tuple[list[str], list[str], int | None]:
    """`(kept, removed, slot)`: the lines kept, the ones dropped, and where the first dropped one was."""
    kept, removed, slot = [], [], None
    for line in lines:
        if pattern_of(line) in _OLD_SPLIT:
            removed.append(line)
            slot = len(kept) if slot is None else slot
        else:
            kept.append(line)
    return kept, removed, slot


def _lines(gitignore: Path) -> list[str]:
    return gitignore.read_text(encoding="utf-8").splitlines() if gitignore.is_file() else []


def _write(gitignore: Path, lines: list[str]) -> None:
    gitignore.write_text("\n".join(lines) + "\n", encoding="utf-8")
