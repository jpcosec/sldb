"""Move a file on disk, through `git mv` when git versions it so git records a rename."""

from __future__ import annotations

from pathlib import Path

from sldb.ports.git import git_ok


def git_tracks(path: Path) -> bool:
    """True when `path` (a file or a directory holding some) is in the git index of its checkout."""
    if not path.exists() and not path.is_symlink():
        return False
    return git_ok(path.parent, "ls-files", "--error-unmatch", "--", path.name)


def relocate_file(source: Path, target: Path) -> None:
    """Move `source` to `target` (its parent is created); `git mv` when git versions `source`,
    else a plain rename, and a rename too when git refuses (an unmerged path, say)."""
    target.parent.mkdir(parents=True, exist_ok=True)
    if git_tracks(source) and git_ok(source.parent, "mv", "--", str(source), str(target)):
        return
    source.rename(target)
