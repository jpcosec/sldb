"""The files a `code_facts` call reads: the requested paths checked against `root`, directories expanded."""

from __future__ import annotations

import os
from pathlib import Path

from sldb.code.files import _SKIP, find_files
from sldb.code.runtime import GRAMMARS


def requested_files(root: Path, paths: list[str] | None) -> list[str]:
    """Relative paths with `/`, unique, sorted like `find_files`; raises `ValueError` on a bad path."""
    rels = list(dict.fromkeys(checked_path(root, p) for p in (["."] if paths is None else paths)))
    files: set[str] = set()
    for rel in rels:
        files.update(_expand(root, rel) if (root / rel).is_dir() else [rel])
    return sorted(files, key=lambda r: tuple(r.split("/")))


def checked_path(root: Path, path: str) -> str:
    """`path` relative to `root` with `/`; absolute, outside `root` or missing raises `ValueError` naming it."""
    if Path(path).is_absolute():
        raise ValueError(f"{path}: absolute path; code_facts paths are relative to root")
    base, full = root.resolve(), (root / path).resolve()
    if not full.is_relative_to(base):
        raise ValueError(f"{path}: outside root {root}")
    if not full.exists():
        raise ValueError(f"{path}: no such file or directory under {root}")
    return full.relative_to(base).as_posix()


def _expand(root: Path, rel: str) -> list[str]:
    """The source files under a directory: what `find_files` reads plus those whose grammar is missing."""
    prefix = "" if rel == "." else rel + "/"
    return [prefix + f for f in find_files(root / rel) + _without_runtime(root / rel)]


def _without_runtime(base: Path) -> list[str]:
    """Files with a known source extension that `find_files` leaves out because the grammar is not installed."""
    out = []
    for at, dirs, names in os.walk(base):
        dirs[:] = [d for d in dirs if d not in _SKIP]
        out += [os.path.relpath(os.path.join(at, n), base).replace(os.sep, "/") for n in names if os.path.splitext(n)[1] in GRAMMARS]
    return out
