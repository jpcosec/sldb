"""Reading a tracked source without following it out of the project (inbox 9c9dac6b, SEGURIDAD
live_stale).

A tracked path is joined to the project root and read; a symlink there (or a directory on the
way that resolves elsewhere) would send the read outside the project, before any consumer of
the store could apply its own guards. A read of the index, or a check of the store, therefore
reads only a regular file whose resolved path stays inside the root: anything else is named,
not read. Its own module, out of ``hashing.py``: computing a hash and deciding whether a file
may be opened are two jobs (``tests/test_clean_code_rules.py``).
"""

from __future__ import annotations

import os
import stat
from pathlib import Path

#: The path resolves outside the project root (a symlink, or a directory on the way, escapes).
OUTSIDE_ROOT = "outside-root"
#: The path is a symlink (even one pointing inside the root): sldb does not follow it.
SYMLINK = "symlink"


def unreadable_reason(root: Path, path: Path) -> str | None:
    """Why `path` must not be read for the store rooted at `root`, or None when it may be (or
    is missing: a missing file is the caller's own verdict). Only `lstat` and `resolve` run;
    the file itself is never opened."""
    try:
        st = path.lstat()
    except OSError:
        return None
    if not path.resolve().is_relative_to(root.resolve()):
        return OUTSIDE_ROOT
    if stat.S_ISLNK(st.st_mode):
        return SYMLINK
    return None


def source_stat(path: Path) -> list[int] | None:
    """`[mtime_ns, size]` of the file itself (never what a symlink points to); None when absent."""
    try:
        st = path.lstat()
    except OSError:
        return None
    return [st.st_mtime_ns, st.st_size]


def read_source_text(path: Path) -> str:
    """The file's text, opened without following a symlink in its last component (`O_NOFOLLOW`),
    so a file swapped for a symlink after `unreadable_reason` said yes is still not followed."""
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    with open(fd, encoding="utf-8") as f:
        return f.read()
