"""The files a move touches and the Markdown files whose links it may rewrite."""

from __future__ import annotations

import os
from pathlib import Path

from sldb.api.documents.move_path_remap import Remap
from sldb.ports.git import unignored_files


def moved_entries(root: Path, remap: Remap) -> tuple[list[str], list[str]]:
    """`(directories, files)` under the moved path, project-relative and sorted; the path itself
    is the one file of a file move, the first directory of a directory move."""
    if not remap.is_dir:
        return [], [remap.old]
    dirs, files = [remap.old], []
    for here, names, leaves in os.walk(root / remap.old):
        base = Path(here).relative_to(root).as_posix()
        dirs += [f"{base}/{n}" for n in names if not (Path(here) / n).is_symlink()]
        files += [f"{base}/{n}" for n in leaves + [n for n in names if (Path(here) / n).is_symlink()]]
    return sorted(dirs), sorted(files)


def markdown_files(root: Path, skip: list[Path]) -> list[str]:
    """Every Markdown file of the repo (git's, untracked ones included, ignored ones not), project-relative."""
    found = [p for p in _candidates(root) if p.endswith((".md", ".markdown"))]
    paths = [p for p in found if (root / p).is_file() and not (root / p).is_symlink()]
    return sorted(p for p in paths if not any(s in (root / p).parents for s in skip))


def _candidates(root: Path) -> list[str]:
    git = _git_files(root)
    if git is not None:
        return git
    return [p.relative_to(root).as_posix() for p in root.rglob("*.md") if ".git" not in p.parts]


def _git_files(root: Path) -> list[str] | None:
    """git's listing of the repo (tracked and untracked, not ignored), or None outside a repo or without git."""
    listed = unignored_files(root)
    return None if listed is None else [p for p in listed.decode("utf-8", "surrogateescape").split("\0") if p]
