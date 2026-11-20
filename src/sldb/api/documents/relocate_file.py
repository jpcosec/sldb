"""Move a file on disk, through `git mv` when git versions it so git records a rename."""

from __future__ import annotations

import subprocess
from pathlib import Path


def git_tracks(path: Path) -> bool:
    """True when `path` (a file or a directory holding some) is in the git index of its checkout."""
    if not path.exists() and not path.is_symlink():
        return False
    return _git(path.parent, "ls-files", "--error-unmatch", "--", path.name).returncode == 0


def relocate_file(source: Path, target: Path) -> None:
    """Move `source` to `target` (its parent is created); `git mv` when git versions `source`,
    else a plain rename, and a rename too when git refuses (an unmerged path, say)."""
    target.parent.mkdir(parents=True, exist_ok=True)
    if git_tracks(source) and _git(source.parent, "mv", "--", str(source), str(target)).returncode == 0:
        return
    source.rename(target)


def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False)
    except OSError:  # no git binary
        return subprocess.CompletedProcess(args, 1, "", "git is not available")
