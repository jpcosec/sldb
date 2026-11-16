"""The source files a scan reads: every `.py`, plus `.ts`, `.tsx`, `.js` and `.jsx` when their grammar is installed."""

from __future__ import annotations

import os
from pathlib import Path

from sldb.code.runtime import TS_SUFFIXES, available

_SKIP = {"__pycache__", "node_modules"}


def find_files(root: Path) -> list[str]:
    """Relative paths with `/`, sorted by their parts; `__pycache__` and `node_modules` are not walked."""
    suffixes = (".py",) + (TS_SUFFIXES if available(".ts") else ())
    out = []
    for base, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in _SKIP)
        out += [os.path.relpath(os.path.join(base, f), root).replace(os.sep, "/") for f in files if f.endswith(suffixes)]
    return sorted(out, key=lambda r: tuple(r.split("/")))
